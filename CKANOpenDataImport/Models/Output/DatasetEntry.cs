using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CKANOpenDataImport.Models.Output
{
    public class DatasetEntry
    {
        public string Title { get; set; }
        public string Owner { get; set; }
        public string PageURL { get; set; }
        public string AssetURL { get; set; }
        public DateTime? DateCreated { get; set; }
        public DateTime? DateUpdated { get; set; }
        public string FileSize { get; set; }
        public string FileType { get; set; }
        public int? NumRecords { get; set; }
        public string Tags { get; set; }
        public string License { get; set; }
        public string Description { get; set; }
    }
}
