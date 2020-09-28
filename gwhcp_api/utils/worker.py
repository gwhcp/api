from amqp import connection
from django.conf import settings


def check_celery_consumer(ip):
    """
    Checks how many Celery consumers are attached to RabbitMQ

    :param str ip: IP Address

    :return: int
    """

    conn = connection.Connection(
        host=settings.BROKER_HOST,
        userid=settings.BROKER_USER,
        password=settings.BROKER_PASSWORD,
        virtual_host=settings.BROKER_VHOST,
        insist=False
    )

    conn.connect()

    chan = conn.channel()

    consumer = chan.queue_declare(
        queue=f"{ip}",
        passive=True
    )

    return consumer.consumer_count


def error_to_human_readable(errors):
    """
    DRF exceptions to human readable

    :param dict errors: Errors

    :return: str
    """

    error = str()

    for item in errors.items():
        error += f"{item[1][0]}\n"

    return error
