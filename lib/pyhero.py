from collections import defaultdict
import json
import requests

from constants import (CLOUD_HERO_CACHE_NODES, CLOUD_HERO_CACHE_ENVIRONMENTS,
                       CLOUD_HERO_CACHE_OPTIONS)
from utils import remove_none_dict_values, cache_to_file, invalidate_cache

DEFAULT_CLIENT_VERSION = '1.0'
DEFAULT_TIMEOUT_SECONDS = 60
CLIENT_CACHE_TTL = 60
CLIENT_CACHE_OPTIONS_TTL = 60 * 60


ENDPOINTS = {
    'register': '/accounts/register',
    'login': '/accounts/tokens',
    'account_keys': '/accounts/keys?private=True',
    'providers': '/providers',
    'integrations': '/integrations',
    'nodes': '/environments/{}/nodes',
    'nodes_delete': '/nodes',
    'nodes_scale': '/environments/{}/scale',
    'environments': '/environments',
    'applications': '/applications',
    'swarm': '/swarm',
}


class Client(object):

    def __init__(self, base_url=None, token=None,
                 timeout=DEFAULT_TIMEOUT_SECONDS,
                 exception_callback=None,
                 clean_up_arguments=False,
                 user_agent=None):
        self.timeout = timeout
        self.token = token
        self.base_url = base_url
        self.user_agent = user_agent
        self.exception_callback = exception_callback
        self.clean_up_arguments = clean_up_arguments
        if self.base_url is None:
            self.base_url = 'https://api.cloudhero.io'

    def register(self, email, password, username):
        data = {
            'email': email,
            'password': password,
            'password_confirm': password,
            'name': username,
            'user_name': username
        }
        response = self._result(self.post_json(ENDPOINTS['register'],
                                               data=data))
        self._get_and_save_token(response)
        return response

    def login(self, email, password):
        data = {
            'email': email,
            'password': password,
        }
        response = self._result(self.post_json(ENDPOINTS['login'], data=data))
        return self._get_and_save_token(response)

    def show_providers(self):
        return self._result(self.options(ENDPOINTS['providers']))

    def create_provider(self, data):
        return self._result(self.post_json(ENDPOINTS['providers'],
                                           data=data))

    def list_providers(self):
        return self._result(self.get(ENDPOINTS['providers']))

    def delete_provider(self, item_id):
        return self._result(self.delete_item(ENDPOINTS['providers'], item_id))

    def list_key(self):
        return self._result(self.get(ENDPOINTS['account_keys']))

    def show_integration_types(self):
        return self._result(self.options(ENDPOINTS['integrations']))

    def create_integration(self, data):
        return self._result(self.post_json(ENDPOINTS['integrations'],
                                           data=data))

    def list_integrations(self):
        return self._result(self.get(ENDPOINTS['integrations']))

    def delete_integration(self, item_id):
        return self._result(self.delete_item(ENDPOINTS['integrations'],
                                             item_id))

    @invalidate_cache(CLOUD_HERO_CACHE_ENVIRONMENTS, CLOUD_HERO_CACHE_NODES)
    def add_environment(self, data):
        return self._result(self.post_json(ENDPOINTS['environments'],
                                           data=data))

    @cache_to_file(CLOUD_HERO_CACHE_ENVIRONMENTS, ttl=CLIENT_CACHE_TTL)
    def list_environments(self):
        return self._result(self.get(ENDPOINTS['environments']))

    @invalidate_cache(CLOUD_HERO_CACHE_ENVIRONMENTS, CLOUD_HERO_CACHE_NODES)
    def delete_environment(self, item_id, **params):
        kwargs = {'params': params}
        return self._result(self.delete_item(ENDPOINTS['environments'], item_id,
                                             **kwargs))

    @invalidate_cache(CLOUD_HERO_CACHE_ENVIRONMENTS, CLOUD_HERO_CACHE_NODES)
    def create_node(self, environment_id, data):
        return self._result(self.post_json(self._nodes_endpoint(environment_id),
                                           data=data))

    @cache_to_file(CLOUD_HERO_CACHE_NODES, ttl=CLIENT_CACHE_TTL)
    def get_all_details(self):
        applications = self._result(self.get(ENDPOINTS['applications']))
        nodes_data = defaultdict(list)
        for application in applications:
            for environment in application['environments']:
                for node in environment['nodes']:
                    node_name = node['name']
                    node_data = {
                        'node': {
                            'id': node['id'],
                            'name': node['name'],
                            'private_ip': node.get('private_ip'),
                            'public_ip': node.get('public_ip'),
                            'packages': node['packages'],
                            'size': node['size'],
                            'tags': node['tags']
                        },
                        'application': {
                            'name': application['application_name'],
                            'id': application['id'],
                        },
                        'environment': {
                            'name': environment['name'],
                            'id': environment['id'],
                            'location': environment['os_region'],
                        },
                        'provider': {
                            'id': environment['provider']['id'],
                            'name': environment['provider']['name'],
                            'username': environment['provider']['username'],
                            'type': environment['provider']['provider_type']
                        }
                    }
                    nodes_data[node_name].append(node_data)
        return nodes_data

    @invalidate_cache(CLOUD_HERO_CACHE_ENVIRONMENTS, CLOUD_HERO_CACHE_NODES)
    def delete_node(self, item_id, **params):
        kwargs = {'params': params}
        return self._result(self.delete_item(ENDPOINTS['nodes_delete'], item_id,
                                             **kwargs))

    @invalidate_cache(CLOUD_HERO_CACHE_ENVIRONMENTS, CLOUD_HERO_CACHE_NODES)
    def scale_up_node(self, environment_id, data):
        result = self.post_json(self._scale_endpoint(environment_id), data=data)
        return self._result(result)

    @invalidate_cache(CLOUD_HERO_CACHE_ENVIRONMENTS, CLOUD_HERO_CACHE_NODES)
    def scale_down_node(self, environment_id, data):
        result = self.delete_json(self._scale_endpoint(environment_id), data)
        return self._result(result)

    @cache_to_file(CLOUD_HERO_CACHE_OPTIONS, ttl=CLIENT_CACHE_OPTIONS_TTL)
    def show_options(self, endpoint):
        """
        Cache all OPTIONS requests.
        """
        return self._result(self.options(ENDPOINTS[endpoint]))

    def create_from_options(self, endpoint, data):
        return self._result(self.post_json(ENDPOINTS[endpoint], data=data))

    def post_json(self, endpoint, data=None, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['Content-Type'] = 'application/json'
        if self.clean_up_arguments:
            data = remove_none_dict_values(data)
        kwargs['data'] = json.dumps(data)
        return self.post(endpoint, **kwargs)

    def delete_json(self, endpoint, data=None, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['Content-Type'] = 'application/json'
        if self.clean_up_arguments:
            data = remove_none_dict_values(data)
        kwargs['data'] = json.dumps(data)
        return self.delete(endpoint, **kwargs)

    def delete_item(self, endpoint, item_id, **kwargs):
        endpoint = '{endpoint}/{id}'.format(endpoint=endpoint, id=item_id)
        return self.delete(endpoint, **kwargs)

    def options(self, endpoint, **kwargs):
        return self.make_request(endpoint, 'OPTIONS',
                                 **self._update_request(kwargs))

    def post(self, endpoint, **kwargs):
        return self.make_request(endpoint, 'POST',
                                 **self._update_request(kwargs))

    def get(self, endpoint, **kwargs):
        return self.make_request(endpoint, 'GET',
                                 **self._update_request(kwargs))

    def delete(self, endpoint, **kwargs):
        return self.make_request(endpoint, 'DELETE',
                                 **self._update_request(kwargs))

    def make_request(self, endpoint, method, **kwargs):
        method_type = method.lower()
        url = self.base_url + endpoint
        return requests.request(method_type, url, **kwargs)

    def _nodes_endpoint(self, environment_id):
        return ENDPOINTS['nodes'].format(environment_id)

    def _scale_endpoint(self, environment_id):
        return ENDPOINTS['nodes_scale'].format(environment_id)

    def _update_request(self, kwargs):
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('headers', {})

        if self.token:
            kwargs['headers']['Authentication-Token'] = self.token

        if self.user_agent:
            kwargs['headers']['User-Agent'] = self.user_agent

        return kwargs

    def _result(self, response, json=True):
        try:
            response.raise_for_status()
        except Exception as exception:
            if self.exception_callback:
                return self.exception_callback(exception)

        if json:
            return response.json()
        return response.text

    def _get_and_save_token(self, response):
        if isinstance(response, dict) and response.get('persistent_token'):
            self.token = response['persistent_token']
        return self.token
