---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# PyTTI (local) Crash Course - maybe

To get started in google colab, just follow the instructions in the notebook. Running PyTTI with the yaml config system is a bit more DIY, so we'll walk through that here. If you're planning on only ever using the UI in the colab notebook, you might still find this demo useful to better understand how different settings impact the image generation process.

We'll start by doing a kind of "factory reset"  by deleting a few folders. You don't necessarily need to do this, but for the purpose of the demo we'll make sure we've got a clean workspace. Make sure you've moved or copied anything you want to hold on to before deleting.

foobar

```{code-cell} ipython3
%%capture
print("foobar")
# these will be rebuilt when we generate images
!rm -rf images_out/
!rm -rf outputs/
!rm -rf logs/
!rm -rf backup/
!rm -rf multirun/

# this will be rebuild when we run pytti.warmup
!rm -rf config/
```

The next cell just creates the default configs and folders if they aren't already present.


```{code-cell} ipython3
# Rebuild config files using "factory defaults"
!python -m pytti.warmup
```

Those outputs there are normal logging messages. We'll suppress those in subsequent cells to make this tutorial easier to read by adding `%%capture` to the tops of cells where we're running pytti. This will also suppress displaying image frames and reporting loss values, so unless you're tracking your experiment extrnally with tensorboard (or even just watching the images pop up as thumbnails in a file browser), you probably won't want to suppress the notebook outputs like this.
