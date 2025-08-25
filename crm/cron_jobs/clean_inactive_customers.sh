#!/bin/bash
# script runs a command using python manage.py to delete customers with no orders since a year ago
# logs the number of detected customers to /tmp/customer_cleanup_log.txt with a timestamp

python manage.py shell <<EOF
from crm.models import Customer, Order
from datetime import timedelta, datetime
from django.utils import timezone


def remove_customer_with_no_order():
    """
    Remove customers who have not placed any orders in the last 12 months.
    """
    twelve_months_ago = timezone.now() - timedelta(days=365)

    customers_with_orders_in_last_12_months = Order.objects.filter(
        order_date__lt=twelve_months_ago
    ).values_list("customer", flat=True)

    customers_to_remove = Customer.objects.exclude(
        id__in=customers_with_orders_in_last_12_months
    )
    customers_to_remove_count = customers_to_remove.count()

    for customer in customers_to_remove:
        customer.delete()

    # Log the number of customers removed to /tmp/customer_cleanup_log.txt with a timestamp.
    with open("/tmp/customer_cleanup_log.txt", "a") as log_file:
        log_file.write(
            f"{datetime.now()}: Removed {customers_to_remove_count} customers with no orders in the last 12 months.\n"
        )



    return customers_to_remove_count


remove_customer_with_no_order()

EOF