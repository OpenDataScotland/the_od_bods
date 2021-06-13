using System;
using System.Collections.Generic;
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
        public string Type { get; set; }
        [JsonProperty("metadata_created")]
        public DateTime? DateModified { get; set; }
        [JsonProperty("metadata_modified")]
        public DateTime? DateCreated { get; set; }
        [JsonProperty("Notes")]
        public string Description { get; set; }
        [JsonProperty("license_title")]
        public string License { get; set; }
        [JsonProperty("tags")]
        public IEnumerable<CKANTag> Tags { get; set; }
        [JsonProperty("Resources")]
        public IEnumerable<CKANResource> Resources { get; set; }
    }
}
