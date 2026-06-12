#!/usr/bin/env python3
"""
OCR Engine: batch-process images and PDFs, with quality scoring.

Usage:
  python ocr_engine.py <input_dir> <output_dir> [--lang chi_sim+eng] [--workers 4]
  python ocr_engine.py <input_dir> <output_dir> --scan-only   # just quality scan existing results
"""
import pytesseract
import os, sys, json, re, subprocess, argparse
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ─── Tesseract setup ───────────────────────────────────────────
def _find_tesseract():
    """Find tesseract binary and tessdata on this system."""
    candidates = [
        r'C:/Program Files/Tesseract-OCR/tesseract.exe',
        r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe',
        '/usr/bin/tesseract',
        '/usr/local/bin/tesseract',
    ]
    for path in candidates:
        if os.path.exists(path):
            return path

    # Try PATH
    import shutil
    found = shutil.which('tesseract')
    if found:
        return found

    sys.exit("ERROR: tesseract not found. Install from: https://github.com/tesseract-ocr/tesseract")

def _find_tessdata():
    """Find or create a writable tessdata directory."""
    candidates = [
        os.path.expanduser('~/AppData/Local/tessdata'),
        os.path.expanduser('~/.local/share/tessdata'),
        '/usr/share/tesseract-ocr/4.00/tessdata',
        '/usr/share/tesseract-ocr/tessdata',
    ]
    for path in candidates:
        if os.path.isdir(path) and os.access(path, os.W_OK):
            eng = os.path.join(path, 'eng.traineddata')
            if os.path.exists(eng):
                return path

    # Create user tessdata
    user_dir = os.path.expanduser('~/AppData/Local/tessdata')
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def setup_tesseract():
    """Configure tesseract and return (binary_path, tessdata_dir)."""
    tesseract_bin = _find_tesseract()
    tessdata_dir = _find_tessdata()
    pytesseract.pytesseract.tesseract_cmd = tesseract_bin
    os.environ['TESSDATA_PREFIX'] = tessdata_dir
    return tesseract_bin, tessdata_dir

# ─── OCR Functions ─────────────────────────────────────────────
def ocr_image(path, lang='chi_sim+eng', preprocess='auto'):
    """
    OCR a single image. preprocess modes:
    - 'auto': try multiple strategies, return best
    - 'simple': grayscale only
    - 'enhanced': contrast + sharpen
    """
    try:
        img = Image.open(path)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        w, h = img.size
        if w > 1400 or h > 1800:
            ratio = min(1400/w, 1800/h)
            img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)

        gray = img.convert('L')

        if preprocess == 'simple':
            return pytesseract.image_to_string(gray, lang=lang, config='--psm 6').strip()

        if preprocess == 'enhanced':
            enhanced = ImageEnhance.Contrast(gray).enhance(1.8)
            sharp = enhanced.filter(ImageFilter.SHARPEN)
            return pytesseract.image_to_string(sharp, lang=lang, config='--psm 6').strip()

        # 'auto': try multiple strategies
        best_text = ""
        best_score = 0
        for name, processed in [
            ('gray', gray),
            ('contrast', ImageEnhance.Contrast(gray).enhance(1.5)),
            ('contrast2', ImageEnhance.Contrast(gray).enhance(2.0)),
            ('sharp', gray.filter(ImageFilter.SHARPEN)),
            ('median3', gray.filter(ImageFilter.MedianFilter(3))),
            ('equalize', ImageOps.equalize(gray)),
            ('smooth_sharp', gray.filter(ImageFilter.SMOOTH_MORE).filter(ImageFilter.SHARPEN)),
        ]:
            for psm in ['--psm 6', '--psm 4']:
                try:
                    text = pytesseract.image_to_string(processed, lang=lang, config=psm)
                    cjk_count = len(re.findall(r'[一-鿿]', text))
                    total = len(text.strip())
                    # Prefer balanced Chinese ratio and length
                    score = cjk_count * 2 + min(total, 500)
                    if score > best_score:
                        best_score = score
                        best_text = text.strip()
                except Exception:
                    pass
        return best_text
    except Exception as e:
        return f"[OCR ERROR: {e}]"

