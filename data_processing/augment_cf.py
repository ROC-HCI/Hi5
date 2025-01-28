import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import cv2
import random
import os

import augment_types as aug

PATH = "D:/hi5_data/data/new_500k/"
FILE_NAME = "output"
SAVE_NAME = "augmented"

IMAGE_PATH = PATH+FILE_NAME+"/"
CSV_PATH = PATH+FILE_NAME+".csv"

SAVE_IMAGE_PATH = PATH+FILE_NAME+"_"+SAVE_NAME+"/"
SAVE_CSV_PATH = PATH+FILE_NAME+"_"+SAVE_NAME+".csv"


def augment_random(image, augment_type, coords, bbox, size):
    if augment_type == "Brightness":
        # random number between -75 and 75
        beta = random.randint(-75, 75)
        image = aug.brightness(image, beta)
        amount = beta
    elif augment_type == "ColorBalance":
        # random float between 0 and 1.2
        magnitude = random.uniform(0, 1.2)
        image = aug.color_balance(image, magnitude)
        amount = magnitude
    elif augment_type == "Contrast":
        # random float between 0.5 and 1.5
        alpha = random.uniform(0.5, 1.5)
        image = aug.contrast(image, alpha)
        amount = alpha
    elif augment_type == "Crop":
        x, y, w, h = bbox
        width, height = size
        x1 = random.randint(0, x) if x >= 0 else 0
        y1 = random.randint(0, y) if y >= 0 else 0
        x2 = random.randint(x+w, width) if x+w <= width else width
        y2 = random.randint(y+h, height) if y+h <= height else height
        image = aug.crop(image, x1, y1, x2, y2)
        coords, bbox = aug.crop_update_coords(coords, bbox, x1, y1)
    elif augment_type == "DownUpscale":
        # random float between 0.1 and 0.9
        scale = random.uniform(0.1, 0.9)
        image = aug.down_upscale(image, scale)
        amount = scale
    elif augment_type == "Equalize":
        image = aug.equalize(image)
        amount = 1
    elif augment_type == "Flip":
        image = aug.flip(image)
        coords, bbox = aug.flip_update_coords(coords, size, bbox)
        amount = 1
    elif augment_type == "KernelFilter":
        image = aug.kernel_filter(image)
        amount = 1
    elif augment_type == "NoiseInject":
        # random float between 0 and 0.5
        noise_amount = random.uniform(0, 0.5)
        image = aug.noise_inject(image, noise_amount)
        amount = noise_amount
    elif augment_type == "PatchShuffle":
        image = aug.patch_shuffle(image)
        amount = 1
    elif augment_type == "GaussianErase":
        image = aug.gaussian_erase(image, bbox)
        amount = 1
    elif augment_type == "ScaleSameRatio":
        # random float between 0.5 and 1.0
        scale = random.uniform(0.5, 1.0)
        image = aug.scale_same_ratio(image, scale)
        coords, bbox = aug.ssr_update_coords(coords, scale, bbox)
        amount = scale
    elif augment_type == "Solarize":
        image = aug.solarize(image)
        amount = 1
    elif augment_type == "SolerizeAdd":
        # random number between 0 and 50
        threshold = random.randint(0, 50)
        image = aug.solerize_add(image, threshold)
        amount = threshold
    elif augment_type == "Stretch":
        # random float between 0.5 and 1.5
        stretch_x = random.uniform(0.5, 1.5)
        stretch_y = random.uniform(0.5, 1.5)
        image = aug.stretch(image, stretch_x, stretch_y)
        coords, bbox = aug.stretch_update_coords(coords, stretch_x, stretch_y, bbox)
        amount = [stretch_x, stretch_y]
    elif augment_type == "Translate":
        # random number between -100 and 100
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        image = aug.translate(image, x, y)
        coords, bbox = aug.translate_update_coords(coords, x, y, bbox)
        amount = [x, y]
    
    size = [image.shape[1], image.shape[0]]
    
    return image, coords, bbox, size, amount


