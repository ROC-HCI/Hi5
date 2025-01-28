# Run sample_train_test in order to sample train, test, and validation data from the augmented dataset
# Run copy_images in order to copy the images from the augmented dataset to the train, test, and validation folders

import pandas as pd
import os
import shutil

FOLDER_PATH = "D:/hi5_data/data/new_500k/"
TEST_PATH = FOLDER_PATH+"test/"
TRAIN_PATH = FOLDER_PATH+"train/"
# VALID_PATH = FOLDER_PATH+"valid/"
OUTPUT_PATH = FOLDER_PATH+"output_augmented/"
CSV_FILE = FOLDER_PATH+"output_augmented.csv"

def sample_train_test():
    df = pd.read_csv(CSV_FILE, dtype={'ID': object})
    # print length
    print("Length of df:", len(df))
    df = df.dropna() #drop rows with NaN
    # before_drop = len(df)
    df = df.drop_duplicates()
    # after_drop = len(df)

    # print("Dropping duplicate and NaN rows...")
    # print(f"Before drop: {before_drop}, After drop: {after_drop}, Drop rate: {(before_drop-after_drop)/before_drop*100}%")

    #sample from df to train and test
    # df = df.sample(frac=0.1, random_state=42)

    ## pick the rows with Animation 10, 23, 2, 14, 5, 4 as test
    # df_test = df[df['Animation'].isin([10, 23, 2, 14, 5, 4])]
    # df_train_valid = df.drop(df_test.index)
    # df_train = df_train_valid.sample(frac=0.8, random_state=42)
    # df_valid = df_train_valid.drop(df_train.index)
    # df_test = df.drop(df_train_valid.index)

    df_test = df.sample(frac=0.10, random_state=42)
    df_train = df.drop(df_test.index)

    #write train and test to csv
    df_train.to_csv(FOLDER_PATH+"train.csv", index=False)
    df_test.to_csv(FOLDER_PATH+"test.csv", index=False)
    # df_valid.to_csv(FOLDER_PATH+"valid.csv", index=False)


def copy_images():
    # make a dictionary of test, train, valid folders to csv file names
    # folders = {TRAIN_PATH: "train", TEST_PATH: "test", VALID_PATH: "valid"}
    folders = {TRAIN_PATH: "train", TEST_PATH: "test"}

    # iterate through the dictionary
    for path, file in folders.items():
        # create train, test, and valid folders
        if not os.path.exists(path):
            os.makedirs(path)

        # ttv: train, test, valid
        df_ttv = pd.read_csv(FOLDER_PATH+file+".csv", dtype={'ID': object})
        counter = 0
        space = " "*10
        for id in df_ttv['ID']:
            if len(df_ttv) > 1000:
                update_freq = 1000
            else:
                update_freq = 10
            if (counter%update_freq == 0):
                end = "\r" if counter != len(df_ttv) - 1 else "\n"
                print(f"{file} image {counter} in {len(df_ttv)}: {int((counter+1)/len(df_ttv)*100)}%{space}", end=end)
            counter += 1
            if os.path.exists(OUTPUT_PATH+id+".png"):
                shutil.copy(OUTPUT_PATH+id+".png", path+id+".png")
            else:
                print(f"{OUTPUT_PATH+id}.png does not exist")

        print(f"{file} image {len(df_ttv)} in {len(df_ttv)}: 100%{space}")


print("\033[92m" + "sample_train_test.py" + "\033[0m")
print("sample_train_test")
sample_train_test()
print("\ncopy_images")
copy_images()
