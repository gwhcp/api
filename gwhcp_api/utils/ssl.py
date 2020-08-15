from OpenSSL import SSL
from OpenSSL import crypto


def create_csr(country, state, locality, org_name, org_unit_name, common_name, email_address, sign='sha1'):
    """
    Create CSR & RSA Keys

    :param str country: Country Code
    :param str state: State Code
    :param str locality: City
    :param str org_name: Organization Name
    :param str org_unit_name: NA
    :param str common_name: Domain Name
    :param str email_address: Email Address
    :param str|bytes sign: Encryption Type

    :return: dict
    """

    # create a key pair
    rsa = crypto.PKey()
    rsa.generate_key(crypto.TYPE_RSA, 2048)

    # create csr
    csr = crypto.X509Req()
    csr.get_subject().C = country
    csr.get_subject().ST = state
    csr.get_subject().L = locality
    csr.get_subject().O = org_name
    csr.get_subject().OU = org_unit_name
    csr.get_subject().CN = common_name
    csr.get_subject().emailAddress = email_address
    csr.set_pubkey(rsa)
    csr.sign(rsa, sign)

    return {
        'csr': crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr),
        'rsa': crypto.dump_privatekey(crypto.FILETYPE_PEM, rsa)
    }


def create_self_signed(country, state, locality, org_name, org_unit_name, common_name, email_address, sign='sha1'):
    """
    Create Self-Signed Certificate

    :param str country: Country Code
    :param str state: State Code
    :param str locality: City
    :param str org_name: Organization Name
    :param str org_unit_name: NA
    :param str common_name: Domain Name
    :param str email_address: Email Address
    :param str|bytes sign: Encryption Type

    :return: dict
    """

    # create a key pair
    rsa = crypto.PKey()
    rsa.generate_key(crypto.TYPE_RSA, 2048)

    # create a self-signed cert
    crt = crypto.X509()
    crt.get_subject().C = country
    crt.get_subject().ST = state
    crt.get_subject().L = locality
    crt.get_subject().O = org_name
    crt.get_subject().OU = org_unit_name
    crt.get_subject().CN = common_name
    crt.get_subject().emailAddress = email_address
    crt.set_serial_number(1000)
    crt.gmtime_adj_notBefore(0)
    # crt.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    crt.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    crt.set_issuer(crt.get_subject())
    crt.set_pubkey(rsa)
    crt.sign(rsa, sign)

    return {
        'rsa': crypto.dump_privatekey(crypto.FILETYPE_PEM, rsa),
        'crt': crypto.dump_certificate(crypto.FILETYPE_PEM, crt)
    }


def validate_cert_with_private_key(cert, private_key):
    """
    Check if Certificate Matches Private Key

    :param str|bytes cert: Certificate
    :param str private_key: Private Key

    :raise: crypto.Error

    :return: bool
    """

    try:
        rsa = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)
    except crypto.Error:
        return False

    try:
        crt = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    except crypto.Error:
        return False

    context = SSL.Context(SSL.TLSv1_METHOD)
    context.use_privatekey(rsa)
    context.use_certificate(crt)

    try:
        context.check_privatekey()

        return True
    except SSL.Error:
        return False
