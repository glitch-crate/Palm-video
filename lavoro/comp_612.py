# 6.12: inserisce lo schermo HD nel monitor verde della clip HR.
# Uscite: /tmp/claude-0/fr/612comp (clip completa RGB) e /tmp/claude-0/fr/612alpha (solo schermo, RGBA)
import cv2, numpy as np, json, os
C=np.array(json.load(open('612_corners.json'))['smooth'],np.float32)
cap=cv2.VideoCapture('input/6.12_HR_greenscreen.mp4')
oc,oa='/tmp/claude-0/fr/612comp','/tmp/claude-0/fr/612alpha'; os.makedirs(oc,exist_ok=True); os.makedirs(oa,exist_ok=True)
src=np.float32([[0,0],[1600,0],[1600,900],[0,900]]); SS=4
for i in range(97):
    ok,f=cap.read(); f=f.astype(np.float32)/255
    q=C[i].reshape(4,2)
    # matte antialiasato (supersampling 4x), allargato di 1 px per coprire l'alone verde
    cen=q.mean(0); qe=cen+(q-cen)*(1+1.2/np.linalg.norm(q-cen,axis=1,keepdims=True))
    big=np.zeros((1080*SS,1920*SS),np.uint8); cv2.fillPoly(big,[np.round(qe*SS).astype(np.int32)],255)
    m=cv2.resize(big,(1920,1080),interpolation=cv2.INTER_AREA).astype(np.float32)[...,None]/255
    scr=cv2.imread(f'/tmp/claude-0/fr/612scr/f_{i:05d}.png',cv2.IMREAD_UNCHANGED)[...,:3].astype(np.float32)/255
    H=cv2.getPerspectiveTransform(src,q)
    w=cv2.warpPerspective(scr,H,(1920,1080),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_REPLICATE)
    # aspetto da monitor ripreso: leggera morbidezza, neri sollevati, un filo di grana
    w=cv2.GaussianBlur(w,(0,0),0.55); w=0.03+w*0.95
    rng=np.random.default_rng(i); w=np.clip(w+rng.normal(0,0.006,w.shape).astype(np.float32),0,1)
    # despill del verde residuo sul bordo della cornice
    g=f[...,1]; mx=np.maximum(f[...,0],f[...,2]); f[...,1]=np.where(g>mx,mx+(g-mx)*0.2,g)
    out=f*(1-m)+w*m
    cv2.imwrite(f'{oc}/f_{i:05d}.png',(np.clip(out,0,1)*255+.5).astype(np.uint8))
    rgba=np.concatenate([w,m],2); cv2.imwrite(f'{oa}/f_{i:05d}.png',(np.clip(rgba,0,1)*255+.5).astype(np.uint8))
print('ok')