def ocr_pdf(path, lang='chi_sim+eng', force_image_ocr=False):
    """Extract text from PDF. Falls back: pdftotext → PyMuPDF → pdftoppm+OCR."""
    text = ""

    if not force_image_ocr:
        # Strategy 1: pdftotext
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', str(path), '-'],
                capture_output=True, timeout=60
            )
            text = result.stdout.decode('utf-8', errors='replace').strip()
        except Exception:
            pass

        if not text or len(text) < 100:
            try:
                result = subprocess.run(
                    ['pdftotext', '-layout', '-enc', 'UTF-8', str(path), '-'],
                    capture_output=True, timeout=60,
                    env={**os.environ, 'LANG': 'en_US.UTF-8'}
                )
                text = result.stdout.decode('utf-8', errors='replace').strip()
            except Exception:
                pass

        # Strategy 2: PyMuPDF
        if not text or len(text) < 100:
            try:
                import fitz
                doc = fitz.open(str(path))
                pages_text = []
                for page in doc:
                    pages_text.append(page.get_text())
                doc.close()
                text = '\n'.join(pages_text).strip()
            except Exception:
                pass

    # Strategy 3: pdftoppm → OCR each page (for image-based PDFs)
    if force_image_ocr or not text or len(text) < 200:
        try:
            import tempfile, shutil
            pdftoppm = shutil.which('pdftoppm')
            if pdftoppm:
                with tempfile.TemporaryDirectory() as tmpdir:
                    prefix = os.path.join(tmpdir, 'page')
                    subprocess.run(
                        [pdftoppm, '-png', '-r', '200', str(path), prefix],
                        capture_output=True, timeout=120, check=True
                    )
                    page_files = sorted(Path(tmpdir).glob('page-*.png'))
                    if page_files:
                        pages_text = []
                        for pf in page_files:
                            pt = ocr_image(str(pf), lang=lang, preprocess='enhanced')
                            pages_text.append(pt)
                        text = '\n\n--- PAGE ---\n\n'.join(pages_text)
            else:
                # Fallback: try pdf2image if available
                pass
        except Exception:
            pass

    return text.strip() or "(no extractable text)"

# ─── Quality Scoring ───────────────────────────────────────────
def quality_score(text):
    """Score OCR quality 0-100. Higher = more readable Chinese text."""
    if not text or len(text) < 20:
        return 0
    total = len(text)
    cjk = len(re.findall(r'[一-鿿]', text))
    # Inverse of garbled-character density
    garbled = len(re.findall(r'[^一-鿿\s\d\w\.\,\。\，\、\：\；\？\！' +
                             r'\《\》\（\）\【\】\—\…\·\n\%\+\-\×\÷\＝]', text))
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    meaningful = sum(1 for l in lines if len(re.findall(r'[一-鿿]', l)) >= 4)

    cjk_ratio = cjk / max(total, 1)
    line_quality = meaningful / max(len(lines), 1)
    garbled_ratio = garbled / max(total, 1)

    score = cjk_ratio * 40 + line_quality * 40 - garbled_ratio * 30 + 20
    return max(0, min(100, int(score)))

def verdict(score):
    if score >= 45: return 'GOOD'
    if score >= 25: return 'FAIR'
    return 'POOR'

# ─── Batch Processing ──────────────────────────────────────────
IMG_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
PDF_EXTS = {'.pdf'}
_total_lock = threading.Lock()
_total_done = [0]
_total_all = [0]

def _process_one(args):
    path, rel_dir, fname, ext, lang = args
    is_pdf = ext in PDF_EXTS
    text = ocr_pdf(path) if is_pdf else ocr_image(path, lang=lang)

    with _total_lock:
        _total_done[0] += 1
        n = _total_done[0]
        if n % 20 == 0:
            print(f"  [{n}/{_total_all[0]}] {100*n//_total_all[0]}%", flush=True)

    return rel_dir, fname, text

