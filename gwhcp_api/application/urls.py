from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # GWHCP URLs
    path('admin/billing/payment/', include('admin.billing.payment.urls')),
    path('admin/billing/reason/', include('admin.billing.reason.urls')),
    path('admin/company/company/', include('admin.company.company.urls')),
    path('admin/company/dns/', include('admin.company.dns.urls')),
    path('admin/company/domain/', include('admin.company.domain.urls')),
    path('admin/company/mail/', include('admin.company.mail.urls')),
    path('admin/company/xmpp/', include('admin.company.xmpp.urls')),
    path('admin/employee/account/', include('admin.employee.account.urls')),
    path('admin/employee/mail/', include('admin.employee.mail.urls')),
    path('admin/employee/manage/', include('admin.employee.manage.urls')),
    path('admin/employee/xmpp/', include('admin.employee.xmpp.urls')),
    path('admin/hardware/client/', include('admin.hardware.client.urls')),
    path('admin/hardware/company/', include('admin.hardware.company.urls')),
    path('admin/network/pool/', include('admin.network.pool.urls')),
    path('admin/network/queue/', include('admin.network.queue.urls')),
    path('admin/setting/banned/', include('admin.setting.banned.urls')),
    path('admin/setting/email/', include('admin.setting.email.urls')),
    path('admin/store/fraud/', include('admin.store.fraud.urls')),
    path('admin/store/product/', include('admin.store.product.urls')),
    path('admin/store/product/domain/', include('admin.store.product.domain.urls')),
    # path('admin/store/product/mail/', include('admin.store.product.mail.urls')),
    # path('admin/store/product/mysql/', include('admin.store.product.mysql.urls')),
    # path('admin/store/product/postgresql/', include('admin.store.product.postgresql.urls')),
    path('admin/store/product/price/', include('admin.store.product.price.urls')),
    # path('admin/store/product/server/', include('admin.store.product.server.urls')),
    path('client/account/', include('client.account.urls')),
    path('client/billing/', include('client.billing.urls')),
    path('client/store/', include('client.store.urls')),
    path('login/', include('login.urls')),
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
