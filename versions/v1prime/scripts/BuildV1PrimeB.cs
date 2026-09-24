using System; using System.IO; using System.Collections.Generic; using mwgc.RealEngine;
// v1prime-b (from v1prime):
//  1) front/rear licence plates (BADGING groups) pushed 10 mm outwards: the bumper
//     paint and the plate-frame wedge pierced the plate at y=0 ("CHAPINHA" residue);
//  2) grille (BASE_A group 2 bars/ring + moved LOGO back panel) extracted into its
//     own leading groups of RIGHT_SIDE_MIRROR_A, two-sided, textures unchanged.
// args: v1prime.bin out.bin
public class BuildV1PrimeB {
  const uint BADGING=0x339D0D44;
  static RealGeometryFile Read(string p){var b=File.ReadAllBytes(p);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);var f=new RealGeometryFile();f.Open(new MemoryStream(b));return f;}
  static bool InGrille(RealVector3 a,RealVector3 b,RealVector3 c){float x=(a.x+b.x+c.x)/3,y=(a.y+b.y+c.y)/3,z=(a.z+b.z+c.z)/3;return x>2.15f&&Math.Abs(y)<0.55f&&z>0.36f&&z<0.6f;}
  class G{public RealShadingGroup g;public List<RealVertex> v=new List<RealVertex>();public List<int> i=new List<int>();public uint tex,sh;}
  // split a part's groups into (kept, extracted) by predicate
  static void Split(RealGeometryPart p,Func<int,bool> groupSel,List<G> keep,List<G> take,bool twoSidedTake){
    var d=p.PartData;int s=0;
    for(int gi=0;gi<d.Groups.Length;gi++){var gr=d.Groups[gi];
      var k=new G{g=gr,tex=p.PartInfo.Textures[gr.TextureIndex0],sh=p.PartInfo.Shaders[gr.ShaderIndex0]};
      var t=new G{g=gr,tex=k.tex,sh=k.sh};
      var mk=new Dictionary<int,int>();var mt=new Dictionary<int,int>();
      for(int q=gr.Offset;q<gr.Offset+gr.Length;q+=3){int a=d.Indices[q],b=d.Indices[q+1],c=d.Indices[q+2];
        bool ext=groupSel(gi)&&InGrille(d.Vertices[a].Position,d.Vertices[b].Position,d.Vertices[c].Position);
        var dst=ext?t:k;var map=ext?mt:mk;
        int[] loc=new int[3];int j=0;foreach(int vi in new[]{a,b,c}){int li;if(!map.TryGetValue(vi,out li)){li=dst.v.Count;dst.v.Add(d.Vertices[vi]);map[vi]=li;}loc[j++]=li;}
        dst.i.AddRange(loc);if(ext&&twoSidedTake){dst.i.Add(loc[2]);dst.i.Add(loc[1]);dst.i.Add(loc[0]);}}
      if(k.i.Count>0)keep.Add(k);if(t.i.Count>0)take.Add(t);s+=gr.VertexCount;}
  }
  static RealGeometryPart Assemble(RealGeometryPart template,List<G> gs){
    var tex=new List<uint>();var sh=new List<uint>();var verts=new List<RealVertex>();var idx=new List<ushort>();var groups=new List<RealShadingGroup>();
    float[] MN={1e9f,1e9f,1e9f},MX={-1e9f,-1e9f,-1e9f};
    foreach(var x in gs){int vb=verts.Count;verts.AddRange(x.v);int off=idx.Count;foreach(int q in x.i)idx.Add((ushort)(q+vb));
      int ti=tex.IndexOf(x.tex);if(ti<0){tex.Add(x.tex);ti=tex.Count-1;}int si=sh.IndexOf(x.sh);if(si<0){sh.Add(x.sh);si=sh.Count-1;}
      var g=x.g;g.Offset=off;g.Length=x.i.Count;g.TriangleCount=x.i.Count/3;g.VertexCount=x.v.Count;
      g.TextureIndex0=g.TextureIndex1=g.TextureIndex2=g.TextureIndex3=g.TextureIndex4=(byte)ti;g.ShaderIndex0=(byte)si;
      float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
      foreach(var v in x.v){var P=v.Position;mn[0]=Math.Min(mn[0],P.x);mn[1]=Math.Min(mn[1],P.y);mn[2]=Math.Min(mn[2],P.z);mx[0]=Math.Max(mx[0],P.x);mx[1]=Math.Max(mx[1],P.y);mx[2]=Math.Max(mx[2],P.z);}
      g.BoundsMin=new RealVector3(mn[0],mn[1],mn[2]);g.BoundsMax=new RealVector3(mx[0],mx[1],mx[2]);
      for(int k=0;k<3;k++){MN[k]=Math.Min(MN[k],mn[k]);MX[k]=Math.Max(MX[k],mx[k]);}
      groups.Add(g);}
    if(verts.Count>65535||idx.Count>65535)throw new Exception("limit exceeded "+verts.Count+"/"+idx.Count);
    var p=new RealGeometryPart();p.PartInfo=template.PartInfo;p.PartInfo.Textures=tex.ToArray();p.PartInfo.Shaders=sh.ToArray();p.PartInfo.TextureCount=(byte)tex.Count;p.PartInfo.ShaderCount=(byte)sh.Count;
    var d=template.PartData;d.Vertices=verts.ToArray();for(int k=0;k<d.Vertices.Length;k++)d.Vertices[k].Initialize(true,0);
    d.Indices=idx.ToArray();d.Groups=groups.ToArray();d.GroupCount=groups.Count;d.IndexCount=idx.Count;d.Materials=null;p.PartData=d;
    p.PartInfo.BoundMin=new RealVector4(MN[0],MN[1],MN[2],template.PartInfo.BoundMin.w);p.PartInfo.BoundMax=new RealVector4(MX[0],MX[1],MX[2],template.PartInfo.BoundMax.w);
    p.PartInfo.TriangleCount=idx.Count/3;p.PartInfo.Unk6_MW=idx.Count/3;return p;}

  static List<G> Decompose(RealGeometryPart p){var keep=new List<G>();var take=new List<G>();Split(p,gi=>false,keep,take,false);return keep;}
  // Replace the licence plate (LICENSEPLATE group, BADGING) of one side: drop the embossed
  // "CHAPINHA" letters and the letter-shaped holes, keep frame/border, add one flat face.
  static int FixPlate(G g,int side){
    // classify triangles
    var faceV=new List<RealVertex>();var tris=new List<int[]>();
    for(int q=0;q<g.i.Count;q+=3)tris.Add(new[]{g.i[q],g.i[q+1],g.i[q+2]});
    Func<int[],RealVector3> C=t=>{var a=g.v[t[0]].Position;var b=g.v[t[1]].Position;var c=g.v[t[2]].Position;return new RealVector3((a.x+b.x+c.x)/3,(a.y+b.y+c.y)/3,(a.z+b.z+c.z)/3);};
    Func<int[],RealVector2> U=t=>{var a=g.v[t[0]].UV;var b=g.v[t[1]].UV;var c=g.v[t[2]].UV;return new RealVector2((a.u+b.u+c.u)/3,(a.v+b.v+c.v)/3);};
    var sideT=tris.FindAll(t=>side>0?C(t).x>2f:C(t).x< -2f);
    var face=sideT.FindAll(t=>{var uv=U(t);return !(uv.u>=0.5f&&uv.v<0.5f);});
    var tr=sideT.FindAll(t=>{var uv=U(t);return uv.u>=0.5f&&uv.v<0.5f;});
    if(face.Count==0)return 0;
    // plate face extent and planar UV fit u,v = a*y + b*z + c (least squares)
    double ymin=1e9,ymax=-1e9,zmin=1e9,zmax=-1e9,xs=0;int n=0;
    double[,] A=new double[3,3];double[] bu=new double[3],bv=new double[3];
    var seen=new HashSet<int>();
    foreach(var t in face)foreach(int vi in t){if(!seen.Add(vi))continue;var P=g.v[vi].Position;var uv=g.v[vi].UV;
      ymin=Math.Min(ymin,P.y);ymax=Math.Max(ymax,P.y);zmin=Math.Min(zmin,P.z);zmax=Math.Max(zmax,P.z);xs+=P.x;n++;
      double[] r={P.y,P.z,1};for(int i=0;i<3;i++){for(int j=0;j<3;j++)A[i,j]+=r[i]*r[j];bu[i]+=r[i]*uv.u;bv[i]+=r[i]*uv.v;}}
    double xface=xs/n; double[] cu=Solve(A,bu),cv=Solve(A,bv);
    // letters: TR triangles whose centroid lies inside the face rectangle shrunk by 8 mm
    double m=0.008;var keepTR=tr.FindAll(t=>{var c=C(t);return !(c.y>ymin+m&&c.y<ymax-m&&c.z>zmin+m&&c.z<zmax-m);});
    int removed=tr.Count-keepTR.Count;
    // rebuild group: other-side triangles + kept border + new face quad
    var other=tris.FindAll(t=>!sideT.Contains(t));
    var nv=new List<RealVertex>(g.v);var ni=new List<int>();
    foreach(var t in other)ni.AddRange(t);foreach(var t in keepTR)ni.AddRange(t);
    var tmpl=g.v[face[0][0]];int b0=nv.Count;
    double[][] corners={new[]{ymin,zmin},new[]{ymax,zmin},new[]{ymax,zmax},new[]{ymin,zmax}};
    foreach(var cz in corners){var v=tmpl;v.Position=new RealVector3((float)(xface+side*0.001),(float)cz[0],(float)cz[1]);
      v.Normal=new RealVector3(side,0,0);v.UV=new RealVector2((float)(cu[0]*cz[0]+cu[1]*cz[1]+cu[2]),(float)(cv[0]*cz[0]+cv[1]*cz[1]+cv[2]));nv.Add(v);}
    // winding: front (+x) needs cross(b-a,c-a).x>0 ; corners go +y then +z => (0,1,2) gives +x
    if(side>0){ni.AddRange(new[]{b0,b0+1,b0+2,b0,b0+2,b0+3});}else{ni.AddRange(new[]{b0,b0+2,b0+1,b0,b0+3,b0+2});}
    // compact unused vertices
    var map=new Dictionary<int,int>();var cv2=new List<RealVertex>();var ci=new List<int>();
    foreach(int vi in ni){int li;if(!map.TryGetValue(vi,out li)){li=cv2.Count;cv2.Add(nv[vi]);map[vi]=li;}ci.Add(li);}
    g.v=cv2;g.i=ci;return removed;}
  static double[] Solve(double[,] A,double[] b){var M=(double[,])A.Clone();var x=(double[])b.Clone();int n=3;
    for(int i=0;i<n;i++){int p=i;for(int r=i+1;r<n;r++)if(Math.Abs(M[r,i])>Math.Abs(M[p,i]))p=r;
      for(int c=0;c<n;c++){var tt=M[i,c];M[i,c]=M[p,c];M[p,c]=tt;}var tb=x[i];x[i]=x[p];x[p]=tb;
      for(int r=0;r<n;r++){if(r==i)continue;double f=M[r,i]/M[i,i];for(int c=0;c<n;c++)M[r,c]-=f*M[i,c];x[r]-=f*x[i];}}
    for(int i=0;i<n;i++)x[i]/=M[i,i];return x;}
  public static void Main(string[] a){
    var f=Read(a[0]);var o=new RealGeometryFile();o.GeometryInfo=f.GeometryInfo;
    RealGeometryPart baseA=null,mirA=null;
    foreach(RealGeometryPart p in f){string n=p.PartInfo.PartName.ToString();if(n=="MUSTANGGT_BASE_A")baseA=p;if(n=="MUSTANGGT_KIT00_RIGHT_SIDE_MIRROR_A")mirA=p;}
    // grille extraction
    var baseKeep=new List<G>();var grille=new List<G>();Split(baseA,gi=>baseA.PartInfo.Textures[baseA.PartData.Groups[gi].TextureIndex0]==0x5A00E244u,baseKeep,grille,true);
    var mirKeep=new List<G>();var back=new List<G>();Split(mirA,gi=>true,mirKeep,back,true);
    var newBase=Assemble(baseA,baseKeep);var mirGroups=new List<G>();mirGroups.AddRange(grille);mirGroups.AddRange(back);mirGroups.AddRange(mirKeep);
    var newMir=Assemble(mirA,mirGroups);
    int moved=0;
    foreach(RealGeometryPart p0 in f){string n=p0.PartInfo.PartName.ToString();RealGeometryPart p=p0;
      if(n=="MUSTANGGT_BASE_A")p=newBase; else if(n=="MUSTANGGT_KIT00_RIGHT_SIDE_MIRROR_A")p=newMir;
      else for(int k=0;k<p.PartData.Vertices.Length;k++)p.PartData.Vertices[k].Initialize(true,0);
      if(n.StartsWith("MUSTANGGT_BASE_")){
        var gs=Decompose(p);int rem=0;
        foreach(var x in gs)if(x.sh==0x4C95C6F8u&&x.tex==BADGING){rem+=FixPlate(x,1);rem+=FixPlate(x,-1);}
        p=Assemble(p,gs);Console.WriteLine(n+": plate letters removed "+rem+" tris, idx "+p.PartData.Indices.Length);
      }
      if(n.StartsWith("MUSTANGGT_BASE_")){ // plates outwards
        var d=p.PartData;int s=0;var done=new HashSet<int>();
        foreach(var g in d.Groups){if(p.PartInfo.Textures[g.TextureIndex0]==BADGING){
            for(int q=g.Offset;q<g.Offset+g.Length;q++){int vi=d.Indices[q];if(!done.Add(vi))continue;var P=d.Vertices[vi].Position;
              if(Math.Abs(P.x)>2.0f){P.x+=P.x>0?0.010f:-0.010f;d.Vertices[vi].Position=P;moved++;}}}
          s+=g.VertexCount;}
        p.PartData=d;
        p.PartInfo.BoundMin.x=Math.Min(p.PartInfo.BoundMin.x,p.PartInfo.BoundMin.x-0.01f);p.PartInfo.BoundMax.x=p.PartInfo.BoundMax.x+0.01f;}
      o.AddPart(p);}
    o.GeometryInfo.PartCount=o.PartCount;o.Save(a[1]);
    Console.WriteLine("grille groups: "+grille.Count+" ("+grille.ConvertAll(x=>x.i.Count/3).ConvertAll(x=>x.ToString()).ToArray().Length+"), back groups: "+back.Count);
    foreach(var x in grille)Console.WriteLine("  grille tex "+x.tex.ToString("X8")+" tris(two-sided) "+x.i.Count/3);
    foreach(var x in back)Console.WriteLine("  back tex "+x.tex.ToString("X8")+" tris(two-sided) "+x.i.Count/3);
    Console.WriteLine("BASE_A idx "+newBase.PartData.Indices.Length+", MIRROR_A idx "+newMir.PartData.Indices.Length+", plate vertices moved "+moved);
  }
}
