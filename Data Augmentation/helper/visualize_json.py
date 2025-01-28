import cv2
import json
import numpy as np
import os

# PATH = "C:/Users/HCI-Beast1/Desktop/hi5_data/data/"
# PATH = "D:/hi5_data/data/"
PATH = "F:/Hand_Dataset/final_split_5_19/"

group = "train_resize"

OUTPUT_PATH = PATH + group+ "/"
# JSON_PATH = PATH + "person_keypoints_"+group+".json"
JSON_PATH = PATH + "annotations/hi5_500k_"+group+".json"

FPS = 0.00001

json_data = json.load(open(JSON_PATH))
# id_list = json_data['image_id']

# print(json_data["annotations"][2]["bbox"])

for index, image in enumerate(json_data["annotations"]):
    img_path = OUTPUT_PATH + json_data["images"][index]["file_name"]
    if not os.path.exists(img_path):
        continue
    print(img_path)
    width = json_data["images"][index]["width"]
    height = json_data["images"][index]["height"]
    bbox = image["bbox"]

    # Draw the image using cv2 and draw the bbox on it
    # First create an empty image that is twice the size of the original image
    # Then draw the image on the empty image and center it
    frame = np.zeros((height*2, width*2, 3), np.uint8)
    img = cv2.imread(img_path)
    frame[height//2:height//2+height, width//2:width//2+width] = img

    keypoints = image["keypoints"]
    for i in range(0, len(keypoints), 3):
        cv2.circle(frame, (int(keypoints[i]+width//2), int(keypoints[i+1]+height//2)), 1, (0, 0, 255), 2)

    # Draw a rectangle around img
    cv2.rectangle(frame, (width//2, height//2), (width//2+width, height//2+height), (255, 255, 255), 2)
    # Draw the bbox
    cv2.rectangle(frame, (int(bbox[0]+width//2), int(bbox[1]+height//2)), (int(bbox[0]+width//2+bbox[2]), int(bbox[1]+height//2+bbox[3])), (0, 255, 0), 2)

    # Show the image
    cv2.imshow("frame", frame)

    k = cv2.waitKeyEx(int(1000/FPS))
    if k == ord('q') or k == ord('Q') or k == 27:
        print("\n")
        break
