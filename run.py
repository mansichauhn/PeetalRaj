from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Run the app
    # In production, use a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
