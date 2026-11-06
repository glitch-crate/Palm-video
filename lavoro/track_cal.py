# Traccia il foglio del calendario (clip 3.3) e salva un'omografia per fotogramma, relativa al fotogramma 0.
import cv2, numpy as np, json, sys
cap=cv2.VideoCapture('../10_PALM_3.3_dettaglio_calendario.mp4')
ok,prev=cap.read(); pg=cv2.cvtColor(prev,cv2.COLOR_BGR2GRAY)
mask=np.zeros_like(pg); cv2.fillPoly(mask,[np.array([[560,110],[1170,90],[1190,950],[550,920]])],255)
p0=cv2.goodFeaturesToTrack(pg,600,0.005,8,mask=mask)
Hs=[np.eye(3).tolist()]; Hacc=np.eye(3)
pts0=p0.copy(); cur=p0.copy(); ref=pg
while True:
    ok,fr=cap.read()
    if not ok: break
    g=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY)
    nxt,st,err=cv2.calcOpticalFlowPyrLK(pg,g,cur,None,winSize=(31,31),maxLevel=4)
    good=st.ravel()==1
    # omografia diretta: punti originali del fotogramma 0 -> posizione attuale
    H,inl=cv2.findHomography(pts0[good],nxt[good],cv2.RANSAC,1.5)
    Hs.append(H.tolist()); pts0=pts0[good]; cur=nxt[good]; pg=g
print(len(Hs),'frames, punti finali',len(cur))
json.dump(Hs,open('cal_H.json','w'))
# verifica: disegna il quad della griglia sull'ultimo fotogramma
quad=np.float32([[597,357],[1069,336],[1069,827],[595,807]]).reshape(-1,1,2)
q=cv2.perspectiveTransform(quad,np.array(Hs[-1]))
cv2.polylines(fr,[q.astype(np.int32)],True,(0,0,255),2); cv2.imwrite('check/track_last.png',fr)
