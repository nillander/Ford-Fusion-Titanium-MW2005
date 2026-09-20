using System;
using System.IO;
using mwgc.RealEngine;

public class DumpNamesRaw {
    public static void Main(string[] args) {
        byte[] bytes = File.ReadAllBytes(args[0]);
        bool nest = args.Length > 1 && args[1] == "nest";
        if (nest) Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        Console.WriteLine("parts=" + file.PartCount);
        foreach (RealGeometryPart part in file) {
            string shaders = part.PartInfo.Shaders == null ? "-" : string.Join(",", Array.ConvertAll(part.PartInfo.Shaders, x => "0x" + x.ToString("X8")));
            string textures = part.PartInfo.Textures == null ? "-" : string.Join(",", Array.ConvertAll(part.PartInfo.Textures, x => "0x" + x.ToString("X8")));
            Console.WriteLine(part.PartInfo.PartName + " tris=" + part.PartData.TriangleCount + " verts=" + part.PartData.VertexCount + " sh=[" + shaders + "] tx=[" + textures + "]");
        }
    }
}
