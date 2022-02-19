# Prompt Engineering

## General tips for Prompt Engineering

* Use terms that are associated with websites/forums where you would find images that have properties similar to what you are trying to generate. 
  * Naming niche online artistic forums can be extremely powerful.
  * If the forum is too niche, the language model might not have a prior for it.
  * Similarly, keep in mind when the data that trained your model was collected. A model published in 2021 is guaranteed to know nothing about a forum created in 2022.
* Use words describing a medium that might characterize the property you are tying to capture. 
  * "A castle" vs. 
  * "A *photograph of* a castle" vs.
  * "An *illustration of* a castle *from the bookcover of fantasy novel* vs.
* Say the same thing in multiple different ways.
  * "queen" vs
  * "queen | princess | royal woman | victorian queen | fairytale princess | disney princess | cinderella | elegant woman wearing a ballroom gown and tiara | beautiful lady wearing a dress and crown"
* Inventing words and portmanteaus can actually be very effective when done meaningfully.
  * PyTTI language models generally use "sub-word units" for tokenizing text.
  * Use primarily linguistic components that are common in English etymology (e.g. words that have greek, latin, or germanic origin)
* If there are particular artists whose style is similar to what you are after, name the artist and/or style
  * "a sketch of a horse" vs.
  * "a minimalist line sketch of a horse by Pablo Picasso"

## Why does this sort of thing work?

CLIP was trained on a massive dataset of images and text collected from the web. As a consequence, there are certain phrases that may be more or less associated with different image qualities because of how the dataset was constructed. For example, imagine you were using a CLIP model that had been trained exclusively using wikipedia data: it might be reasonable to guess that adding `[[Category: Featured Pictures]]` to the prompt might promote a "higher quality" image generation because of how that category of images is curated. Because our hypothetical model was constructed using data from wikipedia, it has encoded a particular "belief" (a prior probability) about what kinds of images tend to be associated with that phrase. Prompt engineering takes advantage of these priors.

As part of your artistic process, you will likely find yourself developing something of a Grimoire of your own that, along with your preferred image generation settings, characterizes your artistic style.

# Grimoire

The following terms and phrases are potentially useful for promoting desired qualities in an image.

## Prompting for Photorealism

### Prefixes

* A Photograph of
* A photorealistic rendering of
* An ultra-high resolution photograph of

### Suffixes

* trending on Artstation
* 4k UHD
* rendered in Unity
* macrophotography

## Artists and styles

...