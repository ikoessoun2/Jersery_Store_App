The main functionality of the system sits on the products.
Users
-> List products
-> Get details of a product
-> Purchase products

Admin
-> Add products
-> Remove products
-> Edit products
-> Manage products

 - Products Table
 -- Id - UUID
 -- Name - text
 -- Category - F.K
 -- Description - text
 -- Price - int
 -- Delivery period - F.K
 
 - Categories Table
 -- Id - UUID
 -- Name - text
 -- Description - text

 - Delivery Schedule Table
 -- Id - UUID
 -- Name - text
 -- Number_Of_Days_To_Deliver - int
 
 - Stock Table
 -- Id - UUID
 -- Product_Id - F.K
 -- Last_Stocked - DateTime
 -- Number_Left - int
 -- Last_Stock_Amount - int

# IMPLEMENTATION ::
1. Create the model.
2. Create repository.
- get_all_products() -> objects
- get_product_by_id() -> object
- create_product() -> object
- edit_product() -> object
- delete_product() -> none [soft delete]
- create_category() -> object
- delete_category() -> none [soft delete]
-
3. Create the service.
- create_product() -> object
- edit_product() -> object
- delete_product() -> none [soft delete]
- create_category() -> object
- delete_category() -> none [soft delete]

4. Create the serializer

4. Create the view
5. Create the url

# Jersey Store --- Catalog Database Schema

## 1. Scope

This document describes the database schema for the **catalog app** of
the Jersey Store.

The catalog stores information about the products offered for sale and
the variants customers can select. It does **not** manage physical stock
quantities or stock movements. Inventory management will be handled
separately.

## 2. Design overview

The catalog contains five models:

1.  `Category`
2.  `Product`
3.  `Size`
4.  `ProductVariant`
5.  `ProductImage`

### Entity relationship diagram

``` mermaid
erDiagram
    CATEGORY ||--o{ PRODUCT : classifies
    PRODUCT ||--o{ PRODUCT_VARIANT : offers
    SIZE ||--o{ PRODUCT_VARIANT : defines
    PRODUCT ||--o{ PRODUCT_IMAGE : displays

    CATEGORY {
        int id PK
        string name
        string description
    }

    PRODUCT {
        int id PK
        int category_id FK
        string name
        text description
        decimal price
        datetime created_at
        datetime updated_at
    }

    SIZE {
        int id PK
        string name
    }

    PRODUCT_VARIANT {
        int id PK
        int product_id FK
        int size_id FK
        string sku
    }

    PRODUCT_IMAGE {
        int id PK
        int product_id FK
        string image
        boolean is_primary
        string alt_text
    }
```

## 3. Model definitions

### 3.1 Category

Represents a classification used to group products.

  Field           Purpose
  --------------- -------------------------------
  `id`            Primary key
  `name`          Category name
  `description`   Optional category description

Examples: Home Jerseys, Away Jerseys, Retro Jerseys.

A category can contain many products. Each product belongs to one
category in this initial design.

### 3.2 Product

Represents the main catalog item.

  Field           Purpose
  --------------- -------------------------------------------
  `id`            Primary key
  `category`      Foreign key to `Category`
  `name`          Product name
  `description`   Product description
  `price`         Base selling price
  `created_at`    Date and time the record was created
  `updated_at`    Date and time the record was last updated

**Pricing assumption:** All sizes of a product have the same price. The
price is therefore stored on `Product`, not `ProductVariant`. If
variants later have different prices, a variant-level price or price
override can be introduced.

### 3.3 Size

Stores the standard size options available in the store.

  Field    Purpose
  -------- ----------------------------------------
  `id`     Primary key
  `name`   Size label, such as S, M, L, XL or XXL

Size records can be reused across many products.

### 3.4 ProductVariant

Represents a specific purchasable configuration of a product. In the
initial design, size is the only variation attribute.

  Field       Purpose
  ----------- ------------------------------------------
  `id`        Primary key
  `product`   Foreign key to `Product`
  `size`      Foreign key to `Size`
  `sku`       Optional unique stock-keeping identifier

A product can have multiple variants, one for each size offered.

**Constraint:** The combination of `product` and `size` must be unique.
This prevents the same product from having duplicate variants for the
same size.

For example, a Manchester United Home Jersey may have Small, Medium and
Large variants. It must not have two separate Small variants.

### 3.5 ProductImage

Stores image references associated with a product.

  Field          Purpose
  -------------- ----------------------------------------------
  `id`           Primary key
  `product`      Foreign key to `Product`
  `image`        Image file reference/path
  `is_primary`   Indicates the main product image
  `alt_text`     Optional accessible description of the image

A product can have multiple images. The actual image files are stored
using Django's media storage; the database stores their references.

Consider enforcing a rule that each product has at most one primary
image. This can be implemented with a conditional database constraint
where supported, or validated in application logic.

## 4. Catalog and inventory are separate

The catalog answers:

-   What products does the store offer?
-   What category does each product belong to?
-   What sizes or variants can customers select?
-   What is the product's description and price?
-   Which images represent the product?

The inventory system answers:

-   How many units of each variant are physically available?
-   Where is the stock held?
-   How does stock change after purchases, returns or adjustments?

For example:

  Product              Variant   Catalog record     Inventory quantity
  -------------------- --------- ---------------- --------------------
  United Home Jersey   Small     Exists                              5
  United Home Jersey   Medium    Exists                             12
  United Home Jersey   Large     Exists                              0

The catalog can list a variant even when its inventory quantity is zero.
Whether a customer can purchase it is determined by the interaction
between the catalog and inventory/business rules.

The catalog's `ProductVariant` model should therefore **not** contain a
stock quantity field.

## 5. Initial design assumptions and boundaries

The first version deliberately keeps the design simple:

-   A product belongs to one category.
-   A product can have multiple sizes.
-   Size is the only variant attribute initially.
-   All variants of a product share the product's price.
-   A product can have multiple images.
-   Inventory quantities and stock movements are outside the catalog
    app.

If the store later needs colour, fit, edition or other selectable
attributes, the variant design can be extended to represent combinations
of attributes. For example, Small/Red and Medium/Blue would be distinct
variants. That flexibility is not required for the initial size-only
implementation.

## 6. Suggested Django app structure

``` text
apps/
└── catalog/
    ├── models/
    │   ├── __init__.py
    │   ├── category.py
    │   ├── product.py
    │   ├── size.py
    │   ├── product_variant.py
    │   └── product_image.py
    ├── admin.py
    ├── apps.py
    └── ...
```

If models are split across files, import them in `models/__init__.py` so
Django can discover them:

``` python
from .category import Category
from .product import Product
from .size import Size
from .product_variant import ProductVariant
from .product_image import ProductImage
```

## 7. Implementation checklist

-   [ ] Create the `catalog` Django app.
-   [ ] Define the five models.
-   [ ] Add foreign-key relationships.
-   [ ] Add a uniqueness constraint to `(product, size)` on
    `ProductVariant`.
-   [ ] Configure image uploads and media storage.
-   [ ] Decide how to enforce one primary image per product.
-   [ ] Register the models in Django Admin.
-   [ ] Create and apply migrations.
-   [ ] Test product creation, variant creation and duplicate-variant
    rejection.

------------------------------------------------------------------------

**Design status:** Initial catalog schema proposal. Inventory
management, order processing and payment models are intentionally
outside this document.
