# Project Overview

This project is a Flask-based web application that manages a database for a food delivery service. It includes functionality for handling couriers, users, restaurants, menus, and orders. The database schema is defined in `databases/term_project.sql`, and the application uses a MySQL database.

The project is structured with a main `server.py` file that creates the Flask application, `views/restaurant_view.py`, `views/menu_view.py`, `views/courier_view.py` for defining the routes, and a `config/settings.py` file for configuration. The `raw_data` directory contains CSV files that are used to populate the database using the various `insert_*.py` scripts.

## Building and Running

### Dependencies

The project requires the following Python libraries:

*   `Flask`
*   `mysql-connector-python`

You can install these dependencies using pip:

```bash
pip install Flask mysql-connector-python
```

### Database Setup

1.  Create a MySQL database named `term_project`.
2.  Execute the `databases/term_project.sql` script to create the tables.
3.  Update the database connection settings in the `insert_*.py` files to match your MySQL configuration.

### Running the Application

1.  Populate the database by running the `insert_*.py` scripts:

    ```bash
    python insert_couriers.py
    python insert_data_orders.py
    python insert_data.py
    python insert_menu.py
    python insert_data.py # This will now include restaurant data via insert_Restaurant_from_csv
    ```

2.  Start the Flask application:

    ```bash
    python server.py
    ```

The application will be available at `http://localhost:8080`.

## Development Conventions

*   The application follows a standard Flask project structure.
*   Database queries are written in SQL and executed using the `mysql-connector-python` library.
*   The `insert_*.py` scripts are used for populating the database from CSV files.
