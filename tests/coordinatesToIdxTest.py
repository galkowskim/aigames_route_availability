import pytest

from utils import coordinates_to_idx

# 2566, 5120

@pytest.mark.parametrize(
    "latitude, longitude, x, y",
    [
        (
            21.943, -67.5, 2566, 5120
        ),
        (
            55.7765, -135, 0, 0
        )
    ]
)
def test_coordinates_to_idx(latitude, longitude, x, y):
    x_pred, y_pred = coordinates_to_idx(latitude, longitude)

    assert x_pred - 100 <= x <= x_pred + 100
    assert y_pred - 100 <= y <= y_pred + 100
