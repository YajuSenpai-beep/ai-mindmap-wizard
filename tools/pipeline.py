#!/usr/bin/env python3
"""
Image Knowledge Extractor — Main Pipeline (Enhanced)

Full workflow:
  python pipeline.py <input_dir> <project_name>

Steps:
  0. dedup   — Remove near-duplicate images (NEW)
  1. ocr     — Batch OCR all images/PDFs (with incremental skip)
  2. scan    — Quality assessment, identify low-quality files
  3. improve — Re-process low-quality files with adaptive OCR
  4. cluster — Content-based topic clustering (NEW)
  5. correct — LLM-based OCR error correction (NEW, optional: --correct)
  6. formats — Extract text from Word/PPT/HTML files (NEW)
  7. notes   — Generate AI agent prompts for each topic cluster
  8. check   — Cross-validate generated notes against OCR sources

Output directory: ./output/<project_name>/
"""
import sys, os, argparse, subprocess, json, logging
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def step_dedup(input_dir, dry_run):
    """Step 0: Remove near-duplicate images."""
    print("\n" + "=" * 60)
    print("STEP 0/8: Image Deduplication")
    print("=" * 60)
    try:
        from dedup import deduplicate
        kept, removed = deduplicate(str(input_dir), threshold=5, dry_run=dry_run)
        if dry_run:
            print(f"  (dry run) Would keep {len(kept)}, remove {sum(len(g['removed']) for g in removed)}")
        else:
            removed_count = sum(len(g['removed']) for g in removed)
            print(f"  Kept: {len(kept)}, removed: {removed_count} duplicates")
        return kept, removed
    except ImportError:
        print("  (dedup module not available, skipping)")
        return [], []


def step_formats(input_dir, output_dir):
    """Step 6: Extract text from Word/PPT/HTML files."""
    print("\n" + "=" * 60)
    print("STEP 6/8: Extended Format Extraction (Word/PPT/HTML)")
    print("=" * 60)
    try:
        from formats import batch_extract
        text_dir = os.path.join(output_dir, 'extracted_text')
        results = batch_extract(str(input_dir), text_dir)
        print(f"  Extracted: {len(results)} files")
        return results
    except ImportError:
        print("  (formats module not available, skipping)")
        return {}


def step_ocr(input_dir, ocr_dir, lang, workers, use_incremental, state_file):
    """Step 1: Batch OCR with incremental skip."""
    print("\n" + "=" * 60)
    print("STEP 1/8: Batch OCR")
    print("=" * 60)

    if use_incremental:
        try:
            from incremental import get_files_to_process
            to_process = get_files_to_process(str(input_dir), state_file)
            if not to_process:
                print("  No new or modified files — skipping OCR.")
                return
            print(f"  Incremental: {len(to_process)} files to process")
        except ImportError:
            print("  (incremental module not available, full OCR)")

    subprocess.run([
        sys.executable, str(SCRIPT_DIR / 'ocr_engine.py'),
        str(input_dir), str(ocr_dir), '--lang', lang, '--workers', str(workers)
    ], check=True)


def step_scan(ocr_dir):
    """Step 2: Quality scan."""
    print("\n" + "=" * 60)
    print("STEP 2/8: Quality Scan")
    print("=" * 60)
    subprocess.run([
        sys.executable, str(SCRIPT_DIR / 'ocr_engine.py'),
        '.', str(ocr_dir), '--scan-only'
    ], check=True)


def step_improve(input_dir, ocr_dir, lang):
    """Step 3: Adaptive re-processing for low-quality files."""
    print("\n" + "=" * 60)
    print("STEP 3/8: Adaptive OCR Improvement")
    print("=" * 60)

    index_path = os.path.join(ocr_dir, '_index.json')
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    poor_files = [k for k, v in index.items() if v['verdict'] != 'GOOD']
    if not poor_files:
        print("  All files are GOOD quality — nothing to improve.")
        return

    print(f"  Files to re-process: {len(poor_files)}")
    for name in poor_files:
        print(f"    [{index[name]['verdict']}] {name} (score={index[name]['avg_score']})")

    from ocr_engine import ocr_image, ocr_pdf, quality_score, setup_tesseract, IMG_EXTS, PDF_EXTS
    setup_tesseract()

    improved_count = 0
    for topic_name in poor_files:
        json_file = os.path.join(ocr_dir, f'{topic_name}.json')
        if not os.path.exists(json_file):
            continue

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            filename = item['file']
            old_text = item.get('text', '')
            old_len = len(old_text) if old_text else 0
            ext = Path(filename).suffix.lower()

            for root, dirs, files in os.walk(str(input_dir)):
                if filename in files:
                    fpath = os.path.join(root, filename)
                    new_text = ocr_pdf(fpath) if ext in PDF_EXTS else ocr_image(fpath, lang=lang)
                    if new_text and len(new_text) > old_len * 0.3:
                        item['text'] = new_text
                        improved_count += 1
                    break

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Improved: {improved_count} items")
    step_scan(ocr_dir)


