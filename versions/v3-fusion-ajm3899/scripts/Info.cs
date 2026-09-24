using System; using System.IO; using mwgc.RealEngine;
public class Info { public static void Main(string[] args){
 var b=File.ReadAllBytes(args[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
 var f=new RealGeometryFile();f.Open(new MemoryStream(b));
 var gi=f.GeometryInfo; Console.WriteLine("GI unk1="+gi.Unk1+" parts="+gi.PartCount+" path="+gi.RelFilePath+" class="+gi.ClassType+" ext="+gi.ExtChunkOffs+"/"+gi.ExtChunkLen+" unk2="+gi.Unk2);
 foreach(RealGeometryPart p in f){var i=p.PartInfo;var d=p.PartData;
  Console.WriteLine(i.PartName+" h="+i.Hash.ToString("X8")+" unk1="+i.Unk1.ToString("X")+" tri="+i.TriangleCount+" u2="+i.Unk2.ToString("X")+" u3="+i.Unk3.ToString("X")+" u4="+i.Unk4_MW+" u5="+i.Unk5_MW+" u6="+i.Unk6_MW+" dflags="+d.Flags.ToString("X")+" dunk1="+d.Unk1+" vb="+d.VBCount+" mats="+(d.Materials==null?0:d.Materials.Count)+" mp="+(i.MountPoints==null?0:i.MountPoints.Length));
  if(i.MountPoints!=null)foreach(var m in i.MountPoints)Console.WriteLine("   MP "+m.Hash.ToString("X8")+" pos=("+m.Transform.m[12].ToString("F3")+","+m.Transform.m[13].ToString("F3")+","+m.Transform.m[14].ToString("F3")+")");
  foreach(var g in d.Groups)Console.WriteLine("   G flags="+g.Flags.ToString("X")+" unk1="+g.Unk1+" tex="+g.TextureIndex0+","+g.TextureIndex1+","+g.TextureIndex2+","+g.TextureIndex3+","+g.TextureIndex4+" sh="+g.ShaderIndex0+" v="+g.VertexCount+" t="+g.TriangleCount+" off="+g.Offset+" len="+g.Length);
  if(d.Materials!=null)foreach(var m in d.Materials)Console.WriteLine("   MAT "+m);
 }}}
