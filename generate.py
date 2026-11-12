#!/usr/bin/env python3
"""Render Schwarzwald's DTCG tokens using only the Python standard library."""
import argparse
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
EXTENSION = "org.schwarzwald"
REFERENCE = re.compile(r"\{([^{}]+)\}")
PLACEHOLDER = re.compile(r"\{\{([^{}|]+)(\|emacs)?\}\}")


class Tokens:
    def __init__(self, document):
        self.tokens = {}
        self._collect(document)
        for path in self.tokens:
            self.resolve(path)

    def _collect(self, node, prefix="", inherited_type=None):
        kind = node.get("$type", inherited_type)
        if "$value" in node:
            self.tokens[prefix] = (kind, node)
        else:
            for key, child in node.items():
                if not key.startswith("$"):
                    if not isinstance(child, dict) or any(c in key for c in ".{}"):
                        raise ValueError(f"Invalid token/group: {prefix}{key}")
                    self._collect(child, f"{prefix}.{key}".lstrip("."), kind)

    def resolve(self, path, stack=()):
        reference = REFERENCE.fullmatch(path)
        if reference:
            path = reference[1]
        if path in stack:
            raise ValueError(f"Circular token reference: {' -> '.join((*stack, path))}")
        if path not in self.tokens:
            raise ValueError(f"Unknown token: {path}")
        kind, token = self.tokens[path]
        value = token["$value"]
        if isinstance(value, str) and REFERENCE.fullmatch(value):
            target_kind, value = self.resolve(value, (*stack, path))
            if kind is not None and kind != target_kind:
                raise ValueError(f"Type mismatch: {path} ({kind} != {target_kind})")
            kind = target_kind
        self._validate(path, kind, value)
        return kind, value

    @staticmethod
    def _validate(path, kind, value):
        def number(n):
            return isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n)

        valid = False
        if kind == "color" and isinstance(value, dict):
            space, components = value.get("colorSpace"), value.get("components", [])
            valid = (space in ("srgb", "oklch") and len(components) == 3
                     and all(number(n) for n in components)
                     and number(value.get("alpha", 1)) and 0 <= value.get("alpha", 1) <= 1)
            if valid:
                if space == "srgb":
                    valid = all(0 <= n <= 1 for n in components)
                else:
                    valid = 0 <= components[0] <= 1 and components[1] >= 0 and 0 <= components[2] < 360
        elif kind == "dimension" and isinstance(value, dict):
            valid = number(value.get("value")) and value.get("unit") in ("px", "rem")
        elif kind == "number":
            valid = number(value)
        if not valid:
            raise ValueError(f"Invalid or unsupported {kind} token: {path}")

    def format(self, path, *, editor=False):
        kind, value = self.resolve(path)
        if kind == "color":
            if value.get("alpha", 1) != 1:
                raise ValueError(f"Adapters require opaque colors: {path}")
            if value["colorSpace"] == "srgb":
                return "#" + "".join(f"{round(n * 255):02x}" for n in value["components"])
            if editor:
                raise ValueError(f"Editor colors must use sRGB: {path}")
            l, c, h = value["components"]
            return f"oklch({l * 100:g}% {c:g} {h:g})"
        if kind == "dimension":
            return f'{value["value"]:g}{value["unit"]}'
        return f"{value:g}"

    def emacs(self, source):
        def replace(match):
            path, triple = match.groups()
            color = self.format(path, editor=True)
            if not triple:
                return color
            variants = self.tokens[path][1].get("$extensions", {}).get(EXTENSION, {})
            values = [json.dumps(color)]
            for key in ("terminal256", "terminal16"):
                value = variants.get(key, "{" + path + "}" if key == "terminal256" else None)
                if value is not None and REFERENCE.fullmatch(value):
                    value = self.format(value, editor=True)
                values.append("nil" if value is None else json.dumps(value))
            return "'(" + " ".join(values) + ")"
        rendered = PLACEHOLDER.sub(replace, source)
        if "{{" in rendered or "}}" in rendered:
            raise ValueError(f"Unresolved Emacs placeholder: {source}")
        return rendered


def render(document):
    tokens = Tokens(document)
    adapters = document["$extensions"][EXTENSION]
    emacs = adapters["emacs"]
    bindings = "\n   ".join(tokens.emacs(form) for form in emacs["bindings"])
    faces = "\n   ".join(tokens.emacs(form) for form in emacs["faces"])
    setup = "\n".join(emacs.get("setup", []))
    el = f''';;; doom-custom-theme.el --- generated -*- lexical-binding: t; no-byte-compile: t; -*-
;; Generated by generate.py from tokens.json; DO NOT EDIT.

(require 'doom-themes)

(defgroup doom-custom-theme nil
  "Options for the `doom-custom' theme."
  :group 'doom-themes)

(defcustom doom-homage-black-padded-modeline doom-themes-padded-modeline
  "If non-nil, adds a 4px padding to the mode-line. Can be an integer to
determine the exact padding."
  :group 'doom-custom-theme
  :type '(choice integer boolean))

(def-doom-theme doom-custom
  "Schwarzwald, a dark theme."
  ({bindings})
  ({faces})
  ())

{setup}

;;; doom-custom-theme.el ends here
'''

    lua = ["-- Generated by generate.py from tokens.json; DO NOT EDIT.",
           "local colorbuddy = require('colorbuddy')", "colorbuddy.colorscheme('theme')",
           "local Color, Group = colorbuddy.Color, colorbuddy.Group",
           "local colors, styles = colorbuddy.colors, colorbuddy.styles", ""]
    nvim = adapters["neovim"]
    for name, ref in nvim["colors"].items():
        lua.append(f"Color.new({json.dumps(name)}, {json.dumps(tokens.format(ref, editor=True))})")
    references = {}
    for group in nvim["groups"]:
        for key in ("foreground", "background"):
            ref = group.get(key)
            if ref and ref != "NONE" and ref not in references:
                name = "token_" + str(len(references))
                references[ref] = name
                lua.append(f"Color.new('{name}', '{tokens.format(ref, editor=True)}')")
    lua.append("")
    for group in nvim["groups"]:
        args = [json.dumps(group["name"])]
        keys = ["foreground", "background", "style"]
        while keys and keys[-1] not in group:
            keys.pop()
        for key in keys:
            value = group.get(key, "NONE")
            if key == "style":
                args.append("styles." + value.lower())
            elif value == "NONE":
                args.append("colors.none")
            else:
                args.append("colors." + references[value])
        lua.append("Group.new(" + ", ".join(args) + ")")

    web = adapters["daisyui"]
    css = ['/* Generated by generate.py from tokens.json; DO NOT EDIT. */', '@plugin "daisyui/theme" {']
    for key in ("name", "default", "prefersdark", "color-scheme"):
        css.append(f"  {key}: {json.dumps(web[key])};")
    for prop, ref in web["properties"].items():
        css.append(f"  --{prop}: {tokens.format(ref)};")
    css.append("}")
    return {"doom-custom-theme.el": el, "theme.lua": "\n".join(lua) + "\n",
            "schwarzwald.css": "\n".join(css) + "\n"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale; do not write")
    args = parser.parse_args()
    try:
        outputs = render(json.loads((ROOT / "tokens.json").read_text()))
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Token error: {error}\n")
    stale = []
    for name, source in outputs.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text() != source:
                stale.append(name)
        else:
            path.write_text(source)
    if stale:
        print("Generated files are stale: " + ", ".join(stale) + "; run python3 generate.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
