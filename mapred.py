#!/dev/python
import sys

class Mapper:
    def __init__(self, parser, handler):
        self.handler = handler
        self.parser = parser
    
    def process(self, fin, fout):
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
    def __init__(self, parser, handler=None, handler_stream=None):
        self.handler = handler
        self.handler_stream = handler_stream
        self.last_key = None
        self.parser = parser

    def parse_it(self, fin):
        for i in fin:
            yield self.parser(i.rstrip())

    def my_it(self, it):
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

    def it_gene(self, it):
        while it.has_next():
            self.last_key = it.peak()[0]
            yield self.my_it(it)

    def process(self, fin=sys.stdin, fout=sys.stdout):
        if self.handler is None:
            raise TypeError("'handle' must be provided")
        for it in self.it_gene(ExtIter(self.parse_it(fin))):
            for line in self.handler(self.last_key, it):
                print >>fout, line

    def process_stream(self, fin=sys.stdin, fout=sys.stdout):
        if self.handler_stream is None:
            raise TypeError("'handle_steam' must be provided")
        for it in self.it_gene(ExtIter(self.parse_it(fin))):
            self.handler_stream(self.last_key, it, fout)
