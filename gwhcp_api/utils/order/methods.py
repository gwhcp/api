from database.gwhcp import models


class OrderMethods(object):
    def __init__(self, data: dict):
        self.data = data

    def get_account(self):
        return models.Account(self.data['account'])

    def get_billing_profile(self):
        return models.BillingProfile(self.data['billing_profile'])

    def get_billing_invoice(self):
        return models.BillingInvoice(self.data['billing_invoice'])

    def get_store_product(self):
        return models.StoreProduct(self.data['store_product'])

    def get_store_product_price(self):
        return models.StoreProductPrice(self.data['store_product_price'])
