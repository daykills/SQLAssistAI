# SQLAssistAI

SQLAssistAI harnesses OpenAI's GPT models and Jinja templates for evaluating SQL queries, offering insights and improvements through Python-driven parsing of AI outputs, streamlining query optimization for developers and data analysts.

## Technical Stack
* Python: Serves as the backbone of the project, orchestrating interactions with the OpenAI API, processing AI-generated responses, and handling the overall logic and data flow.
* Jinja: Facilitates dynamic and flexible generation of prompts, allowing for tailored queries to the AI model based on user-defined templates.
* OpenAI API: Connects to GPT models, tapping into cutting-edge AI for query evaluation and analysis.

## Setup and Installation

1. Clone the Project
```
git clone https://github.com/yourusername/SQLAssistAI.git
cd SQLAssistAI
```

2. Environment Setup
```
python3 -m venv env
source env/bin/activate  # On macOS and Linux
.\env\Scripts\activate   # On Windows
```

## Configuration

* OpenAI API Key: Place your API key in a .env file at the project root:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage
* Run SQLAssistAI to evaluate your SQL queries through a simple command:
```
python query.py path/to/template.jinja

```