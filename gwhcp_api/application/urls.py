from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # GWHCP URLs
    path('account/account/', include('account.account.urls')),
    path('account/login/', include('account.login.urls')),
    path('billing/reason/', include('billing.reason.urls')),
    path('billing/payment/', include('billing.payment.urls')),
    path('company/company/', include('company.company.urls')),
    path('company/dns/', include('company.dns.urls')),
    path('company/domain/', include('company.domain.urls')),
    path('hardware/client/', include('hardware.client.urls')),
    path('hardware/company/', include('hardware.company.urls')),
    path('network/pool/', include('network.pool.urls')),
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
