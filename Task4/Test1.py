from datetime import datetime
from os.path import expanduser, isfile, join
from os import listdir


class Test1:

    def __init__(self, test_id, test_name):
        self.test_id = test_id
        self.name = test_name

    def execute(self):
        result = self.clean_up(self.run(self.prepare()))
        return result

    def run(self, result):
        if result:
            print(self.test_id, self.name, 'running')
            home_dir = expanduser('~')
            for user_file in listdir(home_dir):
                if isfile(join(home_dir, user_file)):
                    print(self.test_id, self.name, user_file)
            print(self.test_id, self.name, 'passed')
            return True
        else:
            print(self.test_id, self.name, 'interrupted')
            return False

    def prepare(self):
        print(self.test_id, self.name, 'preparing')
        now = datetime.now()
        if not (int(now.timestamp()) % 2):
            return True
        else:
            return False

    def clean_up(self, result):
        print(self.test_id, self.name, 'cleaning up')
        return result
