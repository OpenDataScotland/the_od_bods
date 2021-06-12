using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using CKANOpenDataImport.Models;
using Figgle;
using Newtonsoft.Json;
using RestSharp;
using JsonSerializer = System.Text.Json.JsonSerializer;

namespace CKANOpenDataImport
{
    internal class Program
    {
        private const string PACKAGE_LIST_PATH = "api/3/action/package_list";

        // ReSharper disable once UnusedParameter.Local
        private static void Main(string[] args)
        {
            Console.WriteLine(FiggleFonts.Standard.Render("CKAN OD Import v0.1"));

            var urlPath = Path.Combine(Directory.GetCurrentDirectory(),"urls.json");

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

            Console.WriteLine("Processing URLs:\n");
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

                var packages =  JsonConvert.DeserializeObject<CKANPackagesListResponse>(packagesResponse.Content);

                if (packages == null)
                {
                    Console.WriteLine($"ERROR: No packages retrieved");
                    Console.WriteLine("Skipping...");

                    continue;
                }

                Console.WriteLine($"{packages.Result.Count()} packages retrieved");
            }
        }
    }
}
