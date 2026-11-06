# 6.12: trova i 4 angoli dello schermo verde in ogni fotogramma, poi leviga le traiettorie.
import cv2, numpy as np, json
cap=cv2.VideoCapture('input/6.12_HR_greenscreen.mp4'); C=[]; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    m=cv2.inRange(hsv,(35,60,80),(85,255,255))
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cs,key=cv2.contourArea)
    hull=cv2.convexHull(c).reshape(-1,2).astype(np.float32)
    # 4 angoli: estremi lungo le diagonali
    s=hull.sum(1); d=hull[:,0]-hull[:,1]
    q=np.array([hull[s.argmin()],hull[d.argmax()],hull[s.argmax()],hull[d.argmin()]])   # TL TR BR BL
    C.append(q.reshape(-1)); 
    if i in (0,48,96): cv2.imwrite(f'/tmp/claude-0/-workspace/16e8af54-fc03-58a6-82b8-6753b5440978/scratchpad/gm_{i}.png',m)
    i+=1
C=np.array(C); t=np.arange(len(C))
print('fotogrammi',len(C)); print('angoli f0',C[0].round(1)); print('angoli f96',C[-1].round(1))
print('salto max grezzo %.2f px'%np.abs(np.diff(C,axis=0)).max())
Cs=np.stack([np.polyval(np.polyfit(t,C[:,k],5),t) for k in range(8)],1)
print('scarto grezzo/levigato max %.2f medio %.2f'%(np.abs(C-Cs).max(),np.abs(C-Cs).mean()))
json.dump({'raw':C.tolist(),'smooth':Cs.tolist()},open('612_corners.json','w'))
