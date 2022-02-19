# PyTTI-Tools Documentation and Tutorials

[![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](https://pytti-tools.github.io/pytti-book/intro.html)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytti-tools/pytti-notebook/blob/main/pyttitools-PYTTI.ipynb)
[![DOI](https://zenodo.org/badge/461043039.svg)](https://zenodo.org/badge/latestdoi/461043039)
[![DOI](https://zenodo.org/badge/452409075.svg)](https://zenodo.org/badge/latestdoi/452409075)


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
