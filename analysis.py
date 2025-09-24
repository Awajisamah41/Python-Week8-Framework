import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the metadata file
try:
    metadata_path = 'metadata.csv'  # Adjust path if necessary
    df = pd.read_csv(metadata_path)
except FileNotFoundError:
    print("Error: metadata.csv not found.  Make sure it's in the same directory, or specify the full path.")
    exit()
except Exception as e:
    print(f"Error loading metadata: {e}")
    exit()


# Basic Data Exploration
print("First 5 rows of the DataFrame:")
print(df.head())

print("\nDataFrame Information:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())

print("\nMissing Values per column:")
print(df.isnull().sum())





# Handle Missing Values (Example: fill missing abstracts with "No Abstract Provided")
df['abstract'].fillna("No Abstract Provided", inplace=True)

# Convert publication date to datetime objects
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Drop rows with missing 'title' (Important to have titles)
df.dropna(subset=['title'], inplace=True)

#Example data cleaning

df['journal'].fillna("Unknown", inplace=True)




# 1. Publication Trend Over Time
publication_counts = df['publish_time'].dt.year.value_counts().sort_index()

plt.figure(figsize=(12, 6))
plt.plot(publication_counts.index, publication_counts.values, marker='o')
plt.title('COVID-19 Research Publication Trend Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.xticks(publication_counts.index, rotation=45)  # Rotate year labels for readability
plt.grid(True)
plt.tight_layout()
plt.savefig('publication_trend.png') # Save the figure to a file
plt.show()


# 2. Top Journals Publishing COVID-19 Research
top_journals = df['journal'].value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis')
plt.title('Top 10 Journals Publishing COVID-19 Research')
plt.xlabel('Number of Publications')
plt.ylabel('Journal')
plt.tight_layout()
plt.savefig('top_journals.png') # Save the figure to a file
plt.show()

# 3. Example: Distribution of Abstract Lengths
df['abstract_length'] = df['abstract'].apply(len)

plt.figure(figsize=(10, 6))
sns.histplot(df['abstract_length'], bins=50, kde=True)
plt.title('Distribution of Abstract Lengths')
plt.xlabel('Abstract Length')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('abstract_length.png') # Save the figure to a file
plt.show()


# 2. Top Journals Publishing COVID-19 Research
top_journals = df['journal'].value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis')
plt.title('Top 10 Journals Publishing COVID-19 Research')
plt.xlabel('Number of Publications')
plt.ylabel('Journal')
plt.tight_layout()
plt.savefig('top_journals.png') # Save the figure to a file
plt.show()

# 3. Example: Distribution of Abstract Lengths
df['abstract_length'] = df['abstract'].apply(len)

plt.figure(figsize=(10, 6))
sns.histplot(df['abstract_length'], bins=50, kde=True)
plt.title('Distribution of Abstract Lengths')
plt.xlabel('Abstract Length')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('abstract_length.png') # Save the figure to a file
plt.show()
