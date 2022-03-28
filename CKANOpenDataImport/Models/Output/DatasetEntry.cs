namespace CKANOpenDataImport.Models.Output
{
    public class DatasetEntry
    {
        public string Title { get; set; }
        public string Owner { get; set; }
        public string PageURL { get; set; }
        public string AssetURL { get; set; }
        public string DateCreated { get; set; }
        public string DateUpdated { get; set; }
        public string FileName { get; set; }
        public string FileSize { get; set; }
        public string FileSizeUnit { get; set; }
        public string FileType { get; set; }
        public int? NumRecords { get; set; }
        public string OriginalTags { get; set; }
        public string ManualTags { get; set; }  
        public string License { get; set; }
        public string Description { get; set; }
    }
}
