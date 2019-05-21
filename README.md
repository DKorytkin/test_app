# test_app
only for testing


## endpoints:


### user:


- *GET* `/users`
    - filters:
        - role: one of (admin, manager, user)
        - first_name
        - last_name
        - email
- *GET* `/users/{id}` 
- *POST* `/users`
    - body required fields:
        - role: one of (admin, manager, user)
        - first_name
        - last_name
        - email

- *GET* `/users/{id}/orders`
- *GET* `/users/{id}/orders/{id}`