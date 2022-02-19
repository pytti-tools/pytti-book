# Setup

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

    conda install -c conda-forge imageio
    conda install -c conda-forge pytorch-lightning
    conda install -c conda-forge kornia
    conda install -c huggingface transformers
    conda install scikit-learn pandas

### 9. Install pip dependencies

    pip install jupyter gdown loguru einops seaborn PyGLM ftfy regex tqdm hydra-core adjustText exrex matplotlib-label-lines

### 10. Download pytti-core

      git clone --recurse-submodules -j8 --branch dev https://github.com/pytti-tools/pytti-core

Your local directory structure probably looks like this now:

            ├── pytti-notebook
            │   ├── config
            │   ├── images_out
            │   ├── pretrained
            │   ├── pytti-core
            │   └── videos

### 11. Install pytti-core

    pip install ./pytti-core/vendor/AdaBins
    pip install ./pytti-core/vendor/CLIP
    pip install ./pytti-core/vendor/GMA
    pip install ./pytti-core/vendor/taming-transformers
    pip install ./pytti-core
