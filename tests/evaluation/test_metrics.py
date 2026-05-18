import pytest

from mosaic.core import FrameId
from mosaic.evaluation import MetricResult, splat_count_metric
from mosaic.splats import GaussianSplat, SplatMap


def _splat(x: float) -> GaussianSplat:
    return GaussianSplat(center=(x, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))


def test_metric_result_rejects_blank_name() -> None:
    with pytest.raises(ValueError, match="name"):
        MetricResult(name=" ", value=1.0, unit="count")


def test_splat_count_metric_counts_snapshot_splats() -> None:
    snapshot = SplatMap(frame=FrameId("map"), splats=(_splat(0.0), _splat(1.0)))

    metric = splat_count_metric(snapshot)

    assert metric == MetricResult(name="splat_count", value=2.0, unit="splats")


def test_metric_result_converts_to_json_ready_dict() -> None:
    metric = MetricResult(name="tracking_rate", value=1.0, unit="ratio")

    assert metric.as_dict() == {"name": "tracking_rate", "value": 1.0, "unit": "ratio"}
