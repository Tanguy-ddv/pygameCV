import os
import sys
sys.path.insert(0, os.path.abspath(".."))  # Ensure the project root is in the path

# Project information
project = 'PygameCV'
copyright = '2025, Tanguy Dugas du Villard'
author = 'Tanguy Dugas du Villard'

# General configuration
extensions = [
    'sphinx.ext.autodoc',  # Use docstrings for documentation
    'sphinx.ext.napoleon',  # Support for Google-style and NumPy-style docstrings
    'myst_parser',  # Enable Markdown support
    "sphinx.ext.autosummary", # Enable auto summary with docstrings.
]

templates_path = ['_templates']
exclude_patterns = []

# Options for HTML output
html_theme = 'alabaster'  # Simple built-in theme
html_static_path = ['_static']

# Set the main document
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
master_doc = 'README.md'

autosummary_generate = True