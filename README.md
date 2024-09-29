
---

# Ace Interview

**Ace Interview** is an advanced platform designed to enhance the interview process using artificial intelligence and speech recognition technologies. The application integrates real-time speech-to-text conversion with interactive chat capabilities, providing users with an engaging and effective interview simulation experience.

## Features

- **Real-Time Speech Recognition**: Converts spoken language into text using `SpeechRecognition`.
- **Text-to-Speech**: Provides audible responses using `pyttsx3`.
- **Interactive Chat**: Simulates conversations with an AI model from `google.generativeai`.
- **File Parsing**: Extracts text from documents using `tika`.
- **Graphical User Interface (GUI)**: Built with `tkinter` for user-friendly interactions.
- **Image Handling**: Utilizes `PIL` for displaying and manipulating images.

## Installation

To get started with Ace Interview, you can either install it locally from source or download the executable file for easy setup.

### Option 1: Install from Source

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

   Make sure the following libraries are listed in your `requirements.txt`:

   ```
   smtplib
   email
   psycopg2
   opencv-python
   pyttsx3
   SpeechRecognition
   google-generativeai
   tika
   tkinter
   pandas
   pillow
   ```

4. **Run the Application**

   To start the application, run the main script:

   ```bash
   python main.py
   ```

### Option 2: Install Using Executable File

For a simpler installation process, download the executable file and run the application directly without setting up the development environment.

- **Download the executable file** from this [Drive link](#) (replace `#` with the actual link).

1. Download the `.exe` file.
2. Run the file and follow the on-screen instructions to install and use the application.

## Usage

1. **Start Interview**: Initiates the interview simulation.
2. **Chat with AI**: Engage in conversations with the AI model.
3. **Voice Commands**: Use speech recognition to interact with the system.
4. **Text-to-Speech Responses**: Hear responses from the AI.

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
- **tika**: Extracts text from various file formats.
- **pandas**: Data manipulation and analysis.
- **PIL (Pillow)**: Image handling.

## Contact

For any questions or issues, please contact [sak78620@gmail.com](mailto:sak78620@gmail.com).

---
