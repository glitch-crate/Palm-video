# Tracciamento v2 del foglio (clip 3.3): ogni fotogramma registrato direttamente sul fotogramma 0 (ECC, omografia,
# su un ritaglio a metà risoluzione), poi traiettorie degli angoli levigate -> niente salti / flicker.
import cv2, numpy as np, json
X0,Y0,X1,Y1,s=380,0,1320,1080,0.5
cap=cv2.VideoCapture('../10_PALM_3.3_dettaglio_calendario.mp4'); F=[]
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.cvtColor(f[Y0:Y1,X0:X1],cv2.COLOR_BGR2GRAY)
    F.append(cv2.GaussianBlur(cv2.resize(g,None,fx=s,fy=s,interpolation=cv2.INTER_AREA),(0,0),1.0).astype(np.float32)/255)
mask=np.zeros(F[0].shape,np.uint8)
poly=(np.array([[585,165],[1080,160],[1080,835],[585,815]])-[X0,Y0])*s
cv2.fillPoly(mask,[poly.astype(np.int32)],255)
crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,80,1e-5)
# conversione omografia ritaglio-ridotto -> pieno formato
T=np.array([[s,0,-X0*s],[0,s,-Y0*s],[0,0,1]])
quad=np.float32([[597,357],[1069,336],[1069,827],[595,807]]).reshape(-1,1,2)
W=np.eye(3,dtype=np.float32); C=[]
for i,f in enumerate(F):
    if i>0: _,W=cv2.findTransformECC(F[0],f,W,cv2.MOTION_HOMOGRAPHY,crit,mask,3)
    Hfull=np.linalg.inv(T)@W.astype(np.float64)@T   # ECC: W porta il fotogramma 0 nel fotogramma i
    C.append(cv2.perspectiveTransform(quad,Hfull).reshape(-1))
C=np.array(C); t=np.arange(len(C))
print('salto max grezzo tra fotogrammi: %.2f px'%np.abs(np.diff(C,axis=0)).max())
Cs=np.stack([np.polyval(np.polyfit(t,C[:,k],4),t) for k in range(8)],1)
r=np.abs(C-Cs); print('scarto grezzo vs levigato: max %.2f px, medio %.2f px'%(r.max(),r.mean()))
print('angolo alto-sx primo/ultimo:',C[0][:2].round(1),C[-1][:2].round(1))
Hs=[cv2.getPerspectiveTransform(quad.reshape(-1,2),c.reshape(-1,2).astype(np.float32)).tolist() for c in Cs]
json.dump(Hs,open('cal_H.json','w'))
