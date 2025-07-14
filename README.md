# ePub-Name-List
This is a python script that generates a list of all unique names from all *.epub books in the `books-to-read` folder using [SpaCy language models](https://spacy.io/models/en/).  Note, this is just a rough first-pass and definintely still requires some manual cleanup. 

## How to run
1. install requirements
```
pip install -r requirements.txt
```
2. install the [SpaCy language model](https://spacy.io/models/en/) you'd like to use. for example:
```
python -m spacy download en_core_web_lg
```
3. update the name of the model in `get_common_words.py` to match the name of the model you downloaded in step 2
```
nlp = spacy.load('en_core_web_lg')
```
4. place all books you'd like to analyze in the `books-to-read` folder. They must be in epub format.
5. run the script. 
```
python.exe extract_named_characters.py
```
This will generate a file called `named_characters.txt` in the current working directory
