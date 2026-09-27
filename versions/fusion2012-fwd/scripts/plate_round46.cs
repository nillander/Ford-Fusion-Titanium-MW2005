using System;
using System.IO;
using System.Collections.Generic;
using mwgc.RealEngine;

// Round the two flat plate quads in BASE_A/B/C to match the rounded BADGING
// outline.  The old 3D surround has already been removed by plate44.cs.
public class PlateRound46 {
  const uint MustangBadging=0x339D0D44, CobaltBadging=0xEFC2BB05;
  const uint LicensePlate=0x4C95C6F8;
  const float Radius=.013f; // 12 atlas pixels, approximately 13 mm on the car
  const int ArcSteps=4;

  class Group {
    public RealShadingGroup Source;
    public uint Texture,Shader;
    public List<RealVertex> Vertices=new();
    public List<int> Indices=new();
  }

  static RealGeometryFile Read(string path) {
    var bytes=File.ReadAllBytes(path);
    Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
    var file=new RealGeometryFile();file.Open(new MemoryStream(bytes));return file;
  }

  static void CopyGroup(RealGeometryPart part,RealShadingGroup source,Group result) {
    var data=part.PartData;var remap=new Dictionary<int,int>();
    for(int q=source.Offset;q<source.Offset+source.Length;q++) {
      int original=data.Indices[q];
      if(!remap.TryGetValue(original,out int local)) {
        local=result.Vertices.Count;
        result.Vertices.Add(data.Vertices[original]);remap[original]=local;
      }
      result.Indices.Add(local);
    }
  }

  static void AddRoundedPlate(List<RealVertex> source,int side,Group result) {
    if(source.Count!=4)throw new Exception($"Expected four plate corners, got {source.Count}");
    float ymin=999,ymax=-999,zmin=999,zmax=-999,x=0;
    foreach(var v in source) {
      var p=v.Position;x+=p.x/4f;
      ymin=Math.Min(ymin,p.y);ymax=Math.Max(ymax,p.y);
      zmin=Math.Min(zmin,p.z);zmax=Math.Max(zmax,p.z);
    }
    if(ymax-ymin<.35f||zmax-zmin<.10f)throw new Exception("Unexpected plate dimensions");
    var corners=new RealVertex[4];
    float[] cy={ymin,ymax,ymax,ymin},cz={zmin,zmin,zmax,zmax};
    for(int k=0;k<4;k++) {
      float best=999;
      foreach(var v in source) {
        float dy=v.Position.y-cy[k],dz=v.Position.z-cz[k],dist=dy*dy+dz*dz;
        if(dist<best){best=dist;corners[k]=v;}
      }
      if(best>1e-5f)throw new Exception("Plate corners are not rectangular");
    }
    RealVertex Make(float y,float z) {
      float a=(y-ymin)/(ymax-ymin),b=(z-zmin)/(zmax-zmin);
      var v=corners[0];
      v.Position=new RealVector3(x,y,z);
      v.Normal=new RealVector3(side,0,0);
      v.UV=new RealVector2(
        (1-a)*(1-b)*corners[0].UV.u+a*(1-b)*corners[1].UV.u+a*b*corners[2].UV.u+(1-a)*b*corners[3].UV.u,
        (1-a)*(1-b)*corners[0].UV.v+a*(1-b)*corners[1].UV.v+a*b*corners[2].UV.v+(1-a)*b*corners[3].UV.v);
      return v;
    }
    int center=result.Vertices.Count;
    result.Vertices.Add(Make((ymin+ymax)/2f,(zmin+zmax)/2f));
    int begin=result.Vertices.Count;
    float[] centersY={ymin+Radius,ymax-Radius,ymax-Radius,ymin+Radius};
    float[] centersZ={zmin+Radius,zmin+Radius,zmax-Radius,zmax-Radius};
    for(int corner=0;corner<4;corner++) {
      for(int step=0;step<=ArcSteps;step++) {
        float angle=(float)(Math.PI+corner*Math.PI/2+step*Math.PI/(2*ArcSteps));
        float y=centersY[corner]+Radius*(float)Math.Cos(angle);
        float z=centersZ[corner]+Radius*(float)Math.Sin(angle);
        result.Vertices.Add(Make(y,z));
      }
    }
    int count=4*(ArcSteps+1);
    for(int i=0;i<count;i++) {
      int a=begin+i,b=begin+(i+1)%count;
      if(side>0)result.Indices.AddRange(new[]{center,a,b});
      else result.Indices.AddRange(new[]{center,b,a});
    }
  }

