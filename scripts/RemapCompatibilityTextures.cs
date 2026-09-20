using System;
using System.IO;
using mwgc.RealEngine;

public class RemapCompatibilityTextures {
    const uint OpaquePainted = 0x22719FA9u;
    const uint HeadlightAtlas = 0x95DE5B23u;
    const uint BrakelightAtlas = 0x4B7D95B6u;
    const uint RimAtlas = 0x0A7C3B20u;
    const uint WindowGlass = 0x7B220DDFu;
    const uint ChromeA = 0xC83DAC78u;
    const uint ChromeB = 0x0FEDEE40u;
    const uint OfficialHeadlight = 0x12C9453Cu;
    const uint OfficialBrakelight = 0x05BC3A3Cu;
    const uint MissingHeadlight = 0xA532FC46u;
    const uint MissingGlass = 0xF68EF19Fu;

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

    static bool IsDroppedChrome(uint shader) {
        return shader==ChromeA || shader==ChromeB || shader==OfficialHeadlight || shader==OfficialBrakelight;
    }

    static uint Replacement(string partName,uint hash) {
        if(partName.Contains("_WINDOW_")) return WindowGlass;
        if(partName.Contains("_HEADLIGHT_")) return HeadlightAtlas;
        if(partName.Contains("_BRAKELIGHT_")) return BrakelightAtlas;
        if(partName.Contains("_TIRE_")) return RimAtlas;
        if(hash==0xCBADCA49u) return 0x339D0D44u;
        return 0x2AF3D244u;
    }

    static uint KnownPartReplacement(string partName,uint hash) {
        const uint compiledHeadlight=0x6A9A946Du;
        if(hash==MissingHeadlight || hash==MissingGlass) {
            if(partName.Contains("_BRAKELIGHT_")) return BrakelightAtlas;
            return HeadlightAtlas;
        }
        if(partName.Contains("_TIRE_") && hash==0x2AF3D244u) return RimAtlas;
        if(partName.Contains("_WINDOW_") && hash==compiledHeadlight) return WindowGlass;
        if(partName.Contains("_BRAKELIGHT_") && hash==compiledHeadlight) return BrakelightAtlas;
        if(partName.Contains("_HEADLIGHT_") && hash==compiledHeadlight) return HeadlightAtlas;
        if(hash==compiledHeadlight) return HeadlightAtlas;
        return hash;
    }

    public static void Main(string[] args) {
        var geometry=Read(args[0]);
        int changed=0;
        foreach(RealGeometryPart part in geometry) {
            if(part.PartInfo.Textures==null) continue;
            string name=part.PartInfo.PartName.ToString();
            if(part.PartInfo.Shaders!=null) {
                for(int i=0;i<part.PartInfo.Shaders.Length;i++) {
                    if(IsDroppedChrome(part.PartInfo.Shaders[i])) {
                        part.PartInfo.Shaders[i]=OpaquePainted;
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
        Console.WriteLine("Remapped "+changed+" shader/texture slots to painted Fusion hashes");
    }
}
