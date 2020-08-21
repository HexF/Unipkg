#!/bin/python3

import sys
import io
import re

DEFAULT_FORMAT = 1


class Source:
    def __init__(self, sourcedata, fmt=DEFAULT_FORMAT):
        {1: self.fmt_1}[fmt](sourcedata)

    def fmt_1(self, sourcedata):
        data = sourcedata.split(" ")

        self.tag = data[0]
        self.distro = data[1]
        self.repository = data[2]
        self.package = data[3]


class Package:
    def __init__(self, pkgdata, fmt=DEFAULT_FORMAT):
        {1: self.fmt_1}[fmt](pkgdata)

    def fmt_1(self, pkgdata):
        self.name = pkgdata[0]
        self.default_tag = pkgdata[1]
        self.sources = [Source(s.strip(), 1)
                        for s in pkgdata[2].strip().split("\n")]


class Database:
    def __init__(self, db_file):
        lines = db_file.split("\n")
        header = lines[0].split(" ")

        assert header[0] == "UNIPKG"

        self.format = int(header[1])
        self.commit = header[2]
        self.sequence = int(header[3])
        self.packages = []

        {1: self.fmt_1}[self.format](db_file)

    def fmt_1(self, db):
        PKG_REGEX = re.compile(
            r"^([a-z]+) ([a-z]+)((\n [a-z \-]+)+)", re.MULTILINE)
        self.packages = [Package(p, self.format)
                         for p in PKG_REGEX.findall(db)]

    def to_dict(self):
        import json
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))

    def dump_yaml(self):
        import yaml

        def noop(self, *args, **kw):
            pass

        yaml.emitter.Emitter.process_tag = noop
        return yaml.dump(self)

    def dump_json(self):
        import json
        return json.dumps(self.to_dict())

    def dump_toml(self):
        import toml
        return toml.dumps(self.to_dict())

    def dump_fmt1(self):
        out = []
        out.append("UNIPKG {} {} {}".format(
            self.format, self.commit, self.sequence))

        for package in self.packages:
            out.append("{} {}".format(package.name, package.default_tag))
            for source in package.sources:
                out.append(" {} {} {} {}".format(
                    source.tag, source.distro, source.repository, source.package))

        return "\n".join(out)


def main(db_path, format):
    with open(db_path) as db_file:
        db = db_file.read()
        parsed = Database(db)
        print({'yaml': parsed.dump_yaml,
               'json': parsed.dump_json,
               'toml': parsed.dump_toml,
               'fmt1': parsed.dump_fmt1}[format]())


if __name__ == "__main__":
    assert len(sys.argv) == 3   # Make sure we have our `db` file and fmt
    assert sys.argv[2] in ['yaml', 'json', 'toml', 'fmt1']
    main(sys.argv[1], sys.argv[2])
