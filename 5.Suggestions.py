def get_value(data, key, default, lookup=None, mapper=None):
    """
    Finds the value from data associated with key, or default if the
    key isn't present.
    If a lookup enum is provided, this value is then transformed to its
    enum value.
    If a mapper function is provided, this value is then transformed
    by applying mapper to it.
    """
    # Firstly, to check if the key is in the data dictionary
    if key not in data:
        return default
    return_value = data[key]

    if return_value is None or return_value == "":
        return_value = default

    if lookup:
        return_value = lookup.get(return_value, default)
        # To use get() for handling the missing keys

    if mapper:
        return_value = mapper(return_value)

    return return_value


def ftp_file_prefix(namespace):
    """
    Given a namespace string with dot-separated tokens, returns the
    string with the final token replaced by 'ftp'.
    Example: 'a.b.c' => 'a.b.ftp'
    """
    # First suggestion, to split the namespace by dots
    tokens = namespace.split(".")

    # Then, to be assured that there is at least one token
    if len(tokens) < 1:
        raise ValueError("Namespace must contain at least one token")

    return ".".join(tokens[:-1]) + '.ftp'


def string_to_bool(string):
    """
    Returns True if the given string is 'true' case-insensitive,
    False if it is 'false' case-insensitive.
    Raises ValueError for any other input.
    """
    # Firstly, converting the input string to lowercase (case-insensitive comparison)
    lower_string = string.lower()
    if lower_string == 'true':
        return True
    if lower_string == 'false':
        return False
    raise ValueError(f'String "{string}" is neither "true" nor "false"')


def config_from_dict(dict):
    """
    Given a dict representing a row from a namespaces CSV file,
    returns a DAG configuration as a pair whose first element is the
    DAG name and whose second element is a dict describing the DAG's properties.
    """

    # First suggestion, to add a check to ensure required keys exist in the dict before accessing them.
    if 'Namespace' not in dict or 'Airflow DAG' not in dict:
        raise KeyError("Missing required keys in the input dictionary.")

    namespace = dict['Namespace']

    # Secondly, to use more descriptive key names for better readability.
    dag_name = dict['Airflow DAG']

    return (
        dag_name,
        {
            "earliest_available_delta_days": get_value(dict, 'Earliest Delta Days', 0),
            "lif_encoding": 'json',
            "earliest_available_time": str(get_value(dict, 'Available Start Time', '07:00')),
            "latest_available_time": str(get_value(dict, 'Available End Time', '08:00')),
            "require_schema_match": get_value(dict, 'Requires Schema Match', 'True', mapper=string_to_bool),
            "schedule_interval": get_value(dict, 'Schedule', '1 7 * * *'),

            # Suggestion: Handle the case where `DeltaDays` might not be defined or passed correctly.
            "delta_days": get_value(dict, 'Delta Days', 'DAY_BEFORE',
                                    lookup=DeltaDays if 'DeltaDays' in globals() else None),

            "ftp_file_wildcard": get_value(dict, 'File Naming Pattern', None),

            # TO add a check to ensure the ftp_file_prefix function doesn't fail on an empty namespace.
            "ftp_file_prefix": get_value(dict, 'FTP File Prefix', ftp_file_prefix(namespace) if namespace else None),

            "namespace": namespace
        }
    )


