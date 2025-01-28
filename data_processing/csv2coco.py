from __future__ import annotations
import pandas as pd
import json
import os
from datetime import datetime
import numpy as np
import sys
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def write_main(dataframe, json_path):
    # image_id is a list of all image id's
    image_id = dataframe['ID']
    annotations, bbox_list = get_annotation(image_id)
    print("\n")
    data = {
        # "info": get_info(), 
        # "licenses": get_license(), 
        "images": get_image(image_id),
        "annotations": annotations,
        "categories": get_categories()
    } 

    # convert all int64 to int, this affects only width and height
    for key in data:
        if type(data[key]) == list:
            for i in range(len(data[key])):
                for key2 in data[key][i]:
                    if type(data[key][i][key2]) == np.int64:
                        # print(key, key2, data[key][i][key2])
                        data[key][i][key2] = int(data[key][i][key2])

    # with open(bbox_path, 'w') as f:
    #     json.dump(bbox_list, f)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)


def get_info():
    info = {
        "description": "Hi-5 Hand Tracking Dataset",
        "url": "https://roc-hci.com/",
        "version": "1.0",
        "year": "2022",
        "contributor": "ROC-HCI Lab",
        "date_created": "2022/07/27"
    }
    return info


def get_license():
    license_list = []
    license = {
        "url": "https://roc-hci.com/",
        "id": 1,
        "name": "ROC-HCI Lab"
    }
    license_list.append(license)
    return license_list


