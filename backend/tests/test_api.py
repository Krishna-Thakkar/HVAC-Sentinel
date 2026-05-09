"""
API integration tests using FastAPI's TestClient.

The lifespan event runs the full pipeline at startup. The client must be used
as a context manager so Starlette triggers the lifespan before tests run.
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    """Module-scoped client that activates the app lifespan (runs the pipeline)."""
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Root + Health
# ---------------------------------------------------------------------------

def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "HVAC Sentinel" in res.json()["service"]


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# GET /systems
# ---------------------------------------------------------------------------

def test_list_systems_returns_200(client):
    res = client.get("/systems/")
    assert res.status_code == 200


def test_list_systems_returns_five_units(client):
    res = client.get("/systems/")
    assert len(res.json()) == 5


def test_list_systems_response_schema(client):
    required = {
        "id", "name", "health_score", "severity",
        "active_incident_count", "suppressed_alert_count", "last_updated",
    }
    for system in client.get("/systems/").json():
        assert required.issubset(set(system.keys()))


def test_list_systems_severity_values_valid(client):
    valid = {"normal", "warning", "critical"}
    for s in client.get("/systems/").json():
        assert s["severity"] in valid


def test_list_systems_health_score_range(client):
    for s in client.get("/systems/").json():
        assert 0 <= s["health_score"] <= 100


def test_list_systems_ordered_by_urgency(client):
    """Systems should be ordered critical → warning → normal."""
    _rank = {"critical": 0, "warning": 1, "normal": 2}
    ranks = [_rank[s["severity"]] for s in client.get("/systems/").json()]
    assert ranks == sorted(ranks)


def test_hvac_5_is_normal(client):
    hvac5 = next(s for s in client.get("/systems/").json() if s["id"] == "HVAC_5")
    assert hvac5["severity"] == "normal"


# ---------------------------------------------------------------------------
# GET /systems/{id}
# ---------------------------------------------------------------------------

def test_system_detail_returns_200(client):
    assert client.get("/systems/HVAC_2").status_code == 200


def test_system_detail_not_found(client):
    assert client.get("/systems/HVAC_999").status_code == 404


def test_system_detail_schema(client):
    data = client.get("/systems/HVAC_1").json()
    required = {
        "id", "name", "health_score", "severity",
        "active_incident_count", "suppressed_alert_count", "last_updated",
        "incidents", "recent_readings", "anomaly_rate",
    }
    assert required.issubset(set(data.keys()))


def test_system_detail_has_incidents_for_hvac2(client):
    data = client.get("/systems/HVAC_2").json()
    # HVAC_2 has active multi-sensor incidents
    assert len(data["incidents"]) >= 1


def test_system_detail_recent_readings_count(client):
    data = client.get("/systems/HVAC_1").json()
    assert 1 <= len(data["recent_readings"]) <= 20


def test_system_detail_reading_schema(client):
    readings = client.get("/systems/HVAC_1").json()["recent_readings"]
    required = {"timestamp", "pressure", "vibration", "power", "is_imputed", "is_anomaly"}
    for r in readings:
        assert required.issubset(set(r.keys()))


def test_system_detail_anomaly_rate_range(client):
    rate = client.get("/systems/HVAC_1").json()["anomaly_rate"]
    assert 0.0 <= rate <= 1.0


# ---------------------------------------------------------------------------
# GET /alerts
# ---------------------------------------------------------------------------

def test_alerts_returns_200(client):
    assert client.get("/alerts/").status_code == 200


def test_alerts_schema(client):
    data = client.get("/alerts/").json()
    assert "active_alerts" in data
    assert "suppressed_alerts" in data
    assert "total_active" in data
    assert "total_suppressed" in data


def test_alerts_has_active_alerts(client):
    data = client.get("/alerts/").json()
    assert data["total_active"] > 0


def test_alerts_has_suppressed_alerts(client):
    data = client.get("/alerts/").json()
    assert data["total_suppressed"] > 0


def test_active_alert_schema(client):
    data = client.get("/alerts/").json()
    required = {"id", "system_id", "sensor", "value", "z_score", "timestamp", "suppressed"}
    for alert in data["active_alerts"][:5]:
        assert required.issubset(set(alert.keys()))


def test_active_alerts_not_suppressed(client):
    for alert in client.get("/alerts/").json()["active_alerts"]:
        assert alert["suppressed"] is False


def test_suppressed_alerts_are_suppressed(client):
    for alert in client.get("/alerts/").json()["suppressed_alerts"]:
        assert alert["suppressed"] is True


def test_alert_limit_param(client):
    data = client.get("/alerts/?limit=5").json()
    assert len(data["active_alerts"]) <= 5
    assert len(data["suppressed_alerts"]) <= 5