def step_cluster(ocr_dir, notes_dir):
    """Step 4: Content-based topic clustering."""
    print("\n" + "=" * 60)
    print("STEP 4/8: Content-Based Clustering")
    print("=" * 60)

    try:
        from clustering import cluster_by_content
        clusters = cluster_by_content(str(ocr_dir), min_similarity=0.3)
        print(f"  Found {len(clusters)} content-based clusters:")

        cluster_file = os.path.join(notes_dir, '_clusters.json')
        with open(cluster_file, 'w', encoding='utf-8') as f:
            json.dump(clusters, f, ensure_ascii=False, indent=2)

        for i, c in enumerate(clusters, 1):
            print(f"    Cluster {i}: {c['name']} ({len(c['docs'])} docs)")
            for doc in c['docs']:
                print(f"      - {doc}")

        print(f"  Clusters saved to: {cluster_file}")
        return clusters
    except ImportError:
        print("  (clustering module not available, using folder-based grouping)")
        return None


def step_correct(ocr_dir, provider, api_key, model, dry_run):
    """Step 5: LLM-based OCR correction."""
    print("\n" + "=" * 60)
    print("STEP 5/8: LLM OCR Correction")
    print("=" * 60)

    try:
        from llm_correct import correct_ocr_json

        total_corrected = 0
        for fname in sorted(os.listdir(ocr_dir)):
            if fname == '_index.json' or not fname.endswith('.json'):
                continue
            path = os.path.join(ocr_dir, fname)
            result, _ = correct_ocr_json(path, provider, api_key, model, dry_run)

            if dry_run:
                print(f"  {fname}: {len(result)} prompts generated")
                # Save prompts
                prompt_file = os.path.join(ocr_dir, '_correction_prompts.txt')
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    for r in result:
                        f.write(f"### {r['file']}\n\n{r['prompt']}\n\n---\n\n")
                print(f"  Prompts saved to: {prompt_file}")
            else:
                total_corrected += result
                print(f"  {fname}: {result} items corrected")

        if not dry_run:
            print(f"  Total corrected: {total_corrected} items")
    except ImportError:
        print("  (llm_correct module not available, skipping)")


def step_generate_prompts(input_dir, ocr_dir, notes_dir, use_clustering):
    """Step 7: Generate AI agent prompts for note generation."""
    print("\n" + "=" * 60)
    print("STEP 7/8: Generate AI Agent Prompts")
    print("=" * 60)

    index_path = os.path.join(ocr_dir, '_index.json')
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    topics = list(index.keys())
    print(f"\n  Total OCR result files: {len(topics)}")

    # Use content-based clusters if available
    if use_clustering:
        cluster_file = os.path.join(notes_dir, '_clusters.json')
        if os.path.exists(cluster_file):
            with open(cluster_file, 'r', encoding='utf-8') as f:
                clusters = json.load(f)
            print(f"  Using {len(clusters)} content-based clusters")
        else:
            clusters = None
    else:
        clusters = None

    prompt_file = os.path.join(notes_dir, '_agent_prompts.txt')
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(f"# AI Agent Prompts — generated {datetime.now().isoformat()}\n\n")
        f.write(f"Instructions: For each cluster below, have an AI agent:\n")
        f.write(f"1. Read ALL the listed OCR JSON files from: {ocr_dir}\n")
        f.write(f"2. Synthesize into a structured Chinese markdown note\n")
        f.write(f"3. Follow the writing standards in skill_template.md\n")
        f.write(f"4. Save to: {notes_dir}/XX_<topic>.md\n\n")
        f.write("=" * 60 + "\n\n")

        if clusters:
            for i, c in enumerate(clusters, 1):
                topic_files = '\n'.join(f'  - {ocr_dir}/{t}.json' for t in c['docs'])
                prompt = f"""### Cluster {i}: {c['name']}
Files to read:
{topic_files}

Writing prompt:
Read ALL the OCR JSON files listed above. Synthesize the extracted knowledge into
a well-structured markdown note. Follow the writing standards (pyramid structure,
information density, executability). Write in Chinese, no greeting text.
Save to: {notes_dir}/{i:02d}_{c['name']}.md
"""
                f.write(prompt)
                f.write("\n---\n\n")
        else:
            # Fallback: per-folder grouping
            from collections import defaultdict
            folder_clusters = defaultdict(list)
            for t in topics:
                parts = t.split('_')
                key = parts[0] if len(parts) > 1 else t
                folder_clusters[key].append(t)

            for i, (key, ct) in enumerate(sorted(folder_clusters.items()), 1):
                topic_files = '\n'.join(f'  - {ocr_dir}/{t}.json' for t in ct)
                prompt = f"""### Cluster {i}: {key}
Files to read:
{topic_files}

Writing prompt:
Read ALL the OCR JSON files listed above. Synthesize the extracted knowledge...
Save to: {notes_dir}/{i:02d}_{key}.md
"""
                f.write(prompt)
                f.write("\n---\n\n")

    print(f"\n  Prompts saved to: {prompt_file}")
    return prompt_file


