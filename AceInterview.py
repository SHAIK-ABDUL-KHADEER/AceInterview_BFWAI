import sys
import cv2
import time
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
import threading
from tkinter import font as tkfont
from PIL import Image, ImageTk
import openpyxl
import os

# Get the directory where the executable is located
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Create a relative path to your Excel file
excel_path = os.path.join(base_path, 'company_faqs.xlsx')





# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to male voice

# Configure Google Generative AI
genai.configure(api_key="AIzaSyAgmlM70rVc9g-lMtu8NIBD9hYqVRk0dVI")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Extract text from any file using pypdf
def extract_text_from_file(file_path):
    try:
        # Opening the PDF file
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
        return text.strip() if text else None
    except Exception as e:
        messagebox.showerror("Error", f"Error extracting text from the PDF: {e}")
        return None

# Load company-specific questions from Excel
def load_company_questions(company_name):
    try:
        df = pd.read_excel(excel_path)
        if company_name in df.columns:
            faqs = df[company_name].dropna().tolist()
            return faqs
        else:
            messagebox.showerror("Error", f"{company_name} not found in the Excel sheet.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load company-specific questions: {e}")
        return None

# Start the chat session with modified history and company-specific questions
def start_chat_session(text, round_type, company_name=None, user_role=None):
    company_name = company_selection.get()
    user_role = role_entry.get()  # Get user role from entry
    interview_instructions = {
        "HR": (
            "You will conduct an HR interview based on the following resume. "
            "Ask questions about the candidate's communication skills, leadership qualities, and teamwork experiences."
        ),
        "TR": (
            "You will conduct a Technical interview based on the resume. "
            "Ask questions focusing on technical skills, coding knowledge, problem-solving ability, and relevant experience."
        ),
        "MR": (
            "You will conduct a Managerial interview based on the resume. "
            "Ask questions related to managerial skills, decision-making, team management, and handling complex projects."
        ),
    }

    if company_name:
        faqs = load_company_questions(company_name)
        if faqs:
            custom_questions = " ".join(faqs)
            instructions = (
                f"You are conducting a {round_type} interview for {company_name}. "
                f"Here are some frequently asked questions: {custom_questions}. "
                "Ask follow-up questions as necessary."
            )
        else:
            return None
    else:
        instructions = interview_instructions[round_type]

    if user_role:
        instructions += f" The candidate is applying for the role of {user_role}."

    return model.start_chat(
        history=[{
            "role": "user",
            "parts": [
                f"You are conducting a {round_type} interview. {instructions} "
                "Here is the resume: " + text + ". "
                "You must ask 10 questions one by one. Make sure the questions are focused on the candidate's skills, "
                "experience, education, and relevant accomplishments mentioned in the resume. "
                "Don't let the user talk any unnecessary conversation, rather stick to the interview. Be a little strict. "
                "Call the user by the name mentioned in their resume, and if you don't get the name, just ask them their name. "
                "Do not use emojis, bold letters, or any symbols. Just be clear and concise. "
                "After the 15th question, give feedback, including strengths and areas for improvement, and provide a rating out of 10."
            ],
        }, {
            "role": "model",
            "parts": [
                f"Let's begin the {round_type} interview. I'll ask 15 questions based on the provided resume."
            ],
        }]
    )

# Recognize speech from the user
def recognize_speech_from_mic(chat_session, text_widget, duration=10):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    text_widget.insert(tk.END, "Adjusting for ambient noise... Please wait.\n")
    text_widget.update()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        text_widget.insert(tk.END, "Listening for speech...\n")
        text_widget.update()

        while True:
            audio = recognizer.listen(source, timeout=duration)

            text_widget.insert(tk.END, "Recognizing speech...\n")
            text_widget.update()
            try:
                transcription = recognizer.recognize_google(audio)
                text_widget.insert(tk.END, "You said: " + transcription + "\n")
                text_widget.update()

                if "stop listening" in transcription.lower():
                    text_widget.insert(tk.END, "Stopping listening...\n")
                    text_widget.update()
                    break  # Exit the loop if "stop listening" is detected

                # Send message to the chat model
                if chat_session:
                    response = chat_session.send_message(f"{transcription}")
                    text_widget.insert(tk.END, "Response: " + response.text + "\n")
                    text_widget.update()
                    engine.say(response.text)
                    engine.runAndWait()
                else:
                    text_widget.insert(tk.END, "Chat session is not initialized.\n")
                    text_widget.update()

            except sr.RequestError:
                text_widget.insert(tk.END, "API was unreachable or unresponsive\n")
                text_widget.update()
            except sr.UnknownValueError:
                text_widget.insert(tk.END, "Unable to recognize speech\n")
                text_widget.update()
            except Exception as e:
                text_widget.insert(tk.END, f"An error occurred: {e}\n")
                text_widget.update()

