using System;
using System.IO;
using System.Collections.Generic;
using mwgc.RealEngine;

// v44: the plate is now one flat LICENSEPLATE surface.  Remove the separate
// dark/chrome plate surround (including its simplified LOD version) at both
// ends of either car; emblems above the plate remain outside this narrow box.
public class Plate44 {
  const uint MUSTANG_BLACK=0x5A006DE9, COBALT_BLACK=0xE67A0B4A;
  const uint MUSTANG_BADGING=0x339D0D44, COBALT_BADGING=0xEFC2BB05;
  const uint DULL=0x0FEDEE40, LICENSEPLATE=0x4C95C6F8;
  class G { public RealShadingGroup g; public List<RealVertex> v=new(); public List<int> i=new(); public uint tex,sh; }
  static RealGeometryFile Read(string p){var b=File.ReadAllBytes(p);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);var f=new RealGeometryFile();f.Open(new MemoryStream(b));return f;}
  static bool PlateBox(RealVector3 a,RealVector3 b,RealVector3 c){float x=(a.x+b.x+c.x)/3f,y=(a.y+b.y+c.y)/3f,z=(a.z+b.z+c.z)/3f;return Math.Abs(x)>2.00f&&Math.Abs(y)<.27f&&z>.28f&&z<.62f;}
  static bool Drop(uint tex,uint sh,RealVertex a,RealVertex b,RealVertex c){
    // BuildV1PrimeB mapped the physical frame to the upper-right BADGING atlas
    // cell (including the embossed MERCOSUL artwork).  The two white plate
    // quads map to the lower-left cell.  Split by UV, not by a spatial box:
    // the frame extends behind and beyond the edges of the white rectangle.
    if((tex==MUSTANG_BADGING||tex==COBALT_BADGING)&&sh==LICENSEPLATE){
      // A face has all three vertices in the lower-left atlas cell.  Require
      // every vertex there, so edge triangles on the separate frame cannot
      // survive simply because their UV centroid crossed a cell boundary.
      return !(a.UV.u<.5f&&b.UV.u<.5f&&c.UV.u<.5f&&
               a.UV.v>.5f&&b.UV.v>.5f&&c.UV.v>.5f);
    }
    if(!PlateBox(a.Position,b.Position,c.Position))return false;
    return tex==MUSTANG_BLACK||tex==COBALT_BLACK||((tex==MUSTANG_BADGING||tex==COBALT_BADGING)&&sh==DULL);
  }
  static RealGeometryPart Rebuild(RealGeometryPart t,out int removed){removed=0;var d=t.PartData;var gs=new List<G>();foreach(var src in d.Groups){var x=new G{g=src,tex=t.PartInfo.Textures[src.TextureIndex0],sh=t.PartInfo.Shaders[src.ShaderIndex0]};var map=new Dictionary<int,int>();for(int q=src.Offset;q<src.Offset+src.Length;q+=3){int a=d.Indices[q],b=d.Indices[q+1],c=d.Indices[q+2];if(Drop(x.tex,x.sh,d.Vertices[a],d.Vertices[b],d.Vertices[c])){removed++;continue;}foreach(int original in new[]{a,b,c}){if(!map.TryGetValue(original,out int local)){local=x.v.Count;x.v.Add(d.Vertices[original]);map[original]=local;}x.i.Add(local);}}if(x.i.Count>0)gs.Add(x);}var vv=new List<RealVertex>();var ii=new List<ushort>();var og=new List<RealShadingGroup>();var tt=new List<uint>();var ss=new List<uint>();foreach(var x in gs){int baseVertex=vv.Count,offset=ii.Count;vv.AddRange(x.v);foreach(int n in x.i)ii.Add((ushort)(baseVertex+n));int ti=tt.IndexOf(x.tex);if(ti<0){ti=tt.Count;tt.Add(x.tex);}int si=ss.IndexOf(x.sh);if(si<0){si=ss.Count;ss.Add(x.sh);}var g=x.g;g.Offset=offset;g.Length=x.i.Count;g.TriangleCount=x.i.Count/3;g.VertexCount=x.v.Count;g.TextureIndex0=g.TextureIndex1=g.TextureIndex2=g.TextureIndex3=g.TextureIndex4=(byte)ti;g.ShaderIndex0=(byte)si;og.Add(g);}var o=new RealGeometryPart();o.PartInfo=t.PartInfo;o.PartInfo.Textures=tt.ToArray();o.PartInfo.Shaders=ss.ToArray();o.PartInfo.TextureCount=(byte)tt.Count;o.PartInfo.ShaderCount=(byte)ss.Count;var od=t.PartData;od.Vertices=vv.ToArray();for(int i=0;i<od.Vertices.Length;i++)od.Vertices[i].Initialize(true,0);od.Indices=ii.ToArray();od.Groups=og.ToArray();od.GroupCount=og.Count;od.IndexCount=ii.Count;od.Materials=null;o.PartData=od;o.PartInfo.TriangleCount=ii.Count/3;o.PartInfo.Unk6_MW=ii.Count/3;return o;}
  public static void Main(string[] a){var f=Read(a[0]);var o=new RealGeometryFile();o.GeometryInfo=f.GeometryInfo;int total=0;foreach(RealGeometryPart p in f){var q=Rebuild(p,out int n);if(n>0)Console.WriteLine($"{p.PartInfo.PartName}: removed {n} plate-surround triangles");total+=n;o.AddPart(q);}o.GeometryInfo.PartCount=o.PartCount;o.Save(a[1]);Console.WriteLine($"total removed: {total}");}
}
