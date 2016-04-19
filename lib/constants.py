VERBOSE = False
CLI_VERSION = '0.3'

# API-related constants.
# https://docs.cloudhero.io
CLOUD_HERO_URI = 'http://d.cloudhero.io'
CLOUD_HERO_TOKEN_ENV_VARIABLE = 'CLOUD_HERO_TOKEN'
CLOUD_HERO_USER_AGENT = 'cloudhero-cli'

# Local directory-related constants.
CLOUD_HERO_DIR = '~/.herorc/'
CLOUD_HERO_SSH_KEY = CLOUD_HERO_DIR + '.ssh/id_rsa_cloudhero'
CLOUD_HERO_TOKEN = CLOUD_HERO_DIR + 'token'
CLOUD_HERO_CACHE_NODES = CLOUD_HERO_DIR + 'cache/nodes'
CLOUD_HERO_CACHE_ENVIRONMENTS = CLOUD_HERO_DIR + 'cache/enviornments'
CLOUD_HERO_CACHE_OPTIONS = CLOUD_HERO_DIR + 'cache/options'

# Exceptions.
class NotFound(Exception): pass
