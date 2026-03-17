from kfp import dsl


@dsl.component(base_image="python:3.11")
def train_model():
    # Keep the demo self-contained so the Vertex runtime does not depend on
    # third-party packages being installed inside the component container.
    training_samples = [
        ([5.1, 3.5, 1.4, 0.2], "setosa"),
        ([4.9, 3.0, 1.4, 0.2], "setosa"),
        ([6.0, 2.2, 4.0, 1.0], "versicolor"),
        ([5.5, 2.3, 4.0, 1.3], "versicolor"),
        ([6.3, 3.3, 6.0, 2.5], "virginica"),
        ([5.8, 2.7, 5.1, 1.9], "virginica"),
    ]
    test_samples = [
        ([5.0, 3.4, 1.5, 0.2], "setosa"),
        ([6.7, 3.1, 4.4, 1.4], "versicolor"),
        ([6.5, 3.0, 5.8, 2.2], "virginica"),
    ]

    centroids = {}
    for label in {label for _, label in training_samples}:
        label_rows = [features for features, row_label in training_samples if row_label == label]
        centroids[label] = [
            sum(feature_values) / len(feature_values)
            for feature_values in zip(*label_rows)
        ]

    def squared_distance(left, right):
        return sum((lhs - rhs) ** 2 for lhs, rhs in zip(left, right))

    def predict(features):
        return min(
            centroids,
            key=lambda label: squared_distance(features, centroids[label]),
        )

    predictions = [(predict(features), expected) for features, expected in test_samples]
    correct = sum(1 for predicted, expected in predictions if predicted == expected)
    score = correct / len(predictions)

    print(f"Model accuracy: {score}")

@dsl.pipeline(name="vertex-ai-demo-pipeline")
def pipeline():
    train_model()
