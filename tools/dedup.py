#!/usr/bin/env python3
"""
Image Deduplication — detect near-duplicate images before OCR.

Uses perceptual hash (pHash) to find similar images and keep only the best one.
Reduces OCR workload by 30-50% for typical photo collections.

Usage:
  python dedup.py <input_dir> [--threshold 5] [--dry-run]
"""
import os
import argparse
from pathlib import Path
from PIL import Image
from collections import defaultdict
from _common import logger


def dhash(img, hash_size=8):
    """Difference hash: resize to hash_size+1 × hash_size, compare adjacent pixels."""
    resized = img.convert('L').resize((hash_size + 1, hash_size), Image.LANCZOS)
    pixels = list(resized.getdata())
    diff = []
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row * (hash_size + 1) + col]
            right = pixels[row * (hash_size + 1) + col + 1]
            diff.append('1' if left > right else '0')
    return ''.join(diff)


def hamming_distance(h1, h2):
    """Count differing bits between two hashes."""
    return sum(c1 != c2 for c1, c2 in zip(h1, h2))


def find_duplicates(file_paths, threshold=5):
    """
    Group images by perceptual similarity.
    Returns list of groups, each group is [(path, quality_score), ...].
    """
    hashes = {}
    for path in file_paths:
        try:
            img = Image.open(path)
            hashes[path] = dhash(img)
        except Exception:
            continue

    # Simple quality heuristic: larger file size = likely better quality
    def quality(p):
        try:
            return os.path.getsize(p)
        except Exception:
            return 0

    # Union-find to group similar images
    parent = {p: p for p in hashes}
    paths_list = list(hashes.keys())

    for i in range(len(paths_list)):
        for j in range(i + 1, len(paths_list)):
            p1, p2 = paths_list[i], paths_list[j]
            if hamming_distance(hashes[p1], hashes[p2]) <= threshold:
                # Union
                root1 = p1
                while parent[root1] != root1:
                    root1 = parent[root1]
                root2 = p2
                while parent[root2] != root2:
                    root2 = parent[root2]
                if root1 != root2:
                    parent[root2] = root1

    # Collect groups
    groups_map = defaultdict(list)
    for p in hashes:
        root = p
        while parent[root] != root:
            root = parent[root]
        groups_map[root].append((p, quality(p)))

    groups = list(groups_map.values())
    return groups


def deduplicate(input_dir, threshold=5, dry_run=False):
    """
    Scan input_dir for duplicate/near-duplicate images.
    Return: (kept_files, removed_groups) where removed_groups lists duplicates per group.
    """
    base = Path(input_dir)
    img_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
    all_images = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if Path(f).suffix.lower() in img_exts:
                all_images.append(Path(root) / f)

    logger.info(f"Scanning {len(all_images)} images for duplicates...")
    groups = find_duplicates([str(p) for p in all_images], threshold)

    kept = []
    removed_groups = []

    for group in groups:
        if len(group) == 1:
            kept.append(group[0][0])
        else:
            # Keep the one with the best quality (largest file size)
            group.sort(key=lambda x: -x[1])
            best = group[0][0]
            dupes = [p for p, _ in group[1:]]
            kept.append(best)
            removed_groups.append({'kept': best, 'removed': dupes})

    if dry_run:
        logger.info(f"\nDry run — would keep {len(kept)}, remove {sum(len(g['removed']) for g in removed_groups)}")
        for g in removed_groups:
            logger.info(f"\n  KEEP: {g['kept']}")
            for r in g['removed']:
                logger.info(f"    ✗ {r}")
    else:
        for g in removed_groups:
            for r in g['removed']:
                os.remove(r)

        removed_count = sum(len(g['removed']) for g in removed_groups)
        logger.info(f"Done. Kept {len(kept)}, removed {removed_count} duplicates.")

    return kept, removed_groups


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect and remove near-duplicate images')
    parser.add_argument('input_dir', help='Directory to scan for duplicates')
    parser.add_argument('--threshold', type=int, default=5,
                        help='Hamming distance threshold (0-64, lower=stricter, default: 5)')
    parser.add_argument('--dry-run', action='store_true', help='Only show what would be removed')
    args = parser.parse_args()

    deduplicate(args.input_dir, args.threshold, args.dry_run)
