# test_app
only for testing


## endpoints:


### user:

- *GET* `/` _health check_

- *GET* `/users` _get all users_
    - filters:
        - role: one of (admin, manager, user)
        - first_name
        - last_name
        - email

- *GET* `/users/{id}` _get user_

- *POST* `/users`
    - body required fields:
        - role: one of (admin, manager, user)
        - first_name
        - last_name
        - email

- *GET* `/users/{id}/orders` _get user all orders_

- *GET* `/users/{id}/orders/{id}` _get user order_

- *POST* `/orders` _create order for user_
    - body required fields:
        - user_id
        - product_ids

- *GET* `/products` _get all products_

- *GET* `/products/{id}` _get one product_

- *POST* `/products`
    - body required fields:
        - name
        - price
