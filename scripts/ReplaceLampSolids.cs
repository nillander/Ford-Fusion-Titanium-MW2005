using System;
using System.IO;
using mwgc.RealEngine;

// Restore the engine's native organization: each lamp is rendered through its
// own catalogue solid instead of being appended past BASE's large index buffer.
class ReplaceLampSolids {
    static RealGeometryFile Read(string path) {
        var bytes=File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
        var file=new RealGeometryFile();file.Open(new MemoryStream(bytes));return file;
    }
    static RealGeometryPart Find(RealGeometryFile first,RealGeometryFile second,uint hash) {
        var part=first[hash];return part ?? second[hash];
    }
    static bool IsLamp(string name) {
        return name.Contains("_HEADLIGHT_") || name.Contains("_BRAKELIGHT_");
    }
    static void Main(string[] args) {
        var baseline=Read(args[0]);var rear=Read(args[1]);var front=Read(args[2]);
        var output=new RealGeometryFile();output.GeometryInfo=baseline.GeometryInfo;int replaced=0;
        foreach(RealGeometryPart original in baseline) {
            string name=original.PartInfo.PartName.ToString();
            RealGeometryPart chosen=original;
            if(IsLamp(name)) {
                var generated=Find(rear,front,original.PartInfo.Hash);
                if(generated!=null){chosen=generated;replaced++;}
            }
            for(int i=0;i<chosen.PartData.Vertices.Length;i++)chosen.PartData.Vertices[i].Initialize(true,0);
            output.AddPart(chosen);
        }
        if(replaced!=16)throw new Exception("Expected 16 generated lamp solids, found "+replaced);
        output.GeometryInfo.PartCount=output.PartCount;output.Save(args[3]);
        Console.WriteLine("Replaced native lamp solids: "+replaced+"; parts: "+output.PartCount);
    }
}
