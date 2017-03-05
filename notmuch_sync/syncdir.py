from .dump import Dump
from subprocess import check_output
from os import path
import json


class SyncStore(object):
    """Sync information stored outside of notmuch."""

    def __init__(self, rootdir, _check_output=check_output, _open=open):
        self.__rootdir = rootdir
        self.__check_output = _check_output
        self.__open = _open
        self.__host = _check_output(['hostname']).strip()

    def create(self, db):
        self.save_lastmod(db.lastmod())
        self.save_tagsdump(db.all_tags())

    def update(self, db):
        current = db.tags_since(self.load_lastmod())
        stored = self.load_tagsdump()
        stored.update(current)
        self.save_tagsdump(stored)
        self.save_lastmod(db.lastmod())

    def _tagsdump_filename(self):
        return path.join(self.__rootdir, '_tagsdump')

    def _lastmod_filename(self, hostname=None):
        if hostname is None:
            hostname = self.__host
        return path.join(self.__rootdir, '_lastmod.' + hostname)

    def load_lastmod(self, hostname=None,
                     _check_output=check_output, _open=open):
        if hostname is None:
            hostname = self.__host
        with _open(self._lastmod_filename(hostname)) as f:
            return json.loads(f.read())

    def load_tagsdump(self):
        return Dump.from_filename(self._tagsdump_filename(),
                                  _open=self.__open)

    def save_tagsdump(self, dump):
        with self.__open(self._tagdump_filename(), 'w') as f:
            dump.write_to(f)

    def save_lastmod(self, value):
        with self.__open(self._lastmod_filename()) as f:
            f.write(json.dumps(value))


class NotmuchDB(object):

    def __init__(self, _check_output=check_output):
        self.__check_output = _check_output

    def all_tags(self):
        return Dump.loads(self.__check_output(['notmuch', 'dump']))

    def tags_since(self, lastmod):
        number = lastmod['number']
        return Dump.loads(self.__check_output(['notmuch', 'dump', '--',
                                               'lastmod:' + number + '..']))

    def lastmod(self):
        output = self.__check_output(['notmuch', 'count', '--lastmod'])
        output = output.strip()[2]
        return {
            'number': output,
            'messages': list(self.tags_since(output).keys()),
        }
