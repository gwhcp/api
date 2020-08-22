import socket

from ipware.ip import get_client_ip

from login import models


def handle_login(sender, request, user, **kwargs):  # noqa
    ip = get_client_ip(request)

    models.AccessLog.objects.create(
        account=user,
        ipaddress=ip[0],
        reverse_ipaddress=socket.getfqdn(ip[0])
    )
