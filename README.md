# Creative Evaluation Platform

A production-quality prototype for an AI-powered creative evaluation platform. This application allows users to upload scripts or paste text content and receive structured evaluations from specialized AI agents.

## Architecture

The application consists of two main components:

- **Backend**: FastAPI server that orchestrates evaluation requests and routes them to appropriate agents
- **Frontend**: React application (Vite) that provides a clean interface for submitting content and viewing results

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── orchestrator.py      # Routes queries to appropriate agents
│   ├── schemas.py           # Pydantic models for request/response
│   ├── requirements.txt     # Python dependencies
│   └── agents/
│       ├── script_reviewer.py   # Evaluates creative scripts
│       └── impact_agent.py     # Evaluates social impact and sensitivity
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Component styles
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── index.html           # HTML template
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite configuration
│
└── README.md                # This file
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

   The backend will be available at `http://localhost:8000`

   You can also access the interactive API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## How Frontend Connects to Backend

The frontend communicates with the backend via HTTP requests:

1. **API Endpoint**: The frontend sends POST requests to `http://localhost:8000/query`
2. **Request Format**: Uses `multipart/form-data` to send:
   - `text_input` (optional): Text content as a string
   - `file` (optional): PDF or TXT file upload
   - `question` (optional): User's question or evaluation request
3. **Response Format**: The backend returns JSON with:
   - `agent_used`: Which agent processed the request
   - `summary`: High-level evaluation summary
   - `score`: Numerical score (0.0 to 1.0)
   - `details`: Structured evaluation details

**CORS Configuration**: The backend is configured to accept requests from `http://localhost:5173` (Vite default) and `http://localhost:3000` (Create React App default).

## Usage

1. **Start both servers** (backend and frontend) as described above
2. **Open the frontend** in your browser at `http://localhost:5173`
3. **Submit content** using one of these methods:
   - Paste text into the text area
   - Upload a PDF or TXT file
   - Optionally add a question to guide the evaluation
4. **View results** in the "Evaluation Results" section
5. **Check history** in the "Interaction History" section for previous queries

## Agent Routing Logic

The orchestrator routes queries based on the question content:

- **Impact Agent**: Triggered when the question contains keywords like "impact", "sensitivity", "social", "cultural", "representation", "diversity", etc.
- **Script Reviewer**: Default agent for all other evaluative queries

The routing logic is clearly commented in `backend/orchestrator.py` and can be easily extended.

## Current Implementation Notes

- **Mock Responses**: Both agents return mock evaluation results. No actual LLM calls are made.
- **File Support**: Currently supports PDF and TXT files. PDF text extraction uses PyPDF2.
- **No Authentication**: This is a prototype without authentication or user management.
- **Local Only**: Designed to run entirely locally without external API dependencies.

## Future Extensions

The codebase is structured to easily support:

- Adding new agents (create new files in `backend/agents/`)
- Integrating real LLM APIs (replace mock logic in agent functions)
- Adding authentication and user management
- Supporting additional file formats
- Adding more sophisticated routing logic
- Implementing result caching
- Adding database persistence for history

## Development

### Backend Development

- The backend uses FastAPI with automatic API documentation
- Access Swagger UI at `http://localhost:8000/docs`
- Access ReDoc at `http://localhost:8000/redoc`

### Frontend Development

- Uses Vite for fast hot module replacement
- Plain CSS (no frameworks) for styling
- React functional components with hooks

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use

**Frontend won't start:**
- Ensure Node.js 16+ is installed
- Check that dependencies are installed: `npm install`
- Verify port 5173 is not in use

**CORS errors:**
- Ensure backend is running on port 8000
- Check that frontend is making requests to `http://localhost:8000`
- Verify CORS middleware is configured in `backend/main.py`

**File upload errors:**
- Ensure file is PDF or TXT format
- Check file size (very large files may cause issues)
- Verify file is not corrupted

## License

This is a prototype project for educational/demonstration purposes.

