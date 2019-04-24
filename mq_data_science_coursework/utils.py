"""
Utilities to support the COMP257/ITEC657 Portfolio

Author: Steve Cassidy
Author: Ka Yu Lau

You are free to modify and add to this module as much as you
wish as you implement your portfolio.

"""

import pandas as pd
import xml.etree.ElementTree as ET
from geopy.distance import great_circle as gc
from datetime import timedelta


def parse_gpx(filename):
    """Parse data from a GPX file and return a Pandas Dataframe
    with columns for latitude, longitude and elevation and
    with timestamps as the row index"""

    tree = ET.parse(filename)
    root = tree.getroot()

    # define a namespace dictionary to make element names simpler
    # this mirrors the namespace definintions in the XML files
    ns = {'gpx':'http://www.topografix.com/GPX/1/1',
          'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'}

    # when we look for elements, we need to use the namespace prefix
    trk = root.find('gpx:trk', ns)
    trkseg = trk.find('gpx:trkseg', ns)

    data = []
    times = []

    # iterate over the first ten trkpt elements - the children of trkseg
    for trkpt in trkseg:
        # get some properties from the attributes
        lon = trkpt.attrib['lon']
        lat = trkpt.attrib['lat']
        # get values from the child elements
        ele = trkpt.find('gpx:ele', ns).text
        time = trkpt.find('gpx:time', ns).text

        row = {
               'latitude': float(lat),
               'longitude': float(lon),
               'elevation': float(ele),
              }
        data.append(row)
        times.append(time)

    times = pd.to_datetime(times)
    return pd.DataFrame(data, index=times)



def speed_cal(latitude,longitude, elevation, df):
    '''
    calculate speed (km/hr) based on latitude and longitude from a time series
    calculate gradient based on elevation

    return a data frame that consist of
    speed, gradient, distance traveled(delta_dist) and time passed (delt_time)
    '''


    #initializing lists for speed distance traveled and gradient with starting value= 0
    speed = [0]
    delta_dist = [0]
    gradient = [0]
    delta_time = [0]


    #a loop calculate the speed for every instance
    for i in range(len(df)-1):

        #reading latitude and logitude
        lat1 = df.iloc[i][latitude]
        long1 = df.iloc[i][longitude]
        lat2 = df.iloc[i+1][latitude]
        long2 = df.iloc[i+1][longitude]

        #set up coordinates object
        pt1 = (lat1,long1)
        pt2 = (lat2,long2)

        #calculate the distance traveled with global circle (geopy) in kilometers
        d = float(gc(pt1,pt2).km)
        delta_dist.append(d)


        #calculate the time differences between two records
        t = df.index[i+1]-df.index[i]
        t = timedelta.total_seconds(t) #converting the time difference into seconds
        delta_time.append(t)

        #calculation of speed
        s = d/(t/(3600))
        speed.append(s)

        #calculation of gradient
        ele1 = df.iloc[i][elevation]
        ele2 = df.iloc[i+1][elevation]
        if d != 0:
            g = (ele2 - ele1)/d
        else:
            g = 0.0
        gradient.append(g)


    #create a output DataFrame from the list generated
    df1 = pd.DataFrame({'speed':speed,
                      'gradient':gradient,
                      'delta_dist':delta_dist,
                      'delta-time':delta_time},
                      index = df.index
                     )
    output = pd.concat([df,df1],axis=1)
    return output





def lapcount(latitude,longitude,df):
    '''add the number of laps the cyclist is in for every instance'''

    #set up starting point
    #lat_st = df.iloc[0][latitude]
    #long_st = df.iloc[0][longitude]

    #Assume the starting point are the mean of latitude and longitude
    lat_st = -33.8987994160306
    long_st = 150.97898103816814


    #initialize value for lap counter
    lap_count = 0
    lap = [0]

    #set up for checking if passed the starting point
    cross_lat = False
    cross_long = False

    #for loop if the cyclist passed through both the starting longitude and latidude, starts a new lap
    for i in range(len(df)-1):

        plat_1 = df.iloc[i][latitude]
        plong_1 = df.iloc[i][longitude]
        plat_2 = df.iloc[i+1][latitude]
        plong_2 = df.iloc[i+1][longitude]


        if float(plat_1) >= float(lat_st) and float(plat_2) <= float(lat_st):
            cross_lat = True

        if float(plong_1) <= float(long_st) and float(plong_2) >= float(long_st):
            cross_long = True

        if cross_lat == True & cross_long==True:
            lap_count = lap_count + 1
            cross_lat = False #reset checking value
            cross_long = False #reset checking value

        lap.append(lap_count)

    #create a output DataFrame from the list generated
    df1 = pd.DataFrame({'lap' : lap}, index = df.index)
    output = pd.concat([df,df1],axis=1)
    return output
