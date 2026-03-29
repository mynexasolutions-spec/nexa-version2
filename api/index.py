"""
Vercel serverless entry point for Flask app.
This imports and exports the Flask app for Vercel to run as a serverless function.
"""
import sys
import os

# Add parent directory to path so we can import app and other modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

# Export the app for Vercel
__all__ = ['app']
