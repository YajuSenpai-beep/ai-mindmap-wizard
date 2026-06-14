#!/usr/bin/env python3
"""
Content-Based Clustering — group OCR results by semantic similarity.

Replaces the default filename-prefix clustering with TF-IDF + cosine similarity.
Produces topic clusters that reflect actual content, not folder names.

Usage:
  python clustering.py <ocr_results_dir> [--min-similarity 0.3] [--output clusters.json]
"""
import os
import json
import re
import argparse
from pathlib import Path
from collections import defaultdict
from math import log, sqrt
from _common import logger


def tokenize(text):
    """Extract CJK bigrams and meaningful tokens from text."""
    text = text.lower()
    # Extract CJK bigrams
    cjk = re.findall(r'[一-鿿]{2,}', text)
    # Extract alphabetic words (3+ chars)
    eng = re.findall(r'[a-z]{3,}', text)
    return cjk + eng


def compute_tf(tokens):
    """Term frequency."""
    tf = defaultdict(int)
    for t in tokens:
        tf[t] += 1
    # Normalize
    total = len(tokens) or 1
    return {t: c / total for t, c in tf.items()}


def compute_idf(documents):
    """Inverse document frequency across all documents."""
    N = len(documents)
    df = defaultdict(int)
    for doc_tokens in documents:
        for t in set(doc_tokens):
            df[t] += 1
    return {t: log(N / (df[t] + 1)) + 1 for t in df}


def tfidf_vector(tf, idf):
    """Compute TF-IDF vector as dict {term: weight}."""
    return {t: tf[t] * idf.get(t, 0) for t in tf}


def cosine_similarity(v1, v2):
    """Cosine similarity between two sparse vectors."""
    all_keys = set(v1) | set(v2)
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in all_keys)
    norm1 = sqrt(sum(v ** 2 for v in v1.values()))
    norm2 = sqrt(sum(v ** 2 for v in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot / (norm1 * norm2)


def load_ocr_results(ocr_dir):
    """Load all OCR JSON files, return {name: concatenated_text}."""
    ocr_path = Path(ocr_dir)
    docs = {}
    try:
        from tqdm import tqdm
    except ImportError:
        tqdm = lambda x, **kw: x
    for fname in sorted(os.listdir(ocr_path)):
        if fname == '_index.json' or not fname.endswith('.json'):
            continue
        with open(ocr_path / fname, 'r', encoding='utf-8') as f:
            items = json.load(f)
        text = '\n'.join(item.get('text', '') for item in items if item.get('text'))
        name = fname.replace('.json', '')
        if text.strip():
            docs[name] = text
    return docs


def cluster_by_content(ocr_dir, min_similarity=0.3):
    """
    Cluster OCR result files by TF-IDF content similarity.
    Returns list of clusters, each cluster is [doc_name, ...].
    """
    docs = load_ocr_results(ocr_dir)
    if not docs:
        return []

    # Tokenize
    tokenized = {name: tokenize(text) for name, text in docs.items()}
    # Compute TF-IDF
    tfs = {name: compute_tf(tokens) for name, tokens in tokenized.items()}
    idf = compute_idf(list(tokenized.values()))
    vectors = {name: tfidf_vector(tfs[name], idf) for name in docs}

    # Greedy clustering: each doc joins the cluster it's most similar to
    doc_names = list(docs.keys())
    clusters = [[doc_names[0]]]

    for name in doc_names[1:]:
        best_cluster = None
        best_score = 0
        for cluster in clusters:
            # Average similarity to cluster members
            scores = [cosine_similarity(vectors[name], vectors[m]) for m in cluster]
            avg = sum(scores) / len(scores)
            if avg > best_score:
                best_score = avg
                best_cluster = cluster

        if best_score >= min_similarity and best_cluster is not None:
            best_cluster.append(name)
        else:
            clusters.append([name])

    # Auto-name clusters by top TF-IDF terms
    named_clusters = []
    for cluster in clusters:
        # Find top terms across cluster
        term_scores = defaultdict(float)
        for name in cluster:
            for term, weight in vectors[name].items():
                term_scores[term] += weight / len(cluster)
        top_terms = sorted(term_scores, key=term_scores.get, reverse=True)[:3]
        cluster_name = '_'.join(top_terms) if top_terms else cluster[0]
        named_clusters.append({'name': cluster_name, 'docs': cluster})

    return named_clusters


def print_clusters(clusters):
    """Pretty-print clustering results."""
    logger.info(f"\nFound {len(clusters)} content-based clusters:\n")
    for i, c in enumerate(clusters, 1):
        logger.info(f"### Cluster {i}: {c['name']} ({len(c['docs'])} docs)")
        for doc in c['docs']:
            logger.info(f"    - {doc}")
        logger.info()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Content-based clustering of OCR results')
    parser.add_argument('ocr_dir', help='Directory containing OCR JSON files')
    parser.add_argument('--min-similarity', type=float, default=0.3,
                        help='Minimum cosine similarity to join a cluster (default: 0.3)')
    parser.add_argument('--output', help='Save clusters to JSON file')
    args = parser.parse_args()

    clusters = cluster_by_content(args.ocr_dir, args.min_similarity)
    print_clusters(clusters)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(clusters, f, ensure_ascii=False, indent=2)
        logger.info(f"Clusters saved to: {args.output}")
