# islands (connected components per shader) of the Mondeo soup -> mondeo_islands.pkl (used by mondeo_lamps.py)
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/c12/lib')
from common import *
from islands import islands
n,lab=islands(S['M'],S['F'],split_by=S['shader'])
pickle.dump(lab,open('/home/claude/c12/mondeo_islands.pkl','wb')); print('islands',n)
