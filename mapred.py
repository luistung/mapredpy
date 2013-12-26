#!/bin/env python
import sys

class Splitter:
    def __init__(self, sep, keynum):
        self.sep = sep
        self.keynum = keynum
        
    @staticmethod
    def _find_nth_sep(s, sep, n):
        if n == 0: return 0
        count = 0
        pos = 0
        while count < n and pos < len(s):
            if s[pos] == sep: 
                count += 1
                if count == n: return pos
            pos += 1
        if pos == len(s) and count + 1 == n: return pos
        raise ValueError('separator not found')
           
    def __call__(self, line):
        line = line.strip(self.sep)
        pos = Splitter._find_nth_sep(line, self.sep, self.keynum)
        if pos == 0:
            return "", line
        if pos == len(line):
            return line, ""
        return line[:pos], line[pos + 1:]

class Map_handler:
    def __init__(self, sep):
        self.sep = sep
    
    def __call__(self, key, value):
        yield '%s%s%s' % (key, self.sep, value)
        
class Reduce_handler:
    def __init__(self, sep):
        self.sep = sep
    
    def __call__(self, key, value_it):
        for value in value_it:
            yield '%s%s%s' % (key, self.sep, value) 

class Mapper:
    def __init__(self, parser=Splitter('\t', 1), handler=Map_handler('\t')):
        self.handler = handler
        self.parser = parser
    
    def process(self, fin=sys.stdin, fout=sys.stdout):
        for i in fin:
            for j in self.handler(*self.parser(i.rstrip())):
                print >> fout, j

class ExtIter:
    def __init__(self, it):
        self.it = it
        try:
            self.cur = next(it)
        except StopIteration:
            self.cur = None

    def has_next(self):
        return self.cur is not None

    def peak(self):
        return self.cur

    def next(self):
        if self.cur is None:
            raise StopIteration
        else:
            ret = self.cur
            try:
                self.cur = self.it.next()    
            except StopIteration:
                self.cur = None
            return ret
    def __iter__(self):
        return self
        

class Reducer:
    def __init__(self, parser=Splitter('\t', 1), handler=Reduce_handler('\t')):
        self.handler = handler
        self.last_key = None
        self.parser = parser

    def _parse_it(self, fin):
        for i in fin:
            yield self.parser(i.rstrip())

    def _my_it(self, it):
        while it.has_next():
            key, value = it.peak()
            assert key is not None
            if key <> self.last_key:
                self.last_key = key
                raise StopIteration
            else:
                it.next()
                self.last_key = key
                yield value

    def _it_gene(self, it):
        while it.has_next():
            self.last_key = it.peak()[0]
            yield self._my_it(it)

    def process(self, fin=sys.stdin, fout=sys.stdout):
        for it in self._it_gene(ExtIter(self._parse_it(fin))):
            for line in self.handler(self.last_key, it):
                print >>fout, line
