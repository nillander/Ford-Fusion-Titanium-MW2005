using System;
using System.IO;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using mwgc.RealEngine;
public class InspectGeometry {
    public static void Main(string[] args) {
        byte[] bytes=File.ReadAllBytes(args[0]);
        // Retail GEOMETRY.BIN keeps the catalogue and solid chunks as siblings.
        // The legacy reader expects them nested under the first root chunk.
        Buffer.BlockCopy(BitConverter.GetBytes(bytes.Length-8),0,bytes,4,4);
        var f = new RealGeometryFile(); f.Open(new MemoryStream(bytes));
        var data = new List<object>();
        foreach (RealGeometryPart p in f) {
            data.Add(new {name=p.PartInfo.PartName.ToString(), info=p.PartInfo, mesh=p.PartData});
            Console.WriteLine(p.PartInfo.PartName+" vertices="+p.PartData.VertexCount+" triangles="+p.PartData.TriangleCount);
        }
        var j = new JavaScriptSerializer(); j.MaxJsonLength=int.MaxValue;
        File.WriteAllText(args[1], j.Serialize(data));
    }
}
