import socket

from django.conf import settings
from django.conf.urls import include
from django.urls import path
from ipware.ip import get_client_ip
from rest_framework.authtoken import models
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.response import Response

from login import models as login_models

urlpatterns = [
    # GWHCP URLs
    path('admin/billing/payment/', include('admin.billing.payment.urls')),
    path('admin/billing/reason/', include('admin.billing.reason.urls')),
    path('admin/company/account/', include('admin.company.account.urls')),
    path('admin/company/dns/', include('admin.company.dns.urls')),
    path('admin/company/domain/', include('admin.company.domain.urls')),
    path('admin/company/mail/', include('admin.company.mail.urls')),
    path('admin/customer/account/', include('admin.customer.account.urls')),
    path('admin/customer/billing/invoice/', include('admin.customer.billing.invoice.urls')),
    path('admin/customer/billing/profile/', include('admin.customer.billing.profile.urls')),
    path('admin/customer/order/', include('admin.customer.order.urls')),
    path('admin/employee/account/', include('admin.employee.account.urls')),
    path('admin/employee/mail/', include('admin.employee.mail.urls')),
    path('admin/employee/manage/', include('admin.employee.manage.urls')),
    path('admin/hardware/client/', include('admin.hardware.client.urls')),
    path('admin/hardware/company/', include('admin.hardware.company.urls')),
    path('admin/network/pool/', include('admin.network.pool.urls')),
    path('admin/network/queue/', include('admin.network.queue.urls')),
    path('admin/setting/banned/', include('admin.setting.banned.urls')),
    path('admin/setting/email/', include('admin.setting.email.urls')),
    path('admin/store/coupon/', include('admin.store.coupon.urls')),
    path('admin/store/fraud/', include('admin.store.fraud.urls')),
    path('admin/store/product/', include('admin.store.product.urls')),
    path('admin/store/product/domain/', include('admin.store.product.domain.urls')),
    # path('admin/store/product/mail/', include('admin.store.product.mail.urls')),
    # path('admin/store/product/mysql/', include('admin.store.product.mysql.urls')),
    # path('admin/store/product/postgresql/', include('admin.store.product.postgresql.urls')),
    path('admin/store/product/price/', include('admin.store.product.price.urls')),
    # path('admin/store/product/server/', include('admin.store.product.server.urls')),
    path('client/account/', include('client.account.urls')),
    path('client/billing/invoice/', include('client.billing.invoice.urls')),
    path('client/billing/profile/', include('client.billing.profile.urls')),
    path('client/store/coupon/', include('client.store.coupon.urls')),
    path('client/store/product/', include('client.store.product.urls')),
    path('login/', include('login.urls')),
    path('worker/bind/', include('worker.bind.urls')),
    path('worker/console/', include('worker.console.urls')),
    path('worker/cron/', include('worker.cron.urls')),
    path('worker/daemon/', include('worker.daemon.urls')),
    path('worker/dovecot/', include('worker.dovecot.urls')),
    path('worker/gunicorn/', include('worker.gunicorn.urls')),
    path('worker/mail/', include('worker.mail.urls')),
    path('worker/mysql/', include('worker.mysql.urls')),
    path('worker/nginx/', include('worker.nginx.urls')),
    path('worker/php/', include('worker.php.urls')),
    path('worker/postfix/', include('worker.postfix.urls')),
    path('worker/postgresql/', include('worker.postgresql.urls')),
    path('worker/rabbitmq/', include('worker.rabbitmq.urls')),
    path('worker/system/', include('worker.system.urls')),
    path('worker/vsftpd/', include('worker.vsftpd.urls')),
    path('worker/web/', include('worker.web.urls')),

    # Rest API Login
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    # API Documentation
    path('docs/', include_docs_urls(title='Documentation'))
]

# Debug Settings
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]


# Custom Auth Token response
class CustomAuthToken(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, created = models.Token.objects.get_or_create(user=user)

        ip = get_client_ip(request)

        login_models.AccessLog.objects.create(
            account=user,
            ipaddress=ip[0],
            reverse_ipaddress=socket.getfqdn(ip[0])
        )

        return Response({
            'token': {
                'key': token.key
            }
        })


urlpatterns += [
    path('dj-rest-auth/api-token-auth/', CustomAuthToken.as_view())
]