def batch_process(input_dir, output_dir, lang='chi_sim+eng', workers=4):
    """
    Walk input_dir, OCR all images/PDFs, save JSON results to output_dir.
    Returns dict of {rel_dir: [{file, text}]}.
    """
    base = Path(input_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Collect files
    all_files = []
    for root, dirs, files in os.walk(base):
        rel_dir = str(Path(root).relative_to(base))
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in IMG_EXTS or ext in PDF_EXTS:
                all_files.append((Path(root) / f, rel_dir, f, ext, lang))

    _total_all[0] = len(all_files)
    _total_done[0] = 0
    print(f"Files to process: {_total_all[0]}")
    print(f"Using {workers} threads, language: {lang}")

    results = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_process_one, a) for a in all_files]
        for future in as_completed(futures):
            rel_dir, fname, text = future.result()
            results.setdefault(rel_dir, []).append({'file': fname, 'text': text})

    # Save
    for rel_dir, files in results.items():
        safe_name = rel_dir.replace('/', '_').replace('\\', '_')
        with open(out / f'{safe_name}.json', 'w', encoding='utf-8') as fh:
            json.dump(files, fh, ensure_ascii=False, indent=2)

    # Save index with quality scores
    index = {}
    for rel_dir, files in results.items():
        scores = [quality_score(item['text']) for item in files]
        avg = round(sum(scores) / len(scores), 1)
        index[rel_dir] = {'count': len(files), 'avg_score': avg, 'verdict': verdict(avg)}

    with open(out / '_index.json', 'w', encoding='utf-8') as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)

    print(f"\nDone: {_total_all[0]} files → {len(results)} result files → {output_dir}")

    # Print quality summary
    goods = sum(1 for v in index.values() if v['verdict'] == 'GOOD')
    fairs = sum(1 for v in index.values() if v['verdict'] == 'FAIR')
    poors = sum(1 for v in index.values() if v['verdict'] == 'POOR')
    print(f"Quality: GOOD={goods} FAIR={fairs} POOR={poors}")

    return results, index

def quality_scan(results_dir):
    """Scan existing OCR JSON results and print quality report."""
    out = Path(results_dir)
    print(f"{'FILE':<55} {'ITEMS':>5} {'SCORE':>7} {'AVGLEN':>7} {'VERDICT'}")
    print("-" * 85)
    data = {}
    for fname in sorted(os.listdir(out)):
        if fname == '_index.json' or not fname.endswith('.json'):
            continue
        with open(out / fname, 'r', encoding='utf-8') as f:
            items = json.load(f)
        scores = [quality_score(item.get('text', '')) for item in items]
        lengths = [len(item.get('text', '')) for item in items]
        avg_score = round(sum(scores) / len(scores), 1)
        avg_len = int(sum(lengths) / len(lengths))
        v = verdict(avg_score)
        print(f"{fname:<55} {len(items):>5} {avg_score:>7.1f} {avg_len:>7} {v}")
        data[fname] = {'count': len(items), 'avg_score': avg_score, 'verdict': v}
    return data

# ─── CLI ───────────────────────────────────────────────────────
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OCR Engine - batch process images/PDFs')
    parser.add_argument('input_dir', help='Root directory containing images/PDFs')
    parser.add_argument('output_dir', help='Directory to save OCR JSON results')
    parser.add_argument('--lang', default='chi_sim+eng', help='Tesseract language (default: chi_sim+eng)')
    parser.add_argument('--workers', type=int, default=4, help='Parallel threads (default: 4)')
    parser.add_argument('--scan-only', action='store_true', help='Only scan quality of existing results')

    args = parser.parse_args()

    setup_tesseract()

    if args.scan_only:
        quality_scan(args.output_dir)
    else:
        batch_process(args.input_dir, args.output_dir, args.lang, args.workers)
