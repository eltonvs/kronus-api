def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)
    return default


def get_error_message(exc):
    if hasattr(exc, 'message_dict'):
        return exc.message_dict

    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        return ', '.join(error_msg)

    if error_msg is None:
        return str(exc)

    return error_msg
