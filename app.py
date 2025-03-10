import streamlit as st
import random
import auth_functions
import google.generativeai as genai
from gtts import gTTS
import io
import tempfile
import re
from googletrans import Translator

# Configure API key
api_key = "AIzaSyCaUhhi440-KDR96yjf2CHTjnVNxOvjJBM"
genai.configure(api_key=api_key)

# Function to get a random joke
def get_joke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
    ]
    return random.choice(jokes)

# Function to generate a recipe
def generate_recipe(topic, word_count):
    try:
        st.write("🍽 Generating your recipe...")        
        st.write(f"🤖 While I work on your blog, here's a joke for you: \n\n {get_joke()}")

        chat_session = genai.GenerativeModel("gemini-1.5-flash").start_chat()

        prompt = f"Write a recipe blog on '{topic}' with {word_count} words."
        response = chat_session.send_message(prompt)

        st.success("✅ Your recipe is ready!")
        return clean_text_for_tts(response.text)
    
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None

# Function to clean text for text-to-speech conversion
def clean_text_for_tts(text):
    clean_text = re.sub(r'[^\w\s,.!?\'-]', '', text)
    return clean_text

# Function to generate speech
def generate_speech(text):
    cleaned_text = clean_text_for_tts(text)
    tts = gTTS(cleaned_text)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tts.save(tmp_file.name)
        
        with open(tmp_file.name, 'rb') as f:
            audio_stream = io.BytesIO(f.read())
    
    return audio_stream

# Function to translate recipe
def translate_recipe(recipe, target_language):
    translator = Translator()
    translated_text = translator.translate(recipe, dest=target_language).text
    return translated_text

# Main function
def main():
    # Initialize session state variables
    if "recipe" not in st.session_state:
        st.session_state.recipe = None
    if "translated_recipe" not in st.session_state:
        st.session_state.translated_recipe = None
    if "search_history" not in st.session_state:
        st.session_state.search_history = []

    if "user_info" not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])

        do_you_have_an_account = col2.selectbox(
            label='Do you have an account?', options=('Yes', 'No')
        )
        auth_form = col2.form(key='Authentication form', clear_on_submit=False)
        email = auth_form.text_input(label='Email')
        password = auth_form.text_input(label='Password', type='password')
        auth_notification = col2.empty()

        if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In', use_container_width=True, type='primary'):
            with auth_notification, st.spinner('Signing in'):
                auth_functions.sign_in(email, password)

        elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account', use_container_width=True, type='primary'):
            with auth_notification, st.spinner('Creating account'):
                auth_functions.create_account(email, password)

        if 'auth_success' in st.session_state:
            auth_notification.success(st.session_state.auth_success)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            auth_notification.warning(st.session_state.auth_warning)
            del st.session_state.auth_warning

    else:
        st.title("Flavour Fusion: AI-Driven Recipe Blogging 🍲🤖")
        st.header("Generate a Recipe 🍽️")

        # Display search history
        if st.session_state.search_history:
            st.subheader("Your Previous Searches:")
            for i, topic in enumerate(st.session_state.search_history, 1):
                st.write(f"{i}. {topic}")

        # User input fields
        topic = st.text_input("Enter your recipe topic:", placeholder="e.g., Vegan Chocolate Cake")
        word_count = st.number_input("Word count:", min_value=100, max_value=2000, step=100)

        # Generate recipe button
        if st.button("Generate Recipe", type='primary'):
            if topic and word_count:
                st.session_state.recipe = generate_recipe(topic, word_count)  # Store recipe
                st.session_state.translated_recipe = None  # Reset translation when generating a new recipe
                st.session_state.search_history.append(topic)  # Store search history
            else:
                st.warning("Please enter a topic and word count.")

        # Display recipe if available
        if st.session_state.recipe:
            st.text_area("Generated Recipe:", st.session_state.recipe, height=300, key="generated_recipe")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.download_button("Download Recipe", st.session_state.recipe, file_name=f"{topic}.txt")

            # Translation option
            translate = st.radio("Would you like to translate the recipe?", ("No", "Yes"))

            if translate == "Yes":

                language_options = {
                                    "French": "fr",
                                    "Spanish": "es",
                                    "German": "de",
                                    "Italian": "it",
                                    "Hindi": "hi",
                                    "Telugu": "te",
                                    "Chinese (Simplified)": "zh-cn",
                                    "Japanese": "ja",
                                    "Korean": "ko",
                                    "Portuguese": "pt",
                                    "Russian": "ru",
                                     "Arabic": "ar"
                                    }
                selected_language = st.selectbox("Select a language:", options=list(language_options.keys()), key=f"language_dropdown_{len(st.session_state)}")
                if selected_language:
                    target_language_code = language_options[selected_language]
                        # if not st.session_state.translated_recipe:  # Avoid re-translating unnecessarily
                    st.session_state.translated_recipe = translate_recipe(st.session_state.recipe, target_language_code)
                    st.session_state.last_translated_language = selected_language

                    st.text_area("Translated Recipe:", st.session_state.translated_recipe, height=300, key="translated_recipe")
                    audio_stream = generate_speech(st.session_state.translated_recipe)
                    st.audio(audio_stream, format="audio/mp3")
            else:
                audio_stream = generate_speech(st.session_state.recipe)
                st.audio(audio_stream, format="audio/mp3")

        st.button(label='Sign Out', on_click=auth_functions.sign_out, type='primary')

if __name__ == "__main__":
    main()