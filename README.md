# Image noise script

A script made for a university project in the course Scripting languages.
The main goal is adding noise to images so that they can be added into datasets.
Technologies: Python

## Content
- [Image noise script](#image-noise-script)
  - [Content](#content)
  - [Description](#description)
  - [Arguments](#arguments)
  - [Examples](#examples)
    - [Example 1](#example-1)
    - [Example 2](#example-2)
    - [Example 3](#example-3)

## Description

The script is used to add noise to selected parts of the image.
At the beginning, all directories are created, if they do not already exist. After that, it iterates through the images in the directory where the dataset is located. Noise (salt & pepper or gauss) is then added to those images on those parts that were selected with arguments when calling the script. Depending on which parts of the image you chose to add noise to, the resulting ones will be saved in those directories.

## Arguments

```-n, --noise``` – selection of the amount of noise to be set on s&p noise

- Default value: 0.1

```-t, --type``` – selection of the type of noise added to the image:
- sp – salt & pepper
- g – gaussian (mean value – 0.1, variance – 0.01)
Default value: sp

```-p, --part``` – part of the image to which noise should be applied. Each of the selected options saves images to the corresponding directory. For example, if the options up-left and down-right are selected, images for up-left will be saved in its own directory, and images for down-right in its own. The example command in terminal to call this argument is:
```-p "1" "2"```

- 0 – all parts of the image + the whole image
- 1 – top left
- 2 – top right
- 3 – bottom left
- 4 – lower right
- 12 – upper half
- 34 – lower half
- 13 – left half
- 24 – lower half

- Default value: 0

```-c, --color``` – choosing whether the image should be loaded in color (c) or black and white (bw)
- c – in color
- bw – black & white
- Default value: c

## Examples
Dataset available at: https://www.kaggle.com/datasets/andrewmvd/animal-faces

### Example 1
S&P noise added to the left part of the image

<img src="./example1sp.png" alt="example of S&P noise">

### Example 2
Gauss noise added to the left part of the image

<img src="./example2gauss.png" alt="example of gauss noise">

### Example 3
Gauss noise added to all parts of the image

<img src="./example3.png" alt="example of gauss noise">