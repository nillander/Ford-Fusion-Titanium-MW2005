using System;
using System.IO;
using System.Collections.Generic;
using mwgc.RealEngine;
public class MergeGeometry {
    static RealGeometryFile Read(string path) {
        byte[] b=File.ReadAllBytes(path);
        // The original donor stores solid chunks as top-level siblings. Nest them for this reader.
        Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
        var f=new RealGeometryFile(); f.Open(new MemoryStream(b)); return f;
    }
    public static void Main(string[] args) {
        var donor=Read(args[0]); var newer=Read(args[1]); var result=new RealGeometryFile();
        result.GeometryInfo=donor.GeometryInfo;
        int replaced=0,kept=0,empty=0;
        foreach(RealGeometryPart original in donor) {
            var name=original.PartInfo.PartName.ToString();
            var p=newer[original.PartInfo.Hash];
            if(p!=null) {
                p.PartInfo.MountPoints=original.PartInfo.MountPoints;
                result.AddPart(p);replaced++;
            } else if(name.Contains("_TIRE_")||name.Contains("_BRAKE_")||name.Contains("_DRIVER_")||name.Contains("_KIT01_BODY_")||name.Contains("_KIT02_BODY_")) {
                if(name.Contains("_DRIVER_")) {
                    for(int i=0;i<original.PartData.Vertices.Length;i++) {original.PartData.Vertices[i].Position.z-=.2f;original.PartData.Vertices[i].Position.x-=.15f;}
                    original.PartInfo.BoundMin.z-=.2f;original.PartInfo.BoundMax.z-=.2f;
                    original.PartInfo.BoundMin.x-=.15f;original.PartInfo.BoundMax.x-=.15f;
                    for(int i=0;i<original.PartData.Groups.Length;i++) {
                        original.PartData.Groups[i].BoundsMin.z-=.2f;original.PartData.Groups[i].BoundsMax.z-=.2f;
                        original.PartData.Groups[i].BoundsMin.x-=.15f;original.PartData.Groups[i].BoundsMax.x-=.15f;
                    }
                }
                // Initialize write flags lost by the old reader, retaining all donor geometry values.
                for(int i=0;i<original.PartData.Vertices.Length;i++) original.PartData.Vertices[i].Initialize(true,0);
                result.AddPart(original);kept++;
            } else {
                // Preserve the slot hash without leaving the old car's visible panels in the new car.
                p=new RealGeometryPart();p.PartInfo=original.PartInfo;
                p.PartInfo.TriangleCount=1;p.PartInfo.Unk5_MW=1;p.PartInfo.Unk6_MW=1;
                p.PartInfo.Transform.m=new float[]{1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};
                p.PartInfo.BoundMin=new RealVector4();p.PartInfo.BoundMax=new RealVector4();
                p.PartInfo.TextureCount=1;p.PartInfo.Textures=new uint[]{original.PartInfo.Textures[0]};
                p.PartInfo.ShaderCount=1;p.PartInfo.Shaders=new uint[]{0x0fedee40};
                p.PartData.Flags=0x4080;p.PartData.GroupCount=1;p.PartData.Unk1=0x12;p.PartData.VBCount=1;
                p.PartData.Vertices=new RealVertex[3];
                for(int i=0;i<3;i++) {p.PartData.Vertices[i].Initialize(true,0);p.PartData.Vertices[i].Normal.z=1;p.PartData.Vertices[i].Diffuse=-1;}
                p.PartData.Vertices[1].Position.x=.00001f;p.PartData.Vertices[2].Position.y=.00001f;
                p.PartInfo.BoundMax.x=.00001f;p.PartInfo.BoundMax.y=.00001f;
                p.PartData.Indices=new ushort[]{0,1,2};
                p.PartData.IndexCount=3;
                var group=new RealShadingGroup();group.VertexCount=3;group.TriangleCount=1;group.Length=3;group.Unk1=4;group.Flags=0x4080;
                group.BoundsMax.x=.00001f;group.BoundsMax.y=.00001f;
                p.PartData.Groups=new RealShadingGroup[]{group};p.PartData.Materials=new System.Collections.ArrayList(new FixedLenString[]{new FixedLenString("EMPTY")});
                result.AddPart(p);empty++;
            }
        }
        foreach(RealGeometryPart p in newer)if(donor[p.PartInfo.Hash]==null){result.AddPart(p);replaced++;}
        foreach(RealGeometryPart p in result) {
            for(int i=0;i<p.PartData.Vertices.Length;i++)p.PartData.Vertices[i].Initialize(true,0);
            foreach(var index in p.PartData.Indices)if(index>=p.PartData.Vertices.Length)throw new Exception("Index out of range: "+p.PartInfo.PartName);
        }
        result.GeometryInfo.PartCount=result.PartCount;
        result.Save(args[2]);
        Console.WriteLine("Replaced="+replaced+" retained="+kept+" placeholders="+empty+" total="+result.PartCount);
    }
}
