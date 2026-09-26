#include <math.h>
#include <stdint.h>
// tris: n triangles; xy z per vertex (n*3*3 floats: sx,sy,depth(bigger=closer))
// uv: n*3*2 ; col: n*3 (flat rgb per tri) ; tex: per tri texture index (-1 none)
// texdata: floats rgba concatenated; texoff[t] offset (in pixels), texw[t], texh[t]
// out img W*H*3, zb W*H, id W*H (int)
void raster(int n,const float*v,const float*uv,const float*col,const int*tex,
            const float*texdata,const int64_t*texoff,const int*texw,const int*texh,
            int W,int H,float*img,float*zb,int*id,int alphatest){
  for(int t=0;t<n;t++){
    const float*a=v+t*9,*b=a+3,*c=a+6;
    float x0=a[0],y0=a[1],x1=b[0],y1=b[1],x2=c[0],y2=c[1];
    float area=(x1-x0)*(y2-y0)-(x2-x0)*(y1-y0);
    if(fabsf(area)<1e-12f) continue;
    int minx=(int)floorf(fminf(x0,fminf(x1,x2))),maxx=(int)ceilf(fmaxf(x0,fmaxf(x1,x2)));
    int miny=(int)floorf(fminf(y0,fminf(y1,y2))),maxy=(int)ceilf(fmaxf(y0,fmaxf(y1,y2)));
    if(minx<0)minx=0; if(miny<0)miny=0; if(maxx>W-1)maxx=W-1; if(maxy>H-1)maxy=H-1;
    int ti=tex[t];
    for(int y=miny;y<=maxy;y++)for(int x=minx;x<=maxx;x++){
      float px=x+0.5f,py=y+0.5f;
      float w0=((x1-px)*(y2-py)-(x2-px)*(y1-py))/area;
      float w1=((x2-px)*(y0-py)-(x0-px)*(y2-py))/area;
      float w2=1-w0-w1;
      if(w0<0||w1<0||w2<0) continue;
      float z=w0*a[2]+w1*b[2]+w2*c[2];
      int k=y*W+x;
      if(z<=zb[k]) continue;
      float r=col[t*3],g=col[t*3+1],bl=col[t*3+2];
      if(ti>=0){
        const float*u=uv+t*6;
        float uu=w0*u[0]+w1*u[2]+w2*u[4], vv=w0*u[1]+w1*u[3]+w2*u[5];
        uu-=floorf(uu); vv-=floorf(vv);
        int tw=texw[ti],th=texh[ti];
        int tx=(int)(uu*tw); if(tx>=tw)tx=tw-1; int ty=(int)(vv*th); if(ty>=th)ty=th-1;
        const float*p=texdata+(texoff[ti]+(int64_t)ty*tw+tx)*4;
        if(alphatest && p[3]<0.3f) continue;
        r*=p[0];g*=p[1];bl*=p[2];
      }
      zb[k]=z; id[k]=t; img[k*3]=r; img[k*3+1]=g; img[k*3+2]=bl;
    }
  }
}
