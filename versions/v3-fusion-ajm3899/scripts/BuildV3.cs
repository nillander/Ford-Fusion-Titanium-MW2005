using System; using System.IO; using System.Collections.Generic; using mwgc.RealEngine;

// V3: AJM3899 catalogue (64 solids, mount points, wheels, brakes) + Fusion 2018
// content from the V2 checkpoint.  Keeps only the Fusion 2018 mirror pair (in BODY).
// args: ajm.bin v2.bin v1.bin out.bin [--dull-lamps]
public class BuildV3 {
  const uint DULL=0x0FEDEE40, BRAKELIGHT=0x05BC3A3C, INTERIOR_SH=0x2787EDAB, GRILLE_TEX=0xD0612097, OPAQUE_TEX=0x590566EC;
  const uint AJM_INTERIOR=0x2AF3D244;
  public static uint BinHash(string s){uint h=0xFFFFFFFF;foreach(char c in s)h=h*33+(uint)c;return h;}
  static RealGeometryFile Read(string path){var b=File.ReadAllBytes(path);Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);var f=new RealGeometryFile();f.Open(new MemoryStream(b));return f;}
  static RealGeometryPart ByName(RealGeometryFile f,string n){foreach(RealGeometryPart p in f)if(p.PartInfo.PartName.ToString()==n)return p;return null;}
  static string N(string s){return "MUSTANGGT_"+s;}

  // Rebuild a part keeping only selected groups (in given order); optional triangle filter and two-sided duplication.
  static RealGeometryPart Rebuild(RealGeometryPart src,int[] keep,Func<RealVertex,RealVertex,RealVertex,bool> dropTri,bool twoSided){
    var d=src.PartData; var starts=new int[d.Groups.Length]; int acc=0;
    for(int g=0;g<d.Groups.Length;g++){starts[g]=acc;acc+=d.Groups[g].VertexCount;}
    var verts=new List<RealVertex>(); var idx=new List<ushort>(); var groups=new List<RealShadingGroup>();
    foreach(int g in keep){
      var grp=d.Groups[g]; int vbase=verts.Count;
      for(int i=0;i<grp.VertexCount;i++)verts.Add(d.Vertices[starts[g]+i]);
      int off=idx.Count; int tris=0;
      float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
      for(int i=grp.Offset;i<grp.Offset+grp.Length;i+=3){
        int a=d.Indices[i],b=d.Indices[i+1],c=d.Indices[i+2];
        if(dropTri!=null&&dropTri(d.Vertices[a],d.Vertices[b],d.Vertices[c]))continue;
        int na=a-starts[g]+vbase,nb=b-starts[g]+vbase,nc=c-starts[g]+vbase;
        idx.Add((ushort)na);idx.Add((ushort)nb);idx.Add((ushort)nc);tris++;
        if(twoSided){idx.Add((ushort)nc);idx.Add((ushort)nb);idx.Add((ushort)na);tris++;}
        foreach(int k in new[]{a,b,c}){var p=d.Vertices[k].Position;mn[0]=Math.Min(mn[0],p.x);mn[1]=Math.Min(mn[1],p.y);mn[2]=Math.Min(mn[2],p.z);mx[0]=Math.Max(mx[0],p.x);mx[1]=Math.Max(mx[1],p.y);mx[2]=Math.Max(mx[2],p.z);}
      }
      if(tris==0){verts.RemoveRange(vbase,verts.Count-vbase);continue;}
      grp.Offset=off;grp.Length=idx.Count-off;grp.TriangleCount=tris;
      grp.BoundsMin=new RealVector3(mn[0],mn[1],mn[2]);grp.BoundsMax=new RealVector3(mx[0],mx[1],mx[2]);
      groups.Add(grp);
    }
    var outp=new RealGeometryPart(); outp.PartInfo=src.PartInfo; var od=d;
    od.Vertices=verts.ToArray(); od.Indices=idx.ToArray(); od.Groups=groups.ToArray(); od.GroupCount=groups.Count; od.IndexCount=idx.Count; od.Materials=null;
    outp.PartData=od; Finish(outp); return outp;
  }
  // Concatenate several single-source parts into one (groups appended).
  static RealGeometryPart Concat(RealGeometryPart first,RealGeometryPart second){
    var a=first.PartData;var b=second.PartData;
    // unify texture/shader tables
    var tex=new List<uint>(first.PartInfo.Textures);var sh=new List<uint>(first.PartInfo.Shaders);
    var verts=new List<RealVertex>(a.Vertices);var idx=new List<ushort>(a.Indices);var groups=new List<RealShadingGroup>(a.Groups);
    int vbase=verts.Count; verts.AddRange(b.Vertices);
    foreach(var g0 in b.Groups){var g=g0;
      int off=idx.Count; for(int i=g.Offset;i<g.Offset+g.Length;i++)idx.Add((ushort)(b.Indices[i]+vbase));
      g.Offset=off;
      uint t=second.PartInfo.Textures[g.TextureIndex0]; int ti=tex.IndexOf(t); if(ti<0){tex.Add(t);ti=tex.Count-1;}
      uint s=second.PartInfo.Shaders[g.ShaderIndex0]; int si=sh.IndexOf(s); if(si<0){sh.Add(s);si=sh.Count-1;}
      g.TextureIndex0=g.TextureIndex1=g.TextureIndex2=g.TextureIndex3=g.TextureIndex4=(byte)ti; g.ShaderIndex0=(byte)si;
      groups.Add(g);}
    if(verts.Count>65535)throw new Exception("vertex overflow");
    var p=new RealGeometryPart();p.PartInfo=first.PartInfo;p.PartInfo.Textures=tex.ToArray();p.PartInfo.Shaders=sh.ToArray();
    p.PartInfo.TextureCount=(byte)tex.Count;p.PartInfo.ShaderCount=(byte)sh.Count;
    var d=a;d.Vertices=verts.ToArray();d.Indices=idx.ToArray();d.Groups=groups.ToArray();d.GroupCount=groups.Count;d.IndexCount=idx.Count;d.Materials=null;
    p.PartData=d;Finish(p);return p;
  }
  static void Finish(RealGeometryPart p){
    var d=p.PartData; for(int i=0;i<d.Vertices.Length;i++)d.Vertices[i].Initialize(true,0);
    float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
    foreach(var g in d.Groups){mn[0]=Math.Min(mn[0],g.BoundsMin.x);mn[1]=Math.Min(mn[1],g.BoundsMin.y);mn[2]=Math.Min(mn[2],g.BoundsMin.z);mx[0]=Math.Max(mx[0],g.BoundsMax.x);mx[1]=Math.Max(mx[1],g.BoundsMax.y);mx[2]=Math.Max(mx[2],g.BoundsMax.z);}
    if(d.Groups.Length>0){p.PartInfo.BoundMin=new RealVector4(mn[0],mn[1],mn[2],p.PartInfo.BoundMin.w);p.PartInfo.BoundMax=new RealVector4(mx[0],mx[1],mx[2],p.PartInfo.BoundMax.w);}
    p.PartInfo.TriangleCount=d.Indices.Length/3; p.PartInfo.Unk6_MW=d.Indices.Length/3; p.PartInfo.Unk5_MW=1;
    if(d.Indices.Length>65535)throw new Exception("index overflow in "+p.PartInfo.PartName+": "+d.Indices.Length);
    p.PartData=d;
  }
  // Take content of src under the identity (hash/name/mount points) of target.
  static RealGeometryPart As(RealGeometryPart content,RealGeometryPart target,bool keepMounts){
    var p=new RealGeometryPart();p.PartInfo=content.PartInfo;p.PartData=content.PartData;
    p.PartInfo.Hash=target.PartInfo.Hash;p.PartInfo.PartName=target.PartInfo.PartName;p.PartInfo.Transform=target.PartInfo.Transform;
    if(keepMounts)p.PartInfo.MountPoints=target.PartInfo.MountPoints; else p.PartInfo.MountPoints=new RealMountPoint[0];
    Finish(p);return p;
  }
  static RealGeometryPart Clone(RealGeometryPart s){var p=new RealGeometryPart();p.PartInfo=s.PartInfo;p.PartData=s.PartData;
    p.PartData.Vertices=(RealVertex[])s.PartData.Vertices.Clone();p.PartData.Indices=(ushort[])s.PartData.Indices.Clone();p.PartData.Groups=(RealShadingGroup[])s.PartData.Groups.Clone();
    p.PartInfo.Textures=(uint[])s.PartInfo.Textures.Clone();p.PartInfo.Shaders=(uint[])s.PartInfo.Shaders.Clone();return p;}
  static int[] GroupsWhere(RealGeometryPart p,Func<uint,uint,bool> pred){var l=new List<int>();for(int g=0;g<p.PartData.Groups.Length;g++){var gr=p.PartData.Groups[g];if(pred(p.PartInfo.Shaders[gr.ShaderIndex0],p.PartInfo.Textures[gr.TextureIndex0]))l.Add(g);}return l.ToArray();}
  static bool Spike(RealVertex v){return v.Position.x>1.0f&&v.Position.z>1.0f;}
  static float Edge(RealVertex a,RealVertex b){float dx=a.Position.x-b.Position.x,dy=a.Position.y-b.Position.y,dz=a.Position.z-b.Position.z;return (float)Math.Sqrt(dx*dx+dy*dy+dz*dz);}

  public static void Main(string[] args){
    var ajm=Read(args[0]);var v2=Read(args[1]);var v1=Read(args[2]);bool dull=Array.IndexOf(args,"--dull-lamps")>=0;
    var placeholder=ByName(v1,N("KIT00_SPOILER_A")); // 1 degenerate triangle, DULLPLASTIC
    var output=new RealGeometryFile();output.GeometryInfo=ajm.GeometryInfo;
    var log=new List<string>();
    uint ajmInteriorNew=BinHash("MUSTANGGT_AJM_INTERIOR");
    foreach(RealGeometryPart orig in ajm){
      string name=orig.PartInfo.PartName.ToString(); string s=name.Substring(10); char lod=s[s.Length-1]; string stem=s.Substring(0,s.Length-2);
      RealGeometryPart chosen=null; string why="";
      if(stem=="KIT00_BODY"){ // Fusion 2018 paint shell incl. its mirrors; drop synthetic opaque prisms and the (never drawn) grille group
        var b=ByName(v2,N("KIT00_BODY_"+lod));
        chosen=As(Rebuild(b,GroupsWhere(b,(sh,tx)=>tx!=OPAQUE_TEX&&tx!=GRILLE_TEX),null,false),orig,true); why="V2 BODY paint";
      } else if(stem=="BASE"){
        var b=ByName(v2,N("BASE_"+lod)); var keep=new List<int>();for(int g=0;g<b.PartData.Groups.Length;g++)keep.Add(g);
        chosen=As(Rebuild(b,keep.ToArray(),null,false),orig,true);
        // remove long spike triangles only inside the engine-bay INTERIOR-shader group
        var bb=chosen; var gi=GroupsWhere(bb,(sh,tx)=>sh==INTERIOR_SH);
        if(gi.Length>0){ var all=new List<int>();for(int g=0;g<bb.PartData.Groups.Length;g++)all.Add(g);
          var filtered=Rebuild(bb,gi,(x,y,z)=>Edge(x,y)>1.2f||Edge(y,z)>1.2f||Edge(z,x)>1.2f||Spike(x)||Spike(y)||Spike(z),false);
          var rest=Rebuild(bb,all.FindAll(g=>Array.IndexOf(gi,g)<0).ToArray(),null,false);
          chosen=As(Concat(rest,filtered),orig,true);}
        why="V2 BASE + AJM markers";
      } else if(stem=="KIT00_RIGHT_SIDE_MIRROR"){ // AJM trim/2010 mirrors -> Fusion 2018 grille (moved out of BODY)
        var b=ByName(v2,N("KIT00_BODY_"+lod)); var g=GroupsWhere(b,(sh,tx)=>tx==GRILLE_TEX);
        chosen=g.Length>0?As(Rebuild(b,g,null,true),orig,false):As(Clone(placeholder),orig,false); why="V2 grille two-sided";
      } else if(stem=="KIT00_RIGHT_HEADLIGHT"||stem=="KIT00_RIGHT_BRAKELIGHT"){
        string kind=stem.Contains("HEAD")?"HEADLIGHT":"BRAKELIGHT";
        var r=ByName(v2,N("KIT00_RIGHT_"+kind+"_"+lod));var l=ByName(v2,N("KIT00_LEFT_"+kind+"_"+lod));
        var m=Concat(Clone(r),Clone(l));
        if(dull){for(int k=0;k<m.PartInfo.Shaders.Length;k++)if(m.PartInfo.Shaders[k]==BRAKELIGHT)m.PartInfo.Shaders[k]=DULL;}
        chosen=As(m,orig,false); why="V2 2018 lamps L+R (two-sided)"+(dull?" DULLPLASTIC":"");
      } else if(stem.EndsWith("_GLASS")||stem=="KIT00_REAR_WINDOW"||stem=="KIT00_SPOILER"||stem=="KIT00_LEFT_SIDE_MIRROR"){
        chosen=As(Clone(placeholder),orig,false); why="placeholder (2010 part removed)";
      } else if(stem=="KIT00_FRONT_WINDOW"||stem=="KIT00_INTERIOR"){
        chosen=As(ByName(v2,N(stem+"_"+lod)),orig,false); why="V2 "+stem;
      } else if(stem=="KIT00_DRIVER"){
        chosen=As(ByName(v1,name),orig,false); why="V1 driver (aligned to 2018 seat)";
      } else {
        chosen=Clone(orig); // AJM tires, brakes, KIT01/02 plates
        for(int k=0;k<chosen.PartInfo.Textures.Length;k++)if(chosen.PartInfo.Textures[k]==AJM_INTERIOR&&(stem.Contains("TIRE")||stem.Contains("BRAKE"))){chosen.PartInfo.Textures[k]=ajmInteriorNew;why="AJM, tex remapped ";}
        Finish(chosen); why+="AJM original";
      }
      output.AddPart(chosen);
      log.Add(string.Format("{0,-42} idx={1,6} v={2,6} g={3} {4}",name,chosen.PartData.Indices.Length,chosen.PartData.Vertices.Length,chosen.PartData.Groups.Length,why));
    }
    output.GeometryInfo.PartCount=output.PartCount; output.Save(args[3]);
    foreach(var l in log)Console.WriteLine(l);
    Console.WriteLine("AJM_INTERIOR hash="+ajmInteriorNew.ToString("X8")+" parts="+output.PartCount);
  }
}
