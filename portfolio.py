import pandas as pd

def get_portfolio_links(skills):
    df = pd.read_csv("my_portfolio.csv")
    matched_links = []

    for _, row in df.iterrows():
        techstack = row["Techstack"].lower()
        if any(skill.lower() in techstack for skill in skills):
            matched_links.append(row["Links"])

    return matched_links
