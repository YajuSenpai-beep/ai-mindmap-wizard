#!/usr/bin/env python3
"""
Incremental Processing — track file hashes to skip unchanged files on re-runs.

Usage:
  python incremental.py <input_dir> <state_file> [--reset]
"""
import os
import json
import hashlib
import argparse
from pathlib import Path
from _common import logger


def file_hash(path):
    """SHA-256 hash of file contents."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def scan_directory(input_dir):
    """Walk input_dir and return {relative_path: sha256_hash}."""
    base = Path(input_dir)
    img_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.pdf', '.docx', '.pptx', '.html'}
    files = {}
    for root, dirs, filenames in os.walk(base):
        for f in filenames:
            ext = Path(f).suffix.lower()
            if ext in img_exts:
                full_path = Path(root) / f
                rel_path = str(full_path.relative_to(base))
                files[rel_path] = file_hash(str(full_path))
    return files


def load_state(state_file):
    """Load previously saved file hash state."""
    if os.path.exists(state_file):
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_state(state_file, state):
    """Save file hash state."""
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def diff_state(input_dir, state_file, reset=False):
    """
    Compare current file state with saved state.
    Returns: (new_files, modified_files, deleted_files, unchanged_count)
    """
    if reset:
        # Force full re-scan
        current = scan_directory(input_dir)
        return list(current.keys()), [], [], 0

    current = scan_directory(input_dir)
    previous = load_state(state_file)

    new_files = [f for f in current if f not in previous]
    modified = [f for f in current if f in previous and current[f] != previous[f]]
    deleted = [f for f in previous if f not in current]
    unchanged = [f for f in current if f in previous and current[f] == previous[f]]

    return new_files, modified, deleted, unchanged


def get_files_to_process(input_dir, state_file, reset=False):
    """
    Return list of (full_path, reason) for files that need processing.
    Also saves the new state.
    """
    base = Path(input_dir)
    new_files, modified, deleted, unchanged = diff_state(input_dir, state_file, reset)

    to_process = []
    for f in new_files:
        to_process.append((str(base / f), 'new'))
    for f in modified:
        to_process.append((str(base / f), 'modified'))

    # Save current state
    current = scan_directory(input_dir)
    save_state(state_file, current)

    logger.info(f"  New: {len(new_files)} | Modified: {len(modified)} | "
          f"Deleted: {len(deleted)} | Unchanged: {len(unchanged)}")
    return to_process


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Incremental file change detection')
    parser.add_argument('input_dir', help='Directory to scan')
    parser.add_argument('state_file', help='JSON file to save/load state')
    parser.add_argument('--reset', action='store_true', help='Force full re-scan')
    args = parser.parse_args()

    new, mod, deleted, unchanged = diff_state(args.input_dir, args.state_file, args.reset)
    logger.info(f"New: {len(new)} | Modified: {len(mod)} | Deleted: {len(deleted)} | Unchanged: {len(unchanged)}")

    if new:
        logger.info("\nNew files:")
        for f in new:
            logger.info(f"  + {f}")
    if mod:
        logger.info("\nModified files:")
        for f in mod:
            logger.info(f"  ~ {f}")
    if deleted:
        logger.info("\nDeleted files:")
        for f in deleted:
            logger.info(f"  - {f}")