def get_image(image_id):
    image_list = []
    for id in image_id:
        row = id_dict[int(id)]
        filename = '0'*(12-len(id)) + id + '.png'
        img_num = (id_dict[int(id)]+1)
        if (img_num%1000 == 0):
            percetage = int(img_num/len(df)*100)
            sys.stdout.write(f"\rimage {img_num} in {len(df)}\t\t{progress_bar(percetage)}")
            sys.stdout.flush()
        path = IMAGE_PATH+filename
        image = {
            "license": int(id),
            "file_name": filename,
            # "coco_url": filename,
            "height": df.loc[row]['Height'],
            "width": df.loc[row]['Width'],
            "date_captured": str(datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')),
            # "flickr_url": filename,
            "id": int(id)
        }
        image_list.append(image)
    return image_list

def get_annotation(image_id):
    # input: image_id -> list of all image id's
    annotation_list = []
    bbox_list = []
    sys.stdout.write("\r" + " " * 100)
    sys.stdout.flush()
    for id in image_id:
        # id -> each image id
        get_keypoints(int(id))
        row = id_dict[int(id)]
        if ((row+1)%100 == 0):
            percetage = int(id_dict[int(id)]/len(df)*100)
            message = f"\rannotation {row+1} in {len(df)}"
            space = " " * (30 - len(message))
            sys.stdout.write(f"{message}{space}{progress_bar(percetage)}")
        sys.stdout.flush()
        annotation = {
            "segmentation": [],
            "keypoints": last_keypoints,
            "num_keypoints": last_vis,
            "area": 0,
            "iscrowd": 0,
            "image_id": int(id),
            "bbox": get_bbox(row),
            "category_id": get_category_id(row),
            "id": int(id)
        }
        bbox_dict = {
            "image_id": int(id),
            "category_id": 1,
            "bbox": get_bbox(row),
            "score": 1
        }
        bbox_list.append(bbox_dict)
        annotation_list.append(annotation)

    message = f"\rannotation {len(df)} in {len(df)}"
    space = " " * (30 - len(message))
    sys.stdout.write(f"{message}{space}{progress_bar(100)}")
    
    return annotation_list, bbox_list


def get_categories():
    category = {
        "supercategory": "hand",
        "id": 1,
        "name": "right_hand",
        # "keypoints": ["wrist", "thumb_a", "thumb_b", "thumb_c", "thumb_d", "index_a", "index_b", "index_c", "index_d", "middle_a", "middle_b", "middle_c", "middle_d", "ring_a", "ring_b", "ring_c", "ring_d", "pinky_a", "pinky_b", "pinky_c", "pinky_d"],
        # "skeleton": [[1,2],[1,6],[1,10],[1,14],[1,18],[2,6],[6,10],[10,14],[2,3],[3,4],[4,5],[6,7],[7,8],[8,9],[10,11],[11,12],[12,13],[14,15],[15,16],[16,17],[18,19],[19,20],[20,21]],
        "keypoints": [
                "wrist",
                "thumb1",
                "thumb2",
                "thumb3",
                "thumb4",
                "forefinger1",
                "forefinger2",
                "forefinger3",
                "forefinger4",
                "middle_finger1",
                "middle_finger2",
                "middle_finger3",
                "middle_finger4",
                "ring_finger1",
                "ring_finger2",
                "ring_finger3",
                "ring_finger4",
                "pinky_finger1",
                "pinky_finger2",
                "pinky_finger3",
                "pinky_finger4"
            ],
        "skeleton": [ [ 1, 2 ], [ 2, 3 ], [ 3, 4 ], [ 4, 5 ], [ 1, 6 ], [ 6, 7 ], [ 7, 8 ], [ 8, 9 ], [ 1, 10 ], [ 10, 11 ], [ 11, 12 ], [ 12, 13 ], [ 1, 14 ], [ 14, 15 ], [ 15, 16 ], [ 16, 17 ], [ 1, 18 ], [ 18, 19 ], [ 19, 20 ], [ 20, 21 ] ]
    }

    category_2 = category.copy()
    category_2['name'] = 'left_hand'
    category_2['id'] = 2
    category_list = [category, category_2]
    return category_list


def get_keypoints(row):
    # row is the iteration number
    global last_vis
    global last_keypoints
    global v_total
    v_total = 0
    # row becomes the row number
    row = id_dict[row]

    keypoints = []
    image_coords = df.loc[:, 'Wrist_X':'Pinky_D_Y']

    add_x = 0

    for i in range(0, len(image_coords.columns)):
        # print("====> i:", i, "row:", row, "image_coords:", len(image_coords))
        if i % 2 == 0:
            add_x = image_coords.loc[row][i]
            # round to nerest in
            add_x = round(add_x)
            keypoints.append(add_x)
        else:
            add_y = image_coords.loc[row][i]
            add_y = round(add_y)
            keypoints.append(add_y)
            keypoints.append(get_v(add_x,add_y,df.loc[row]['Width'],df.loc[row]['Height']))

    last_vis = v_total

    last_keypoints = keypoints


def get_v(x,y,max_x,max_y):
    # 0 labeled but not visible, 1 labled but not visible, 2 is labeled and visible
    # v_total is the total number of visible keypoints
    global v_total
    if x < 0 or y < 0 or x > max_x or y > max_y:
        last_vis = 1 # not visible
    else:
        last_vis = 2 # visible
        v_total += 1
    return last_vis


def get_h(row):
    # row is the iteration number
    # row becomes the row number
    row = id_dict[row]

    h = df.loc[row]['Height']
    return h


def get_bbox(row):
    # xs = last_keypoints[::3]
    # ys = last_keypoints[1::3]

    # bbox_scale = 0.3

    # # print(np.array(xs))

    # left_x, left_y = np.array(xs).min(), np.array(ys).min()
    # dist_x, dist_y = np.array(xs).max() - left_x, np.array(ys).max() - left_y
    # left_x, left_y = left_x - dist_x * bbox_scale, left_y - dist_y * bbox_scale
    # dist_x, dist_y = dist_x * (1 + 2 * bbox_scale), dist_y * (1 + 2 * bbox_scale)
    # bbox = [left_x, left_y, dist_x, dist_y]
    

    # round to 2 decimal places
    bbox = [round(df.loc[row]['Bbox_X'],2), round(df.loc[row]['Bbox_Y'],2), round(df.loc[row]['Bbox_W'],2), round(df.loc[row]['Bbox_H'],2)]

    # bbox = [df.loc[row]['Bbox_X'], df.loc[row]['Bbox_Y'], df.loc[row]['Bbox_W'], df.loc[row]['Bbox_H']]

    return bbox


def get_category_id(row):
    if df.loc[row]['RL'] == 'right':
        category_id = 1
    else:
        category_id = 2

    return category_id


def progress_bar(x):
    space = " " * 20
    x = math.ceil(x/2)
    progresss = f"[{bcolors.OKGREEN}"
    for i in range(x):
        progresss += "▮"
    progresss += bcolors.ENDC
    for i in range(50-x):
        progresss += " "
    progresss += f" ] {x*2}%{space}"

    return progresss


def csv2coco(dataframe, json_path):
    # os.system("clear")
    title = f"Converting {type_name}.csv to coco format..."
    print(title)
    print("=" * len(title))
    write_main(dataframe, json_path)


type2name = {
    # "valid": "valid",
    "train": "train",
    "test": "test"
}

print("\033[94m" + "\ncsv2coco.py" + "\033[0m")
for name in type2name:
    type_name = name
    csv_name = type2name[type_name]
    json_name = type2name[type_name]

    PATH = "D:/hi5_data/data/new_500k/"

    IMAGE_PATH = f"{PATH}{type2name[type_name]}/"
    CSV_PATH = f"{PATH}{csv_name}.csv"
    JSON_PATH = f"{PATH}person_keypoints_{json_name}.json"
    bbox_path = f"{PATH}bbox_{json_name}.json"

    last_vis = 0
    last_keypoints = []
    v_total = 0
    id_dict = {}

    df = pd.read_csv(CSV_PATH, dtype={'ID': object})

    im_id_list = df['ID'].tolist()
    # each value is a string rep of the id with leading zeros

    # i is the counter, id is the value
    for (i, id) in enumerate(im_id_list):
        id_dict[int(id)] = i
    # random index becomes equal to the counter\

    csv2coco(df, JSON_PATH)
    