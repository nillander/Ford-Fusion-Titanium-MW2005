using System;
using System.IO;
using mwgc.RealEngine;
class DumpParts {
  static void Main(string[] args) {
    var f = new RealGeometryFile(); f.Open(args[0]);
    foreach (RealGeometryPart p in f) {
      string tex = "";
      if (p.PartInfo.Textures != null) foreach (uint t in p.PartInfo.Textures) tex += t.ToString("X8") + " ";
      string sh = "";
      if (p.PartInfo.Shaders != null) foreach (uint s in p.PartInfo.Shaders) sh += s.ToString("X8") + " ";
      Console.WriteLine("{0}\ttris={1}\tverts={2}\tflags=0x{3:X}\tsh={4}\ttex={5}\tunk1=0x{6:X}\tunk5={7}\tunk6={8}\tgroups={9}\tmat={10}",
        p.PartInfo.PartName, p.PartData.TriangleCount, p.PartData.VertexCount, p.PartData.Flags,
        sh.Trim(), tex.Trim(), p.PartInfo.Unk1, p.PartInfo.Unk5_MW, p.PartInfo.Unk6_MW, p.PartData.GroupCount,
        p.PartData.Materials==null?0:p.PartData.Materials.Count);
    }
  }
}
