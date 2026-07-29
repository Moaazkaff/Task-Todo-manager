                +----------------+
                |     Users      |
                +----------------+
                | user_id (PK)   |
                | name           |
                | email          |
                | password_hash  |
                | created_at     |
                +----------------+
                   |           \
                 1 |            \ 1
                   |             \
                   | M            \ M
        +----------------+    +----------------+
        |   Categories   |    |     Tasks      |
        +----------------+    +----------------+
        | category_id PK |    | task_id PK     |
        | user_id FK     |    | user_id FK     |
        | name           |    | category_id FK |
        | color          |    | title          |
        +----------------+    | description    |
                              | priority       |
                              | status         |
                              | deadline       |
                              | created_at     |
                              | updated_at     |
                              +----------------+
                              