streamlit_app.py
)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image  # Import the Pillow library for image handling


# Set page configuration
st.set_page_config(
    page_title="CORD-19 Research Analysis",
    page_icon=":microscope:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load data (you might want to cache this for performance)
@st.cache_data
def load_data():
    metadata_path = 'metadata.csv'
    df = pd.read_csv(metadata_path)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['abstract'].fillna("No Abstract Provided", inplace=True)
    df.dropna(subset=['title'], inplace=True)
    df['journal'].fillna("Unknown", inplace=True)

    return df

df = load_data()


# --- Sidebar ---
st.sidebar.header("Filters")

# Date Range Filter
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [df['publish_time'].min().date(), df['publish_time'].max().date()],  # Ensure .date() is used
    min_value=df['publish_time'].min().date(),
    max_value=df['publish_time'].max().date()
)


# Convert date objects to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Journal Filter
selected_journals = st.sidebar.multiselect(
    "Select Journals",
    options=df['journal'].unique(),
    default=df['journal'].unique()[:5]  # Select a few by default
)

# Filter the DataFrame
filtered_df = df[
    (df['publish_time'] >= start_date) & (df['publish_time'] <= end_date) & (df['journal'].isin(selected_journals))
]


# --- Main Content ---
st.title("CORD-19 Research Analysis")

st.markdown("""
This Streamlit app provides a basic analysis of the CORD-19 research dataset.
You can explore publication trends, top journals, and filter the data by date and journal.
""")

# --- Display Metrics ---
total_articles = len(filtered_df)
st.metric("Total Articles in Selected Range", total_articles)

# --- Load images from files ---

try:
    publication_trend_image = Image.open("publication_trend.png")
    top_journals_image = Image.open("top_journals.png")
    abstract_length_image = Image.open("abstract_length.png")
except FileNotFoundError as e:
    st.error(f"Error loading image: {e}. Make sure you ran analysis.py and the images are in the same directory.")
    publication_trend_image = None
    top_journals_image = None
    abstract_length_image = None


# --- Display Visualizations ---
st.header("Visualizations")

if publication_trend_image:
    st.subheader("Publication Trend Over Time")
    st.image(publication_trend_image, caption="COVID-19 Research Publication Trend")
else:
    st.write("Publication trend image not available.")


if top_journals_image:
    st.subheader("Top Journals Publishing COVID-19 Research")
    st.image(top_journals_image, caption="Top 10 Journals Publishing COVID-19 Research")
else:
    st.write("Top journals image not available.")

if abstract_length_image:
    st.subheader("Distribution of Abstract Lengths")
    st.image(abstract_length_image, caption="Distribution of Abstract Lengths")
else:
    st.write("Abstract length image not available.")



# --- Display Data Table (Optional) ---
st.header("Filtered Data")
st.dataframe(filtered_df)
