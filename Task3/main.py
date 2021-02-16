from hashlib import sha1, sha256, md5
from os.path import join, curdir
from sys import argv


def is_hash_valid(opened_file, hashlib_algo, file_hash):
    computed_hash = hashlib_algo(opened_file.read()).hexdigest()
    if computed_hash == file_hash:
        return 'OK'
    else:
        return 'FAIL'


def main(argv):
    checksums_filename = join(curdir, argv[1])
    files_dir = join(curdir, argv[2])

    with open(checksums_filename, 'r') as checksums_opened_file:
        for string in checksums_opened_file.readlines():
            words = string.split()
            filename = words[0]
            full_filename = join(files_dir, filename)
            algo = words[1]
            file_hash = words[2]
            
            try:
                with open(full_filename, 'rb') as opened_file:
                    if algo == 'md5':
                        valid_status = is_hash_valid(opened_file, md5, file_hash)
                    elif algo == 'sha1':
                        valid_status = is_hash_valid(opened_file, sha1, file_hash)
                    elif algo == 'sha256':
                        valid_status = is_hash_valid(opened_file, sha256, file_hash)
                    else:
                        valid_status = 'UNKNOWN ALGORITHM'
                    print(filename, valid_status)

            except FileNotFoundError:
                print(filename, 'NOT FOUND')


if __name__ == '__main__':
    main(argv)
