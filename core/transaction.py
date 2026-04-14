class Transaction:
    def __init__(self, id: int, amount: float, date: str, category: str, type: str):
        self._id = id
        self._amount = amount
        self._date = date
        self._category = category
        self._type = type

    @property
    def id(self) -> int:
        return self._id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def date(self) -> str:
        return self._date

    @property
    def category(self) -> str:
        return self._category

    @property
    def type(self) -> str:
        return self._type

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "amount": self._amount,
            "date": self._date,
            "category": self._category,
            "type": self._type,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            id=int(data["id"]),
            amount=float(data["amount"]),
            date=str(data["date"]),
            category=str(data["category"]),
            type=str(data["type"]),
        )

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self._id}, amount={self._amount}, "
            f"date={self._date}, category={self._category}, type={self._type})"
        )
