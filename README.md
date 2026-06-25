# python-content

A **content repo** for the `graphl-ux` learning app (sibling repo). It holds the
**Python** concept — notebooks, per-section narration scripts, and the `manifest.json`
that wires sections to scenes — fetched by the app **at runtime** over raw GitHub.

There is **nothing to build, run, or test** here. Correctness is verified by the
`graphl-ux` app consuming this content. The executables are tools:
`scripts/split_tts.py` (splits the source monologues into per-section scripts),
`scripts/gen_manifest.py` (emits `manifest.json`), and
`scripts/colab_generate_audio.ipynb` (turns `tts/` scripts into `audio/` `.wav`s).

## Layout

```
manifest.json   # GENERATED — wires each module: notebook ref + per-section overlay
                #   (scene/spine/role/audio/highlight/focus). Edit gen_manifest.py, not this.
notebooks/      # the teaching .ipynb (prose + code source of truth) — 01..10
tts/            # per-section narration scripts (plain spoken prose) — 187 files
audio/          # generated .wav narration (per-section) — generated on Colab
scenes/         # reserved/empty — real scenes live in the graphl-ux app (src/scenes)
scripts/        # split_tts.py · gen_manifest.py · colab_generate_audio.ipynb
```

## The contract (shared with apache-spark-content)

1. **The notebook is the single source of truth** for a module's prose and code.
   The `manifest.json` only *wires* — it must never duplicate notebook content.
2. The app splits each notebook at every `## ` heading into **sections** (= pages),
   matched to the manifest overlay by **normalized heading text** (case / backticks /
   whitespace insensitive). A heading edit in a notebook must be mirrored here.
3. A section's diagram **images are stripped** by the app — a **scene** replaces them.
4. **Scenes live in `graphl-ux`** (`src/scenes`), authored in TypeScript — not here.
   The Python concept's two maps are `python-cpython` (the CPython runtime) and
   `python-anatomy` (the language grammar). Here you only reference a scene **by id**.

## Narration (per-section TTS)

One `.tts` script **per section**, plain spoken prose — what a teacher would say at a
whiteboard. Naming: `tts/<NN>-<SS>-<slug>.tts` → `audio/<NN>-<SS>-<slug>.wav`, where
`NN` is the module number and `SS` the section order. The stem is shared by the
`.tts`, the `.wav`, and the manifest `audio` field. The notebook's "What's covered"
overview and the trailing "What's next" outro are dropped — those are reading-only.

See `apache-spark-content/CLAUDE.md` "TTS guidelines" for the full style rules (plain
prose, no markdown/code, spell out symbols and acronyms).

## How content is served

The app fetches this repo at runtime over **raw GitHub**:
`https://raw.githubusercontent.com/schemabotview/python-content/main/…`
A content change is live once pushed to `main` — no app rebuild needed.

## Source

Notebooks are copied as-is from the runnable curriculum at `~/Projects/python`; the
per-section `.tts` scripts are split from that repo's per-notebook narration. The two
scenes are ported from NodeMap (`python.ts`, `python-anatomy.ts`).

## Status

- 10 notebooks copied in; **all 10 modules wired** in `manifest.json` (each section
  mapped to `python-cpython` or `python-anatomy` with `spine`/`highlight`/`focus`/`role`).
- **Fully narrated** — 187 per-section `tts/*.tts` scripts, each wired to a matching
  `audio/*.wav` stem; the per-section `.wav`s still need a Colab generation pass.
- The two scenes are authored in NodeMap but **not yet ported to graphl-ux**
  (`status: "todo"`), and the concept is **not yet in the app catalog** — both are
  follow-ups, along with the first push to GitHub.
