import json

# Goes through the dataframe and limits the bbox values (x, y, w, h) to the image size (width, height)
def bbox_clip_csv(df):
    for index, row in df.iterrows():
        if index % 100 == 0:
            print("Clipping: " + str(index) + "/" + str(len(df)), end="\r")
        df.at[index, 'Bbox_X'] = max(0, df.at[index, 'Bbox_X'])
        df.at[index, 'Bbox_Y'] = max(0, df.at[index, 'Bbox_Y'])
        df.at[index, 'Bbox_W'] = min(df.at[index, 'Width'] - df.at[index, 'Bbox_X'], df.at[index, 'Bbox_W'])
        df.at[index, 'Bbox_H'] = min(df.at[index, 'Height'] - df.at[index, 'Bbox_Y'], df.at[index, 'Bbox_H'])
    print("Clipping: " + str(len(df)) + "/" + str(len(df)))
    return df


def bbox_clip_bbox_json(bbox_json_data, keypoint_json_data):
    for index, image in enumerate(bbox_json_data):
        if index % 100 == 0:
            print("Clipping: " + str(index) + "/" + str(len(bbox_json_data)), end="\r")
        bbox = image["bbox"].copy()
        if bbox[0] < 0:
            bbox[2] += bbox[0]
            bbox[0] = 0
        if bbox[1] < 0:
            bbox[3] += bbox[1]
            bbox[1] = 0
        bbox[2] = min(keypoint_json_data["images"][index]["width"] - bbox[0], bbox[2])
        bbox[3] = min(keypoint_json_data["images"][index]["height"] - bbox[1], bbox[3])
        # print(f"{image['image_id']}: {image['bbox'][0]+image['bbox'][2]} > {keypoint_json_data['images'][index]['width']} or {image['bbox'][1]+image['bbox'][3]} > {keypoint_json_data['images'][index]['height']}")
        if image['bbox'] != bbox:
            print(f"Old: {image['bbox']}, New: {bbox} (width: {keypoint_json_data['images'][index]['width']}, height: {keypoint_json_data['images'][index]['height']}))")
        bbox_json_data[index]["bbox"] = bbox
        keypoint_json_data["annotations"][index]["bbox"] = bbox
    print("Clipping: " + str(len(bbox_json_data)) + "/" + str(len(bbox_json_data)))
    return bbox_json_data, keypoint_json_data


PATH = "C:/Users/HCI-Beast1/Desktop/hi5_data/data/"

group = "train"

# read json file
bbox_json_file = open(PATH+'bbox_'+group+'.json')
bbox_json_str = bbox_json_file.read()
bbox_json_data = json.loads(bbox_json_str)

keypoint_json_file = open(PATH+'person_keypoints_'+group+'.json')
keypoint_json_str = keypoint_json_file.read()
keypoint_json_data = json.loads(keypoint_json_str)

# clip bbox
bbox_json_data, keypoint_json_data = bbox_clip_bbox_json(bbox_json_data, keypoint_json_data)

# write json file
with open('new_bbox_'+group+'.json', 'w') as outfile:
    json.dump(bbox_json_data, outfile)

with open('new_person_keypoints_'+group+'.json', 'w') as outfile:
    json.dump(keypoint_json_data, outfile)
