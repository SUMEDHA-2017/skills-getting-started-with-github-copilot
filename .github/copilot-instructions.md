# Copilot Instructions for Mergington High School Activities API

## Project Overview
A lightweight **full-stack FastAPI web application** for managing extracurricular activity signups at a high school. The backend provides REST endpoints while the frontend is a vanilla JavaScript SPA that fetches and displays activities.

## Architecture

### Backend (`src/app.py`)
- **FastAPI** REST API with in-memory data storage
- Two main endpoints:
  - `GET /activities` - Returns all activities with participant lists
  - `POST /activities/{activity_name}/signup?email=<email>` - Adds student to activity
- Static file serving mounted at `/static`
- Activity data structure: name (key) → description, schedule, max_participants, participants list

### Frontend (`src/static/`)
- **index.html** - Two-section layout: activity cards display + signup form
- **app.js** - Fetches activities on page load, populates UI, handles form submission
- **styles.css** - Basic styling for cards and layout

## Key Conventions

1. **Data Storage**: Activities use name as identifier (e.g., "Chess Club"). Students identified by email. All data is **in-memory only** - resets on server restart.
2. **API Responses**: Activities endpoint returns full activity objects; signup endpoint returns status messages.
3. **Error Handling**: Use `HTTPException(status_code=404)` for missing activities; frontend shows error messages via DOM updates.
4. **Email Format**: Assumes `@mergington.edu` domain convention.

## Running & Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (from workspace root or src/)
cd src && python app.py
# OR directly from workspace root:
python -m uvicorn src.app:app --reload

# Access
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs (interactive Swagger UI)
```

## Common Patterns

- **Frontend Data Flow**: `DOMContentLoaded` → `fetchActivities()` populates list & dropdown → form submission calls `/activities/{name}/signup`
- **Validation**: Check activity exists before signup; frontend validates email input (HTML5)
- **DOM Updates**: Use `innerHTML` for rendering activity cards; message div shows signup feedback

## Integration Points

- FastAPI's automatic OpenAPI docs at `/docs`
- Static file serving requires correct `Path` and `os.path.join()` setup
- CORS not currently configured (single-origin only)

## Development Notes

- No database setup required - ideal for learning/demos
- Frontend is tightly coupled to API response format
- Consider adding duplicate signup prevention, capacity checks in future enhancements
