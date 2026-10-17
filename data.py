def get_financial_data():
    return {
        "income": float(input("Ingresos: ")),
        "budget": float(input("Presupuesto: ")),
        "expenses": float(input("Egresos: ")),
        "expense_limit": float(input("Límite de egresos: ")),
        "overdue_receivables": float(input("Cartera vencida: ")),
        "accounts_receivable": float(input("Cuentas por cobrar: "))
    }