# ALX Backend GraphQL CRM

A lightweight CRM backend built with Django and Graphene-Django that exposes a GraphQL API to manage customers, products and orders.

## Key features

- GraphQL API (GraphiQL enabled) at `/graphql/`
- Simple models: Customer, Product, Order
- Create single / bulk customers, create products and orders via mutations
- Filtering and Relay connections via `graphene-django` and `django-filter`

## Requirements

- Python 3.10+
- Django (5.x compatible)
- graphene-django
- django-filter

The project includes a `pyproject.toml` with declared dependencies for `graphene-django` and `django-filter`.

## Quick start

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install the project dependencies. If you use the provided `pyproject.toml` you can install the package in editable mode:

```bash
pip install -e .
```

If you prefer a requirements file but none exists, you can install the main dependencies directly:

```bash
pip install django graphene-django django-filter
```

3. Apply migrations and create a superuser (optional):

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run the development server:

```bash
python manage.py runserver
```

5. Open the GraphiQL interface at:

```
http://localhost:8000/graphql/
```

The Django admin is available at `/admin/`.

## GraphQL schema overview & examples

Top-level queries exposed by the schema:

- `customers`, `products`, `orders` — return simple lists
- `allCustomers`, `allProducts`, `allOrders` — Relay connections with filtering

Example queries:

List all customers:

```graphql
query {
  customers {
    id
    name
    email
    phone
    createdAt
  }
}
```

Using the Relay connection with filters:

```graphql
query {
  allCustomers(name_Icontains: "john") {
    edges {
      node {
        id
        name
        email
      }
    }
  }
}
```

Create a single customer (mutation field is `createCustomer`):

```graphql
mutation {
  createCustomer(
    name: "Alice Example"
    email: "alice@example.com"
    phone: "+1234567890"
  ) {
    success
    message
    customer {
      id
      name
      email
    }
  }
}
```

Bulk create customers (field `bulkCreateCustomers`):

```graphql
mutation {
  bulkCreateCustomers(
    customers: [
      { name: "Bob", email: "bob@example.com", phone: "+15551234567" }
      { name: "Carol", email: "carol@example.com" }
    ]
  ) {
    newCustomers {
      id
      name
      email
    }
    errors
  }
}
```

Create a product:

```graphql
mutation {
  createProduct(name: "T-shirt", price: 19.99, stock: 10) {
    success
    message
    product {
      id
      name
      price
      stock
    }
  }
}
```

Create an order (pass numeric DB IDs for `customer` and `products`):

```graphql
mutation {
  createOrder(customer: 1, products: [1, 2]) {
    success
    message
    order {
      id
      orderDate
      customer {
        id
        name
      }
      products {
        id
        name
      }
    }
  }
}
```

Note: Mutations in the code are declared in Python as `create_customer`, `bulk_create_customers`, `create_product`, and `create_order`, but the GraphQL field names are exposed in camelCase (for example `createCustomer`).

## Project structure (high level)

- `alx_backend_graphql/` — Django project settings and `urls.py` (GraphQL endpoint wired at `/graphql/`)
- `crm/` — app with models, filters, GraphQL schema and tests

## Contributing

Suggestions, bug reports and PRs are welcome. Keep changes small and include tests when you add or change behavior.
