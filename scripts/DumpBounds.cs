using System;
using System.IO;
using mwgc.RealEngine;
public class DumpBounds {
    public static void Main(string[] args) {
        byte[] bytes = File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        foreach (RealGeometryPart part in file) {
            string name = part.PartInfo.PartName.ToString();
            if (!name.Contains("TIRE") && !name.Contains("WHEEL")) continue;
            var bmin = part.PartInfo.BoundMin;
            var bmax = part.PartInfo.BoundMax;
            Console.WriteLine(name + " tris=" + part.PartData.TriangleCount
                + " x=(" + bmin.x.ToString("0.00") + "," + bmax.x.ToString("0.00") + ")"
                + " y=(" + bmin.y.ToString("0.00") + "," + bmax.y.ToString("0.00") + ")"
                + " z=(" + bmin.z.ToString("0.00") + "," + bmax.z.ToString("0.00") + ")");
        }
    }
}
