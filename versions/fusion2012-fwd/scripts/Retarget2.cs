using System; using System.IO; using System.Collections.Generic; using System.Globalization; using mwgc.RealEngine;
// Retarget2 in.bin out.bin SRC DST texmap.txt : rename solids SRC_* -> DST_* (new hashes) and remap texture hashes
public class Retarget2 {
  static uint H(string s){uint h=0xFFFFFFFF;foreach(char c in s){h*=33;h+=(uint)c;}return h;}
  public static void Main(string[] a){
    var b=File.ReadAllBytes(a[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
    var f=new RealGeometryFile();f.Open(new MemoryStream(b));
    var map=new Dictionary<uint,uint>();
    foreach(var line in File.ReadAllLines(a[4])){var t=line.Split(' ',StringSplitOptions.RemoveEmptyEntries);if(t.Length<2)continue;map[uint.Parse(t[0],NumberStyles.HexNumber)]=uint.Parse(t[1],NumberStyles.HexNumber);}
    int n=0,tx=0;
    foreach(RealGeometryPart p in f){var d=p.PartData;for(int i=0;i<d.Vertices.Length;i++)d.Vertices[i].Initialize(true,0);p.PartData=d;
      var info=p.PartInfo;string name=info.PartName.ToString();
      if(name.StartsWith(a[2]+"_")){string nn=a[3]+name.Substring(a[2].Length);info.PartName=new FixedLenString(nn);info.Hash=H(nn);n++;}
      if(info.Textures!=null)for(int i=0;i<info.Textures.Length;i++)if(map.ContainsKey(info.Textures[i])){info.Textures[i]=map[info.Textures[i]];tx++;}
      p.PartInfo=info;}
    f.GeometryInfo.PartCount=f.PartCount;f.Save(a[1]);Console.WriteLine("retargeted "+n+" solids, "+tx+" texture refs");}}
