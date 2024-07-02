# EchoMind

## Description

A personal memory embedding and search system that allows you to store text memories and retrieve them based on semantic similarity using vector embeddings.

## Features

- Add personal memories via text input
- Search memories using natural language queries
- View all stored memories
- Delete unwanted memories
- Vector-based similarity search with configurable threshold

## Technologies

- Backend: FastAPI, ChromaDB, Sentence Transformers
- Frontend: Streamlit
- Embeddings: all-MiniLM-L6-v2 model

## Prerequisites

- Python 3.11 or higher
- Git
- Docker and Docker Compose (for easy setup)

## Quick Start with Docker Compose (Recommended for Non-Tech Users)

1. Install Docker and Docker Compose on your system.

2. Clone the repository:
   ```
   git clone https://github.com/ashangupta/echomind
   cd echomind
   ```

3. Run the application:
   ```
   docker-compose up
   ```

4. Open your browser and go to `http://localhost:8501` to access the app.

That's it! The backend and frontend will start automatically.

## Local Setup (For Developers)

1. Clone the repository:
   ```
   git clone https://github.com/ashankgupta/echomind
   cd echomind
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Linux/Mac: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

6. In another terminal, run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

## Usage

- Open the Streamlit app in your browser (usually http://localhost:8501)
- Add memories in the "Add Memory" section
- Search for memories in the "Search Memories" section
- View and delete memories in the "Show all stored memories" section

## API Endpoints

- POST /ingest: Ingest a new memory (text)
- POST /context: Query similar memories (query, top_k)
- GET /all_memories: Retrieve all stored memories
- DELETE /delete: Delete a memory by ID

## Docker

### Backend (FastAPI)

1. Build the backend image:
   ```
   docker build -t echomind-backend .
   ```

2. Run the backend container:
   ```
   docker run -p 8000:8000 echomind-backend
   ```

### Frontend (Streamlit)

1. Build the frontend image:
   ```
   docker build -f Dockerfile.streamlit -t echomind-frontend .
   ```

2. Run the frontend container:
   ```
   docker run -p 8501:8501 echomind-frontend
   ```

Note: The Streamlit app is configured to connect to `http://localhost:8000`. When running in Docker, you may need to use Docker networking or adjust the API_URL in `streamlit_app.py` to point to the backend container.

## License

This project is licensed under the MIT License.
