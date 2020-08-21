#!/bin/python3

import yaml
import yamale
import sys


def make_single(schema, package_info):

    pkg = yaml.safe_load(package_info)
    yamale.validate(schema, yamale.make_data(content=package_info))

    out = []

    default_tags = [tag['tag']
                    for tag in pkg['tags'] if 'default' in tag and tag['default']]

    assert len(default_tags) == 1

    out.append("{} {}".format(pkg['name'], default_tags[0]))

    for tag in pkg['tags']:
        for p in tag['packages']:
            out.append("{} {} {} {}".format(
                tag['tag'], p['distro'], p['repo'], p['package']))
    return "\n".join(out)


def main():
    assert len(sys.argv) > 1
    schema = yamale.make_schema(sys.argv[1])

    package_yaml = sys.stdin
    if len(sys.argv) > 2:
        package_yaml = open(sys.argv[2])
    package_yaml = package_yaml.read()

    print(make_single(schema, package_yaml))


if __name__ == "__main__":
    main()
