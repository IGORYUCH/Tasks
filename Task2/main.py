from subprocess import Popen, PIPE
from sys import argv
from re import findall


def main(argv):
    service_type = argv[1]
    service_name = argv[2]
    if service_type == '--service' or service_type == '--timer':
        with Popen(['systemctl', 'show', service_name], stdout=PIPE, stderr=PIPE) as systemctl:
            with Popen(['grep', '-e', 'GID', '-e', 'UID', '-e', 'ActiveState', '-e', 'ExecStart='],
                    stdout=PIPE, stderr=PIPE, stdin=systemctl.stdout) as grep:
                user = None
                group = None
                active_state = None
                last_start = None
                for string in grep.stdout.readlines():
                    string = string.decode('utf-8')
                    if ('GID' in string) and not ('[not set]' in string) and not ('Restrict' in string):
                        group = findall(r'GID=(\w+)\n', string)[0]
                    elif ('UID' in string) and not ('[not set]' in string) and not ('Restrict' in string):
                        user = findall(r'UID=(\w+)\n', string)[0]
                    elif 'ActiveState' in string:
                        active_state = findall(r'ActiveState=(\w+)\n', string)[0]
                    elif 'ExecStart' in string:
                        last_start = findall(r' start_time=\[(\w{3} \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \w{3})\]', string)[0]
                if not last_start:
                    print(service_name, 'not found')
                else:
                    if service_type == '--service':
                        print(service_name + '.service', user, group, active_state,'last started', last_start)
                    elif service_type == '--timer':
                        print(service_name + '.timer', active_state,'last started', last_start)
    else:
        print('unknown type', service_type)


if __name__ == '__main__':
    main(argv)