def data_expurgation(df):
    # go through each row, pair up x and y coordinates, check if 11 or more are more than (0,0) and less than (576,720)
    # if so, keep the row, else, delete the row and delete the image based on the ID
    print("\nExpurgating data...")
    # create empty df
    df_new = pd.DataFrame(columns=df.columns)
    removed = 0
    for index, row in df.iterrows():
        if index % 100 == 0:
            print("Expurgating: " + str(index) + "/" + str(len(df)), end="\r")
        list_coords = row['Wrist_X':'Pinky_D_Y'].values.tolist()
        list_bbox = row['Bbox_X':'Bbox_H'].values.tolist()
        w, h = row['Width'], row['Height']
        xs = list_coords[0::2]
        ys = list_coords[1::2]
        id = row['ID']
        # zip the x and y coordinates together
        coords = list(zip(xs, ys))
        # count how many coordinates are in the image
        count = 0
        skip = False
        for coord in coords:
            if coord[0] >= 0 and coord[1] >= 0 and coord[0] <= w and coord[1] <= h:
                count += 1
            if coord[0] < -0.5*w or coord[1] < -0.5*h or coord[0] > 1.5*w or coord[1] > 1.5*h:
                skip = True
        if list_bbox[0] < -0.5*w or list_bbox[1] < -0.5*h or list_bbox[0]+list_bbox[2] > 1.5*w or list_bbox[1]+list_bbox[3] > 1.5*h:
            skip = True
        if count >= 11 and not skip:
            df_new = df_new.append(row)
        else: 
            removed += 1
            os.remove(SAVE_IMAGE_PATH + str(id).zfill(12) + ".png")
    print("Expurgating: " + str(len(df)) + "/" + str(len(df)))
    print("Expurgated " + str(removed) + " images")
    print("Remaining images: " + str(len(df_new)))
    return df_new


