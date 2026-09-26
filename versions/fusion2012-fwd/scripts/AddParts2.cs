using System; using System.IO; using System.Text; using System.Collections.Generic; using mwgc.RealEngine;
// AddParts in.bin spec.bin out.bin
// spec: repeated parts: name, templateName, nTex, uint[], nSh, uint[], nGroups,
//   per group: texIdx, shIdx, flags, unk1, nV, (pos3 n3 uv2 diffuse:uint)[nV], nI, int[nI] (local)
// A part with an existing name is replaced; otherwise it is appended.
public class AddParts2 {
  static uint BinHash(string s){uint h=0xFFFFFFFF;foreach(char c in s)h=h*33+(byte)c;return h;}
  static string Str(BinaryReader r){int l=r.ReadInt32();return Encoding.ASCII.GetString(r.ReadBytes(l));}
  public static void Main(string[] a){
    var b=File.ReadAllBytes(a[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
    var f=new RealGeometryFile();f.Open(new MemoryStream(b));
    var byName=new Dictionary<string,RealGeometryPart>();var order=new List<RealGeometryPart>();
    foreach(RealGeometryPart p in f){var d=p.PartData;for(int i=0;i<d.Vertices.Length;i++)d.Vertices[i].Initialize(true,0);p.PartData=d;byName[p.PartInfo.PartName.ToString()]=p;order.Add(p);}
    using(var r=new BinaryReader(File.OpenRead(a[1]))){while(r.BaseStream.Position<r.BaseStream.Length){
      string name=Str(r),tname=Str(r);var T=byName[tname];
      int nt=r.ReadInt32();var tex=new uint[nt];for(int k=0;k<nt;k++)tex[k]=r.ReadUInt32();
      int ns=r.ReadInt32();var sh=new uint[ns];for(int k=0;k<ns;k++)sh[k]=r.ReadUInt32();
      int ng=r.ReadInt32();var verts=new List<RealVertex>();var idx=new List<ushort>();var groups=new List<RealShadingGroup>();
      float[] MN={1e9f,1e9f,1e9f},MX={-1e9f,-1e9f,-1e9f};var tv=T.PartData.Vertices[0];
      for(int g=0;g<ng;g++){var G=T.PartData.Groups[0];
        G.TextureIndex0=G.TextureIndex1=G.TextureIndex2=G.TextureIndex3=G.TextureIndex4=(byte)r.ReadInt32();G.ShaderIndex0=(byte)r.ReadInt32();
        G.Flags=r.ReadInt32();G.Unk1=r.ReadInt32();int nv=r.ReadInt32();int vb=verts.Count;
        float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
        for(int k=0;k<nv;k++){var v=tv;v.Position=new RealVector3(r.ReadSingle(),r.ReadSingle(),r.ReadSingle());v.Normal=new RealVector3(r.ReadSingle(),r.ReadSingle(),r.ReadSingle());v.UV=new RealVector2(r.ReadSingle(),r.ReadSingle());v.Diffuse=r.ReadInt32();verts.Add(v);
          var P=v.Position;mn[0]=Math.Min(mn[0],P.x);mn[1]=Math.Min(mn[1],P.y);mn[2]=Math.Min(mn[2],P.z);mx[0]=Math.Max(mx[0],P.x);mx[1]=Math.Max(mx[1],P.y);mx[2]=Math.Max(mx[2],P.z);}
        int ni=r.ReadInt32();int off=idx.Count;for(int k=0;k<ni;k++)idx.Add((ushort)(vb+r.ReadInt32()));
        G.Offset=off;G.Length=ni;G.TriangleCount=ni/3;G.VertexCount=nv;G.BoundsMin=new RealVector3(mn[0],mn[1],mn[2]);G.BoundsMax=new RealVector3(mx[0],mx[1],mx[2]);
        for(int k=0;k<3;k++){MN[k]=Math.Min(MN[k],mn[k]);MX[k]=Math.Max(MX[k],mx[k]);}groups.Add(G);}
      if(verts.Count>65535)throw new Exception("vertex limit "+name);
      var p=new RealGeometryPart();var info=T.PartInfo;info.PartName=new FixedLenString(name);info.Hash=BinHash(name);
      info.Textures=tex;info.Shaders=sh;info.TextureCount=(byte)nt;info.ShaderCount=(byte)ns;if(name!=tname)info.MountPoints=null;
      info.BoundMin=new RealVector4(MN[0],MN[1],MN[2],T.PartInfo.BoundMin.w);info.BoundMax=new RealVector4(MX[0],MX[1],MX[2],T.PartInfo.BoundMax.w);
      info.TriangleCount=idx.Count/3;info.Unk5_MW=1;info.Unk6_MW=idx.Count/3;
      var d=T.PartData;d.Vertices=verts.ToArray();for(int k=0;k<d.Vertices.Length;k++)d.Vertices[k].Initialize(true,0);
      d.Indices=idx.ToArray();d.Groups=groups.ToArray();d.GroupCount=groups.Count;d.IndexCount=idx.Count;d.Materials=null;
      p.PartInfo=info;p.PartData=d;
      int at=order.FindIndex(x=>x.PartInfo.PartName.ToString()==name);if(at>=0)order[at]=p;else order.Add(p);byName[name]=p;
      Console.WriteLine((at>=0?"replaced ":"added ")+name+" hash "+info.Hash.ToString("X8")+" tris "+idx.Count/3+" verts "+verts.Count+" groups "+ng);}}
    var o=new RealGeometryFile();o.GeometryInfo=f.GeometryInfo;foreach(var p in order)o.AddPart(p);o.GeometryInfo.PartCount=o.PartCount;o.Save(a[2]);}}
