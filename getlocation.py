#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
from contextlib import contextmanager
from pyipinfodb import pyipinfodb
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from sys import stdin, stdout, stderr
import numpy as np


def plot_locations(locations, output_filename):
    ip_map = Basemap(projection='robin', lon_0=0, resolution='c')

    for line in locations:
    	srclong, srclat = map(float, line.split(','))
    	x, y = ip_map(srclong, srclat)
    	plt.plot(x,y, 'o', color='#ff0000', ms=2.7, markeredgewidth=0.5)


    ip_map.drawcountries(color='#ffffff')
    ip_map.fillcontinents(color='#cccccc',lake_color='#ffffff')
    
    plt.savefig(output_filename, dpi=600)

def memoize(func):
    '''
    Decorator for a function which caches results. Based on
    http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/
    '''
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = func(*key)
            return ret
        def __call__(self, *args):
            return self[args]
    
    return memodict()


@memoize
def get_location(ip_lookup, ip):
    print('Getting location for', ip, file=stderr)
    ip_data = ip_lookup.get_city(ip)
    yield ip_data['longitude'], ip_data['latitude']


@contextmanager
def smart_open(file_or_filename, *args, **kwargs):
    try:
        f = open(file_or_filename, *args, **kwargs)
    except TypeError:
        yield file_or_filename
    else:
        with f:
            yield f


def main():
    parser = ArgumentParser()
    parser.add_argument('--input', '-i', default=stdin)
    parser.add_argument('--output', '-o', default=stdout)
    parser.add_argument('--gen-map', '-G', action='store_true')
    parser.add_argument('API_KEY')
    args = parser.parse_args()
    
    ip_lookup = pyipinfodb.IPInfo(args.API_KEY)
    
    with smart_open(args.input) as istr:
        with smart_open(args.output, 'w') as ostr:
            if args.gen_map:
                for ip in istr:
                    plot_locations(*(get_location(ip_lookup, ip), "ip_map.png"))
            else:
                for ip in istr:
                    print(*get_location(ip_lookup, ip), sep=",", file=ostr)

if __name__ == '__main__':
    main()
