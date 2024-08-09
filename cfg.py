import datetime as dt
import getpass
import logging
import socket
from base64 import b64decode
from pathlib import Path

import pytz
import passwords

PROGRAM_NAME = "DataViewer"
DEVELOPER_UNAMES = ["rboone", "localadmin"]
LNX_SERVERS = ["cerberus", "seabert", "speedy", "localhost"]  # localhost == testing vm


class PysharkDB:
    username = "tcuser"
    password = b64decode(passwords.pysharkdb).decode("utf-8")
    name = "testchipdb"
    host = "10.31.13.30"
    port = 3306


class OpenSharknetDB:
    username = "opensharknetltd"
    password = b64decode(passwords.opensharknetdb).decode("utf-8")
    name = "opensharknet"
    host = "10.31.13.31"
    port = 3306


class TeggyDB:
    username = "tcuser"
    password = b64decode(passwords.teggydb).decode("utf-8")
    name = "Teggy"
    host = "10.31.13.30"
    port = 3306


class VaultDB:
    username = "root"
    password = b64decode(passwords.vaultdb).decode("utf-8")
    name = "vault_db"
    host = "127.0.0.1"
    port = 3306


class ServerUser:
    """user with rights on the vault server."""

    username = "custsoft"
    password = b64decode(passwords.custsoft).decode("utf-8")


# <editor-fold desc="AUTOMATIC STUFF BELOW, DON'T TOUCH">
TIMEZONE = pytz.timezone("Europe/Brussels")

IN_WINE = socket.gethostname() in LNX_SERVERS  # Wine on linux
IN_THE_VAULT = socket.gethostname() == "cerberus"
if IN_THE_VAULT:
    LICENSE_SERVER = "127.0.0.1"

# LOGGING CONFIG
if not IN_WINE:  # Win
    log_dir = Path(r"C:\Sofics\logs")
    if not log_dir.exists():
        Path.mkdir(log_dir, parents=True)
    log_file = log_dir / f"{PROGRAM_NAME}.log"
else:  # Wine on linux server:
    log_dir = Path(r"Z:\opt\Sofics\logs")
    if not log_dir.exists():
        Path.mkdir(log_dir, parents=True)
    log_file = log_dir / f"{PROGRAM_NAME}_{getpass.getuser()}.log"  # shared system => + _user
if getpass.getuser() in DEVELOPER_UNAMES:
    # Don't log output to file + show debug level:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M %m/%d",
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        filename=log_file,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M %m/%d",
    )
# </editor-fold>
