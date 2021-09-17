from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # GWHCP URLs
    path('billing/payment/', include('billing.payment.urls')),
    path('billing/reason/', include('billing.reason.urls')),
    path('client/account/', include('client.account.urls')),
    path('client/billing/', include('client.billing.urls')),
    path('company/company/', include('company.company.urls')),
    path('company/dns/', include('company.dns.urls')),
    path('company/domain/', include('company.domain.urls')),
    path('company/mail/', include('company.mail.urls')),
    path('company/xmpp/', include('company.xmpp.urls')),
    path('employee/account/', include('employee.account.urls')),
    path('employee/mail/', include('employee.mail.urls')),
    path('employee/manage/', include('employee.manage.urls')),
    path('employee/xmpp/', include('employee.xmpp.urls')),
    path('hardware/client/', include('hardware.client.urls')),
    path('hardware/company/', include('hardware.company.urls')),
    path('network/pool/', include('network.pool.urls')),
    path('network/queue/', include('network.queue.urls')),
    path('setting/banned/', include('setting.banned.urls')),
    path('setting/email/', include('setting.email.urls')),
    path('store/fraud/', include('store.fraud.urls')),
    path('store/product/', include('store.product.urls')),
    path('store/product/domain/', include('store.product.domain.urls')),
    # path('store/product/mail/', include('store.product.mail.urls')),
    # path('store/product/mysql/', include('store.product.mysql.urls')),
    # path('store/product/postgresql/', include('store.product.postgresql.urls')),
    path('store/product/price/', include('store.product.price.urls')),
    # path('store/product/server/', include('store.product.server.urls')),
    path('worker/apache/', include('worker.apache.urls')),
    path('worker/awstats/', include('worker.awstats.urls')),
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
    path('worker/prosody/', include('worker.prosody.urls')),
    path('worker/rabbitmq/', include('worker.rabbitmq.urls')),
    path('worker/system/', include('worker.system.urls')),
    path('worker/vsftpd/', include('worker.vsftpd.urls')),
    path('worker/web/', include('worker.web.urls')),

    # Rest API URLs
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),

    # API Documentation
    path('docs/', include_docs_urls(title='Documentation'))
]

# Debug Settings
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
