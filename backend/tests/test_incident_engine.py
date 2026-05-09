import pytest
from app.services.incident_engine import compute_system_health


# ---------------------------------------------------------------------------
# Incident structure
# ---------------------------------------------------------------------------

def test_incidents_is_list(incidents):
    assert isinstance(incidents, list)


def test_incident_has_required_keys(incidents):
    required = {
        "id", "system_id", "severity", "confidence", "started_at",
        "ended_at", "duration_minutes", "sensors_triggered",
        "anomaly_row_count", "suppressed", "suppression_reason", "max_zscores",
    }
    for inc in incidents:
        assert required.issubset(set(inc.keys())), f"Missing keys in {inc['id']}"


def test_severity_values_valid(incidents):
    valid = {"info", "warning", "critical"}
    for inc in incidents:
        assert inc["severity"] in valid


def test_confidence_range(incidents):
    for inc in incidents:
        assert 0.0 <= inc["confidence"] <= 1.0


def test_suppressed_incidents_have_zero_confidence(incidents):
    for inc in incidents:
        if inc["suppressed"]:
            assert inc["confidence"] == 0.0


def test_suppressed_incidents_have_info_severity(incidents):
    for inc in incidents:
        if inc["suppressed"]:
            assert inc["severity"] == "info"


# ---------------------------------------------------------------------------
# Duration gating (single-sensor isolated spikes are suppressed)
# ---------------------------------------------------------------------------

def test_single_sensor_single_row_spike_is_suppressed(incidents):
    """
    Isolated single-sensor, single-row spikes must be suppressed.
    This is the core noise-suppression requirement.
    """
    single_sensor_single_row = [
        i for i in incidents
        if i["anomaly_row_count"] == 1 and len(i["sensors_triggered"]) == 1
    ]
    assert len(single_sensor_single_row) > 0, "Expected some isolated spikes in the dataset"
    for inc in single_sensor_single_row:
        assert inc["suppressed"], f"{inc['id']} should be suppressed (1 row, 1 sensor)"


# ---------------------------------------------------------------------------
# Multi-sensor exception (correlated events bypass duration gating)
# ---------------------------------------------------------------------------

def test_multi_sensor_single_row_incident_not_suppressed(incidents):
    """
    A single row where 2+ sensors are simultaneously anomalous (HVAC_2 at 04:10, 10:00)
    should NOT be suppressed — correlated multi-sensor events are real signals.
    """
    multi_sensor_single_row = [
        i for i in incidents
        if i["anomaly_row_count"] == 1 and len(i["sensors_triggered"]) >= 2
    ]
    assert len(multi_sensor_single_row) > 0, "Expected multi-sensor single-row events"
    for inc in multi_sensor_single_row:
        assert not inc["suppressed"], f"{inc['id']} should NOT be suppressed"


# ---------------------------------------------------------------------------
# HVAC-2 specific assertions
# ---------------------------------------------------------------------------

def test_hvac_2_has_active_incidents(incidents):
    """HVAC_2's multi-sensor spike events must generate active incidents."""
    hvac2 = [i for i in incidents if i["system_id"] == "HVAC_2" and not i["suppressed"]]
    assert len(hvac2) >= 1


def test_hvac_2_has_critical_incident(incidents):
    """HVAC_2 has a 3-sensor simultaneous event — must produce at least one critical incident."""
    hvac2_critical = [
        i for i in incidents
        if i["system_id"] == "HVAC_2" and i["severity"] == "critical"
    ]
    assert len(hvac2_critical) >= 1


# ---------------------------------------------------------------------------
# HVAC-3 specific assertions
# ---------------------------------------------------------------------------

def test_hvac_3_has_sustained_active_incident(incidents):
    """
    HVAC_3 has a sustained pressure drop in its final 3 hours.
    It should produce at least one active incident.
    """
    hvac3 = [i for i in incidents if i["system_id"] == "HVAC_3" and not i["suppressed"]]
    assert len(hvac3) >= 1


def test_hvac_3_sustained_incident_is_long(incidents):
    """The HVAC_3 pressure incident should span many consecutive rows."""
    hvac3_active = [
        i for i in incidents
        if i["system_id"] == "HVAC_3" and not i["suppressed"]
    ]
    assert any(i["anomaly_row_count"] >= 4 for i in hvac3_active), (
        "Expected HVAC_3 to have a sustained incident with >= 4 rows"
    )


# ---------------------------------------------------------------------------
# HVAC-1 specific assertions
# ---------------------------------------------------------------------------

def test_hvac_1_has_critical_drift_incident(incidents):
    """HVAC_1 shows sustained multi-sensor drift in its final 1.5 hours — must be critical."""
    hvac1_critical = [
        i for i in incidents
        if i["system_id"] == "HVAC_1" and i["severity"] == "critical"
    ]
    assert len(hvac1_critical) >= 1


# ---------------------------------------------------------------------------
# HVAC-5 specific assertions
# ---------------------------------------------------------------------------

def test_hvac_5_has_no_active_incidents(incidents):
    """HVAC_5 is the cleanest unit — all its alerts should be suppressed."""
    hvac5_active = [i for i in incidents if i["system_id"] == "HVAC_5" and not i["suppressed"]]
    assert len(hvac5_active) == 0


# ---------------------------------------------------------------------------
# Health scoring
# ---------------------------------------------------------------------------

def test_health_score_range(incidents, anomalies_df):
    for unit_id in anomalies_df["unit_id"].unique():
        unit_df = anomalies_df[anomalies_df["unit_id"] == unit_id]
        unit_incidents = [i for i in incidents if i["system_id"] == unit_id]
        score, _ = compute_system_health(
            unit_incidents, len(unit_df), int(unit_df["is_anomaly"].sum())
        )
        assert 0 <= score <= 100


def test_hvac5_has_max_health(incidents, anomalies_df):
    h5 = anomalies_df[anomalies_df["unit_id"] == "HVAC_5"]
    h5_incidents = [i for i in incidents if i["system_id"] == "HVAC_5"]
    score, severity = compute_system_health(h5_incidents, len(h5), int(h5["is_anomaly"].sum()))
    assert score == 100
    assert severity == "normal"
