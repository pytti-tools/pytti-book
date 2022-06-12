from copy import deepcopy
from itertools import (
    product, 
    combinations,
)
from pathlib import Path
from typing import List

from hydra import initialize, compose
from loguru import logger
import matplotlib.pyplot as plt
import numpy as np
from pytti.workhorse import _main as render_frames
from torchvision.io import read_image
import torchvision.transforms.functional as F
from torchvision.utils import make_grid

# this is useful enough that maybe I should just ship it with pytti

class ExperimentMatrix:
    """
    Class for facilitating running experiments over varying sets of parameters
    ...which I should probably just be doing with hydra's multirun anyway, now that I think about it.
    you know what, I'm not sure that's actually easier for what I'm doing.
    """
    def __init__(
        self,
        variant: dict=None,
        invariant:dict=None,
        mapped:dict=None,
        conditional:dict=None, # cutpow = 2 if cutouts>80 else 1 # {param0: f(kw)}
        CONFIG_BASE_PATH:str = "config",
        CONFIG_DEFAULTS:str = "default.yaml",
    ):
        """
        :param: variant: Parameters to be varied and the values they can take
        :param: invariant: Parameters that will stay fixed each experiment
        :param: mapped: Settings whose values should be copied from other settings
        :param: conditional: Settings whose values are conditoinal on the values of variants, in form: `{conditional_param: f(kw)}`
        """
        self.variant = variant
        self.invariant = invariant
        self.mapped = mapped
        self.conditional = conditional
        self.CONFIG_BASE_PATH = CONFIG_BASE_PATH
        self.CONFIG_DEFAULTS = CONFIG_DEFAULTS

    def variant_combinations(self, n:int=None):
        """
        Generates combinations of variant parameters, where n is the number of parameters 
        per combination. Defaults to pairs
        """
        if not n:
            n = len(self.variant)
        return combinations(self.variant.items(), n)

    def populate_mapped_settings(self, kw:dict) -> dict:
        """
        Adds mapped settings to experiment kwargs
        """
        for k0, krest in self.mapped.items():
            for k1 in krest:
                kw[k1] = kw[k0]
        return kw

    def populate_conditional_settings(self, kw:dict) -> dict:
        """
        Adds conditional settings to experiment kwargs
        """
        if self.conditional is None:
            return kw
        for p, f in self.conditional.items():
            kw[p] = f(kw)
        return kw

    def populate_invariants(self, kw:dict)->dict:
        """
        Seeds experiment with invariant settings
        """
        return kw.update(deepcopy(self.invariant))

    def dict2hydra(self, kw:dict)->List[str]:
        """
        Converts dict of settings to hydra.compose format
        """
        return [f"{k}={v}" for k,v in kw.items()]

    def build_parameterizations(self, n:int=None):
        """
        Builds settings for each respective experiment
        """
        #if n != 2:
        #    raise NotImplementedError
        if not n:
            n = len(self.variant)
        kargs = []
        #for param0, param1 in self.variant_combinations(n):
        #    (p0_name, p0_vals_all), (p1_name, p1_vals_all) = param0, param1
        #    for p0_val, p1_val in product(p0_vals_all, p1_vals_all):
        #        kw = {
        #            p0_name:p0_val,
        #            p1_name:p1_val,
        #            'file_namespace':f"matrix_{p0_name}-{p0_val}_{p1_name}-{p1_val}",
        #            }
        #for args in self.variant_combinations(n):
        #for args in combinations(self.variant.values(), n):
        for args in product(*self.variant.values()):
                kw = {k:v for k,v in zip(self.variant.keys(), args)}
                #kw = {k:v for k,v in args}
                self.populate_invariants(kw)
                self.populate_mapped_settings(kw)
                self.populate_conditional_settings(kw)
                kargs.append(kw)
        #kws = [self.dict2hydra(kw) for kw in kargs]
        #return kargs, kws
        self.kargs= kargs
        return deepcopy(kargs)

    def run_all(self, kargs:dict=None, convert_to_hydra:bool=True):
        """
        Runs all experiments per given parameterizations
        """
        if not kargs:
            if not hasattr(self, 'kargs'):
                self.build_parameterizations()
            kargs = self.kargs
        with initialize(config_path=self.CONFIG_BASE_PATH):
            for kws in kargs:
                #logger.debug(f"kws: {kws}")
                print(f"kws: {kws}")
                if convert_to_hydra:
                    kws = self.dict2hydra(kws)
                self.run_experiment(kws)
        
    def run_experiment(self, kws:dict):
        """
        Runs a single experiment. Factored at to an isolated function
        to facilitate overriding if hydra isn't needed.
        """
        logger.debug(kws)
        cfg = compose(
            config_name=self.CONFIG_DEFAULTS, 
            overrides=kws
            )
        render_frames(cfg)

    def display_results(self, kargs=None, variant=None):
        """
        Displays a matrix of generated outputs
        """
        if not kargs:
            kargs = self.kargs
        if not variant:
            variant = self.variant

        images = []
        for k in kargs:
            fpath = Path("images_out") / k['file_namespace'] / f"{k['file_namespace']}_1.png"
            images.append(read_image(str(fpath)))

        nr = len(list(variant.values())[0])
        grid = make_grid(images, nrow=nr)
        fix, axs = show(grid)

        ax0_name, ax1_name = list(self.variant.keys())
        fix.savefig(f"TestMatrix_{ax0_name}_{ax1_name}.png")
        return fix, axs






