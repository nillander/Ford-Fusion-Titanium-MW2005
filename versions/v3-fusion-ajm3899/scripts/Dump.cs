using System; using System.IO; using System.Text; using System.Globalization; using mwgc.RealEngine;
// Dump GEOMETRY.BIN to a simple binary for python: see dumpfmt in geo.py
public class Dump { public static void Main(string[] args){
 var b=File.ReadAllBytes(args[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
 var f=new RealGeometryFile();f.Open(new MemoryStream(b));
 using(var w=new BinaryWriter(File.Create(args[1]))){
  w.Write(f.PartCount);
  foreach(RealGeometryPart p in f){var i=p.PartInfo;var d=p.PartData;
   var nm=Encoding.ASCII.GetBytes(i.PartName.ToString());w.Write(nm.Length);w.Write(nm);
   w.Write(i.Hash);
   foreach(var v in new[]{i.BoundMin.x,i.BoundMin.y,i.BoundMin.z,i.BoundMax.x,i.BoundMax.y,i.BoundMax.z})w.Write(v);
   var tx=i.Textures??new uint[0];w.Write(tx.Length);foreach(var t in tx)w.Write(t);
   var sh=i.Shaders??new uint[0];w.Write(sh.Length);foreach(var t in sh)w.Write(t);
   w.Write(d.Flags);
   w.Write(d.Groups.Length);
   foreach(var g in d.Groups){w.Write(g.TextureIndex0);w.Write(g.TextureIndex1);w.Write(g.TextureIndex2);w.Write(g.TextureIndex3);w.Write(g.TextureIndex4);w.Write(g.ShaderIndex0);
     w.Write(g.Flags);w.Write(g.VertexCount);w.Write(g.TriangleCount);w.Write(g.Offset);w.Write(g.Length);w.Write(g.Unk1);}
   w.Write(d.Vertices.Length);
   foreach(var v in d.Vertices){w.Write(v.Position.x);w.Write(v.Position.y);w.Write(v.Position.z);w.Write(v.Normal.x);w.Write(v.Normal.y);w.Write(v.Normal.z);w.Write(v.Diffuse);w.Write(v.UV.u);w.Write(v.UV.v);}
   w.Write(d.Indices.Length);foreach(var x in d.Indices)w.Write(x);
  }}
 Console.WriteLine("dumped "+f.PartCount);
}}
