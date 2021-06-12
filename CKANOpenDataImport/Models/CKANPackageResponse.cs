using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace CKANOpenDataImport.Models
{
    public class CKANPackageResponse
    {
        public bool? Success { get; set; }
        public CKANPackageResponseResult Result { get; set; }
    }

    public class CKANPackageResponseResult
    {
        public string Title { get; set; }
        [JsonProperty("metadata_created")]
        public DateTime? DateModified { get; set; }
        [JsonProperty("metadata_modified")]
        public DateTime? DateCreated { get; set; }
        [JsonProperty("Notes")]
        public string Description { get; set; }
        [JsonProperty("license_title")]
        public string License { get; set; }
    }
}
