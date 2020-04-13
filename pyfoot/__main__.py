def init_folders():
    import argparse
    import os
    import pathlib
    import shutil
    parser = argparse.ArgumentParser(prog="pyfoot", description="This is the pyfoot cli used for quickly creating the baseline structure of your Project.")
    parser.add_argument("init", choices=["init"])
    parser.add_argument("projectname", help="Name of the Project")
    parser.add_argument("-dir", nargs="?", default=".", help="Can be specified to initialize the project in a given subdirectory")
    args = parser.parse_args()
    if args.init == "init":
        p = pathlib.Path(args.dir)
        p.mkdir(parents=True, exist_ok=True)
        os.chdir(p.as_posix())
        os.mkdir(args.projectname)
        os.chdir(args.projectname)
        os.mkdir("Graphics")
        os.mkdir("Sounds")
        examplefile = (pathlib.Path(__file__).parent / "Examples/example.py").as_posix()
        shutil.copy2(examplefile, pathlib.Path(".").as_posix())


init_folders()
