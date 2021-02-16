import os


class Test2:

    def __init__(self, test_id, test_name):
        self.test_id = test_id
        self.name = test_name

    def execute(self):
        result = self.clean_up(self.run(self.prepare()))
        return result

    def run(self, result):
        if result:
            test_filename = 'test'
            print(self.test_id, self.name, 'running')
            test_file = open(test_filename, 'wb')
            test_file.write(os.urandom(1024))
            print(self.test_id, self.name, 'passed')
            return (True, test_file, test_filename)
        else:
            print(self.test_id, self.name, 'interrupted')
            return (False, None, None)

    def prepare(self):
        print(self.test_id, self.name, 'preparing')
        if os.name == 'nt':
            return True
        else:
            mem_bytes = os.sysconf('SC_PHYS_PAGES') * 4096
            mem_gbytes = mem_bytes / 1024**3
            if mem_gbytes > 1:
                return True
            else:
                return False

    def clean_up(self, result):
        print(self.test_id, self.name, 'cleaning up')
        if result[0]:
            test_file = result[1]
            test_file.close()
            test_filename = result[2]
            os.remove(test_filename)
            test_file.close()
        return result[0]