  static void RoundGroup(RealGeometryPart part,RealShadingGroup source,Group result) {
    var d=part.PartData;
    if(source.Length!=12)throw new Exception($"Unexpected LICENSEPLATE triangle count in {part.PartInfo.PartName}");
    foreach(int side in new[]{1,-1}) {
      var seen=new HashSet<int>();var vertices=new List<RealVertex>();int triangles=0;
      for(int q=source.Offset;q<source.Offset+source.Length;q+=3) {
        var p0=d.Vertices[d.Indices[q]].Position;
        var p1=d.Vertices[d.Indices[q+1]].Position;
        var p2=d.Vertices[d.Indices[q+2]].Position;
        float x=(p0.x+p1.x+p2.x)/3f;
        if(side*x<2f)continue;
        triangles++;
        for(int k=0;k<3;k++) {
          int vi=d.Indices[q+k];
          if(seen.Add(vi))vertices.Add(d.Vertices[vi]);
        }
      }
      if(triangles!=2)throw new Exception($"Expected two triangles per plate in {part.PartInfo.PartName}");
      AddRoundedPlate(vertices,side,result);
    }
  }

  static RealGeometryPart Rebuild(RealGeometryPart part,out int rounded) {
    rounded=0;var groups=new List<Group>();
    foreach(var source in part.PartData.Groups) {
      uint texture=part.PartInfo.Textures[source.TextureIndex0];
      uint shader=part.PartInfo.Shaders[source.ShaderIndex0];
      var item=new Group{Source=source,Texture=texture,Shader=shader};
      if((texture==MustangBadging||texture==CobaltBadging)&&shader==LicensePlate) {
        RoundGroup(part,source,item);rounded+=2;
      } else CopyGroup(part,source,item);
      if(item.Indices.Count>0)groups.Add(item);
    }
    if(rounded==0)return part;
    var verts=new List<RealVertex>();var indices=new List<ushort>();
    var shading=new List<RealShadingGroup>();var textures=new List<uint>();var shaders=new List<uint>();
    foreach(var item in groups) {
      int baseVertex=verts.Count,offset=indices.Count;
      verts.AddRange(item.Vertices);
      foreach(int index in item.Indices)indices.Add((ushort)(baseVertex+index));
      int ti=textures.IndexOf(item.Texture);if(ti<0){ti=textures.Count;textures.Add(item.Texture);}
      int si=shaders.IndexOf(item.Shader);if(si<0){si=shaders.Count;shaders.Add(item.Shader);}
      var g=item.Source;g.Offset=offset;g.Length=item.Indices.Count;
      g.TriangleCount=item.Indices.Count/3;g.VertexCount=item.Vertices.Count;
      g.TextureIndex0=g.TextureIndex1=g.TextureIndex2=g.TextureIndex3=g.TextureIndex4=(byte)ti;
      g.ShaderIndex0=(byte)si;shading.Add(g);
    }
    if(verts.Count>65535)throw new Exception("Part exceeds 16-bit vertex limit");
    var output=new RealGeometryPart();output.PartInfo=part.PartInfo;
    output.PartInfo.Textures=textures.ToArray();output.PartInfo.Shaders=shaders.ToArray();
    output.PartInfo.TextureCount=(byte)textures.Count;output.PartInfo.ShaderCount=(byte)shaders.Count;
    var data=part.PartData;data.Vertices=verts.ToArray();
    for(int i=0;i<data.Vertices.Length;i++)data.Vertices[i].Initialize(true,0);
    data.Indices=indices.ToArray();data.Groups=shading.ToArray();
    data.GroupCount=shading.Count;data.IndexCount=indices.Count;data.Materials=null;
    output.PartData=data;output.PartInfo.TriangleCount=indices.Count/3;
    output.PartInfo.Unk6_MW=indices.Count/3;
    return output;
  }

  public static void Main(string[] args) {
    var input=Read(args[0]);var output=new RealGeometryFile();
    output.GeometryInfo=input.GeometryInfo;int total=0;
    foreach(RealGeometryPart part in input) {
      var rounded=Rebuild(part,out int count);total+=count;
      if(count>0)Console.WriteLine($"{part.PartInfo.PartName}: rounded {count} plates");
      output.AddPart(rounded);
    }
    if(total!=6)throw new Exception($"Expected six plate surfaces (two on each LOD A-C), got {total}");
    output.GeometryInfo.PartCount=output.PartCount;output.Save(args[1]);
  }
}
