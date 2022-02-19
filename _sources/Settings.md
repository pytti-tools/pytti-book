`scenes:` Descriptions of scenes you want generated, separated by `||`. Each scene can contain multiple prompts, separated by `|`.

*Example:* `Winter sunrise | icy landscape || Winter day | snowy skyline || Winter sunset | chilly air || Winter night | clear sky` would go through several winter scenes.

**Advanced:** weight prompts with `description:weight`. Higher `weight` values will be prioritized by the optimizer, and negative `weight` values will remove the description from the image. The default weight is $1$. Weights can also be functions of $t$ to change over the course of an animation.

*Example scene:* `blue sky:10|martian landscape|red sky:-1` would try to turn the martian sky blue.

**Advanced:** stop prompts once the image matches them sufficiently with `description:weight:stop`. `stop` should be between $0$ and $1$ for positive prompts, or between $-1$ and $0$ for negative prompts. Lower `stop` values will have more effect on the image (remember that $-1<-0.5<0$). A prompt with a negative `weight` will often go haywire without a stop. Stops can also be functions of $t$ to change over the course of an animation.

*Example scene:* `Feathered dinosaurs|birds:1:0.87|scales:-1:-.9|text:-1:-.9` Would try to make feathered dinosaurs, lightly like birds, without scales or text, but without making 'anti-scales' or 'anti-text.'

#**NEW:**

**Advanced:** Use `description:weight_mask description` with a text prompt as `mask`. The prompt will only be applied to areas of the image that match `mask description` according to CLIP.

*Example scene:* `Khaleesi Daenerys Targaryen | mother of dragons | dragon:3_baby` would only apply the weight `dragon` to parts of the image that match `baby`, thus turning the babies that `mother` tends to make into dragons (hopefully).

**Advanced:** Use `description:weight_[mask]` with a URL or path to an image, or a path to a .mp4 video to use as a `mask`. The prompt will only be applied to the masked (white) areas of the mask image. Use `description:weight_[-mask]` to apply the prompt to the black areas instead.

*Example scene:* `sunlight:3_[mask.mp4]|midnight:3_[-mask.mp4]` Would apply `sunlight` in the white areas of `mask.mp4`, and `midnight` in the black areas.

**Legacy:** Directional weights will still work as before, but they aren't as good as masks.

**Advanced:** Use `[path or url]` as a prompt to add a semantic image prompt. This will be read by CLIP and understood as a near perfect text description of the image.

*Example scene:* `[artist signature.png]:-1:-.95|[https://i.redd.it/ewpeykozy7e71.png]:3|fractal clouds|hole in the sky`

---

`scene_prefix:` text prepended to the beginning of each scene.

*Example:* `Trending on Arstation|`

`scene_suffix:` text appended to the end of each scene.

*Example:* ` by James Gurney`

`interpolation_steps:` number of steps to spend smoothly transitioning from the last scene at the start of each scene. $200$ is a good default. Set to $0$ to disable.

`steps_per_scene:` total number of steps to spend rendering each scene. Should be at least `interpolation_steps`. This will indirectly control the total length of an animation.

---
#**NEW**: 
`direct_image_prompts:` paths or urls of images that you want your image to look like in a literal sense, along with `weight_mask` and `stop` values, separated by `|`.

Apply masks to direct image prompts with `path or url of image:weight_path or url of mask` For video masks it must be a path to an mp4 file.

**Legacy** latent image prompts are no more. They are now rolled into direct image prompts.

---

`init_image:` path or url of start image. Works well for creating a central focus.


`direct_init_weight:` Defaults to $0$. Use the initial image as a direct image prompt. Equivalent to adding `init_image:direct_init_weight` as a `direct_image_prompt`. Supports weights, masks, and stops.

`semantic_init_weight:` Defaults to $0$. Defaults to $0$. Use the initial image as a semantic image prompt. Equivalent to adding `[init_image]:direct_init_weight` as a prompt to each scene in `scenes`. Supports weights, masks, and stops. **IMPORTANT** since this is a semantic prompt, you still need to put the mask in `[` `]` to denote it as a path or url, otherwise it will be read as text instead of a file.

---

`width`, `height:` image size. Set one of these $-1$ to derive it from the aspect ratio of the init image.

`pixel_size:` integer image scale factor. Makes the image bigger. Set to $1$ for VQGAN or face VRAM issues.

`smoothing_weight:` makes the image smoother. Defaults to $0$ (no smoothing). Can also be negative for that deep fried look.

`image_model:` select how your image will be represented.

`vqgan_model:` select your VQGAN version (only for `image_model: VQGAN`)

`random_initial_palette:` if checked, palettes will start out with random colors. Otherwise they will start out as grayscale. (only for `image_model: Limited Palette`)

`palette_size:` number of colors in each palette. (only for `image_model: Limited Palette`)

`palettes:` total number of palettes. The image will have `palette_size*palettes` colors total. (only for `image_model: Limited Palette`)

`gamma:` relative gamma value. Higher values make the image darker and higher contrast, lower values make the image lighter and lower contrast. (only for `image_model: Limited Palette`). $1$ is a good default.

`hdr_weight:` how strongly the optimizer will maintain the `gamma`. Set to $0$ to disable. (only for `image_model: Limited Palette`)

`palette_normalization_weight:` how strongly the optimizer will maintain the palettes' presence in the image. Prevents the image from losing palettes. (only for `image_model: Limited Palette`)

`show_palette:` check this box to see the palette each time the image is displayed. (only for `image_model: Limited Palette`)

`target_pallete:` path or url of an image which the model will use to make the palette it uses.

`lock_pallete:` force the model to use the initial palette (most useful from restore, but will force a grayscale image or a wonky palette otherwise).

---

