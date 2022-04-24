# Settings

## Prompt Controls

scenes
: Descriptions of scenes you want generated, separated by `||`. Each scene can contain multiple prompts, separated by `|`. See [](SceneDSL) for details on scene specification syntax and usage examples.

scene_prefix
: Prompts prepended to the beginning of each scene.

scene_suffix
: prompts appended to the end of each scene.

interpolation_steps
: Number of steps to use smoothly transitioning from the last scene at the start of each scene. $200$ is a good default. Set to $0$ to disable. Transitions are performed by linearly interpolating between the prompts of the two scenes in semantic (CLIP) space.

steps_per_scene 
: Total number of steps to spend rendering each scene. Should be at least `interpolation_steps`. Along with `save_every`, this will control the total length of an animation.

direct_image_prompts
: Paths or urls of images that you want your image to look like in a literal sense, along with `weight_mask` and `stop` values, separated by `|`.

  Apply masks to direct image prompts with `path or url of image:weight_path or url of mask` For video masks it must be a path to an mp4 file.

init_image
: Path or url to an image that will be used to seed the initialization of the image generation process. Useful for creating a central focus or imposing a particular layout on the generated images. If not provided, random noise will be used instead

direct_init_weight
: Defaults to $0$. Use the initial image as a direct image prompt. Equivalent to adding `init_image:direct_init_weight` as a `direct_image_prompt`. Supports weights, masks, and stops.

semantic_init_weight
: Defaults to $0$. Defaults to $0$. Use the initial image as a semantic image prompt. Equivalent to adding `[init_image]:direct_init_weight` as a prompt to each scene in `scenes`. Supports weights, masks, and stops. 

:::{important} Since this is a semantic prompt, you still need to put the mask in `[` `]` to denote it as a path or url, otherwise it will be read as text instead of a file.
:::

## Image Representation Controls

width, height 
: Image size. Set one of these $-1$ to derive it from the aspect ratio of the init image.

pixel_size 
: Integer image scale factor. Makes the image bigger. Set to $1$ for VQGAN or face VRAM issues.

smoothing_weight
: Makes the image smoother. Defaults to $0$ (no smoothing). Can also be negative for that deep fried look.

image_model
: Select how your image will be represented. Supported image models are:
  * Limited Palette - Use CLIP to optimize image pixels directly, constrained to a fix number of colors. Generally used for pixel art.
  * Unlimited Palette - Use CLIP to optimize image pixels directly
  * VQGAN - Use CLIP to optimize a VQGAN's latent representation of an image

vqgan_model
: Select which VQGAN model to use (only considered for `image_model: VQGAN`)

random_initial_palette
: If checked, palettes will start out with random colors. Otherwise they will start out as grayscale. (only for `image_model: Limited Palette`)

palette_size
: Number of colors in each palette. (only for `image_model: Limited Palette`)

palettes
: total number of palettes. The image will have `palette_size*palettes` colors total. (only for `image_model: Limited Palette`)

gamma
: Relative gamma value. Higher values make the image darker and higher contrast, lower values make the image lighter and lower contrast. (only for `image_model: Limited Palette`). $1$ is a good default.

hdr_weight
: How strongly the optimizer will maintain the `gamma`. Set to $0$ to disable. (only for `image_model: Limited Palette`)

palette_normalization_weight
: How strongly the optimizer will maintain the palettes' presence in the image. Prevents the image from losing palettes. (only for `image_model: Limited Palette`)

show_palette
: Display a palette sample each time the image is displayed. (only for `image_model: Limited Palette`)

target_pallete
: Path or url of an image which the model will use to make the palette it uses.

lock_pallete
: Force the model to use the initial palette (most useful from restore, but will force a grayscale image or a wonky palette otherwise).

## Animation Controls

animation_mode
: Select animation mode or disable animation. Supported animation modes are:
  * off
  * 2D
  * 3D
  * Video Source

sampling_mode
: How pixels are sampled during animation. `nearest` will keep the image sharp, but may look bad. `bilinear` will smooth the image out, and `bicubic` is untested :)

