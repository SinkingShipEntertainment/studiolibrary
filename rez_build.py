"""Install for REZ."""

# Standard imports
import argparse
import os
import shutil
import sys


def copy_dirs_and_files(dirs, files, source_dir, dest_dir):

    # Copy all the desired dirs
    for d in dirs:
        src_d = source_dir + "/" + d
        dst_d = dest_dir + "/" + d
        try:
            shutil.copytree(src_d, dst_d, ignore=shutil.ignore_patterns("*.pyc"))
            print("Copying: {0} --> {1}".format(src_d, dst_d))
        except Exception as e:
            print(str(e))

    # Copy all the desired files
    for f in files:
        src_f = source_dir + "/" + f
        dst_f = dest_dir + "/" + f
        try:
            shutil.copy(src_f, dst_f)
            print("Copying: {0} --> {1}".format(src_f, dst_f))
        except Exception as e:
            print(str(e))


def symlink(dirs, source_dir, dest_dir):

    # Symlink all the desired dirs
    for d in dirs:
        try:
            src_d = source_dir + "/" + d
            symlink = dest_dir + "/" + d
            print("Symlinking: {0} --> {1}".format(symlink, src_d))
            os.symlink(src_d, symlink)
        except Exception as e:
            print(str(e))


def str2bool(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        return False


if __name__ == "__main__":

    print("----------- Building Python Package -----------")

    # Collect the source and destination directories
    source_dir = os.environ["REZ_BUILD_SOURCE_PATH"]
    dest_dir = os.environ["REZ_BUILD_INSTALL_PATH"]

    dirs = ["src", "config"]
    files = ["install.gif", "install.mel", "install.py"]

    if os.environ["REZ_BUILD_TYPE"] == "local":
        # Clear the destination directory if it exists
        if os.path.exists(dest_dir):
            try:
                for f in os.listdir(dest_dir):
                    print("Evaluating {0}".format(f))
                    full_path = dest_dir + "/" + f
                    if os.path.islink(full_path):
                        print("    Removing symlink: {0}".format(f))
                        os.unlink(full_path)
                    elif os.path.isfile(full_path):
                        print("    Removing file: {0}".format(f))
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        print("    Removing dir: {0}".format(f))
                        shutil.rmtree(full_path)
            except Exception as e:
                print(str(e))


        if ("__PARSE_ARG_SYMLINK" in os.environ) and (str2bool(os.environ["__PARSE_ARG_SYMLINK"])):
            symlink(dirs, source_dir, dest_dir)
        else:
            copy_dirs_and_files(dirs, files, source_dir, dest_dir)

    else:
        copy_dirs_and_files(dirs, files, source_dir, dest_dir)

    print("----------- Done -----------")
