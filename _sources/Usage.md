# Usage

If you are running pytti in google colab, [this notebook](https://colab.research.google.com/github/pytti-tools/pytti-notebook/blob/main/pyttitools-PYTTI.ipynb) is recommended.

If you would like a notebook experience but are not using colab, please use the ["_local"](https://github.com/pytti-tools/pytti-notebook/blob/main/pyttitools-PYTTI_local.ipynb) notebook instead.

The following usage notes are written with the _local notebook and command-line (CLI) use in mind.

## YAML Configuration Crash-Course

PYTTI uses [OmegaConf](https://omegaconf.readthedocs.io/)/[Hydra](https://hydra.cc/docs/) for configuring experiments (i.e. "runs", "renders", "generating images", etc.). In this framework, experiments are specified using text files that contain the parameters we want to use in our experiment.

A starting set of [configuration files](https://github.com/pytti-tools/pytti-notebook/tree/main/config) is provided with the notebook repository. If you followed the setup instructions above, this `config/` folder should be in the same directory as your notebooks. If you are using the CLI, create a "config" folder with a "conf" subfolder in your current working directory.

### `config/default.yaml`

This file contains the default settings for all available parameters. The colab notebook can be used as a reference for how to use individual settings and what options can be used for settings that expect specific values or formats.

Entries in this file are in the form `key: value`. Feel free to modify this file to specify defaults that are useful for you, but we recommend holding off on tampering with `default.yaml` until after you are comfortable specifying your experiments with an override config (discussed below).

### `config/conf/*.yaml`

PYTTI requires that you specify a "config node" with the `conf` argument. The simplest use here is to add a yaml file in `config/conf/` with a name that somehow describes your experiment. A `demo.yaml` is provided.

**IMPORTANT**: The first line of any non-default YAML file you create needs to be:

    # @package _global_

for it to work properly in the current config scheme. See the `demo.yaml` as an example [here](https://github.com/pytti-tools/pytti-notebook/blob/main/config/conf/demo.yaml#L1)

As with `default.yaml`, each parameter should appear on its own line in the form `key: value`. Starting a line with '#' is interpreted as a comment: you can use this to annotate your config file with your own personal notes, or deactivate settings you want ignored.

## Notebook Usage

The first code cell in the notebook tells PYTTI where to find your experiment configuration. The name of your configuration gets stored in the `CONFIG_OVERRIDES` variable. When you clone the notebook repo, the variable is set to `demo.yaml`.

Executing the "RUN IT!" cell in the notebook will load the settings in `default.yaml` first, then the contents of the filename you gave to `CONFIG_OVERRIDES` are loaded and these settings will override the defaults. Therefore, you only need to explicitly specify settings you want to be different from the defaults given in `default.yaml`.

### "Multirun" in the Notebook (Intermediate)

#### Specifying multiple override configs

The `CONFIG_OVERRIDES` variable can accept a list of filenames. All files should be located in `config/conf` and follow the override configuration conventions described above. If multiple config filenames are provided, they will be iterated over sequentially.

As a simple example, let's say we wanted try three different prompts against the default settings. To achieve this, we will treat each set of prompts as its own "experiment" we want to run, so we'll need to create two override config files, one for each text prompt ("scene") we want to specify:

* `config/conf/experiment1.yaml`

      # @package _global_
      scenes: fear is the mind killer

* `config/conf/experiment2.yaml`

      # @package _global_
      scenes: it is by will alone I set my mind in motion

Now to run both of these experiments, in the second cell of the notebook we change:

    CONFIG_OVERRIDES="demo.yaml"

to

    CONFIG_OVERRIDES= [ "experiment1.yaml" , "experiment2.yaml" ]

(whitespace exaggerated for clarity.)


### Config Groups (advanced)

More details on this topic in the [hydra docs](https://hydra.cc/docs/tutorials/basic/your_first_app/config_groups/) and great examples in the [vissl docs](https://vissl.readthedocs.io/en/latest/hydra_config.html).

Hydra supports creating nested hierarchies of config files called "config groups". The hierarchy is organized using subfolders. To select a particular config file from a group, you use the same `key: value` syntax as the normal pytti parameters, except here the `key` is the name of a subdirectory you created and `value` is the name of a yaml file (without the .yaml extension) or folder in that subdirectory.

To demonstrate how this works, let's create a `motion` parameter group for storing sets of animation transformations we like to use.

First, we create a `motion` folder in `config/conf`, and add yaml files with the settings we want in that folder. So maybe something like:

* `config/conf/motion/zoom_in_slow.yaml`

      # @package _global_
      animation_mode: 3D
      translate_z_3D: 10

* `config/conf/motion/zoom_in_fast.yaml`

      # @package _global_
      animation_mode: 3D
      translate_z_3D: 100

* `config/conf/motion/zoom_out_spinning.yaml`

      # @package _global_
      animation_mode: 3D
      translate_z_3D: -50
      rotate_2D: 10

The config layout might look something like this now:

    ├── pytti-notebook/
    │   ├── config/
    |   │   ├── default.yaml
    |   │   ├── conf/
    |   │   |   ├── demo.yaml
    |   │   |   ├── experiment1.yaml
    |   │   |   ├── experiment2.yaml
    |   │   |   ├── motion/
    |   │   |   |   ├── zoom_in_slow.yaml
    |   │   |   |   ├── zoom_in_fast.yaml
    |   │   |   |   └── zoom_out_spinng.yaml

Now if we want to add one of these effects to an experiment, all we have to do is name it in the configuration like so:

* `config/conf/experiment1.yaml`

      # @package _global_
      scenes: fear is the mind killer
      motion: zoom_in_slow

## CLI usage

To e.g. run the configuration specified by `config/conf/demo.yaml`, our command would look like this:

    python -m pytti.workhorse conf=demo

Not that on the command line the convention is now `key=value` whereas it was `key: value` in the yaml files. Same keys and values work here, just need that `=` sign.

We can actually override arguments from the command line directly:

```
# to make this easier to read, I'm
# using the line continuation character: "\"

python -m pytti.workhorse \
    conf=demo \
    steps_per_scene=300 \
    translate_x=5 \
    seed=123
```

### CLI Superpowers

---
WARNING: invoking multi-run from the CLI will likely re-download vgg weights for LPIPS. This will hopefully be patched soon, but until it is, please be aware that:
* downloading large files repeatedly may eat up your internet quota if that's how your provider bills you.
* these files may consume disk space. To free up space, delete any vgg.pth files in subdirectories of the "outputs" folders pytti creates in multirun mode.
---

A superpower commandline hydra gives us is the ability to specify multiple values for the same key, we just need to add the argument `--multirun`. For example, we can do this:

    python -m pytti.workhorse \
        --multirun \
        conf=experiment1,experiment2

This will first run `conf/experiment1.yaml` then `conf/experiment2.yaml`. Simple as that.

The real magic here is that we can provide multiple values like this *to multiple keys*, creating permutations of settings.

Lets say that we wanted to compare our two experiments across several different random seeds:

```
python -m pytti.workhorse \
  --multirun \
  conf=experiment1,experiment2 \
  seed=123,42,1001
```

Simple as that, pytti will now run each experiment for all three seeds provided, giving us six experiments.

This works for parameter groups as well (you may have already figured out that `conf` *is* a parameter group, so we've actually already been using this feature with parameter groups):

```
# to make this easier to read, I'm
# using the line continuation character: "\"

python -m pytti.workhorse \
  conf=experiment1,experiment2 \
  seed=123,42,1001 \
  motion=zoom_in_slow,zoom_in_fast,zoom_and_spin
```

And just like that, we're permuting two prompts against 3 different motion transformations, and 3 random seeds. That tiny chunk of code is now generating 18 experiments for us.
