using System;
using System.IO;
using mwgc.RealEngine;

// Replace only matching rear-lamp solids. Reject absent/unexpected names so
// a rebuild cannot silently drop a source mesh or regress the rest of the car.
public class ReplaceRearLights {
    static RealGeometryFile Read(string path) {
        byte[] bytes = File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile(); file.Open(new MemoryStream(bytes)); return file;
    }
    public static void Main(string[] args) {
        var original = Read(args[0]); var lamps = Read(args[1]);
        var result = new RealGeometryFile(); result.GeometryInfo = original.GeometryInfo;
        foreach (RealGeometryPart lamp in lamps) {
            if (!lamp.PartInfo.PartName.ToString().Contains("_BRAKELIGHT_") || original[lamp.PartInfo.Hash] == null)
                throw new Exception("Unknown rear light slot: " + lamp.PartInfo.PartName);
        }
        int changed = 0;
        foreach (RealGeometryPart part in original) {
            var replacement = lamps[part.PartInfo.Hash]; var chosen = replacement ?? part;
            if (replacement != null) changed++;
            for (int i = 0; i < chosen.PartData.Vertices.Length; i++) chosen.PartData.Vertices[i].Initialize(true, 0);
            result.AddPart(chosen);
        }
        if (changed != 8 || lamps.PartCount != 8) throw new Exception("Expected exactly eight rear light solids");
        result.GeometryInfo.PartCount = result.PartCount; result.Save(args[2]);
        Console.WriteLine("Replaced rear light solids: " + changed + "; total: " + result.PartCount);
    }
}
