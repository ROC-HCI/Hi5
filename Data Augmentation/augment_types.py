import random
import cv2
import numpy as np

def blur(image, bbox_w, width):
    # blur_type is a random number between 1 and 4
    blur_type = random.randint(1, 4)
    blur_amt = int(bbox_w/width*15 + 1.5)
    if blur_amt > 9:
        blur_amt = 9
    odd = random.randint(1, blur_amt) * 2 + 1

    # add random amount of blur
    if blur_type == 1:
        new_image = cv2.GaussianBlur(image, (odd, odd), 0)
    elif blur_type == 2:
        new_image = cv2.medianBlur(image, odd)
    elif blur_type == 3:
        new_image = cv2.bilateralFilter(image, odd, 75, 75)
    elif blur_type == 4:
        new_image = cv2.blur(image, (odd, odd))

    blur_type_amt = [blur_type, odd]

    return new_image, blur_type_amt


def brightness(image, beta):
    new_image = np.zeros(image.shape, image.dtype)
    new_image = cv2.convertScaleAbs(image, beta=beta)
    return new_image


def color_balance(image, magnitude):
    # convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # split the channels
    h, s, v = cv2.split(hsv)
    # adjust the color balance
    s = s * magnitude
    # convert back to uint8
    s = s.astype('uint8')
    # merge the channels
    hsv = cv2.merge((h, s, v))
    # convert back to BGR
    new_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return new_image


def contrast(image, alpha):
    new_image = np.zeros(image.shape, image.dtype)
    new_image = cv2.convertScaleAbs(image, alpha=alpha)
    return new_image

# New augmentation 4/10/23
def crop(image, x1, x2, y1, y2):
    new_image = image[y1:y2, x1:x2]
    return new_image

def crop_update_coords(coords, bbox, x1, y1):
    x, y, w, h = bbox
    new_bbox = [x-x1, y-y1, w, h]
    new_coords = []
    for i in range(0, len(coords), 2):
        new_coords.append(coords[i]-x1)
        new_coords.append(coords[i+1]-y1)
    return new_coords, new_bbox

def down_upscale(image, scale):
    # resize image
    new_image = cv2.resize(image, None, fx=scale, fy=scale)
    # resize image back to original size
    new_image = cv2.resize(new_image, (image.shape[1], image.shape[0]))
    return new_image


def equalize(image):
    # convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # split the channels
    h, s, v = cv2.split(hsv)
    # equalize the value channel
    v = cv2.equalizeHist(v)
    # merge the channels
    hsv = cv2.merge((h, s, v))
    # convert back to BGR
    new_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return new_image


def flip(image):
    # Flips it both vertically only
    # We trust that this will happen a similar number of times to both right and left hands
    new_image = cv2.flip(image, 0)
    return new_image


def flip_update_coords(coords, size , bbox):
    new_coords = []
    for i in range(0, len(coords), 2):
        new_coords.append(coords[i])
        new_coords.append(size[1] - coords[i+1])

    # update bbox
    x, y, w, h = bbox
    # bbox = [size[0] - x - w, size[1] - y - h, w, h]
    bbox = [x, size[1] - y - h, w, h]
    return new_coords, bbox


def kernel_filter(image):
    new_image = cv2.GaussianBlur(image, (0, 0), 3)
    new_image = cv2.addWeighted(image, 1.5, new_image, -0.5, 0, new_image)
    return new_image


def noise_inject(image, noise_amount):
    # add random noise to the image
    noise = np.zeros(image.shape, np.uint8)
    cv2.randn(noise, (0,0,0), (255,255,255))
    new_image = cv2.addWeighted(image, 1 - noise_amount, noise, noise_amount, 0)
    return new_image


def patch_shuffle(image):
    m = 2
    n = 2
    new_image = np.copy(image)
    for y in range(0, image.shape[0], 2):
        for x in range(0, image.shape[1], 2):
            # randomly shuffle pixels in a mxn patch
            patch = image[y:y + m, x:x + n].copy()
            np.random.shuffle(patch)
            new_image[y:y + m, x:x + n] = patch
    return new_image


def gaussian_erase(image, bbox):
    x, y, w, h = bbox
    mid_x, mid_y = x+w/2, y+h/2
    sigma_x, sigma_y = w/2, h/2
    min_frac, max_frac = 0.15, 0.75
    scew_factor = 0.75
    # random fraction up to h and w
    crop_w, crop_h = np.random.randint(int(w*min_frac), int(w*max_frac)), np.random.randint(int(h*min_frac), int(h*max_frac))
    # crop_w, crop_h = np.random(h/2), np.random(h/2)
    rand_x, rand_y = np.random.normal(mid_x, sigma_x*scew_factor, 1), np.random.normal(mid_y, sigma_y*scew_factor, 1)
    # print(rand_x, rand_y, crop_w, crop_h)
    crop_x, crop_y = int(rand_x - crop_w/2), int(rand_y - crop_h/2)
    # crop image
    image[ crop_y : crop_y + crop_h, crop_x : crop_x + crop_w] = 0
    return image


def scale_same_ratio(image, scale):
    # resize image
    new_image = cv2.resize(image, None, fx=scale, fy=scale)
    return new_image


def ssr_update_coords(coords, scale, bbox):
    new_coords = []
    for i in range(0, len(coords), 2):
        new_coords.append(coords[i]*scale)
        new_coords.append(coords[i+1]*scale)

    # update bbox
    for i in range(0, len(bbox)):
        bbox[i] = bbox[i]*scale

    return new_coords, bbox


def solarize(image):
    mean = image.mean()
    # invert image
    magnitude = int(mean + (255 - mean) * np.random.uniform(0, 1))
    image[image > magnitude] = 255 - image[image > magnitude]
    return image


def solerize_add(image, threshold):
    # invert image
    image[image < 128] = threshold + image[image < 128]
    return image


def stretch(image, stretch_x, stretch_y):
    # get image dimensions
    height, width = image.shape[:2]
    image = cv2.resize(image, (int(width*stretch_x), int(height*stretch_y)), interpolation=cv2.INTER_CUBIC)
    return image


def stretch_update_coords(coords, stretch_x, stretch_y, bbox):
    new_coords = []
    for i in range(0, len(coords), 2):
        new_coords.append(coords[i]*stretch_x)
        new_coords.append(coords[i+1]*stretch_y)

    # update bbox
    bbox[0] = bbox[0]*stretch_x
    bbox[1] = bbox[1]*stretch_y
    bbox[2] = bbox[2]*stretch_x
    bbox[3] = bbox[3]*stretch_y
    return new_coords, bbox

def translate(image, x, y):
    # get image dimensions
    height, width = image.shape[:2]
    # get translation matrix
    translation_matrix = np.float32([[1, 0, x], [0, 1, y]])
    # translate image
    new_image = cv2.warpAffine(image, translation_matrix, (width, height))
    return new_image

def translate_update_coords(coords, x, y, bbox):
    new_coords = []
    for i in range(0, len(coords), 2):
        # print(coords[i])
        new_coords.append(coords[i]+x)
        new_coords.append(coords[i+1]+y)

    # update bbox
    bbox[0] = bbox[0]+x
    bbox[1] = bbox[1]+y
    return new_coords, bbox