import environ
from django.core.management.utils import get_random_secret_key

# ----------------------------------------------------
# *** Project Environment ***
# ----------------------------------------------------

DEFAULT_ENV_PATH = environ.Path(__file__) - 2
DEFAULT_ENV_FILE = DEFAULT_ENV_PATH.path('.env')()
DEFAULT_ENV_EXAMPLE_FILE = DEFAULT_ENV_PATH.path('.env.example')()


def get_env_key_values():
    KEY_VALUES = {}
    with open(DEFAULT_ENV_EXAMPLE_FILE, "r") as f:
        for line in f.readlines():
            try:
                key, value = line.split('=')
                KEY_VALUES[key] = value
            except ValueError:
                # syntax error
                pass
    return KEY_VALUES


with open(DEFAULT_ENV_FILE, "w") as f:
    key_values = get_env_key_values()
    for key, value in key_values.items():
        if key == 'SECRET_KEY':
            value = get_random_secret_key()
        elif key == 'DATABASE_URL' and len(value.strip()) < 1:
            # skip if Database URL is not set
            continue
        else:
            value = value.strip() if len(value.strip()) >= 1 else ""
        try:
            f.write(f"{key}={value}\n")
        except ValueError:
            # syntax error
            pass
