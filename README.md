# PromptWizard

**PromptWizard** is a simple and efficient web application built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. It allows users to create, read, update, and delete prompts through a user-friendly interface. The backend manages the data using a SQLite database, while the frontend provides an intuitive interface for interacting with the prompts.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Create Prompts:** Add new prompts with a name and content.
- **Read Prompts:** View a list of all existing prompts.
- **Update Prompts:** Modify the name or content of existing prompts.
- **Delete Prompts:** Remove unwanted prompts.
- **Responsive Frontend:** User-friendly interface built with Tailwind CSS and Axios for seamless interactions.

## Tech Stack

- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast web framework for building APIs with Python.
  - [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM for Python.
  - [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management using Python type annotations.
  
- **Frontend:**
  - [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework.

## Installation

### Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SamPink/promptwizard.git
   cd promptwizard
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt`, you can install the necessary packages directly:

   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

## Running the Application

1. **Start the Backend Server**

   Navigate to the project directory and run:

   ```bash
   uvicorn backend:app --host 0.0.0.0 --port 8300 --reload
   ```

   - **`backend`** refers to the `backend.py` file.
   - **`app`** is the FastAPI instance.
   - **`--reload`** enables auto-reloading on code changes (useful during development).

2. **Access the Application**

   Open your browser and navigate to [http://localhost:8300](http://localhost:8300) to view the frontend.

3. **API Documentation**

   FastAPI provides interactive API documentation. Access it at [http://localhost:8300/docs](http://localhost:8300/docs).

## API Endpoints

### Base URL

```
http://localhost:8300
```

### Endpoints

- **Get All Prompts**

  - **URL:** `/api/prompts`
  - **Method:** `GET`
  - **Description:** Retrieves a list of all prompts.
  - **Response:** JSON array of prompt objects.

- **Create a New Prompt**

  - **URL:** `/api/prompts`
  - **Method:** `POST`
  - **Description:** Creates a new prompt.
  - **Request Body:**

    ```json
    {
      "name": "Prompt Name",
      "contents": "Prompt contents..."
    }
    ```

  - **Response:** JSON object of the created prompt.

- **Update an Existing Prompt**

  - **URL:** `/api/prompts/{prompt_id}`
  - **Method:** `PUT`
  - **Description:** Updates the specified prompt.
  - **Path Parameters:**
    - `prompt_id` (integer): ID of the prompt to update.
  - **Request Body:**

    ```json
    {
      "name": "Updated Name",
      "contents": "Updated contents..."
    }
    ```

  - **Response:** JSON object of the updated prompt.

- **Delete a Prompt**

  - **URL:** `/api/prompts/{prompt_id}`
  - **Method:** `DELETE`
  - **Description:** Deletes the specified prompt.
  - **Path Parameters:**
    - `prompt_id` (integer): ID of the prompt to delete.
  - **Response:** HTTP 204 No Content.

## Frontend

The frontend is a simple HTML page (`index.html`) that interacts with the backend API using **Axios** for HTTP requests and **Tailwind CSS** for styling. It provides the following functionalities:

- **View Prompts:** Displays a list of all prompts.
- **Search Prompts:** Allows users to search through prompts.
- **Create Prompt:** Opens a modal to create a new prompt.
- **Edit Prompt:** Opens a modal to edit an existing prompt.
- **Delete Prompt:** Removes a prompt from the list.

### Serving `index.html`

The backend serves `index.html` at the root URL (`/`). Ensure that `index.html` is located in the same directory as `backend.py`.

## Project Structure

```
.
├── backend.py          # FastAPI backend
├── index.html          # Frontend HTML file
├── requirements.txt    # Python dependencies
└── prompts.db          # SQLite database (auto-generated)
```

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

**Note:** This is a basic README to get you started. Depending on your project's complexity and requirements, you might want to add more sections such as **Testing**, **Deployment**, **Environment Variables**, etc.