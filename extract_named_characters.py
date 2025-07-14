import os
import ebooklib
from ebooklib import epub
import spacy
from bs4 import BeautifulSoup
from collections import Counter

# Load spaCy English model
nlp = spacy.load('en_core_web_lg')

def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text(separator=' ', strip=True) + " "
    return text

def get_named_characters(text):
    doc = nlp(text)

    def get_common_words(doc):
        # Create a counter for words that:
        # 1. Don't contain uppercase letters
        # 2. Aren't punctuation or whitespace
        # 3. Aren't stop words (common words like 'the', 'is', 'at')
        words = Counter(
            token for token in doc
            if (
                token.text.islower() and  # only lowercase words
                token.is_alpha and        # only alphabetic characters
                token.pos_ == 'NOUN' and  # only nouns
                len(token.text) > 2       # more than 2 characters
            )
        )
        # Get the most common words
        return [word for word, _ in words.most_common(100)]
    
    common_words = get_common_words(doc)

    # Only include names withat least two words (full names), each starting with a capital letter
    def is_full_name_with_capitals(name):
        parts = name.split()
        return (
            len(parts) > 1 and
            all(part[0].isupper() for part in parts[:2])
        )
    def has_number(name):
        return any(char.isdigit() for char in name)
    
    def does_not_contain_punctuation(name):
        return all(char.isalpha() or char.isspace() for char in name)
    
    def name_is_not_common_word(name):
        return name.lower() not in common_words
    
    return set(
        entry.text for entry in doc.ents
        if entry.label_ == 'PERSON'
        and is_full_name_with_capitals(entry.text)
        and not has_number(entry.text)
        and does_not_contain_punctuation(entry.text)
        and name_is_not_common_word(entry.text)
    )

def main():
    folder = "books-to-read"
    unique_characters = set()
    for filename in os.listdir(folder):
        if filename.lower().endswith('.epub'):
            epub_path = os.path.join(folder, filename)
            print(f"Processing: {filename}")
            text = extract_text_from_epub(epub_path)
            characters = get_named_characters(text)
            unique_characters.update(characters)
    # Remove names that are a subset of another name
    filtered_characters = set()
    for name in unique_characters:
        if not any(
            other != name and name in other
            for other in unique_characters
        ):
            filtered_characters.add(name)
    with open("named_characters.txt", "w", encoding="utf-8") as f:
        for name in sorted(filtered_characters):
            f.write(name + "\n")
    print(f"Found {len(filtered_characters)} unique named characters. See named_characters.txt.")

if __name__ == "__main__":
    main()
