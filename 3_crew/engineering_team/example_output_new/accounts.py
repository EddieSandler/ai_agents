def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol.upper(), 0.0)


class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit_funds(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw_funds(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append({'type': 'withdrawal', 'amount': amount})
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        if price == 0.0:
            return False
        total_cost = price * quantity
        if quantity > 0 and total_cost <= self.balance:
            self.balance -= total_cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self.transactions.append({
                'type': 'buy',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'total': total_cost
            })
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if quantity > 0 and self.holdings.get(symbol, 0) >= quantity:
            price = get_share_price(symbol)
            total_revenue = price * quantity
            self.balance += total_revenue
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append({
                'type': 'sell',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'total': total_revenue
            })
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, qty in self.holdings.items():
            total_value += get_share_price(symbol) * qty
        return total_value

    def calculate_profit_or_loss(self) -> float:
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return dict(self.holdings)

    def get_transactions(self) -> list:
        return list(self.transactions)

    def get_report(self) -> dict:
        return {
            'user_id': self.user_id,
            'balance': self.balance,
            'portfolio_value': self.calculate_portfolio_value(),
            'profit_or_loss': self.calculate_profit_or_loss(),
            'holdings': self.get_holdings()
        }
