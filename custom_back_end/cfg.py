from base64 import b64decode
import logging
import sys

from sqlalchemy import create_engine

import custom_back_end.passwords as passwords

logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


class PysharkDB:
    username = "tcuser"
    password = b64decode(passwords.pysharkdb).decode("utf-8")
    name = "testchipdb"
    host = "10.31.13.14"
    port = 3306


class OpenSharknetDB:
    username = "opensharknetltd"
    password = b64decode(passwords.opensharknetdb).decode("utf-8")
    name = "sharknet4db"  # database
    host = "10.31.13.14"
    port = 3306


class TeggyDB:
    username = "tcuser"
    password = b64decode(passwords.teggydb).decode("utf-8")
    name = "TeggyDB"
    host = "10.31.13.14"
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
