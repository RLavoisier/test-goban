import enum
from typing import List, Tuple, Set


class Status(enum.Enum):
    """
    Enum representing the Status of a position on a goban
    """

    WHITE = 1
    BLACK = 2
    EMPTY = 3
    OUT = 4


class Goban:
    def __init__(self, goban: List[str]) -> None:
        self.goban = goban

    def get_status(self, x: int, y: int) -> Status:
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if self._position_is_out_of_bound(x, y):
            return Status.OUT
        elif self.goban[y][x] == ".":
            return Status.EMPTY
        elif self.goban[y][x] == "o":
            return Status.WHITE
        elif self.goban[y][x] == "#":
            return Status.BLACK
        raise ValueError(f"Unknown goban value {self.goban[y][x]}")

    def is_taken(
        self, x: int, y: int, checked_points: Set[Tuple[int, int]] | None = None
    ) -> bool:
        """
        This method check if a given position is taken,
        meaning that it has no empty position on the same continuous line or column of the same colour
        """
        current_position_status = self.get_status(x, y)

        if current_position_status not in (Status.BLACK, Status.WHITE):
            # only colors can be taken
            return False

        checked_points = checked_points or set()

        checked_points.add((x, y))

        adjacent_valid_positions = self._adjacent_valid_positions(x, y)

        if any(
            self.get_status(*position) == Status.EMPTY
            for position in adjacent_valid_positions
        ):
            # if one of the adjacent point is empty, the position has liberty
            return False

        for adjacent_position in adjacent_valid_positions - checked_points:
            if adjacent_position:
                # recursively check for empty adjacent spots in the valid positions
                return self.is_taken(*adjacent_position, checked_points=checked_points)

        return True

    def _adjacent_valid_positions(self, x: int, y: int) -> Set[Tuple[int, int]]:
        """
        This method return a list of valid position to check for a given position

        A valid position is either:
        - Not out of bound
        - Empty
        - The same color as the current position
        """
        current_position_status = self.get_status(x, y)

        potential_move_position = set()

        for offset in (-1, 1):
            potential_move_position.add((x + offset, y))
            potential_move_position.add((x, y + offset))

        return {
            position
            for position in potential_move_position
            if not self._position_is_out_of_bound(*position)
            and self.get_status(*position) in (Status.EMPTY, current_position_status)
        }

    def _position_is_out_of_bound(self, x: int, y: int) -> bool:
        return (
            not self.goban
            or x < 0
            or y < 0
            or y >= len(self.goban)
            or x >= len(self.goban[0])
        )
