### Setting the environment
import pandas as pd
import os
import datetime as dt

def merge_data():
    ### Loading data

    ### From ckan output
    source_ckan = pd.read_csv('../data/ckan_output.csv', parse_dates=['DateUpdated'])
    source_ckan['Source'] = 'ckan API'

    ### From google sheets
    source_gsheets = pd.read_csv('../data/from_Google_Sheets.csv', parse_dates=['DateUpdated'])
    source_gsheets['Source'] = 'manual extraction'

    ### From arcgis api
    source_arcgis = pd.DataFrame()
    folder = '../data/arcgis/'
    for dirname, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.rsplit('.',1)[1] == 'csv':
                source_arcgis = source_arcgis.append(pd.read_csv(folder + r'/' + filename, parse_dates=['DateUpdated']))
    source_arcgis['Source'] = 'arcgis API'

    ### From usmart api
    source_usmart = pd.DataFrame()
    folder = '../data/USMART/'
    for dirname, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.rsplit('.',1)[1] == 'csv':
                source_usmart = source_usmart.append(pd.read_csv(folder + r'/' + filename, parse_dates=['DateUpdated']))
    source_usmart['Source'] = 'USMART API'
    source_usmart['DateUpdated'] = source_usmart['DateUpdated'].apply(lambda x: x.replace(tzinfo=None))

    ## From DCAT
    source_dcat = pd.read_csv('../data/dcat/glasgow.csv', parse_dates=['DateUpdated'])
    source_dcat['Source'] = 'DCAT feed'


    ### Combine all data into single table
    data = source_ckan.append([source_gsheets, source_arcgis, source_usmart, source_dcat])
    data = data.reset_index(drop=True)

    ### Some cleaning
    ### Remove these irrelevant entries (not councils)
    drop_list = ['Development, Safety and Regulation']
    data = data[~data['Owner'].isin(drop_list)]
    ### Renaming entries to match
    owner_renames = {
                    'Aberdeen': 'Aberdeen City',
                    'Dundee': 'Dundee City',
                    'Perth': 'Perth and Kinross',
                    'open.data@southayrshire':'South Ayrshire'
                    }
    data['Owner'] = data['Owner'].replace(owner_renames)
    ### Format dates as datetime type
    data['DateUpdated'] = pd.to_datetime(data['DateUpdated'], format='%Y-%m-%d', errors='coerce').dt.date
    ### Inconsistencies in casing for FileType
    data['FileType'] = data['FileType'].str.upper()
    ### Creating a dummy column
    data['AssetStatus'] = None


    ### Cleaning dataset categories
    def tidy_categories(categories_string):
        """tidies the categories: removes commas, strips whitespace, converts all to lower and strips any trailing ";"

        Args:
            categories_string (string): the dataset categories as a string
        """
        tidied_string = str(categories_string).replace(',',';')
        tidied_list = [cat.lower().strip() for cat in tidied_string.split(';') if cat!=""]
        tidied_string=";".join(str(cat) for cat in tidied_list if str(cat)!='nan')
        if (len(tidied_string)>0):
            if (tidied_string[-1]==";"):
                tidied_string = tidied_string[:-1]
        return tidied_string

    data['OriginalTags'] = data['OriginalTags'].apply(lambda x: tidy_categories(x))
    data['ManualTags'] = data['ManualTags'].apply(lambda x: tidy_categories(x))
    
    ### Output combined data to csv
    data.to_csv('../data/merged_output.csv')

    return data 

if __name__=="__main__":
    merge_data()
