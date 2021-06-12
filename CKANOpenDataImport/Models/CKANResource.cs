using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata;
using System.Text;
using System.Threading.Tasks;

namespace CKANOpenDataImport.Models
{
    public class CKANResource
    {
        public string Format { get; set; }
        public string Name { get; set; }
        public string URL { get; set; }
        public CKANArchiver Archiver { get; set; }  
    }
}
