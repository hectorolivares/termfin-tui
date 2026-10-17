from prompt_toolkit import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame, Label, TextArea

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from calc import (
    calculate_profit,
    calculate_variation,
    calculate_variation_percentage,
    calculate_expense_excess,
    calculate_overdue_rate,
)
from eval import (
    evaluate_income,
    evaluate_expenses,
    evaluate_receivables,
    evaluate_global_status,
)


FORM_WIDTH = 36

# Inputs vacíos al iniciar
inputs = {
    "income": TextArea(text="", multiline=False, height=1),
    "budget": TextArea(text="", multiline=False, height=1),
    "expenses": TextArea(text="", multiline=False, height=1),
    "expense_limit": TextArea(text="", multiline=False, height=1),
    "accounts_receivable": TextArea(text="", multiline=False, height=1),
    "overdue_receivables": TextArea(text="", multiline=False, height=1),
}


def to_float(val: str, default: float = 0.0) -> float:
    """Convierte texto a float de forma segura."""
    try:
        return float(val.strip().replace(",", ""))
    except ValueError:
        return default


def format_money(val: float) -> str:
    """Formatea moneda con signo y separador de miles."""
    if val < 0:
        return f"-${abs(val):,.2f}"
    return f"${val:,.2f}"


def get_screen_dimensions() -> tuple[int, int]:
    """Calcula el ancho y alto exactos disponibles en la terminal."""
    try:
        size = get_app().output.get_size()
        width = max(45, size.columns - FORM_WIDTH - 4)
        height = max(15, size.rows - 2)
        return width, height
    except Exception:
        return 70, 22


def get_results_ansi() -> ANSI:
    """Calcula las métricas y genera la vista Rich ajustada a todo el alto y ancho."""
    width, height = get_screen_dimensions()
    console = Console(force_terminal=True, color_system="standard", width=width)

    has_data = any(ta.text.strip() for ta in inputs.values())

    with console.capture() as capture:
        if not has_data:
            welcome_text = Text.assemble(
                ("💡 Esperando datos financieros...\n\n", "bold cyan"),
                ("Ingresa los valores en el panel izquierdo para calcular en tiempo real:\n\n", "white"),
                ("  1. Ingresos y Presupuesto ", "bold yellow"), ("→ Calcula desvíos y cumplimiento\n", "dim"),
                ("  2. Egresos y Límite       ", "bold yellow"), ("→ Determina exceso y control de gastos\n", "dim"),
                ("  3. Cartera y Mora         ", "bold yellow"), ("→ Evalúa el riesgo crediticio\n\n", "dim"),
                ("Usa [Tab] o [Enter] para moverte entre campos.", "italic cyan")
            )
            console.print(
                Panel(
                    welcome_text,
                    title="[bold blue]Resultados Financieros[/bold blue]",
                    border_style="blue",
                    expand=True,
                    height=height
                ),
                end=""
            )
        else:
            income = to_float(inputs["income"].text)
            budget = to_float(inputs["budget"].text)
            expenses = to_float(inputs["expenses"].text)
            expense_limit = to_float(inputs["expense_limit"].text)
            accounts_receivable = to_float(inputs["accounts_receivable"].text)
            overdue_receivables = to_float(inputs["overdue_receivables"].text)

            profit = calculate_profit(income, expenses)
            variation = calculate_variation(income, budget)
            var_pct = calculate_variation_percentage(variation, budget)
            excess = calculate_expense_excess(expenses, expense_limit)
            overdue_rate = calculate_overdue_rate(overdue_receivables, accounts_receivable)

            eval_inc = evaluate_income(var_pct)
            eval_exp = evaluate_expenses(excess)
            eval_rec = evaluate_receivables(overdue_rate)
            global_stat = evaluate_global_status(var_pct, excess, overdue_rate)

            table = Table(title="[bold]Resumen de Indicadores[/bold]", expand=True)
            table.add_column("Indicador", style="bold", ratio=2)
            table.add_column("Valor", justify="right", ratio=2)
            table.add_column("Diagnóstico", justify="center", ratio=2)

            profit_style = "green" if profit >= 0 else "red"
            var_style = "green" if variation >= 0 else "yellow"
            excess_style = "red" if excess > 0 else "green"
            overdue_style = "red" if overdue_rate >= 25 else ("yellow" if overdue_rate >= 10 else "green")

            table.add_row("Utilidad", format_money(profit), f"[{profit_style}]{'Positivo' if profit >= 0 else 'Pérdida'}[/]")
            table.add_row("Variación", format_money(variation), f"[{var_style}]{'Favorable' if variation >= 0 else 'Déficit'}[/]")
            table.add_row("Variación porcentual", f"{var_pct:+.2f}%", f"[{var_style}]{eval_inc}[/]")
            table.add_row("Exceso de egresos", format_money(excess), f"[{excess_style}]{eval_exp}[/]")
            table.add_row("Cartera vencida", f"{overdue_rate:.2f}%", f"[{overdue_style}]{eval_rec}[/]")

            status_border = "red" if "CRÍTICO" in global_stat else ("yellow" if "ADVERTENCIA" in global_stat else "green")
            status_panel = Panel(
                f"[bold]ESTADO GENERAL:[/] {global_stat}",
                border_style=status_border,
                expand=True
            )

            console.print(
                Panel(
                    Group(table, Text(""), status_panel),
                    title="[bold blue]Resultados en Tiempo Real[/bold blue]",
                    border_style="blue",
                    expand=True,
                    height=height
                ),
                end=""
            )

    return ANSI(capture.get())


