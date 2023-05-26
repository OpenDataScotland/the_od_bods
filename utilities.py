from loguru import logger
import glob
import os
from pathlib import Path
from textwrap import dedent


def clear_folder(path: str, verbose: bool = False):
    """
    Takes the path provided and deletes all the files within it

    Arguments:
        path: The folder path for deleting the files
        verbose: Add more detailed logging
    """
    # Safety check: Make sure path ends with trailing slash
    if not path.endswith("/") and not path.endswith("\\"):
        path = f"{path}/"

    # Get all files and delete them
    files = glob.glob(f"{path}*")
    for f in files:
        try:
            os.remove(f)
            if verbose:
                logger.info(f"Deleted {f}")
        except:
            logger.error(f"Failed to delete {f}")


def safe_delete_file(path: str, verbose: bool = False):
    """
    Takes the file path provided and deletes it if it exists

    Arguments:
        path: The file path for deleting the file
        verbose: Add more detailed logging
    """
    if os.path.exists(path):
        os.remove(path)
        if verbose:
            logger.info(f"Deleted {path}")
    else:
        logger.warning(f'File "{path}" does not exist')


def init_logs(verbose: str = False):
    Path("log.json").touch()
    if verbose:
        logger.info("Written log.json")
    with open("log.md", "w+") as f:
        f.write("# pipeline error log\n\n")
        f.write("## Unaccessible Webpages\n\n")
        f.write("|URL | Error Code | Error Reason|\n")
        f.write("|--- | --- | ---|\n")
        f.close()
    if verbose:
        logger.info("Written log.md")
