using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Text.Json;
using Common;
using Common.Geometry.Data;
using Common.Textures.Data;

// Geometry validation does not require decompression. Reject unexpected compressed resources explicitly.
namespace Common {
    public static class Compression {
        public static Span<byte> Decompress(ReadOnlySpan<byte> input) {
            if(input[..4].SequenceEqual("RAWW"u8))return input[16..].ToArray();
            if(input[..4].SequenceEqual("JDLZ"u8))return NFSTools.LibNFS.Compression.JDLZ.decompress(input.ToArray());
            throw new NotSupportedException("Unsupported compression signature");
        }
        public static long DecompressCip(Stream src,Stream dst,long size) {throw new NotSupportedException("Compressed resources are not supported by the geometry validator.");}
    }
}
class Program {
    static void Main(string[] args) {
        bool isTexture=args[0].EndsWith("TEXTURES.BIN",StringComparison.OrdinalIgnoreCase);
        string readPath=args[0];string temporaryPath=null;
        if(!isTexture) {
            // mwgc writes the retail layout: a short catalogue followed by sibling
            // solid chunks. NFS-ModTools expects those siblings nested for parsing.
            byte[] bytes=File.ReadAllBytes(args[0]);
            BitConverter.GetBytes(bytes.Length-8).CopyTo(bytes,4);
            temporaryPath=Path.GetTempFileName();File.WriteAllBytes(temporaryPath,bytes);
            readPath=temporaryPath;
        }
        var cm=new ChunkManager(GameDetector.Game.MostWanted);
        try { cm.Read(readPath); }
        finally { if(temporaryPath!=null)File.Delete(temporaryPath); }
        if(isTexture) {
            var textures=cm.Chunks.Where(c=>c.Resource is TexturePack).SelectMany(c=>((TexturePack)c.Resource).Textures).ToList();
            if(textures.Count==0)throw new Exception("No textures parsed");
            Directory.CreateDirectory(args[2]);
            foreach(var t in textures) {
                if(t.Data.Length!=t.DataSize)throw new Exception("Truncated texture");
                var minBytes=((t.Width+3)/4)*((t.Height+3)/4)*(t.Format==0x31545844?8:16);
                if(t.DataSize<minBytes)throw new Exception("Incomplete top mip: "+t.Name);
                t.DumpToFile(Path.Combine(args[2],t.TexHash.ToString("X8")+".dds"));
            }
            File.WriteAllText(args[1],JsonSerializer.Serialize(new{passed=true,count=textures.Count,textures=textures.Select(t=>new{t.Name,t.TexHash,t.Width,t.Height,t.DataSize,t.MipMapCount,t.Format})},new JsonSerializerOptions{WriteIndented=true}));
            Console.WriteLine("Independent TPK read passed: "+textures.Count+" textures");return;
        }
        var solids=cm.Chunks.Where(c=>c.Resource is SolidList).SelectMany(c=>((SolidList)c.Resource).Objects).ToList();
        if(solids.Count==0)throw new Exception("No solids parsed");
        var records=new List<object>();int triangles=0;
        foreach(var s in solids) {
            int tris=0;
            foreach(var m in s.Materials) {
                var vs=s.VertexSets[m.VertexSetIndex];
                foreach(var i in m.Indices)if(i>=vs.Count)throw new Exception("Invalid index in "+s.Name);
                if(m.Indices.Length%3!=0)throw new Exception("Incomplete triangle");
                tris+=m.Indices.Length/3;
                foreach(var v in vs) {
                    if(!float.IsFinite(v.Position.X)||!float.IsFinite(v.Position.Y)||!float.IsFinite(v.Position.Z))throw new Exception("Non-finite vertex");
                }
            }
            triangles+=tris;records.Add(new{name=s.Name,hash=s.Hash,triangles=tris,vertices=s.VertexSets.Sum(v=>v.Count),materials=s.Materials.Count});
        }
        if(solids.Select(s=>s.Hash).Distinct().Count()!=solids.Count)throw new Exception("Duplicate part hash");
        File.WriteAllText(args[1],JsonSerializer.Serialize(new {reader="NFSTools/NFS-ModTools MostWantedSolidReader",parts=records,triangles=triangles,passed=true},new JsonSerializerOptions{WriteIndented=true}));
        Console.WriteLine("Independent read passed: "+solids.Count+" parts, "+triangles+" triangles");
    }
}
