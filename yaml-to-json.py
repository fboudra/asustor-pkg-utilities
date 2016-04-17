#!/usr/bin/python
# (C) 2016 Fathi Boudra <fboudra@gmail.com>

import itertools
import json
import os
import string
import sys
import yaml


# Find all placeholders in the input and replace them with the values of
# equivalently-named environment variables.
def main():
    with open(sys.argv[1]) as f:
        template = string.Template(f.read())

    placeholders = map(lambda match: match.group('named', 'braced'),
                       string.Template.pattern.finditer(template.template))
    placeholders = set(filter(None, itertools.chain(*placeholders)))

    # Pretend that missing environment variables are set to empty strings.
    # It would be better to throw an error on missing environment variables,
    # but this doesn't play nicely with Jenkins. When Jenkins adds parameters to
    # a triggered job via a properties file, any parameters explicitly set to
    # the empty string will be unset in the environment of the downstream job.
    substitutions = {x: os.environ.get(x) or '' for x in placeholders}
    lava_template = template.safe_substitute(substitutions)

    # FIXME: use ordered dictionaries - see http://pyyaml.org/ticket/29
    config = json.dumps(yaml.safe_load(lava_template), indent=2, separators=(',', ': '))
    print config


if __name__ == '__main__':
    main()
