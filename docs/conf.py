import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "con24ma"
author = "Linqa Kiriyama"
release = "1.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_docstring = True

html_theme = "alabaster"

exclude_patterns = ["_build"]
