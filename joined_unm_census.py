import reformat_csv as rf
import geo_info as geo
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pdb

rf.census_tracts['GeoID'] = rf.census_tracts['GeoID'].apply(str)
census_tracts = geo.nm.data_join(data_frame=rf.census_tracts)

df = rf.students
geo_df = geo.make_geospatial(df)
x = gpd.sjoin(geo_df, census_tracts, how='left', op='intersects')
x.to_csv('./other/full_training_data.csv')
x.to_csv('./other/training_data.csv', columns=rf.headers['training_cols'])
