# Literary Landscape: Sentiment, Language, and Style Across Centuries

This project studies how emotional tone, sentiment polarity, and language style in literature have evolved from the 17th century to the 21st century.  
It combines Python-based text analysis with interactive Power BI dashboards to uncover long-term patterns in literary writing.

The goal of the project is not literary criticism, but data-driven comparison of how tone, structure, and expression change over time.



## Project Objectives

- Compare sentiment and subjectivity across literary centuries  
- Study changes in book length and language complexity  
- Analyze relationships between emotional tone and structure  
- Present findings through a clear, story-driven dashboard  



## Tools and Technologies

- Python  
- pandas, nltk, textblob  
- requests, BeautifulSoup  
- Power BI  



## Data Collection and Preparation

### Text Sources
- 17th to 20th century works were downloaded from Project Gutenberg  
- 21st century works were collected by scraping plot and summary excerpts from Wikipedia  

### Cleaning and Processing
- Removed headers, footers, and metadata from raw texts  
- Standardized text for analysis  
- Stored cleaned versions separately for reuse  

### Text Analysis
For each book, the following features were calculated:
- Sentiment polarity  
- Subjectivity  
- Word count  
- Lexical richness  
- Most frequent words  

The final dataset was exported as a single CSV file for visualization.


#### Raw and cleaned text files are not included in this repository due to size constraints.
#### All analysis is reproducible using the provided scripts and source links.


## Dashboard Overview

The Power BI dashboard is structured as a four-page narrative.

### Page 1: Overview
- High-level KPIs such as total books, average sentiment, subjectivity, and word count  
- Century-wise sentiment and subjectivity trends  
- Establishes overall patterns before deeper analysis  

### Page 2: Emotional Tone Trends
- Scatter plot showing sentiment versus subjectivity by century  
- Sentiment polarity distribution across eras  
- Highlights emotional restraint and tonal shifts over time  

### Page 3: Language and Style
- Word count distribution by century  
- Lexical richness comparison  
- Shows transition from longer, structured texts to shorter but more flexible language  

### Page 4: Comparative Insights
- Relationship between book length and emotional tone  
- Sentiment patterns across word count bands  
- Integrates emotional and structural insights across centuries  



## Project Structure

literature_project/
│
├── books_raw/  
├── books_clean/  
├── data/  
├── notebooks/  
├── dashboard/  
│
├── scrape_excerpts.py  
├── download_clean_analyse.py  
├── requirements.txt  
└── README.md  



## Key Insights

- Literary sentiment clusters around neutral across all centuries  
- Earlier works tend to be longer and more structurally dense  
- Modern literature favors concision with higher lexical flexibility  
- Emotional tone shows weak correlation with book length, suggesting stylistic choice  



## How to Run the Project

1. Install dependencies  
   pip install -r requirements.txt  

2. Run the scripts  
   python scrape_excerpts.py  
   python download_clean_analyse.py  

3. Open the Power BI dashboard from the dashboard folder  



## Notes

This project was designed to demonstrate skills in Python, NLP, data cleaning, and visual storytelling.  
The focus is on clarity, interpretability, and meaningful comparison rather than exhaustive literary theory.



## Author
Amrutha Venkata Sai Chillarige
🔗 LinkedIn: www.linkedin.com/in/amrutha-vs-chillarige

