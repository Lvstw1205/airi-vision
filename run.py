#!/usr/bin/env python3
"""Local camera landmarks, enrolled face comparison and Ollama visual questions."""
import argparse,base64,io,json,mimetypes,threading,time,urllib.request
from pathlib import Path
from types import SimpleNamespace
from PIL import Image
from local_http import LocalHandler,serve
import camera_presence
ROOT=Path(__file__).resolve().parent
OLLAMA='http://127.0.0.1:11434'

def ollama(path,body=None):
 req=urllib.request.Request(OLLAMA+path,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
 try:
  with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req,timeout=120) as r:return json.load(r)
 except (OSError,ValueError) as exc:
  raise ValueError('Ollama is unavailable or rejected the request. Start Ollama and install a vision-capable model.') from exc

def decode_frame(value):
 if not isinstance(value,str) or len(value)>2800000:raise ValueError('Frame is missing or too large.')
 try:
  raw=base64.b64decode(value,validate=True)
  with Image.open(io.BytesIO(raw)) as image:
   if image.format!='JPEG' or max(image.size)>1920 or min(image.size)<32:raise ValueError()
   image.verify()
 except Exception as exc:raise ValueError('Send a valid JPEG frame, maximum 1920 pixels per side.') from exc
 return raw

class Frames:
 def __init__(self):self.raw=None;self.timestamp=0
 def get(self):
  if not self.raw or time.monotonic()-self.timestamp>5:raise ValueError('Start the camera and provide a fresh frame.')
  return self.raw

def main():
 p=argparse.ArgumentParser(description='AIRI Vision · local camera intelligence')
 p.add_argument('--port',type=int,default=8768);p.add_argument('--data-dir',type=Path,default=ROOT/'data')
 args=p.parse_args()
 if not 1024<=args.port<=65535:p.error('Port must be between 1024 and 65535')
 app=SimpleNamespace(DATA=args.data_dir.resolve(),frames=Frames());lock=threading.RLock()
 presence=camera_presence.Presence(app)
 class Handler(LocalHandler):
  def route_get(self,path):
   if path=='/api/status':
    ready=all((ROOT/name).is_file() for name in json.loads((ROOT/'config/vision-assets.json').read_text())['assets'])
    with lock:self.send_json({'models_ready':ready,'presence':presence.status()})
    return True
   if path=='/api/models':
    self.send_json({'models':[m['name'] for m in ollama('/api/tags').get('models',[])]});return True
   relative='index.html' if path=='/' else path.lstrip('/')
   file=(ROOT/'web'/relative).resolve()
   if not file.is_relative_to(ROOT/'web') or not file.is_file():return False
   raw=file.read_bytes();kind=mimetypes.guess_type(file)[0] or 'application/octet-stream'
   self.send_response(200);self.headers_common();self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw);return True
  def route_post(self,path,body):
   if path=='/api/vision':
    raw=decode_frame(body.get('image'));model=str(body.get('model',''))
    if not model or len(model)>128:raise ValueError('Choose an installed vision model.')
    info=ollama('/api/show',{'model':model})
    if info.get('remote_host') or info.get('remote_model') or model.endswith(('-cloud',':cloud')):raise ValueError('Choose a local model; remote Ollama models are not used for camera frames.')
    if 'vision' not in info.get('capabilities',[]):raise ValueError('This model cannot read images. Choose a vision-capable Ollama model.')
    question=str(body.get('question','Describe what is visible.'))[:2000]
    result=ollama('/api/chat',{'model':model,'stream':False,'messages':[{'role':'system','content':'Describe only what is visible. Say when uncertain. Do not identify people or infer sensitive attributes from appearance.'},{'role':'user','content':question,'images':[base64.b64encode(raw).decode()]}],'options':{'num_predict':400}})
    return {'answer':result.get('message',{}).get('content',''),'model':model}
   if path!='/api/presence':raise ValueError('Unknown API endpoint')
   with lock:
    try:
     if 'image' in body:app.frames.raw=decode_frame(body['image']);app.frames.timestamp=time.monotonic()
     result=presence.action(body);result.pop('image',None);return result
    finally:app.frames.raw=None
 serve(Handler,args.port)
if __name__=='__main__':main()
