import pandas as pd
from datetime import datetime

def parse_date_posted(date_str, scraped_at_str):
    """
    date_str: e.g. '03 July'
    scraped_at_str: e.g. '2026-07-08T14:30:00' (from your scraped_at column)
    Returns a proper datetime, guessing the year based on when it was scraped.
    """
    print(f"\n  📅 Parsing date: '{date_str}' (scraped at: '{scraped_at_str}')")
    
    scraped_at = datetime.fromisoformat(scraped_at_str)
    print(f"  🕐 Scraped at datetime: {scraped_at}")
    
    try:
        # Try parsing with the same year as when we scraped it
        candidate = datetime.strptime(f"{date_str} {scraped_at.year}", "%d %B %Y")
        print(f"  ✅ Initial parse: {candidate}")
    except ValueError as e:
        # print(f"  ❌ Failed to parse: {e}")
        return pd.NaT  # NaT = "Not a Time", pandas' version of a missing date

    # Edge case: if the parsed date is AFTER the scrape date, 
    # it must actually be from last year (e.g. scraped in Jan, post says "20 December")
    if candidate > scraped_at:
        # print(f"  ⚠️  Candidate ({candidate}) is after scrape date ({scraped_at})")
        candidate = candidate.replace(year=candidate.year - 1)
        # print(f"  🔄 Adjusted to previous year: {candidate}")
    # else:
        # print(f"  ✅ Date is valid: {candidate}")
    
    return candidate

def categorize_seniority(title):
    title_lower = title.lower()
    if "intern" in title_lower:
        return "Intern"
    elif "senior" in title_lower or "sr." in title_lower:
        return "Senior"
    elif "lead" in title_lower or "principal" in title_lower:
        return "Lead"
    elif "junior" in title_lower or "jr." in title_lower:
        return "Junior"
    else:
        return "Mid/Unspecified"

def detect_work_mode(description):
    if not isinstance(description, str):
        return "Unknown"
    desc_lower = description.lower()
    if "remote" in desc_lower or "work from home" in desc_lower or "wfh" in desc_lower:
        return "Remote"
    elif "hybrid" in desc_lower:
        return "Hybrid"
    elif "on-site" in desc_lower or "onsite" in desc_lower or "in-office" in desc_lower:
        return "On-site"
    else:
        return "Unspecified"

def main():
    df = pd.read_csv("jobs.csv")

    df["date_posted_clean"] = df.apply(
        lambda row: parse_date_posted(row["date_posted"], row["scraped_at"]),
        axis=1
    )
    df["seniority"] = df["title"].apply(categorize_seniority)
    df["work_mode"] = df["description"].apply(detect_work_mode)

    df.to_csv("jobs_clean.csv", index=False)

    print(f"Cleaned {len(df)} rows")
    print(df["seniority"].value_counts())   # quick sanity check: how many of each category
    print(df["work_mode"].value_counts())

if __name__ == "__main__":
    main()