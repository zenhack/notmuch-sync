from subprocess import check_output, check_call
from pipes import quote


class Repo(object):

    def __init__(self,
                 remote_name, remote_dir,
                 local_name=None,
                 _check_output=check_output,
                 _check_call=check_call):
        self.__check_call = _check_call
        if local_name is None:
            local_name = _check_output(['hostname'])
        self.__local_name = local_name
        self.__remote_name = remote_name
        self.__remote_dir = remote_dir

    def commit(self):
        self.__check_call(['git', 'add', '.'])
        self.__check_call(['git', 'commit', '-m',
                           'committing on ' + self.__local_name])

    def sync(self):
        self.__check_call(['git', 'fetch', self.__remote_name])
        self.__check_call(['git', 'merge',
                           self.__remote_name + '/' + self.__remote_name,
                           '-m', 'Merge ' + self.__remote_name +
                                 ' into ' + self.__local_name,
                           ])
        self.__check_call(['git', 'push', self.__remote_name])
        self.__check_call([
            'ssh', self.__remote_name, 'sh', '-c',
            """
            cd %(remote_dir)s
            git merge %(local_name)s -m "Merge %(local_name) into %(remote_name)"
            """.format({
                'local_name': quote(self.__local_name),
                'remote_name': quote(self.__remote_name),
                'remote_dir': quote(self.__remote_dir),
            }),
        ])
