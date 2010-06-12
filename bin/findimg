#!/usr/bin/python2.6

import flickrapi
import urllib
import os,sys

try:
    api_key = sys.argv[1]
except:
    print "Usage:" + sys.argv[0] + 'Flickr-app-key'
    exit(2)


flickr = flickrapi.FlickrAPI(api_key)

photos = flickr.photos_search(tag='milano', has_geo='1', 
                              lat='45.467535', lon='9.192724', radius='32', 
                              per_page='500',  license='4,6,5',
                              safe_search='1', content_type='1', media='photos')


for i in xrange(len(photos[0])):
    f = photos[0][i]
    try: 
        loc = flickr.photos_geo_getLocation(photo_id=f.attrib['id'])
        f.attrib['lat'] = loc[0][0].attrib['latitude']
        f.attrib['lon'] = loc[0][0].attrib['longitude']
        f.attrib['url'] = "http://farm{farm}.static.flickr.com/{server}/{id}_{secret}.jpg".format(**f.attrib)
        f.attrib['fname'] = f.attrib['id'] + ".jpg"
        if os.access(f.attrib['fname'], os.F_OK):
            continue
        urllib.urlretrieve(f.attrib['url'], f.attrib['fname'])
        try:
            f.attrib['title'] = f.attrib['title'].decode('ascii','ignore').replace("'", "")
        except UnicodeEncodeError:
            f.attrib['title'] = ''
        if f.attrib['lat'] > 0: f.attrib['latref'] = 'N' 
        else: 
            f.attrib['lat'] *= -1 
            f.attrib['latref'] = 'S'
        if f.attrib['lon'] > 0: f.attrib['lonref'] = 'E' 
        else: 
            f.attrib['lon'] *= -1 
            f.attrib['lonref'] = 'W'
        cmd = "exiftool -overwrite_original -Title='{title}' -Author='Flickr {owner}' -Description='{url}' -GPSLatitude={lat} -GPSLongitude={lon} -GPSLatitudeRef={latref} -GPSLongitudeRef={lonref} {fname}".format(**f.attrib)
        os.system(cmd)
    except flickrapi.exceptions.FlickrError: 
        pass

