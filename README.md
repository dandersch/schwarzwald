# Schwarzwald

A shared dark palette for Doom Emacs, Neovim/Colorbuddy, and daisyUI 5.

**Edit `tokens.json` only for theme changes.** The three root theme files are
generated, checked in for installation without build tools, and must not be
edited by hand. Generation needs Python 3.10+ and no third-party packages:

```sh
python3 generate.py
python3 generate.py --check
python3 -B -m unittest -v
```

CI checks that outputs match the canonical definition and exercises palette
propagation, independent semantic roles, shared surfaces, and invalid aliases.
`--check` never writes files. Generation validates and renders all three outputs
before writing any of them. Run the same commands after every token change.

## Token organization

`tokens.json` uses the [DTCG 2025.10 format](https://www.designtokens.org/tr/2025.10/format/)
and [color values](https://www.designtokens.org/tr/2025.10/color/):

- `palette.base00`–`palette.base0F`: the canonical Base16-style palette. The
  neutral ramp runs from `#18191b` to white; the chromatic slots are error red,
  string/number brown, keyword yellow, green, teal, blue, purple, and deletion red.
  `base07` aliases `base06`: there is no invented extra white. Emacs's `base0`–
  `base8` symbols are Doom variables, **not** Base16 slot names.
- `palette.selection`: the existing dark selection blue, beyond the Base16 ramp.
- `semantic`: aliases for background, foreground, accents, syntax, selection,
  state, and platform roles. `semantic.foreground` uses `base06` (white), not
  Base16's customary `base05`; `base05` preserves Emacs's softer `#dfdfdf` text.
  Changing a palette value affects every alias to it. Changing a semantic alias
  affects that role without recoloring unrelated uses of the same palette slot.
- `$extensions.org.schwarzwald`: platform bindings. Emacs binding and face forms
  retain Doom's native runtime expressions; Neovim records specify highlight
  groups; daisyUI properties map to typed tokens. These are adapter metadata, not
  custom DTCG token types. Keeping the bindings here also makes new highlights,
  styles, blend amounts, and component sizes canonical rather than hidden in a
  second theme definition.

Color literals use `colorSpace` and `components`, not legacy hex-string token
values. For sRGB, components are red/green/blue in 0–1 (divide each hex byte by
255); for OKLCH they are lightness in 0–1, chroma, hue. All current colors use
sRGB, including the web theme, so shared roles have identical values. The small
generator supports opaque sRGB/OKLCH colors (OKLCH for web only), px/rem
dimensions, and numbers. It rejects unknown/circular aliases, mismatched types,
invalid components, and unsupported editor color spaces.

Emacs placeholders `{{semantic.emacs.bg|emacs}}` expand to
true-color/256-color/16-color triples. The 256-color value defaults to the same
RGB color; optional terminal fallbacks are declared in the token's namespaced
extension, and `null` stays Lisp `nil`. A placeholder without
`|emacs` expands to a single color inside an existing Lisp string. Doom blends
remain runtime expressions so terminal behavior and modeline customization are
preserved. The generator does not evaluate Lisp.

## Reconciliation decisions

| Role / existing difference | Uniform default |
| --- | --- |
| Numbers, strings, characters | Brown `#b4916d`; numbers are not bold. |
| Types, including struct tags and function-pointer typedefs | Teal `#4db5bd`. |
| Keywords, constants, macros | Yellow `#ecbe7b`; macro replacement numbers remain brown. |
| Functions, variables, operators, punctuation | White `#ffffff`. |
| Emacs green `#98be65` vs Neovim/web green `#99bb66` | Comments, primary accent, success and additions use `#99bb66`. |
| Different editor and web surfaces | Background `#18191b`, surface/current line `#202328`, raised surface `#3f444a`, foreground white. Line numbers use `#9ca0a4`. |
| Different status colors, including web info brown | Error red `#ff6c6b`, warning yellow, success green, info teal. |
| Emacs monochrome substitutions for chromatic colors | Restore shared chromatic roles; retain compatibility names, including `greeen` and Neovim's teal `blue`. |
| Neovim background depends on Colorbuddy defaults | Bind the background explicitly. |
| daisyUI dark preference with a light native color scheme | Use `color-scheme: "dark"`. |

These differences were accidental, not compatibility requirements. Platform
color aliases now reference shared semantic roles instead of preserving separate
RGB/OKLCH variants. Doom integrations, modeline padding, Colorbuddy exports,
legacy Tree-sitter groups, Org and which-key integrations remain available.

Modern Neovim Tree-sitter and LSP groups are mapped as well as legacy groups.
Emacs's C adapter supplies missing numeric highlighting in classic C/C++ modes;
for C/C++ Tree-sitter modes it also handles macro names/replacement numbers,
constants and character literals. It does not enable a parser or change major
modes. Its buffer-local rules are removed/reinstalled when switching themes.
Syntax classification still depends on the active parser: a theme cannot give
classic regex-based highlighting all the information available to a parser or
language server. In particular, native Neovim C queries classify function-like
macro calls as ordinary calls; LSP macro captures are yellow, but calls remain
white without that semantic classification. Macro definitions are yellow in
either case.

## Showcase and editor checks

`examples/showcase.c` is a compilable sample covering object/function/variadic
macros, struct tags, typedefs, enums, a function-pointer typedef and indirect call,
designated initializers, casts, operators, strings, escapes, and decimal, hex,
octal and scientific numeric literals. Compile with
`cc -std=c11 -Wall -Wextra -Werror examples/showcase.c -o /tmp/schwarzwald-showcase`.

Optional real-editor tests run alongside the dependency-free generator tests:

```sh
DOOM_THEMES_DIR=/path/to/doom-themes \
TREE_SITTER_C_DIR=/path/to/emacs/grammars \
COLORBUDDY_DIR=/path/to/colorbuddy.nvim \
python3 -B -m unittest -v
```

They require Emacs, Neovim, and their C grammars; unset paths skip the respective
checks. Tests exercise actual syntax captures, comment/string negative controls,
and Emacs theme switching rather than just inspecting generated text.

## Installation and extension

Use the generated files exactly as before: load `doom-custom-theme.el` with
`doom-themes` installed; place `theme.lua` on Neovim's colorscheme path with
Colorbuddy available; import `schwarzwald.css` from a Tailwind CSS 4/daisyUI 5
stylesheet and select `data-theme="schwarzwald"`.

To add a role, add an alias under `semantic`, then bind it in the relevant
namespaced adapter metadata. To add a new consumer, extend `generate.py` with one
renderer that resolves the existing tokens. Do not copy a palette into an
adapter or add another editable theme file.
