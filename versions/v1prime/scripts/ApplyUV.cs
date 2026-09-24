using System; using System.IO; using System.Text; using System.Collections.Generic; using mwgc.RealEngine;
// Replace vertex UVs of the listed solids (file from vinyluv.py: name, count, float2[count]).
public class ApplyUV { public static void Main(string[] a){
  var b=File.ReadAllBytes(a[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
  var f=new RealGeometryFile();f.Open(new MemoryStream(b));
  var map=new Dictionary<string,float[]>();
  using(var r=new BinaryReader(File.OpenRead(a[1]))){while(r.BaseStream.Position<r.BaseStream.Length){int l=r.ReadInt32();string n=Encoding.ASCII.GetString(r.ReadBytes(l));int c=r.ReadInt32();var uv=new float[c*2];for(int i=0;i<c*2;i++)uv[i]=r.ReadSingle();map[n]=uv;}}
  int parts=0;
  foreach(RealGeometryPart p in f){var d=p.PartData;for(int i=0;i<d.Vertices.Length;i++)d.Vertices[i].Initialize(true,0);
    float[] uv;if(map.TryGetValue(p.PartInfo.PartName.ToString(),out uv)){
      if(uv.Length!=d.Vertices.Length*2)throw new Exception("count mismatch "+p.PartInfo.PartName);
      for(int i=0;i<d.Vertices.Length;i++)d.Vertices[i].UV=new RealVector2(uv[2*i],uv[2*i+1]);parts++;}
    p.PartData=d;}
  f.Save(a[2]);Console.WriteLine("UV replaced in "+parts+" solids");}}
