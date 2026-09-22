using System;
using System.IO;
using mwgc.RealEngine;

class ReplaceBodySolids {
    static RealGeometryFile Read(string path) {
        var bytes=File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
        var file=new RealGeometryFile();file.Open(new MemoryStream(bytes));return file;
    }
    static bool IsBody(string name) {
        return name.Contains("_KIT00_BODY_");
    }
    static void Main(string[] args) {
        var current=Read(args[0]);var historical=Read(args[1]);
        var output=new RealGeometryFile();output.GeometryInfo=current.GeometryInfo;int replaced=0;
        foreach(RealGeometryPart original in current) {
            RealGeometryPart chosen=original;
            if(IsBody(original.PartInfo.PartName.ToString())) {
                chosen=historical[original.PartInfo.Hash];
                if(chosen==null)throw new Exception("Missing historical "+original.PartInfo.PartName);
                replaced++;
            }
            for(int i=0;i<chosen.PartData.Vertices.Length;i++)chosen.PartData.Vertices[i].Initialize(true,0);
            output.AddPart(chosen);
        }
        if(replaced!=5)throw new Exception("Expected five BODY solids, found "+replaced);
        output.GeometryInfo.PartCount=output.PartCount;output.Save(args[2]);
        Console.WriteLine("Historical BODY solids restored: "+replaced);
    }
}
