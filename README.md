# AI-Blind-Assistant
An AI-based accessibility solution that uses computer vision and voice assistance to detect objects, recognize currency notes and search for user-requested objects in real time, helping visually impaired individuals navigate their surroundings.
# Features
- Real-time Object Detection
- Currency Recognition
- Voice Feedback
- Search and Locate User-Requested Objects
- Accessibility-Focused Interface
  # Technologies Used
- Python
- OpenCV
- YOLO
- EasyOCR / Tesseract OCR
- pyttsx3 (Text-to-Speech)
- NumPy
- # Installation steps
### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Blind-Assistant.git
cd AI-Blind-Assistant
```
### 2. Create Environment

```bash
conda create -n blindai python=3.10
conda activate blindai
```
### 3. Install Dependencies

```bash
pip install ultralytics
pip install opencv-python
pip install pywin32
```
### 4. Download Models

* YOLOv8 Object Detection Model (`yolov8s.pt`)
* Custom Indian Currency Detection Model (`best.pt`)

Update the currency model path inside the code.

### 5. Run the Project
#### AI Blind Assistant

```bash
python blind_assistant.py
```
Features:
* Object Detection
* Obstacle Awareness
* Voice Navigation
* Currency Recognition
#### Object Finder

```bash
python find_object.py
```
Features:
* Voice Command Recognition
* Object Search
* Real-Time Guidance to Locate Objects
  
## Usage Instructions
### AI Blind Assistant
1. Run the application:

```bash
python blind_assistant.py
```
2. Allow webcam access.
3. The system will:

   * Detect surrounding objects.
   * Provide voice-based obstacle warnings.
   * Guide the user with left, right, and ahead directions.
   * Recognize Indian currency notes and announce their denomination.

### Object Finder
1. Run the Object Finder module:

```bash
python find_object.py
```
2. Speak the name of the object you want to find.
Example commands:

* Find my bottle
* Find my backpack
* Find my chair
* Find my mobile phone

3. The system will search for the requested object using the webcam and provide voice guidance when the object is detected.
### Exit
Press **Q** to close the application window.

# Future Improvements
- Integration with smart glasses for hands-free assistance
- Multi-language voice assistance
- GPS-based outdoor navigation
- Improved currency recognition for folded and damaged notes
- Enhanced object finder with distance estimation.
