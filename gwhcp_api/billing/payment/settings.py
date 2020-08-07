def merchants():
    return {
        'authorize': 'Authorize.net',
        'paypal': 'Paypal.com'
    }


def merchant_methods(name):
    """
    Merchant methods

    :param str name: Name of merchant

    :return: dict
    """

    from billing.payment.merchant import authorize

    return {
        'authorize': authorize.Payment.methods()
    }.get(name)


# TODO check where this is even used and remove it
def merchant_settings(name):
    """
    Specific Merchant Settings

    :param str name: Name of merchant

    :return: dict
    """

    from billing.payment.merchant import authorize

    return {
        'authorize': {
            'methods': authorize.Payment.methods()
        }
    }.get(name)
