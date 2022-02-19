# PyTTI-Tools Documentation and Tutorials

https://pytti-tools.github.io/pytti-book/intro.html

Made with [![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](https://jupyterbook.org)

## Requirements

    pip install jupyter-book
    pip install ghp-import

## Building and publishing

    # Add a new document to the book
    git add NewArticle.ipynb
    
    # The page won't show up unless you specify where it goes in the TOC
    git add _toc.yml
    git commit -am "Added NewArticle.ipynb"
    jupyter-book build .
    ghp-import -n -p -f _build/html
