using System;
using System.Collections.Generic;
using System.IO;
using mwgc.RealEngine;

// MW has no Blender backface toggle in the exported mesh. Opposite index
// winding shares the same vertices/UVs and leaves one visible face per side.
class MakeLampFacesTwoSided {
    static void Main(string[] args) {
        var bytes=File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
        var file=new RealGeometryFile();file.Open(new MemoryStream(bytes));
        int groups=0;
        foreach(RealGeometryPart p in file) {
            for(int i=0;i<p.PartData.Vertices.Length;i++)p.PartData.Vertices[i].Initialize(true,0);
            string name=p.PartInfo.PartName.ToString();
            bool nativeLamp=name.Contains("_HEADLIGHT_") || name.Contains("_BRAKELIGHT_");
            bool basePart=name.Contains("_BASE_");
            if(!nativeLamp && !basePart)continue;
            var indices=new List<ushort>();var original=p.PartData.Indices;
            for(int g=0;g<p.PartData.Groups.Length;g++) {
                var group=p.PartData.Groups[g];int start=group.Offset;
                bool lamp=nativeLamp || p.PartInfo.Shaders[group.ShaderIndex0]==0x05BC3A3Cu;
                group.Offset=indices.Count;
                for(int i=start;i<start+group.Length;i+=3) {
                    indices.Add(original[i]);indices.Add(original[i+1]);indices.Add(original[i+2]);
                    if(lamp){indices.Add(original[i+2]);indices.Add(original[i+1]);indices.Add(original[i]);}
                }
                if(lamp){group.Length*=2;group.TriangleCount*=2;groups++;}
                p.PartData.Groups[g]=group;
            }
            p.PartData.Indices=indices.ToArray();p.PartData.IndexCount=indices.Count;
            p.PartInfo.TriangleCount=indices.Count/3;p.PartInfo.Unk6_MW=indices.Count/3;
        }
        if(groups!=16)throw new Exception("Expected 16 lamp groups, found "+groups);
        file.Save(args[1]);Console.WriteLine("Two-sided lamp groups: "+groups);
    }
}
