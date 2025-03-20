import re
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import FunctionTransformer
from sklearn.naive_bayes import MultinomialNB


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

# preprocessor = FunctionTransformer(lambda emails: preprocess_email(emails))
preprocessor = FunctionTransformer(preprocess_email)

# Convert emails to feature vectors using CountVectorizer
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('vectorizer', CountVectorizer(token_pattern=r'\b[a-zA-Z]{2,}\b')),
    ('naive_bayes', MultinomialNB())
])
