import jinja2.nativetypes

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.validation import Function
from textual.widgets import Static, Input, Label


class ExpressionError(Exception):
    pass


class QueryWidget(Static):
    def __init__(self):
        super().__init__()
        self.jinja_env = jinja2.nativetypes.NativeEnvironment()
        self.query_template = None
        self.expression_error = Label(classes="error_label")

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Label("data", id="data_label")
                yield Input(
                    placeholder="Data Query",
                    validate_on=["changed"],
                    validators=Function(self.check_jinja2_expression, "Is not valid jinja2 expression."),
                    id="data_input",
                )
            yield self.expression_error

    def check_jinja2_expression(self, query):
        try:
            self.set_query_template(query)
            self.expression_error.update()
            return True
        except jinja2.exceptions.TemplateError as e:
            self.expression_error.update(e.message)
            return False

    def set_query_template(self, expression):
        self.query_template = self.jinja_env.compile_expression(f"data{expression}", undefined_to_none=False)

    def filter_data(self, data):
        result = self.query_template(data=data)
        if isinstance(result, jinja2.Undefined):
            self.expression_error.update('Error: Undefined variable')
            raise ExpressionError('Undefined variable')
        return result
