# Rule Engine Application

This project is a simple 3-tier rule engine application that uses Abstract Syntax Tree (AST) to determine user eligibility based on attributes like age, department, income, etc.

## Features
- Dynamic rule creation and evaluation using AST.
- Combine multiple rules for evaluation.
- API-based interaction.
- PostgreSQL database for rule storage.

## Requirements
- Docker
- Docker Compose

## How to Build and Run

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/rule-engine.git
    cd rule-engine
    ```

2. **Build the Docker containers**:
    ```bash
    docker-compose build
    ```

3. **Run the application**:
    ```bash
    docker-compose up
    ```

4. The Python app will be accessible on port 5000, and PostgreSQL will be available inside the Docker network.

## Design Choices
- **AST Representation**: We use a tree structure with nodes representing operators and operands for flexible rule evaluation.
- **PostgreSQL**: Chosen for its robustness in handling complex queries and data storage.
- **Docker**: Simplifies environment setup by containerizing both the app and database.
