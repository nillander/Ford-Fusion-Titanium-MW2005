using System;
using System.IO;
using mwgc.RealEngine;

public class ProbeFrontGrille {
    public static void Main(string[] args) {
        byte[] bytes = File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        foreach (RealGeometryPart part in file) {
            string name = part.PartInfo.PartName.ToString();
            if (!name.Contains("BASE_A") && !name.Contains("BODY_A") && !name.Contains("HEADLIGHT") && !name.Contains("BRAKELIGHT")) continue;
            int front = 0;
            var verts = part.PartData.Vertices;
            var indices = part.PartData.Indices;
            for (int index = 0; index + 2 < indices.Length; index += 3) {
                var a = verts[indices[index]].Position;
                var b = verts[indices[index + 1]].Position;
                var c = verts[indices[index + 2]].Position;
                float cx = (a.x + b.x + c.x) / 3;
                float cy = (a.y + b.y + c.y) / 3;
                float cz = (a.z + b.z + c.z) / 3;
                if (cx > 2.05f && Math.Abs(cy) < 0.70f && cz < 0.75f) front++;
            }
            Console.WriteLine(name + " tris=" + part.PartData.TriangleCount + " front_cavity=" + front
                + " xmin=" + part.PartInfo.BoundMin.x.ToString("0.00")
                + " xmax=" + part.PartInfo.BoundMax.x.ToString("0.00")
                + " zmin=" + part.PartInfo.BoundMin.z.ToString("0.00")
                + " zmax=" + part.PartInfo.BoundMax.z.ToString("0.00"));
        }
    }
}
