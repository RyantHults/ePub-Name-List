import os
import ebooklib
from ebooklib import epub
import spacy
from bs4 import BeautifulSoup
from collections import Counter

# Load spaCy English model
nlp = spacy.load('<model_name>')

def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text(separator=' ', strip=True) + " "
    return text

def get_common_words(text):
    doc = nlp(text)
    # Create a counter for words that:
    # 1. Don't contain uppercase letters
    # 2. Aren't punctuation or whitespace
    # 3. Aren't stop words (common words like 'the', 'is', 'at')
    words = Counter(
        token.text.lower() for token in doc
        if (
            token.text.islower() and  # only lowercase words
            token.is_alpha and        # only alphabetic characters
            len(token.text) > 3       # more than 2 characters
        )
    )
    # Get the 10 most common words
    return words.most_common(100)

def main():
    folder = "books-to-read"
    for filename in os.listdir(folder):
        if filename.lower().endswith('.epub'):
            epub_path = os.path.join(folder, filename)
            print(f"Processing: {filename}")
            text = extract_text_from_epub(epub_path)
            common_words = get_common_words(text)
            
            print("\nTop 100 most common words:")
            with open("common_words.txt", "w", encoding="utf-8") as f:
                for word, count in common_words:
                    print(f"{word}: {count}")
                    f.write(f"{word}\n")

if __name__ == "__main__":
    main()
