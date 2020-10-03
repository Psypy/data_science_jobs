import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

jobs = pd.read_csv("/home/max/PycharmProjects/GlassDoor/venv/jobs.csv")
print(jobs.info())

# drop job that have null in company name
jobs = jobs.dropna(subset=['Company Name'], axis=0)

# clean job title column
jobs['job_title_clean'] = jobs['Job Title'].apply(lambda x: x.split('(')[0].lower())


# simplify job titles
def simplify_title(title):
    if 'data scientist' in title:
        return 'data scientist'
    elif 'data engineer' in title:
        return 'data engineer'
    elif 'analyst' in title:
        return 'data analyst'
    elif 'machine learning' in title:
        return 'mle'
    elif 'bi' or 'intelligence' in title:
        return 'business intelligence'
    elif 'insight' in title:
        return 'insight manager'
    elif 'director' in title:
        return 'director'
    else:
        return 'na'


jobs['title_simple'] = jobs['job_title_clean'].apply(simplify_title)


# assign seniority of job
def seniority(title):
    for s in ['sr', 'senior', 'lead', 'principal', 'head']:
        if s in title:
            return 'senior'
    if 'jr' in title or 'junior' in title:
        return 'junior'
    else:
        return 'na'


jobs['seniority'] = jobs['job_title_clean'].apply(seniority)

''' extract (minimum) salary from job description text'''
job_descriptions = jobs['Job Description'].str.lower()

# Regex to capture numbers that are preceded or followed by € or eur(o)
regex = r'(?:euro?|€)\s?((?:[0-9]{1,3}),?.?\d{0,3})|((?:[0-9]{0,3}),?\.?(?:[0-9]{1,3}))(?:,?\.?\d{0,3})?-?\s?(?:euro?|€)'

salaries_matches = job_descriptions.str.extract(regex)

# combine extracted groups
salaries_series = salaries_matches[salaries_matches \
    .columns[0]] \
    .fillna(salaries_matches[salaries_matches.columns[1]])

salaries_clean = salaries_series \
    .str.replace(".", "") \
    .str.replace(",", "") \

salaries = pd.to_numeric(salaries_clean, errors='coerce')

# multiply monthly salaries by 14 and append to dataframe
jobs['salary'] = [x * 14 if x < 10000 else x for x in salaries]

# Cleaning company names
jobs['company'] = jobs['Company Name'].apply(lambda x: x.splitlines()[0])

# cleaning revenue column
revenue_dict = {
    None: '-1',
    'Unknown / Non-Applicable': -1,
    'Less than $1 million (USD)': 1,
    '$1 to $5 million (USD)': 2,
    '$10 to $25 million (USD)': 3,
    '$25 to $50 million (USD)': 4,
    '$50 to $100 million (USD)': 5,
    '$100 to $500 million (USD)': 6,
    '$500 million to $1 billion (USD)': 7,
    '$1 to $2 billion (USD)': 8,
    '$2 to $5 billion (USD)': 9,
    '$5 to $10 billion (USD)': 10,
    '$10+ billion (USD)': 10
}

jobs['revenue_clean'] = jobs['Revenue'].map(revenue_dict).fillna(-1)

# clean size (# of employees) column
size_dict = {
    'Unknown': -1,
    '1 to 50 Employees': 1,
    '51 to 200 Employees': 2,
    '201 to 500 Employees': 3,
    '501 to 1000 Employees': 4,
    '1001 to 5000 Employees': 5,
    '5001 to 10000 Employees': 6,
    '10000+ Employees': 7
}

jobs['size_clean'] = jobs['Size'].map(size_dict).fillna(-1)

# Extract skills from job description
skills = ['python', 'rstudio', ' r ', 'sql', 'spark', 'excel', 'tableau', 'hadoop', 'spss', 'statistics']
for s in skills:
    jobs[s] = jobs['Job Description'].apply(lambda x: 1 if s in x.lower() else 0)

# combine r columns (rstudio + r)
jobs['r_clean'] = [1 if a + b > 0 else 0 for a, b in zip(jobs['rstudio'], jobs[' r '])]

jobs['python'] = jobs['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
