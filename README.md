# Flavour Fusion: AI-Driven Recipe Blogging 🍲🤖

Welcome to **Flavour Fusion**, an AI-powered recipe blogging platform that helps you generate, find, and translate recipes effortlessly! Whether you have specific ingredients or a topic in mind, our app can assist you with AI-generated recipes, jokes, and even text-to-speech conversion.

## 🚀 Features

### 🔹 User Authentication
- Sign in or create an account to access personalized features.
- Secure authentication using `auth_functions`.

### 🔹 Recipe Suggestions Based on Ingredients
- Enter a list of ingredients, and AI will suggest relevant recipes.
- Recipes are fetched using Google Gemini AI (`gemini-1.5-flash`).

### 🔹 AI-Generated Recipes
- Generate a full recipe blog based on a given topic and word count.
- Get a joke while the recipe is being generated for a fun experience.

### 🔹 Recipe Translation
- Translate recipes into multiple languages, including:
  - French 🇫🇷
  - Spanish 🇪🇸
  - German 🇩🇪
  - Hindi 🇮🇳
  - and more!

### 🔹 Text-to-Speech (TTS)
- Convert the generated or translated recipe into speech using `gTTS`.
- Listen to your recipe while cooking!

### 🔹 Download Recipe
- Save and download your recipe as a `.txt` file for future reference.

### 🔹 Dark Mode & Enhanced UI
- Beautiful and simple UI with a responsive layout.
- Styled using `st.markdown` to enhance user experience.

---

## 🛠 Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Streamlit
- Required dependencies (`pip install -r requirements.txt`)

### Clone the Repository
```bash
 git clone https://github.com/chavapardhakalyan/Flavour-Fusion-AI-Driven-Recipe-Blogging.git
 cd Flavour-Fusion-AI-Driven-Recipe-Blogging
```

### Install Dependencies
```bash
 pip install -r requirements.txt
```

### Run the Application
```bash
 streamlit run app.py
```

---

## 📌 Technologies Used
- **Streamlit** - For building the web interface.
- **Google Gemini AI** - For recipe generation.
- **gTTS** - For text-to-speech conversion.
- **Google Translate API** - For translating recipes.
- **SpeechRecognition** - For future voice input features.

---

## 📩 Contributing
We welcome contributions! Feel free to submit a pull request or open an issue for any improvements.

Happy Cooking! 🍽🔥

