import configobj
import sys
import validate

CONFIG_SPEC = """
[privacyidea]
endpoint = string
realm = string(default='')

[ldap-backend]
host = string
port = integer
use-tls = boolean

[ldap-proxy]
port = integer
hostname = string(default='')
passthrough-binds = force_list
bind-service-account = boolean(default=False)
allow-search = boolean(default=False)

[service-account]
dn = string
password = string

[bind-cache]
enabled = boolean
timeout = integer(default=3)
"""

def report_config_errors(config, result):
    """
    Interpret configobj results and report configuration errors to the user.
    """
    # from http://www.voidspace.org.uk/python/configobj.html#example-usage
    print 'Invalid config file:'
    for entry in configobj.flatten_errors(config, result):
        # each entry is a tuple
        section_list, key, error = entry
        if key is not None:
            section_list.append(key)
        else:
            section_list.append('(missing section)')
        section_string = ', '.join(section_list)
        if error == False:
            error = 'Invalid value (or section).'
        print '{}: {}'.format(section_string, error)


def load_config(filename):
    with open(filename, 'r') as f:
        config = configobj.ConfigObj(f, configspec=CONFIG_SPEC.splitlines())

    validator = validate.Validator()
    result = config.validate(validator, preserve_errors=True)
    if result != True:
        report_config_errors(config, result)
        sys.exit(1)
    return config