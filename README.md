# **Spam Email Classifier 📩🚫**

This project is a **Spam Email Classifier** that uses **Naïve Bayes** and **Natural Language Processing (NLP)** techniques to classify email messages as spam or not spam. It is built with **scikit-learn**, using **text preprocessing**, **CountVectorizer**, and **Multinomial Naïve Bayes** to train and evaluate the model. The trained model can then be used for real-time spam detection.

## **Table of Contents**
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Model Training](#model-training)
- [Spam Prediction](#spam-prediction)
- [Example Predictions](#example-predictions)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## **Project Overview**
This project:
✅ **Preprocesses email messages** by removing punctuation, converting to lowercase, and replacing URLs and numbers.  
✅ **Uses a Naïve Bayes model** with **CountVectorizer** for feature extraction.  
✅ **Performs hyperparameter tuning** using **GridSearchCV** to optimize model performance.  
✅ **Evaluates the model** using accuracy, precision, recall, and F1-score.  
✅ **Allows users to classify new messages** using a trained spam classifier.  

---

## **Dataset**
The dataset used is a CSV file containing email messages and their corresponding labels (`true` for spam, `false` for non-spam). The file should be structured as follows:

| body                | is_spam |
|---------------------|---------|
| "Win a free iPhone now!" | true    |
| "Meeting at 5 PM, please confirm." | false   |

You should place the dataset in the `data/` directory.

---

## **Installation**
To run the project, follow these steps:

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/DOOMSDAY101/ml-spam-detector.git
cd ml-spam-detector

## **Usage**
You can classify new messages using the trained spam classifier.

### **Run the Spam Classifier**
Execute the following command to start the classifier:

```bash
python predict.py
