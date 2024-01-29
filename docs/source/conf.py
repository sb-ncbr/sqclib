import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "sqclib"
copyright = "2024, Martin Jediny"
author = "Martin Jediny"
release = "0.1.0"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.coverage", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
html_static_path = ["_static"]
