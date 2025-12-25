import os
import requests
import re
import nltk
import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
from collections import Counter

# Create folders
os.makedirs("books_raw", exist_ok=True)
os.makedirs("books_clean", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

# List of books to process
books = [
    # --- 17th Century ---
    {"title": "Hamlet", "author": "William Shakespeare", "century": "17th",
     "url": "https://www.gutenberg.org/files/1524/1524-0.txt"},
    {"title": "Macbeth", "author": "William Shakespeare", "century": "17th",
     "url": "https://www.gutenberg.org/files/1533/1533-0.txt"},
    {"title": "Othello", "author": "William Shakespeare", "century": "17th",
     "url": "https://www.gutenberg.org/files/11231/11231-0.txt"},
    {"title": "King Lear", "author": "William Shakespeare", "century": "17th",
     "url": "https://www.gutenberg.org/files/1128/1128-0.txt"},
    {"title": "Paradise Lost", "author": "John Milton", "century": "17th",
     "url": "https://www.gutenberg.org/files/20/20-0.txt"},
    {"title": "Paradise Regained", "author": "John Milton", "century": "17th",
     "url": "https://www.gutenberg.org/files/58/58-0.txt"},
    {"title": "The Pilgrim's Progress", "author": "John Bunyan", "century": "17th",
     "url": "https://www.gutenberg.org/files/131/131-0.txt"},
    {"title": "Leviathan", "author": "Thomas Hobbes", "century": "17th",
     "url": "https://www.gutenberg.org/files/3207/3207-0.txt"},
    {"title": "Essays", "author": "Francis Bacon", "century": "17th",
     "url": "https://www.gutenberg.org/files/56466/56466-0.txt"},
    {"title": "The Duchess of Malfi", "author": "John Webster", "century": "17th",
     "url": "https://www.gutenberg.org/cache/epub/2232/pg2232.txt"},
    {"title": "Volpone; Or, The Fox", "author": "Ben Jonson", "century": "17th",
     "url": "https://www.gutenberg.org/cache/epub/4039/pg4039.txt"},
    {"title": "Religio Medici", "author": "Thomas Browne", "century": "17th",
     "url": "https://www.gutenberg.org/files/586/586-0.txt"},

    # --- 18th Century ---
    {"title": "Robinson Crusoe", "author": "Daniel Defoe", "century": "18th",
     "url": "https://www.gutenberg.org/files/521/521-0.txt"},
    {"title": "Moll Flanders", "author": "Daniel Defoe", "century": "18th",
     "url": "https://www.gutenberg.org/files/370/370-0.txt"},
    {"title": "Gulliver's Travels", "author": "Jonathan Swift", "century": "18th",
     "url": "https://www.gutenberg.org/files/829/829-0.txt"},
    {"title": "Candide", "author": "Voltaire", "century": "18th",
     "url": "https://www.gutenberg.org/cache/epub/19942/pg19942.txt"},
    {"title": "Pamela, or Virtue Rewarded", "author": "Samuel Richardson", "century": "18th",
     "url": "https://www.gutenberg.org/cache/epub/6124/pg6124.txt"},
    {"title": "Clarissa", "author": "Samuel Richardson", "century": "18th",
     "url": "https://www.gutenberg.org/files/12188/12188-0.txt"},
    {"title": "The Mysteries of Udolpho", "author": "Ann Radcliffe", "century": "18th",
     "url": "https://www.gutenberg.org/files/3268/3268-0.txt"},
    {"title": "The Castle of Otranto", "author": "Horace Walpole", "century": "18th",
     "url": "https://www.gutenberg.org/files/696/696-0.txt"},
    {"title": "Tom Jones", "author": "Henry Fielding", "century": "18th",
     "url": "https://www.gutenberg.org/files/6593/6593-0.txt"},
    {"title": "Tristram Shandy", "author": "Laurence Sterne", "century": "18th",
     "url": "https://www.gutenberg.org/files/1079/1079-0.txt"},
    {"title": "Fanny Hill", "author": "John Cleland", "century": "18th",
     "url": "https://www.gutenberg.org/files/25305/25305-0.txt"},
    {"title": "Rasselas", "author": "Samuel Johnson", "century": "18th",
     "url": "https://www.gutenberg.org/files/652/652-0.txt"},

    # --- 19th Century ---
    {"title": "Pride and Prejudice", "author": "Jane Austen", "century": "19th",
     "url": "https://www.gutenberg.org/files/1342/1342-0.txt"},
    {"title": "Sense and Sensibility", "author": "Jane Austen", "century": "19th",
     "url": "https://www.gutenberg.org/files/161/161-0.txt"},
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "century": "19th",
     "url": "https://www.gutenberg.org/files/1260/1260-0.txt"},
    {"title": "Wuthering Heights", "author": "Emily Brontë", "century": "19th",
     "url": "https://www.gutenberg.org/files/768/768-0.txt"},
    {"title": "Frankenstein", "author": "Mary Shelley", "century": "19th",
     "url": "https://www.gutenberg.org/files/84/84-0.txt"},
    {"title": "David Copperfield", "author": "Charles Dickens", "century": "19th",
     "url": "https://www.gutenberg.org/files/766/766-0.txt"},
    {"title": "Great Expectations", "author": "Charles Dickens", "century": "19th",
     "url": "https://www.gutenberg.org/files/1400/1400-0.txt"},
    {"title": "Tess of the D’Urbervilles", "author": "Thomas Hardy", "century": "19th",
     "url": "https://www.gutenberg.org/files/110/110-0.txt"},
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "century": "19th",
     "url": "https://www.gutenberg.org/files/174/174-0.txt"},
    {"title": "Dracula", "author": "Bram Stoker", "century": "19th",
     "url": "https://www.gutenberg.org/files/345/345-0.txt"},
    {"title": "The Scarlet Letter", "author": "Nathaniel Hawthorne", "century": "19th",
     "url": "https://www.gutenberg.org/files/33/33-0.txt"},
    {"title": "Les Misérables", "author": "Victor Hugo", "century": "19th",
     "url": "https://www.gutenberg.org/files/135/135-0.txt"},

    # --- 20th Century ---
    {"title": "The Metamorphosis", "author": "Franz Kafka", "century": "20th",
     "url": "https://www.gutenberg.org/files/5200/5200-0.txt"},
    {"title": "The Secret Garden", "author": "Frances Hodgson Burnett", "century": "20th",
     "url": "https://www.gutenberg.org/files/113/113-0.txt"},
    {"title": "The Call of the Wild", "author": "Jack London", "century": "20th",
     "url": "https://www.gutenberg.org/files/215/215-0.txt"},
    {"title": "White Fang", "author": "Jack London", "century": "20th",
     "url": "https://www.gutenberg.org/files/910/910-0.txt"},
    {"title": "My Ántonia", "author": "Willa Cather", "century": "20th",
     "url": "https://www.gutenberg.org/files/242/242-0.txt"},
    {"title": "Sons and Lovers", "author": "D. H. Lawrence", "century": "20th",
     "url": "https://www.gutenberg.org/files/217/217-0.txt"},
    {"title": "A Room with a View", "author": "E. M. Forster", "century": "20th",
     "url": "https://www.gutenberg.org/files/2641/2641-0.txt"},
    {"title": "Howards End", "author": "E. M. Forster", "century": "20th",
     "url": "https://www.gutenberg.org/files/2890/2890-0.txt"},
    {"title": "The Age of Innocence", "author": "Edith Wharton", "century": "20th",
     "url": "https://www.gutenberg.org/files/4217/4217-0.txt"},
    {"title": "Main Street", "author": "Sinclair Lewis", "century": "20th",
     "url": "https://www.gutenberg.org/files/543/543-0.txt"},
    {"title": "The Good Soldier", "author": "Ford Madox Ford", "century": "20th",
     "url": "https://www.gutenberg.org/cache/epub/2775/pg2775.txt"},
    {"title": "The Lodger", "author": "Marie Belloc Lowndes", "century": "20th",
     "url": "https://www.gutenberg.org/cache/epub/2014/pg2014.txt"},
]

