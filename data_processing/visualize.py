import cv2
import numpy as np
import pandas as pd
from enum import Enum

PATH = "D:/hi5_data/data/new_500k/"

OUTPUT_PATH = PATH + "test/"
CSV_PATH = PATH + "test.csv"
# OUTPUT_PATH = PATH + "output/"
# CSV_PATH = PATH + "output.csv"

df = pd.read_csv(CSV_PATH, dtype={'ID': object}, low_memory=False)
df = df.sample(frac=1).reset_index(drop=True)

# filter out rows to test certain augmentation types
# augmentations = ["Brightness", "ColorBalance", "Contrast", "DownUpscale", "Equalize", "Flip", "KernelFilter", "NoiseInject", "PatchShuffle", "GaussianErase", "ScaleSameRatio", "Solarize", "SolerizeAdd", "Stretch", "Translate"]
# df = df[df['Changed'] == 1]
# sort df by Translate value
# df = df.sort_values(by=['Changed'], ascending=False)

list_frames = df.loc[:, 'ID'].values.tolist()
list_coords = df.loc[:, 'Wrist_X':'Pinky_D_Y'].values.tolist()
list_bbox = df.loc[:, 'Bbox_X':'Bbox_H'].values.tolist()
list_conf = df.loc[:, 'Hand':'Height'].values.tolist()
list_conf_names = df.loc[:, 'Hand':'Height'].columns.values.tolist()


class Joint(Enum):
    Wrist = 0
    Thumb_A = 1
    Thumb_B = 2
    Thumb_C = 3
    Thumb_D = 4
    Index_A = 5
    Index_B = 6
    Index_C = 7
    Index_D = 8
    Middle_A = 9
    Middle_B = 10
    Middle_C = 11
    Middle_D = 12
    Ring_A = 13
    Ring_B = 14
    Ring_C = 15
    Ring_D = 16
    Pinky_A = 17
    Pinky_B = 18
    Pinky_C = 19
    Pinky_D = 20


# lines_guide = [[(0,1),(0,5),(0,9),(0,13),(0,17)],[(1,5),(5,9),(9,13)],[(1, 2), (2, 3), (3, 4)],[(5, 6), (6, 7), (7, 8)],[(9, 10), (10, 11), (11, 12)],[(13,14),(14,15),(15,16)],[(17,18),(18,19),(19,20)]]
lines_guide = [
    [(Joint.Wrist.value, Joint.Thumb_A.value), (Joint.Wrist.value, Joint.Index_A.value), (Joint.Wrist.value, Joint.Middle_A.value), (Joint.Wrist.value, Joint.Ring_A.value), (Joint.Wrist.value, Joint.Pinky_A.value)],
    [(Joint.Index_A.value, Joint.Middle_A.value), (Joint.Middle_A.value, Joint.Ring_A.value), (Joint.Ring_A.value, Joint.Pinky_A.value)],
    [(Joint.Thumb_A.value, Joint.Thumb_B.value), (Joint.Thumb_B.value, Joint.Thumb_C.value), (Joint.Thumb_C.value, Joint.Thumb_D.value)],
    [(Joint.Index_A.value, Joint.Index_B.value), (Joint.Index_B.value, Joint.Index_C.value), (Joint.Index_C.value, Joint.Index_D.value)],
    [(Joint.Middle_A.value, Joint.Middle_B.value), (Joint.Middle_B.value, Joint.Middle_C.value), (Joint.Middle_C.value, Joint.Middle_D.value)],
    [(Joint.Ring_A.value, Joint.Ring_B.value), (Joint.Ring_B.value, Joint.Ring_C.value), (Joint.Ring_C.value, Joint.Ring_D.value)],
    [(Joint.Pinky_A.value, Joint.Pinky_B.value), (Joint.Pinky_B.value, Joint.Pinky_C.value), (Joint.Pinky_C.value, Joint.Pinky_D.value)]
]


try:
    list_augment = df.loc[:, 'RL':'Translate'].values.tolist()
    list_augment_names = df.loc[:, 'RL':'Translate'].columns.values.tolist()
except:
    pass

for i in range(len(list_frames)):
    list_frames[i] = list_frames[i] + '.png'

FPS = 0.00001
# FPS = 1

def background_type(n, img):
    width_multiplier = 2
    height_multiplier = 1.75
    bg_width = width * width_multiplier + 400
    bg_height = int(max((height * height_multiplier), 576*1.75))
    if n == 1:
        return np.zeros((bg_height, bg_width, img.shape[2]), np.uint8)
    else:
        return_image = cv2.resize(img, (bg_width, bg_height))
        return_image = cv2.blur(return_image, (55, 55), cv2.BORDER_DEFAULT)
        return_image[:, :, 0:3] = return_image[:, :, 0:3] * 0.6
        return return_image

def get_theme_color():
    tc = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
    while tc[0] < 100 and tc[1] < 100 and tc[2] < 100:
        tc = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
    return tc

theme_color_1 = get_theme_color()
theme_color_2 = get_theme_color()
theme_color_3 = get_theme_color()

