# utils/translator.py

from deep_translator import GoogleTranslator

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Bengali": "bn",
    "Marathi": "mr",
    "Telugu": "te",
    "Kannada": "kn",
}

def translate_text(text, target_lang_code):
    try:
        if target_lang_code == "en":
            return text  # No translation needed
            
        translated = GoogleTranslator(
            source='auto',
            target=target_lang_code
        ).translate(text)
        
        return translated
    
    except Exception as e:
        return text  # If translation fails, return original text