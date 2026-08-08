#!/usr/bin/env python3
"""Citation pipeline: scan the manuscript for informal citation tags, resolve
them against INSPIRE-HEP, and merge full BibTeX entries into refs/references.bib
keyed by INSPIRE texkeys.

Finds: bare arXiv IDs (2503.17357), old-style (hep-lat/0007038), and bracketed
tags like [Ding et al 1504.05274]. Requires network; run locally or in CI.

Usage:
    python3 tools/build_bib.py            # report + update refs/references.bib
    python3 tools/build_bib.py --dry-run  # report only
"""
import pathlib, re, sys, json, time, urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
BIB = REPO / "refs" / "references.bib"
ARXIV_RX = re.compile(r"\b(\d{4}\.\d{4,5})\b|\b((?:hep-(?:lat|ph|th)|nucl-th|cond-mat)/\d{7})\b")

def found_ids():
    ids = set()
    for f in sorted(REPO.glob("chapters/*/*.tex")):
        for m in ARXIV_RX.finditer(f.read_text(encoding="utf-8")):
            ids.add(m.group(1) or m.group(2))
    return sorted(ids)

def inspire_bibtex(arxiv_id):
    url = f"https://inspirehep.net/api/arxiv/{arxiv_id}"
    with urllib.request.urlopen(url, timeout=30) as r:
        rec = json.load(r)
    links = rec.get("links", {})
    bib_url = links.get("bibtex")
    if not bib_url:
        return None
    with urllib.request.urlopen(bib_url, timeout=30) as r:
        return r.read().decode()

def main():
    dry = "--dry-run" in sys.argv
    existing = BIB.read_text(encoding="utf-8") if BIB.exists() else ""
    ids = found_ids()
    print(f"found {len(ids)} arXiv-style IDs in manuscript")
    added = 0
    for aid in ids:
        if aid in existing:
            continue
        print(f"  resolving {aid} ...", end=" ")
        try:
            bib = inspire_bibtex(aid)
        except Exception as e:
            print(f"FAILED ({e})"); continue
        if not bib:
            print("no bibtex"); continue
        key = re.search(r"@\w+\{([^,]+),", bib)
        print(key.group(1) if key else "ok")
        if not dry:
            existing += "\n" + bib
            added += 1
        time.sleep(0.5)  # be polite to INSPIRE
    if not dry and added:
        BIB.write_text(existing, encoding="utf-8")
        print(f"wrote {added} new entries to {BIB.relative_to(REPO)}")

if __name__ == "__main__":
    main()
