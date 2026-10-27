# Toy Domain Model — Order Management (Worked Example Fixture)

**Purpose**: Minimal domain-model fixture used solely to validate the UI Model schema in T03. Not a real project's domain model — do not treat this as authoritative for any actual EDPS project.

## Domain Entities

### Customer
- `customer_id` (identifier)
- `name` (string)
- `email` (string)

### Order
- `order_id` (identifier)
- `order_date` (date)
- `status` (enumeration: pending, shipped, delivered, cancelled)
- `customer_ref` (reference → Customer)

### LineItem
- `line_item_id` (identifier)
- `order_ref` (reference → Order)
- `product_ref` (reference → Product)
- `quantity` (integer)
- `unit_price` (decimal)

### Product
- `product_id` (identifier)
- `name` (string)
- `price` (decimal)

## Domain Class Diagram

```mermaid
classDiagram
    class Customer {
        +customer_id: String
        +name: String
        +email: String
    }
    class Order {
        +order_id: String
        +order_date: Date
        +status: String
        +customer_ref: Customer
    }
    class LineItem {
        +line_item_id: String
        +order_ref: Order
        +product_ref: Product
        +quantity: Integer
        +unit_price: Decimal
    }
    class Product {
        +product_id: String
        +name: String
        +price: Decimal
    }

    Customer "1" --> "many" Order : places
    Order "1" --> "many" LineItem : contains
    Product "1" --> "many" LineItem : referenced by
```
