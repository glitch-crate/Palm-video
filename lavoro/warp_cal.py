# Proietta la texture del calendario sul foglio tracciato (clip 3.3) -> PNG RGBA 1920x1080 per fotogramma
import cv2, numpy as np, json, os
Hs=json.load(open('cal_H.json')); out='/tmp/claude-0/fr/33'; os.makedirs(out,exist_ok=True)
quad=np.float32([[597,357],[1069,336],[1069,827],[595,807]])
canon=np.float32([[0,0],[700,0],[700,680],[0,680]])
H0=cv2.getPerspectiveTransform(canon,quad)
T=np.array([[1/3,0,-20],[0,1/3,-300],[0,0,1]])
for i,H in enumerate(Hs):
    tex=cv2.imread(f'/tmp/claude-0/fr/cal_tex/f_{i:05d}.png',cv2.IMREAD_UNCHANGED).astype(np.float32)/255
    a=tex[...,3:4]; pm=np.concatenate([tex[...,:3]*a,a],2)       # alfa premoltiplicato
    M=np.array(H)@H0@T
    w=cv2.warpPerspective(pm,M,(1920,1080),flags=cv2.INTER_AREA if False else cv2.INTER_LINEAR)
    w=cv2.GaussianBlur(w,(0,0),0.7)                               # morbidezza come il fuoco della ripresa
    a=w[...,3:4]; rgb=np.where(a>1e-4,w[...,:3]/np.maximum(a,1e-4),0)
    o=np.concatenate([rgb,a],2); cv2.imwrite(f'{out}/f_{i:05d}.png',(np.clip(o,0,1)*255+.5).astype(np.uint8))
print('ok',len(Hs))
