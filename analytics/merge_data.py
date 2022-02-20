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

    ### From scotgov csv
    source_scotgov = pd.read_csv('../data/scotgov-datasets.csv')
    source_scotgov = source_scotgov.rename(columns={
                                                    'title':'Title',
                                                    'category':'OriginalTags',
                                                    'organization':'Owner',
                                                    'notes':'Description',
                                                    'date_created':'DateCreated',
                                                    'date_updated':'DateUpdated',
                                                    'url':'PageURL'
                                                    })
    source_scotgov['Source'] = 'manual extraction'
    source_scotgov['License'] = 'OGL3'

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
    source_dcat = pd.DataFrame()
    folder = '../data/dcat/'
    for dirname, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.rsplit('.',1)[1] == 'csv':
                source_usmart = source_usmart.append(pd.read_csv(folder + r'/' + filename, parse_dates=['DateUpdated']))
    source_dcat['Source'] = 'DCAT feed'


    ### Combine all data into single table
    data = source_ckan.append([source_gsheets, source_arcgis, source_usmart, source_scotgov, source_dcat])
    data = data.reset_index(drop=True)

    ### Saves copy of data without cleaning - for analysis purposes
    data.to_csv('../data/merged_output_untidy.csv', index=False)

    ### Some cleaning
    ### Renaming entries to match
    owner_renames = {
                    'Aberdeen': 'Aberdeen City',
                    'Dundee': 'Dundee City',
                    'Perth': 'Perth and Kinross',
                    'open.data@southayrshire':'South Ayrshire',
                    'SEPA': 'Scottish Environment Protection Agency',
                    'South Ayrshire': 'South Ayrshire Council'
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

    data['OriginalTags'] = data['OriginalTags'].apply(tidy_categories)
    data['ManualTags'] = data['ManualTags'].apply(tidy_categories)
    

    ### Tidy licence names
    def tidy_licence(licence_name):
        """ Temporary licence conversion to match export2jkan -- FOR ANALYTICS ONLY, will discard in 2022Q2 Milestone

        Returns:
            string: a tidied licence name
        """
        known_licences= {
                    'https://creativecommons.org/licenses/by-sa/3.0/': 'Creative Commons Attribution Share-Alike 3.0',
                    'Creative Commons Attribution 4.0':'Creative Commons Attribution 4.0',
                    'https://creativecommons.org/licenses/by/4.0/legalcode':'Creative Commons Attribution 4.0',
                    'OGL3':'Open Government Licence v3.0',
                    'Open Government Licence 3.0 (United Kingdom)':'Open Government Licence v3.0',
                    'UK Open Government Licence (OGL)':'Open Government Licence v3.0',
                    'uk-ogl':'Open Government Licence v3.0',
                    'Open Data Commons Open Database License 1.0':'Open Data Commons Open Database License 1.0',
                    'http://opendatacommons.org/licenses/odbl/1-0/':'Open Data Commons Open Database License 1.0',
                    'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/':'Open Government Licence v2.0',
                    'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/':'Open Government Licence v3.0',
                    }
        if licence_name in known_licences:
            tidied_licence = known_licences[licence_name]
        elif str(licence_name)=="nan":
            tidied_licence = "No licence"
        else:
            tidied_licence = "Custom licence: " + str(licence_name)
        return tidied_licence
    data['License'] = data['License'].apply(tidy_licence)

    
    ### Output combined data to csv
    data.to_csv('../data/merged_output.csv')

    return data 

if __name__=="__main__":
    merge_data()
