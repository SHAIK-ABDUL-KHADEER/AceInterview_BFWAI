# Ace Interview

**Ace Interview** is an advanced platform designed to enhance the interview process using artificial intelligence and speech recognition technologies. The application integrates real-time speech-to-text conversion with interactive chat capabilities, providing users with an engaging and effective interview simulation experience.

## Features

- **Real-Time Speech Recognition**: Converts spoken language into text using `SpeechRecognition`.
- **Text-to-Speech**: Provides audible responses using `pyttsx3`.
- **Interactive Chat**: Simulates conversations with an AI model from `google.generativeai`.
- **File Parsing**: Extracts text from documents using `pypdf2`.
- **Graphical User Interface (GUI)**: Built with `tkinter` for user-friendly interactions.
- **Image Handling**: Utilizes `PIL` for displaying and manipulating images.

## Installation

To get started with Ace Interview, you need to install the required dependencies. You can install them using `pip`. Here's how to set up your environment:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/SHAIK-ABDUL-KHADEER/AceInterview.git
   cd ace-interview
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Make sure you have the following libraries listed in your `requirements.txt`:

   ```
   smtplib
   email
   psycopg2
   opencv-python
   pyttsx3
   SpeechRecognition
   google-generativeai
   pypdf2
   tkinter
   pandas
   pillow
   ```

## Usage

1. **Run the Application**

   To start the application, run the main script:

   ```bash
   python main.py
   ```

2. **Features**

   - **Start Interview**: Initiates the interview simulation.
   - **Chat with AI**: Engage in conversations with the AI model.
   - **Voice Commands**: Use speech recognition to interact with the system.
   - **Text-to-Speech Responses**: Hear responses from the AI.

## Dependencies

- **smtplib**: Used for sending emails.
- **email.mime**: Handles email creation and sending.
- **random**: Generates random values.
- **psycopg2**: Interface for PostgreSQL database.
- **tkinter**: GUI toolkit for creating the user interface.
- **cv2 (OpenCV)**: Image processing.
- **pyttsx3**: Text-to-speech conversion.
- **SpeechRecognition**: Speech-to-text conversion.
- **google.generativeai**: Interacts with Google's generative AI model.
- **pypdf**: Extracts text from various file formats.
- **pandas**: Data manipulation and analysis.
- **PIL (Pillow)**: Image handling.


## Contact

For any questions or issues, please contact [sak78620@gmail.com](mailto:sak78620@gmail.com).

---

Feel free to adjust the text and sections according to your specific needs and project details.
