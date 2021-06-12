using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using CKANOpenDataImport.Models;
using CKANOpenDataImport.Models.Output;
using Figgle;
using Newtonsoft.Json;
using RestSharp;
using JsonSerializer = System.Text.Json.JsonSerializer;

namespace CKANOpenDataImport
{
    internal class Program
    {
        private const string PACKAGE_LIST_PATH = "api/3/action/package_list";
        private const string PACKAGE_SHOW_PATH = "api/3/action/package_show";
        public static List<DatasetEntry> DatasetEntries { get; set; } = new List<DatasetEntry>();

        // ReSharper disable once UnusedParameter.Local
        private static void Main(string[] args)
        {
            Console.WriteLine(FiggleFonts.Standard.Render("CKAN OD Import v0.1"));

            var urlPath = Path.Combine(Directory.GetCurrentDirectory(), "urls.json");

            Console.WriteLine($"Reading CKAN URLs from {urlPath}");

            var urlsJson = File.ReadAllText(urlPath);

            Console.WriteLine("Parsing JSON file...");

            var ckanRootUrls = JsonConvert.DeserializeObject<List<CKANRootUrl>>(urlsJson);

            if (ckanRootUrls == null)
            {
                Console.WriteLine("No URLs found");
                Environment.Exit(-1);
            }

            Console.WriteLine($"Got {ckanRootUrls.Count} URLs from file");

            Console.WriteLine("Press any key to start processing URLs");
            Console.ReadLine();

            Console.WriteLine("Processing URLs:");
            foreach (var ckanRootUrl in ckanRootUrls)
            {
                Console.WriteLine();
                Console.WriteLine($"Running for instance: {ckanRootUrl.SourceName}");
                Console.WriteLine($"Root URL is {ckanRootUrl.Url}");

                var client = new RestClient(ckanRootUrl.Url);

                Console.WriteLine("Getting packages list...");
                var packagesRequest = new RestRequest(PACKAGE_LIST_PATH);
                var packagesResponse = client.Execute(packagesRequest);

                if (!packagesResponse.IsSuccessful)
                {
                    Console.WriteLine($"ERROR: Could not get packages list for instance. Got response {packagesResponse.StatusCode}");
                    Console.WriteLine("Skipping...");

                    continue;
                }

                var packages = JsonConvert.DeserializeObject<CKANPackagesListResponse>(packagesResponse.Content);

                if (packages == null)
                {
                    Console.WriteLine($"ERROR: No packages retrieved");
                    Console.WriteLine("Skipping...");

                    continue;
                }

                Console.WriteLine($"{packages.Result.Count()} packages retrieved");
                Console.WriteLine("Processing packages...");

                foreach (var package in packages.Result)
                {
                    var showPackageRequest = new RestRequest(PACKAGE_SHOW_PATH);
                    showPackageRequest.AddParameter("id", package);
                    var showPackageResponse = client.Execute(showPackageRequest);

                    if (!showPackageResponse.IsSuccessful)
                    {
                        Console.WriteLine($"ERROR: Could not get package metadata for {package}. Got response {showPackageResponse.StatusCode}");
                        Console.WriteLine("Skipping...");

                        continue;
                    }

                    var parsedPackageResponse =
                        JsonConvert.DeserializeObject<CKANPackageResponse>(showPackageResponse.Content);

                    if (parsedPackageResponse == null)
                    {
                        Console.WriteLine($"ERROR: Could not parse package");
                        Console.WriteLine("Skipping...");

                        continue;
                    }

                    var packageMetadata = parsedPackageResponse.Result;

                    var newEntry = new DatasetEntry
                    {
                        Title = packageMetadata.Title,
                        Owner = ckanRootUrl.SourceName,
                        PageURL = $"{ckanRootUrl.Url}/dataset/{package}",
                        AssetURL = null,
                        DateCreated = packageMetadata.DateCreated,
                        DateUpdated = packageMetadata.DateModified,
                        FileSize = null,
                        FileType = null,
                        NumRecords = null,
                        Tags = null,
                        License = packageMetadata.License
                    };

                    DatasetEntries.Add(newEntry);

                    //Console.WriteLine($"\t {package}");
                    //DatasetEntries.Add(new DatasetEntry(){Title = package});
                }
                //Console.WriteLine();
                //Console.ReadLine();
            }
            
            Console.WriteLine();
            Console.WriteLine($"Package total: {DatasetEntries.Count} packages from {ckanRootUrls.Count} CKAN instances");
        }
    }
}
