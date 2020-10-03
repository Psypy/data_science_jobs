import glassdoor_scraper as gs
import pandas as pd
path = "/home/max/PycharmProjects/GlassDoor/chromedriver/chromedriver"
df = gs.get_jobs('data scientist', num_jobs=500, verbose=False, path=path, slp_time=5)

df.to_csv('jobs.csv', index=False)