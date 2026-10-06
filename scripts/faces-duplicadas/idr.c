#include <math.h>
/* ortho id-buffer: P[n*3*2] screen xy, Z[n*3] depth (bigger = closer), cull: keep only tris with ccw area>0 */
void idbuf(int n,const float*X,const float*Y,const float*Z,int W,int H,float*zb,int*id){
  for(int i=0;i<W*H;i++){zb[i]=-1e30f;id[i]=-1;}
  for(int t=0;t<n;t++){
    float x0=X[3*t],x1=X[3*t+1],x2=X[3*t+2],y0=Y[3*t],y1=Y[3*t+1],y2=Y[3*t+2];
    float a=(x1-x0)*(y2-y0)-(x2-x0)*(y1-y0); if(a<=0)continue;
    int mnx=(int)floorf(fminf(x0,fminf(x1,x2))),mxx=(int)ceilf(fmaxf(x0,fmaxf(x1,x2)));
    int mny=(int)floorf(fminf(y0,fminf(y1,y2))),mxy=(int)ceilf(fmaxf(y0,fmaxf(y1,y2)));
    if(mnx<0)mnx=0;if(mny<0)mny=0;if(mxx>W-1)mxx=W-1;if(mxy>H-1)mxy=H-1;
    for(int py=mny;py<=mxy;py++)for(int px=mnx;px<=mxx;px++){
      float sx=px+0.5f,sy=py+0.5f;
      float w0=((x1-sx)*(y2-sy)-(x2-sx)*(y1-sy))/a, w1=((x2-sx)*(y0-sy)-(x0-sx)*(y2-sy))/a, w2=1-w0-w1;
      if(w0<0||w1<0||w2<0)continue;
      float z=w0*Z[3*t]+w1*Z[3*t+1]+w2*Z[3*t+2]; int k=py*W+px;
      if(z>zb[k]){zb[k]=z;id[k]=t;}
    }
  }
}
