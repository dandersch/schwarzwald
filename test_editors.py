"""Optional real-editor checks; see README for the local dependency paths."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from generate import ROOT


class EmacsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.themes = os.environ.get("DOOM_THEMES_DIR")
        if not cls.themes or not shutil.which("emacs"):
            raise unittest.SkipTest("Set DOOM_THEMES_DIR to run Emacs integration checks")

    def emacs(self, forms):
        result = subprocess.run(
            ["emacs", "--batch", "-Q", "-L", self.themes, "-l", str(ROOT / "doom-custom-theme.el"),
             "--eval", "(progn (require 'json) " + forms + ")"],
            cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_classic_c_numbers_and_theme_switching(self):
        result = self.emacs('''
          (find-file "examples/showcase.c")
          (enable-theme 'doom-custom)
          (font-lock-ensure)
          (dolist (text '("42u" "1.25" "0x2Au" "0755" "6.25e-2" ".5f"))
            (goto-char (point-min)) (search-forward text)
            (unless (eq (get-text-property (- (point) (length text)) 'face) 'font-lock-number-face)
              (error "Number not highlighted: %s" text)))
          (goto-char (point-min)) (search-forward "12345")
          (unless (eq (get-text-property (- (point) 5) 'face) 'font-lock-comment-face)
            (error "Number matcher recolored a comment"))
          (search-forward "123")
          (unless (eq (get-text-property (- (point) 3) 'face) 'font-lock-string-face)
            (error "Number matcher recolored a string"))
          (disable-theme 'doom-custom) (font-lock-ensure)
          (goto-char (point-min)) (search-forward "42u")
          (when (eq (get-text-property (- (point) 3) 'face) 'font-lock-number-face)
            (error "Theme left its number matcher enabled"))
          (enable-theme 'doom-custom) (font-lock-ensure)
          (goto-char (point-min)) (search-forward "42u")
          (unless (eq (get-text-property (- (point) 3) 'face) 'font-lock-number-face)
            (error "Re-enabling the theme did not restore number highlighting"))
          (princ "ok")''')
        self.assertEqual(result, "ok")

    def test_tree_sitter_c_roles(self):
        directory = os.environ.get("TREE_SITTER_C_DIR")
        if not directory:
            self.skipTest("Set TREE_SITTER_C_DIR to the Emacs C grammar directory")
        probes = {"42u": "font-lock-number-face", "1.25": "font-lock-number-face",
                  "forest forest_t;": "font-lock-type-face",
                  "forest_t;": "font-lock-type-face", "forest_visit_fn)(": "font-lock-type-face",
                  "0x2Au": "font-lock-number-face", "6.25e-2": "font-lock-number-face",
                  ".5f": "font-lock-number-face", "SCALE(value)": "font-lock-constant-face",
                  "12345": "font-lock-comment-face", "Bannwald 123": "font-lock-string-face"}
        strings = " ".join(json.dumps(text) for text in probes)
        result = self.emacs(f'''
          (setq treesit-extra-load-path '({json.dumps(directory)}) treesit-font-lock-level 4)
          (enable-theme 'doom-custom)
          (find-file "examples/showcase.c") (c-ts-mode) (font-lock-ensure)
          (disable-theme 'doom-custom) (font-lock-ensure)
          (goto-char (point-min)) (search-forward "42u")
          (when (eq (get-text-property (- (point) 3) 'face) 'font-lock-number-face)
            (error "Theme left its Tree-sitter macro rules enabled"))
          (enable-theme 'doom-custom) (font-lock-ensure)
          (princ (json-encode
            (mapcar (lambda (text)
              (goto-char (point-min)) (search-forward text)
              (cons text (symbol-name (get-text-property (- (point) (length text)) 'face))))
              '({strings}))))''')
        self.assertEqual(json.loads(result), probes)


class NeovimTests(unittest.TestCase):
    def test_tree_sitter_c_roles(self):
        colorbuddy = os.environ.get("COLORBUDDY_DIR")
        if not colorbuddy or not shutil.which("nvim"):
            self.skipTest("Set COLORBUDDY_DIR to run Neovim integration checks")
        probes = {"42u": "number", "1.25": "number", "forest forest_t;": "type",
                  "forest_t;": "type", "forest_visit_fn)(": "type",
                  "0x2Au": "number", "6.25e-2": "number", ".5f": "number",
                  "SCALE(value)": "function.macro", "Bannwald 123": "string"}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "captures.json"
            script = Path(directory) / "test.lua"
            script.write_text('''
              dofile('theme.lua')
              vim.treesitter.start(0, 'c')
              vim.treesitter.get_parser(0, 'c'):parse(true)
              local source = table.concat(vim.api.nvim_buf_get_lines(0, 0, -1, false), '\\n')
              local result = {}
              for needle, _ in pairs(vim.json.decode(''' + json.dumps(json.dumps(probes)) + ''')) do
                local position = assert(source:find(needle, 1, true))
                local prefix = source:sub(1, position - 1)
                local _, row = prefix:gsub('\\n', '')
                local column = #(prefix:match('[^\\n]*$'))
                local captures = vim.treesitter.get_captures_at_pos(0, row, column)
                result[needle] = {}
                for _, capture in ipairs(captures) do
                  table.insert(result[needle], capture.capture)
                end
              end
              vim.fn.writefile({vim.json.encode(result)}, ''' + json.dumps(str(output)) + ''')
            ''')
            subprocess.run(["nvim", "--headless", "-u", "NONE", "--cmd", "set rtp+=" + colorbuddy,
                            "examples/showcase.c", "-c", "luafile " + str(script), "-c", "qa!"],
                           cwd=ROOT, check=True, capture_output=True)
            actual = json.loads(output.read_text())
        for needle, capture in probes.items():
            with self.subTest(needle=needle):
                self.assertIn(capture, actual[needle])


if __name__ == "__main__":
    unittest.main()
