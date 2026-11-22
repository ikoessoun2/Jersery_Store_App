
## Introduction

This is a backend meant to serve the functionality of a store. In the store there are three users; Administrator(ADMIN), User(USER) and Guest(GUEST). The administrator is responsible for managing the store and items within it. The user is assumed to be a regular customer who wants to frequent the store and the guest is assumed to be making one time stop at the store so the application will not store details about the Guest. 


**The Developer has come to the conclusion that the below activities are in scope of the behavior of the application.**
1. ADMIN
[] Admin should be able to manage products that others will buy.(Create, Update, Read, Delete)
[] Admin should be able to manage tickets that arrive from orders placed. (Read, Update).
[] Admin should recieve notifications when orders are placed 
[] Admin should recieve notifications when a new user registers.

2. USER
[] User should be able to place order from inventory. (Read)
[] User should be able to create a cart and manage cart. (Create, Read, Update, Delete)
[] User should be able to recieve notifications when they place orders.
[] User should be able to recieve notifications when their orders have been delivered successfully.

3. GUEST
[] Guest should be able to place order from inventory but would go the extra mile of filling essential details needed for delivery. (read)
[] Guest should be able to recieve notifications when they place orders.
[] Guest should be able to recieve notifications when their orders have been delivered successfully.

4. SYSTEM
[] system should be able to create tickets when orders are placed.
[] system should be able to manage inventory when orders are placed.
[] system should be able to notify users, admins, guests when orders are delivered and created.
[] system should be able to autofill users details on order form when they create orders.
[] system should be able to log essential business actions that mutate db.
[] system should be able to log errors for up to two days.

**The Developer has concluded that the following are out of scope.**
1. Payments.
2. Caching.
3. Shipping tracking.



**Authentication**
- Use JWT token authentication.
- use cookies.

**Database**
- PostgreSql

**Interface**
- React (Typescript)
- Vite

