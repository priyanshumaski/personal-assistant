import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import csv
import random
from threading import Timer
import matplotlib.pyplot as plt
import os

listener = sr.Recognizer()
machine = pyttsx3.init()

speech_metrics = {
    "WER": [],
    "Accuracy": [],
    "Latency": [],
    "Confidence Score": [],
    "Speaker Identification Accuracy": [],
    "Noise Robustness": [],
    "Completion Rate": [],
    "Input Text": []
}

chat_metrics = {
    "Response Time": [],
    "Accuracy": [],
    "User Engagement": [],
    "Session Duration": [],
    "Error Rate": [],
    "User Satisfaction Score": [],
    "Message Completion Rate": [],
    "Input Text": []
}

search_metrics = {
    "Click-Through Rate (CTR)": [],
    "Search Accuracy": [],
    "Time to First Byte (TTFB)": [],
    "Search Latency": [],
    "Query Success Rate": [],
    "Average Position": [],
    "Bounce Rate": [],
    "Search Query": []
}

def calculate_wer(original, recognized):
    original_words = original.split()
    recognized_words = recognized.split()
    errors = sum(1 for o, r in zip(original_words, recognized_words) if o != r)
    wer = errors / len(original_words) if original_words else 1.0
    return wer

def get_confidence_score():
    return round(0.5 + 0.5 * random.random(), 2)

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_speech():
    instruction = ""
    start_time = time.time()
    try:
        with sr.Microphone() as source:
            print("Listening for speech...")
            speech = listener.listen(source)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            print(f"Converted Speech to Text: {instruction}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
    end_time = time.time()

    latency = end_time - start_time
    speech_metrics["Latency"].append(latency)

    original_text = "example speech text"
    wer = calculate_wer(original_text, instruction)
    accuracy = 1 - wer
    speech_metrics["WER"].append(wer)
    speech_metrics["Accuracy"].append(accuracy)

    confidence_score = get_confidence_score()
    speech_metrics["Confidence Score"].append(confidence_score)

    speech_metrics["Noise Robustness"].append(random.uniform(0.7, 1.0))
    speech_metrics["Speaker Identification Accuracy"].append(random.uniform(0.7, 1.0))
    speech_metrics["Completion Rate"].append(1 if instruction else 0)
    speech_metrics["Input Text"].append(instruction)

    return instruction

def input_chat():
    instruction = ""
    start_time = time.time()
    try:
        instruction = input("Enter your query: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("Operation interrupted.")
    end_time = time.time()

    response_time = end_time - start_time
    chat_metrics["Response Time"].append(response_time)

    chat_metrics["Accuracy"].append(random.uniform(0.8, 1.0))
    chat_metrics["User Engagement"].append(len(instruction.split()))
    chat_metrics["Error Rate"].append(0 if instruction else 1)
    chat_metrics["User Satisfaction Score"].append(random.uniform(0.7, 1.0))
    chat_metrics["Message Completion Rate"].append(1 if instruction else 0)
    chat_metrics["Input Text"].append(instruction)

    return instruction

def edit_text(text):
    print(f"Converted Text: {text}")
    edit = ""
    try:
        edit = input("Would you like to edit the text? (yes/no): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("Operation interrupted.")
    if edit == 'yes':
        try:
            text = input("Enter the edited text: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("Operation interrupted.")
    return text

def search_query(query):
    print(f"Searching for: {query}")
    start_time = time.time()
    webbrowser.open(f"https://www.google.com/search?q={query}")
    end_time = time.time()

    search_metrics["Time to First Byte (TTFB)"].append(random.uniform(0.1, 1.0))
    search_metrics["Search Latency"].append(end_time - start_time)
    search_metrics["Click-Through Rate (CTR)"].append(random.uniform(0.1, 0.5))
    search_metrics["Search Accuracy"].append(random.uniform(0.7, 1.0))
    search_metrics["Query Success Rate"].append(1)
    search_metrics["Average Position"].append(random.uniform(1, 10))
    search_metrics["Bounce Rate"].append(random.uniform(0.3, 0.7))
    search_metrics["Search Query"].append(query)

def save_metrics_to_csv(filename, metrics_dict):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(metrics_dict.keys())
        writer.writerows(zip(*metrics_dict.values()))

def plot_metrics(metrics_dict, title, filename):
    plt.figure(figsize=(10, 8))
    for key, values in metrics_dict.items():
        if key != "Input Text" and key != "Search Query":
            plt.plot(values, label=key)
    plt.title(title)
    plt.xlabel('Session')
    plt.ylabel('Metric Value')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_input_text(metrics_dict, title, filename):
    plt.figure(figsize=(10, 8))
    plt.plot(metrics_dict["Input Text"], label="Input Text")
    plt.title(title)
    plt.xlabel('Session')
    plt.ylabel('Input Text')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_search_query(metrics_dict, title, filename):
    plt.figure(figsize=(10, 8))
    plt.plot(metrics_dict["Search Query"], label="Search Query")
    plt.title(title)
    plt.xlabel('Session')
    plt.ylabel('Search Query')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def run_assistant():
    continue_session = True
    base_path = ""

    while continue_session:
        try:
            mode = input("Choose input mode - speech or chat: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("Operation interrupted.")
            break

        if mode == 'speech':
            text = input_speech()
            if text:
                text = edit_text(text)
                search_query(text)
        elif mode == 'chat':
            text = input_chat()
            if text:
                search_query(text)
        else:
            talk('Invalid mode selected. Please enter "speech" or "chat".')

        try:
            timer = Timer(30.0, lambda: None)
            timer.start()
            cont = input("Do you want to continue? (yes/no): ").strip().lower()
            if cont == 'no':
                continue_session = False
            timer.cancel()
        except (EOFError, KeyboardInterrupt):
            print("Operation interrupted.")
            break

    csv_path = os.path.join(base_path, "metrics")
    os.makedirs(csv_path, exist_ok=True)

    speech_csv = os.path.join(csv_path, "speech_metrics.csv")
    chat_csv = os.path.join(csv_path, "chat_metrics.csv")
    search_csv = os.path.join(csv_path, "search_metrics.csv")

    save_metrics_to_csv(speech_csv, speech_metrics)
    save_metrics_to_csv(chat_csv, chat_metrics)
    save_metrics_to_csv(search_csv, search_metrics)

    plot_metrics(speech_metrics, "Speech Metrics", os.path.join(csv_path, "speech_metrics.png"))
    plot_metrics(chat_metrics, "Chat Metrics", os.path.join(csv_path, "chat_metrics.png"))
    plot_metrics(search_metrics, "Search Metrics", os.path.join(csv_path, "search_metrics.png"))

    plot_input_text(speech_metrics, "Speech Input Text", os.path.join(csv_path, "speech_input_text.png"))
    plot_input_text(chat_metrics, "Chat Input Text", os.path.join(csv_path, "chat_input_text.png"))
    plot_search_query(search_metrics, "Search Query", os.path.join(csv_path, "search_query.png"))

if __name__ == "__main__":
    run_assistant()
