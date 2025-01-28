import cv2
import pandas as pd
import numpy as np
import random

set = "sample/output_augmented_sample"

PATH = "D:/hi5_data/data/new_500k/"
IMG_PATH = PATH + f"{set}/"
SAVE_PATH = PATH + f"{set}_crop/"
CSV_PATH = PATH + f"{set}.csv"

def crop(image, x1, x2, y1, y2):
    # print("image shape: ", image.shape)
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
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

def main():
    df = pd.read_csv(CSV_PATH)
    for index, row in df.iterrows():
        # skip this iteration with 70% probability
        if random.random() < 0.7:
            df.loc[index, 'Crop'] = 0
            continue
        # print(f"index: {index}, ID: {str(row['ID']).zfill(12)}")
        img_name = IMG_PATH + str(row['ID']).zfill(12) + ".png"
        img = cv2.imread(img_name)
        print(f"reading img num: {index}       ", end="\r")
        # print("reading img shape: ", img.shape)
        
        list_coords = row['Wrist_X':'Pinky_D_Y'].values.tolist()
        list_bbox = row['Bbox_X':'Bbox_H'].values.tolist()
        list_size = row['Width':'Height'].values.tolist()
        
        x, y, w, h = list_bbox
        width, height = list_size
        x1 = random.uniform(0, x) if x >= 0 else 0
        y1 = random.uniform(0, y) if y >= 0 else 0
        x2 = random.uniform(x+w, width) if x+w <= width else width
        y2 = random.uniform(y+h, height) if y+h <= height else height
        # print(f"x1 is between 0 and {x} = {x1}")
        # print(f"y1 is between 0 and {y} = {y1}")
        # print(f"x2 is between {x+w} and {width} = {x2}")
        # print(f"y2 is between {y+h} and {height} = {y2}")
        image = crop(img, x1, x2, y1, y2)
        coords, bbox = crop_update_coords(list_coords, list_bbox, x1, y1)
        
        size = [image.shape[1], image.shape[0]]
        
        # print("new image shape: ", image.shape)
        write_name = SAVE_PATH + str(row['ID']).zfill(12) + ".png"
        # print(f"write name: {write_name}\n")
        cv2.imwrite(write_name, image)

        df.loc[index, 'Wrist_X':'Pinky_D_Y'] = coords
        df.loc[index, 'Bbox_X':'Bbox_H'] = bbox
        df.loc[index, 'Width':'Height'] = size
        df.loc[index, 'Crop'] = 1

    print("Writing to csv...")
    df.to_csv(PATH + "{set}_crop.csv", index=False)

if __name__ == "__main__":
    main()
