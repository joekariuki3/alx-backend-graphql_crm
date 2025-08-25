#!/bin/bash
# script runs a command using python manage.py to delete customers with no orders since a year ago
# logs the number of detected customers to /tmp/customer_cleanup_log.txt with a timestamp

python manage.py shell < crm/cron_jobs/scripts/remove_customer_with_no_order.py