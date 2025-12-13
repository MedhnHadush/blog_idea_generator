"""
AI Blog Generator - Flask Backend
A simple Flask application that generates blog posts using OpenAI API
"""

from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


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
        
        # Validate that topic is not empty
        if not topic:
            return jsonify({'error': 'Please enter a blog topic'}), 400
        
        # Create a prompt for the OpenAI API
        prompt = f"Write a short, engaging blog post (approximately 300-400 words) about: {topic}. Make it informative and well-structured with an introduction, main content, and conclusion."
        
        # Call OpenAI API to generate the blog post
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 for cost efficiency
            messages=[
                {"role": "system", "content": "You are a professional blog writer who creates engaging and informative content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Limit tokens to keep response concise
            temperature=0.7  # Balance between creativity and consistency
        )
        
        # Extract the generated blog content
        blog_content = response.choices[0].message.content
        
        # Return the generated blog as JSON
        return jsonify({'blog': blog_content})
    
    except Exception as e:
        # Handle any errors (e.g., API key issues, network problems)
        return jsonify({'error': f'Error generating blog: {str(e)}'}), 500


if __name__ == '__main__':
    # Run the Flask app in debug mode (for development)
    # In production, use a proper WSGI server like Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)

