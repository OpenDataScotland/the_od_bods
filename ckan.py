from processor import Processor

class ProcessorCKAN(Processor):
    def __init__(self):
        super().__init__(type="ckan")

    def get_datasets(self, portal_owner, start_url, fname):
        print(f"Processing {start_url}")

        url = start_url

        ### catch for missing trailing "/" in url
        if url[-1] != "/": 
            url = url + "/"            

        datasets = processor.get_json(f"{url}/api/3/action/package_list")

        print(f"Found {len(datasets['result'])} datasets")

        prepped = []
        for dataset_name in datasets['result']:
            dataset_metadata = processor.get_json(f"{url}/api/3/action/package_show?id={dataset_name}")

            print(f"Got {dataset_name} with success status: {dataset_metadata['success']}")

            dataset_metadata = dataset_metadata['result']

            ### gets provided owner name if exists, else uses the owner of the portal.
            if 'organization' in dataset_metadata and 'title' in dataset_metadata['organization']:
                    owner = dataset_metadata['organization']['title']
            else: owner = portal_owner

            for resource in dataset_metadata['resources']:
                tags = list(map(lambda x: x['name'], dataset_metadata['tags']))

                file_size = 0

                if 'archiver' in resource and 'size' in resource['archiver']:
                    file_size = resource['archiver']['size']

                prepped.append(
                    [
                        dataset_metadata['title'],  # Title
                        owner,  # Owner
                        f"{url}dataset/{dataset_name}",  # PageURL
                        resource['url'],  # AssetURL
                        resource['name'], # FileName
                        dataset_metadata["metadata_created"],  # DateCreated
                        dataset_metadata["metadata_modified"],  # DateUpdated  
                        file_size,  # FileSize
                        "B",  # FileSizeUnit
                        resource['format'],  # FileType
                        None,  # NumRecords
                        ';'.join(tags),  # OriginalTags
                        None,  # ManualTags
                        dataset_metadata['license_title'],  # License
                        dataset_metadata['notes'].encode('unicode_escape').decode()  # Description
                    ]
                )

            processor.write_csv(fname, prepped)

processor = ProcessorCKAN()
processor.process()
