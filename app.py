"""
AI Blog Generator - Flask Backend
A simple Flask application that generates blog posts using OpenAI API
"""

from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, Timeout
import os
import re
import logging
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration constants
MAX_TOPIC_LENGTH = 200
MIN_TOPIC_LENGTH = 3
MAX_TOKENS = 800
TEMPERATURE = 0.7
MODEL = "gpt-3.5-turbo"
REQUEST_TIMEOUT = 60  # seconds

# Initialize OpenAI client with API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY environment variable is required")

client = OpenAI(api_key=api_key, timeout=REQUEST_TIMEOUT)


def sanitize_input(text):
    """
    Sanitize user input to prevent injection attacks
    Remove potentially harmful characters while preserving content
    """
    if not text:
        return ""
    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    # Limit consecutive whitespace
    text = re.sub(r'\s{3,}', ' ', text)
    return text.strip()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Blog Generator',
        'version': '1.0.0'
    }), 200


@app.route('/')
def index():
    """Render the main page with the blog generator form"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_blog():
    """
    Generate a blog post based on the topic provided by the user
    Returns JSON response with generated blog content or error message
    """
    try:
        # Get the blog topic from the form data
        topic = request.form.get('topic', '').strip()
        
        # Sanitize input
        topic = sanitize_input(topic)
        
        # Validate topic length
        if not topic:
            logger.warning("Empty topic received")
            return jsonify({'error': 'Please enter a blog topic'}), 400
        
        if len(topic) < MIN_TOPIC_LENGTH:
            logger.warning(f"Topic too short: {len(topic)} characters")
            return jsonify({'error': f'Topic must be at least {MIN_TOPIC_LENGTH} characters long'}), 400
        
        if len(topic) > MAX_TOPIC_LENGTH:
            logger.warning(f"Topic too long: {len(topic)} characters")
            return jsonify({'error': f'Topic must not exceed {MAX_TOPIC_LENGTH} characters'}), 400
        
        logger.info(f"Generating blog for topic: {topic[:50]}...")
        
        # Create a well-structured prompt for the OpenAI API
        system_prompt = (
            "You are a professional blog writer who creates engaging, informative, "
            "and well-structured blog posts. Your writing is clear, concise, and "
            "engaging for a general audience."
        )
        
        user_prompt = (
            f"Write a comprehensive blog post (approximately 400-500 words) about: {topic}. "
            "Structure it with:\n"
            "1. An engaging introduction that hooks the reader\n"
            "2. Well-organized main content with clear paragraphs\n"
            "3. A thoughtful conclusion that summarizes key points\n"
            "Make it informative, engaging, and easy to read."
        )
        
        # Call OpenAI API to generate the blog post
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
        except RateLimitError as e:
            logger.error(f"Rate limit error: {str(e)}")
            return jsonify({
                'error': 'API rate limit exceeded. Please try again in a moment.'
            }), 429
        except Timeout as e:
            logger.error(f"Request timeout: {str(e)}")
            return jsonify({
                'error': 'Request timed out. The AI service is taking too long to respond. Please try again.'
            }), 504
        except APIConnectionError as e:
            logger.error(f"API connection error: {str(e)}")
            return jsonify({
                'error': 'Connection error. Please check your internet connection and try again.'
            }), 503
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            error_msg = str(e).lower()
            if 'invalid api key' in error_msg or 'authentication' in error_msg:
                return jsonify({
                    'error': 'Invalid API key. Please check your configuration.'
                }), 401
            return jsonify({
                'error': 'Error communicating with AI service. Please try again later.'
            }), 500
        
        # Extract the generated blog content
        if not response.choices or not response.choices[0].message.content:
            logger.error("Empty response from OpenAI API")
            return jsonify({'error': 'Received empty response from AI service'}), 500
        
        blog_content = response.choices[0].message.content.strip()
        
        logger.info(f"Successfully generated blog post ({len(blog_content)} characters)")
        
        # Return the generated blog as JSON
        return jsonify({
            'blog': blog_content,
            'topic': topic,
            'word_count': len(blog_content.split())
        })
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred. Please try again later.'
        }), 500


if __name__ == '__main__':
    # Run the Flask app in debug mode (for development)
    # In production, use a proper WSGI server like Gunicorn
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port} (debug={debug_mode})")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

