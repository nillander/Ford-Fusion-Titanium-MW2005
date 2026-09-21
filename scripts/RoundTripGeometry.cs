using System;
using System.IO;
using mwgc.RealEngine;

// Diagnostic control: serialize a working donor without changing its meshes.
public class RoundTripGeometry {
    public static void Main(string[] args) {
        byte[] b = File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(b.Length - 8), 0, b, 4, 4);
        var f = new RealGeometryFile();
        f.Open(new MemoryStream(b));
        f.Save(args[1]);
        Console.WriteLine("Round-trip only: " + f.PartCount + " parts");
    }
}
