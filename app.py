import streamlit as st
import random
import auth_functions
import google.generativeai as genai
from gtts import gTTS
import io
import tempfile
import re
from googletrans import Translator
import speech_recognition as sr

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

# Function to query Gemini AI for recipe suggestions
def query_gemini_for_recipes(ingredients):
    prompt = f"Suggest recipes that can be made with the following ingredients: {', '.join(ingredients)}. Provide a list of recipe names."
    chat_session = genai.GenerativeModel("gemini-1.5-flash").start_chat()
    response = chat_session.send_message(prompt)
    recipes = response.text.split("\n")
    formatted_recipes = [f" {re.sub(r'[🍽*]', '', recipe).strip()}" for recipe in recipes if recipe.strip()]
    return formatted_recipes


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
    translated = translator.translate(recipe, dest=target_language)
    return translated.text

# Main function
def main():
    if "user_info" not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])
        do_you_have_an_account = col2.selectbox('Do you have an account?', ('Yes', 'No'))
        auth_form = col2.form(key='Authentication form', clear_on_submit=False)
        email = auth_form.text_input(label='Email')
        password = auth_form.text_input(label='Password', type='password')
        auth_notification = col2.empty()

        if do_you_have_an_account == 'Yes' and auth_form.form_submit_button('Sign In', use_container_width=True, type='primary'):
            with auth_notification, st.spinner('Signing in'):
                auth_functions.sign_in(email, password)
        elif do_you_have_an_account == 'No' and auth_form.form_submit_button('Create Account', use_container_width=True, type='primary'):
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
        st.header("Find or Generate Recipes 🍽")
        
        ingredients_input = st.text_area("Enter the ingredients you have (comma-separated):", placeholder="e.g., egg, milk, cheese")
        topic = st.text_input("Or enter your recipe topic:", placeholder="e.g., Vegan Chocolate Cake")
        word_count = st.number_input("Word count (if generating recipe):", min_value=100, max_value=2000, step=100)
        
        if st.button("Find or Generate Recipe", type='primary'):
            if ingredients_input:
                ingredients_list = [ingredient.strip().lower() for ingredient in ingredients_input.split(",")]
                matching_recipes = query_gemini_for_recipes(ingredients_list)
                if matching_recipes:
                    st.success("Here are some recipes you can make:")
                    for recipe in matching_recipes:
                        st.write(f"🍽 {recipe}")
                else:
                    st.warning("No matching recipes found. Try adding more ingredients!")
            elif topic and word_count:
                st.session_state.recipe = generate_recipe(topic, word_count)
                st.session_state.translated_recipe = None
                #st.session_state.search_history.append(topic)
            else:
                st.warning("Please enter either ingredients or a recipe topic with word count.")

        if 'recipe' in st.session_state and st.session_state.recipe:
            st.text_area("Generated Recipe:", st.session_state.recipe, height=300)
            col1, col2 = st.columns([2, 1])
            with col1:
                st.download_button("Download Recipe", st.session_state.recipe, file_name=f"{topic}.txt")

            st.audio(generate_speech(st.session_state.recipe), format="audio/mp3")
            translate = st.radio("Would you like to translate the recipe?", ("No", "Yes"))

            if translate == "Yes":
                language_options = {"French": "fr", "Spanish": "es", "German": "de", "Italian": "it", "Telugu": "te", "Hindi": "hi", "Chinese": "zh-cn", "Japanese": "ja", "Korean": "ko", "Portuguese": "pt", "Russian": "ru", "Arabic": "ar"}
                selected_language = st.selectbox("Select a language:", options=list(language_options.keys()))
                if selected_language:
                    target_language_code = language_options[selected_language]
                    translated_recipe = translate_recipe(st.session_state.recipe, target_language_code)
                    st.text_area("Translated Recipe:", translated_recipe, height=300)
                    audio_stream = generate_speech(translated_recipe)
                    st.audio(audio_stream, format="audio/mp3")

        st.button('Sign Out', on_click=auth_functions.sign_out, type='primary')

if __name__ == "__main__":
    main()