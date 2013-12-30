#!/bin/env python
import sys
import mapred

def map_parser(line):
    return 'k', 'v'

def map_handler(key, value):
    yield '%s\t%s' % (key, value)

def reduce_parser(line):
    return 'k', 'v'

def reduce_handler(key, value_it):
    for value in value_it:
        yield '%s\t%s' % (key, value)

if sys.argv[1] == '-m':
    #mapred.Mapper(parser=Splitter('\t', 1), handler=Map_handler('\t')).process()
    mapred.Mapper(map_parser, map_handler).process()

elif sys.argv[1] == '-r':
    #mapred.Mapper(parser=Splitter('\t', 1), handler=Reduce_handler('\t')).process()
    mapred.Reducer(reduce_parser, reduce_handler).process()
