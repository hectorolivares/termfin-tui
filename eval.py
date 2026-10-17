def evaluate_income(variation_percentage):
    if variation_percentage >= 0:
        return "Cumple con el presupuesto"
    elif variation_percentage > -10:
        return "Punto crítico de ingresos"
    else:
        return "No se cumple el presupuesto"

def evaluate_expenses(expense_excess):
    if expense_excess > 0:
        return "Alerta de egresos"
    return "Egresos dentro del límite"

def evaluate_receivables(overdue_rate):
    if overdue_rate >= 25:
        return "Alto riesgo de cartera"
    elif overdue_rate >= 10:
        return "Riesgo de cartera"
    return "Bajo riesgo de cartera"

def evaluate_global_status(
    variation_percentage,
    expense_excess,
    overdue_rate
):
    if variation_percentage < -10 or overdue_rate >= 25:
        return "🔴 CRÍTICO"

    if variation_percentage < 0 or expense_excess > 0 or overdue_rate >= 10:
        return "🟡 ADVERTENCIA"

    return "🟢 NORMAL"