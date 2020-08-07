import ipaddress

from database import models


def available(assigned):
    """
    Available

    :param str assigned: Assigned (public / reserved)

    :return: list
    """

    available_array = []

    range_array = []

    used_array = []

    for ipaddress_setup in models.IpaddressSetup.objects.filter(assigned=assigned, is_active=True):
        for ip in list(ipaddress.ip_network(ipaddress_setup.network + '/' + str(ipaddress_setup.subnet)).hosts()):
            range_array.append((str(ip), str(ip) + ' - ' + ipaddress_setup.name))

        for ipaddress_pool in models.IpaddressPool.objects.filter(ipaddress_setup=ipaddress_setup):
            used_array.append((str(ipaddress_pool.ipaddress),
                               str(ipaddress_pool.ipaddress) + ' - ' + ipaddress_pool.ipaddress_setup.name))

        available_array.extend(sorted(list(set(range_array) - set(used_array))))

    return available_array


def ip_in_network(assigned, ip):
    for item in models.IpaddressSetup.objects.filter(assigned=assigned, is_active=True):
        if ipaddress.ip_address(str(ip)) in ipaddress.ip_network(item.network + '/' + str(item.subnet)):
            return True

    return False


def pool_id(value):
    """
    Pool ID

    :param str value: IP Address

    :return: int
    """

    ip = ipaddress.ip_address(value)

    for item in models.IpaddressSetup.objects.all():
        if ip in list(ipaddress.ip_network(item.network + '/' + str(item.subnet)).hosts()):
            return item
