"""
Shared pytest fixtures — pipeline stages built once per session.

All unit tests import from here so the CSV is read and processed exactly once,
keeping the full test suite fast even as the dataset grows.
"""
import pytest

from app.services.data_loader import load_raw_data
from app.services.preprocessing import preprocess
from app.services.feature_engineering import engineer_features
from app.services.anomaly_detection import detect_anomalies
from app.services.incident_engine import build_incidents


@pytest.fixture(scope="session")
def raw_df():
    return load_raw_data()


@pytest.fixture(scope="session")
def processed_df(raw_df):
    return preprocess(raw_df)


@pytest.fixture(scope="session")
def features_df(processed_df):
    return engineer_features(processed_df)


@pytest.fixture(scope="session")
def anomalies_df(features_df):
    return detect_anomalies(features_df)


@pytest.fixture(scope="session")
def incidents(anomalies_df):
    return build_incidents(anomalies_df)
