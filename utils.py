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
