#!/usr/bin/env python3
import argparse
import glob
import json
import os
import sys
import yake

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import pos_tag

# Ensure NLTK data is available
nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)


def load_file_descriptions(input_dir):
    """
    Reads each JSON file under input_dir and returns a dict:
      key -> { 'descriptions': [...], 'path': filepath }
    where key is filename stem minus '_data'.
    Skips any null or non-dict entries.
    """
    out = {}
    pattern = os.path.join(input_dir, "*.json")
    for path in glob.glob(pattern):
        fname = os.path.basename(path)
        stem = os.path.splitext(fname)[0]         # e.g. "al_ml_data"
        key  = stem[:-5] if stem.endswith("_data") else stem

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # collect all non-empty descriptions from dict-valued records
        descs = []
        for rec in data.values():
            if not isinstance(rec, dict):
                continue
            desc = rec.get("description")
            if isinstance(desc, str) and desc.strip():
                descs.append(desc.strip())

        if not descs:
            print(f"Warning: no valid descriptions in {fname}", file=sys.stderr)
            continue

        out[key] = {
            "descriptions": descs,
            "path": path
        }
    return out


def extract_group_keywords(descriptions, uni_n=50, bi_n=25, tri_n=10):
    """
    Returns three lists concatenated:
      - top uni_n single words
      - top bi_n two-word phrases
      - top tri_n three-word phrases
    """
    text = " ".join(descriptions)
    # single‐words
    ext1 = yake.KeywordExtractor(lan="en", n=1, top=uni_n)
    kws1 = [kw for kw, _ in ext1.extract_keywords(text)]
    # bi-grams
    ext2 = yake.KeywordExtractor(lan="en", n=2, top=bi_n)
    kws2 = [kw for kw, _ in ext2.extract_keywords(text)]
    # tri-grams
    ext3 = yake.KeywordExtractor(lan="en", n=3, top=tri_n)
    kws3 = [kw for kw, _ in ext3.extract_keywords(text)]
    return kws1 + kws2 + kws3, kws1


def partition_by_pos(keywords):
    """
    Tag each keyword; return (verbs, nouns/proper-nouns).
    """
    tagged = pos_tag(keywords)
    verbs = [w for w, tag in tagged if tag.startswith("VB")]
    nouns = [w for w, tag in tagged if tag.startswith("NN")]
    return verbs, nouns


def resolve_path(maybe_path, project_root):
    """
    If maybe_path exists as given, leave it.
    Else if it's relative, try project_root/maybe_path.
    """
    if os.path.isabs(maybe_path) or os.path.exists(maybe_path):
        return maybe_path
    alt = os.path.join(project_root, maybe_path)
    return alt


def main(args):
    # Determine project root (two levels up from this script)
    script_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    input_dir = resolve_path(args.input_dir, project_root)
    output_file = resolve_path(args.output_file, project_root)

    # Load & process
    groups = load_file_descriptions(input_dir)
    result = {}
    for key, info in groups.items():
        # 1) extract raw keywords and unigrams+bi+tri
        ats_all, _ = extract_group_keywords(
            info["descriptions"],
            uni_n=args.uni,
            bi_n=args.bi,
            tri_n=args.tri
        )

        # 2) dedupe ats_all (case-insensitive), preserve order
        seen = set()
        ats_unique = []
        for kw in ats_all:
            lk = kw.lower()
            if lk not in seen:
                seen.add(lk)
                ats_unique.append(kw)

        # 3) POS-tag every phrase (uni/bi/tri), loosen filter to include adjectives
        verbs = []
        skills = []
        for phrase in ats_unique:
            tokens = phrase.split()
            tags = pos_tag(tokens)
            # if any token is a verb → include phrase
            if any(tag.startswith("VB") for _, tag in tags):
                verbs.append(phrase)
            # if any token is noun (NN.*) or adjective (JJ.*) → include phrase
            if any(tag.startswith("NN") or tag.startswith("JJ") for _, tag in tags):
                skills.append(phrase)

        # 4) dedupe verbs & skills, preserve order
        verbs = list(dict.fromkeys(verbs))
        skills = list(dict.fromkeys(skills))

        # 5) assign cleaned lists to result
        result[key] = {
            "ats_keywords": ats_unique,
            "action_verbs": verbs,
            "skills": skills
        }

    # Ensure output folder exists (only if a directory was given)
    outdir = os.path.dirname(output_file)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Extract ATS keywords, verbs, and skills per job-title bucket"
    )
    p.add_argument(
        "--input_dir", required=True,
        help="e.g. data/script/linkedin/data"
    )
    p.add_argument(
        "--output_file", required=True,
        help="e.g. extracted_data.json"
    )
    p.add_argument(
        "--top_n", type=int, default=20,
        help="(deprecated) total keywords per group"
    )
    p.add_argument(
        "--uni", type=int, default=50,
        help = "number of unigrams to extract"
    )
    p.add_argument(
        "--bi", type=int, default=25,
        help = "number of bigrams to extract"
    )
    p.add_argument(
        "--tri", type=int, default=10,
        help = "number of trigrams to extract"
    )

main(p.parse_args())
