import cv2
import numpy as np
import skimage
import os
import argparse

parser = argparse.ArgumentParser(description='Add noise to images.')
parser.add_argument("-n", "--noise", help="Choose the amount of noise (s&p).", default="0.1", type=float)
parser.add_argument("-t", "--type", help="Choose the noise type: either g - gaussian or sp - salt&pepper.", default="sp", choices=['g', 'sp'])
parser.add_argument("-p", "--part", help="Choose the part of the image where you want to apply the noise. Choose all that apply (e.g. -p \"1\" \"2\"): 0 - all, 1 - top left, 2 - top right, 3 - bottom left, 4 - bottom right., 12 - top, 34 - bottom, 13 - left,  24 - right", default="0", nargs="*", choices=["0", "1", "2", "3", "4"])
parser.add_argument("-c", "--color", help="Choose if the image should be loaded as black and white or color.", default="c", choices=["bw", "c"])
args = parser.parse_args()

NOISE_AMOUNT = args.noise
MODE = args.type
PART = args.part
COLOR = args.color

if(COLOR == "bw"):
    COLOR = 0
else:
    COLOR = 3

images_directory = "./images"
noise_directory = "./noisedImages"
noise_top_left_directory = "./noisedTopLeft"
noise_top_right_directory = "./noisedTopRight"
noise_bottom_left_directory = "./noisedBottomLeft"
noise_bottom_right_directory = "./noisedBottomRight"
noise_top_directory = "./noisedTop"
noise_bottom_directory = "./noisedBottom"
noise_left_directory = "./noisedLeft"
noise_right_directory = "./noisedRight"

directories = [noise_directory, noise_top_left_directory, noise_top_right_directory, \
noise_bottom_left_directory, noise_bottom_right_directory, noise_top_directory, \
noise_bottom_directory, noise_left_directory, noise_right_directory]

# Create all directories if they don't exist
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

"""
Adds noise to the image in the following order:
- full image
- top left quarter
- top right quarter
- bottom left quarter
- bottom right quarter

This function works as follows:
It loads an image and applies noise to it. Then it takes the needed noised part.
After this, the other parts that are not noised, are being added from the original image.
These images are then saved to the according directory.

Parameters
----------
file: str
    Path to the image that is being noised

"""

def add_noise(file):
    # Get filename for saving image
    filename = os.path.split(file)[1]
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]

    # Load the image
    img = cv2.imread(file, COLOR)

    # Get width and height
    width = int(img.shape[1])
    height = int(img.shape[0])

    # Get half width and height
    halfWidth = int(img.shape[1] / 2)
    halfHeight = int(img.shape[0] / 2)

    # Add noise
    if(MODE == "g"):
        # Add gaussian noise
        noise_img_full = skimage.util.random_noise(img, mode='gaussian', mean=0.1, var=0.01)
    else:
        # Add salt-and-pepper noise to the image
        noise_img_full = skimage.util.random_noise(img, mode='s&p', amount=NOISE_AMOUNT)

    # Create empty image to which the noised part will be pasted
    if(COLOR == 3):
        noise_img = np.zeros([img.shape[0], img.shape[1], img.shape[2]])
    else:
        noise_img = np.zeros([img.shape[0], img.shape[1]])

    # full image
    if("0" in PART):
        full_noise_img = noise_img_full
        cv2.imwrite(f"{noise_directory}/{name}_noise{ext}", full_noise_img * 255)

    # top left
    if("0" in PART or "1" in PART):
        noise_img2 = noise_img_full[:halfHeight, :halfWidth]
        noise_img[:halfHeight, :halfWidth] = noise_img2
        noise_img[halfHeight:] = img[halfHeight:] / 255
        noise_img[:halfHeight, halfWidth:] = img[:halfHeight, halfWidth:] / 255
        cv2.imwrite(f"{noise_top_left_directory}/{name}_top_left{ext}", noise_img * 255)

    # top right
    if("0" in PART or "2" in PART):
        noise_img2 = noise_img_full[:halfHeight, halfWidth:]
        noise_img[:halfHeight, halfWidth:] = noise_img2
        noise_img[halfHeight:] = img[halfHeight:] / 255
        noise_img[:halfHeight, :halfWidth] = img[:halfHeight, :halfWidth] / 255
        cv2.imwrite(f"{noise_top_right_directory}/{name}_top_right{ext}", noise_img * 255)

    # bottom left
    if("0" in PART or "3" in PART):
        noise_img2 = noise_img_full[halfHeight:, :halfWidth]
        noise_img[halfHeight:, :halfWidth] = noise_img2
        noise_img[:halfHeight] = img[:halfHeight] / 255
        noise_img[halfHeight:, halfWidth:] = img[halfHeight:, halfWidth:] / 255
        cv2.imwrite(f"{noise_bottom_left_directory}/{name}_bottom_left{ext}", noise_img * 255)

    # bottom right
    if("0" in PART or "4" in PART):
        noise_img2 = noise_img_full[halfHeight:, halfWidth:]
        noise_img[halfHeight:, halfWidth:] = noise_img2
        noise_img[:halfHeight] = img[:halfHeight] / 255
        noise_img[halfHeight:, :halfWidth] = img[halfHeight:, :halfWidth] / 255
        cv2.imwrite(f"{noise_bottom_right_directory}/{name}_bottom_right{ext}", noise_img * 255)

    # top half
    if("0" in PART or "12" in PART):
        noise_img2 = noise_img_full[:halfHeight]
        noise_img[:halfHeight] = noise_img2
        noise_img[halfHeight:] = img[halfHeight:] / 255
        cv2.imwrite(f"{noise_top_directory}/{name}_top{ext}", noise_img * 255)

    # bottom half
    if("0" in PART or "34" in PART):
        noise_img2 = noise_img_full[halfHeight:]
        noise_img[halfHeight:] = noise_img2
        noise_img[:halfHeight] = img[:halfHeight] / 255
        cv2.imwrite(f"{noise_bottom_directory}/{name}_bottom{ext}", noise_img * 255)

    # left half
    if("0" in PART or "13" in PART):
        noise_img2 = noise_img_full[:, :halfWidth]
        noise_img[:, :halfWidth] = noise_img2
        noise_img[:, halfWidth:] = img[:, halfWidth:] / 255
        cv2.imwrite(f"{noise_left_directory}/{name}_left{ext}", noise_img * 255)

    # right half
    if("0" in PART or "24" in PART):
        noise_img2 = noise_img_full[:, halfWidth:]
        noise_img[:, halfWidth:] = noise_img2
        noise_img[:, :halfWidth] = img[:, :halfHeight] / 255
        cv2.imwrite(f"{noise_right_directory}/{name}_right{ext}", noise_img * 255)

    # Display the resized noised image
    scale_percent = 40 # percent of original size
    width = int(noise_img.shape[1] * scale_percent / 100)
    height = int(noise_img.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(noise_img, dim, interpolation = cv2.INTER_AREA)

    # cv2.imshow('Noise image', resized)

    # cv2.waitKey(0)

for file in os.listdir(images_directory):
    f = os.path.join(images_directory, file)
    if os.path.isfile(f):
        add_noise(f)