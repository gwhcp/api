import socket

from ipware.ip import get_client_ip

from login import models


def handle_login(sender, request, user, **kwargs):  # noqa
    """
    Handle the login event and save access log.

    :param sender: The sender of the signal.
    :param request: The login request object.
    :param user: The authenticated user.
    :param kwargs: Additional keyword arguments.
    :return: None
    """
    ip = get_client_ip(request)

    models.AccessLog.objects.create(
        account=user,
        ipaddress=ip[0],
        reverse_ipaddress=socket.getfqdn(ip[0])
    )
