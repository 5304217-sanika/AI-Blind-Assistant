from ultralytics import YOLO
import cv2
import win32com.client
import speech_recognition as sr

# Voice
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Speech Recognition
recognizer = sr.Recognizer()

# YOLO Model
model = YOLO("yolov8s.pt")

print("Say: Find my bottle / chair / backpack")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = recognizer.listen(source)

try:
    command = recognizer.recognize_google(audio).lower()
    print("You said:", command)

except:
    speaker.Speak("I could not understand")
    exit()

if "find my" in command:
    target_object = command.replace("find my", "").strip()
else:
    speaker.Speak("Please say find my object")
    exit()

speaker.Speak(f"Searching for {target_object}")

cap = cv2.VideoCapture(0)

announced = False

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, verbose=False)

    boxes = results[0].boxes
    names = results[0].names

    frame_width = frame.shape[1]

    found = False

    for box in boxes:

        confidence = float(box.conf[0])

        if confidence < 0.50:
            continue

        cls = int(box.cls[0])
        object_name = names[cls].lower()

        if object_name != target_object:
            continue

        found = True

        x1, y1, x2, y2 = box.xyxy[0]

        center_x = (x1 + x2) / 2

        if center_x < frame_width / 3:
            position = "on the left"

        elif center_x < 2 * frame_width / 3:
            position = "ahead"

        else:
            position = "on the right"

        message = f"{target_object} found {position}"

        print(message)

        if not announced:
            speaker.Speak(message)
            announced = True

    if not found:
        announced = False

    annotated_frame = results[0].plot()

    cv2.imshow("Voice Object Finder", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()