import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter
from wordcloud import WordCloud

STOPWORDS = {
    "the", "and", "to", "of", "a", "in", "for", "is", "on", "with", "as",
    "an", "be", "or", "will", "are", "our", "you", "we", "this", "that",
    "at", "by", "from", "your", "have", "has", "role", "job",
    "team", "work", "experience", "including",
}

def tokenize(text):
    if not isinstance(text, str):
        return []
    words = re.findall(r"[a-z]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

def main():
    df = pd.read_csv("jobs_clean.csv", parse_dates=["date_posted_clean"])

    # 1. Bar chart: top companies
    company_counts = df["company"].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    company_counts.plot(kind="bar")
    plt.title("Top Companies by Job Postings")
    plt.xlabel("Company")
    plt.ylabel("Number of Postings")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("chart_top_companies.png")
    plt.close()  # closes the figure so it doesn't overlap with the next one

    # 2. Timeline: postings per week
    df["week"] = df["date_posted_clean"].dt.to_period("W")
    postings_per_week = df.groupby("week").size()
    postings_per_week.index = postings_per_week.index.to_timestamp()
    plt.figure(figsize=(10, 6))
    postings_per_week.plot(kind="line", marker="o")
    plt.title("Job Postings Per Week")
    plt.xlabel("Week")
    plt.ylabel("Number of Postings")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("chart_postings_timeline.png")
    plt.close()

    # 3. Word cloud of description keywords
    all_words = []
    for desc in df["description"]:
        all_words.extend(tokenize(desc))
    word_freq = Counter(all_words)
    wc = WordCloud(width=1000, height=600, background_color="white").generate_from_frequencies(word_freq)
    plt.figure(figsize=(12, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Common Words in Job Descriptions")
    plt.tight_layout()
    plt.savefig("chart_wordcloud.png")
    plt.close()

    print("Saved: chart_top_companies.png, chart_postings_timeline.png, chart_wordcloud.png")

if __name__ == "__main__":
    main()