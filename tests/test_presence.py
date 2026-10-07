import base64,io,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from PIL import Image
from run import decode_frame,Frames
from camera_presence import Presence
class PresenceTests(unittest.TestCase):
 def test_decode_and_limits(self):
  out=io.BytesIO();Image.new('RGB',(640,360)).save(out,format='JPEG');encoded=base64.b64encode(out.getvalue()).decode()
  self.assertEqual(decode_frame(encoded),out.getvalue())
  for value in ('invalid',None,'A'*2800001):
   with self.assertRaises(ValueError):decode_frame(value)
 def test_fresh_install_and_forget_pending(self):
  with tempfile.TemporaryDirectory() as tmp:
   presence=Presence(SimpleNamespace(DATA=Path(tmp),frames=Frames()))
   self.assertFalse(presence.status()['registered']);self.assertFalse(presence.status()['authentication'])
   presence.action({'action':'enroll_begin','name':'Example'});presence.pending=[[0]*128]
   result=presence.action({'action':'forget_all'})
   self.assertEqual(result['pending_samples'],0);self.assertFalse(result['enrolling']);self.assertFalse(result['registered'])
 def test_no_implicit_camera_frame(self):
  with self.assertRaises(ValueError):Frames().get()
 def test_real_models_blank_frame(self):
  model=Path(__file__).resolve().parents[1]/'.runtime/presence/models/face_recognition_sface_2021dec.onnx'
  if not model.exists():self.skipTest('Optional model weights not downloaded')
  with tempfile.TemporaryDirectory() as tmp:
   p=Presence(SimpleNamespace(DATA=Path(tmp),frames=Frames()))
   out=io.BytesIO();Image.new('RGB',(640,360)).save(out,format='JPEG')
   self.assertEqual(p.detect(out.getvalue()),[])
