import errno
import functools
import json
import os
import time

from constants import CLOUD_HERO_CACHE_OPTIONS, NotFound


def write_to_file(content, file_path, is_json=False):
    expanded_file_path = os.path.expanduser(file_path)
    dirname = os.path.dirname(expanded_file_path)
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(expanded_file_path, 'w') as file_handler:
        if is_json:
            json.dump(content, file_handler)
        else:
            file_handler.write(content)


def read_from_file(file_path, is_json=False):
    expanded_file_path = os.path.expanduser(file_path)
    try:
        with open(expanded_file_path, 'r') as file_handler:
            if is_json:
                return json.load(file_handler)
            return file_handler.read()
    except IOError as exception:
        if exception.errno == 2:
            return None
        raise


def cache_to_file(file_path, ttl=60):
    def wrap(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_file = file_path
            if cache_file == CLOUD_HERO_CACHE_OPTIONS:
                cache_file = cache_file + '/' + args[1]

            # Try reading from cache file, if it was created within the TTL.
            expanded_file_path = os.path.expanduser(cache_file)
            cached = read_cache_file(expanded_file_path, ttl)
            if cached:
                return cached

            # Request data.
            result = func(*args, **kwargs)

            # Write data to cache file.
            write_to_file(result, expanded_file_path, is_json=True)

            return result

        return wrapper

    return wrap


def invalidate_cache(*file_paths):
    def wrap(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for file_path in file_paths:
                expanded_file_path = os.path.expanduser(file_path)
                try:
                    os.remove(expanded_file_path)
                except OSError as exc:
                    if exc.errno == errno.ENOENT:
                        continue
                    raise
            return func(*args, **kwargs)
        return wrapper
    return wrap


def read_cache_file(file_path, ttl):
    if not os.path.exists(file_path):
        return None
    file_stats = os.stat(file_path)
    creation_time = file_stats.st_ctime
    if time.time() - creation_time < float(ttl):
        cached = read_from_file(file_path, is_json=True)
        return cached
    return None


def remove_none_dict_values(obj):
    """
    Remove None values from dict.
    """
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none_dict_values(x) for x in obj)
    elif isinstance(obj, dict):
        return type(obj)((k, remove_none_dict_values(v))
                         for k, v in obj.items()
                         if v is not None)
    else:
        return obj


def set_keys_to_empty_values(obj):
    if isinstance(obj, dict):
        return dict((k, set_keys_to_empty_values(v)) for k, v in obj.items())
    else:
        return ''


def get_docker_ip_for_environment(node_details, environment_id):
    environment_found = False
    for node, nodes_data in node_details.items():
        for node_data in nodes_data:
            if node_data['environment']['id'] == environment_id:
                environment_found = True
                if node_data['node'].get('public_ip'):
                    return node_data['node']['public_ip']

    if environment_found is False:
        raise NotFound('Environment {} not found!'.format(environment_id))
