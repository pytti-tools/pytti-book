(SceneDSL)=
# Scene Syntax

prompts `first prompt | second prompt`
: Each scene can contain multiple prompts, separated by `|`. Each text prompt is separately interpreted by the CLIP Perceptor to create a representation of each prompt in "semantic space" or "concept space". The semantic representations are then combined into a single representation which will be used to steer the image generation process. 


:::{admonition} Example: A single scene with multiple prompts
```
Winter sunrise | icy landscape | snowy skyline 
```
Would generate a wintry scene.
:::


scenes `first scene || second scene`
: Scenes are separated by `||`

:::{admonition} Example: Multiple scenes with multiple prompts each
```
Winter sunrise | icy landscape || Winter day | snowy skyline || Winter sunset | chilly air || Winter night | clear sky` 
```
would go through 4 winter scenes, with two prompts each:

1. `Winter sunrise` + `icy landscape`
2. `Winter day` + `snowy skyline`
3. `Winter sunset` + `chilly air`
4. `Winter night` + `clear sky`
:::

weights `prompt:weight`
: Apply weights to prompts using the syntx `prompt:weight`

  Higher `weight` values will have more influence on the image, and negative `weight` values will "subtract" the prompt from the image. The default weight is $1$. Weights can also be functions of $t$ to change over the course of an animation.

:::{admonition} Example: Prompts with weights
```
blue sky:10|martian landscape|red sky:-1
``` 
would try to turn the martian sky blue.
:::

stop weights `prompt:targetWeight:stopWeight`
: stop prompts once the image matches them sufficiently with `description:weight:stop`. `stop` should be between $0$ and $1$ for positive prompts, or between $-1$ and $0$ for negative prompts. Lower `stop` values will have more effect on the image (remember that $-1<-0.5<0$). A prompt with a negative `weight` will often go haywire without a stop. Stops can also be functions of $t$ to change over the course of an animation.

:::{admonition} Example: Prompts with stop weights
```
Feathered dinosaurs|birds:1:0.87|scales:-1:-.9|text:-1:-.9
``` 
Would try to make feathered dinosaurs, lightly like birds, without scales or text, but without making 'anti-scales' or 'anti-text.'
:::

Semantic Masking `_`
: Use an underscore to attach a semantic mask to a prompt, using the syntax: `prompt:promptWeight_semantic mask prompt`. The prompt will only be applied to areas of the image that match `semantic mask prompt` according to the CLIP perceiver(s).

:::{admonition} Example: Targeted prompting with a semantic mask
```Khaleesi Daenerys Targaryen | mother of dragons | dragon:3_baby``` 
Would only apply the prompt `dragon:3` to parts of the image that matched the semantic mask's prompt `baby`. If the `mother` prompt causes any images of babies to be generated, this mask will encourage PyTTI to transform just those parts of the image into dragons.
:::

Semantic Image/Video prompts `[fpath]`
: If a prompt is enclosed in brackets, PyTTI will interpret it as a filename or URL. The `fpath` can be a URL or path to an imagefile, or a path to an .mp4 video  The image or video frames will be interpreted by the CLIP perceptor, which will then use the semantic representation of the provided image/video to steer the generative process just as though the perceptor had been asked to interpret the semantic content of a text prompt instead.

:::{admonition} Example: A scene with semantic image prompts and semantic text prompts
```
[artist signature.png]:-1:-.95|[https://i.redd.it/ewpeykozy7e71.png]:3|fractal clouds|hole in the sky
```
:::

Direct Masking `_[fpath]`
: As above, enclosing the mask prompt in brackets will be interpreted as a filename or URL, e.g. `prompt:weight_[fpath]`. If an image or video is provided as a mask, it will be used as a **direct** mask rather than a symantic mask. The prompt will only be applied to the masked (white) areas of the mask image/video. Use `description:weight_[-mask]` to apply the prompt to the black areas instead.

:::{admonition} Example: Targeted prompting with a direct video mask
```
sunlight:3_[mask.mp4]|midnight:3_[-mask.mp4]
``` 
Would apply `sunlight` in the white areas of `mask.mp4`, and `midnight` in the black areas.
:::
