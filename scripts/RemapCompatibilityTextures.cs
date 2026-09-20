using System;
using System.IO;
using mwgc.RealEngine;

public class RemapCompatibilityTextures {
    static RealGeometryFile Read(string path) {
        byte[] bytes=File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
        var file=new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        return file;
    }

    static bool IsFusionTexture(uint hash) {
        return (hash & 0xFFFFFF00u)==0xCBADCA00u;
    }

    static uint Replacement(string partName,uint hash) {
        // These hashes already exist in the working donor pack and are known
        // to be resolved by the retail game.
        if(partName.Contains("_WINDOW_")) return 0x7B220DDFu;
        if(partName.Contains("_HEADLIGHT_GLASS_")) return 0x95DE5B23u;
        if(partName.Contains("_BRAKELIGHT_GLASS_")) return 0x95DE5B23u;
        if(partName.Contains("_HEADLIGHT_")) return 0x4B7D95B6u;
        if(partName.Contains("_BRAKELIGHT_")) return 0x4B7D95B6u;
        if(hash==0xCBADCA49u) return 0x339D0D44u; // source licence plate
        return 0x2AF3D244u; // opaque donor interior texture
    }

    static uint KnownPartReplacement(string partName,uint hash) {
        const uint compiledHeadlight=0x6A9A946Du;
        if(partName.Contains("_TIRE_") && hash==0x2AF3D244u) return 0x0A7C3B20u;
        if(partName.Contains("_WINDOW_") && hash==compiledHeadlight) return 0x7B220DDFu;
        if(partName.Contains("_BRAKELIGHT_") && hash==compiledHeadlight) return 0x4B7D95B6u;
        if(partName.Contains("_HEADLIGHT_") && hash==compiledHeadlight) return 0x95DE5B23u;
        if(hash==compiledHeadlight) return 0x95DE5B23u;
        return hash;
    }

    public static void Main(string[] args) {
        var geometry=Read(args[0]);
        int changed=0;
        foreach(RealGeometryPart part in geometry) {
            if(part.PartInfo.Textures==null) continue;
            string name=part.PartInfo.PartName.ToString();
            bool frontLight=name.Contains("_HEADLIGHT_");
            bool rearLight=name.Contains("_BRAKELIGHT_");
            if((frontLight || rearLight) && false) {
                uint solidTexture=frontLight ? 0x68EF82F9u : 0x680D9D7Au;
                if(part.PartInfo.Shaders!=null) {
                    for(int i=0;i<part.PartInfo.Shaders.Length;i++) {
                        if(part.PartInfo.Shaders[i]!=0x0FEDEE40u) changed++;
                        part.PartInfo.Shaders[i]=0x0FEDEE40u;
                    }
                }
                for(int i=0;i<part.PartInfo.Textures.Length;i++) {
                    if(part.PartInfo.Textures[i]!=solidTexture) changed++;
                    part.PartInfo.Textures[i]=solidTexture;
                }
                continue;
            }
            if(name.Contains("_TIRE_") && part.PartInfo.Shaders!=null) {
                for(int i=0;i<part.PartInfo.Shaders.Length;i++) {
                    if(part.PartInfo.Shaders[i]==0xC83DAC78u || part.PartInfo.Shaders[i]==0x0FEDEE40u) {
                        // Main opaque rim shader used by stock and shop wheels.
                        part.PartInfo.Shaders[i]=0x22719FA9u;
                        changed++;
                    }
                }
            }
            for(int i=0;i<part.PartInfo.Textures.Length;i++) {
                uint hash=part.PartInfo.Textures[i];
                uint replacement=IsFusionTexture(hash) ? Replacement(name,hash) : KnownPartReplacement(name,hash);
                if(replacement!=hash) {
                    part.PartInfo.Textures[i]=replacement;
                    changed++;
                }
            }
        }
        geometry.GeometryInfo.PartCount=geometry.PartCount;
        geometry.Save(args[1]);
        Console.WriteLine("Remapped "+changed+" texture slots to donor-compatible hashes");
    }
}