infill_mode
: Select how new pixels should be filled if they come in from the edge.
  * mirror: reflect image over boundary
  * wrap: pull pixels from opposite side
  * black: fill with black 
  * smear: sample closest pixel in image

pre_animation_steps
: Number of steps to run before animation starts, to begin with a stable image. $250$ is a good default.

steps_per_frame
: number of steps between each image move. $50$ is a good default.

frames_per_second
: Number of frames to render each second. Controls how $t$ is scaled.

direct_stabilization_weight
: Keeps the current frame as a direct image prompt. For `Video Source` this will use the current frame of the video as a direct image prompt. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_mask.mp4`.

semantic_stabilization_weight
: Keeps the current frame as a semantic image prompt. For `Video Source` this will use the current frame of the video as a direct image prompt. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_[mask.mp4]` or `weight_mask phrase`.

depth_stabilization_weight
: Keeps the depth model output somewhat consistent at a *VERY* steep performance cost. For `Video Source` this will use the current frame of the video as a semantic image prompt. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_mask.mp4`.

edge_stabilization_weight
: Keeps the images contours somewhat consistent at very little performance cost. For `Video Source` this will use the current frame of the video as a direct image prompt with a sobel filter. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_mask.mp4`.

flow_stabilization_weight
: Used for `animation_mode: 3D` and `Video Source` to prevent flickering. Comes with a slight performance cost for `Video Source`, and a great one for `3D`, due to implementation differences. Also supports masks: `weight_mask.mp4`. For video source, the mask should select the part of the frame you want to move, and the rest will be treated as a still background.

video_path
: path to mp4 file for `Video Source`

frame_stride
: Advance this many frames in the video for each output frame. This is surprisingly useful. Set to $1$ to render each frame. Video masks will also step at this rate.

reencode_each_frame
: Use each video frame as an `init_image` instead of warping each output frame into the init for the next. Cuts will still be detected and trigger a reencode.