`animation_mode:` select animation mode or disable animation.

`sampling_mode:` how pixels are sampled during animation. `nearest` will keep the image sharp, but may look bad. `bilinear` will smooth the image out, and `bicubic` is untested :)

`infill_mode:` select how new pixels should be filled if they come in from the edge.
* mirror: reflect image over boundary
* wrap: pull pixels from opposite side
* black: fill with black 
* smear: sample closest pixel in image

`pre_animation_steps:` number of steps to run before animation starts, to begin with a stable image. $250$ is a good default.

`steps_per_frame:` number of steps between each image move. $50$ is a good default.

`frames_per_second:` number of frames to render each second. Controls how $t$ is scaled.

`direct_stabilization_weight: ` keeps the current frame as a direct image prompt. For `Video Source` this will use the current frame of the video as a direct image prompt. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_mask.mp4`.

`semantic_stabilization_weight: ` keeps the current frame as a semantic image prompt. For `Video Source` this will use the current frame of the video as a direct image prompt. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_[mask.mp4]` or `weight_mask phrase`.

`depth_stabilization_weight: ` keeps the depth model output somewhat consistent at a *VERY* steep performance cost. For `Video Source` this will use the current frame of the video as a semantic image prompt. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_mask.mp4`.

`edge_stabilization_weight: ` keeps the images contours somewhat consistent at very little performance cost. For `Video Source` this will use the current frame of the video as a direct image prompt with a sobel filter. For `2D` and `3D` this will use the shifted version of the previous frame. Also supports masks: `weight_mask.mp4`.

`flow_stabilization_weight: ` used for `animation_mode: 3D` and `Video Source` to prevent flickering. Comes with a slight performance cost for `Video Source`, and a great one for `3D`, due to implementation differences. Also supports masks: `weight_mask.mp4`. For video source, the mask should select the part of the frame you want to move, and the rest will be treated as a still background.

---
`video_path: ` path to mp4 file for `Video Source`

`frame_stride` advance this many frames in the video for each output frame. This is surprisingly useful. Set to $1$ to render each frame. Video masks will also step at this rate.

`reencode_each_frame: ` check this box to use each video frame as an `init_image` instead of warping each output frame into the init for the next. Cuts will still be detected and trigger a reencode.


`flow_long_term_samples: ` Sample multiple frames into the past for consistent interpolation even with disocclusion, as described by [Manuel Ruder, Alexey Dosovitskiy, and Thomas Brox (2016)](https://arxiv.org/abs/1604.08610). Each sample is twice as far back in the past as the last, so the earliest sampled frame is $2^{\text{long_term_flow_samples}}$ frames in the past. Set to $0$ to disable.

---

`translate_x:` horizontal image motion as a function of time $t$ in seconds.

`translate_y:` vertical image motion as a function of time $t$ in seconds.

`translate_z_3d:` forward image motion as a function of time $t$ in seconds. (only for `animation_mode:3D`)

`rotate_3d:` image rotation as a quaternion $\left[r,x,y,z\right]$ as a function of time $t$ in seconds. (only for `animation_mode:3D`)

`rotate_2d:` image rotation in degrees as a function of time $t$ in seconds. (only for `animation_mode:2D`)

`zoom_x_2d:` horizontal image zoom as a function of time $t$ in seconds. (only for `animation_mode:2D`)

`zoom_y_2d:` vertical image zoom as a function of time $t$ in seconds. (only for `animation_mode:2D`)

`lock_camera:` check this box to prevent all scrolling or drifting. Makes for more stable 3D rotations. (only for `animation_mode:3D`)

`field_of_view:` vertical field of view in degrees. (only for `animation_mode:3D`)

`near_plane:` closest depth distance in pixels. (only for `animation_mode:3D`)

`far_plane:` farthest depth distance in pixels. (only for `animation_mode:3D`)

---

`file_namespace:` output directory name.

`allow_overwrite:` check to overwrite existing files in `file_namespace`.

`display_every:` how many steps between each time the image is displayed in the notebook.

`clear_every:` how many steps between each time notebook console is cleared.

`display_scale:` image display scale in notebook. $1$ will show the image at full size. Does not affect saved images.

`save_every:` how many steps between each time the image is saved. Set to `steps_per_frame` for consistent animation.

`backups:` number of backups to keep (only the oldest backups are deleted). Large images make very large backups, so be warned. Set to `all` to save all backups. These are used for the `flow_long_term_samples` so be sure that this is at least $2^{\text{flow_long_term_samples}}+1$ for `Video Source` mode.

`show_graphs:` check this to see graphs of the loss values each time the image is displayed. Disable this for local runtimes.

`approximate_vram_usage:` currently broken. Don't believe its lies.

---

`ViTB32, ViTB16, RN50, RN50x4:` select your CLIP models. These take a lot of VRAM.

`learning_rate:` how quickly the image changes.

`reset_lr_each_frame:` the optimizer will adaptively change the learning rate, so this will thwart it.

`seed:` pseudorandom seed.

---

`cutouts:` number of cutouts. Reduce this to use less VRAM at the cost of quality and speed.

`cut_pow:` should be positive. Large values shrink cutouts, making the image more detailed, small values expand the cutouts, making it more coherent. $1$ is a good default. $3$ or higher can cause crashes.

`cutout_border:` should be between $0$ and $1$. Allows cutouts to poke out over the edges of the image by this fraction of the image size, allowing better detail around the edges of the image. Set to $0$ to disable. $0.25$ is a good default.

`border_mode:` how to fill cutouts that stick out over the edge of the image. Match with `infill_mode` for consistent infill.

* clamp: move cutouts back onto image
* mirror: reflect image over boundary
* wrap: pull pixels from opposite side
* black: fill with black 
* smear: sample closest pixel in image