from collections import defaultdict
from io import StringIO
import sys


class Dump(defaultdict):

    def __init__(self, *args, **kwargs):
        defaultdict.__init__(self, lambda: set(), *args, **kwargs)

    @staticmethod
    def from_filename(filename, _open=open):
        with _open(filename) as f:
            return Dump.read_from(f)

    @staticmethod
    def read_from(f):
        return Dump.loads(f.read())

    @staticmethod
    def loads(text):
        lines = text.split('\n')
        lines = [line.split() for line in lines]
        dump_dict = Dump()
        for line in lines:
            if line == []:  # this might happen at the end of the file.
                continue
            ident = line.pop()
            line.pop()  # get rid of the '--' delimiter
            line = [tag[1:] for tag in line]  # strip off the leading '+'
            dump_dict[ident] = set(line)
        return dump_dict

    def write_to(self, f):
        for key in self.keys():
            tags = ['+' + tag for tag in self[key]]
            f.write(' '.join(tags + ['--', key, '\n']))

    def dumps(self):
        f = StringIO()
        self.write_to(f)
        return f.getvalue()


def merge(ancestor, left, right):
    result = Dump()

    keys = set()
    for dump in (ancestor, left, right):
        for key in dump.keys():
            keys.add(key)

    for key in keys:
        added = left[key].union(right[key]).difference(ancestor[key])
        in_both = left[key].intersection(right[key])
        result[key] = added.union(in_both)
    return result


def main(argv=sys.argv, exit=exit, stderr=sys.stderr, open=open):
    if len(argv) != 5:
        stderr.write(
            "usage: %s <ancestor> <left> <right> <result>\n" % argv[0]
        )
        exit(1)
    ancestor, left, right, out = [Dump.from_filename(fname, _open=open)
                                  for fname in argv[1:4]]
    result = merge(ancestor, left, right)
    with open(out) as f:
        result.write_to(f)


if __name__ == '__main__':
    main()
