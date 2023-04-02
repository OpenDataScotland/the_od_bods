import pandas as pd
import json

data = pd.read_csv("../data/merged_output.csv", lineterminator="\n")

### Reducing assets to datasets as per display in frontend (grouped by Title + PageURL)
data = data[
    [
        "Title",
        "Owner",
        "PageURL",
        "Description",
        "OriginalTags",
        "ManualTags",
        "ODSCategories",
        "ODSCategories_Keywords",
    ]
].drop_duplicates()

### Converting json string into dictionary
data["ODSCategories_Keywords"] = data["ODSCategories_Keywords"].apply(eval)

with open("../ODSCategories.json", "r") as json_file:
    ods_categories = json.load(json_file)

    ### Cleaning of ODSCategories.json file
    for cat in ods_categories:
        ods_categories[cat] = [keyword.lower() for keyword in ods_categories[cat]]
        ods_categories[cat].sort()
### Save cleaned file
with open("../ODSCategories.json", "w") as json_file:
    json.dump(ods_categories, json_file, indent=3)


### Number of datasets in each category
def categories_count(df_column):
    temp_df = data[[df_column]].copy()
    temp_df["categories"] = data[df_column].str.split(";")
    return (
        pd.DataFrame(
            temp_df[["categories"]]
            .explode("categories", ignore_index=True)
            .value_counts()
        )
        .reset_index()
        .rename(columns={0: df_column})
    )


cat_counts = categories_count("ODSCategories")


### Number of datasets with n categories (out of 16 possible categories)
asset_catcounts = (
    data["ODSCategories"].str.split(";").str.len().value_counts().sort_index()
)


### Keywords used in each category
cat_set = {}
for asset in data["ODSCategories_Keywords"]:
    for cat, keywords in asset.items():
        if cat in cat_set:
            cat_set[cat].extend(keywords)
        else:
            cat_set[cat] = keywords

for cat in cat_set:
    cat_set[cat] = [keyword.lower() for keyword in cat_set[cat]]

cat_set_aggregated = {}
for cat in cat_set:
    cat_set_aggregated[cat] = pd.Series(cat_set[cat]).value_counts().to_dict()


### Keywords not used in each category
cat_set_unused = {}
for cat in ods_categories:
    cat_set_unused[cat] = [
        k for k in ods_categories[cat] if k not in cat_set_aggregated[cat]
    ]


### Duplicate keywords in each category
cat_set_duped = {}
for cat in ods_categories:
    list_dupes = list(
        set([i for i in ods_categories[cat] if ods_categories[cat].count(i) >= 2])
    )
    if len(list_dupes) > 0:
        cat_set_duped[cat] = list_dupes

if len(cat_set_duped) < 1:
    cat_set_duped["No duplicates"] = 0


### Keywords in multiple categories
cat_set_multicat = {}
cat_set_multicat_temp = pd.DataFrame()
for cat in ods_categories:
    temp = pd.DataFrame(ods_categories[cat], columns=["keyword"])
    temp["cat"] = cat
    cat_set_multicat_temp = pd.concat(
        [cat_set_multicat_temp, temp], axis=0, ignore_index=True
    )

cat_set_multicat_temp["freq"] = cat_set_multicat_temp["keyword"].map(
    cat_set_multicat_temp["keyword"].value_counts()
)
cat_set_multicat_temp = cat_set_multicat_temp[cat_set_multicat_temp["freq"] > 1]

unique_keywords = list(set(cat_set_multicat_temp["keyword"]))
unique_keywords.sort()
for keyword in unique_keywords:
    cat_set_multicat[keyword] = list(
        set(cat_set_multicat_temp[cat_set_multicat_temp["keyword"] == keyword]["cat"])
    )

if len(cat_set_multicat) < 1:
    cat_set_multicat["No multi-category keywords"] = 0


### Uncategorised datasets
uncategorised_datasets = data.loc[
    data["ODSCategories"] == "Uncategorised", ["Title", "Description"]
].drop_duplicates()


### Writes results to log
output_filename = "health_categories_results.txt"
with open(output_filename, "w") as log_file:

    log_file.write("### Number of categories assigned to assets (out of 16) ###\n")
    log_file.write(asset_catcounts.to_string())

    log_file.write("\n\n")
    log_file.write("### Number of datasets in each category ###\n")
    log_file.write(cat_counts.to_string(header=False, index=False))

    log_file.write("\n\n")
    log_file.write("### Keywords used in each category ###\n")
    log_file.write(json.dumps(cat_set_aggregated, indent=2))

    log_file.write("\n\n")
    log_file.write("### Keywords not used in each category ###\n")
    log_file.write(json.dumps(cat_set_unused, indent=2))

    log_file.write("\n\n")
    log_file.write("### Duplicate keywords in each category ###\n")
    log_file.write(json.dumps(cat_set_duped, indent=2))

    log_file.write("\n\n")
    log_file.write(
        "### Keywords in multiple categories (" + str(len(cat_set_multicat)) + ") ###\n"
    )
    log_file.write(json.dumps(cat_set_multicat, indent=2))

    log_file.write("\n\n")
    log_file.write(
        "### Uncategorised datasets (" + str(len(uncategorised_datasets)) + ") ###\n"
    )
    for row in uncategorised_datasets.index:
        log_file.write(
            str(uncategorised_datasets.loc[row, "Title"])
            + " "
            + str(uncategorised_datasets.fillna("").loc[row, "Description"])
            + "\n\n"
        )

print(f"Checks complete. Results written to {output_filename}")
