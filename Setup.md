# Setup

Pytti-Tools can be run without any complex setup -- completely for free! -- via google colab. The instructions below are for users who would like to install pytti-tools locally. If you would like to use pytti-tools on google colab, click this button to open the colab notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytti-tools/pytti-notebook/blob/main/pyttitools-PYTTI.ipynb)

## Requirements

* Python 3.x
* [Pytorch](https://pytorch.org/get-started/locally/)
* CUDA-capable GPU
* OpenCV
* ffmpeg
* Python Image Library (PIL/pillow)
* git - simplifies downloading code and keeping it up to date
* gdown - simplifies downloading pretrained models
* jupyter - (Optional) Notebook interface


The following instructions assume local setup. Most of it is just setting up a local ML environment that has similar tools installed as google colab.

### 1. Install git and python (anaconda is recommended)

* https://www.anaconda.com/products/individual
* https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### 2. Clone the pytti-notebook project and change directory into it.

The pytti-notebook folder will be our root directory for the rest of the setup sequence.

    git clone https://github.com/pytti-tools/pytti-notebook
    cd pytti-notebook

### 3.  Create and acivate a new environment

    conda create -n pytti-tools
    conda activate pytti-tools

The environment name shows up at the beginning of the line in the terminal. After running this command, it should have changed from `(base)` to `(pytti-tools)`. The installation steps that follow will now install into our new "pytti-tools" environment only.

### 4. Install Pytorch

Follow the installation steps for installing pytorch with CUDA/GPU support here: https://pytorch.org/get-started/locally/ . For windows with anaconda:

    conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

### 5. Install tensorflow

    conda install tensorflow-gpu
### 6. Install OpenCV

    conda install -c conda-forge opencv

### 7. Install the Python Image Library (aka pillow/PIL)

    conda install -c conda-forge pillow

### 8. ... More conda installations

    conda install conda-forge::imageio \
     conda-forge::pytorch-lightning \
     conda-forge::kornia \
     huggingface::transformers \
     defaults::scikit-learn \
     defaults::pandas

### 9. Install pip dependencies

    pip install jupyter gdown loguru einops seaborn PyGLM ftfy regex tqdm hydra-core adjustText exrex matplotlib-label-lines

### 10. Download pytti-core

      git clone --recurse-submodules -j8 https://github.com/pytti-tools/pytti-core
### 11. Install pytti-core

    pip install ./pytti-core/vendor/AdaBins \
      ./pytti-core/vendor/CLIP \
      ./pytti-core/vendor/GMA \
      ./pytti-core/vendor/taming-transformers \
      ./pytti-core

### 12. (optional) Build local configs

If you skip this step, PyTTI will do it for you anyway the first time you import it.

```
python -m pytti.warmup
```

Your local directory structure probably looks something like this now:

            ├── pytti-notebook
            │   ├── config
            │   └── pytti-core

If you want to "factory reset" your default.yaml, just delete the config folder and run the warmup command above to rebuild it with PyTTI's shipped defaults.


# Uninstalling and/or Updating

### 1. Uninstall PyTTI

```
pip uninstall -y ./pytti-core/vendor/AdaBins
pip uninstall -y ./pytti-core/vendor/CLIP
pip uninstall -y ./pytti-core/vendor/GMA
pip uninstall -y ./pytti-core/vendor/taming-transformers
pip uninstall -y pyttitools-core;
```

### 2. Delete PyTTI and any remaining build artifacts from installing it

```
rm -rf build
rm -rf config
rm -rf pytti-core
```

### 3. Downloaded the latest pytti-core and re-install

```
git clone --recurse-submodules -j8 https://github.com/pytti-tools/pytti-core

pip install ./pytti-core/vendor/AdaBins
pip install ./pytti-core/vendor/CLIP
pip install ./pytti-core/vendor/GMA
pip install ./pytti-core/vendor/taming-transformers
pip install ./pytti-core

python -m pytti.warmup
```
