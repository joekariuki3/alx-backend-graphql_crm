from . import celery_app
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

graph_ql_endpoint = "http://localhost:8000/graphql"

@celery_app.task
def generate_crm_report():
    """
    Celery task that uses GraphQL to fetch:
      - total number of customers
      - total number of orders
      - total revenue (sum of product prices across all orders)
    Then logs the report to /tmp/crm_report_log.txt with a timestamp.
    """

    log_file = "/tmp/crm_report_log.txt"
    open_file_mode = "a"
    transport = RequestsHTTPTransport(url=graph_ql_endpoint)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
        """
        query {
            customers
            orders {
                products
            }
        }
        """
    )

    result = client.execute(query)
    total_customers = len(result["customers"])
    orders = result["orders"]
    total_revenue = 0
    for order in orders:
        for product in order["products"]:
            total_revenue += product["price"]

    total_revenue = round(total_revenue, 2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"{timestamp} Report: {total_customers} customers, {len(orders)} orders, {total_revenue} revenue."
    with open(log_file, open_file_mode) as f:
        f.write(f"{report}\n")
