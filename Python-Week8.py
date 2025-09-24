import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ========================
# Load Data
# ========================
df = pd.read_csv("metadata.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))

st.title("CORD19 datasets - Sheet 1")
st.write("Explore COVID-19 Research Papers Metadata")

# ========================
# Year Filter
# ========================
year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select year range", year_min, year_max, (2020, 2021))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"Showing {len(filtered)} papers between {year_range[0]} and {year_range[1]}")

# ========================
# Publications over time
# ========================
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
st.bar_chart(year_counts)

# ========================
# Top Journals
# ========================
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
st.bar_chart(top_journals)

# ========================
# Word Cloud of Titles
# ========================
st.subheader("Word Cloud of Titles")
all_titles = " ".join(filtered['title'].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_titles)
st.image(wordcloud.to_array())

# ========================
# Sample Data
# ========================
st.subheader("Sample Data")
st.write(filtered[['title', 'journal', 'publish_time']].head(10))

