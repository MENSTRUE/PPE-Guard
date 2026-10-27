import time
from io import BytesIO
import base64
from threading import Lock
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from app.inference.loader import get_model
from app.inference.contract import CLASS_NAMES
from app.inference.safety_rules import summarize_observations

_predict_lock = Lock()  # shared Ultralytics model may not be thread-safe

def annotate(image: Image.Image, detections: list[dict]) -> str:
    canvas = image.copy().convert("RGB")
    draw = ImageDraw.Draw(canvas)
    for det in detections:
        b = det["bbox"]
        label = f"{det['class_name']} {det['confidence']:.2f}"
        draw.rectangle((b["x1"], b["y1"], b["x2"], b["y2"]), outline=(30, 220, 160), width=max(2, image.width//250))
        tx,ty=int(b["x1"]), max(0,int(b["y1"])-17)
        text_w = min(image.width-tx, max(60, 8*len(label)))
        draw.rectangle((tx,ty,min(image.width,tx+text_w),min(image.height,ty+17)),fill=(0,55,48))
        draw.text((tx+3,ty+2), label, fill=(255,255,255))
    buf = BytesIO()
    canvas.save(buf,format="JPEG",quality=85,optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")

def predict_image(image: Image.Image, *, conf:float, iou:float, imgsz:int, include_annotated:bool=False) -> dict:
    model = get_model()
    start = time.perf_counter()
    with _predict_lock:
        output = model.predict(source=np.array(image),conf=conf,iou=iou,imgsz=imgsz,verbose=False,device="cpu" if __import__("torch").cuda.is_available() is False else None)[0]
    elapsed = (time.perf_counter()-start)*1000
    detections=[]
    if output.boxes is not None:
        for box in output.boxes:
            idx = int(box.cls.item())
            if idx < 0 or idx >= len(CLASS_NAMES):
                raise RuntimeError(f"Unexpected model class index: {idx}")
            x1,y1,x2,y2 = [float(v) for v in box.xyxy[0].tolist()]
            detections.append({
                "class_id":idx,"class_name":CLASS_NAMES[idx],"confidence":round(float(box.conf.item()),6),
                "bbox":{"x1":round(x1,2),"y1":round(y1,2),"x2":round(x2,2),"y2":round(y2,2)}
            })
    return {
        "model":"ppe_guard_best.pt", "task":"detect", "detections":detections,
        "detection_count":len(detections),"inference_ms":round(elapsed,2),
        "safety_observations":summarize_observations(detections),
        "annotated_image_base64":annotate(image,detections) if include_annotated else None,
    }
