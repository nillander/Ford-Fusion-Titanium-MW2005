using System;
using System.IO;
using mwgc.RealEngine;
public class DumpPartShaders {
    public static void Main(string[] args) {
        byte[] bytes = File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        foreach (RealGeometryPart part in file) {
            string name = part.PartInfo.PartName.ToString();
            if (args.Length > 1) {
                bool hit = false;
                for (int i = 1; i < args.Length; i++) if (name.IndexOf(args[i], StringComparison.OrdinalIgnoreCase) >= 0) hit = true;
                if (!hit) continue;
            }
            string shaders = part.PartInfo.Shaders == null ? "-" : string.Join(",", Array.ConvertAll(part.PartInfo.Shaders, x => "0x" + x.ToString("X8")));
            string textures = part.PartInfo.Textures == null ? "-" : string.Join(",", Array.ConvertAll(part.PartInfo.Textures, x => "0x" + x.ToString("X8")));
            Console.WriteLine(name + " tris=" + part.PartData.TriangleCount + " verts=" + part.PartData.VertexCount + " sh=[" + shaders + "] tx=[" + textures + "]");
        }
    }
}
