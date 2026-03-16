from kfp import dsl

@dsl.component
def train_model():
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier

    X, y = load_iris(return_X_y=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)

    print(f"Model accuracy: {score}")

@dsl.pipeline(name="vertex-ai-demo-pipeline")
def pipeline():
    train_model()