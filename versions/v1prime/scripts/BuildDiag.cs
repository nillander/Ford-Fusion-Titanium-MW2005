using System; using System.IO; using System.Collections.Generic; using mwgc.RealEngine;
// Diagnostic from v1prime-b: recolour the grille groups (first groups of RIGHT_SIDE_MIRROR_A)
// with solid BADGING patches and add a forward-shifted magenta copy of the bars as the first
// group of BASE_A.  red = bars in RIGHT_SIDE_MIRROR_A, green = back panel there,
// magenta = copy of the bars in BASE_A (+5 mm).
public class BuildDiag {
  const uint BADGING=0x339D0D44, DULL=0x0FEDEE40;
  static RealGeometryFile Read(string p){var b=File.ReadAllBytes(p);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);var f=new RealGeometryFile();f.Open(new MemoryStream(b));return f;}
  static int AddTex(ref RealGeometryPart p,uint h,bool shader){var l=new List<uint>(shader?p.PartInfo.Shaders:p.PartInfo.Textures);int i=l.IndexOf(h);if(i<0){l.Add(h);i=l.Count-1;}
    if(shader){p.PartInfo.Shaders=l.ToArray();p.PartInfo.ShaderCount=(byte)l.Count;}else{p.PartInfo.Textures=l.ToArray();p.PartInfo.TextureCount=(byte)l.Count;}return i;}
  static void Recolor(RealGeometryPart p,int gi,float u,float v,int ti,int si){var d=p.PartData;int s=0;for(int g=0;g<gi;g++)s+=d.Groups[g].VertexCount;
    var gr=d.Groups[gi];for(int k=s;k<s+gr.VertexCount;k++)d.Vertices[k].UV=new RealVector2(u,v);
    gr.TextureIndex0=gr.TextureIndex1=gr.TextureIndex2=gr.TextureIndex3=gr.TextureIndex4=(byte)ti;gr.ShaderIndex0=(byte)si;d.Groups[gi]=gr;p.PartData=d;}
  public static void Main(string[] a){
    var f=Read(a[0]);var o=new RealGeometryFile();o.GeometryInfo=f.GeometryInfo;
    RealGeometryPart mir=null;foreach(RealGeometryPart p in f)if(p.PartInfo.PartName.ToString()=="MUSTANGGT_KIT00_RIGHT_SIDE_MIRROR_A")mir=p;
    // groups 0 (bars, MISC) and 1 (back, LOGO) were placed first by BuildV1PrimeB
    if(mir.PartInfo.Textures[mir.PartData.Groups[0].TextureIndex0]!=0x5A00E244u||mir.PartInfo.Textures[mir.PartData.Groups[1].TextureIndex0]!=0x5A006DE9u)throw new Exception("layout");
    // copy of bars for BASE_A
    var md=mir.PartData;var bars=new List<RealVertex>();for(int k=0;k<md.Groups[0].VertexCount;k++){var v=md.Vertices[k];var P=v.Position;P.x+=0.005f;v.Position=P;v.UV=new RealVector2(0.8125f,0.5625f);bars.Add(v);}
    var barIdx=new List<ushort>();for(int q=md.Groups[0].Offset;q<md.Groups[0].Offset+md.Groups[0].Length;q++)barIdx.Add(md.Indices[q]);
    var barGroup=md.Groups[0];
    {int ti=AddTex(ref mir,BADGING,false),si=AddTex(ref mir,DULL,true);Recolor(mir,0,0.5625f,0.5625f,ti,si);Recolor(mir,1,0.6875f,0.5625f,ti,si);}
    foreach(RealGeometryPart p0 in f){var p=p0;string n=p.PartInfo.PartName.ToString();
      if(n=="MUSTANGGT_BASE_A"){var d=p.PartData;int ti=AddTex(ref p,BADGING,false),si=AddTex(ref p,DULL,true);
        var verts=new List<RealVertex>(bars);verts.AddRange(d.Vertices);int vb=bars.Count;
        var idx=new List<ushort>(barIdx);foreach(var x in d.Indices)idx.Add((ushort)(x+vb));
        var gs=new List<RealShadingGroup>();var g0=barGroup;g0.Offset=0;g0.TextureIndex0=g0.TextureIndex1=g0.TextureIndex2=g0.TextureIndex3=g0.TextureIndex4=(byte)ti;g0.ShaderIndex0=(byte)si;gs.Add(g0);
        foreach(var g in d.Groups){var h=g;h.Offset+=barIdx.Count;gs.Add(h);}
        d.Vertices=verts.ToArray();d.Indices=idx.ToArray();d.Groups=gs.ToArray();d.GroupCount=gs.Count;d.IndexCount=idx.Count;p.PartData=d;
        p.PartInfo.TriangleCount=idx.Count/3;p.PartInfo.Unk6_MW=idx.Count/3;if(idx.Count>65535)throw new Exception("over");}
      for(int k=0;k<p.PartData.Vertices.Length;k++)p.PartData.Vertices[k].Initialize(true,0);
      o.AddPart(p);}
    o.GeometryInfo.PartCount=o.PartCount;o.Save(a[1]);Console.WriteLine("diag written; bar tris "+barIdx.Count/3);
  }
}
