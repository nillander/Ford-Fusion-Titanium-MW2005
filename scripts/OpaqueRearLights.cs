using System;
using System.Collections.Generic;
using System.IO;
using mwgc.RealEngine;

// Patch only rear lamp materials; all geometry and other car parts survive.
public class OpaqueRearLights {
    // The Shelby lens is a thin, partially open shell.  MW consequently lets
    // the cabin show through it.  Add a closed, opaque reflector volume behind
    // each full-detail tail lamp.  It remains in the lamp's own part so the
    // existing LOD/catalogue layout is preserved.
    static void AddReflectorBacking(RealGeometryPart p) {
        RealVector4 bmin = p.PartInfo.BoundMin;
        RealVector4 bmax = p.PartInfo.BoundMax;
        float x0 = bmax.x - 0.055f;
        float x1 = bmax.x + 0.004f;
        float y0 = bmin.y - 0.006f, y1 = bmax.y + 0.006f;
        float z0 = bmin.z - 0.006f, z1 = bmax.z + 0.006f;
        float[,] points = new float[,] {
            {x0,y0,z0},{x1,y0,z0},{x1,y1,z0},{x0,y1,z0},
            {x0,y0,z1},{x1,y0,z1},{x1,y1,z1},{x0,y1,z1}
        };
        int[,] faces = new int[,] {
            {0,2,1},{0,3,2},{4,5,6},{4,6,7},{0,1,5},{0,5,4},
            {3,6,2},{3,7,6},{0,4,7},{0,7,3},{1,2,6},{1,6,5}
        };
        var vertices = new List<RealVertex>(p.PartData.Vertices);
        ushort first = (ushort)vertices.Count;
        for (int i = 0; i < 8; i++) {
            var v = new RealVertex(); v.Initialize(true, 0);
            v.Position.x = points[i,0]; v.Position.y = points[i,1]; v.Position.z = points[i,2];
            // Opaque red diffuse: remains visible even if the donor atlas has
            // an unexpected transparent pixel at its sampled UV.
            v.Diffuse = unchecked((int)0xFF3030D0);
            v.UV.u = (i == 1 || i == 2 || i == 5 || i == 6) ? 0.5f : 0.25f;
            v.UV.v = (i >= 4) ? 0.5f : 0.25f;
            vertices.Add(v);
        }
        var indices = new List<ushort>(p.PartData.Indices);
        int offset = indices.Count;
        for (int i = 0; i < 12; i++) {
            indices.Add((ushort)(first + faces[i,0]));
            indices.Add((ushort)(first + faces[i,1]));
            indices.Add((ushort)(first + faces[i,2]));
        }
        RealShadingGroup group = p.PartData.Groups[0];
        group.BoundsMin.x=x0; group.BoundsMin.y=y0; group.BoundsMin.z=z0;
        group.BoundsMax.x=x1; group.BoundsMax.y=y1; group.BoundsMax.z=z1;
        group.Offset=offset; group.Length=36; group.VertexCount=8; group.TriangleCount=12;
        group.TextureIndex0=0; group.TextureIndex1=0; group.TextureIndex2=0; group.TextureIndex3=0; group.TextureIndex4=0;
        group.ShaderIndex0=0; group.Flags=0x14080;
        var groups = new List<RealShadingGroup>(p.PartData.Groups); groups.Add(group);
        p.PartData.Vertices=vertices.ToArray(); p.PartData.Indices=indices.ToArray(); p.PartData.Groups=groups.ToArray();
        p.PartData.GroupCount=groups.Count; p.PartData.IndexCount=indices.Count;
        p.PartInfo.TriangleCount=indices.Count/3; p.PartInfo.Unk6_MW=p.PartInfo.TriangleCount;
        if (x1 > p.PartInfo.BoundMax.x) p.PartInfo.BoundMax.x=x1;
        if (y0 < p.PartInfo.BoundMin.y) p.PartInfo.BoundMin.y=y0;
        if (y1 > p.PartInfo.BoundMax.y) p.PartInfo.BoundMax.y=y1;
        if (z0 < p.PartInfo.BoundMin.z) p.PartInfo.BoundMin.z=z0;
        if (z1 > p.PartInfo.BoundMax.z) p.PartInfo.BoundMax.z=z1;
    }
    public static void Main(string[] args) {
        byte[] b=File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
        var f=new RealGeometryFile(); f.Open(new MemoryStream(b));
        int count=0;
        foreach(RealGeometryPart p in f) {
            for(int i=0;i<p.PartData.Vertices.Length;i++) p.PartData.Vertices[i].Initialize(true,0);
            if(!p.PartInfo.PartName.ToString().Contains("_BRAKELIGHT_")) continue;
            for(int i=0;i<p.PartInfo.Shaders.Length;i++) p.PartInfo.Shaders[i]=0x0FEDEE40u;
            for(int i=0;i<p.PartInfo.Textures.Length;i++) {
                // Separate the Shelby housing atlas from the Fusion's atlas.
                if(p.PartInfo.Textures[i]==0x5A00E244u) p.PartInfo.Textures[i]=0xF18A0001u;
            }
            for(int i=0;i<p.PartData.Vertices.Length;i++) p.PartData.Vertices[i].Diffuse |= unchecked((int)0xFF000000);
            if (p.PartInfo.PartName.ToString().EndsWith("_BRAKELIGHT_A")) AddReflectorBacking(p);
            count++;
        }
        f.GeometryInfo.PartCount=f.PartCount; f.Save(args[1]);
        Console.WriteLine("Opaque rear lamp parts: "+count);
    }
}
