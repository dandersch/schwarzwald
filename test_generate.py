"""Public generator contracts; no editor plugins needed to run these checks."""
import copy
import json
import re
import unittest

from generate import ROOT, render


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((ROOT / "tokens.json").read_text())

    def test_checked_in_outputs_are_current(self):
        for name, source in render(self.document).items():
            with self.subTest(name=name):
                self.assertEqual((ROOT / name).read_text(), source)

    def test_shared_palette_edit_reaches_all_platforms(self):
        self.document["palette"]["base0A"]["$value"] = {
            "colorSpace": "srgb", "components": [0.2, 0.4, 0.8]}
        outputs = render(self.document)
        self.assertRegex(outputs["doom-custom-theme.el"], r'\(yellow\s+\x27\("#3366cc" "#3366cc" "yellow"\)\)')
        self.assertIn('--color-secondary: #3366cc;', outputs["schwarzwald.css"])
        self.assertIn('--color-warning: #3366cc;', outputs["schwarzwald.css"])
        self.assertIn('Color.new("yellow", "#3366cc")', outputs["theme.lua"])

    def test_syntax_role_edit_is_independent_of_accents(self):
        self.document["palette"]["base0D"]["$value"] = {
            "colorSpace": "srgb", "components": [0.2, 0.6, 1]}
        before = render(self.document)
        self.document["semantic"]["syntax"]["keyword"]["$value"] = "{palette.base0D}"
        outputs = render(self.document)
        self.assertRegex(outputs["doom-custom-theme.el"], r'\(syntax-keyword\s+\x27\("#3399ff"')
        lua = outputs["theme.lua"]
        name = re.search(r'Group.new\("Keyword", colors\.(\w+)', lua)[1]
        self.assertIn(f"Color.new('{name}', '#3399ff')", lua)
        self.assertEqual(before["schwarzwald.css"], outputs["schwarzwald.css"])

    def test_shared_surfaces_and_green_have_no_platform_variants(self):
        self.document["palette"]["base0B"]["$value"] = {
            "colorSpace": "srgb", "components": [0.8, 0.6, 0.2]}
        self.document["palette"]["base00"]["$value"] = {
            "colorSpace": "srgb", "components": [0.2, 0.4, 0.8]}
        self.document["semantic"]["web"]["size-field"]["$value"] = {"value": 0.375, "unit": "rem"}
        outputs = render(self.document)
        el, lua, css = (outputs[k] for k in ("doom-custom-theme.el", "theme.lua", "schwarzwald.css"))
        self.assertRegex(el, r'\(comments\s+\x27\("#cc9933" "#cc9933" "green"\)\)')
        self.assertIn('Color.new("green", "#cc9933")', lua)
        self.assertIn('--color-primary: #cc9933;', css)
        self.assertRegex(el, r'\(bg\s+\x27\("#3366cc" "#3366cc" nil\)\)')
        self.assertIn('Color.new("background", "#3366cc")', lua)
        self.assertIn('--color-base-100: #3366cc;', css)
        self.assertIn('--size-field: 0.375rem;', css)
        self.assertIn('color-scheme: "dark";', css)

    def test_oklch_web_tokens_remain_supported(self):
        self.document["semantic"]["web"]["color-info"]["$value"] = {
            "colorSpace": "oklch", "components": [0.17, 0.03, 142]}
        self.assertIn('--color-info: oklch(17% 0.03 142);', render(self.document)["schwarzwald.css"])

    def test_bad_tokens_fail_before_rendering(self):
        for value, error in (("{missing.color}", "Unknown token"),
                             ("{semantic.foreground}", "Circular token"),
                             ({"colorSpace": "srgb", "components": [-0.1, 0, 1]}, "Invalid")):
            with self.subTest(value=value):
                doc = copy.deepcopy(self.document)
                doc["palette"]["base06"]["$value"] = value
                with self.assertRaisesRegex(ValueError, error):
                    render(doc)
        self.document["semantic"]["foreground"]["$value"] = "{semantic.web.depth}"
        with self.assertRaisesRegex(ValueError, "Type mismatch"):
            render(self.document)


if __name__ == "__main__":
    unittest.main()
