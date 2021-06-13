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
