from django.db.models.signals import post_save
from django.dispatch import receiver


from robots.models import Robot
from robots import tasks
from orders.models import Order


@receiver(post_save, sender=Robot)
def notify_customer(sender, instance: Robot, created, **kwargs):
    """
    Send email to customers if the ordered robot appears.

    Check if created robot is new one and if someone ordered it before.
    Then send emails to that customers.
    """
    serial = instance.serial
    serial_count = Robot.objects.filter(serial=serial).count()
    if created and serial_count == 1:
        waiting_orders = Order.objects \
            .filter(robot_serial=instance.serial) \
            .select_related("customer")

        for order in waiting_orders:
            tasks.send_notification_to_customers(
                order.customer.email,
                instance.serial,
                instance.model,
                instance.version,
            )

