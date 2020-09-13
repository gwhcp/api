import hmac
import uuid
from hashlib import sha1

from cryptography.fernet import Fernet
from django.conf import settings
from passlib.hash import scram
from passlib.hash import sha512_crypt


def encrypt_string(string_to_encrypt):
    """
    Encrypt String

    :param str string_to_encrypt: Unencrypted String

    :return: str
    """

    cipher = Fernet(settings.FERNET_KEY)

    if not isinstance(string_to_encrypt, bytes):
        string_to_encrypt = string_to_encrypt.encode('UTF-8')

    return cipher.encrypt(string_to_encrypt).decode('UTF-8')


def decrypt_string(string_to_decrypt):
    """
    Decrypt String

    :param str string_to_decrypt: Encrypted String

    :return: str
    """

    cipher = Fernet(settings.FERNET_KEY)

    if not isinstance(string_to_decrypt, bytes):
        string_to_decrypt = string_to_decrypt.encode('UTF-8')

    return cipher.decrypt(string_to_decrypt).decode('UTF-8')


def dovecot_password(password):
    """
    Create Dovecot Compatible Password

    :param str password: Password

    :return str
    """

    return sha512_crypt(password)


def xmpp_password(password):
    """
    Create Compatible Password

    :param str password: Password

    :return str
    """

    uuid_salt = str(uuid.uuid4())

    sscram = scram.using(
        algs='SHA1',
        rounds=4096,
        salt=uuid_salt.encode('UTF-8')
    ).hash(password)

    salted_password = scram.extract_digest_info(sscram, "sha1")[2]

    stored_key = sha1(hmac.new(salted_password, "Client Key".encode('UTF-8'), sha1).digest()).hexdigest()

    server_key = hmac.new(salted_password, "Server Key".encode('UTF-8'), sha1).hexdigest()

    return {
        'salt': uuid_salt,
        'stored_key': stored_key,
        'server_key': server_key
    }
