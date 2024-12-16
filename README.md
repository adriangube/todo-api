
# To-Do API with FastAPI

This is a simple **To-Do API** built with **FastAPI** to practice the fundamentals of building APIs in Python. The project uses **Poetry** as the package manager, as per the project requirements. It includes basic CRUD operations for managing a to-do list and is a great starting point for learning FastAPI and Python's web development capabilities.

## Project Overview

- **FastAPI** is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- This project is designed to practice:
  - Creating APIs with FastAPI.
  - Using **Poetry** as a package manager.
  - Understanding fundamental Python concepts, such as routing, request handling, and dependency injection.

## Technologies Used

- **FastAPI** – For creating the API.
- **Poetry** – For managing dependencies and packaging.
- **pytest** – For testing the application.
- **Uvicorn** – ASGI server to run the FastAPI app.



## Installation and Setup

Follow these steps to get the project up and running:

### **1. Install Poetry**
If you don't have Poetry installed, you can install it by following the official documentation: [Poetry Installation Guide](https://python-poetry.org/docs/#installation).

Alternatively, you can install it directly via the terminal:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### **2. Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/adriangube/todo-fastapi.git
cd todo-fastapi
```

### **3. Install Dependencies**
Use Poetry to install the project dependencies:
```bash
poetry install
```

This will create a virtual environment and install the necessary dependencies listed in the `pyproject.toml` file.

### **4. Run the Application**
To run the FastAPI app with Uvicorn, use the following command:
```bash
poetry run dev
```

This will start the development server on `http://127.0.0.1:8000`. You can view the API documentation at `http://127.0.0.1:8000/docs`.


### **4.1 Run the application as production (without reload)**
To run the FastAPI app with Uvicorn, use the following command:
```bash
poetry run prod
```

This will start the production server on `http://127.0.0.1:8000`. You can view the API documentation at `http://127.0.0.1:8000/docs`.

### **5. Running Tests**
To run the tests with **pytest**, use this command:
```bash
poetry run pytest
```

This will execute the tests located in the `tests/` directory.

---

## API Endpoints

Here are the available API endpoints for the To-Do list:

- **GET /todos** – Retrieve a list of all to-do items.
- **POST /todos** – Create a new to-do item.
- **GET /todos/{id}** – Retrieve a specific to-do item by ID.
- **PUT /todos/{id}** – Update a specific to-do item by ID.
- **DELETE /todos/{id}** – Delete a specific to-do item by ID.

All responses are in JSON format.

---

## Testing

The project includes basic tests using **pytest**. To add or modify tests, edit the files in the `tests/` directory. The tests cover basic CRUD operations and the routes defined in `main.py`.

To run the tests, simply execute:
```bash
poetry run pytest
```

---
