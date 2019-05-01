SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

def read_key_file(key_file_path):
    with open(key_file_path) as key_file:
        return key_file.read().strip()


def get_allowed_hosts():
    return ["cybered.localhost", "cybered.agill.xyz"]

# When not in debug mode, attempt to get the secret key from file
RELEASE_KEY_FILE = "/etc/django/secret.txt"
ALLOWED_HOSTS = get_allowed_hosts()

try:
    SECRET_KEY = read_key_file(RELEASE_KEY_FILE)
except OSError as e:
    print("WARNING: Unable to open key file - ", e)
