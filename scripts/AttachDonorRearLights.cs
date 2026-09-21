using System;
using System.IO;
using System.Collections.Generic;
using mwgc.RealEngine;

public class AttachDonorRearLights {
    static RealGeometryFile Read(string path) {
        byte[] b=File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
        var f=new RealGeometryFile();f.Open(new MemoryStream(b));return f;
    }
    public static void Main(string[] args) {
        var f=Read(args[0]);var donor=Read(args[1]);
        RealGeometryPart lamp=null;
        foreach(RealGeometryPart p in donor)
            if(p.PartInfo.PartName.ToString()=="MUSTANGGT_KIT00_RIGHT_BRAKELIGHT_A")lamp=p;
        if(lamp==null)throw new Exception("Missing AJM rear light");
        // Keep the donor's working opaque lens/reflector group, including UVs
        // and shader. Other groups are shared interior and a global light map.
        RealShadingGroup g=new RealShadingGroup();bool found=false;
        foreach(RealShadingGroup candidate in lamp.PartData.Groups)
            if(lamp.PartInfo.Textures[candidate.TextureIndex0]==0x4B7D95B6u) {g=candidate;found=true;break;}
        if(!found)throw new Exception("Missing native opaque lamp group");
        var vertices=new List<RealVertex>();var indices=new List<ushort>();var remap=new Dictionary<ushort,ushort>();
        for(int i=g.Offset;i<g.Offset+g.Length;i++) {
            ushort old=lamp.PartData.Indices[i], n;
            if(!remap.TryGetValue(old,out n)) {
                n=(ushort)vertices.Count;remap.Add(old,n);vertices.Add(lamp.PartData.Vertices[old]);
            }
            indices.Add(n);
        }
        float xmin=float.MaxValue,xmax=float.MinValue,ymin=float.MaxValue,ymax=0,zmin=float.MaxValue,zmax=float.MinValue;
        foreach(var v in vertices) {
            xmin=Math.Min(xmin,v.Position.x);xmax=Math.Max(xmax,v.Position.x);
            ymin=Math.Min(ymin,Math.Abs(v.Position.y));ymax=Math.Max(ymax,Math.Abs(v.Position.y));
            zmin=Math.Min(zmin,v.Position.z);zmax=Math.Max(zmax,v.Position.z);
        }
        float sx=(-1.806f+2.285f)/(xmax-xmin), sy=(.808f-.345f)/(ymax-ymin), sz=(.792f-.635f)/(zmax-zmin);
        for(int i=0;i<vertices.Count;i++) {
            var v=vertices[i];float side=v.Position.y<0?-1:1;
            v.Position.x=-2.289f+(v.Position.x-xmin)*sx;
            v.Position.y=side*(.345f+(Math.Abs(v.Position.y)-ymin)*sy);
            v.Position.z=.635f+(v.Position.z-zmin)*sz;
            v.Normal.x/=sx;v.Normal.y/=sy;v.Normal.z/=sz;
            float len=(float)Math.Sqrt(v.Normal.x*v.Normal.x+v.Normal.y*v.Normal.y+v.Normal.z*v.Normal.z);
            if(len>0){v.Normal.x/=len;v.Normal.y/=len;v.Normal.z/=len;}
            v.Diffuse=-1;v.Initialize(true,0);vertices[i]=v;
        }
        var addition=new RealGeometryPart();addition.PartInfo=lamp.PartInfo;
        addition.PartInfo.Textures=new uint[]{0x4B7D95B6u};addition.PartInfo.TextureCount=1;
        addition.PartInfo.Shaders=new uint[]{lamp.PartInfo.Shaders[g.ShaderIndex0]};addition.PartInfo.ShaderCount=1;
        addition.PartInfo.BoundMin=new RealVector4();addition.PartInfo.BoundMax=new RealVector4();
        addition.PartInfo.BoundMin.x=-2.289f;addition.PartInfo.BoundMin.y=-.808f;addition.PartInfo.BoundMin.z=.635f;
        addition.PartInfo.BoundMax.x=-1.81f;addition.PartInfo.BoundMax.y=.808f;addition.PartInfo.BoundMax.z=.792f;
        addition.PartData=lamp.PartData;
        addition.PartData.Vertices=vertices.ToArray();addition.PartData.Indices=indices.ToArray();
        addition.PartData.IndexCount=indices.Count;addition.PartData.GroupCount=1;
        g.Offset=0;g.Length=indices.Count;g.VertexCount=vertices.Count;g.TriangleCount=indices.Count/3;
        g.TextureIndex0=g.TextureIndex1=g.TextureIndex2=g.TextureIndex3=g.TextureIndex4=g.ShaderIndex0=0;
        g.BoundsMin=new RealVector3(-2.289f,-.808f,.635f);g.BoundsMax=new RealVector3(-1.81f,.808f,.792f);
        addition.PartData.Groups=new RealShadingGroup[]{g};
        foreach(RealGeometryPart p in f) {
            string name=p.PartInfo.PartName.ToString();
            if(name.StartsWith("MUSTANGGT_BASE_")&&!name.EndsWith("_E"))AppendPartMeshes.Append(p,addition);
            if(name.Contains("_BRAKELIGHT_")) {
                for(int i=0;i<p.PartData.Vertices.Length;i++)p.PartData.Vertices[i].Position=new RealVector3();
            }
            foreach(var idx in p.PartData.Indices)if(idx>=p.PartData.Vertices.Length)throw new Exception("Index out of bounds");
            if(p.PartData.Vertices.Length>=30000)throw new Exception("Vertex budget exceeded: "+name);
        }
        f.GeometryInfo.PartCount=f.PartCount;f.Save(args[2]);
        Console.WriteLine("Appended AJM opaque rear group: "+vertices.Count+" vertices; native shader "+addition.PartInfo.Shaders[0].ToString("X8"));
    }
}
