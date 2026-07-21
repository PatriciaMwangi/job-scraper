import pandas as pd
import re
from collections import Counter

STOPWORDS = {
    "the", "and", "to", "of", "a", "in", "for", "is", "on", "with", "as",
    "an", "be", "or", "will", "are", "our", "you", "we", "this", "that",
    "at", "by", "from", "your", "have", "has", "role", "job",
    "team", "work", "experience", "including","through"
}

def tokenize(text):
    if not isinstance(text, str):
        return []
    words = re.findall(r"[a-z]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

def main():
    df = pd.read_csv("jobs_clean.csv", parse_dates=["date_posted_clean"])

    print("=== Top companies ===")
    print(df["company"].value_counts().head(10))

    print("\n=== Postings per week ===")
    df["week"] = df["date_posted_clean"].dt.to_period("W")
    print(df.groupby("week").size())

    print("\n=== Seniority trend by week ===")
    print(df.groupby(["week", "seniority"]).size().unstack(fill_value=0))

    print("\n=== Top 20 keywords in descriptions ===")
    all_words = []
    for desc in df["description"]:
        all_words.extend(tokenize(desc))
    print(Counter(all_words).most_common(20))

    print("\n=== Postings by day of week ===")
    df["day_of_week"] = df["date_posted_clean"].dt.day_name()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    print(df["day_of_week"].value_counts().reindex(day_order, fill_value=0))

if __name__ == "__main__":
    main()