def read_key_file(key_file_path):
    with open(key_file_path) as key_file:
        return key_file.read().strip()


def get_allowed_hosts():
    return ["cybered.localhost", "cybered.agill.xyz"]
