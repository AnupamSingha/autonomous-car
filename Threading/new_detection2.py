import cv2

# Load class names
classNames = []
classFile = "coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

# Load model configuration and weights
configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(150, 150)  # Increased input size for better small object detection
net.setInputScale(1.0 / 127.5)  # Normalize input for better detection
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres=0.3, nms=0.2, draw=True, objects=[]):
    img = cv2.flip(img, 0)  # Flip vertically for correct orientation

    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)

    if len(objects) == 0:
        objects = classNames

    objectInfo = []
    if len(classIds) != 0:
        detections = sorted(zip(classIds.flatten(), confs.flatten(), bbox), key=lambda x: x[1], reverse=True)
        detections = detections[:3]  # Detect up to 4 objects

        for classId, confidence, box in detections:
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className])
                if draw:
                    # Draw larger bounding boxes for small objects
                    x, y, w, h = box
                    cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=3)
                    cv2.putText(img, className.upper(), (x + 5, y + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  # Slightly larger font
                    cv2.putText(img, f"{round(confidence * 100, 1)}%", (x + 5, y + 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return img, objectInfo

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Set frame width
    cap.set(4, 480)  # Set frame height
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce camera buffer
    cap.set(cv2.CAP_PROP_FPS, 30)  # Try to stabilize FPS

    frame_skip = 3  # Reduce frame skip to improve small object detection
    frame_count = 0

    while True:
        success, img = cap.read()
        if not success:
            break

        frame_count += 1
        if frame_count % frame_skip == 0:  # Process every 3rd frame
            result, objectInfo = getObjects(img, thres=0.3, nms=0.2)  # Improved small object detection
            cv2.imshow("Output", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
