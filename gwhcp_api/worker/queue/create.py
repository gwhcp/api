from worker.queue import models


class CreateQueue:
    def __init__(self, account_id=None, product_profile_id=None, order_id=None, service_id=None):
        """
        Create the Queue Status which will later be used for each item in the queue

        :param None|int account_id: Account ID
        :param None|int product_profile_id: Product Profile ID
        :param None|int order_id: Order ID
        :param None|dict service_id: Service ID's which need to be updated after the queue finishes successfully
        """

        self.queue_status = models.QueueStatus.objects.create(
            account_id=account_id,
            product_profile_id=product_profile_id,
            order_id=order_id,
            service_id=service_id
        )

        self.order_id = 0

    def item(self, kwargs=None):
        """
        Queue Items

        :param None|dict kwargs: Key Word Arguments

        :return: None
        """

        # Increase Order ID
        self.order_id += 1

        # Create Queue Item
        models.QueueItem.objects.create(
            queue_status=self.queue_status,
            order_id=self.order_id,
            ipaddress=kwargs['ipaddress'],
            name=kwargs['name'],
            args=kwargs.get('args')
        )
