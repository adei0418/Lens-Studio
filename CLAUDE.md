# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this repository is

This is the **Lens Studio Templates** collection — the set of starter/template projects
that ship inside [Lens Studio](https://lensstudio.snapchat.com), Snap's authoring tool for
augmented‑reality "Lenses." It is **not** an application with source code that compiles. It is
a curated library of 50 self‑contained Lens Studio projects, each demonstrating a feature or
use case. Per‑template guides live on the [documentation site](https://lensstudio.snapchat.com/templates/).

Because the deliverables are Lens Studio projects (mostly binary assets plus embedded
JavaScript), there is **no build system, no package manager, no test suite, and no CI** in the
usual sense. Do not look for `package.json`, `Makefile`, or a `src/` tree — they do not exist.

## Repository layout

Templates are grouped into top‑level category folders by tracking/experience type:

| Category | What the templates target |
|----------|---------------------------|
| `Face/` | Face‑tracking effects (masks, makeup, distort, triggers, segmentation, etc.) |
| `World/` | Rear‑camera / world‑tracking experiences (portals, particles, placed objects) |
| `Interactive/` | Game/UI mechanics (high scores, tap interactions, fullscreen, soundboard) |
| `Object/` | Body/object tracking (hand, pet, shoulder, skeletal) |
| `Landmarker/` | City landmark AR (Eiffel Tower, US Capitol, etc.) |
| `Marker/` | Image‑marker and Snapcode‑triggered AR |
| `Spectacles/` | Spectacles‑device experiences (depth, path) |

### Anatomy of a single template

Each template is a directory `Category/Template Name/` containing:

```
Template Name/
├── Template Name.lsproj    # The Lens Studio project file (JSON manifest)
├── project.data            # Binary scene/asset database (the bulk of the project)
├── icon.png                # Project thumbnail / preview
├── LICENSE.txt             # Per-template license
└── Public/                 # Resources exposed in the project's Resources panel
    ├── Scripts/            # JavaScript behavior scripts (*.js)
    ├── Materials/          # *.lsmat materials
    ├── Meshes/             # *.mesh geometry
    ├── Textures/           # *.png / *.jpg / *.t3d textures
    ├── Tween/              # Bundled tween animation library (see below)
    └── folder.lock         # Folder lock markers (Lens Studio bookkeeping — leave alone)
```

### File formats you will encounter

- **`*.lsproj`** — JSON project manifest (`lens_id`, `document_id`, `version`, preview refs).
  Editable text, but normally only the Lens Studio editor should change it.
- **`project.data`** — binary scene graph + asset database. **Do not hand‑edit.**
- **`*.lsmat`** — binary Lens Studio material. **Do not hand‑edit.**
- **`*.mesh`, `*.t3d`** — binary geometry/texture assets. **Do not hand‑edit.**
- **`*.js`** — the only routinely human‑editable code. See conventions below.
- **`folder.lock`** — empty marker files used by Lens Studio; do not delete or create them.
- **`info.json`** — image‑marker metadata for Marker/Landmarker templates.

## JavaScript scripting conventions

Scripts use Lens Studio's **legacy JavaScript scripting API** (the `script.*` / `global.*`
runtime), not the newer TypeScript component API. Follow the existing style:

- **Script header comment block** at the top of every script:
  ```js
  // ScriptName.js
  // Version: 0.0.2
  // Event: Lens Initialized
  // Description: One-line summary of what the script does
  ```
- **Input declarations** drive the editor's Inspector UI via `// @input` and `// @ui`
  annotations. These are parsed by Lens Studio — keep the exact comment syntax, including the
  JSON widget specs:
  ```js
  // @input float showTime = 2.0 {"label": "Show Time"}
  // @input Component.AnimationMixer AnimationMixer
  // @ui {"widget":"separator"}
  // @ui {"widget":"group_start", "label":"Sound Control"}
  ```
  Declared inputs are accessed at runtime as `script.<inputName>`.
- **Events** are created and bound, e.g.
  `script.createEvent("TapEvent").bind(callback)`.
- **Globals**: the runtime exposes singletons on `global.` — most commonly
  `global.tweenManager`, `global.scene`, `global.touchSystem`, `global.behaviorSystem`.
  Helpers like `getTime()`, `getDeltaTime()`, `print()` are also global.
- **No module system**: there is no `require`/`import` and (outside the Tween library) no
  `module.exports`. Scripts communicate through `script.*` inputs and `global.*`.
- Style in existing scripts is ES5‑flavored (`var`, function declarations). Match the file
  you are editing rather than modernizing it.

### The bundled Tween library

Many templates vendor a copy of [tween.js](https://github.com/tweenjs/tween.js) under
`Public/Tween/` (`Tween.js`, `TweenManager.js`, and `TweenTypes/`). These copies are
duplicated verbatim across ~17 templates. Treat them as **third‑party vendored code** — do not
"refactor" or deduplicate them, and preserve the MIT license header. Files marked
`[DEPRECATED]` (e.g. `TweenBillboard [DEPRECATED].js`) are kept intentionally.

### Placeholder content conventions

Folders tagged in their name signal intent to the template user:

- **`[REPLACE_ME]`** — example content the creator is expected to swap out (e.g.
  `Markers [REPLACE_ME]`, `image_marker [REPLACE_ME]`).
- **`[REMOVE_ME]`** — demo content meant to be deleted before publishing (e.g.
  `Trophy [REMOVE_ME]`, `Pet Template Content [REMOVE_ME]`).

Preserve these naming tags; they are a deliberate part of the template UX.

## Development workflow

There is no compile/run step in this repo. The real authoring loop happens **inside Lens
Studio**, where a `.lsproj` is opened, edited, previewed, and exported. In this repository the
practical workflow is:

1. **Edits** are typically limited to `*.js` scripts, `README.md`, or `*.lsproj` text fields.
   Binary assets (`project.data`, `*.lsmat`, `*.mesh`, `*.t3d`, media) are produced by Lens
   Studio and should not be edited by hand.
2. **Adding/updating templates** is done in bulk per Lens Studio release. Git history shows
   the pattern: each release adds a batch of templates via a PR titled like
   `adding templates from release 2.3`. New template versions are merged in wholesale rather
   than incrementally diffed.
3. **No automated verification exists.** You cannot "run the tests" or "build" here. If you
   change a script, reason about correctness against the Lens Studio scripting API; you cannot
   execute it without the editor.

### Git conventions

- Develop on the branch selected by the user or the environment for the current task; create it
  locally if it doesn't exist. Do not push to `main` or other branches without explicit
  permission.
- Always push with `git push -u origin <branch-name>`; retry network failures with exponential
  backoff.
- **Do not open a pull request unless explicitly asked.**
- Commit messages: clear and descriptive. Match the existing terse, release‑oriented style for
  template additions.

## Guidance for AI assistants

- **Stay surgical.** This repo is overwhelmingly binary template data. Confine edits to text
  files (`*.js`, `*.lsproj` fields, markdown) unless explicitly told otherwise.
- **Never hand‑edit binaries** (`project.data`, `*.lsmat`, `*.mesh`, `*.t3d`, images, audio,
  fonts). They cannot be meaningfully patched outside Lens Studio and will corrupt the project.
- **Respect editor‑managed artifacts**: `folder.lock`, `// @input`/`// @ui` comment syntax,
  `document_id`/`version` fields in `.lsproj`, and the `[REPLACE_ME]`/`[REMOVE_ME]` folder tags.
- **Preserve per‑template `LICENSE.txt`** files and the vendored Tween MIT headers.
- When editing a script, **match the existing ES5 style and header‑comment format** of the file
  rather than introducing new patterns or a module system.
- Each template is **self‑contained**; a change to one template's script does not propagate to
  the duplicated copies in other templates. Update each one deliberately if a cross‑template
  change is intended.

## License

Each template ships its own `LICENSE.txt`. Full terms:
[https://lensstudio.snapchat.com/template-license](https://lensstudio.snapchat.com/template-license).
