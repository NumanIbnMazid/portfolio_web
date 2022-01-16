import environ

def get_settings_file():

    # ----------------------------------------------------
    # *** Project Environment ***
    # ----------------------------------------------------

    root = environ.Path(__file__) - 3

    DEFAULT_ENV_PATH = root
    DEFAULT_ENV_FILE = DEFAULT_ENV_PATH.path('.env')()

    env = environ.Env(DEBUG=(bool, False),)
    environ.Env.read_env(env.str('ENV_PATH', DEFAULT_ENV_FILE))  # reading .env file

    # ----------------------------------------------------
    # *** Project's Settings File ***
    # ----------------------------------------------------

    if env.bool('IS_PRODUCTION', default=False):
        return "config.settings.production"
    elif env.bool('IS_STAGING', default=False):
        return "config.settings.staging"
    return "config.settings.local"
