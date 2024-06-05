import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Axiomic'
copyright = '2024, Victor Bittorf'
author = 'Victor Bittorf'
release = '0.5'

html_title = f'{project} Docs'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon']

html_theme = 'sphinx_material'

html_theme_options = {
    'color_primary': 'blue',
    'color_accent': 'deep-orange',
    'globaltoc_depth': 2,
    'globaltoc_collapse': True,
    'globaltoc_includehidden': True,
    'nav_links': [
        # {'href': 'index', 'title': 'Home', 'internal': True},
        # {'href': 'about', 'title': 'About', 'internal': True},
        {'href': 'https://github.com/axiomic-ai/axiomic', 'title': 'GitHub', 'internal': False},
        {'href': 'https://discord.com/invite/jj9kgkWb', 'title': 'Discord', 'internal': False},
    ],
}

html_sidebars = {
    '**': [
        'globaltoc.html',  # Include the global TOC
        'localtoc.html',   # Include the local TOC
        'sidebar.html',    # Use the custom sidebar template
    ]
}


templates_path = ['_templates']

# only incldue white listed modules
exclude_patterns = ['axiomic/*']

# List of directories to exclude from documentation
exclude_dirnames = ['axiomic/']

# List of modules to document
include_modules = [
    'axiomic.frontend.text',
    # Add other modules to document as needed
]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
