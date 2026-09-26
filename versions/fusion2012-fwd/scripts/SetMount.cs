using System; using System.IO; using System.Globalization; using mwgc.RealEngine;
// SetMount in.bin hashHex x y z out.bin : set translation of a mount point in every solid that has it.
public class SetMount { public static void Main(string[] a){
  var b=File.ReadAllBytes(a[0]);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
  var f=new RealGeometryFile();f.Open(new MemoryStream(b));
  uint h=uint.Parse(a[1],NumberStyles.HexNumber);var ci=CultureInfo.InvariantCulture;
  float x=float.Parse(a[2],ci),y=float.Parse(a[3],ci),z=float.Parse(a[4],ci);int n=0;
  foreach(RealGeometryPart p in f){var d=p.PartData;for(int i=0;i<d.Vertices.Length;i++)d.Vertices[i].Initialize(true,0);p.PartData=d;
    var m=p.PartInfo.MountPoints;if(m==null)continue;
    for(int i=0;i<m.Length;i++)if(m[i].Hash==h){m[i].Transform.m[12]=x;m[i].Transform.m[13]=y;m[i].Transform.m[14]=z;n++;}}
  f.Save(a[5]);Console.WriteLine("set "+n+" mount points");}}
