import pytest
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

import mlflow
from mlflow.tracking import MlflowClient


def is_matplotlib_installed():
    try:
        import matplotlib  # pylint: disable=unused-import

        return True
    except ImportError:
        return False


@pytest.mark.skipif(
    is_matplotlib_installed(), reason="matplotlib must be uninstalled to run this test"
)
def test_sklearn_autolog_works_without_matplotlib():
    mlflow.sklearn.autolog()
    model = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
    X, y = load_breast_cancer(return_X_y=True)
    with mlflow.start_run() as run:
        model.fit(X, y)

    run = MlflowClient().get_run(run.info.run_id)
    expected_metric_keys = {
        "training_score",
        "training_accuracy_score",
        "training_precision_score",
        "training_recall_score",
        "training_f1_score",
        "training_log_loss",
    }
    assert set(run.data.metrics).issuperset(expected_metric_keys)
