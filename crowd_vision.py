import cv2
import numpy as np
import base64
from pathlib import Path
# Lazy load model on demand to conserve memory (keeps startup under 512MB RAM on Render)
_model = None

def get_yolo_model():
    global _model
    if _model is None:
        import os
        os.environ["OMP_NUM_THREADS"] = "1"
        try:
            import torch
            torch.set_num_threads(1)
        except Exception:
            pass
        from ultralytics import YOLO
        _model = YOLO('yolov8n.pt')
    return _model

def estimate_crowd_from_image(image_bytes: bytes, destination_id: str):
    """
    Runs YOLOv8 person detection on an image.
    This signal is illustrative/demo-only and would feed into UI 1's model 
    as a live feature in a production version.
    """
    # Convert bytes to numpy array for cv2
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Invalid image data")

    # Run inference
    model = get_yolo_model()
    results = model(img)
    
    # Class 0 in COCO is 'person'
    person_count = 0
    annotated_img = img.copy()
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            if cls_id == 0:  # person
                person_count += 1
                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Encode back to base64 for frontend display
    _, buffer = cv2.imencode('.jpg', annotated_img)
    b64_img = base64.b64encode(buffer).decode('utf-8')
    
    # Heuristic density score just for demo
    density_score = min(100, int((person_count / 50.0) * 100))
    
    return {
        "destination_id": destination_id,
        "detected_count": person_count,
        "estimated_density_score": density_score,
        "annotated_image": f"data:image/jpeg;base64,{b64_img}"
    }

def list_sample_images():
    sample_dir = Path("sample_images")
    if not sample_dir.exists():
        return []
    return [f.name for f in sample_dir.glob("*.jpg")]

def get_sample_image_bytes(filename: str) -> bytes:
    sample_path = Path("sample_images") / filename
    if sample_path.exists():
        return sample_path.read_bytes()
    raise FileNotFoundError(f"Sample {filename} not found")
