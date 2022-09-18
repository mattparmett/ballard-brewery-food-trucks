class FoodTruck:
    def __init__(self, name: str, date: str, hours: str) -> None:
        self.name = name
        self.date = date
        self.hours = hours

    def __str__(self) -> str:
        hours = f" at {self.hours}" if self.hours else ""
        return f"{self.name}" + hours

    def __repr__(self) -> str:
        return str(self)
