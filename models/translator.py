import json
import os

class Translator:
    def __init__(self, language="en", locales_dir="locales"):
        self.language = language
        self.locales_dir = locales_dir
        self.strings = self.load_language(language)

    def load_language(self, lang_code):
        try:
            path = os.path.join(self.locales_dir, f"{lang_code}.json")
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def set_language(self, lang_code):
        self.language = lang_code
        self.strings = self.load_language(lang_code)

    def translate(self, key):
        return self.strings.get(key, f"[{key}]")