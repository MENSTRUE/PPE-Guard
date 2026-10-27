from unittest.mock import patch

def test_invalid_upload(client):
    r=client.post("/api/v1/predict/image",files={"file":("x.txt",b"hello","text/plain")})
    assert r.status_code==415

def test_corrupt_image(client):
    r=client.post("/api/v1/predict/image",files={"file":("x.png",b"not a png","image/png")})
    assert r.status_code==422

def test_mocked_prediction_contract(client,sample_jpeg):
    # Mock only expensive neural inference; exercises real FastAPI+decode+response schema
    prediction={
        "model":"ppe_guard_best.pt","task":"detect","detections":[
            {"class_id":0,"class_name":"helmet","confidence":0.9,"bbox":{"x1":5,"y1":5,"x2":50,"y2":40}}
        ],
        "detection_count":1,"inference_ms":12.5,
        "safety_observations":{
            "ppe_detected":["helmet"],"source_labeled_absences":[],"compliance_status":"not_assessed",
            "requires_human_review":False,"note":"mock only"},
        "annotated_image_base64":None
    }
    with patch("app.api.routes.predict.predict_image",return_value=prediction):
        r=client.post("/api/v1/predict/image",files={"file":("sample.jpg",sample_jpeg,"image/jpeg")})
    assert r.status_code==200,r.text
    data=r.json()
    assert data["image"]["width"]==80
    assert data["detections"][0]["class_name"]=="helmet"
    assert data["detection_count"]==1
