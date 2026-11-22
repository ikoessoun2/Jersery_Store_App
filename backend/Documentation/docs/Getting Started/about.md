## ABOUT 

### Overview


Rashid sells jerseys, sports shoes and shorts and wants a simple way for his customers to purchase from him. The best way is a web app that collates his work and allows people to purchase from him. The app should also help him organise and make delivery as an additional bonus.

### The Solution

As the developer the solution is a django app with a react frontend. 
There would be two users of the system. The public facing side would be for the customers who want to purchase and the admin side for those managing the customers and products.


### SOFTWARE DESIGN AND BUILDING STRATEGY

The developer uses the **TDD sofware development method**. The idea is to ask the problem, write the test cases and then implement the solution.


I would introduce a dedicated section called **Test Planning and Specifications**.

# **1. Problem Definition**

Before writing a test, establish the problem you are trying to solve.

For every feature or operation, document:

- What problem are we addressing?
- Under what circumstances does it occur?
- What should the system do?
- What should the system prevent?
- What conditions must be satisfied?

For example, consider product creation.

**Problem: Product Creation**

An administrator needs to create products in the store. However, the system must ensure that incomplete or invalid product information is not persisted.

**Problems to address:**

1. Products must have a valid name.
2. Products must belong to an existing category.
3. Duplicate product identifiers must not be accepted.
4. Invalid data must not reach the persistence layer.
5. Unauthorized users must not create products.

**Expected outcome:**

A valid product is successfully created and persisted. Invalid requests are rejected with appropriate errors.

# **2. Behaviour Specifications**

Translate the problem into explicit expected behaviours.

I recommend using a format similar to this:

| Scenario             | Expected behaviour |
| -------------------- | ------------------ |
| Valid product data   | Product is created |
| Missing product name | Validation fails   |
| Invalid category     | Validation fails   |
| Duplicate SKU        | Conflict is raised |
| Unauthorized request | Access is denied   |

This becomes your behavioural specification.

You can also use Given-When-Then notation:

```
Scenario: Create a product successfully

Given an authenticated administrator
And a valid product category exists
When the administrator submits valid product data
Then the product should be created
And the product should be persisted
And the API should return HTTP 201
```

# **3. Test Specifications**

Now define the actual tests you intend to write.

I would organise them according to your existing architecture.

For example:

**Product Service Tests**

| Test                                    | Expected result            |
| --------------------------------------- | -------------------------- |
| test_create_product_success             | Product is created         |
| test_create_product_invalid_category    | ResourceNotFound is raised |
| test_create_product_duplicate_sku       | ResourceConflict is raised |
| test_create_product_persistence_failure | Transaction is rolled back |

**Product API Tests**

| Test                                             | Expected result |
| ------------------------------------------------ | --------------- |
| test_create_product_returns_201                  | HTTP 201        |
| test_create_product_returns_400_for_invalid_data | HTTP 400        |
| test_create_product_requires_authentication      | HTTP 401        |
| test_create_product_rejects_unauthorized_user    | HTTP 403        |

These are illustrative cases; the exact tests should reflect your actual business rules and implementation boundaries.

# **4. Test Execution and Results**

Since you use TDD, your documentation should also track the evolution of the tests.

I would record:

- Test identifier.
- Test description.
- Initial status.
- Implementation status.
- Final result.
- Related feature or requirement.

For example:

| Test                        | Initial status | Current status |
| --------------------------- | -------------- | -------------- |
| Create product successfully | Failing        | Passing        |
| Reject invalid category     | Failing        | Passing        |
| Reject duplicate SKU        | Failing        | Passing        |
| Require authentication      | Failing        | Passing        |

You do not necessarily need to maintain this table manually. Your test runner and CI pipeline can provide execution results.

# **5. Testing Strategy**

Create a separate document explaining your overall testing approach.

For your Django backend, I would consider:

| Test category     | What it verifies                        |
| ----------------- | --------------------------------------- |
| Unit tests        | Individual functions and business logic |
| Service tests     | Business operations and orchestration   |
| Repository tests  | Data access and persistence             |
| Serializer tests  | Input validation and transformation     |
| API tests         | HTTP contracts and permissions          |
| Integration tests | Interaction between multiple components |

Also document your testing tools, fixtures, test database configuration, mocking conventions and coverage expectations.

# **6. Recommended MkDocs structure**

I would organise your testing documentation like this:

```
Testing/
│
├── overview.md
│
├── test-strategy.md
│
├── test-planning/
│   ├── problem-definitions.md
│   ├── behaviour-specifications.md
│   └── test-cases.md
│
├── test-implementation/
│   ├── unit-tests.md
│   ├── integration-tests.md
│   └── api-tests.md
│
└── test-execution/
    ├── running-tests.md
    └── test-results.md
```

# **7. One distinction I want you to appreciate**

There are three separate things happening in your TDD workflow:

Stage 1

**Problem and Behaviour Definition**

What problem are we solving, and what should happen?

Stage 2

**Test Design and Implementation**

How will we verify that the expected behaviour is satisfied?

Stage 3

**Implementation and Verification**

Build the solution, run the tests, refactor, and verify that the requirements remain satisfied.

One correction worth making: in strict TDD, you write an executable test before implementing the behaviour, rather than writing a separate document containing every test and then implementing later. Your problem and behaviour specifications can be documented beforehand, while the executable tests become the authoritative verification.

**My strongest recommendation:** Treat your problem definitions and behavioural specifications as part of requirements engineering, and your executable tests as part of the implementation. Link them together using requirement or feature identifiers.

That gives you traceability:

`Problem → Requirement → Behaviour → Test → Implementation`

This is particularly valuable when you eventually revisit a feature to extend or redesign it. You can understand not only what the code does, but also what problems it was originally intended to solve and what behaviour must not regress.