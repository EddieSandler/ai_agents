from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List


_PRICE_MAP: Dict[str, float] = {
    "AAPL": 150.0,
    "TSLA": 700.0,
    "GOOGL": 2800.0,
}


def get_share_price(symbol: str) -> float:
    """Return the last known price for a supported symbol."""
    return _PRICE_MAP.get(symbol.upper(), 0.0)


@dataclass
class Transaction:
    type: str
    amount: float
    balance: float
    symbol: str | None = None
    quantity: int | None = None
    price: float | None = None
    total: float | None = None


class Account:
    """Simple brokerage account model used by the Gradio examples."""

    def __init__(self, account_id: str, initial_deposit: float = 0.0) -> None:
        self.account_id = account_id
        self.balance = max(0.0, float(initial_deposit))
        self._net_deposits = self.balance
        self._holdings: Dict[str, int] = {}
        self._transactions: List[Transaction] = []

        if self.balance:
            self._transactions.append(
                Transaction(type="deposit", amount=self.balance, balance=self.balance)
            )

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        self._net_deposits += amount
        self._transactions.append(
            Transaction(type="deposit", amount=amount, balance=self.balance)
        )
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self._net_deposits -= amount
        self._transactions.append(
            Transaction(type="withdraw", amount=amount, balance=self.balance)
        )
        return True

    def buy_shares(
        self,
        symbol: str,
        quantity: int,
        price_lookup: Callable[[str], float] = get_share_price,
    ) -> bool:
        if quantity <= 0:
            return False
        price = price_lookup(symbol)
        if price <= 0:
            return False
        total_cost = price * quantity
        if total_cost > self.balance:
            return False

        self.balance -= total_cost
        self._holdings[symbol] = self._holdings.get(symbol, 0) + quantity
        self._transactions.append(
            Transaction(
                type="buy",
                symbol=symbol,
                quantity=quantity,
                price=price,
                total=total_cost,
                amount=total_cost,
                balance=self.balance,
            )
        )
        return True

    def sell_shares(
        self,
        symbol: str,
        quantity: int,
        price_lookup: Callable[[str], float] = get_share_price,
    ) -> bool:
        if quantity <= 0 or self._holdings.get(symbol, 0) < quantity:
            return False
        price = price_lookup(symbol)
        if price <= 0:
            return False
        total_revenue = price * quantity

        self.balance += total_revenue
        self._holdings[symbol] -= quantity
        if self._holdings[symbol] == 0:
            del self._holdings[symbol]
        self._transactions.append(
            Transaction(
                type="sell",
                symbol=symbol,
                quantity=quantity,
                price=price,
                total=total_revenue,
                amount=total_revenue,
                balance=self.balance,
            )
        )
        return True

    def get_holdings(self) -> Dict[str, int]:
        return dict(self._holdings)

    def get_transactions(self) -> List[Dict[str, float | int | str]]:
        return [transaction.__dict__.copy() for transaction in self._transactions]

    def get_profit_or_loss(
        self, price_lookup: Callable[[str], float] = get_share_price
    ) -> float:
        holdings_value = sum(
            price_lookup(symbol) * quantity for symbol, quantity in self._holdings.items()
        )
        return (self.balance + holdings_value) - self._net_deposits
