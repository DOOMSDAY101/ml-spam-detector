from joblib import load

model_path = "../models/spam_classifier.pkl"
model = load(model_path)

while True:
    isspam_input = input('Enter a message to classify (or type "exit" to quit):\n')
    if isspam_input.lower() == "exit":
        break

    # Ensure only one input (remove extra spaces)
    cleaned_input = " ".join(isspam_input.split())
    prediction = model.predict([cleaned_input])
    print(f"Spam: {prediction[0]}")