def step_check(notes_dir, ocr_dir, output_report):
    """Step 8: Cross-validate notes against OCR sources."""
    print("\n" + "=" * 60)
    print("STEP 8/8: Quality Check (cross-validation)")
    print("=" * 60)
    subprocess.run([
        sys.executable, str(SCRIPT_DIR / 'quality_checker.py'),
        str(notes_dir), str(ocr_dir), '--output', str(output_report)
    ], check=True)


def main():
    parser = argparse.ArgumentParser(
        description='Image Knowledge Extractor — turn images into structured notes'
    )
    parser.add_argument('input_dir', help='Root directory containing images, PDFs, Word, PPT, HTML files')
    parser.add_argument('project', help='Project name (used for output directory)')
    parser.add_argument('--lang', default='chi_sim+eng', help='Tesseract language (default: chi_sim+eng)')
    parser.add_argument('--workers', type=int, default=4, help='OCR parallel threads (default: 4)')
    parser.add_argument('--start-from', choices=['dedup', 'ocr', 'scan', 'improve', 'cluster',
                                                  'correct', 'formats', 'notes', 'check'],
                        default='dedup', help='Skip to a specific step')
    parser.add_argument('--only', choices=['dedup', 'ocr', 'scan', 'improve', 'cluster',
                                            'correct', 'formats', 'notes', 'check'],
                        help='Run only one step')
    parser.add_argument('--no-incremental', action='store_true', help='Disable incremental OCR')
    parser.add_argument('--no-clustering', action='store_true', help='Use folder-based grouping')
    parser.add_argument('--no-dedup', action='store_true', help='Skip deduplication')
    parser.add_argument('--correct', action='store_true', help='Enable LLM OCR correction')
    parser.add_argument('--correct-provider', choices=['claude', 'openai'], help='LLM provider for correction')
    parser.add_argument('--correct-api-key', help='API key for LLM correction')
    parser.add_argument('--correct-model', help='Model name for LLM correction')
    parser.add_argument('--dry-run', action='store_true', help='Dedup/Correct in preview mode')

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        sys.exit(f"ERROR: input directory not found: {args.input_dir}")

    output_dir = Path('./output') / args.project
    ocr_dir = output_dir / 'ocr_results'
    notes_dir = output_dir / 'notes'
    report_path = output_dir / '校准报告.md'
    log_path = output_dir / 'pipeline.log'
    state_file = output_dir / '.file_state.json'

    ocr_dir.mkdir(parents=True, exist_ok=True)
    notes_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=str(log_path),
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    logging.info(f"Pipeline started: project={args.project}, input={args.input_dir}")

    steps_order = ['dedup', 'ocr', 'scan', 'improve', 'cluster', 'correct', 'formats', 'notes', 'check']

    if args.only:
        steps_to_run = [args.only]
    else:
        start_idx = steps_order.index(args.start_from)
        steps_to_run = steps_order[start_idx:]

    try:
        for step in steps_to_run:
            if step == 'dedup':
                if not args.no_dedup:
                    step_dedup(args.input_dir, args.dry_run)
                else:
                    print("\n  (dedup skipped via --no-dedup)")
            elif step == 'ocr':
                step_ocr(args.input_dir, str(ocr_dir), args.lang, args.workers,
                         not args.no_incremental, str(state_file))
            elif step == 'scan':
                step_scan(str(ocr_dir))
            elif step == 'improve':
                step_improve(args.input_dir, str(ocr_dir), args.lang)
            elif step == 'cluster':
                step_cluster(str(ocr_dir), str(notes_dir)) if not args.no_clustering else None
            elif step == 'correct':
                if args.correct:
                    step_correct(str(ocr_dir), args.correct_provider, args.correct_api_key,
                                 args.correct_model, args.dry_run)
                else:
                    print("\n  (LLM correction skipped — use --correct to enable)")
            elif step == 'formats':
                step_formats(args.input_dir, str(output_dir))
            elif step == 'notes':
                step_generate_prompts(args.input_dir, str(ocr_dir), str(notes_dir),
                                      not args.no_clustering)
            elif step == 'check':
                step_check(str(notes_dir), str(ocr_dir), str(report_path))

        print(f"\n{'=' * 60}")
        print(f"Pipeline complete!")
        print(f"  OCR results: {ocr_dir}")
        print(f"  Notes:       {notes_dir}")
        print(f"  Report:      {report_path}")
        print(f"  Log:         {log_path}")
        print(f"{'=' * 60}")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
