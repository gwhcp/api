def error_to_human_readable(errors):
    """
    DRF exceptions to human readable

    :param dict errors: Errors

    :return: str
    """

    error = str()

    for item in errors.items():
        error += f"{item[1][0]}\n"

    return error
