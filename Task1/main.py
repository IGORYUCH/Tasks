from subprocess import Popen, PIPE
from sys import argv


def main():
    filename = argv[1]

    with open(filename, 'r') as opened_file:
        path_to_device = opened_file.readline().strip()
    dev_name = path_to_device.split('/')[-1]

    with Popen('lsblk', stdout=PIPE, stderr=PIPE) as lsblk:
        with Popen(['grep', dev_name], stdout=PIPE, stderr=PIPE, stdin=lsblk.stdout) as grep:
            grep_output = grep.stdout.read()
            if grep_output:
                words = grep_output.split()
                dev_size = words[3]
                dev_type = words[5]
                if dev_type == b'part':
                    with Popen(['df', '-T', '-B', 'M'], stdout=PIPE, stderr=PIPE) as df:
                        with Popen(['grep', path_to_device], stdout=PIPE, stderr=PIPE, stdin = df.stdout) as grep:
                            grep_output = grep.stdout.read()
                            if grep_output:
                                words = grep_output.split()
                                dev_filesystem_type = words[1]
                                dev_free_size = words[4]
                                dev_mountpoint = words[6]
                                print(path_to_device, dev_type, dev_size, dev_free_size,
                                      dev_filesystem_type, dev_mountpoint)
                            else:
                                print(path_to_device, 'invalid device path')
                else:
                    print(path_to_device, dev_type, dev_size)
            else:
                print(path_to_device, 'no such device')
        

if __name__ == '__main__':
    main(argv)
