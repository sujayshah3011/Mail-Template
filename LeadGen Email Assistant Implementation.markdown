# LeadGen Email Assistant: A 5-Hour Lead Generation Tool

## Introduction

This project enhances the lead generation process by automating personalized cold email template creation, a critical component of sales outreach. Built within 5 hours using Neon tech database, FastAPI, Google Gemini 1.5 Flash API, and Streamlit, it aligns with the business model of [Saasquatchleads.com](https://www.saasquatchleads.com/), a platform for lead scraping, enrichment, and outreach. The tool focuses on the **Quality First** approach, enhancing outreach efficiency while avoiding ethical complexities of scraping.

## Business Use Case

Lead generation is vital for sales, involving identifying target companies, enriching lead data, and engaging prospects. Saasquatchleads.com offers features like:

- **Scraping Leads**: Gathering company/contact data from public sources.
- **Enrichment**: Adding details like emails, phones, and LinkedIn profiles.
- **Save/Export**: Storing leads for export to CSV/Excel.
- **Outreach Tools**: Enabling cold calls/emails for enterprise users.

The **LeadGen Email Assistant** focuses on outreach, automating email template creation. Sales teams often spend significant time drafting personalized emails. This tool streamlines that process, improving efficiency and consistency, which aligns with real-world sales needs.

## Design Choices

### Feature Selection

- **Personalized Email Template Generation**:
  - **Why**: Outreach is a high-impact area where automation saves time. It mirrors Saasquatchleads.com's enterprise outreach tools.
  - **How**: Users input lead details (company name, contact name, industry), and Google Gemini 1.5 Flash API generates tailored email templates.
- **Lead and Template Storage**:
  - **Why**: Storing data allows users to manage leads and revisit templates, enhancing usability.
  - **How**: Neon PostgreSQL database stores leads and templates.

### Why Not Scraping or Enrichment?

- **Scraping**: Ethically and legally complex, requiring compliance with website terms. Public APIs (e.g., Clearbit) are often paid, and free alternatives lack contact data.
- **Enrichment**: Generating contact details (e.g., emails) without APIs is speculative and less accurate. Gemini could infer industry/revenue, but its knowledge is outdated (pre-2023).

Focusing on outreach avoids these issues while delivering value within 5 hours.

### Technologies

- **FastAPI**: Lightweight, scalable backend for API endpoints.
- **Neon PostgreSQL**: Serverless database for storing leads/templates, using the provided connection string.
- **Google Gemini 1.5 Flash API**: Generates high-quality email templates ([Google AI Studio](https://ai.google.dev/)).
- **Streamlit**: Rapid UI prototyping for user-friendly input and display.
- **.env**: Securely stores API credentials and database URL.

## Implementation Plan

### Project Structure

```
LeadGen/
├── main.py           # FastAPI backend with API endpoints
├── app.py            # Streamlit UI for user interaction
├── database.py       # Database models and connection setup
├── .env              # Environment variables (API keys, DB URL)
├── requirements.txt  # Python dependencies
└── __pycache__/      # Python cache files
```

### Dependencies

```
fastapi
uvicorn
streamlit
sqlalchemy
psycopg2-binary
google-generativeai
python-dotenv
```

### .env File

```
DATABASE_URL=your_neon_postgresql_url
GEMINI_API_KEY=your_gemini_api_key
```

### Database Schema

| Table         | Fields                                                              |
| ------------- | ------------------------------------------------------------------- |
| **leads**     | `id` (PK), `company_name`, `contact_name`, `industry`, `created_at` |
| **templates** | `id` (PK), `lead_id` (FK), `generated_at`, `subject`, `body`        |

**Implementation Details**:

- Uses SQLAlchemy ORM with PostgreSQL
- Database models defined in `database.py`
- Automatic table creation via `Base.metadata.create_all(engine)`
- Session management through `SessionLocal` sessionmaker

### FastAPI Endpoints

| Endpoint             | Method | Description                           | Status         |
| -------------------- | ------ | ------------------------------------- | -------------- |
| `/`                  | GET    | API info and available endpoints      | ✅ Implemented |
| `/generate_template` | POST   | Generates email template using Gemini | ✅ Implemented |
| `/leads`             | POST   | Creates a new lead                    | ✅ Implemented |
| `/templates`         | POST   | Saves a new template                  | ✅ Implemented |

**Note**: The current implementation focuses on POST endpoints for creating data. GET endpoints for listing leads and templates are planned for future iterations.

### Streamlit UI

The Streamlit application (`app.py`) provides a user-friendly interface with:

- **Lead Input Form**:

  - Company name, contact name, industry, and email purpose fields
  - Form validation and session state management
  - Generate template button with API integration

- **Template Display**:

  - Shows AI-generated email subject and body
  - Professional formatting with expandable sections
  - Copy-to-clipboard functionality for generated content

- **Lead Management**:
  - Save lead functionality with database integration
  - Template storage linked to specific leads
  - Error handling and user feedback

**Key Features**:

- Real-time API communication with FastAPI backend
- Session state persistence for better UX
- Responsive design with clear visual hierarchy

### Implementation Timeline

| Hour | Task                        | Status      |
| ---- | --------------------------- | ----------- |
| 1    | Project setup, dependencies | ✅ Complete |
| 2    | Database integration        | ✅ Complete |
| 3    | FastAPI endpoints           | ✅ Complete |
| 4    | Streamlit UI                | ✅ Complete |
| 5    | Testing, error handling     | ✅ Complete |

**Actual Implementation Details**:

- **Hour 1**: Set up FastAPI project structure, installed dependencies (FastAPI, SQLAlchemy, psycopg2-binary, google-generativeai, Streamlit)
- **Hour 2**: Implemented database models, connection setup, and session management with Neon PostgreSQL
- **Hour 3**: Created API endpoints for template generation, lead creation, and template storage with proper error handling
- **Hour 4**: Built Streamlit interface with form handling, API integration, and user feedback
- **Hour 5**: Debugging database sessions, testing all endpoints, and ensuring proper error handling

## Technical Implementation

### API Architecture

The FastAPI backend (`main.py`) implements:

- **Dependency Injection**: Proper database session management with `get_db()` function
- **Pydantic Models**: Input validation for `GenerateTemplateInput`, `LeadInput`, and `TemplateInput`
- **Error Handling**: Comprehensive exception handling with appropriate HTTP status codes
- **Logging**: Debug-level logging for request tracking and troubleshooting

### Key Components

1. **Google Gemini Integration**: Uses `google-generativeai` library with Gemini 1.5 Flash model
2. **Database Layer**: SQLAlchemy ORM with PostgreSQL, automatic schema creation
3. **Session Management**: Proper database connection lifecycle with dependency injection
4. **UI Layer**: Streamlit with session state management and real-time API communication

### Performance Considerations

- Database connection pooling through SQLAlchemy
- Async endpoint support in FastAPI
- Efficient session management to prevent connection leaks
- Error boundaries to handle API failures gracefully

## Submission Requirements

- **GitHub Repository**: Includes code, `README.md` with setup instructions, and `.env.example`.
- **Report**: 1-page PDF/Markdown detailing approach, model (Gemini 1.5 Flash), and performance (template quality).
- **Video Walkthrough**: 1-2 minute demo showing input, template generation, and lead management.
- **Demo**: Optional, but Streamlit UI serves as a live demo.

## Running the Application

### Prerequisites

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file with:

```
DATABASE_URL=your_neon_postgresql_url
GEMINI_API_KEY=your_gemini_api_key
```

### Start the Application

```bash
# Terminal 1: Start FastAPI backend
uvicorn main:app --reload

# Terminal 2: Start Streamlit UI
streamlit run app.py
```

### API Testing

```bash
# Test API directly
curl -X POST "http://localhost:8000/generate_template" \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Test Corp", "contact_name": "John Doe", "industry": "Technology", "purpose": "Product demo"}'
```

## Conclusion

The LeadGen Email Assistant enhances lead generation by automating personalized email template creation. It leverages specified technologies effectively, delivering a practical tool for sales teams within 5 hours. Future improvements could include CSV export or integration with public APIs for lead enrichment.