def augment_cf(df):
    print("Augmentation started")
    df["RL"] = np.nan
    df['Augment'] = np.nan
    df['Blur'] = np.nan
    df['Geometric'] = np.nan
    df['Color'] = np.nan
    df['Gaussian 1'] = np.nan
    df['Gaussian 2'] = np.nan

    augmentations = ["Brightness", "ColorBalance", "Contrast", "DownUpscale", "Equalize", "Flip", "KernelFilter", "NoiseInject", "PatchShuffle", "GaussianErase", "ScaleSameRatio", "Solarize", "SolerizeAdd", "Stretch", "Translate"]
    for augment in augmentations:
        df[augment] = np.nan

    geometric_transformations = ["DownUpscale", "ScaleSameRatio", "Stretch", "Translate"]
    color_operations = ["Brightness", "ColorBalance", "Contrast", "Equalize", "KernelFilter", "NoiseInject", "PatchShuffle", "Solarize", "SolerizeAdd"]

    for index, row in df.iterrows(): 
        if index % 100 == 0:
            print("Augmenting: " + str(index) + "/" + str(len(df)), end="\r")
        image = cv2.imread(IMAGE_PATH + str(row["ID"]).zfill(12) + ".png")

        # probability(0.15, 0.5, 0.3, 0.3) # GE, BL, GT, CO
        # 0.7917500000000001
        # probability(0.075, 0.25, 0.15, 0.15)
        # 0.498765625
        # probability(0.15/4, 0.5/4, 0.3/4, 0.3/4)
        # 0.27940332031250004
        low_aug = {"GE": 0.15/4, "BL": 0.5/4, "GT": 0.3/4, "CO":  0.3/4}
        mid_aug = {"GE": 0.075, "BL":  0.25, "GT": 0.15, "CO":  0.15}
        high_aug = {"GE": 0.15, "BL":  0.5, "GT": 0.3, "CO":  0.3}

        is_flip = random.choice([True, False]) # Right to left -> Not an augmentation
        is_vertical_flip = random.choice([True, False]) # Vertical flip -> Is an augmentation (but not counted as such in the csv to ensure we get the expected 79% augmentation rate)

        # Augmentation probabilities
        is_gaussian_1 = random.random() < high_aug["GE"]/2 # Gaussian erase
        is_blur = random.random() < high_aug["BL"] # Blur
        is_geometric = random.random() < high_aug["GT"] # Geometric transformations
        is_color = random.random() < high_aug["CO"] # Color operations
        is_gaussian_2 = random.random() < high_aug["GE"]/2 # Gaussian erase

        df.at[index, "Augment"] = 1 if is_gaussian_1 or is_blur or is_geometric or is_color or is_gaussian_2 else 0
        df.at[index, "GaussianErase"] = 1 if is_gaussian_1 or is_gaussian_2 else 0

        # Updates all the columns that ends with '_X', 'Bbox_X', and 'RL' to the new values
        if is_flip: # Flips from right to left
            # For all columns that ends with '_X', subtract the value from the width of the image (given by the 'Width' column)
            df.loc[index, df.columns.str.endswith('_X')] = df.loc[index, 'Width'] - df.loc[index, df.columns.str.endswith('_X')]
            # Additionally, subtract the 'Bbox_W' value from the 'Bbox_X' value
            df.loc[index, 'Bbox_X'] = df.loc[index, 'Bbox_X'] - df.loc[index, 'Bbox_W']
            df.at[index, "RL"] = "left"
            image = cv2.flip(image, 1)
        else: 
            df.at[index, "RL"] = "right"

        # These are the values that will be updated throughout the augmentation process
        list_coords = df.loc[index, 'Wrist_X':'Pinky_D_Y'].values.tolist()
        list_bbox = df.loc[index, 'Bbox_X':'Bbox_H'].values.tolist()
        list_size = df.loc[index, 'Width':'Height'].values.tolist()

        # Augmentation step 1 - No coordinates changed
        if is_gaussian_1: # Gaussian erase
            image, list_coords, list_bbox, list_size, amount = augment_random(image, "GaussianErase", list_coords, list_bbox, list_size)
            df.at[index, "Gaussian 1"] = amount
        else:
            df.at[index, "Gaussian 1"] = 0

        # Augmentation step 2 - No coordinates changed
        if is_blur and df.at[index, "MotionBlur"] == 0: # Dataset does not have motion blur since Unity adds it  to the background too
            bbox_width = df.at[index, "Bbox_W"]
            image_width = df.at[index, "Width"]
            image, blur_type_amt = aug.blur(image, bbox_width, image_width)
            df.at[index, "Blur"] = str(blur_type_amt)
        else:
            df.at[index, "Blur"] = 0

        # Augmentation step 3 - Coordinates updated (1/2)
        if is_vertical_flip:
            # print("\nold coords: ", list_coords[:5])
            # print("old bbox: ", list_bbox)
            image, list_coords, list_bbox, list_size, amount = augment_random(image, "Flip", list_coords, list_bbox, list_size)
            df.at[index, "RL"] = "right" if df.at[index, "RL"] == "left" else "left"
            df.at[index, "Flip"] = amount
            # print("new coords: ", list_coords[:5])
            # print("new bbox: ", list_bbox)
            # cv2.imshow("image", image)
            # cv2.waitKey(0)
        else:
            df.at[index, "Flip"] = 0

        # Augmentation step 4 - Coordinates updated (2/2)
        if is_geometric:
            df.at[index, "Geometric"] = 1
            # pick a random geometric transformation
            geometric_choice = random.choice(geometric_transformations)
            image, list_coords, list_bbox, list_size, amount = augment_random(image, geometric_choice, list_coords, list_bbox, list_size)
            for geometric in geometric_transformations:
                if geometric == geometric_choice:
                    df.at[index, geometric] = str(amount)
                else:
                    df.at[index, geometric] = 0
        else:
            df.at[index, "Geometric"] = 0
            for geometric in geometric_transformations:
                df.at[index, geometric] = 0

        # Augmentation step 5 - No coordinates changed
        if is_color:
            df.at[index, "Color"] = 1
            # pick a random color operation
            color_choice = random.choice(color_operations)
            image, list_coords, list_bbox, list_size, amount = augment_random(image, color_choice, list_coords, list_bbox, list_size)
            for color in color_operations:
                if color == color_choice:
                    df.at[index, color] = str(amount)
                else:
                    df.at[index, color] = 0
        else:
            df.at[index, "Color"] = 0
            for color in color_operations:
                df.at[index, color] = 0

        # Augmentation step 6 - No coordinates changed
        if is_gaussian_2: # Gaussian erase
            image, list_coords, list_bbox, list_size, amount = augment_random(image, "GaussianErase", list_coords, list_bbox, list_size)
            df.at[index, "Gaussian 2"] = amount
        else:
            df.at[index, "Gaussian 2"] = 0

        df.loc[index, 'Wrist_X':'Pinky_D_Y'] = list_coords
        df.loc[index, 'Bbox_X':'Bbox_H'] = list_bbox
        df.loc[index, 'Width':'Height'] = list_size

        # Image have gone through all augmentation steps, save it
        cv2.imwrite(SAVE_IMAGE_PATH + str(row["ID"]).zfill(12) + ".png", image)
    print("Augmenting: " + str(len(df)) + "/" + str(len(df)))
    print("Augmentation finished")
    return df


