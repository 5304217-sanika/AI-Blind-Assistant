from ultralytics import YOLO
import cv2
import win32com.client
import time

# Voice
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# General object detection model
object_model = YOLO("yolov8s.pt")

# Currency detection model
currency_model = YOLO(
    r"C:\Users\DELL\Downloads\Indian Currency Detection.v1i.yolov8\runs\detect\train\weights\best.pt"
)
# Camera
cap = cv2.VideoCapture(0)

spoken_objects = {}
FORGET_TIME = 5

while True:

    ret, frame = cap.read()

    if not ret:
        break

    current_time = time.time()
    frame_width = frame.shape[1]

    visible_objects = set()

    obstacle_ahead = False
    obstacle_left = False
    obstacle_right = False

    # ==========================
    # OBJECT DETECTION
    # ==========================

    object_results = object_model(frame, verbose=False)

    boxes = object_results[0].boxes
    names = object_results[0].names

    for box in boxes:

        confidence = float(box.conf[0])

        if confidence < 0.90:
            continue

        cls = int(box.cls[0])
        object_name = names[cls]

        visible_objects.add(object_name)

        x1, y1, x2, y2 = box.xyxy[0]

        center_x = (x1 + x2) / 2
        object_width = x2 - x1

        if center_x < frame_width / 3:
            position = "on left"
            obstacle_left = True

        elif center_x < 2 * frame_width / 3:
            position = "ahead"
            obstacle_ahead = True

        else:
            position = "on right"
            obstacle_right = True

        if object_width > 200:

            if position == "ahead":
                message = f"Warning! {object_name} very close. Move left."

            elif position == "on left":
                message = f"Warning! {object_name} very close on left. Move right."

            else:
                message = f"Warning! {object_name} very close on right. Move left."

        else:
            message = f"{object_name} {position}"

        if object_name not in spoken_objects:

            print(message)
            speaker.Speak(message)

            spoken_objects[object_name] = current_time

    # ==========================
    # CURRENCY DETECTION
    # ==========================

    currency_results = currency_model(frame, verbose=False)
    print(currency_results[0].boxes)
    currency_boxes = currency_results[0].boxes
    currency_names = currency_results[0].names

    for box in currency_boxes:

        confidence = float(box.conf[0])

        if confidence < 0.60:
            continue

        cls = int(box.cls[0])
        note_name = currency_names[cls]

        visible_objects.add(note_name)

        if note_name not in spoken_objects:

            if note_name == "50_rupees":
                message = "50 rupees note detected"

            elif note_name == "100_rupees":
                message = "100 rupees note detected"

            elif note_name == "200_rupees":
                message = "200 rupees note detected"

            elif note_name == "500_rupees":
                message = "500 rupees note detected"

            else:
                message = "Currency note detected"

            print(message)
            speaker.Speak(message)

            spoken_objects[note_name] = current_time

    # ==========================
    # NAVIGATION
    # ==========================

    if obstacle_ahead:
        print("Obstacle ahead")

    elif not obstacle_ahead and not obstacle_left and not obstacle_right:
        print("Path clear")

    # ==========================
    # FORGET OLD OBJECTS
    # ==========================

    remove_list = []

    for obj, last_time in spoken_objects.items():

        if current_time - last_time > FORGET_TIME:
            remove_list.append(obj)

    for obj in remove_list:
        del spoken_objects[obj]

    # Display camera
    annotated_frame = object_results[0].plot()

    cv2.imshow("AI Blind Assistant", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