flow_long_term_samples
: Sample multiple frames into the past for consistent interpolation even with disocclusion, as described by [Manuel Ruder, Alexey Dosovitskiy, and Thomas Brox (2016)](https://arxiv.org/abs/1604.08610). Each sample is twice as far back in the past as the last, so the earliest sampled frame is $2^{\text{long_term_flow_samples}}$ frames in the past. Set to $0$ to disable.

## Motion Controls

translate_x
: Horizontal image motion as a function of time $t$ in seconds.

translate_y
: Vertical image motion as a function of time $t$ in seconds.

translate_z_3d
: Forward image motion as a function of time $t$ in seconds. (only for `animation_mode:3D`)

rotate_3d
: Image rotation as a quaternion $\left[r,x,y,z\right]$ as a function of time $t$ in seconds. (only for `animation_mode:3D`)

rotate_2d
: Image rotation in degrees as a function of time $t$ in seconds. (only for `animation_mode:2D`)

zoom_x_2d
: Horizontal image zoom as a function of time $t$ in seconds. (only for `animation_mode:2D`)

zoom_y_2d
: Vertical image zoom as a function of time $t$ in seconds. (only for `animation_mode:2D`)

lock_camera
: Prevents scrolling or drifting. Makes for more stable 3D rotations. (only for `animation_mode:3D`)

field_of_view
: Vertical field of view in degrees. (only for `animation_mode:3D`)

near_plane
: Closest depth distance in pixels. (only for `animation_mode:3D`)

far_plane
: Farthest depth distance in pixels. (only for `animation_mode:3D`)

## Audio Reactivity controls

:::{admonition} Experimental Feature
As of 2022-04-24, this section describes features that are available on the 'test' branch but have not yet been merged into the main release
:::

input_audio
: path to audio file.

input_audio_offset
: timestamp (in seconds) where pytti should start reading audio. Defaults to `0`.

input_audio_filters
: list of specifications for individual Butterworth bandpass filters.

### Bandpass filter specification

For technical details on how these filters work, see: [Butterworth Bandpass Filters](https://en.wikipedia.org/wiki/Butterworth_filter)


variable_name
: the variable name through which the value of the filter will be referenced in the `weight` expression of the prompt. Subject to rules of python variable naming.

f_center
: The target frequency of the bandpass filter.

f_width
: the range of frequencies about the central frequency which the filter will be responsive to.

order
: the slope of the frequency response. Default is 5. The higher the "order" of the filter, the more closely the frequency response will resemble a square/step function. Decreasing order will make the filter more permissive of frequencies outside of the range strictly specified by the center and width above. See [https://en.wikipedia.org/wiki/Butterworth_filter#Transfer_function](https://en.wikipedia.org/wiki/Butterworth_filter#Transfer_function) for details.

:::{admonition} Example: Audio reactivity specification
```

scenes:"
  a photograph of a beautiful spring day:2 | 
  flowers blooming: 10*fHi |

  coloful sparks: (fHi+fLo) | 
  sun rays: fHi | 
  forest: fLo | 

  ominous: fLo/(fLo + fHi) | 
  hopeful: fHi/(fLo + fHi) | 
  "

input_audio: '/path/to/audio/source.mp3'
input_audio_offset: 0
input_audio_filters:
- variable_name: fLo
  f_center: 105
  f_width: 65
  order: 5
- variable_name: fHi
  f_center: 900
  f_width: 600
  order: 5

frames_per_second: 30
``` 
Would create two filters named `fLo` and `fHi`, which could then be referenced in the scene specification DSL to tie prompt weights to properties of the input audio at the appropriate time stamp per the specified FPS.
:::


## Output Controls

file_namespace
: Output directory name.

allow_overwrite
: Check to overwrite existing files in `file_namespace`.

display_every
: How many steps between each time the image is displayed in the notebook.

clear_every
: How many steps between each time notebook console is cleared.

display_scale
: Image display scale in notebook. $1$ will show the image at full size. Does not affect saved images.

save_every
: How many steps between each time the image is saved. Set to `steps_per_frame` for consistent animation.

backups
: Number of backups to keep (only the oldest backups are deleted). Large images make very large backups, so be warned. Set to `all` to save all backups. These are used for the `flow_long_term_samples` so be sure that this is at least $2^{\text{flow_long_term_samples}}+1$ for `Video Source` mode.

show_graphs
: Display graphs of the loss values each time the image is displayed. Disable this for local runtimes.

approximate_vram_usage
: Currently broken. Don't believe its lies.

## Perceptor Settings

ViTB32, ViTB16, RN50, RN50x4... 
: Select which CLIP models to use for semantic perception. Multiple models may be selected. Each model requires significant VRAM.

learning_rate
: How quickly the image changes.

reset_lr_each_frame
: The optimizer will adaptively change the learning rate, so this will thwart it.

seed 
: Pseudorandom seed. Using a fixed seed will make your process more deterministic, which can be useful for comparing how change specific settings impacts the generated images

cutouts
: The number of cutouts from the image that will be scored by the perceiver. Think of each cutout as a "glimpse" at the image. The more glimpses you give the perceptor, the better it will understand what it is looking at. Reduce this to use less VRAM at the cost of quality and speed.

cut_pow
: Should be positive. Large values shrink cutouts, making the image more detailed, small values expand the cutouts, making it more coherent. $1$ is a good default. $3$ or higher can cause crashes.

cutout_border
: Should be between $0$ and $1$. Allows cutouts to poke out over the edges of the image by this fraction of the image size, allowing better detail around the edges of the image. Set to $0$ to disable. $0.25$ is a good default.

border_mode
: how to fill cutouts that stick out over the edge of the image. Match with `infill_mode` for consistent infill.

* clamp: move cutouts back onto image
* mirror: reflect image over boundary
* wrap: pull pixels from opposite side
* black: fill with black 
* smear: sample closest pixel in image

gradient_accumulation_steps
: How many batches to use to process cutouts. Must divide `cutouts` evenly, defaults to $1$. If you are using high cutouts and receiving VRAM errors, increasing `gradient_accumulation_steps` may permit you to generate images without reducing the cutouts setting. Setting this higher than $1$ will slow down the process proportionally.

models_parent_dir
: Parent directory beneath which models will be downloaded. Defaults to `~/.cache/`, a hidden folder in your user namespace. E.g. the default storage location for the AdaBins model is `~/.cache/adabins/AdaBins_nyu.pt`
