import packages


def parsedb(name, file):
    import tarfile
    import re
    tar = tarfile.open(file, mode="r:*")

    for member in [f for f in tar.getmembers() if "desc" in f.name]:
        file = tar.extractfile(member)
        desc = file.read().decode("utf-8")
        results = re.findall(r"%([A-Z0-9]+)%\n(.+)", desc)
        pkginfo = {}
        for a, b in results:
            pkginfo[a] = b

        packages.write_package(pkginfo['NAME'], "arch", name)


parsedb('core', 'core.db')