frame_num = 0
while frame_num < len(list_frames):
    filename = list_frames[frame_num]

    # margun multiplier
    mm = 0.375 # because height_multiplier = 1.75 and (1.75-1)/2 = 0.375

    # filename = OUTPUT_PATH + str("%012d" % (frame_num,)) + ".png"
    unity_img = cv2.imread(OUTPUT_PATH+filename, cv2.IMREAD_UNCHANGED)

    # print(unity_img)

    height = unity_img.shape[0]
    width = unity_img.shape[1]

    font_scale = 0.75
    full_image = background_type(1, unity_img)

    x_start = 2*width + 25
    y_start = 30
    y_offset = 30
    full_image[(int(mm * height) - 1):(int(mm* height) + height - 1),
    (int(mm * width) - 1):(int(mm * width) + width - 1)] = unity_img
    full_image = cv2.putText(full_image, "ID: " + str(list_frames[frame_num][:12]), (x_start, y_offset), cv2.FONT_HERSHEY_SIMPLEX, font_scale, theme_color_1, 2)
    y_offset += y_start
    for i in range(len(list_conf[frame_num])):
        full_image = cv2.putText(full_image, list_conf_names[i] + ": " + str(list_conf[frame_num][i]), (x_start, y_offset), cv2.FONT_HERSHEY_SIMPLEX, font_scale, theme_color_1, 2)
        y_offset += y_start
    try:
        for i in range(len(list_augment[frame_num])):
            full_image = cv2.putText(full_image, list_augment_names[i] + ": " + str(list_augment[frame_num][i]), (x_start, y_offset), cv2.FONT_HERSHEY_SIMPLEX, font_scale, theme_color_2, 2)
            y_offset += y_start
    except:
        pass

    # draw a vertical line at 2*width from top to bottom
    full_image = cv2.line(full_image, (2*width, 0), (2*width, full_image.shape[0]), theme_color_3, 2)
    # draw a rectange around the image (widtth/2, height/2) to (width/2 + width, height/2 + height)
    full_image = cv2.rectangle(full_image, (int(mm* width), int(mm * height)), (int(mm* width) + width, int(mm* height) + height), theme_color_3, 2)

    a = []
    b = []

    # get even number elements from the list list_coords and convert it to int
    a = [int((float(list_coords[frame_num][i]) + (mm * width))) for i in range(0, len(list_coords[frame_num]), 2)]
    # get odd number elements from the list list_coords and convert it to int
    b = [int((float(list_coords[frame_num][i]) + (mm * height))) for i in range(1, len(list_coords[frame_num]), 2)]

    outs = list(zip(a, b))

    for out in outs:
        cv2.circle(full_image, out, radius=3, color=(0, 255, 0), thickness=-1)
    
    # draw rectangles based on bbox
    current_bbox = list_bbox[frame_num]
    bbox_x = int(current_bbox[0] + (mm * width))
    bbox_y = int(current_bbox[1] + (mm * height))
    bbox_w = int(current_bbox[2])
    bbox_h = int(current_bbox[3])
    cv2.rectangle(full_image, (bbox_x, bbox_y), (bbox_x + bbox_w, bbox_y + bbox_h), (0, 0, 255), 2)
    # draw filled circle
    cv2.circle(full_image, (bbox_x, bbox_y), radius=3, color=(0, 0, 255), thickness=-1)

    # convert list_bbox to int
    list_bbox[frame_num] = [int(i) for i in list_bbox[frame_num]]
    # add text for all elements of list_bbox converted to int and in one line
    full_image = cv2.putText(full_image, "Bbox: " + str(list_bbox[frame_num]), (25, y_start), cv2.FONT_HERSHEY_SIMPLEX, font_scale, theme_color_3, 2)

    color_i = 0
    colors = [(0, 0, 255), (0, 0, 0), (50, 50, 50), (100, 100, 100), (150, 150, 150), (200, 200, 200), (250, 250, 250)]
    for finger in lines_guide:
        for connection in finger:
            cv2.line(full_image, outs[connection[0]], outs[connection[1]], colors[color_i],1)

        color_i += 1
        color_i = color_i%len(colors)

    # if the height of full_image is higher than 1000, resize it to 1080 (keep the aspect ratio), and add a text at the top left that says "image resized"
    if full_image.shape[0] > 1152:
        full_image = cv2.resize(full_image, (int(full_image.shape[1] * 1152 / full_image.shape[0]), 1152))
        full_image = cv2.putText(full_image, "Window Resized", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, theme_color_3, 2)
    if full_image.shape[1] > 1920:
        full_image = cv2.resize(full_image, (1920, int(full_image.shape[0] * 1920 / full_image.shape[1])))
        full_image = cv2.putText(full_image, "Window Resized", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, theme_color_3, 2)
    if height < 576:
        full_image = cv2.putText(full_image, "Window Resized", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, theme_color_3, 2)

    cv2.imshow("Synthetic Hand Visualizer", full_image)
    # cv2.moveWindow("Synthetic Hand Visualizer", 0, 0)
    # cv2.setWindowProperty("Synthetic Hand Visualizer", cv2.WND_PROP_TOPMOST, 1)

    k = cv2.waitKeyEx(int(1000/FPS))
    if k == ord('q') or k == ord('Q') or k == 27:
        print("\n")
        break
    elif k == ord('a') or k == ord('A') or k == 2424832:
        frame_num -= 2
        if frame_num < 0:
            frame_num = 0
            continue
    elif k == ord('d') or k == ord('D') or k == 2555904:
        print(f"\rframe_num: {frame_num+1}", end="")
        if frame_num >= len(list_coords) - 1:
            break
    else:
        print(f"\rframe_num: {frame_num+1}", end="")
        if frame_num >= len(list_coords) - 1:
            break

    frame_num += 1
