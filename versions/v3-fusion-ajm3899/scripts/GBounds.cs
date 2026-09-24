using System; using System.IO; using mwgc.RealEngine;
public class GBounds { public static void Main(string[] args){
 var b=File.ReadAllBytes(args[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
 var f=new RealGeometryFile();f.Open(new MemoryStream(b));
 foreach(RealGeometryPart p in f){var d=p.PartData; if(!p.PartInfo.PartName.ToString().EndsWith(args.Length>1?args[1]:"_A"))continue;
  int vb=0;
  for(int gi=0;gi<d.Groups.Length;gi++){var g=d.Groups[gi];
   float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
   for(int i=g.Offset;i<g.Offset+g.Length;i++){var v=d.Vertices[d.Indices[i]].Position;mn[0]=Math.Min(mn[0],v.x);mn[1]=Math.Min(mn[1],v.y);mn[2]=Math.Min(mn[2],v.z);mx[0]=Math.Max(mx[0],v.x);mx[1]=Math.Max(mx[1],v.y);mx[2]=Math.Max(mx[2],v.z);}
   Console.WriteLine(string.Format("{0} g{1} stored=({2:F2},{3:F2},{4:F2})-({5:F2},{6:F2},{7:F2}) actual=({8:F2},{9:F2},{10:F2})-({11:F2},{12:F2},{13:F2}) n1-5={14},{15},{16},{17},{18}",
    p.PartInfo.PartName,gi,g.BoundsMin.x,g.BoundsMin.y,g.BoundsMin.z,g.BoundsMax.x,g.BoundsMax.y,g.BoundsMax.z,mn[0],mn[1],mn[2],mx[0],mx[1],mx[2],g.Null1,g.Null2,g.Null3,g.Null4,g.Null5));
  }}}}
