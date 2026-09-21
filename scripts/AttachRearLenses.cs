using System;
using System.IO;
using mwgc.RealEngine;

public class AttachRearLenses {
    static RealGeometryFile Read(string path) {
        var bytes=File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
        var f=new RealGeometryFile(); f.Open(new MemoryStream(bytes)); return f;
    }
    public static void Main(string[] args) {
        var f=Read(args[0]); var lenses=Read(args[1]);
        bool diagnostic=args.Length>3 && args[3]=="diagnostic";
        foreach(RealGeometryPart p in f)
            for(int i=0;i<p.PartData.Vertices.Length;i++)p.PartData.Vertices[i].Initialize(true,0);
        foreach(RealGeometryPart lamp in lenses) {
            string name=lamp.PartInfo.PartName.ToString(); string lod=name.Substring(name.Length-1);
            RealGeometryPart target=null;
            foreach(RealGeometryPart p in f)if(p.PartInfo.PartName.ToString()=="MUSTANGGT_BASE_"+lod)target=p;
            if(target==null)throw new Exception("Missing BASE_"+lod);
            if(diagnostic) {
                bool left=name.Contains("_LEFT_");
                lamp.PartInfo.Shaders=new uint[]{left?0xD6D6080Au:0x0FEDEE40u};
                lamp.PartInfo.Textures=new uint[]{left?0x9A8AAD9Eu:0x5A00E244u};
                for(int i=0;i<lamp.PartData.Vertices.Length;i++) {
                    lamp.PartData.Vertices[i].UV.u=.5f; lamp.PartData.Vertices[i].UV.v=.05f;
                }
            }
            AppendPartMeshes.Append(target,lamp);
            if(target.PartData.Vertices.Length>=30000)throw new Exception("BASE vertex budget exceeded");
            // Keep the catalogue entry without rendering the same lens twice.
            var old=f[lamp.PartInfo.Hash];
            if(old!=null) {
                old.PartData.Vertices=new RealVertex[3];
                for(int i=0;i<3;i++) {
                    old.PartData.Vertices[i].Initialize(true,0);
                    old.PartData.Vertices[i].Diffuse=-1;
                    old.PartData.Vertices[i].Normal.z=1;
                }
                old.PartData.Vertices[1].Position.x=.00001f;
                old.PartData.Vertices[2].Position.y=.00001f;
                old.PartData.Indices=new ushort[]{0,1,2};
                old.PartData.IndexCount=3; old.PartData.GroupCount=1;
                var group=old.PartData.Groups[0];
                group.VertexCount=3;group.TriangleCount=1;group.Offset=0;group.Length=3;
                group.BoundsMin=new RealVector3();group.BoundsMax=new RealVector3(.00001f,.00001f,0);
                old.PartData.Groups=new RealShadingGroup[]{group};
                old.PartInfo.TriangleCount=1;old.PartInfo.Unk5_MW=1;old.PartInfo.Unk6_MW=1;
                old.PartInfo.BoundMin=new RealVector4();old.PartInfo.BoundMax=new RealVector4();
                old.PartInfo.BoundMax.x=.00001f;old.PartInfo.BoundMax.y=.00001f;
            }
        }
        f.GeometryInfo.PartCount=f.PartCount; f.Save(args[2]);
        Console.WriteLine("Attached Fusion lenses to BASE A-D; diagnostic="+diagnostic);
    }
}
