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
propagation, independent semantic roles, platform variants, and invalid aliases.
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
- Other `palette` colors: only existing platform-specific colors that cannot be
  collapsed without changing the appearance, including terminal and web colors.
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
255); for OKLCH they are lightness in 0–1, chroma, hue. Existing OKLCH values stay
OKLCH: generation never converts or gamut-clips the web palette. The small
generator supports the types used here: opaque sRGB/OKLCH colors, px/rem
dimensions, and numbers. It rejects unknown/circular aliases, mismatched types,
invalid components, and unsupported editor color spaces.

Emacs placeholders `{{semantic.emacs.bg|emacs}}` expand to the original
true-color/256-color/16-color triples. Their terminal fallbacks are declared in
the token's namespaced extension; `null` stays Lisp `nil`. A placeholder without
`|emacs` expands to a single color inside an existing Lisp string. Doom blends
remain runtime expressions so terminal behavior and modeline customization are
preserved. The generator does not evaluate Lisp.

## Reconciliation decisions

| Existing difference | Resolution |
| --- | --- |
| Emacs comment/success/addition green `#98be65`; Neovim/web green `#99bb66` | Preserve the Emacs variant explicitly; shared green is `base0B`. |
| Emacs `green`, `blue`, `magenta`, `violet`, `cyan`, `dark-cyan` are white in true color | Preserve the intentional monochrome substitutions and every terminal fallback. The old `greeen` symbol remains compatible. |
| Neovim's `blue` is actually teal `#4db5bd` | Bind it to the shared type color, `base0C`; retain the Colorbuddy export name. |
| Emacs operator/category constants vs Neovim operator/constants and legacy `TSConstant` | Preserve their distinct roles: Emacs operators are yellow and constants white; Neovim operators are white and `Constant` yellow, while `TSConstant` stays white. Explicit Emacs font-lock overrides remain separate from Doom categories. |
| Editor background `#18191b`; different Emacs/Neovim secondary surfaces and muted grays; web OKLCH surfaces/content | Preserve named platform variants rather than forcing a new neutral ramp on existing UIs. |
| Emacs error red, unused Neovim fallback red, and web OKLCH error red differ | Preserve all three. Neovim's extra exported colors remain available to Colorbuddy consumers. Web info stays its original brown/orange, not a newly invented blue. |
| Neovim `colors.bg` depends on Colorbuddy defaults | Bind Normal and Whitespace backgrounds explicitly to `semantic.background`; verified identical with the installed Colorbuddy. Keep the original `gray0` export. |
| daisyUI says `prefersdark: true` but `color-scheme: "light"` | Correct to `"dark"`. All custom property values are unchanged; native browser controls/scrollbars now use the intended dark scheme. |
| Emacs describes itself as a light Atom One theme and has the wrong footer | Correct descriptive text only. Retain the `doom-custom` theme name and `doom-homage-black-padded-modeline` customization for compatibility. |

No plugin integrations were removed: Doom face overrides, Colorbuddy C/C++, legacy
Tree-sitter and Org groups, which-key groups, styles, and modeline logic remain.
The disabled alternative Lua implementation and commented-out color experiments
were not additional active theme definitions and are not generated.

## Installation and extension

Use the generated files exactly as before: load `doom-custom-theme.el` with
`doom-themes` installed; place `theme.lua` on Neovim's colorscheme path with
Colorbuddy available; import `schwarzwald.css` from a Tailwind CSS 4/daisyUI 5
stylesheet and select `data-theme="schwarzwald"`.

To add a role, add an alias under `semantic`, then bind it in the relevant
namespaced adapter metadata. To add a new consumer, extend `generate.py` with one
renderer that resolves the existing tokens. Do not copy a palette into an
adapter or add another editable theme file.
