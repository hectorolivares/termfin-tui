def calculate_profit(income, expenses):
    return income - expenses


def calculate_variation(income, budget):
    return income - budget


def calculate_variation_percentage(variation, budget):
    if not budget:
        return 0.0
    return (variation / budget) * 100


def calculate_expense_excess(expenses, expense_limit):
    return expenses - expense_limit


def calculate_overdue_rate(overdue_receivables, accounts_receivable):
    if not accounts_receivable:
        return 0.0
    return (overdue_receivables / accounts_receivable) * 100