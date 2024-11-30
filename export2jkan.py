import os
import shutil
import urllib
import markdown
import pandas as pd
import yaml
from utils.export2jkan_functions import (
    DataFile,
    Dataset,
    find_field_index,
    get_licence_url,
    safe_parse_int,
    split_tags,
    strip_date_from_iso8601,
)


def main():
    """
    Main function to process and export datasets to JKAN.
    This function performs the following steps:
    1. Reads merged data from a JSON file.
    2. Cleans the date fields in the data.
    3. Iterates over the records (individual data files) to create dataset objects.
    4. Merges records into datasets using a unique identifier.
    5. Updates the JKAN datasets folder by removing the existing datasets folder and creating a new empty one for populating.
    6. Writes each dataset to a YAML file in the JKAN datasets folder.
    Raises:
        FileNotFoundError: If the input JSON file is not found.
        OSError: If there is an error removing or creating directories.
    """

    merged_data = pd.read_json("data/merged_output.json", orient="records").fillna("")

    # CLEAN: Strip the date from the ISO8601 format
    strip_date_from_iso8601(merged_data, ["DateCreated", "DateUpdated"])

    # Create an empty dictionary to store the merged datasets
    merged_datasets = {}

    # Iterate over the records of the merged output and create a dataset object for each
    # Each record is a file in a dataset. These can be merged into a single dataset object by using the page URL and title as a unique identifier
    for record in merged_data.values:

        # Create a unique identifier for the dataset using the page URL and title
        dataset_identifier = (
            str(record[find_field_index("PageURL")]) + record[find_field_index("Title")]
        )

        # If the dataset is not already in the merged datasets, create a new dataset object
        if dataset_identifier not in merged_datasets:
            merged_dataset = Dataset(
                title=record[find_field_index("Title")],
                owner=record[find_field_index("Owner")],
                page_url=record[find_field_index("PageURL")],
                date_created=record[find_field_index("DateCreated")],
                date_updated=record[find_field_index("DateUpdated")],
                ods_categories=split_tags(record[find_field_index("ODSCategories")]),
                license=record[find_field_index("License")],
                description=str(record[find_field_index("Description")]),
                num_records=safe_parse_int(record[find_field_index("NumRecords")]),
                files=[],
            )

            # Sort categories to keep consistent when syncing
            merged_dataset.ods_categories.sort()

            # Add the dataset to the merged datasets
            merged_datasets[dataset_identifier] = merged_dataset

        # Add the file to the dataset
        merged_datasets[dataset_identifier].files.append(
            DataFile(
                url=record[find_field_index("AssetURL")],
                size=record[find_field_index("FileSize")],
                size_unit=record[find_field_index("FileSizeUnit")],
                file_type=record[find_field_index("FileType")],
                file_name=record[find_field_index("FileName")],
                show_name=(
                    record[find_field_index("FileName")]
                    if record[find_field_index("FileName")]
                    else record[find_field_index("FileType")]
                ),
            )
        )

    # Update the JKAN datasets folder by removing the existing datasets folder and creating a new empty one for populating
    print(f"Current working directory: {os.getcwd()}")
    shutil.rmtree("../jkan/_datasets/")
    os.makedirs("../jkan/_datasets/")

    # Iterate over the merged datasets and create a YAML file for each
    for index, (merged_dataset_key, merged_dataset) in enumerate(
        merged_datasets.items()
    ):

        # Build the dataset YAML content
        dataset_yaml_content = {"schema": "default"}
        # CLEAN: Sentence case for presentability
        dataset_yaml_content["title"] = (
            merged_dataset.title[0].upper() + merged_dataset.title[1:]
        )
        dataset_yaml_content["organization"] = merged_dataset.owner
        dataset_yaml_content["notes"] = markdown.markdown(merged_dataset.description)
        dataset_yaml_content["original_dataset_link"] = merged_dataset.page_url
        dataset_yaml_content["resources"] = [
            {
                "name": data_file.show_name,
                "url": data_file.url,
                "format": data_file.file_type,
            }
            for data_file in merged_dataset.files
            if data_file.url
        ]
        dataset_yaml_content["license"] = get_licence_url(merged_dataset.license)
        dataset_yaml_content["category"] = merged_dataset.ods_categories
        dataset_yaml_content["maintainer"] = merged_dataset.owner
        dataset_yaml_content["date_created"] = merged_dataset.date_created
        dataset_yaml_content["date_updated"] = merged_dataset.date_updated
        dataset_yaml_content["records"] = merged_dataset.num_records

        # Generate dataset file name by concatenating the owner and title in lowercase
        # Url encode the file name to handle special characters
        # TODO: Do we need to handle instances where there are duplicates between owners and titles? e.g. the same dataset "hosted" by different portals
        dataset_file_name = urllib.parse.quote_plus(
            f"{(merged_dataset.owner).lower()}-{(merged_dataset.title).lower()}"
        )

        # Write the dataset YAML content to a file
        with open(f"../jkan/_datasets/{dataset_file_name}.md", "w") as f:
            print(f" Writing {os.path.abspath(f.name)}")
            f.write("---\n")
            f.write(yaml.dump(dataset_yaml_content))
            f.write("---\n")


if __name__ == "__main__":
    main()
