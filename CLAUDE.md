# CLAUDE.md — python-content

A **content repo** (not an app) for the `graphl-ux` engine. It holds the **Python**
concept: notebooks, per-section narration, and the `manifest.json` that wires them.
The app fetches this repo's `manifest.json` + notebooks over the network and renders
them. Read `README.md` first; this file is the working orientation.

This repo is a sibling of `apache-spark-content` / `java-content` / `scala-content`
and follows the **same contract** — when in doubt, mirror what those repos do (the
`apache-spark-content` `CLAUDE.md`/`DESIGN.md`/`MODULES.md` are the mature reference,
especially the **TTS guidelines** and the **fixed semantic palette**).

## The core contract (do not break)

1. **The notebook is the single source of truth** for prose and code. `manifest.json`
   only *wires* sections — never duplicate notebook content here.
2. The app splits each notebook at every `## ` heading into sections (= pages) and
   matches them to the manifest by **normalized heading** (lowercase, backticks
   stripped, whitespace collapsed — see graphl-ux `content/module.ts`). A heading edit
   in a notebook must be mirrored in the manifest `heading`.
3. Section diagram **images are stripped** by the app — a **scene** replaces them.
4. **Scenes live in `graphl-ux`** (`src/scenes`), authored in TypeScript — not here.
   The `scenes/` dir is reserved/empty. Reference a scene by **id** only.

## The Python scenes (to be ported into graphl-ux)

