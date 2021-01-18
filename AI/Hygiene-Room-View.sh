

#Load video with ssd mobilenet
#python3 Hygiene_Tracking_Room_Subscriber.py --file --filename ./video/Case6_QEH_Sze.mp4 --model ssd_mobilenet_v1_coco  --num-classes 1 --confidence 0.4 

#Load video with faster rcnn
#python3 Hygiene_Tracking_Room_Subscriber.py --file --filename ./video/003.mp4 --model faster_rcnn_inception_v2_coco  --num-classes 1 --confidence 0.4 


#RTSP VStar Camera with mobilenet
#python3 Hygiene_Tracking_Room_Subscriber.py --rtsp --uri rtsp://admin:51689453@192.168.0.112:554/udp/av0_0 --model ssd_mobilenet_v1_coco  --num-classes 1 --confidence 0.4

#RTSP VStar Camera with faster rcnn
#python3 Hygiene_Tracking_Room_Subscriber.py --rtsp --uri rtsp://admin:51689453@192.168.0.112:554/udp/av0_0 --model faster_rcnn_inception_v2_coco  --num-classes 1 --confidence 0.4

#RTSP Hikvision Camera with faster rcnn
python3 /home/nvidia/vincent/workspace/handhygiene_QE_ws/Hygiene_Tracking_Room_Subscriber.py --rtsp --uri rtsp://158.132.152.121:554/live4.sdp --model faster_rcnn_inception_v2_coco  --num-classes 1 --confidence 0.4 





