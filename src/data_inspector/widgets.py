import jinja2.nativetypes

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.validation import Function
from textual.widgets import Static, Input, Label


class QueryWidget(Static):
    DEFAULT_CSS = """
    QueryWidget {
        layout: horizontal;
    }

    #data_label {
        align-vertical: middle;
        border: hkey $accent;
    }

    #data_input {
        border: hkey $accent;
        padding-left: 0;
    }
    """

    def __init__(self):
        super().__init__()
        self.jinja_env = jinja2.nativetypes.NativeEnvironment()
        self.query_template = None
        self.expression_error = ""

    def compose(self) -> ComposeResult:
        yield Label("data", id="data_label")
        yield Input(
            placeholder="Data Query",
            validate_on=["changed"],
            validators=Function(self.check_jinja2_expression, "Is not valid jinja2 expression."),
            id="data_input",
        )

    def check_jinja2_expression(self, query):
        try:
            self.expression_error = ""
            self.set_query_template(query)
            return True
        except jinja2.exceptions.TemplateError as e:
            self.expression_error = e.message
            return False

    def set_query_template(self, expression):
        self.query_template = self.jinja_env.compile_expression(f"data{expression}", undefined_to_none=False)