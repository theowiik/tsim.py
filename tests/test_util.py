from src.core.data import Direction
from src.core.util import DirectionUtils


def test_dir_to_coordinate():
    # Arrange
    expected_mapping = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
    }

    # Act
    actual_mapping = DirectionUtils.dir_to_coordinate

    # Assert
    assert actual_mapping == expected_mapping
