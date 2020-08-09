from django_celery_results.models import TaskResult

from worker.queue import models


def update(queue_status, order_id):
    """
    Cleans up the active queue when the entire Ticket ID is active

    :param QueueStatus queue_status: Queue Status Object
    :param int order_id: Order ID

    :return: None
    """

    result = models.QueueItem.objects.filter(queue_status=queue_status)

    statuses = []

    for item in result:
        statuses.append((True if item.status == 'active' else False))

    # Last item in queue is active, start the cleanup process
    if result.count() == order_id and all(statuses) is True:
        result2 = models.QueueStatus.objects.get(pk=queue_status.pk)

        # Set Queue to False
        if result2.service_id is not None:
            for key, value in result2.service_id.items():
                set_queue(key, value)

        # Remove from Celery Results
        for item in result:
            result3 = TaskResult.objects.filter(task_id=str(item.task_id))

            if result3.exists():
                result3.delete()

        # Remove Queue
        result2.delete()


def set_queue(key, value):
    """
    Updates Queue Status

    :param str key: Table Type
    :param int value: Unique ID

    :raise: ValueError

    :return: None
    """

    array = {
        'cron_id': models.CronTab,
        'ftp_id': models.FtpUser,
        'domain_id': models.Domain,
        'domain_ssl_id': models.DomainSsl,
        'list_id': models.MailList,
        'mail_id': models.Mail,
        'mysql_id': models.MysqlDatabase,
        'mysql_user_id': models.MysqlUser,
        'postgresql_id': models.PostgresqlDatabase,
        'postgresql_user_id': models.PostgresqlUser,
        'server_id': models.Server
    }

    try:
        result = array.get(key).objects.get(pk=value, in_queue=True)
    except:
        raise ValueError('Worker: Queue query was not found.')

    result.in_queue = False
    result.save()
