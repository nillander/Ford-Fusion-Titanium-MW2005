from graft import *
import time
G={}
pass
for k in ["headL","headR","tailL","tailR","fogL","fogR"]:
    t=time.time(); G[k]=compute_graft4(k); print(' %.1fs'%(time.time()-t))
pickle.dump(G,open('grafts_A.pkl','wb'))
