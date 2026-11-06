# 6.12: zoom finale sui genitori con la bambina (applicato alla clip composta e al livello schermo)
import cv2, numpy as np, os
T0, T1 = 2.2, 4.04            # inizio e fine dello zoom (s)
S1, CX, CY = 1.6, 990, 480    # ingrandimento finale e centro (tra mamma con bambina e papà)
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)*0+ (1-(1-x)**3 if x<0 else (3*x*x-2*x*x*x))
for src,dst,alpha in [('612comp','612zoom',False),('612alpha','612zoom_a',True)]:
    os.makedirs(f'/tmp/claude-0/fr/{dst}',exist_ok=True)
    for i in range(97):
        t=i/24; k=ease((t-T0)/(T1-T0)); s=1+(S1-1)*k
        cx=960+(CX-960)*k; cy=540+(CY-540)*k
        M=np.float32([[s,0,960-s*cx],[0,s,540-s*cy]])
        f=cv2.imread(f'/tmp/claude-0/fr/{src}/f_{i:05d}.png',cv2.IMREAD_UNCHANGED)
        o=cv2.warpAffine(f,M,(1920,1080),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(f'/tmp/claude-0/fr/{dst}/f_{i:05d}.png',o)
print('ok')
