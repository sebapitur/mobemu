import os
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn2pmml import PMMLPipeline
from sklearn2pmml import sklearn2pmml
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn import svm
from sklearn.neural_network import MLPClassifier


df = pd.read_csv(f"dataset/{os.environ.get('DATASET')}/useful_messages.csv")
positive_df = df.loc[df["usefulTransfer"] == 1]
negative_df = df.loc[df["usefulTransfer"] == 0].sample(len(positive_df))
balanced_df = pd.concat([positive_df, negative_df], ignore_index=True)
preprocessed_df = balanced_df.drop(columns="usefulTransfer").copy()

minmax_columns = ["messageHopCount"]
categorial_columns = [
    "oldFriendWithDestination",
    "oldCommonCommunity",
    "newFriendWithDestination",
    "newCommonCommunity",
]

standard_columns = [
    col
    for col in preprocessed_df.select_dtypes(include=["float64", "int64"]).columns
    if col not in minmax_columns and col not in categorial_columns
]

preprocessor = ColumnTransformer(
    transformers=[
        ("minmax", MinMaxScaler((0, 1)), minmax_columns),
        ("standard", StandardScaler(), standard_columns),
        ("onehotencoder", OneHotEncoder(), categorial_columns),
    ],
    remainder="passthrough",
)

preprocessed_df = preprocessor.fit_transform(preprocessed_df)
X = balanced_df.copy().drop(columns=["usefulTransfer"])
result_df = pd.DataFrame(balanced_df["usefulTransfer"].copy().squeeze())
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(result_df)


def display_metrics(y_test, y_pred, save=False):
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    display_func = print

    if save:
        f = open(f"metrics-{os.environ['MODEL']}.txt", "w")
        display_func = f.write
    display_func("Number of entries trained on: " + str(5 * len(y_test)) + "\n")
    display_func(f"Accuracy: {accuracy:.2f}\n")
    display_func("Classification Report:\n")
    display_func(str(classification_report(y_test, y_pred)) + "\n")
    display_func("Confusion Matrix:\n")
    display_func(str(confusion_matrix(y_test, y_pred)) + "\n")

    if save:
        f.close()


def train_neural(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = MLPClassifier(
        solver="lbfgs",
        activation="relu",
        alpha=1e-5,
        hidden_layer_sizes=(64, 32),
        random_state=42,
        max_iter=500,
    )

    # Build the pipeline
    neural_pipeline = Pipeline([("preprocessor", preprocessor), ("classifier", clf)])

    neural_pipeline.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = neural_pipeline.predict(X_test)

    # Create a PMML pipeline
    pmml_pipeline = PMMLPipeline([("preprocessor", preprocessor), ("classifier", clf)])

    base_working_dir = os.getcwd()

    os.chdir(f"{base_working_dir}/dataset/{os.environ.get('DATASET')}")
    pmml_pipeline.fit(X_train, y_train)

    # Export the model to PMML
    sklearn2pmml(pmml_pipeline, f"model-neural-{os.environ.get('DATASET')}.pmml")
    display_metrics(y_test, y_pred, save=True)

    os.chdir(base_working_dir)


def train_svm(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    base = svm.SVC(kernel="rbf")

    # Hyperparameter tuning using Grid Search
    param_grid = {
        "C": [0.1, 1, 10],
        "gamma": ["scale", "auto"],  # Kernel coefficient
    }

    grid_poly = GridSearchCV(base, param_grid, refit=True, cv=5)
    grid_poly.fit(X_train, y_train)

    best_svm = grid_poly.best_estimator_

    # Build the pipeline
    svm_pipeline = Pipeline([("preprocessor", preprocessor), ("classifier", best_svm)])

    svm_pipeline.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = svm_pipeline.predict(X_test)

    # Create a PMML pipeline
    pmml_pipeline = PMMLPipeline(
        [("preprocessor", preprocessor), ("classifier", best_svm)]
    )

    base_working_dir = os.getcwd()
    os.chdir(f"{base_working_dir}/dataset/{os.environ.get('DATASET')}")
    pmml_pipeline.fit(X_train, y_train)

    # Export the model to PMML
    sklearn2pmml(pmml_pipeline, f"model-svm-{os.environ.get('DATASET')}.pmml")
    display_metrics(y_test, y_pred, save=True)

    os.chdir(base_working_dir)


def train_random_forest(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    # Build the pipeline
    rf_pipeline = Pipeline(
        [("preprocessor", preprocessor), ("classifier", rf_classifier)]
    )

    rf_pipeline.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = rf_pipeline.predict(X_test)

    # Create a PMML pipeline
    pmml_pipeline = PMMLPipeline(
        [("preprocessor", preprocessor), ("classifier", rf_classifier)]
    )

    base_working_dir = os.getcwd()
    os.chdir(f"{base_working_dir}/dataset/{os.environ.get('DATASET')}")
    pmml_pipeline.fit(X_train, y_train)

    # Export the model to PMML
    sklearn2pmml(pmml_pipeline, f"model-rf-{os.environ.get('DATASET')}.pmml")
    display_metrics(y_test, y_pred, save=True)

    os.chdir(base_working_dir)


if os.environ.get("MODEL") == "rf":
    train_random_forest(X, y)
elif os.environ.get("MODEL") == "neural":
    train_neural(X, y)
elif os.environ.get("MODEL") == "svm":
    train_svm(X, y)