def create_form() -> Frame:
    """Crea el formulario ocupando todo el alto disponible."""
    form_items = [
        Label(" 1. Ingresos:"),
        inputs["income"],
        Label(""),
        Label(" 2. Presupuesto:"),
        inputs["budget"],
        Label(""),
        Label(" 3. Egresos:"),
        inputs["expenses"],
        Label(""),
        Label(" 4. Límite de egresos:"),
        inputs["expense_limit"],
        Label(""),
        Label(" 5. Cuentas por cobrar:"),
        inputs["accounts_receivable"],
        Label(""),
        Label(" 6. Cartera vencida:"),
        inputs["overdue_receivables"],
        Window(),  # Espaciador flexible para forzar que el marco llene todo el alto
    ]

    return Frame(
        body=HSplit(form_items, padding=0),
        title="Captura de Datos",
        width=FORM_WIDTH
    )


def main():
    form_frame = create_form()

    results_window = Window(
        content=FormattedTextControl(get_results_ansi),
        wrap_lines=True
    )

    header = Window(
        content=FormattedTextControl(" SISTEMA FINANCIERO TUI │ Ingreso de datos y análisis en tiempo real"),
        height=1,
        style="class:header"
    )

    footer = Window(
        content=FormattedTextControl(" [Tab / Enter] Siguiente campo  │  [Shift+Tab] Anterior  │  [Esc / Ctrl+C] Salir"),
        height=1,
        style="class:footer"
    )

    root = HSplit([
        header,
        VSplit([
            form_frame,
            results_window
        ], padding=1),
        footer
    ])

    kb = KeyBindings()

    @kb.add("tab")
    @kb.add("enter")
    @kb.add("down")
    def next_field(event):
        event.app.layout.focus_next()

    @kb.add("s-tab")
    @kb.add("up")
    def prev_field(event):
        event.app.layout.focus_previous()

    @kb.add("escape")
    @kb.add("c-c")
    def exit_app(event):
        event.app.exit()

    style = Style.from_dict({
        "header": "bold #ffffff bg:#1d4ed8",
        "footer": "#93c5fd bg:#1e293b",
        "frame.border": "#3b82f6",
        "frame.label": "bold #60a5fa",
        "text-area": "bg:#0f172a #f8fafc",
        "text-area.focused": "bg:#1e40af #ffffff bold",
    })

    app = Application(
        layout=Layout(root, focused_element=inputs["income"]),
        key_bindings=kb,
        style=style,
        full_screen=True
    )

    app.run()


if __name__ == "__main__":
    main()