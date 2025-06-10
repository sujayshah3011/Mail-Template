# LeadGen Email Assistant

A powerful lead generation tool that automates personalized cold email template creation using AI.

## Features

- 🤖 **AI-Powered Email Generation**: Uses Google Gemini 1.5 Flash to create personalized email templates
- 💾 **Lead Management**: Store and manage leads in PostgreSQL database
- 🎯 **Template Storage**: Save generated templates linked to specific leads
- 🖥️ **User-Friendly Interface**: Streamlit web interface for easy interaction
- 🚀 **FastAPI Backend**: High-performance API with automatic documentation

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database (we use Neon)
- Google Gemini API key

<img width="1121" alt="Screenshot 2025-06-10 at 11 38 28 PM" src="https://github.com/user-attachments/assets/42e1dde3-38d9-4134-9e3c-ed4ffdd00c3e" />
<img width="1265" alt="Screenshot 2025-06-10 at 11 38 52 PM" src="https://github.com/user-attachments/assets/ed7557d3-a0df-44c1-a1f3-70614c8c1e73" />


### Installation

1. **Clone and navigate to the project**:

```bash
cd LeadGen
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
   Create a `.env` file with:

```
DATABASE_URL=your_postgresql_connection_string
GEMINI_API_KEY=your_gemini_api_key
```

### Running the Application

1. **Start the FastAPI backend**:

```bash
uvicorn main:app --reload
```

2. **In a new terminal, start the Streamlit UI**:

```bash
streamlit run app.py
```

3. **Access the application**:
   - **Web Interface**: http://localhost:8501 (Streamlit)
   - **API Documentation**: http://localhost:8000/docs (FastAPI Swagger)
   - **API Root**: http://localhost:8000/ (API info)

## API Endpoints

| Endpoint             | Method | Description                             |
| -------------------- | ------ | --------------------------------------- |
| `/`                  | GET    | API information and available endpoints |
| `/generate_template` | POST   | Generate AI-powered email templates     |
| `/leads`             | POST   | Create and store new leads              |
| `/templates`         | POST   | Save generated templates                |

## Usage Example

### Using the Web Interface

1. Open http://localhost:8501
2. Fill in the lead details form
3. Click "Generate Template"
4. Review and save the generated email template

### Using the API Directly

```bash
curl -X POST "http://localhost:8000/generate_template" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "TechCorp",
    "contact_name": "John Smith",
    "industry": "Software Development",
    "purpose": "Schedule a product demo"
  }'
```

## Project Structure

```
LeadGen/
├── main.py           # FastAPI backend with API endpoints
├── app.py            # Streamlit UI for user interaction
├── database.py       # Database models and connection setup
├── .env              # Environment variables (API keys, DB URL)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Database Schema

- **leads**: `id`, `company_name`, `contact_name`, `industry`, `created_at`
- **templates**: `id`, `lead_id`, `generated_at`, `subject`, `body`

<img width="1436" alt="Screenshot 2025-06-10 at 11 37 54 PM" src="https://github.com/user-attachments/assets/f2a786dd-9c4a-466b-b293-2d7e4b8424f8" />
<img width="1439" alt="Screenshot 2025-06-10 at 11 38 07 PM" src="https://github.com/user-attachments/assets/e6b11bdc-f88f-4934-b9c3-2baa5b19c2a2" />


## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Streamlit**: Easy-to-use framework for data apps
- **SQLAlchemy**: SQL toolkit and ORM for Python
- **PostgreSQL**: Robust relational database (via Neon)
- **Google Gemini**: Advanced AI model for text generation
- **Pydantic**: Data validation using Python type annotations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
