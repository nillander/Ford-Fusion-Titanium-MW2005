using System;
using System.IO;
using mwgc.RealEngine;

// Controlled test: change only the lamp material, retaining the compiled mesh,
// atlas, UV coordinates and BASE attachment. Input must be the lamp checkpoint.
class ProbeLampMaterial {
    static void Main(string[] args) {
        var bytes=File.ReadAllBytes(args[0]);
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
        var file=new RealGeometryFile();file.Open(new MemoryStream(bytes));
        uint replacement=Convert.ToUInt32(args[2],16);int changed=0;
        foreach(RealGeometryPart p in file) {
            for(int i=0;i<p.PartData.Vertices.Length;i++)p.PartData.Vertices[i].Initialize(true,0);
            if(!p.PartInfo.PartName.ToString().Contains("_BASE_"))continue;
            for(int i=0;i<p.PartInfo.Shaders.Length;i++)
                if(p.PartInfo.Shaders[i]==0x05BC3A3Cu){p.PartInfo.Shaders[i]=replacement;changed++;}
        }
        if(changed!=4)throw new Exception("Expected exactly four BASE lamp shader entries");
        file.Save(args[1]);Console.WriteLine("Changed only lamp shader: "+replacement.ToString("X8"));
    }
}
