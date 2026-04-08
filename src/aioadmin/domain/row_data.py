from typing import Iterable, Sequence



class Row:
    def __init__(self, columns: Sequence[str], values: Iterable[Sequence[object]]):
        self.columns = tuple(columns)
        self.values = [row for row in values]
    
    def __eq__(self, value: 'Row') -> bool:
        return self.columns == value.columns and self.values == value.values

    def __iter__(self) -> Iterable[Sequence[object]]:
        return iter(self.rows)