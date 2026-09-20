using System;
using System.IO;
using mwgc.RealEngine;

public class DumpWindowShaders {
    public static void Main(string[] args) {
        byte[] bytes = File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        Console.WriteLine("file=" + args[0]);
        foreach (RealGeometryPart part in file) {
            string name = part.PartInfo.PartName.ToString();
            if (!name.Contains("WINDOW")) continue;
            string shaders = part.PartInfo.Shaders == null ? "-" : string.Join(",", Array.ConvertAll(part.PartInfo.Shaders, x => "0x" + x.ToString("X8")));
            string textures = part.PartInfo.Textures == null ? "-" : string.Join(",", Array.ConvertAll(part.PartInfo.Textures, x => "0x" + x.ToString("X8")));
            Console.WriteLine(name + " tris=" + part.PartData.TriangleCount + " verts=" + part.PartData.VertexCount + " sh=[" + shaders + "] tx=[" + textures + "]");
        }
    }
}
