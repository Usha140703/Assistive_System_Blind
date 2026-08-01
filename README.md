# Assistive System for the Blind

An AI-powered accessibility tool that helps visually impaired users understand their surroundings. Users capture an image of their environment, ask a question about it, and receive a spoken answer describing what the AI sees — enabling real-time visual understanding through voice interaction.

## How It Works
1. The user captures an image through the web interface
2. They ask a question about the image (e.g., "What is in front of me?")
3. The image and question are sent to Google's Gemini AI for analysis
4. Gemini generates a natural language answer describing the scene
5. The answer is converted to speech and read aloud to the user

## Features
- Real-time image capture via webcam
- Natural language Q&A about captured images using Gemini's vision capabilities
- Automatic language detection for multilingual responses
- Text-to-speech output for accessibility
- Simple, lightweight web interface built with Django

## Tech Stack
- **Backend:** Django (Python)
- **AI / Vision-Language Model:** Google Gemini API
- **Image Processing:** OpenCV, NumPy
- **Text-to-Speech:** pyttsx3
- **Language Detection:** langdetect

## Getting Started

1. Clone the repository and navigate into it
2. Create a virtual environment and activate it
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Create a `.env` file in the project root with your Gemini API key:

GOOGLE_API_KEY=your_api_key_here

5. Run the development server:
```bash
   python manage.py runserver
```
6. Open `http://localhost:8000` in your browser

## Author
**Miriyala Usha Rani**
