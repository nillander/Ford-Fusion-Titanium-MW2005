from common import *
from xray import xcast
import sys
src=sys.argv[1]; nm=sys.argv[2] if len(sys.argv)>2 else 'MUSTANGGT_KIT00_BODY_A'
Pb=pickle.load(open(src,'rb')) if src.endswith('.pkl') else geo.load(src)
B=mwsoup.soup([p for p in Pb if p['name']==nm])
C=B['P'][B['F']].mean(1); r=(C[:,0]<-2.0)&(C[:,2]>0.65)&(C[:,2]<0.85)
ys=np.linspace(-0.34,0.34,341); zs=np.arange(0.70,0.82,0.0007)
YY,ZZ=np.meshgrid(ys,zs); Q=np.c_[YY.ravel(),ZZ.ravel()]
x=xcast(B['P'],B['F'][r],Q).reshape(YY.shape)
miss=~np.isfinite(x); print(src,nm,'miss total',miss.sum(),'z rows',np.round(zs[miss.any(1)],4)[:40])
