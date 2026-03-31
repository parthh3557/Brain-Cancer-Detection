🧠 Brain Cancer Classifier

This is a web application that uses a PyTorch model to classify brain tumor types from uploaded MRI images. It is built using Flask for the backend and HTML/JavaScript for the frontend.

⚠️ Important: Project Structure

Before you begin, your project files must be organized in this structure. Flask requires the index.html file to be in a folder named templates.

/your-project-directory
|
|-- /models
|   |-- BrainCancerModel1_ver2.pth
|
|-- /templates
|   |-- index.html
|
|-- app.py
|-- requirements.txt
|-- README.md


🛠️ Setup and Installation

Follow these steps to set up your environment and install the necessary packages.

1. Create requirements.txt

In your main project directory (the same folder as app.py), create a file named requirements.txt and paste the following lines into it:

flask
torch
torchvision
Pillow


(I have already generated this file for you in this chat.)

2. Create and Activate a Virtual Environment (venv)

Open a terminal or command prompt and navigate to your main project directory.

a. Create the venv:
Run the following command to create a virtual environment folder named venv.

python -m venv venv


b. Activate the venv:
You must activate the environment every time you work on the project.

On Windows (Command Prompt):

venv\Scripts\activate


On macOS / Linux (Bash/Zsh):

source venv/bin/activate


Note: When activated, your terminal prompt will usually show (venv) at the beginning.

3. Install Required Packages

With your virtual environment active, run the following command to install all the packages from your requirements.txt file:

pip install -r requirements.txt


🚀 Running the Application

Make sure your virtual environment is active.

Ensure you are in your main project directory.

Run the app.py file to start the Flask server:

python app.py


Open your web browser and go to the following address:

http://127.0.0.1:5000/

You should now see your web application. You can upload an image and click "Predict" to get a classification.

🛑 Stopping the Application

To stop the Flask server, go back to your terminal and press Ctrl + C.

To deactivate the virtual environment when you are finished, simply type:

deactivate
---------------------------------------------------------

Here is a professional `README.md` file for your project. You can just copy and paste the text below into a new file named `README.md` in your project's main directory.

-----

```markdown
# 🧠 Brain Tumor Classifier Web App

This project is a complete web application for classifying brain tumors from MRI images. It uses a Python Flask backend to serve a deep learning model (a ResNet-50 variant) and an interactive HTML/JavaScript frontend to handle image uploads and display results.

The app also features a **Gemini API integration**: after a classification is made, the user can click a button to get a simple, AI-powered summary of the predicted tumor type.

## ✨ Features

* **PyTorch Backend:** A Flask server loads a pre-trained PyTorch model for fast and accurate predictions.
* **Interactive Frontend:** A modern, responsive UI allows users to upload images and see a preview.
* **Drag-and-Drop:** Supports (or simulates) drag-and-drop for file uploads.
* **Real-time Classification:** Get predictions from the local model in seconds.
* **Gemini API Integration:** A "Learn More" button appears after prediction, calling the Google Gemini API to provide users with more context about the result.

## 🏛️ Project Architecture

This application uses a classic client-server architecture.

### 1. Backend (Server-Side)

* **Framework:** **Flask** (`app.py`)
* **Language:** Python
* **Core Logic:**
    * **`/` Route:** Serves the main `test.html` file to the user's browser.
    * **`/predict` Route (API):** A `POST` endpoint that accepts an image file. It processes the image, feeds it to the loaded PyTorch model (`BrainNet50`), and returns a JSON response with the `prediction` and `confidence`.
    * **Model:** The `BrainNet50` model (defined in `app.py`) is loaded from the `models/` folder once at startup for high performance.

### 2. Frontend (Client-Side)

* **File:** `templates/test.html`
* **Technologies:** HTML, CSS, JavaScript
* **Core Logic:**
    * **Local Model Prediction:** Uses the `fetch` API to send the image to its *own backend* (the `/predict` endpoint). It then parses the JSON response and displays the result.
    * **Gemini API:** Uses the `fetch` API to send a prompt *directly* to the **Google Gemini API** (an external server) to get a summary of the tumor. This entire flow is handled in the browser and does **not** involve the Flask backend.

## 📁 Project Structure

```

/your-project-directory
|
|-- /models
|   |-- BrainCancerModel1\_ver2.pth  (Your pre-trained model)
|
|-- /templates
|   |-- index.html                   (The main HTML/CSS/JS frontend)
|
|-- app.py                          (The Flask backend server)
|-- requirements.txt                (List of Python dependencies)
|-- README.md                       (This file)

````

## 🛠️ Setup & Installation

### Prerequisites

* Python 3.7+
* `pip` (Python package installer)



### 1\. Create a Virtual Environment

It's highly recommended to use a virtual environment.

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 2\. Install Dependencies

This project requires Flask, PyTorch, Torchvision, and Pillow.

```bash
pip install -r requirements.txt
```

*(If you don't have a `requirements.txt` file, create one and add the following lines, then run `pip install -r requirements.txt`)*

**requirements.txt:**

```
flask
torch
torchvision
Pillow
```

### 3\. Add Your Gemini API Key

To use the "✨ Learn More" feature, you must add your own **free** Google Gemini API key.

1.  Get your key from [Google AI Studio](https://aistudio.google.com).
2.  Open the `templates/test.html` file.
3.  Find the JavaScript section near the bottom (inside the `<script>` tag).
4.  Locate this line (around line 300):
    ```javascript
    const apiKey = ""; 
    ```
5.  Paste your API key inside the quotes:
    ```javascript
    const apiKey = "YOUR_API_KEY_GOES_HERE";
    ```
6.  Save the file.

## 🚀 How to Run the App

1.  Make sure your virtual environment is active.

2.  Run the Flask application:

    ```bash
    python app.py
    ```

3.  Open your web browser and go to:

    **`http://127.0.0.1:5000/`**

4.  Upload an MRI image and click "Predict"\!

