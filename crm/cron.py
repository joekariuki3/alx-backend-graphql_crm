from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """
    logs (appends) a message in the format DD/MM/YYYY-HH:MM:SS CRM is alive to/tmp/crm_heartbeat_log.txt.
    also queries the GraphQL hello field to verify the endpoint is responsive.
    """
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{datetime.now()}: CRM is alive.\n")

    # query hello
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
        """
        query {
        hello
        }"""
    )
    result = client.execute(query)
    assert result["hello"] == "Hello stranger"