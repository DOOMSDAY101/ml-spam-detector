import re

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import FunctionTransformer


def preprocess_email(emails, lowercase=True, remove_punctuation=True, replace_urls=True, replace_numbers=True):
    processed_emails = []
    for email in emails:
        # Convert to lowercase
        if lowercase:
            email = email.lower()

        # Remove punctuation
        if remove_punctuation:
            email = re.sub(r"[^\w\s]", "", email)

        # Replace URLs with "URL"
        if replace_urls:
            email = re.sub(r"https?://\S+", "URL", email)

        # Replace numbers with "NUMBER"
        if replace_numbers:
            email = re.sub(r"\b\d+\b", "NUMBER", email)

        processed_emails.append(email)

    return processed_emails

preprocessor = FunctionTransformer(lambda emails: preprocess_email(emails))


file_name = '../data/emails.csv'
df = pd.read_csv(file_name)
df['body'] = df['body'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()  # Remove extra spaces/newlines

df.dropna(subset=['body', 'is_spam'], inplace=True)
x = df['body']
y = df['is_spam']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Convert emails to feature vectors using CountVectorizer
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('vectorizer', CountVectorizer(token_pattern=r'\b[a-zA-Z]{2,}\b'))
])
# Fit & Transform training data
X_train_transformed = pipeline.fit_transform(X_train)

feature_names = pipeline.named_steps['vectorizer'].get_feature_names_out()
print("Top 50 words in vocabulary:", feature_names[:50])
X_train_df = pd.DataFrame(X_train_transformed.toarray(), columns=feature_names)
print(X_train_df.head())
