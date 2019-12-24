def init_folders():
    import argparse, os, pathlib, shutil
    parser = argparse.ArgumentParser(prog="pyfoot", description=__doc__)
    parser.add_argument("init")
    parser.add_argument("name")
    parser.add_argument("-dir", nargs="?", default=".")
    args = parser.parse_args()
    if args.init == "init":
        os.chdir(args.dir)
        os.mkdir(args.name)
        os.chdir(args.name)
        os.mkdir("Graphics")
        os.mkdir("Sounds")
        examplefile = (pathlib.Path(__file__).parent/"Examples/example.py").as_posix()
        shutil.copy2(examplefile, pathlib.Path(".").as_posix())


init_folders()