# Goes through the dataframe and limits the bbox values (x, y, w, h) to the image size (width, height)
def bbox_clip(df):
    print()
    for index, row in df.iterrows():
        if index % 100 == 0:
            print("Clipping: " + str(index) + "/" + str(len(df)) + "   ", end="\r")
        (x1, y1) = (df.at[index, 'Bbox_X'], df.at[index, 'Bbox_Y'])
        (x2, y2) = (df.at[index, 'Bbox_X'] + df.at[index, 'Bbox_W'], df.at[index, 'Bbox_Y'] + df.at[index, 'Bbox_H'])
        frame_width, frame_height = df.at[index, 'Width'], df.at[index, 'Height']
        x1 = df.at[index, 'Bbox_X'] = max(0, x1)
        y1 = df.at[index, 'Bbox_Y'] = max(0, y1)
        (x2, y2) = (min(frame_width, x2), min(frame_height, y2))
        df.at[index, 'Bbox_W'] = x2 - x1
        df.at[index, 'Bbox_H'] = y2 - y1
    print("Clipping: " + str(len(df)) + "/" + str(len(df)))
    return df


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[91m" + "augment_cf.py" + "\033[0m")
    # If there is no folder named SAVE_IMAGE_PATH, create one
    if not os.path.exists(SAVE_IMAGE_PATH):
        os.makedirs(SAVE_IMAGE_PATH)
    df = pd.read_csv(CSV_PATH, dtype={'ID': object}, low_memory=False)
    # first 1000 rows of the dataframe
    # df = df.head(1000)
    df = augment_cf(df)
    # df.to_csv(PATH + "pre_expurgation.csv", index=False)
    df = data_expurgation(df) # Remove rows with hands that are mostly outside the frame
    # df.to_csv(PATH + "post_expurgation.csv", index=False)
    df = bbox_clip(df) # Clip the bounding box values to the image size
    df.to_csv(SAVE_CSV_PATH, index=False)

    print("\nRL Flipped: " + str(len(df[df["RL"] == "left"])) + " - " + str(round((len(df[df["RL"] == "left"])/len(df)*100), 2)) + "%")
    print("Augmented: " + str(len(df[df["Augment"] == 1])) + " - " + str(round((len(df[df["Augment"] == 1])/len(df)*100), 2)) + "%")
    
    print("\nBlurred: " + str(len(df[df["Blur"] != 0])) + " - " + str(round((len(df[df["Blur"] != 0])/len(df)*100), 2)) + "%")
    print("Gaussion 1: " + str(len(df[df["Gaussian 1"] != 0])) + " - " + str(round((len(df[df["Gaussian 1"] != 0])/len(df)*100), 2)) + "%")
    print("Vertical flip: " + str(len(df[df["Flip"] == 1])) + " - " + str(round((len(df[df["Flip"] == 1])/len(df)*100), 2)) + "%")
    print("Geometric: " + str(len(df[df["Geometric"] == 1])) + " - " + str(round((len(df[df["Geometric"] == 1])/len(df)*100), 2)) + "%")
    print("Color: " + str(len(df[df["Color"] == 1])) + " - " + str(round((len(df[df["Color"] == 1])/len(df)*100), 2)) + "%")
    print("Gaussian 2: " + str(len(df[df["Gaussian 2"] != 0])) + " - " + str(round((len(df[df["Gaussian 2"] != 0])/len(df)*100), 2)) + "%\n")

    # Show the first 5 rows of the dataframe
    print(df.head())

    print("\nSaved CSV\n\nFULL DATA AUGMENTATION COMPLETE!\n")


if __name__ == "__main__":
    main()
