### Helper Functions ###
# This py file stores the general functions for the project

# import dependency
import pandas as pd

# define cleaning function
def clean(df:pd.DataFrame, missing=True, outliers=True, new_col=True):
    '''
    Doc String:
    Objective:
    The function is used to clean the data source file for future analytic.
    Input:
    df: The original data source imported as pandas dataframe
    missing: perform missing value detection and replacement, default=True
    outliers: perform outlier detection and replacement, default=True
    new_col: create new field for analtytic, default=True
    '''

    data = df.copy()

    # replace column names with standardize format
    col_names = {'DR_NO':'crimeID',
                'Date Rptd':'reportDate',
                'DATE OCC':'eventDate',
                'TIME OCC':'eventTime',
                'AREA NAME':'areaName',
                'Crm Cd Desc':'crimeDesc',
                'Vict Age':'victimAge',
                'Vict Sex':'victimSex',
                'Premis Desc':'permisDesc',
                'Status Desc':'statusDesc',
                'LAT':'lat',
                'LON':'lon'}

    col = ['DR_NO', 'Date Rptd', 'DATE OCC', 'TIME OCC',
            'AREA NAME', 'Crm Cd Desc', 'Vict Age', 'Vict Sex',
            'Premis Desc', 'Status Desc', 'LAT', 'LON']

    rename = data[col].rename(columns=col_names)

    if outliers==True:
        # replace outliers with median
        median = rename['victimAge'].median()
        outliers = rename
        outliers.loc[(outliers['victimAge']<=0) | (outliers['victimAge']>80), 'victimAge'] = median

        # replace missing values with mode
        crime_mode = outliers.groupby('crimeDesc', as_index=False)['victimSex'].value_counts()
        crime_max = crime_mode.groupby('crimeDesc', as_index=False)['count'].max()
        victim_sex = (crime_mode.merge(crime_max, 
                                    on=['crimeDesc', 'count'], 
                                    how='inner')[['crimeDesc', 'victimSex']]
                                    .rename(columns={'victimSex':'sex'})
        )
    else:
        pass

    if missing==True:
        # calculate the days of report after the crime happended
        missing = outliers.merge(victim_sex, on='crimeDesc', how='left')
        missing.loc[missing['victimSex'].isnull(), 'victimSex'] = missing['sex']
        missing = missing.drop(columns=['sex'])
    else:
        pass

    if new_col==True:
        # calculate the days of report after the crime happended
        missing['reportDate'] = pd.to_datetime(missing['reportDate'])
        missing['eventDate'] = pd.to_datetime(missing['eventDate'])
        missing['dayDiff'] = missing['reportDate'] - missing['eventDate']
    else:
        pass

    clean = missing

    return clean