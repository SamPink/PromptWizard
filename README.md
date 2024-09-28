# PromptWizard

**PromptWizard** is a simple and efficient web application built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. It allows users to create, read, update, and delete prompts through a user-friendly interface. The backend manages the data using a SQLite database, while the frontend provides an intuitive interface for interacting with the prompts.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Using Docker](#using-docker)
  - [Without Docker](#without-docker)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Create Prompts:** Add new prompts with a name, content, and category.
- **Read Prompts:** View a list of all existing prompts, filtered by category.
- **Update Prompts:** Modify the name, content, or category of existing prompts.
- **Delete Prompts:** Remove unwanted prompts.
- **Categories:** Organize prompts into categories for better management.
- **Search:** Quickly find prompts using the search functionality.
- **Responsive Frontend:** User-friendly interface built with Tailwind CSS and Axios for seamless interactions.

## Tech Stack

- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast web framework for building APIs with Python.
  - [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM for Python.
  - [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management using Python type annotations.
- **Frontend:**
  - [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework.
  - [Axios](https://axios-http.com/) - Promise-based HTTP client for the browser and Node.js.
- **Containerization:**
  - [Docker](https://www.docker.com/) - Platform for developing, shipping, and running applications in containers.

## Installation

### Prerequisites

- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) (for Docker installation)
- [Python 3.7+](https://www.python.org/downloads/) (for non-Docker installation)
- [pip](https://pip.pypa.io/en/stable/installation/) (for non-Docker installation)

### Steps

1. **Clone the Repository**

   Open a command prompt and run:

   ```cmd
   git clone https://github.com/SamPink/promptwizard.git
   cd promptwizard
   ```

2. **Choose Installation Method**

   Follow either the [Docker](#using-docker) or [non-Docker](#without-docker) instructions below.

## Running the Application

### Using Docker

1. **Install Docker Desktop for Windows**

   If you haven't already, download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop). Follow the installation instructions provided on the Docker website.

2. **Start Docker Desktop**

   Launch Docker Desktop and wait for it to fully start. You should see the Docker icon in your system tray when it's ready.

3. **Open a Command Prompt**

   Press `Win + R`, type `cmd`, and press Enter to open a command prompt.

4. **Navigate to the Project Directory**

   Use the `cd` command to navigate to your project directory. For example:

   ```cmd
   cd C:\path\to\promptwizard
   ```

5. **Build and Start the Docker Container**

   Run the following command:

   ```cmd
   docker-compose up --build
   ```

   This command will build the Docker image and start the container. You should see output indicating that the server is running.

6. **Access the Application**

   Open your web browser and navigate to [http://localhost:8300](http://localhost:8300) to view the application.

7. **Stop the Container**

   When you're done using the application, go back to the command prompt where docker-compose is running and press `Ctrl + C`. Then run:

   ```cmd
   docker-compose down
   ```

   This will stop and remove the containers.

### Without Docker

1. **Create a Virtual Environment**

   Open a command prompt in your project directory and run:

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```cmd
   pip install -r requirements.txt
   ```

3. **Start the Backend Server**

   In the project directory, run:

   ```cmd
   uvicorn backend:app --host 0.0.0.0 --port 8300 --reload
   ```

4. **Access the Application**

   Open your browser and navigate to [http://localhost:8300](http://localhost:8300) to view the frontend.

## API Documentation

FastAPI provides interactive API documentation. Access it at [http://localhost:8300/docs](http://localhost:8300/docs).

## API Endpoints

### Base URL

```
http://localhost:8300/api
```

### Endpoints

- **Get All Categories**

  - **URL:** `/categories`
  - **Method:** `GET`
  - **Description:** Retrieves a list of all categories.
  - **Response:** JSON array of category objects.

- **Create a New Category**

  - **URL:** `/categories`
  - **Method:** `POST`
  - **Description:** Creates a new category.
  - **Request Body:**

    ```json
    {
      "name": "Category Name"
    }
    ```

  - **Response:** JSON object of the created category.

- **Get All Prompts**

  - **URL:** `/prompts`
  - **Method:** `GET`
  - **Query Parameters:**
    - `category_id` (optional): Filter prompts by category ID.
  - **Description:** Retrieves a list of all prompts, optionally filtered by category.
  - **Response:** JSON array of prompt objects.

- **Create a New Prompt**

  - **URL:** `/prompts`
  - **Method:** `POST`
  - **Description:** Creates a new prompt.
  - **Request Body:**

    ```json
    {
      "name": "Prompt Name",
      "contents": "Prompt contents...",
      "category_id": 1
    }
    ```

  - **Response:** JSON object of the created prompt.

- **Update an Existing Prompt**

  - **URL:** `/prompts/{prompt_id}`
  - **Method:** `PUT`
  - **Description:** Updates the specified prompt.
  - **Path Parameters:**
    - `prompt_id` (integer): ID of the prompt to update.
  - **Request Body:**

    ```json
    {
      "name": "Updated Name",
      "contents": "Updated contents...",
      "category_id": 2
    }
    ```

  - **Response:** JSON object of the updated prompt.

- **Delete a Prompt**

  - **URL:** `/prompts/{prompt_id}`
  - **Method:** `DELETE`
  - **Description:** Deletes the specified prompt.
  - **Path Parameters:**
    - `prompt_id` (integer): ID of the prompt to delete.
  - **Response:** HTTP 204 No Content.

## Frontend

The frontend is a single-page application built with HTML, JavaScript, and Tailwind CSS. It interacts with the backend API using Axios for HTTP requests. The main features include:

- **Category Management:** Create and view categories.
- **Prompt Management:** Create, read, update, and delete prompts within categories.
- **Search Functionality:** Search for prompts across all categories.
- **Responsive Design:** Works well on both desktop and mobile devices.

## Project Structure

```
.
├── backend.py          # FastAPI backend
├── index.html          # Frontend HTML file
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration file
├── docker-compose.yml  # Docker Compose configuration
└── prompts.db          # SQLite database (auto-generated)
```

## Running Tests

PromptWizard includes a set of console tests that can be run directly in the browser's developer tools. To run these tests:

1. Ensure the application is running (either using Docker or without Docker, as described in the [Running the Application](#running-the-application) section).
2. Open your web browser and navigate to [http://localhost:8300](http://localhost:8300).
3. Open the browser's developer tools:
   - For Chrome or Edge: Press F12 or right-click and select "Inspect"
   - For Firefox: Press F12 or right-click and select "Inspect Element"
4. Go to the "Console" tab in the developer tools.
5. In the console, type the following command and press Enter:
   ```javascript
   runTests();
   ```

This will execute a series of tests that create categories, prompts, and perform various operations to verify the functionality of the application. The test results will be displayed in the console.

### Test Cases

The console tests cover the following scenarios:

1. Creating a new category
2. Creating a prompt and assigning it to the category
3. Creating a second prompt and assigning it to the same category
4. Deleting the second prompt
5. Deleting the category with the first prompt still in it
6. Creating another category and deleting it

These tests help ensure that the core functionality of PromptWizard is working as expected.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note:** This README provides instructions for both Docker and non-Docker setups on Windows. Depending on your project's complexity and requirements, you might want to add more sections such as **Testing**, **Deployment**, **Environment Variables**, etc.
