#!/bin/bash

./darknet detector train ~/darknet/build/darknet/x64/data/obj.data /home/gael/darknet/cfg/yolo-obj.cfg /home/gael/darknet/build/darknet/x64/yolov4.conv.137 -clear -map > results_train/result_train.txt
sleep 10

for i in {1..10}
do
    ./darknet detector train ~/darknet/build/darknet/x64/data/obj.data /home/gael/darknet/cfg/yolo-obj"$i".cfg /home/gael/darknet/build/darknet/x64/yolov4.conv.137 -clear -map > results_train/result_train"$i".txt
    sleep 10
done
