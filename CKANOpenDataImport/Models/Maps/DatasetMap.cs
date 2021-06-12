using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CKANOpenDataImport.Models.Output;
using CsvHelper.Configuration;

namespace CKANOpenDataImport.Models
{
    public sealed class DatasetMap : ClassMap<DatasetEntry>
    {
        public DatasetMap()
        {
            Map(x => x.Title).Name("Title");
            Map(x => x.Owner).Name("Owner");
            Map(x => x.PageURL).Name("PageURL");
            Map(x => x.AssetURL).Name("AssetURL");
            Map(x => x.DateCreated).Name("DateCreated");
            Map(x => x.DateUpdated).Name("DateUpdated");
            Map(x => x.FileSize).Name("FileSize");
            Map(x => x.FileType).Name("FileType");
            Map(x => x.NumRecords).Name("NumRecords");
            Map(x => x.Tags).Name("Tags");
            Map(x => x.License).Name("License");
            Map(x => x.Description).Name("Description");
        }
    }
}
