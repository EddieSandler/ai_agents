def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)

class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append({'type': 'withdraw', 'amount': amount})

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        price = get_share_price(symbol)
        if price == 0.0:
            raise ValueError(f"Invalid stock symbol: {symbol}")
        total_cost = price * quantity
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares")
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': price})

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.holdings.get(symbol, 0) < quantity:
            raise ValueError(f"Insufficient shares of {symbol} to sell")
        price = get_share_price(symbol)
        total_revenue = price * quantity
        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'price': price})

    def portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, qty in self.holdings.items():
            total_value += get_share_price(symbol) * qty
        return total_value

    def profit_or_loss(self) -> float:
        return self.portfolio_value() - self.initial_deposit

    def report_holdings(self) -> str:
        if not self.holdings:
            return "No holdings"
        holdings_list = []
        for symbol, qty in self.holdings.items():
            price = get_share_price(symbol)
            holdings_list.append(f"{symbol}: {qty} shares @ ${price:.2f} each")
        return ", ".join(holdings_list)

    def report_transactions(self) -> list:
        transaction_strings = []
        for trans in self.transactions:
            if trans['type'] == 'deposit':
                transaction_strings.append(f"Deposit: ${trans['amount']:.2f}")
            elif trans['type'] == 'withdraw':
                transaction_strings.append(f"Withdraw: ${trans['amount']:.2f}")
            elif trans['type'] == 'buy':
                transaction_strings.append(f"Buy: {trans['quantity']} shares of {trans['symbol']} @ ${trans['price']:.2f}")
            elif trans['type'] == 'sell':
                transaction_strings.append(f"Sell: {trans['quantity']} shares of {trans['symbol']} @ ${trans['price']:.2f}")
        return transaction_strings
