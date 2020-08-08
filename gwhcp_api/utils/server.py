import random
import re

from django.db.models import Q

from database import models


class Server:
    def __init__(self, domain, hardware_type, target_type=None):
        self.domain = domain

        self.hardware_type = hardware_type

        self.target_type = target_type

        if domain is None:
            raise ValueError('Domain object is missing.')

        if hardware_type is None:
            raise ValueError('Hardware Type is missing.')

    @staticmethod
    def _find_missing_low_number(array):
        """
        Find Missing Number(s) in list

        :param list array: List of INT's

        :return: None|int
        """

        set1 = set(range(1, max(array)))

        set2 = set(array)

        set_math = set1 - set2

        try:
            return min(set_math)
        except ValueError:
            return None

    def _target(self):
        if self.target_type == 'admin':
            return Q(is_admin=True)

        if self.target_type == 'bind':
            return Q(is_bind=True)

        if self.target_type == 'cp':
            return Q(is_cp=True)

        if self.target_type == 'domain':
            return Q(is_domain=True)

        if self.target_type == 'mail':
            return Q(is_mail=True)

        if self.target_type == 'managed':
            return Q(is_managed=True)

        if self.target_type == 'mysql':
            return Q(is_mysql=True)

        if self.target_type == 'postgresql':
            return Q(is_postgresql=True)

        if self.target_type == 'store':
            return Q(is_store=True)

        if self.target_type == 'unmanaged':
            return Q(is_unmanaged=True)

        if self.target_type == 'xmpp':
            return Q(is_xmpp=True)

    def _query(self):
        # Hardware Company
        if not self.hardware_type and self.target_type in [
            'admin',
            'bind',
            'cp',
            'mail',
            'store',
            'xmpp'
        ]:
            obj = models.Server.objects.filter(
                self._target(),
                company=self.domain.company,
                domain__related_to=self.domain,
                hardware_type='private',
                server_type='company'
            )

        # Hardware Client
        else:
            obj = models.Server.objects.filter(
                self._target(),
                company=self.domain.company,
                domain__related_to=self.domain,
                hardware_type=self.hardware_type,
                server_type='client'
            )

        return obj

    def re_use_id(self):
        query = self._query()

        if query.exists() and query.count() > 0:
            count = []

            for item in query:
                name = item.domain.name.split('.', 1)

                number = re.sub('[^0-9]', '', name[0])

                count.append(int(number))

            pre_total = self._find_missing_low_number(sorted(count))

            if pre_total is None:
                total = query.count() + 1
            else:
                total = pre_total
        else:
            total = 1

        return total


