#!/usr/bin/env python3
"""Split the source per-notebook narration monologues at
`~/Projects/python/tts/<stem>.tts` into per-section scripts
`python-content/tts/<NN>-<SS>-<slug>.tts`.

The source `.tts` is one spoken monologue per notebook: a title line, a "What is
covered" overview, then for every `## ` section a short spoken heading paragraph
followed by its body, and a trailing "What's next" outro. The app pages per `## `
section, so narration must be per section too.

Strategy: pull the notebook's ordered `## ` headings (the real sections, plus the
trailing "What's next" as a cut-point), then walk the monologue's paragraphs and
fuzzy-match each expected heading in order to find section boundaries. Everything
before the first section = the overview (dropped); everything from "What's next"
on = the outro (dropped). Each emitted file is the section's spoken heading +
body, unchanged prose.
"""
import json, re, glob, sys
from pathlib import Path
from difflib import SequenceMatcher

SRC_NB = Path.home() / "Projects/python"
SRC_TTS = SRC_NB / "tts"
OUT = Path("/Users/maddipotiganesh/Products/python-content/tts")
DROP = {"what's covered", "what's next"}

def slug(s: str) -> str:
    s = s.lower().replace("`", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    if len(s) > 42:
        cut = s[:42].rsplit("-", 1)[0]
        s = cut or s[:42]
    return s.strip("-")

def headings(stem):
    nb = json.load(open(SRC_NB / f"{stem}.ipynb"))
    out = []
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        for line in c["source"]:
            t = line.rstrip("\n")
            if t.startswith("## ") and not t.startswith("### "):
                out.append(t[3:].strip())
    return [h for h in out if h.strip().lower().rstrip(".") not in DROP]

STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "for", "on",
        "with", "that", "it", "its", "as", "you", "your", "not", "but", "this",
        "these", "how", "what", "when", "where", "s", "i", "be", "do", "does"}

def words(s):
    # letters-only tokens; digits dropped (spoken form expands them to words)
    s = s.lower().replace("`", " ")
    s = re.sub(r"[^a-z]+", " ", s)
    return [w for w in s.split() if w]

def sig(s):
    return [w for w in words(s) if w not in STOP]

def norm(s):
    return "".join(words(s))

def is_boundary(head, para):
    # heading paragraphs are short single sentences; bodies run long
    if len(para) > 200:
        return False
    hw, pw = set(sig(head)), set(sig(para))
    inter = hw & pw
    score = max(len(inter) / len(hw), len(inter) / len(pw)) if hw and pw else 0.0
    ratio = SequenceMatcher(None, norm(head), norm(para)).ratio()
    # fallback for retitled headings (e.g. "The itertools module." for the heading
    # "`itertools` — the standard library's iterator toolbox"): a long heading word
    # surfacing in a *very short* paragraph. Kept tight (len>=7, para<=65) so common
    # domain words like "python"/"decorators" in body sentences don't false-trigger.
    long_hit = any(w in pw for w in hw if len(w) >= 7)
    return score >= 0.55 or ratio >= 0.6 or (long_hit and len(para) <= 65)

def is_outro(para):
    # the dropped "What's next" heading: a short paragraph turning to "next"
    return len(para) <= 120 and "next" in words(para)

def split_one(stem, write=False):
    heads = headings(stem)
    raw = (SRC_TTS / f"{stem}.tts").read_text()
    paras = [p.strip() for p in re.split(r"\n\s*\n", raw) if p.strip()]
    # locate each real heading's paragraph index, in order
    idx = []
    hp = 0
    for i, p in enumerate(paras):
        if hp < len(heads) and is_boundary(heads[hp], p):
            idx.append(i); hp += 1
    ok = (hp == len(heads))
    # end of the last section: cut at a trailing "What's next" outro if present,
    # otherwise the final section runs to the end of the monologue
    end = len(paras)
    if ok:
        for j in range(idx[-1] + 1, len(paras)):
            if is_outro(paras[j]):
                end = j
                break
    nn = stem.split("-")[0]
    results = []
    if ok:
        bounds = idx + [end]
        for s in range(len(heads)):
            body = "\n\n".join(paras[bounds[s]: bounds[s + 1]])
            ss = f"{s+1:02d}"
            fn = f"{nn}-{ss}-{slug(heads[s])}.tts"
            results.append((fn, heads[s], body))
            if write:
                (OUT / fn).write_text(body.rstrip() + "\n")
    return heads, idx, ok, results

if __name__ == "__main__":
    write = "--write" in sys.argv
    total = 0
    allok = True
    for f in sorted(glob.glob(str(SRC_NB / "*.ipynb"))):
        stem = Path(f).stem
        heads, idx, ok, results = split_one(stem, write=write)
        status = "OK " if ok else "FAIL"
        print(f"[{status}] {stem}: matched {len(idx)}/{len(heads)} headings")
        if not ok:
            allok = False
            print(f"        stalled expecting: {heads[len(idx)]!r}")
        total += len(results)
    print(f"\n{'WROTE' if write else 'DRY-RUN'} {total} section files. all_ok={allok}")
