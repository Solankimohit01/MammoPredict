import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load the dataset
column_names = [
    'id', 'clump_thickness', 'uniformity_of_cell_size',
    'uniformity_of_cell_shape', 'marginal_adhesion',
    'single_epithelial_cell_size', 'bare_nuclei',
    'bland_chromatin', 'normal_nucleoli', 'mitoses', 'class'
]
df = pd.read_csv('datasets/breast-cancer-wisconsin.csv', header=None, names=column_names)
# df = pd.read_csv('datasets/breast-cancer-wisconsin.csv')

#drop id column
# df = df.drop(['id'], axis=1)

# 2. Handle missing values if any
df.replace('?', pd.NA, inplace=True)
df.dropna(inplace=True)

# Convert bare_nuclei to integer
df['bare_nuclei'] = df['bare_nuclei'].astype(int)

# # 3. Map numeric features into human-readable symptoms
# df['symptoms'] = df.apply(
#     lambda row: f"Clump thickness {row['clump_thickness']}, "
#                 f"Cell shape {row['uniformity_of_cell_shape']}, "
#                 f"Nuclei {row['bare_nuclei']}, "
#                 f"Bland chromatin {row['bland_chromatin']}, "
#                 f"Mitoses {row['mitoses']}",
#     axis=1
# )

# 4. Target variable (2 = benign, 4 = malignant)
df['class'] = df['class'].map({2: 0, 4: 1})  # 0 = benign, 1 = malignant

X = df.drop('class', axis=1)
y = df['class']

# 5. Split into train/test
# X_train, X_test, y_train, y_test = train_test_split(df['symptoms'], df['class'], test_size=0.2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# 6. Create a pipeline: TF-IDF + Logistic Regression
# model = LogisticRegression(max_iter=1000)
# model = Pipeline([
#     ('tfidf', TfidfVectorizer()),
#     ('clf', LogisticRegression(max_iter=1000))
# ])

model = RandomForestClassifier(n_estimators=100, random_state=42)


# 7. Train
model.fit(X_train, y_train)

# 8. Save model
joblib.dump(model, 'symptom_model.pkl')

# 9. Evaluate (optional)
acc = model.score(X_test, y_test)
print(f"Model trained. Test Accuracy: {acc:.2f}")