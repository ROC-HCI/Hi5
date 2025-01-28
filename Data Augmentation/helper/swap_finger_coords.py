import json

PATH = "C:/Users/HCI-Beast1/Desktop/hi5_data/data/"
type = "train"
JSON_PATH = PATH + "person_keypoints_"+type+".json"
OUTPUT_JSON_PATH = PATH + "new_person_keypoints_"+type+".json"

json_data = json.load(open(JSON_PATH))

for index, image in enumerate(json_data["annotations"]):
    keypoints = image["keypoints"]
    new_keypoints = []
    # append 0-2
    # append 51-62
    # append 3-50
    for i in keypoints[0:3]:
        new_keypoints.append(i)
    for i in keypoints[51:63]:
        new_keypoints.append(i)
    for i in keypoints[3:51]:
        new_keypoints.append(i)
    json_data["annotations"][index]["keypoints"] = new_keypoints

with open(OUTPUT_JSON_PATH, 'w') as outfile:
    json.dump(json_data, outfile, indent=4)
