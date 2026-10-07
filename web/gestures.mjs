// Joint-relative geometry adapted from AIRI's camera gesture controller.
export function classify(p,aspect=16/9){
 if(!p||p.length!==21||!p.every(v=>Number.isFinite(v.x)&&Number.isFinite(v.y)))return 'No hand';
 const d=(a,b)=>Math.hypot((p[a].x-p[b].x)*aspect,p[a].y-p[b].y,((p[a].z||0)-(p[b].z||0))*aspect);
 const ext=t=>{const n=d(t-3,t-2)+d(t-2,t-1)+d(t-1,t);return n>.025&&d(t-3,t)/n>.82&&d(t-3,t)>d(t-3,t-2)*1.35;};
 const f=[8,12,16,20].map(ext);
 if(f.every(Boolean))return 'Open hand';
 if(f.every(x=>!x))return 'Closed hand';
 if(f[0]&&f[1]&&!f[2]&&!f[3])return 'V sign';
 if(!f[0]||f.slice(1).some(Boolean))return 'Hand detected';
 const dx=(p[8].x-p[5].x)*aspect,dy=p[8].y-p[5].y;
 return Math.abs(dx)>Math.abs(dy)?(dx<0?'Point left':'Point right'):(dy<0?'Point up':'Point down');
}
export const connections=[[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[5,9],[9,10],[10,11],[11,12],[9,13],[13,14],[14,15],[15,16],[13,17],[0,17],[17,18],[18,19],[19,20]];