class GenerateServer:
    def __init__(self, order_id):
        self.order = order_id

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        try:
            obj = models.Order.objects.get(pk=value)
        except models.Order.DoesNotExist:
            raise ValueError('Order does not exist.')

        self._order = obj

    def bind(self):
        """
        Bind

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='private',
            target_type='bind',
            server_type='company',
            is_installed=True
        )

        if server.exists() and server.count() >= 2:
            ns_list = []

            for item in server:
                ns_list.append(item.pk)

            return random.sample(ns_list, 2)
        else:
            return 0

    def control_panel(self):
        """
        Control Panel

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='private',
            target_type='cp',
            server_type='company',
            is_installed=True
        )

        if server.exists():
            cp_list = []

            for item in server:
                cp_list.append(item.pk)

            return random.choice(cp_list)
        else:
            return 0

    def dedicated_domain(self, web_type=None):
        """
        Dedicated Domain

        :param str web_type: Web Type (apache / nginx)

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='dedicated',
            target_type='domain',
            server_type='client',
            is_installed=True,
            web_type=web_type
        )

        if server.exists():
            dedicated_web_list = []

            for item in server:
                dedicated_web_list.append(item.pk)

            return random.choice(dedicated_web_list)
        else:
            return 0

    def dedicated_mail(self):
        """
        Dedicated Mail

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='dedicated',
            target_type='mail',
            server_type='client',
            is_installed=True,
            is_mail=True
        )

        if server.exists():
            dedicated_mail_list = []

            for item in server:
                dedicated_mail_list.append(item.pk)

            return random.choice(dedicated_mail_list)
        else:
            return 0

    def dedicated_mysql(self):
        """
        Dedicated MySQL

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='dedicated',
            target_type='mysql',
            server_type='client',
            is_installed=True,
            is_mysql=True
        )

        if server.exists():
            dedicated_mysql_list = []

            for item in server:
                dedicated_mysql_list.append(item.pk)

            return random.choice(dedicated_mysql_list)
        else:
            return 0

    def dedicated_postgresql(self):
        """
        Dedicated PostgreSQL

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='dedicated',
            target_type='postgresql',
            server_type='client',
            is_installed=True,
            is_postgresql=True
        )

        if server.exists():
            dedicated_postgresql_list = []

            for item in server:
                dedicated_postgresql_list.append(item.pk)

            return random.choice(dedicated_postgresql_list)
        else:
            return 0

    def private(self, has_domain=False, has_mail=False, has_mysql=False, has_postgresql=False, web_type=None):
        """
        Private

        :param bool has_domain: Has Domain
        :param bool has_mail: Has Mail
        :param bool has_mysql: Has MySQL
        :param bool has_postgresql: Has PostgreSQL
        :param str web_type: Web Type (apache / nginx)

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='private',
            target_type='custom',
            server_type='client',
            is_installed=True,
            account=None,
            order=None,
            is_domain=has_domain,
            is_mail=has_mail,
            is_mysql=has_mysql,
            is_postgresql=has_postgresql,
            web_type=web_type
        )

        if server.exists():
            private_list = []

            for item in server:
                private_list.append(item.pk)

            return random.choice(private_list)
        else:
            return 0

    def shared(self, has_domain=False, has_mail=False, has_mysql=False, has_postgresql=False, web_type=None):
        """
        Shared

        :param bool has_domain: Has Domain
        :param bool has_mail: Has Mail
        :param bool has_mysql: Has MySQL
        :param bool has_postgresql: Has PostgreSQL
        :param str web_type: Web Type (apache / nginx)

        :return: int
        """

        server = models.Server.objects.filter(
            company_id=self.order.company_id,
            is_active=True,
            hardware_type='shared',
            target_type='custom',
            server_type='client',
            is_installed=True,
            account=None,
            order=None,
            is_domain=has_domain,
            is_mail=has_mail,
            is_mysql=has_mysql,
            is_postgresql=has_postgresql,
            web_type=web_type
        )

        if server.exists():
            shared_list = []

            for item in server:
                shared_list.append(item.pk)

            return random.choice(shared_list)
        else:
            return 0

    def prepare(self):
        """
        Prepare Servers for use in order creation.

        :return: dict
        """

        error = []

        servers = {}

        # Control Panel
        cp = self.control_panel()

        (servers.update({'cp': cp}) if cp > 0 else error.append('cp'))

        # Bind Pair
        bind = self.bind()

        (servers.update({'ns1': bind[0], 'ns2': bind[1]}) if type(bind) is list else error.append('bind'))

        # Dedicated - Domain
        domain = self.dedicated_domain(web_type=self.order.product_profile.store_product.web_type)

        (servers.update({'domain': domain}) if domain > 0 else error.append('domain'))

        # Dedicated - Mail
        mail = self.dedicated_mail()

        (servers.update({'mail': mail}) if mail > 0 else error.append('mail'))

        # Dedicated - MySQL
        mysql = self.dedicated_mysql()

        (servers.update({'mysql': mysql}) if mysql > 0 else error.append('mysql'))

        # Dedicated - PostgreSQL
        postgresql = self.dedicated_postgresql()

        (servers.update({'postgresql': postgresql}) if postgresql > 0 else error.append('postgresql'))

        # Private
        private = self.private(
            has_domain=self.order.product_profile.store_product.has_domain,
            has_mail=self.order.product_profile.store_product.has_mail,
            has_mysql=self.order.product_profile.store_product.has_mysql,
            has_postgresql=self.order.product_profile.store_product.has_postgresql,
            web_type=self.order.product_profile.store_product.web_type
        )

        (servers.update({'private': private}) if private > 0 else error.append('private'))

        # Shared
        shared = self.shared(
            has_domain=self.order.product_profile.store_product.has_domain,
            has_mail=self.order.product_profile.store_product.has_mail,
            has_mysql=self.order.product_profile.store_product.has_mysql,
            has_postgresql=self.order.product_profile.store_product.has_postgresql,
            web_type=self.order.product_profile.store_product.web_type
        )

        (servers.update({'shared': shared}) if shared > 0 else error.append('shared'))

        # Product - Domain
        if self.order.product_profile.store_product.product_type == 'domain':
            # Dedicated
            if self.order.product_profile.store_product.hardware_type == 'dedicated':
                error.remove('private')
                servers.pop('private', None)

                error.remove('shared')
                servers.pop('shared', None)

                # Domain
                if not self.order.product_profile.store_product.has_domain:
                    error.remove('domain')
                    servers.pop('domain', None)

                # Mail
                if not self.order.product_profile.store_product.has_mail:
                    error.remove('mail')
                    servers.pop('mail', None)

                # MySQL
                if not self.order.product_profile.store_product.has_mysql:
                    error.remove('mysql')
                    servers.pop('mysql', None)

                # PostgreSQL
                if not self.order.product_profile.store_product.has_postgresql:
                    error.remove('postgresql')
                    servers.pop('postgresql', None)

        # Check for any errors
        if len(error):
            return sorted(list(set(error)))

        # No errors found
        else:
            return servers
