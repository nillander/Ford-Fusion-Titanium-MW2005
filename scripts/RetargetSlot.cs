using System;
using System.IO;
using mwgc.RealEngine;

public class RetargetSlot {
    static uint RealHash(string value) {
        uint hash = uint.MaxValue;
        foreach (char character in value) {
            hash *= 33;
            hash += (uint)character;
        }
        return hash;
    }

    static RealGeometryFile Read(string path) {
        byte[] bytes = File.ReadAllBytes(path);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length - 8), 0, bytes, 4, 4);
        var file = new RealGeometryFile();
        file.Open(new MemoryStream(bytes));
        return file;
    }

    public static void Main(string[] args) {
        var geometry = Read(args[0]);
        string sourceSlot = args[2];
        string targetSlot = args[3];
        string sourcePrefix = sourceSlot + "_";
        int changed = 0;
        foreach (RealGeometryPart part in geometry) {
            string name = part.PartInfo.PartName.ToString();
            if (!name.StartsWith(sourcePrefix)) continue;
            string retargeted = targetSlot + name.Substring(sourceSlot.Length);
            part.PartInfo.PartName = new FixedLenString(retargeted);
            part.PartInfo.Hash = RealHash(retargeted);
            changed++;
        }
        geometry.GeometryInfo.PartCount = geometry.PartCount;
        geometry.Save(args[1]);
        Console.WriteLine("Retargeted " + changed + " parts " + sourceSlot + " -> " + targetSlot);
    }
}