#########################################


def run_experiment_matrix(
    kws,

):
    # https://github.com/facebookresearch/hydra/blob/main/examples/jupyter_notebooks/compose_configs_in_notebook.ipynb
    # https://omegaconf.readthedocs.io/
    # https://hydra.cc/docs/intro/
    with initialize(config_path=CONFIG_BASE_PATH):

        for k in kws:
            logger.debug(k)
            cfg = compose(config_name=CONFIG_DEFAULTS, 
                        overrides=k)
            render_frames(cfg)


def build_experiment_parameterizations(
    cross_product,
    invariants,
    map_kv,
):
    kargs = []
    NAME, VALUE = 0, 1
    for param0, param1 in combinations(cross_product, 2):
        p0_name, p1_name = param0[NAME], param1[NAME]
        for p0_val, p1_val in product(param0[VALUE], param1[VALUE]):
            kw = deepcopy(invariants)
            kw.update({
                p0_name:p0_val,
                p1_name:p1_val,
                'file_namespace':f"matrix_{p0_name}-{p0_val}_{p1_name}-{p1_val}",
                })
            # map in "variable imputations"
            for k0, krest in map_kv:
                for k1 in krest:
                    kw[k1] = kw[k0]
            kargs.append(kw)
    kws = [[f"{k}={v}" for k,v in kw.items()] for kw in kargs]
    return kargs, kws


def build_experiment_parameterizations_from_dicts(
    cross_product: dict,
    invariants: dict,
    map_kv: dict,
    conditional: dict = None,
):
    kargs = []
    for param0, param1 in combinations(cross_product.items(), 2):
        (p0_name, p0_vals_all), (p1_name, p1_vals_all) = param0, param1
        for p0_val, p1_val in product(p0_vals_all, p1_vals_all):
            kw = deepcopy(invariants)
            kw.update({
                p0_name:p0_val,
                p1_name:p1_val,
                'file_namespace':f"matrix_{p0_name}-{p0_val}_{p1_name}-{p1_val}",
                })
            # map in "variable imputations"
            for k0, krest in map_kv:
                for k1 in krest:
                    kw[k1] = kw[k0]

            #if (conditional is not None):
            #    for p in conditional:
            #        if p 

            kargs.append(kw)
    kws = [[f"{k}={v}" for k,v in kw.items()] for kw in kargs]
    return kargs, kws

def run_experiment_matrix(
    kws,
    CONFIG_BASE_PATH = "config",
    CONFIG_DEFAULTS = "default.yaml",
):
    # https://github.com/facebookresearch/hydra/blob/main/examples/jupyter_notebooks/compose_configs_in_notebook.ipynb
    # https://omegaconf.readthedocs.io/
    # https://hydra.cc/docs/intro/
    with initialize(config_path=CONFIG_BASE_PATH):

        for k in kws:
            logger.debug(k)
            cfg = compose(config_name=CONFIG_DEFAULTS, 
                        overrides=k)
            render_frames(cfg)

# https://pytorch.org/vision/master/auto_examples/plot_visualization_utils.html#visualizing-a-grid-of-images
# sphinx_gallery_thumbnail_path = "../../gallery/assets/visualization_utils_thumbnail2.png"

def show(imgs):
    plt.rcParams["savefig.bbox"] = 'tight'
    plt.rcParams['figure.figsize'] = 20,20
    if not isinstance(imgs, list):
        imgs = [imgs]
    fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = F.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
    return fix, axs

def display_study_results(kargs, cross_product):
    images = []
    for k in kargs:
        fpath = Path("images_out") / k['file_namespace'] / f"{k['file_namespace']}_1.png"
        images.append(read_image(str(fpath)))

    nr = len(cross_product[0][-1])
    grid = make_grid(images, nrow=nr)
    fix, axs = show(grid)

    ax0_name, ax1_name = cross_product[0][0], cross_product[1][0]
    fix.savefig(f"TestMatrix_{ax0_name}_{ax1_name}.png")
        