# FastAPI Learning Project

This project explores FastAPI by following the official [FastAPI documentation](https://fastapi.tiangolo.com/learn/) and particularly the [User Guide](https://fastapi.tiangolo.com/tutorial/). The goal was to create an API with various endpoints to explore FastAPI's extensive features.

## Project Objectives
- Understand and implement different path operations.
- Explore data validation and conversion using Pydantic.
- Learn request parameter handling with Query, Body, Header, Cookie, Path, Form, and File.
- Handle exceptions effectively.
- Utilize FastAPI's middleware and dependency injection system.
- Implement secure API authentication using OAuth2 and Bearer tokens.
- Integrate SQL databases using SQLModel.
- Apply best practices for project structure and testing.

## Key Features

### Path Operations
- Created path operation functions using decorators like `@app.get("/")`.

### Data Validation with Pydantic
- Leveraged Pydantic models inherited from `pydantic.BaseModel` for request validation.

### Request Parameter Handling
- Explored `Query`, `Body`, `Header`, `Cookie`, `Path`, `Form`, and `File` functions.
- Enhanced validation with `typing.Annotated`.

### Enhanced OpenAPI Documentation
- Created examples using `openapi_examples` for better API documentation.

### Status Code Management
- Utilized `fastapi.status` for intuitive status code definitions.

### Error Handling
- Handled custom and standard exceptions using decorators like `@app.exception_handler(RequestValidationError)`.

### Data Serialization
- Used `fastapi.encoders.jsonable_encoder` for complex object serialization.

### PATCH Operations
- Implemented effective item updates using `.model_dump(exclude_unset=True)` and `.model_copy(update=body_data)`.

### Dependency Injection
- Explored the power of `fastapi.Depends` for modular and reusable functions.

### Security and Authentication
- Implemented authentication using `fastapi.security.OAuth2PasswordBearer`.
- Created bearer tokens with `fastapi.security.OAuth2PasswordRequestForm`.

### Middleware
- Implemented middleware with `@app.middleware("http")`.
- Addressed CORS issues using `fastapi.middleware.cors.CORSMiddleware`.

### Database Integration
- Integrated SQL databases using `sqlmodel`.
- Managed sessions with `Session(engine)`.

### Table Modeling
- Defined database tables using `sqlmodel.SQLModel` with `table=True`.
- Enforced response models to control exposed data.

### Best Practices and Refactoring
- Refactored the application into the following directory structure:
  ```
  app/
  ├── db/                # Table models and database storage
  ├── logs/              # Application logs
  ├── routers/           # Route definitions
  ├── tests/             # Unit tests
  ├── utils/             # Utility functions
  ├── main.py            # Application entry point
  └── dependencies.py    # Application dependencies
  ```

## How to Run the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/Lucas-I-Marciano/15.study_fast_api
   ```

2. Navigate to the project directory:

   ```bash
   cd 15.study_fast_api
   ```

3. Create a virtual environment and activate it:
   
   **On Linux/MacOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the interactive API documentation at:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Author
[Lucas I. Marciano](https://github.com/Lucas-I-Marciano)

## License
This project is for educational purposes only and does not include a specific license.

