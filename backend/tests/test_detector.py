from unittest.mock import patch
from PIL import Image
from app.inference.detector import predict_image
from app.inference.contract import CLASS_NAMES

class FakeValue:
    def __init__(self,value): self.value=value
    def item(self): return self.value

class FakeCoords:
    def __init__(self,values): self.values=values
    def tolist(self): return self.values

class FakeBox:
    cls=FakeValue(1)
    conf=FakeValue(0.91)
    xyxy=[FakeCoords([5,6,50,40])]

class FakeResult:
    boxes=[FakeBox()]

class FakeModel:
    def predict(self, **kwargs):
        assert kwargs['imgsz']==640
        return [FakeResult()]

def test_detector_real_postprocessing_with_fake_model():
    with patch('app.inference.detector.get_model',return_value=FakeModel()):
        out=predict_image(Image.new('RGB',(80,60)),conf=.25,iou=.45,imgsz=640,include_annotated=True)
    assert out['detections'][0]['class_name']=='no_helmet'
    assert out['detection_count']==1
    assert out['safety_observations']['requires_human_review']
    assert out['annotated_image_base64']
