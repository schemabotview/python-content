#!/usr/bin/env python3
"""Generate python-content/manifest.json. Pulls exact `## ` headings from each
notebook (dropping "What's covered" / "What's next"), pairs them in order with a
hand-authored (scene, spine, highlight, focus, role) row, and emits the manifest.
SS runs sequentially over the wired sections; the tts/audio stem = f"{NN}-{SS}-{slug}".

Two Python scenes are referenced by id (authored in graphl-ux/src/scenes, ported
from NodeMap's python.ts + python-anatomy.ts — parallels java-jvm/java-anatomy):
  - python-cpython : the CPython runtime map (node ids from NodeMap python.ts —
        gil, ceval, py-pipeline, import-subsystem, per-thread, exec-engine-py, ...)
  - python-anatomy : the language grammar map (node ids `pa-*` from python-anatomy.ts)
"""
import json, re
from pathlib import Path

NB_DIR = Path.home() / "Projects/python"
OUT = Path("/Users/maddipotiganesh/Products/python-content/manifest.json")
DROP = {"what's covered", "what's next"}

R = "python-cpython"   # runtime scene
A = "python-anatomy"   # language-grammar scene

def slug(s: str) -> str:
    s = s.lower().replace("`", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    if len(s) > 42:
        cut = s[:42].rsplit("-", 1)[0]
        s = cut or s[:42]
    return s.strip("-")

def headings(stem: str):
    nb = json.load(open(NB_DIR / f"{stem}.ipynb"))
    out = []
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        for line in c["source"]:
            t = line.rstrip("\n")
            if t.startswith("## ") and not t.startswith("### "):
                out.append(t[3:].strip())
    return [h for h in out if h.strip().lower().rstrip(".") not in DROP]

# (scene, spine, [highlight...], [focus...], role|None) per wired section, in order.
MAP = {
"01-intro-and-setup": (R, [
  (R, True,  [], [], "hook"),
  (R, True,  [], [], None),
  (R, True,  ["py-compiler", "pyc-file", "ceval"], ["py-pipeline", "exec-engine-py"], None),
  (R, True,  [], [], None),
  (R, True,  ["py-source", "py-compiler", "pyc-file", "ceval"], ["py-pipeline", "exec-engine-py"], None),
  (R, False, [], [], None),
  (R, True,  ["path-finder", "sys-modules"], ["import-subsystem"], None),
  (R, False, ["path-finder"], ["import-subsystem"], None),
  (R, False, [], [], None),
  (R, True,  ["ceval"], ["exec-engine-py"], None),
  (R, False, ["ceval"], ["exec-engine-py"], None),
  (R, False, ["ceval"], ["exec-engine-py"], None),
  (R, False, ["import-subsystem"], ["import-subsystem"], None),
  (R, False, [], [], None),
  (R, True,  ["gil"], ["interp-state"], None),
]),
"02-values-types-operators-expressions": (A, [
  (A, True,  ["pa-name", "pa-mem-stack"], ["pa-bind-row"], "hook"),
  (A, True,  ["pa-value", "pa-mem-heap"], ["pa-mem-heap"], None),
  (A, True,  ["pa-type", "pa-t-prim"], ["pa-type"], None),
  (A, False, ["pa-t-prim-int", "pa-t-prim-float"], ["pa-t-prim"], None),
  (A, True,  ["pa-t-prim-str", "pa-value-primitive"], ["pa-value"], None),
  (A, False, ["pa-t-optional"], ["pa-type"], None),
  (A, False, ["pa-value-primitive"], ["pa-bind-row"], None),
  (A, False, ["pa-ctrl-bool"], ["pa-control"], None),
  (A, True,  ["pa-ctrl-bool"], ["pa-control"], None),
  (A, True,  ["pa-mem-stack", "pa-mem-heap-refs"], ["pa-memory"], None),
  (A, True,  ["pa-ctrl-if"], ["pa-control"], None),
  (A, True,  ["pa-mem-heap", "pa-mem-heap-refs"], ["pa-memory"], None),
  (A, False, ["pa-type"], ["pa-type"], None),
  (A, True,  ["pa-ctrl-walrus"], ["pa-control"], None),
  (A, False, ["pa-value-primitive"], ["pa-bind-row"], None),
]),
"03-control-flow-and-functions": (A, [
  (A, True,  ["pa-control", "pa-loops"], ["pa-verbs"], "hook"),
  (A, True,  ["pa-ctrl-if"], ["pa-control"], None),
  (A, True,  ["pa-ctrl-tern"], ["pa-control"], None),
  (A, True,  ["pa-loop-while"], ["pa-loops"], None),
  (A, True,  ["pa-loop-for"], ["pa-loops"], None),
  (A, False, ["pa-loop-for"], ["pa-loops"], None),
  (A, False, ["pa-loop-break"], ["pa-loops"], None),
  (A, False, ["pa-loop-break"], ["pa-loops"], None),
  (A, True,  ["pa-match", "pa-match-stmt", "pa-match-dest"], ["pa-match"], None),
  (A, False, ["pa-ctrl-if"], ["pa-control"], None),
  (A, True,  ["pa-fn"], ["pa-fn"], None),
  (A, True,  ["pa-fn-def"], ["pa-fn"], None),
  (A, True,  ["pa-fn-def"], ["pa-fn"], None),
  (A, True,  ["pa-fn-varargs", "pa-mem-heap"], ["pa-fn"], None),
  (A, True,  ["pa-fn-varargs"], ["pa-fn"], None),
  (A, False, ["pa-fn-def"], ["pa-fn"], None),
  (A, True,  ["pa-fn-def", "pa-value-fn"], ["pa-fn"], None),
  (A, True,  ["pa-mem-stack"], ["pa-memory"], None),
  (A, True,  ["pa-value-fn", "pa-mem-heap"], ["pa-fn"], None),
  (A, True,  ["pa-value-fn"], ["pa-value"], None),
  (A, False, ["pa-fn-def"], ["pa-fn"], None),
]),
"04-collections-and-comprehensions": (A, [
  (A, True,  ["pa-value-container"], ["pa-value"], "hook"),
  (A, True,  ["pa-loop-for"], ["pa-loops"], None),
  (A, True,  ["pa-value-container"], ["pa-value"], None),
  (A, True,  ["pa-value-container"], ["pa-value"], None),
  (A, True,  ["pa-ctx-unpack", "pa-ctx-star"], ["pa-context"], None),
  (A, True,  ["pa-value-container"], ["pa-value"], None),
  (A, False, ["pa-t-prim-str"], ["pa-value"], None),
  (A, True,  ["pa-value-container"], ["pa-value"], None),
  (A, True,  ["pa-comp-dict", "pa-value-container"], ["pa-value"], None),
  (A, False, ["pa-value-container"], ["pa-value"], None),
  (A, False, ["pa-value-container"], ["pa-value"], None),
  (A, True,  ["pa-comp-set", "pa-value-container"], ["pa-value"], None),
  (A, True,  ["pa-mem-heap-type"], ["pa-memory"], None),
  (A, True,  ["pa-comp"], ["pa-comp"], None),
  (A, True,  ["pa-comp-list"], ["pa-comp"], None),
  (A, True,  ["pa-comp-set", "pa-comp-dict"], ["pa-comp"], None),
  (A, True,  ["pa-comp-gen"], ["pa-comp"], None),
  (A, False, ["pa-comp-list"], ["pa-comp"], None),
  (A, False, ["pa-ctrl-walrus", "pa-comp-list"], ["pa-comp"], None),
  (A, False, ["pa-comp"], ["pa-comp"], None),
]),
"05-oop": (A, [
  (A, True,  ["pa-oop-dog"], ["pa-model"], "hook"),
  (A, True,  ["pa-mem-heap-val"], ["pa-model"], None),
  (A, False, ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-name"], ["pa-bind-row"], None),
  (A, True,  ["pa-fn-deco"], ["pa-fn"], None),
  (A, True,  ["pa-fn-deco", "pa-value-object"], ["pa-model"], None),
  (A, False, ["pa-value-container", "pa-t-custom"], ["pa-type"], None),
  (A, True,  ["pa-oop-mammal", "pa-oop-dog"], ["pa-model"], None),
  (A, True,  ["pa-oop-animal", "pa-oop-walker", "pa-oop-mammal"], ["pa-model"], None),
  (A, False, ["pa-oop-walker"], ["pa-model"], None),
  (A, True,  ["pa-oop-animal", "pa-t-protocol"], ["pa-model"], None),
  (A, True,  ["pa-fn-def"], ["pa-fn"], None),
  (A, False, ["pa-mem-heap", "pa-mem-heap-val"], ["pa-memory"], None),
  (A, True,  ["pa-t-protocol", "pa-oop-walker"], ["pa-model"], None),
  (A, False, ["pa-value-fn"], ["pa-value"], None),
]),
"06-errors-files-modules": (A, [
  (A, True,  ["pa-ret-raise"], ["pa-results"], "hook"),
  (A, True,  ["pa-ret-raise"], ["pa-results"], None),
  (A, True,  ["pa-ret-raise"], ["pa-results"], None),
  (A, True,  ["pa-ret-raise"], ["pa-results"], None),
  (A, True,  ["pa-ret-raise"], ["pa-results"], None),
  (A, False, ["pa-ret-raise", "pa-oop-dog"], ["pa-results"], None),
  (A, True,  ["pa-ret-raise"], ["pa-results"], None),
  (A, True,  ["pa-ctx-with"], ["pa-context"], None),
  (A, False, ["pa-ctx-with"], ["pa-context"], None),
  (A, False, ["pa-ret-raise"], ["pa-results"], None),
  (A, True,  ["pa-ctx-with"], ["pa-context"], None),
  (A, True,  ["pa-ctx-with"], ["pa-context"], None),
  (A, False, ["pa-ctx-with"], ["pa-context"], None),
  (A, True,  ["pa-value-object"], ["pa-value"], None),
  (A, False, ["pa-ctx-with"], ["pa-context"], None),
  (R, True,  ["import-subsystem"], ["import-subsystem"], None),
  (R, True,  ["module-dicts", "sys-modules"], ["object-heap"], None),
  (R, True,  ["import-subsystem", "sys-modules"], ["import-subsystem"], None),
  (R, True,  ["py-initialization"], ["import-subsystem"], None),
  (R, True,  ["path-finder", "sys-modules"], ["import-subsystem"], None),
  (R, False, ["path-finder"], ["import-subsystem"], None),
  (R, False, ["source-loader", "path-finder"], ["import-subsystem"], None),
]),
"07-iterators-generators-decorators": (A, [
  (A, True,  ["pa-loop-for"], ["pa-loops"], "hook"),
  (A, True,  ["pa-loop-for"], ["pa-loops"], None),
  (A, True,  ["pa-loop-for", "pa-oop-dog"], ["pa-loops"], None),
  (A, True,  ["pa-loop-for"], ["pa-loops"], None),
  (A, False, ["pa-comp-gen"], ["pa-loops"], None),
  (A, True,  ["pa-loop-yield", "pa-ret-yield"], ["pa-loops"], None),
  (A, True,  ["pa-loop-yield", "pa-ret-yield"], ["pa-loops"], None),
  (A, True,  ["pa-comp-gen", "pa-ret-yield"], ["pa-results"], None),
  (A, False, ["pa-loop-yield"], ["pa-loops"], None),
  (A, True,  ["pa-comp-gen", "pa-ret-yield"], ["pa-results"], None),
  (A, False, ["pa-loop-yield"], ["pa-loops"], None),
  (A, True,  ["pa-fn-deco"], ["pa-fn"], None),
  (A, True,  ["pa-fn-deco", "pa-value-fn"], ["pa-fn"], None),
  (A, False, ["pa-fn-deco"], ["pa-fn"], None),
  (A, True,  ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-fn-deco", "pa-oop-dog"], ["pa-fn"], None),
  (A, False, ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-fn-deco"], ["pa-fn"], None),
]),
"08-type-hints-and-best-practices": (A, [
  (A, True,  ["pa-type"], ["pa-type"], "hook"),
  (A, True,  ["pa-type"], ["pa-type"], None),
  (A, True,  ["pa-t-prim", "pa-t-generic", "pa-t-callable"], ["pa-type"], None),
  (A, True,  ["pa-t-optional"], ["pa-type"], None),
  (A, False, ["pa-t-custom"], ["pa-type"], None),
  (A, False, ["pa-t-generic"], ["pa-type"], None),
  (A, True,  ["pa-t-protocol"], ["pa-type"], None),
  (A, True,  ["pa-t-generic", "pa-t-custom"], ["pa-type"], None),
  (A, False, ["pa-type"], ["pa-type"], None),
  (A, True,  ["pa-type"], ["pa-type"], None),
  (A, True,  ["pa-name"], ["pa-bind-row"], None),
  (A, True,  ["pa-name"], ["pa-bind-row"], None),
  (A, False, ["pa-name"], ["pa-bind-row"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, False, ["pa-ret-mutate"], ["pa-results"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, True,  ["pa-mem-heap"], ["pa-memory"], None),
  (A, False, ["pa-name"], ["pa-bind-row"], None),
]),
"09-concurrency-threading-multiprocessing-asyncio": (R, [
  (R, True,  ["gil"], ["interp-state"], "hook"),
  (R, True,  ["per-thread"], ["memory-area-py"], None),
  (R, True,  ["gil", "ceval"], ["exec-engine-py"], None),
  (R, True,  ["per-thread", "thread-1", "thread-n"], ["per-thread"], None),
  (R, True,  ["thread-1", "thread-n"], ["per-thread"], None),
  (R, True,  ["gil"], ["interp-state"], None),
  (R, True,  ["gil", "object-heap"], ["interp-state"], None),
  (R, True,  ["per-thread"], ["per-thread"], None),
  (R, True,  ["thread-1", "thread-n", "cpu-py"], ["per-thread"], None),
  (R, False, ["code-object", "object-heap"], ["object-heap"], None),
  (R, True,  ["ceval", "frames-1"], ["exec-engine-py"], None),
  (R, True,  ["frames-1", "ceval"], ["exec-engine-py"], None),
  (R, False, ["frames-1"], ["exec-engine-py"], None),
  (R, True,  ["gil", "per-thread"], ["interp-state"], None),
  (R, False, ["per-thread", "ceval"], ["exec-engine-py"], None),
  (R, True,  ["gil"], ["interp-state"], None),
  (R, False, ["gil", "per-thread"], ["memory-area-py"], None),
  (R, True,  ["gil"], ["interp-state"], None),
]),
"10-testing-with-pytest": (A, [
  (A, True,  ["pa-results"], ["pa-results"], "hook"),
  (A, True,  ["pa-ret-value"], ["pa-results"], None),
  (A, True,  ["pa-fn-def"], ["pa-fn"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, True,  ["pa-ret-raise"], ["pa-results"], None),
  (A, True,  ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-ctx-with"], ["pa-context"], None),
  (A, True,  ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-fn-deco"], ["pa-fn"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, True,  ["pa-ret-mutate"], ["pa-results"], None),
  (A, False, ["pa-ret-value"], ["pa-results"], None),
  (A, False, ["pa-ret-value"], ["pa-results"], None),
  (A, True,  ["pa-value-module"], ["pa-value"], None),
  (A, False, ["pa-value-object"], ["pa-value"], None),
  (A, False, ["pa-value-object"], ["pa-value"], None),
  (A, True,  ["pa-value-container"], ["pa-value"], None),
  (A, False, ["pa-t-prim-str"], ["pa-value"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, False, ["pa-value-module"], ["pa-value"], None),
  (A, True,  [], [], None),
]),
}

TITLES = {
  "01-intro-and-setup": "Intro & Setup",
  "02-values-types-operators-expressions": "Values, Types, Operators & Expressions",
  "03-control-flow-and-functions": "Control Flow & Functions",
  "04-collections-and-comprehensions": "Collections & Comprehensions",
  "05-oop": "Object-Oriented Programming",
  "06-errors-files-modules": "Errors, Files & Modules",
  "07-iterators-generators-decorators": "Iterators, Generators & Decorators",
  "08-type-hints-and-best-practices": "Type Hints & Best Practices",
  "09-concurrency-threading-multiprocessing-asyncio": "Concurrency — Threading, Multiprocessing & Asyncio",
  "10-testing-with-pytest": "Testing with pytest & the Standard Library",
}

presentations = []
for stem, (default_scene, rows) in MAP.items():
    nn = stem.split("-")[0]
    heads = headings(stem)
    assert len(heads) == len(rows), f"{stem}: {len(heads)} headings vs {len(rows)} rows"
    sections = []
    for i, (h, (scene, spine, hi, fo, role)) in enumerate(zip(heads, rows), start=1):
        ss = f"{i:02d}"
        st = f"{nn}-{ss}-{slug(h)}"
        sec = {"heading": h, "scene": scene, "spine": spine}
        if role:
            sec["role"] = role
        if hi:
            sec["highlight"] = hi
        if fo:
            sec["focus"] = fo
        sec["audio"] = f"audio/{st}.wav"
        sections.append(sec)
    presentations.append({
        "id": stem,
        "title": TITLES[stem],
        "notebook": f"notebooks/{stem}.ipynb",
        "defaultScene": default_scene,
        "sections": sections,
    })

manifest = {
    "concept": "Python",
    "design": "DESIGN.md",
    "scenes": [
        {"id": "python-cpython", "title": "Python on CPython", "status": "built"},
        {"id": "python-anatomy", "title": "Python — Anatomy", "status": "built"},
    ],
    "presentations": presentations,
}

OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
n = sum(len(p["sections"]) for p in presentations)
print(f"wrote {OUT} — {len(presentations)} modules, {n} wired sections")
