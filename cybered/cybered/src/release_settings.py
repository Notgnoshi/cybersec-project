def read_key_file(key_file_path):
    with open(key_file_path) as key_file:
        return key_file.readline()


# TODO: Return something reasonable
def get_allowed_hosts():
    return ["localhost", "127.0.0.1", "[::1]"]

