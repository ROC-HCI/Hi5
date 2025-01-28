import cv2
import os
import json

folder_name = "F:\\Hand_Dataset\\final_split_5_19\\"

annotations = f"{folder_name}annotations\\"

test_annotations = open(f"{annotations}hi5_500k_test.json")
train_annotations = open(f"{annotations}hi5_500k_train.json")
test_annotations = json.load(test_annotations)
train_annotations = json.load(train_annotations)

new_test_annotations = test_annotations
new_train_annotations = train_annotations

test = f"{folder_name}test\\"
train = f"{folder_name}train\\"

test_resize = f"{folder_name}test_resize\\"
train_resize = f"{folder_name}train_resize\\"

if not os.path.exists(test_resize):
    os.makedirs(test_resize)
if not os.path.exists(train_resize):
    os.makedirs(train_resize)


def pad_image_to_square(img, x_coord, y_coord, bbox):
    height, width = img.shape[:2]

    if height == width:
        return img, x_coord, y_coord, bbox
    elif height > width:
        difference = height - width
        left_pad = difference // 2
        right_pad = difference - left_pad
        result = cv2.copyMakeBorder(img, 0, 0, left_pad, right_pad, cv2.BORDER_CONSTANT, value = [0, 0, 0])
        # Loop through bounding box and every other coordinate
        x_coord = [x + left_pad for x in x_coord]
        bbox[0] += left_pad

    else:
        difference = width - height
        top_pad = difference // 2
        bottom_pad = difference - top_pad
        result = cv2.copyMakeBorder(img, top_pad, bottom_pad, 0, 0, cv2.BORDER_CONSTANT, value = [0, 0, 0])
        # Loop through bounding box and every other coordinate
        y_coord = [y + top_pad for y in y_coord]
        bbox[1] += top_pad

    return result, x_coord, y_coord, bbox

def resize_256(image, x_coord, y_coord, bbox):
    height, width = image.shape[:2]
    if height != width:
      print("Input not sqaure")
      return
    resized_image = cv2.resize(image, (256, 256))
    scale_factor = 256/height
    # Loop through bounding box and every other coordinate
    x_coord = [x * scale_factor for x in x_coord]
    y_coord = [y * scale_factor for y in y_coord]
    bbox = [b * scale_factor for b in bbox]
    ## Cast them to integer if necessary

    return resized_image, x_coord, y_coord, bbox

for i, annotations in enumerate(train_annotations["annotations"]):
    if i % 1000 == 0:
        print(f"train: {i}")

    filename = train_resize + train_annotations["images"][i]["file_name"]
    if os.path.isfile(filename):
        continue

    # print(f"filename: {filename}")
    
    keypoints = annotations['keypoints']
    x_coord = keypoints[0::3]
    y_coord = keypoints[1::3]
    bbox = annotations['bbox']

    # print(f"bbox: {bbox}\nkeypoints: {keypoints}")

    n = cv2.imread(train + train_annotations["images"][i]["file_name"])
    n, x_coord, y_coord, bbox = pad_image_to_square(n, x_coord, y_coord, bbox)
    n, x_coord, y_coord, bbox = resize_256(n, x_coord, y_coord, bbox)

    x_coord = [round(x, 2) for x in x_coord]
    y_coord = [round(y, 2) for y in y_coord]
    bbox = [round(b, 2) for b in bbox]

    keypoints = []
    for x, y in zip(x_coord, y_coord):
        keypoints.append(x)
        keypoints.append(y)
        keypoints.append(2)

    new_train_annotations['annotations'][i]['keypoints'] = keypoints
    new_train_annotations['annotations'][i]['bbox'] = bbox
    new_train_annotations['images'][i]['width'] = 256
    new_train_annotations['images'][i]['height'] = 256

    # print(f"bbox: {bbox}\nkeypoints: {keypoints}\n")

    cv2.imwrite(filename, n)

with open(f"{folder_name}hi5_500k_train_resize.json", "w") as outfile:
    json.dump(new_train_annotations, outfile, indent=4)
    print("Done writing to hi5_500k_train_resize.json")
