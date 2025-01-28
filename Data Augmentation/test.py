import numpy as np
import pandas as pd
import cv2
import os
import sys

image_path = 'images/test/'
output_path = 'images/out/'
csv_path = 'images/test.csv'

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

# Read csv
df = pd.read_csv(csv_path)[5000:]
print("Size of df: ", len(df))
df = df[df['Augment'] == 0]
df = df.reset_index(drop=True)
print("Size of df after: ", len(df))

## Load all images in image_path and apply gaussian_erase
# bbox = df.loc[0, 'Bbox_X':'Bbox_H'].values.tolist()

# sys.exit(0)
for index in range(100):
    # print(list(df['ID'])[index])
    image = str(list(df['ID'])[index])
    image = (12-len(image)) * '0' + image + '.png'
    print("image_path + image: ", image_path + image)
    
    bbox = df.loc[index, 'Bbox_X':'Bbox_H'].values.tolist()
    ## Read image if it exists
    
    if os.path.exists(image_path + image):
        # print("image exists")
        img = cv2.imread(image_path + image)
        img = gaussian_erase(img, bbox)
        cv2.imwrite(output_path + image, img)

        print(bbox)
    