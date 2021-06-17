using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using CKANOpenDataImport.Models;
using CKANOpenDataImport.Models.Output;
using CsvHelper;
using CsvHelper.Configuration;
using Figgle;
using Newtonsoft.Json;
using RestSharp;

namespace CKANOpenDataImport
{
    internal class Program
    {
        private const string PACKAGE_LIST_PATH = "api/3/action/package_list";
        private const string PACKAGE_SHOW_PATH = "api/3/action/package_show";
        public static List<DatasetEntry> DatasetEntries { get; set; } = new();

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
                    Console.WriteLine("ERROR: No packages retrieved");
                    Console.WriteLine("Skipping...");

                    continue;
                }

                Console.WriteLine($"{packages.Result.Count()} packages retrieved");
                Console.WriteLine("Processing packages...");

                foreach (var package in packages.Result)
                {
                    Console.WriteLine($"Processing {package}...");
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
                        Console.WriteLine("ERROR: Could not parse package");
                        Console.WriteLine("Skipping...");

                        continue;
                    }

                    var packageMetadata = parsedPackageResponse.Result;

                    if (!packageMetadata.Type.Equals("dataset"))
                    {
                        Console.WriteLine($"ERROR: Package type {packageMetadata.Type} is not a recognized dataset");
                        Console.WriteLine("Skipping...");
                        continue;
                    }

                    Console.WriteLine($"Package has {packageMetadata.Resources.Count()} assets");

                    foreach (var resource in packageMetadata.Resources)
                    {
                        var newEntry = new DatasetEntry
                        {
                            Title = packageMetadata.Title,
                            Owner = ckanRootUrl.SourceName,
                            PageURL = $"{ckanRootUrl.Url}dataset/{package}",
                            AssetURL = resource.URL,
                            DateCreated = packageMetadata.DateCreated.HasValue ? packageMetadata.DateCreated.Value.ToString("yyyy-MM-dd") : "",
                            DateUpdated = packageMetadata.DateModified.HasValue ? packageMetadata.DateModified.Value.ToString("yyyy-MM-dd") : "",
                            FileSize = resource.Archiver != null ? resource.Archiver.Size.ToString() : "",
                            FileSizeUnit = resource.Archiver != null ? "B": "",
                            FileType = resource.Format,
                            NumRecords = null,
                            OriginalTags = string.Join(';', packageMetadata.Tags.Select(x => x.Name)),
                            ManualTags = null,
                            License = packageMetadata.License,
                            Description = packageMetadata.Description
                        };

                        DatasetEntries.Add(newEntry);
                    }
                }
            }

            var datasetCount = DatasetEntries.GroupBy(x => new { x.Title, x.Owner }).Count();

            Console.WriteLine();
            Console.WriteLine($"Total: {DatasetEntries.Count} assets from {datasetCount} datasets stored across {ckanRootUrls.Count} CKAN instances");

            Console.WriteLine();
            var csvPath = Path.Combine(Directory.GetCurrentDirectory(), "ckan_output.csv");
            Console.WriteLine($"Writing CSV to {csvPath}");

            using StreamWriter sw = new(csvPath, false, new UTF8Encoding(true));
            using CsvWriter cw = new(sw, new CsvConfiguration(CultureInfo.CurrentCulture));

            cw.WriteHeader<DatasetEntry>();
            cw.NextRecord();
            foreach (var entry in DatasetEntries)
            {
                cw.WriteRecord(entry);
                cw.NextRecord();
            }
        }
    }
}
