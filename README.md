# AI Blog Generator

A simple end-to-end Generative AI project that generates blog posts using OpenAI's API.

## Features

- Clean, minimal interface
- Generate blog posts from any topic
- Real-time generation with loading indicators
- Error handling for API issues

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup Instructions

### 1. Clone or navigate to the project directory

```bash
cd ideagent
```

### 2. Create a virtual environment (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
   (On macOS/Linux: `cp .env.example .env`)

2. Open `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### 5. Run the application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 6. Open in your browser

Navigate to: `http://localhost:5000`

## Usage

1. Enter a blog topic in the input field (e.g., "The Future of AI")
2. Click "Generate Blog Post"
3. Wait for the AI to generate your blog post
4. The generated blog will appear below the form

## Project Structure

```
ideagent/
├── app.py                 # Flask backend with OpenAI integration
├── templates/
│   └── index.html        # Frontend HTML with form and display
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables file
├── .env                 # Your actual environment variables (create this)
└── README.md            # This file
```

## Technical Details

- **Backend**: Flask (Python web framework)
- **LLM**: OpenAI GPT-3.5-turbo
- **Frontend**: Vanilla HTML, CSS, and JavaScript
- **API Client**: Official OpenAI Python client

## Notes

- The app runs in debug mode for development
- For production, use a proper WSGI server like Gunicorn
- Make sure to keep your `.env` file secure and never commit it to version control

## Troubleshooting

- **"Error generating blog"**: Check that your OpenAI API key is correct and has credits
- **Module not found**: Make sure you've activated your virtual environment and installed requirements
- **Port already in use**: Change the port in `app.py` (last line) from 5000 to another port

