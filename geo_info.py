# This program provides a geospatial class that enables spatial joins.
# It also provides the census tract shapefile that is used to join basic dataframes to create geospatial dataframes
# with census information
# Also, a make_geospatial method is provide to convert a regular pandas dataframe into a geopandas GeoDataFrame
# The add_distance method also uses the distance_to_unm method to add a column in the dataframe that computes the spatial_join
# distance between the university and the coordinate values from the dataframe
import geopandas as gpd
import numpy as np
import pandas as pd
import requests as rq
from zipfile import ZipFile as zp
import us, io
import geocoder
from geopy.distance import vincenty

docs = {
    'shape_files': '/Users/edwinagbenyega/Documents/Thesis/data/shape_files',
    'nm_tract_shape': 'tl_2010_35_tract10.shp'
}

nm_tract_url = us.states.NM.shapefile_urls('tract')
nm_shape_file = docs['shape_files'] + '/' + docs['nm_tract_shape']
unm_address = 'The University of New Mexico Albuquerque, NM 87131'
unm_latlng = geocoder.google(unm_address).latlng

## extract_shapefile() pulls and unzips geospatial zip files from the census bureau
def extract_shapefile(state=us.states.NM, type='tract', folder=docs['shape_files']):
    shape_url = state.shapefile_urls(type)
    return zp(io.BytesIO(rq.get(shape_url).content)).extractall(folder)

def make_geospatial(df):
    geometry = [Point(x, y) for x, y in zip(df.Longitude, df.Latitude)]
    crs = {'init': 'epsg:4326'}
    geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
    return geo_df

def distance_to_unm(x,y):
    return vincenty(list([x, y]), unm_latlng)

def add_distance(df):
    df['distance_to_unm'] = df.apply(lambda x: distance_to_unm(x['Longitude'], x['Latitude']), axis=1)
    return df

## The GeoSpatial class reads a shapefile and operates on it as a geospatial dataframe
class GeoSpatial:
    def __init__(self, shape_file):
        # geospatial dataframe read from shape_file
        self.shape_file = gpd.read_file(shape_file)

    def spatial_join(self, shape_file, how='left', op='intersects'):
        # returns a geospatial dataframe derived from joining two geospatial dataframes
        return gpd.sjoin(shape_file, self.shape_file, how='left', op='intersects')

    def data_join(self, data_frame, left=['GEOID10'], right=['GeoID']):
        # returns a dataframe joined by merging a regular dataframe with a geospatial dataframe
        return self.shape_file.merge(data_frame, left_on=left, right_on=right)


nm = GeoSpatial(nm_shape_file)
