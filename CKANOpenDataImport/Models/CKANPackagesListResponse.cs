using System.Collections.Generic;

namespace CKANOpenDataImport.Models
{
    public class CKANPackagesListResponse
    {
        public bool? Success { get; set; }
        public IEnumerable<string> Result { get; set; }
    }
}
