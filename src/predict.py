import cv2
from ultralytics import YOLO
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
MODEL_PATH = BASE_DIR / "models" / "best.pt"
IMG_PATH = BASE_DIR / "assets" / "buoy_boat.jpg"
CONFIDENCE_THRESHOLD = 0.7


def run_inference(source=None):
    model = YOLO(MODEL_PATH)
    # Source None = webcam
    input_source = 0 if source is None else source
    img_source = str(input_source).lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))

    if img_source:
        results = model.predict(input_source, conf=CONFIDENCE_THRESHOLD, save=True)
        results[0].show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    else:
        results = model.predict(source=input_source, 
                                conf=CONFIDENCE_THRESHOLD, 
                                stream=True, 
                                show=True)
        for r in results:
            pass
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test Webcam 
    #run_inference() 

    # Test Image
    run_inference(IMG_PATH)