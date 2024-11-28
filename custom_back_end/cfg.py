from base64 import b64decode

import passwords


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