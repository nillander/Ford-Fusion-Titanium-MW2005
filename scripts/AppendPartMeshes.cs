using System;
using System.Collections.Generic;
using System.IO;
using mwgc.RealEngine;

public class AppendPartMeshes {
    static RealGeometryFile Read(string path) {
        byte[] bytes = File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        return file;
    }

    static void ExpandBounds(ref RealVector4 minimum, ref RealVector4 maximum, RealVector4 extraMin, RealVector4 extraMax) {
        if (extraMin.x < minimum.x) minimum.x = extraMin.x;
        if (extraMin.y < minimum.y) minimum.y = extraMin.y;
        if (extraMin.z < minimum.z) minimum.z = extraMin.z;
        if (extraMax.x > maximum.x) maximum.x = extraMax.x;
        if (extraMax.y > maximum.y) maximum.y = extraMax.y;
        if (extraMax.z > maximum.z) maximum.z = extraMax.z;
    }

    static int IndexOf(uint[] values, uint hash) {
        if (values == null) return -1;
        for (int index = 0; index < values.Length; index++) {
            if (values[index] == hash) return index;
        }
        return -1;
    }

    static uint[] AppendUnique(uint[] values, uint[] extra, out int[] remap) {
        var list = new List<uint>();
        if (values != null) list.AddRange(values);
        remap = extra == null ? new int[0] : new int[extra.Length];
        if (extra == null) return list.ToArray();
        for (int index = 0; index < extra.Length; index++) {
            int found = list.IndexOf(extra[index]);
            if (found < 0) {
                found = list.Count;
                list.Add(extra[index]);
            }
            remap[index] = found;
        }
        return list.ToArray();
    }

    static RealGeometryPart Append(RealGeometryPart original, RealGeometryPart extra) {
        int[] textureRemap;
        int[] shaderRemap;
        original.PartInfo.Textures = AppendUnique(original.PartInfo.Textures, extra.PartInfo.Textures, out textureRemap);
        original.PartInfo.Shaders = AppendUnique(original.PartInfo.Shaders, extra.PartInfo.Shaders, out shaderRemap);
        original.PartInfo.TextureCount = (byte)original.PartInfo.Textures.Length;
        original.PartInfo.ShaderCount = (byte)original.PartInfo.Shaders.Length;

        var vertices = new List<RealVertex>(original.PartData.Vertices);
        int vertexOffset = original.PartData.Vertices.Length;
        for (int index = 0; index < extra.PartData.Vertices.Length; index++) {
            RealVertex vertex = extra.PartData.Vertices[index];
            vertex.Initialize(true, 0);
            vertices.Add(vertex);
        }
        var indices = new List<ushort>(original.PartData.Indices);
        for (int index = 0; index < extra.PartData.Indices.Length; index++) {
            indices.Add((ushort)(extra.PartData.Indices[index] + vertexOffset));
        }
        var groups = new List<RealShadingGroup>(original.PartData.Groups);
        foreach (RealShadingGroup group in extra.PartData.Groups) {
            RealShadingGroup copy = group;
            copy.Offset = group.Offset + original.PartData.IndexCount;
            if (group.TextureIndex0 < textureRemap.Length) {
                byte mapped = (byte)textureRemap[group.TextureIndex0];
                copy.TextureIndex0 = mapped;
                copy.TextureIndex1 = mapped;
                copy.TextureIndex2 = mapped;
                copy.TextureIndex3 = mapped;
                copy.TextureIndex4 = mapped;
            }
            if (group.ShaderIndex0 < shaderRemap.Length) {
                copy.ShaderIndex0 = (byte)shaderRemap[group.ShaderIndex0];
            }
            groups.Add(copy);
        }
        original.PartData.Vertices = vertices.ToArray();
        original.PartData.Indices = indices.ToArray();
        original.PartData.Groups = groups.ToArray();
        original.PartData.GroupCount = groups.Count;
        original.PartData.IndexCount = indices.Count;
        original.PartInfo.TriangleCount = indices.Count / 3;
        original.PartInfo.Unk6_MW = original.PartInfo.TriangleCount;
        ExpandBounds(ref original.PartInfo.BoundMin, ref original.PartInfo.BoundMax, extra.PartInfo.BoundMin, extra.PartInfo.BoundMax);
        return original;
    }

    public static void Main(string[] args) {
        var donor = Read(args[0]);
        var extra = Read(args[1]);
        var result = new RealGeometryFile();
        result.GeometryInfo = donor.GeometryInfo;
        int appended = 0;
        int kept = 0;
        foreach (RealGeometryPart original in donor) {
            RealGeometryPart addition = extra[original.PartInfo.Hash];
            RealGeometryPart chosen = original;
            if (addition != null) {
                chosen = Append(original, addition);
                appended++;
            } else {
                kept++;
            }
            for (int index = 0; index < chosen.PartData.Vertices.Length; index++) {
                chosen.PartData.Vertices[index].Initialize(true, 0);
            }
            result.AddPart(chosen);
        }
        result.GeometryInfo.PartCount = result.PartCount;
        result.Save(args[2]);
        Console.WriteLine("Appended=" + appended + " retained=" + kept + " total=" + result.PartCount);
    }
}
