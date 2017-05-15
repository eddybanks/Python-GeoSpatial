import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv

files = {
    'students': '/Users/edwinagbenyega/Documents/Thesis/scripts/other/census2.csv',
    'output': './output/',
    'csv_defs': '/Users/edwinagbenyega/Documents/Thesis/scripts/other/csv_defs.json'
}

class CSV_File:
    def __init__(self, file, cols=None, encoding=None):
        self.file = read_csv(file, encoding=encoding)
        self.data_frame = DataFrame(data=self.file, columns=cols)
        self.headers = list(self.data_frame)

    def create_csv(self, file_name=files['output'] + 'output.csv', encoding=None):
        self.data_frame.to_csv(file_name, encoding=encoding)

    def csv_with_conds(self, file_name=files['output'] + 'output_with_conds.csv', encoding=None, conds={}):
        df = self.data_frame
        for k,v in conds.items():
            if v[1] == 'eq':
                df = df[df[k] == v[0]]
            elif v[1] == 'gt':
                df = df[df[k] == v[0]]
            elif v[1] == 'lt':
                df = df[df[k] == v[0]]
        return df


students = CSV_File(files['students'], encoding='latin1')
american_indian_areas = students.csv_with_conds(conds={'GeoType': ['American Indian Area', 'eq']})
census_tracts = students.csv_with_conds(conds={'GeoType': ['Census Tract', 'eq']})
counties = students.csv_with_conds(conds={'GeoType': ['County', 'eq']})
msa = students.csv_with_conds(conds={'GeoType': ['MSA', 'eq']})
places = students.csv_with_conds(conds={'GeoType': ['Place', 'eq']})
states = students.csv_with_conds(conds={'GeoType': ['State', 'eq']})
usa = students.csv_with_conds(conds={'GeoType': ['USA', 'eq']})
