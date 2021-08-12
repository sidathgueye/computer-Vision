import darknet
import cv2
from sys import argv
from threading import Thread
import time
import test_upload


def saveVideo(array_image, label_class):
    filename = '/data/www/ia/_www/movies/' + argv[1] + '_' + str(time.time()) + '.avi'
    if len(array_image) > 0:
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), 8,
                              (darknet.network_width(network), darknet.network_height(network)))
        for i in range(len(array_image)):
            out.write(array_image[i])
        test_upload.send(filename, argv[1], label_class)
        out.release()
        print("video uploaded")


def getLabel(detection):
    for label, confidence, bbox in detection:
        return label
    return False


# Sort Dictionary in descending order
def sortDict(dict_class):
    return {k: v for k, v in sorted(dict_class.items(), key=lambda item: item[1], reverse=True)}


# ------------ load Yolov4 network ------------
network, class_names, class_colors = darknet.load_network(
    config_file='/home/gael/darknet/cfg/yolo-obj.cfg',
    data_file='/home/gael/darknet/build/darknet/x64/data/obj.data',
    weights='/home/gael/darknet/backup/yolo-obj_best.weights')

# ------------ Connect to stream ------------
url = "rtmp://91.121.83.50:1935/live/" + argv[1]
print("Connect to: " + url)
cap = cv2.VideoCapture(url)

count = 0
img_array = []
count_detections = 0
first_detection = True
time_last_video = 0
dict_classes = {}

while True:
    ret, frame = cap.read()

    if not ret:
        break
    else:
        count = (count + 1) % 3
    if count == 0:
        width = darknet.network_width(network)
        height = darknet.network_height(network)
        darknet_image = darknet.make_image(width, height, 3)

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (width, height),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=0.5)
        if len(detections) > 0:
            count_detections += 1
            # add the label in the dict if it's not already there and increase by 1 the value dict = {label: counter}
            label = getLabel(detections)
            if label not in dict_classes.keys():
                dict_classes[label] = 1
            else:
                dict_classes[label] += 1
        darknet.free_image(darknet_image)
        image = darknet.draw_boxes(detections, image_resized, class_colors)
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_array.append(new_image)
        # cv2.imshow('inference', new_image)
        if count_detections >= 15 and (time.time() - time_last_video) > 120:
            # sort the dictionary and return the key of the first element
            dict_classes = sortDict(dict_classes)
            class_name = list(dict_classes.keys())[0]
            print(class_name)
            img_array_copy = img_array
            saveVideo(img_array, class_name)
            img_array.clear()
            count_detections = 0
            time_last_video = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        img_array.append(frame)

cap.release()
cv2.destroyAllWindows()
