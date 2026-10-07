document.getElementById('check').onclick=async()=>{
 const result=document.getElementById('result'),button=document.getElementById('check');button.disabled=true;
 let detector;
 try{
  result.textContent='Loading the local model…';
  const {FilesetResolver,HandLandmarker}=await import('/hand-assets/vision_bundle.mjs');
  const files=await FilesetResolver.forVisionTasks('/hand-assets/wasm');
  detector=await HandLandmarker.createFromOptions(files,{baseOptions:{modelAssetPath:'/hand-assets/hand_landmarker.task',delegate:'CPU'},runningMode:'IMAGE',numHands:2});
  const canvas=document.createElement('canvas');canvas.width=640;canvas.height=360;
  canvas.getContext('2d').fillRect(0,0,640,360);
  const output=detector.detect(canvas);
  if(output.landmarks.length!==0)throw Error('Unexpected landmarks on blank input');
  result.textContent='PASS · MediaPipe loaded and returned zero hands for a blank image. No camera was accessed.';
 }catch(error){result.textContent='Check failed: '+error.message+'. Run python scripts/download_vision_models.py and retry.';}
 finally{detector?.close();button.disabled=false;}
};
