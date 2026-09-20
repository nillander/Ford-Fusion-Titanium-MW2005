using System;
using System.IO;
using mwgc.RealEngine;
public class RemapSkinTexture {
    static RealGeometryFile Read(string path) {
        byte[] b=File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(b.Length-8),0,b,4,4);
        var f=new RealGeometryFile(); f.Open(new MemoryStream(b)); return f;
    }
    public static void Main(string[] args) {
        const uint from=0xCBADCA0Bu; // MUSTANGGT_F18_05
        const uint to=0x9A8AAD9Eu;   // MUSTANGGT_SKIN1
        var geom=Read(args[0]);
        int changed=0;
        foreach (RealGeometryPart part in geom) {
            if (part.PartInfo.Textures==null) continue;
            for (int index=0; index<part.PartInfo.Textures.Length; index++) {
                if (part.PartInfo.Textures[index]==from) {
                    part.PartInfo.Textures[index]=to;
                    changed++;
                }
            }
        }
        geom.GeometryInfo.PartCount=geom.PartCount;
        geom.Save(args[1]);
        Console.WriteLine("Remapped "+changed+" CARSKIN texture slots to MUSTANGGT_SKIN1");
    }
}
