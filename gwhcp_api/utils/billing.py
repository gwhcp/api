import re


def credit_card_type(card_number):
    """
    Credit Card Type based on Credit Card Number

    :param str card_number: Credit Card Number

    :return: str
    """

    if re.match('^4[0-9]{12}(?:[0-9]{3})?$', card_number):
        return 'visa'
    elif re.match('^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$', card_number):
        return 'mastercard'
    elif re.match('^6(?:011|5[0-9]{2})[0-9]{12}$', card_number):
        return 'discover'
    elif re.match('^3[47][0-9]{13}$', card_number):
        return 'amex'
    else:
        return 'Unknown Credit Card Type'


def validate_credit_card(card_number):
    """
    Validate Credit Card

    Checks to make sure that the card passes a luhn mod-10 checksum

    :param str card_number: Credit Card Number
    :raise: TypeError
    """

    try:
        summ = 0

        num_digits = len(card_number)

        oddeven = num_digits & 1

        for count in range(num_digits):
            digit = int(card_number[count])

            if not ((count & 1) ^ oddeven):
                digit *= 2

            if digit > 9:
                digit -= 9

            summ += digit

        return (summ % 10) == 0
    except TypeError:
        return False
