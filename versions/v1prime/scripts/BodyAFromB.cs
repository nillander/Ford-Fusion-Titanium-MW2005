using System; using System.IO; using mwgc.RealEngine;
// Test: every LOD-A solid above 65,535 indices takes the content of its LOD B.
public class BodyAFromB { public static void Main(string[] a){
  var b=File.ReadAllBytes(a[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
  var f=new RealGeometryFile();f.Open(new MemoryStream(b));
  var byName=new System.Collections.Generic.Dictionary<string,RealGeometryPart>();foreach(RealGeometryPart p in f)byName[p.PartInfo.PartName.ToString()]=p;
  var o=new RealGeometryFile();o.GeometryInfo=f.GeometryInfo;
  foreach(RealGeometryPart p0 in f){var p=p0;
    string nm=p.PartInfo.PartName.ToString();if(p.PartData.Indices.Length>65535&&nm.EndsWith("_A")&&byName.ContainsKey(nm.Substring(0,nm.Length-1)+"B")){var B=byName[nm.Substring(0,nm.Length-1)+"B"];Console.WriteLine(nm+" <- B");var n=new RealGeometryPart();n.PartInfo=B.PartInfo;n.PartData=B.PartData;
      n.PartInfo.Hash=p.PartInfo.Hash;n.PartInfo.PartName=p.PartInfo.PartName;n.PartInfo.MountPoints=p.PartInfo.MountPoints;p=n;}
    for(int i=0;i<p.PartData.Vertices.Length;i++)p.PartData.Vertices[i].Initialize(true,0);
    o.AddPart(p);}
  o.GeometryInfo.PartCount=o.PartCount;o.Save(a[1]);}}
