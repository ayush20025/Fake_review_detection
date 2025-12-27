#!/usr/bin/env python3
"""
Production runner for Fake Review Detection System
"""

import os
from app import app

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))

    # Get host from environment variable or default to localhost
    host = os.environ.get('HOST', '127.0.0.1')

    # Run the application
    app.run(host=host, port=port, debug=False)
