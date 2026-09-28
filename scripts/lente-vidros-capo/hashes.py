def bh(s):
    h=0xFFFFFFFF
    for c in s.encode(): h=(h*33+c)&0xFFFFFFFF
    return h
