#! py -3

from argparse import ArgumentParser

PARSER = ArgumentParser(description="Search Deflector Build Script")
ARGUMENTS = {
    "all": {
        "flags": ("-a", "-all"),
        "action": "store_true",
        "help": "build setup, updater, and deflector binaries"
    },
    "setup": {
        "flags": ("-s", "-setup"),
        "action": "store_true",
        "help": "build setup binary"
    },
    "updater": {
        "flags": ("-u", "-updater"),
        "action": "store_true",
        "help": "build updater binary"
    },
    "deflector": {
        "flags": ("-d", "-deflector"),
        "action": "store_true",
        "help": "build deflector binary"
    },
    "installer": {
        "flags": ("-i", "-installer"),
        "action": "store_true",
        "help": "build installer executable"
    },
    "clean": {
        "flags": ("-c", "-clean"),
        "action": "store_true",
        "help": "remove object and debug files"
    },
    "copy": {
        "flags": ("-cp", "-copy"),
        "action": "store_true",
        "help": "copy libraries and imports"
    },
    "mode": {
        "flags": ("-m", "-mode"),
        "choices": ("r", "release", "s", "store", "d", "debug"),
        "default": "release",
        "help": "build classic installer, store edition, or debug mode"
    },
    "source": {
        "flags": "-source",
        "default": "source",
        "metavar": "<path>",
        "help": "path of the source code"
    },
    "libs": {
        "flags": "-libs",
        "default": "libs",
        "metavar": "<path>",
        "help": "path of the libraries"
    },
    "out": {
        "flags": "-out",
        "default": "build",
        "metavar": "<path>",
        "help": "path of the output binaries"
    },
    "verbose": {
        "flags": ("-v", "-verbose"),
        "action": "store_true",
        "help": "show log output"
    }
}


def assemble_args(parser, arguments):
    for dest, kwargs in arguments.items():
        flags = kwargs["flags"]
        kwargs.pop("flags", None)

        if isinstance(flags, str):
            parser.add_argument(flags, dest=dest, **kwargs)
        else:
            parser.add_argument(*flags, dest=dest, **kwargs)


def reform_args(args):
    if args.mode == "r":
        args.mode = "release"
    elif args.mode == "s":
        args.mode = "store"
    elif args.mode == "d":
        args.mode = "debug"

    if args.mode == "debug":
        args.installer = False
        args.clean = False
    elif args.mode in ("release", "store"):
        args.all = True
        args.installer = True
        args.clean = True

    if args.all:
        args.setup = True
        args.updater = True
        args.deflector = True

    return args


def copy_files(libs, out):
    pass


def clean_files(out):
    from glob import glob
    from os import remove
    from os.path import join

    for file in glob(join(out, "*.pdb")):
        print("Removing debug file: " + file)
        remove(file)

    for file in glob(join(out, "*.obj")):
        print("Removing object file: " + file)
        remove(file)


def build_setup(source, libs, out):
    pass


def build_updater(source, libs, out):
    pass


def build_deflector(source, libs, out):
    pass


def build_installer(out):
    pass


if __name__ == "__main__":
    from os.path import join
    from shutil import rmtree

    assemble_args(PARSER, ARGUMENTS)

    ARGS = reform_args(PARSER.parse_args())

    BIN_PATH = join(ARGS.out, "bin")
    VARS_PATH = join(ARGS.out, "vars")
    DIST_PATH = join(ARGS.out, "dist")

    if not ARGS.verbose:
        print = lambda *_, **__: None

    if ARGS.mode in ("release", "store"):
        print("Removing build path: " + ARGS.out)
        rmtree(ARGS.out, ignore_errors=True)

    if ARGS.setup:
        build_setup(ARGS.source, ARGS.libs, ARGS.out)

    if ARGS.updater:
        build_updater(ARGS.source, ARGS.libs, ARGS.out)

    if ARGS.deflector:
        build_deflector(ARGS.source, ARGS.libs, ARGS.out)

    if ARGS.installer:
        build_installer(ARGS.out)

    if ARGS.copy:
        copy_files(ARGS.libs, ARGS.out)

    if ARGS.clean:
        clean_files(BIN_PATH)