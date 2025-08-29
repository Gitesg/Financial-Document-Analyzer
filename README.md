

---

# Financial Document Analyzer

## Overview

The Financial Document Analyzer is an AI-powered system for analyzing financial reports such as annual statements, quarterly updates, and investor documents.
It uses **FastAPI** for the API layer, **CrewAI agents** for analysis, and **Celery with Redis** for background processing.

Features:

* Upload PDF financial documents
* Automated analysis of key metrics and trends
* Investment recommendations
* Risk assessments
* Document verification

---

## Quick Start

Clone the repo and run:

```bash
git clone https://github.com/<your-username>/financial-document-analyzer.git
cd financial-document-analyzer
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Requirements

* Python 3.10 or higher
* Redis (for Celery broker/backend)
* MongoDB (optional for storage)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file in the root:

```env
OPENAI_API_KEY=your_api_key_here
MONGO_URI=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379/0
```

---

## Running the Application

1. Start Redis:

```bash
docker run -d -p 6379:6379 redis
```

2. Start Celery worker:

```bash
celery -A celery_app.celery_app worker --loglevel=info
```

3. Run FastAPI:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## API Usage

### Health check

```
GET http://localhost:8000/
```

Response:

```json
{"message": "Financial Document Analyzer API is running"}
```

### Analyze a PDF

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=Analyze Tesla Q2 report"
```

---

## Interactive API Docs (Swagger / ReDoc)

FastAPI automatically provides **interactive API documentation**.
Once the server is running, open:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

From Swagger UI you can:

* Upload a PDF file
* Enter your query
* Run the `/analyze` endpoint interactively
* See the response without using curl

Example workflow:

1. Start FastAPI with:

   ```bash
   uvicorn main:app --reload
   ```
2. Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
3. Expand the **/analyze** endpoint, upload a document, and run your query.

---

## Project Structure

```
.
├── agents.py          # AI agents
├── task.py            # Task definitions
├── tools.py           # Utility tools (PDF reader, analysis, risk)
├── main.py            # FastAPI entry point
├── celery_app.py      # Celery worker setup
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
└── data/              # PDF sample files
```

---

## Development Notes

* Agents are powered by GPT-4o-mini (via CrewAI).
* Tools handle PDF reading, investment analysis, and risk assessment.
* MongoDB is optional, Redis is required for Celery.

---

## Roadmap

* Expand `tools.py` with financial analysis logic
* Add richer outputs for each agent
* Build error monitoring and logging system
* Improve scalability with task orchestration

---

## Contributing

Contributions are welcome. Please open issues and submit pull requests.

---

## License
MIT License

---

```mermaid
flowchart TD
    U[User] --> API[FastAPI API Layer]
    API --> Celery[Celery Worker]
    API --> Tasks[Tasks Layer]
    Celery --> Tasks
    Tasks --> Agents[Agents Layer]
    Agents --> Tools[Tools Layer]
    Agents --> LLM["LLM Service (GPT-4o-mini)"]
    Tools --> DB[MongoDB]
    Celery --> Redis[Redis Broker/Backend]
    Agents --> Output[Analysis & Recommendations]
    Output --> U
