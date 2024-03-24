import os

import jinja2.nativetypes

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.validation import Function
from textual.widgets import Static, Input, Label, ContentSwitcher
from textual.suggester import Suggester

class ExpressionError(Exception):
    pass


class InputWidget(ContentSwitcher):
    def __init__(self, data_widget):
        self.query_widget = QueryWidget(data_widget, id="query_widget")
        self.save_widget = SaveWidget(id="save_widget")
        super().__init__(self.query_widget, self.save_widget, initial="query_widget")

    def switch(self):
        self.current = (
            self.save_widget.id
            if self.current == self.query_widget.id
            else
            self.query_widget.id
        )


class SaveWidget(Static):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Input(
                value=os.path.abspath(os.curdir),
                suggester=FilesystemSuggester(),
            )
            yield Label(classes="error_label")

    def on_input_submitted(self, event):
        pass


class FilesystemSuggester(Suggester):
    async def get_suggestion(self, value: str) -> str | None:
        pass


class QueryWidget(Static):
    def __init__(self, data_widget, **kwargs):
        super().__init__(**kwargs)
        self.data_widget = data_widget
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

    def on_input_changed(self, event):
        if not event.validation_result.is_valid:
            return
        try:
            self.data_widget.update(self.filter_data(self.data_widget.full_data))
        except ExpressionError:
            pass
