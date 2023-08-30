from utils import models


class Invoice(object):
    def __init__(self, account: models.Account, billing_profile: models.BillingProfile,
                 product_profile: models.ProductProfile, store_product: models.StoreProduct,
                 store_product_price: models.StoreProductPrice, billing_invoice: models.BillingInvoice = None,
                 order: models.Order = None, payment_gateway: models.PaymentGateway = None,
                 reason: models.Reason = None):
        self.account = account

        self.billing_invoice = billing_invoice

        self.billing_profile = billing_profile

        self.order = order

        self.payment_gateway = payment_gateway

        self.product_profile = product_profile

        self.reason = reason

        self.store_product = store_product

        self.store_product_price = store_product_price

        self.items = list()

    def create(self):
        """
        Create billing invoice

        :return: models.BillingInvoice | dict
        """

        billing_invoice = models.BillingInvoice.objects.create(
            account=self.account,
            billing_profile=self.billing_profile,
            order=self.order,
            payment_gateway=self.payment_gateway,
            product_profile=self.product_profile,
            reason=self.reason,
            store_product=self.store_product,
            store_product_price=self.store_product_price
        )

        for item in self.items:
            models.BillingInvoiceItem.objects.create(
                amount=item['total_amount'],
                base_price=item['base_price'],
                billing_invoice=billing_invoice,
                coupon_price=item['coupon_price'],
                invoice_type=item['invoice_type'],
                setup_price=item['setup_price'],
                transaction=item['transaction'],
                transaction_type=item['transaction_type']
            )

        return billing_invoice

    def set_item(self, invoice_type: str, store_product_price: models.StoreProductPrice, coupon: models.Coupon = None,
                 transaction: dict = None, transaction_type: str = None):
        """
        Add item

        :param str invoice_type: charge | coupon | debit | refund | void
        :param models.StoreProductPrice store_product_price: Store product price object
        :param models.Coupon coupon: Coupon object
        :param dict transaction: Transaction response
        :param dict transaction_type: auth_capture | refund | void
        """

        coupon_amount = '0.00'

        if coupon is not None:
            total_amount = (store_product_price.base_price + store_product_price.setup_price) - coupon.amount

            coupon_amount = coupon.amount
        else:
            total_amount = store_product_price.base_price + store_product_price.setup_price

        self.items.append({
            'invoice_type': invoice_type,
            'base_price': store_product_price.base_price,
            'coupon_price': coupon_amount,
            'setup_price': store_product_price.setup_price,
            'total_amount': total_amount,
            'transaction': transaction,
            'transaction_type': transaction_type
        })

    def update(self):
        """
        Update billing invoice

        :return: models.BillingInvoice | dict
        """

        for item in self.items:
            models.BillingInvoiceItem.objects.create(
                amount=item['total_amount'],
                base_price=item['base_price'],
                billing_invoice=self.billing_invoice,
                invoice_type=item['invoice_type'],
                setup_price=item['setup_price'],
                transaction=item['transaction'],
                transaction_type=item['transaction_type']
            )

        return self.billing_invoice