# Capture and display webcam feed with smooth frame updates
def update_webcam():
    global cap, photo
    ret, frame = cap.read()
    if ret:
        # Convert the image from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = image.resize((400, 300), Image.Resampling.LANCZOS)  # Smooth resizing
        photo = ImageTk.PhotoImage(image)
        webcam_label.config(image=photo)
        webcam_label.image = photo  # Keep a reference to avoid garbage collection

    # Schedule the next frame update
    if running:
        root.after(10, update_webcam)  # Update every 10ms for smoother display

def start_webcam():
    global cap, running
    cap = cv2.VideoCapture(0)
    running = True
    update_webcam()  # Start the webcam update loop

def stop_webcam():
    global cap, running
    running = False
    cap.release()
    cv2.destroyAllWindows()

# GUI functions
def upload_resume():
    def _upload_resume():
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:
            global text
            text = extract_text_from_file(file_path)

            if text:
                text_widget.insert(tk.END, "Text extracted successfully.\n")
                text_widget.update()
                start_button.config(state=tk.NORMAL)
                global chat_session
                global round_type
                round_type = round_selection.get()


            else:
                messagebox.showerror("Error", "Failed to extract text from the file.")
        else:
            messagebox.showwarning("Warning", "No file selected.")

    threading.Thread(target=_upload_resume).start()

def start_interview():
    def _start_interview():
        chat_session = start_chat_session(text, round_type, company_name=None, user_role=None)
        if not chat_session:
            text_widget.insert(tk.END, "Failed to start chat session.\n")
            text_widget.update()
        if chat_session:
            text_widget.insert(tk.END, "Starting the interview...\n")
            text_widget.update()
            initial_response = chat_session.send_message("Let's begin.")
            text_widget.insert(tk.END, "Response: " + initial_response.text + "\n")
            text_widget.update()
            engine.say(initial_response.text)
            engine.runAndWait()
            recognize_speech_from_mic(chat_session, text_widget)
        else:
            messagebox.showwarning("Warning", "Please upload a resume first.")

    threading.Thread(target=_start_interview).start()

# Create the main window
root = tk.Tk()
root.title("AceInterview")

# Define custom fonts and colors
title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
button_font = tkfont.Font(family="Helvetica", size=14)
highlight_color = "#4CAF50"
button_hover_color = "#45a049"

# Left Frame (for resume upload and interview controls)
left_frame = tk.Frame(root, width=600, height=600, bg="#f0f0f0", borderwidth=2, relief="solid")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Title Label
title_label = tk.Label(left_frame, text="AceInterview", font=title_font, bg="#f0f0f0")
title_label.pack(pady=20)

upload_button = tk.Button(left_frame, text="Upload Resume", command=upload_resume, font=button_font, bg=highlight_color, fg="white", activebackground=button_hover_color)
upload_button.pack(pady=10, padx=10, fill=tk.X)

round_selection = ttk.Combobox(left_frame, values=["HR", "TR", "MR"], state="readonly")
round_selection.pack(pady=10, padx=10, fill=tk.X)
round_selection.set("Select Interview Round")

company_selection = ttk.Combobox(left_frame, values=["TCS", "Amazon", "Accenture", "Not Specific"], state="readonly")
company_selection.pack(pady=10, padx=10, fill=tk.X)
company_selection.set("Select Specific Company")

role_entry = tk.Entry(left_frame, font=button_font)
role_entry.pack(pady=10, padx=10, fill=tk.X)
role_entry.insert(0, "Enter Role or Leave Empty")

start_button = tk.Button(left_frame, text="Start Interview", command=start_interview, font=button_font, bg=highlight_color, fg="white", activebackground=button_hover_color, state=tk.DISABLED)
start_button.pack(pady=10, padx=10, fill=tk.X)

text_widget = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=20, width=70, font=button_font)
text_widget.pack(pady=10, padx=10)

# Right Frame (for webcam feed)
right_frame = tk.Frame(root, width=400, height=300, bg="#e0e0e0", borderwidth=2, relief="solid")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

right_label = tk.Label(
    right_frame,
    text="This webcam preview allows the interviewee to \n improve their facial expressions during the interview.",
    font=("Helvetica", 12),
    bg="#f0f0f0"
)
right_label.pack(pady=20)


webcam_label = tk.Label(right_frame, bg="#e0e0e0", borderwidth=2, relief="solid")
webcam_label.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Start webcam feed
start_webcam()

# Run the Tkinter event loop
root.mainloop()

# Stop the webcam feed when the program exits
stop_webcam()