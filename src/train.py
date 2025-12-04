import os
from pathlib import Path
from dotenv import load_dotenv
from ultralytics import YOLO
import torch
from roboflow import Roboflow

load_dotenv()

def main():
    BASE_DIR = Path(__file__).parent[1]
    DATASET_DIR = BASE_DIR / "datasets"
    RUNS_DIR = BASE_DIR / "runs" / "detect"

    if not torch.cuda.is_available():
        print("Entraînement sur CPU (Lent)")

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("Clé api invalide")
        exit()    

    original_cwd = Path.cwd()

    try:
        os.chdir(DATASET_DIR)
        rf = Roboflow(api_key=api_key)
        project = rf.workspace("corentin-nvesn").project("buoys-and-boats-5wfca")
        version = project.version(1)
        dataset = version.download("yolov8")
    
    except Exception as e:
        print(f"Erreur Roboflow {e}")
        os.chdir(original_cwd)
        exit()
    
    os.chdir(original_cwd)
    data_yaml_path = Path(dataset.location) / "data.yaml"

    print(f"Entrainement {data_yaml_path}")

    model = YOLO('yolov8n.pt')

    model.train(
        data=str(data_yaml_path),
        epochs=50,
        imgsz=640,
        batch=16,
        patience=10,
        project=str(RUNS_DIR),
        name='modele_buoy_v1',
        exist_ok=True,
        verbose=True
    )

if __name__ == '__main__':
    main()