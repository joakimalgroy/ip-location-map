#!/usr/bin/env python
from pyipinfodb import pyipinfodb

ip_lookup = pyipinfodb.IPInfo('API_KEY_HERE')

coord_list = [] # List of tuples containing coordinates as (Longitude, Latitude)
cache = {} # Dict containing data from IPs that have already been requested
           # from the API
           
if os.path.exists('ips.txt'):
    with open('ips.txt','r') as ip_file:
        for ip in ip_file:
            print('Getting location for {}'.format(ip))
            if ip not in cache:
                ip_data=ip_lookup.get_city(ip)
                cache[ip] = ip_data
            else:
                ip_data = cache[ip]
            coord_list.append((ip_data['longitude'], ip_data['latitude']))

else:
    print('File \'ips.text\' not found!')
    raise SystemExit()
with open('geo.txt', 'w') as geo_file:
    for coordinates in coord_list:
        ip_longitude, ip_latitude = coordinates
        geo_file.write('{},{}\n'.format(ip_longitude, ip_latitude))
