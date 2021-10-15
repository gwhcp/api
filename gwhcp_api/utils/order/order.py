from datetime import date
from datetime import timedelta

from utils import models
from utils.invoice import Invoice
from utils.order import methods


class Order(methods.OrderMethods):
    def create(self):
        if self.get_store_product().product_type == 'domain':
            return self.create_domain()

        return self.data

    def create_domain(self):
        account = self.get_account()

        billing_profile = self.get_billing_profile()

        store_product = self.get_store_product()

        store_product_price = self.get_store_product_price()

        date_to = date.today() + timedelta(days=store_product_price.billing_cycle)

        product_profile = models.ProductProfile.objects.create(
            account=account,
            billing_invoice=None,
            billing_profile=billing_profile,
            store_product=store_product,
            store_product_price=store_product_price,
            date_to=date_to,
            date_paid_to=date_to,
            bandwidth=store_product.bandwidth,
            cron_tab=store_product.cron_tab,
            diskspace=store_product.diskspace,
            domain=store_product.domain,
            ftp_user=store_product.ftp_user,
            has_cron=store_product.has_cron,
            has_domain=store_product.has_domain,
            has_mail=store_product.has_mail,
            has_mysql=store_product.has_mysql,
            has_postgresql=store_product.has_postgresql,
            ipaddress=store_product.ipaddress,
            ipaddress_type=store_product.ipaddress_type,
            mail_account=store_product.mail_account,
            mail_list=store_product.mail_list,
            mysql_database=store_product.mysql_database,
            mysql_user=store_product.mysql_user,
            postgresql_database=store_product.postgresql_database,
            postgresql_user=store_product.postgresql_user,
            sub_domain=store_product.sub_domain,
            web_type=store_product.web_type,
            mail=None,
            mysql=None,
            ns=None,
            postgresql=None,
            web=None
        )

        invoice = Invoice(account=account, billing_profile=billing_profile, product_profile=product_profile,
                          store_product=store_product, store_product_price=store_product_price)
        invoice.set_item('debit', store_product_price)

        invoice_object = invoice.create()

        order_object = models.Order.objects.create(
            account=account,
            billing_invoice=invoice_object,
            company=account.company,
            product_profile=product_profile,
            status='new'
        )

        invoice_object.order = order_object
        invoice_object.save(update_fields=['order'])

        product_profile.billing_invoice = invoice_object
        product_profile.save(update_fields=['billing_invoice'])