# === 21st Century Books (from Wikipedia excerpts) ===
books_21st = [
    {"title": "The Kite Runner", "author": "Khaled Hosseini"},
    {"title": "The Book Thief", "author": "Markus Zusak"},
    {"title": "Life of Pi", "author": "Yann Martel"},
    {"title": "A Thousand Splendid Suns", "author": "Khaled Hosseini"},
    {"title": "Never Let Me Go", "author": "Kazuo Ishiguro"},
    {"title": "The Road", "author": "Cormac McCarthy"},
    {"title": "Normal People", "author": "Sally Rooney"},
    {"title": "The Night Circus", "author": "Erin Morgenstern"},
    {"title": "The Testaments", "author": "Margaret Atwood"},
    {"title": "Shantaram", "author": "Gregory David Roberts"},
    {"title": "On Earth We're Briefly Gorgeous", "author": "Ocean Vuong"},
    {"title": "Small Things Like These", "author": "Claire Keegan"},
]

# === Functions ===
def download_book(book):
    try:
        r = requests.get(book["url"])
        if r.status_code == 200:
            path = f"books_raw/{book['title']}.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"✅ {book['title']} downloaded")
            return path
        else:
            print(f"❌ Failed: {book['title']}")
            return None
    except:
        print(f"⚠️ Error downloading {book['title']}")
        return None

def clean_book(file_path, title):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    start, end = 0, len(lines)
    for i, line in enumerate(lines):
        if "*** START" in line:
            start = i + 1
        if "*** END" in line:
            end = i
            break
    cleaned = ''.join(lines[start:end])
    with open(f"books_clean/{title}_clean.txt", "w", encoding="utf-8") as f:
        f.write(cleaned)
    return cleaned

def analyze_text(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    words = re.findall(r'\b\w+\b', text.lower())
    filtered = [w for w in words if w not in stop_words]
    word_count = len(words)
    top_words = [w for w, _ in Counter(filtered).most_common(5)]
    return sentiment, subjectivity, word_count, top_words

# === RUN ===
summary = []

# 📕 Process Gutenberg books (17th–20th)
for book in books:
    raw = download_book(book)
    if raw:
        clean = clean_book(raw, book["title"])
        s, sub, wc, top = analyze_text(clean)
        summary.append({
            "Title": book["title"],
            "Author": book["author"],
            "Century": book["century"],
            "Sentiment": s,
            "Subjectivity": sub,
            "Word Count": wc,
            "Top Words": ', '.join(top)
        })

# 📘 Process 21st-century excerpts
for book in books_21st:
    excerpt_path = f"books_raw/{book['title'].replace(' ', '_')}_excerpt.txt"
    if os.path.exists(excerpt_path):
        with open(excerpt_path, "r", encoding="utf-8") as f:
            text = f.read()
        s, sub, wc, top = analyze_text(text)
        summary.append({
            "Title": book["title"],
            "Author": book["author"],
            "Century": "21st",
            "Sentiment": s,
            "Subjectivity": sub,
            "Word Count": wc,
            "Top Words": ', '.join(top)
        })
        print(f"📊 Analyzed: {book['title']}")
    else:
        print(f"⚠️ Excerpt missing: {book['title']}")

# === Export CSV ===
df = pd.DataFrame(summary)
df.to_csv("data/literature_summary.csv", index=False)
print("📁 literature_summary.csv created successfully!")