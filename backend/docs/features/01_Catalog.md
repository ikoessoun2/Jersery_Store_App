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
