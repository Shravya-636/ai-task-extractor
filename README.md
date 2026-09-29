# AI Meeting Task Extractor

An AI-powered full-stack application that converts unstructured meeting notes into structured, actionable tasks.

The application uses Google Gemini to identify tasks, assignees, and due dates from meeting notes. Extracted tasks are validated using Pydantic and stored in PostgreSQL for persistence.

## Features

- Extract actionable tasks from meeting notes using AI
- Identify task title, assignee, and due date
- Validate AI-generated responses using Pydantic
- Store extracted tasks in PostgreSQL
- Responsive and user-friendly web interface
- REST API built with FastAPI
- Handles empty input and API errors

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

The frontend provides a simple interface where users can enter meeting notes and view the extracted tasks.

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Google Gemini API

The backend receives meeting notes, sends them to Gemini for task extraction, validates the structured response, and stores the extracted tasks in PostgreSQL.

### Database

- PostgreSQL
- Neon

Neon is used as the cloud PostgreSQL database for persistent task storage.

## How It Works

1. The user enters meeting notes through the React frontend.
2. The frontend sends the notes to the FastAPI backend.
3. The backend sends the meeting notes to Google Gemini.
4. Gemini extracts actionable tasks and returns structured JSON.
5. Pydantic validates the AI response.
6. Valid tasks are stored in PostgreSQL.
7. The extracted tasks are returned to the frontend and displayed to the user.

## API

### Health Check

```http GET /health```

Returns the current API status.

### Extract Tasks
```http POST /extract```

**Request:**

```json
{
  "notes": "Rahul will prepare the database schema by Friday. Priya needs to review the UI tomorrow."
}
```
**Response:**

```json
{
  "tasks": [
    {
      "title": "Prepare the database schema",
      "assignee": "Rahul",
      "due_date": "Friday"
    },
    {
      "title": "Review the UI",
      "assignee": "Priya",
      "due_date": "tomorrow"
    }
  ]
}
```
## Environment Variables

The backend requires the following environment variables:

```
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_connection_string
```

Keep API keys and database credentials private and do not commit the .env file to GitHub.

## Running Locally
### Backend

Create and activate a Python virtual environment, install the required dependencies, configure the environment variables, and start the FastAPI server.

```
uvicorn app.main:app --reload
```

The backend runs at:

```
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```
http://127.0.0.1:8000/docs
```

### Frontend

Install the frontend dependencies and start the Vite development server:

```
npm install
npm run dev
```

The frontend runs at:

```
http://localhost:5173
```