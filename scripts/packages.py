import yaml
import os.path


class Package(yaml.YAMLObject):
    yaml_tag = '!pkg'

    def __init__(self, name, tags):
        self.name = name.replace('_', '-').replace('+', '-').lower()
        self.tags = tags
        # run a quick check if tags has a default

    @staticmethod
    def load(yml):
        yaml.add_path_resolver('!pkg', [], dict)
        for i in range(0, 30):
            # super hacky but idc - ive wasted too much time on this
            yaml.add_path_resolver('!tag', ['tags', i], dict)
            for j in range(0, 30):
                yaml.add_path_resolver(
                    '!src', ['tags', i, 'packages', j], dict)
        return yaml.load(yml, Loader=yaml.loader.FullLoader)

    def dump_yaml(self):
        import yaml

        def noop(self, *args, **kw):
            pass

        yaml.emitter.Emitter.process_tag = noop
        return yaml.dump(self)


class Tag(yaml.YAMLObject):
    yaml_tag = '!tag'

    def __init__(self, name, packages, default=False):
        self.tag = name
        self.packages = packages
        self.default = default


class Source(yaml.YAMLObject):
    yaml_tag = '!src'

    def __init__(self, distro, package, repo):
        self.distro = distro
        self.package = package
        self.repo = repo


def write_package(name, distro, repo):
    existing = None
    if os.path.exists("packages/" + name + ".yaml"):
        with open("packages/" + name + ".yaml", "r") as f:
            existing = Package.load(f.read())

    if existing is None:
        existing = Package(name, [Tag("stable", [], True)])

    existing.tags[0].packages.append(Source(distro, name, repo))
    with open("packages/" + name + ".yaml", "w") as f:
        f.write(existing.dump_yaml())
