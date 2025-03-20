import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from preprocessing import pipeline
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score, classification_report
from joblib import dump


file_name = '../data/emails.csv'
df = pd.read_csv(file_name)
df['body'] = df['body'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()  # Remove extra spaces/newlines

df.dropna(subset=['body', 'is_spam'], inplace=True)
x = df['body']
y = df['is_spam']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)

param_grid = {
    "naive_bayes__alpha": [0.01, 0.1, 0.5, 1.0],
    "vectorizer__ngram_range": [(1, 1), (1, 2)]
}
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid_search.fit(X_train, y_train, naive_bayes__sample_weight=sample_weight)

best_nb = grid_search.best_estimator_
print("BEST ESTIMATOR: ", best_nb)

X_test_pred = best_nb.predict(X_test)
print("Predictions")
print(X_test_pred)

accuracy = accuracy_score(y_test,X_test_pred)
precision = precision_score(y_test, X_test_pred, average="weighted")
recall = recall_score(y_test, X_test_pred, average="weighted")
f1 = f1_score(y_test, X_test_pred)

print("\n===== Test Set Evaluation =====")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Print detailed classification report
print("Print detailed classification report: ")
print(classification_report(y_test, X_test_pred))

dump(best_nb , "../models/spam_classifier.pkl")
print("Model saved successfully")

# feature_names = pipeline.named_steps['vectorizer'].get_feature_names_out()
# print("Top 50 words in vocabulary:", feature_names[:50])
# X_train_df = pd.DataFrame(X_train_transformed.toarray(), columns=feature_names)
# print(X_train_df.head())

# print("Training Samples (Body and Label):\n")
# for body, label in zip(X_train.head(), y_train.head()):
#     print(f"Body: {body}\nSpam: {label}\n{'-'*50}")
#
# print("\nX_train: ")
# print(X_train.info())
# print("\nY_train: ")
# print(y_train.info())