Two dense maps, authored in NodeMap and **not yet ported** to graphl-ux (so they are
listed `status: "todo"` in the manifest). When ported, register them in
`graphl-ux/src/scenes/index.ts` under these ids, **preserving the NodeMap node ids**
(the manifest's `highlight`/`focus` reference them verbatim — exactly how `java-jvm` /
`java-anatomy` preserved NodeMap's `j-*` / `ja-*` ids):

- **`python-cpython`** — the runtime, ported from
  `~/Projects/NodeMap/src/data/scenes/python.ts` (title "Python on CPython", parallel
  to `java-jvm`). Source pipeline (`.py` → `compile()` → `.pyc`) → import sub-system
  (finders/loaders/initialization) → CPython runtime (GIL / object heap / pymalloc /
  per-thread state) → execution engine (CEval loop / specializer+JIT / GC) → C API →
  CPU. Node ids include: `py-pipeline`, `py-source`, `py-compiler`, `pyc-file`,
  `import-subsystem`, `path-finder`, `source-loader`, `py-initialization`, `gil`,
  `sys-modules`, `interp-state`, `object-heap`, `pyobject`, `code-object`,
  `module-dicts`, `pymalloc`, `per-thread`, `thread-1`, `thread-n`, `frames-1`,
  `memory-area-py`, `exec-engine-py`, `ceval`, `specializer`, `gc-py`, `c-api`,
  `native-ext`, `cpu-py`.
- **`python-anatomy`** — the language grammar, ported from
  `~/Projects/NodeMap/src/data/scenes/python-anatomy.ts` (title "Python — Anatomy",
  parallel to `java-anatomy`). Four rhythm rows — **Model ▸ Bind ▸ Transform ▸
  Return** (Python's binding has no `val/var`/type keyword: `x [: Type] = value`) —
  plus a Memory column. Node ids are `pa-*`: `pa-model`, `pa-oop-animal`,
  `pa-oop-walker`, `pa-oop-mammal`, `pa-oop-dog`, `pa-bind-row`, `pa-name`, `pa-type`
  (+ `pa-t-prim`/`pa-t-prim-int|str|bool|float`, `pa-t-generic`, `pa-t-custom`,
  `pa-t-optional`, `pa-t-callable`, `pa-t-protocol`), `pa-value`
  (+ `pa-value-primitive|container|object|fn|module`), `pa-verbs`, `pa-comp`
  (+ `pa-comp-list|dict|set|gen`), `pa-control` (+ `pa-ctrl-if|tern|walrus|bool`),
  `pa-loops` (+ `pa-loop-for|while|util|break|yield`), `pa-fn`
  (+ `pa-fn-def|deco|varargs`), `pa-context` (+ `pa-ctx-with|unpack|star`), `pa-match`
  (+ `pa-match-stmt|dest`), `pa-results` (+ `pa-ret-value|yield|raise|mutate`),
  `pa-memory` (+ `pa-mem-stack`, `pa-mem-heap`/`pa-mem-heap-type|val|refs`,
  `pa-mem-gc`, `pa-mem-gil`).

Highlighting a container id lights its children, so spotlight the box (`pa-type`,
`pa-loops`, `import-subsystem`, `per-thread`) to light a whole group. The full id
lists live in the two NodeMap source files — check them before adding a
`highlight`/`focus`.

## manifest.json shape

Top level: `concept`, `design`, `scenes[]` (id/title/status), `presentations[]` (one
per module). Each presentation: `id`, `title`, `notebook`, `defaultScene`,
`sections[]`. Each section overlay: `heading` (must match a notebook `## ` heading,
normalized), `scene`, `spine` (bool — feed-mode narration), optional `role` (`"hook"`),
optional `audio` (repo-relative `.wav`), optional `highlight` (scene node ids — AMBER,
rest dim), optional `focus` (node id(s) the camera frames).

**Do not hand-edit `manifest.json`** — it is generated. Edit
`scripts/gen_manifest.py` (the per-section `(scene, spine, highlight, focus, role)`
rows live in its `MAP`) and re-run it. Each module rides one of the two scenes;
module 01 (intro/runtime) and module 09 (concurrency/GIL) use `python-cpython`, the
rest use `python-anatomy`, and module 06's "Part 3 — Modules and packages" sections
switch to `python-cpython` to light the import sub-system.

## Narration

One `.tts` per section, plain spoken prose. Naming `tts/<NN>-<SS>-<slug>.tts` →
`audio/<NN>-<SS>-<slug>.wav`; the stem is shared by the `.tts`, the `.wav`, and the
manifest `audio` field. **Drop the notebook's "What's covered" overview and the
trailing "What's next" outro** — those are reading-only, not narrated. Follow
`apache-spark-content/CLAUDE.md` "TTS guidelines" verbatim (no markdown/code, spell
out symbols/acronyms — e.g. GIL → "global interpreter lock", `==` → "double equals",
`:=` → "walrus", `.py` → "dot p-y").

The source curriculum at `~/Projects/python/tts/` has **one `.tts` per notebook** (a
monologue with the coverage-map intro and "What's next" outro). The per-section files
here were **split** from that prose by `scripts/split_tts.py`, anchored to each
notebook's `## ` headings (intro + outro dropped). Re-run that script to regenerate.

## Regenerating

```
python3 scripts/split_tts.py --write   # tts/  (split from ~/Projects/python/tts/*.tts)
python3 scripts/gen_manifest.py        # manifest.json
```

Both are deterministic and assert that every notebook's heading count matches its
hand-authored row count, so a notebook edit that adds/removes a `## ` section fails
loudly until the `MAP` is updated.

## When wiring a module

1. Confirm the notebook is in `notebooks/` and its `## ` headings are final.
2. Add/adjust the module's row list in `scripts/gen_manifest.py` `MAP` (one
   `(scene, spine, highlight, focus, role)` tuple per `## ` section, in order);
   re-run it. List every section (each becomes a page).
3. Set `scene` per section (`python-cpython` for runtime/import topics,
   `python-anatomy` for language-grammar topics), `spine` for essentials,
   `role: "hook"` on the first.
4. Re-run `scripts/split_tts.py --write`, set each `audio` (the generator already
   does), then run `scripts/colab_generate_audio.ipynb` to generate + push the `.wav`s.

## Status

- **All 10 modules (core Python)** scene-wired AND narrated in `manifest.json`
  (scene/spine/highlight/focus/role + per-section `audio`). **187** `tts/*.tts`
  scripts, 1:1 with the manifest `audio` stems. `.wav`s pending Colab.
- The two scenes `python-cpython` + `python-anatomy` are **not yet ported** into
  graphl-ux (`status: "todo"` in the manifest) — they exist only in NodeMap. They
  must be ported (preserving node ids) and registered before the app can render this
  concept.
- Not yet pushed; not yet in the app catalog (`graphl-ux/src/content/catalog.ts`).
- Notebooks copied as-is from the runnable curriculum at `~/Projects/python`.
