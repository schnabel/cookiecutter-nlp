import re
import sys


DNS_REGEX = r'^[a-zA-Z][-a-zA-Z0-9]*[a-zA-Z]+$'

service_dns = '{{ cookiecutter.service_dns }}'

if not re.match(DNS_REGEX, service_dns):
    print('ERROR: %s is not a valid service dns!' % service_dns)

    # exits with status 1 to indicate failure
    sys.exit(1)