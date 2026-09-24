using System; using System.IO; using System.Collections.Generic; using mwgc.RealEngine;
// v1prime = vprime + only one structural fix: BASE_A crossed 65,535 indices
// (78,144). Group 4 (LOGO sheet, holds the grille core) began at 38,646 and its
// tail passed the limit; group 5 (HEADLIGHTGLASS) began at 76,539 and was never drawn.
// Move group 4 into the empty RIGHT_SIDE_MIRROR_A slot and leave group 5 out so the
// rest of the car keeps exactly the vprime look.  args: vprime.bin out.bin
public class BuildV1Prime {
  static RealGeometryFile Read(string p){var b=File.ReadAllBytes(p);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);var f=new RealGeometryFile();f.Open(new MemoryStream(b));return f;}
  static RealGeometryPart Sub(RealGeometryPart src,int[] keep){
    var d=src.PartData;var starts=new int[d.Groups.Length];int acc=0;
    for(int g=0;g<d.Groups.Length;g++){starts[g]=acc;acc+=d.Groups[g].VertexCount;}
    var verts=new List<RealVertex>();var idx=new List<ushort>();var groups=new List<RealShadingGroup>();
    foreach(int g in keep){var grp=d.Groups[g];int vb=verts.Count;
      for(int i=0;i<grp.VertexCount;i++)verts.Add(d.Vertices[starts[g]+i]);
      int off=idx.Count;for(int i=grp.Offset;i<grp.Offset+grp.Length;i++)idx.Add((ushort)(d.Indices[i]-starts[g]+vb));
      grp.Offset=off;groups.Add(grp);}
    var p=new RealGeometryPart();p.PartInfo=src.PartInfo;var od=d;
    od.Vertices=verts.ToArray();od.Indices=idx.ToArray();od.Groups=groups.ToArray();od.GroupCount=groups.Count;od.IndexCount=idx.Count;od.Materials=null;
    for(int i=0;i<od.Vertices.Length;i++)od.Vertices[i].Initialize(true,0);
    p.PartData=od;
    float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
    foreach(var g in od.Groups){mn[0]=Math.Min(mn[0],g.BoundsMin.x);mn[1]=Math.Min(mn[1],g.BoundsMin.y);mn[2]=Math.Min(mn[2],g.BoundsMin.z);mx[0]=Math.Max(mx[0],g.BoundsMax.x);mx[1]=Math.Max(mx[1],g.BoundsMax.y);mx[2]=Math.Max(mx[2],g.BoundsMax.z);}
    p.PartInfo.BoundMin=new RealVector4(mn[0],mn[1],mn[2],src.PartInfo.BoundMin.w);p.PartInfo.BoundMax=new RealVector4(mx[0],mx[1],mx[2],src.PartInfo.BoundMax.w);
    p.PartInfo.TriangleCount=idx.Count/3;p.PartInfo.Unk6_MW=idx.Count/3;
    if(idx.Count>65535)throw new Exception("still over 65535: "+idx.Count);
    return p;}
  public static void Main(string[] a){
    var f=Read(a[0]);var o=new RealGeometryFile();o.GeometryInfo=f.GeometryInfo;
    RealGeometryPart baseA=null;foreach(RealGeometryPart p in f)if(p.PartInfo.PartName.ToString()=="MUSTANGGT_BASE_A")baseA=p;
    if(baseA.PartData.Groups.Length!=6||baseA.PartInfo.Textures[baseA.PartData.Groups[4].TextureIndex0]!=0x5A006DE9u)throw new Exception("unexpected BASE_A layout");
    foreach(RealGeometryPart p in f){string n=p.PartInfo.PartName.ToString();RealGeometryPart c=p;
      if(n=="MUSTANGGT_BASE_A"){c=Sub(p,new[]{0,1,2,3});}
      else if(n=="MUSTANGGT_KIT00_RIGHT_SIDE_MIRROR_A"){var m=Sub(baseA,new[]{4});
        m.PartInfo.Hash=p.PartInfo.Hash;m.PartInfo.PartName=p.PartInfo.PartName;m.PartInfo.Transform=p.PartInfo.Transform;m.PartInfo.MountPoints=new RealMountPoint[0];c=m;}
      else{for(int i=0;i<c.PartData.Vertices.Length;i++)c.PartData.Vertices[i].Initialize(true,0);}
      o.AddPart(c);Console.WriteLine(string.Format("{0,-42} idx={1}",n,c.PartData.Indices.Length));}
    o.GeometryInfo.PartCount=o.PartCount;o.Save(a[1]);}
}
