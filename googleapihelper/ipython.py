from collections import namedtuple
import httplib2
from apiclient import discovery
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
import logging


logger = logging.getLogger(__name__)

DEFAULT_LOGGING_LEVEL = 'DEBUG'
DEFAULT_NOAUTH_LOCAL_WEBSERVER = True
DEFAULT_AUTH_HOST_PORT = [8080, 8090]

DEFAULT_CREDENTIALS_PATH = './credentials'
DEFAULT_SECRETS_PATH = './client_secrets.json'
DEFAULT_REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

Flags = namedtuple('Flags',
        ['logging_level', 'auth_host_port', 'noauth_local_webserver'])

def extract_flags_from_kwargs(kwargs):
    if 'logging_level' in kwargs:
        logging_level = kwargs['logging_level']
        del kwargs['logging_level']
    else:
        logging_level = DEFAULT_LOGGING_LEVEL

    if 'auth_host_port' in kwargs:
        auth_host_port = kwargs['auth_host_port']
        del kwargs['auth_host_port']
    else:
        auth_host_port = DEFAULT_AUTH_HOST_PORT

    if 'noauth_local_webserver' in kwargs:
        noauth_local_webserver = kwargs['noauth_local_webserver']
        del kwargs['noauth_local_webserver']
    else:
        noauth_local_webserver = DEFAULT_NOAUTH_LOCAL_WEBSERVER

    flags = Flags(logging_level, noauth_local_webserver, auth_host_port)
    return flags, kwargs

def build(*args, **kwargs):
    ip = get_ipython()
    if 'google_credential_path' in kwargs:
        credential_path = kwargs['google_credential_path']
        del kwargs['google_credential_path']
    elif 'Googleapihelper' in ip.config and 'credential_path' in ip.config.Googleapihelper:
        credential_path = ip.config.Googleapihelper['credential_path']
    else:
        logger.info('Credential store path not specified, trying default: '+
                DEFAULT_CREDENTIALS_PATH)
        credential_path = DEFAULT_CREDENTIALS_PATH

    if 'google_secrets_path' in kwargs:
        secrets_path = kwargs['google_secrets_path']
        del kwargs['google_secrets_path']
    elif 'Googleapihelper' in ip.config and 'secrets_path' in ip.config.Googleapihelper:
        secrets_path = ip.config.Googleapihelper['secrets_path']
    else:
        logger.info('Secrets path not specified, trying default: '+
                DEFAULT_SECRETS_PATH)
        secrets_path = DEFAULT_SECRETS_PATH

    if 'redirect_uri' in kwargs:
        redirect_uri = kwargs['redirect_uri']
        del kwargs['redirect_uri']
    elif 'Googleapihelper' in ip.config and 'redirect_uri' in ip.config.Googleapihelper:
        redirect_uri = ip.config.Googleapihelper['redirect_uri']
    else:
        logger.info('Redirect uri not specified, trying default: '+
            DEFAULT_REDIRECT_URI)
        redirect_uri = DEFAULT_REDIRECT_URI

    if 'scope' in kwargs:
        scope = kwargs['scope']
        del kwargs['scope']
    elif 'Googleapihelper' in ip.config and 'scope' in ip.config.Googleapihelper:
        scope = ip.config.Googleapihelper['scope']
    else:
        logger.error('No scope specified in options or ipython config. '+
            'Store scope in ipython profile or specify on command line.')
        return None

    storage = Storage(credential_path)
    credentials = storage.get()

    if credentials is None:
        flow = flow_from_clientsecrets(secrets_path, scope=scope,
                    redirect_uri=redirect_uri)
        flags, kwargs = extract_flags_from_kwargs(kwargs)
        tools.run_flow(flow, storage, flags)
        credentials = storage.get()

    if credentials is None:
        logger.error("Unable to retrieve google oauth credentials")
        return None

    http = httplib2.Http()
    http = credentials.authorize(http)
    kwargs['http'] = http
    return discovery.build(*args, **kwargs)
