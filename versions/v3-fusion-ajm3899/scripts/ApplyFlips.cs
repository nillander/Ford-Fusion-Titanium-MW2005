using System; using System.IO; using System.Collections.Generic; using mwgc.RealEngine;
// Reverse winding of listed triangles (part name + index offset of the triangle).
public class ApplyFlips { public static void Main(string[] args){
 var b=File.ReadAllBytes(args[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
 var f=new RealGeometryFile();f.Open(new MemoryStream(b));
 var map=new Dictionary<string,List<int>>();
 foreach(var line in File.ReadAllLines(args[1])){var t=line.Trim().Split(' ');if(t.Length<2)continue;if(!map.ContainsKey(t[0]))map[t[0]]=new List<int>();map[t[0]].Add(int.Parse(t[1]));}
 int n=0;
 foreach(RealGeometryPart p in f){var d=p.PartData;for(int i=0;i<d.Vertices.Length;i++)d.Vertices[i].Initialize(true,0);
  List<int> l; if(!map.TryGetValue(p.PartInfo.PartName.ToString(),out l))continue;
  foreach(int o in l){var x=d.Indices[o+1];d.Indices[o+1]=d.Indices[o+2];d.Indices[o+2]=x;n++;}}
 f.Save(args[2]);Console.WriteLine("Flipped triangles: "+n);
}}
