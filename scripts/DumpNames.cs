using System;
using System.IO;
using mwgc.RealEngine;

public class DumpNames {
    public static void Main(string[] args) {
        byte[] bytes = File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        Console.WriteLine("parts=" + file.PartCount);
        foreach (RealGeometryPart part in file) {
            Console.WriteLine(part.PartInfo.PartName + " tris=" + part.PartData.TriangleCount + " verts=" + part.PartData.VertexCount);
        }
    }
}
