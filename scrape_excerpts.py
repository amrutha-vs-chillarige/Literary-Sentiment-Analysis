import requests
from bs4 import BeautifulSoup
import os

# Create folder for saving text files
os.makedirs("books_raw", exist_ok=True)

# List of 12 top 21st-century books and their Wikipedia URLs
books_21st = [
    {
        "title": "The Kite Runner",
        "author": "Khaled Hosseini",
        "url": "https://en.wikipedia.org/wiki/The_Kite_Runner"
    },
    {
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "url": "https://en.wikipedia.org/wiki/The_Book_Thief"
    },
    {
        "title": "Life of Pi",
        "author": "Yann Martel",
        "url": "https://en.wikipedia.org/wiki/Life_of_Pi"
    },
    {
        "title": "A Thousand Splendid Suns",
        "author": "Khaled Hosseini",
        "url": "https://en.wikipedia.org/wiki/A_Thousand_Splendid_Suns"
    },
    {
        "title": "Never Let Me Go",
        "author": "Kazuo Ishiguro",
        "url": "https://en.wikipedia.org/wiki/Never_Let_Me_Go_(novel)"
    },
    {
        "title": "The Road",
        "author": "Cormac McCarthy",
        "url": "https://en.wikipedia.org/wiki/The_Road"
    },
    {
        "title": "Normal People",
        "author": "Sally Rooney",
        "url": "https://en.wikipedia.org/wiki/Normal_People"
    },
    {
        "title": "The Night Circus",
        "author": "Erin Morgenstern",
        "url": "https://en.wikipedia.org/wiki/The_Night_Circus"
    },
    {
        "title": "The Testaments",
        "author": "Margaret Atwood",
        "url": "https://en.wikipedia.org/wiki/The_Testaments"
    },
    {
        "title": "Shantaram",
        "author": "Gregory David Roberts",
        "url": "https://en.wikipedia.org/wiki/Shantaram_(novel)"
    },
    {
        "title": "On Earth We're Briefly Gorgeous",
        "author": "Ocean Vuong",
        "url": "https://en.wikipedia.org/wiki/On_Earth_We%27re_Briefly_Gorgeous"
    },
    {
        "title": "Small Things Like These",
        "author": "Claire Keegan",
        "url": "https://en.wikipedia.org/wiki/Small_Things_Like_These"
    }
]

def scrape_plot(book):
    response = requests.get(book["url"])
    if response.status_code != 200:
        print(f"❌ Failed to fetch {book['title']}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Try multiple possible section IDs
    plot_heading = (
        soup.find(id="Plot") or
        soup.find(id="Synopsis") or
        soup.find(id="Summary") or
        soup.find(id="Plot_summary") or
        soup.find(id="Premise")
    )

    if not plot_heading:
        print(f"⚠️ Plot/Synopsis not found for {book['title']}")
        return

    plot_text = ""
    for tag in plot_heading.find_all_next():
        if tag.name == "h2":
            break  # Stop at the next major section
        if tag.name == "p":
            plot_text += tag.get_text(separator=" ", strip=True) + "\n"

    if plot_text.strip():
        filename = f"books_raw/{book['title'].replace(' ', '_')}_excerpt.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(plot_text)
        print(f"✅ Saved plot for {book['title']}")
    else:
        print(f"⚠️ No plot text found for {book['title']}")

# Run the scraper
for book in books_21st:
    scrape_plot(book)
