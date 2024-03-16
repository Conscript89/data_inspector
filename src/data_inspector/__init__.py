#!/bin/python3

import argparse
import json

import jinja2
import jinja2.nativetypes
from textual.app import App
from textual.validation import Function
from textual.widgets import Header, Footer, Input, Pretty, Label
#import yaml


class DataInspector(App):
    CSS_PATH = "./layout.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit")
    ]

    def __init__(self, datafile):
        super().__init__()
        self.data = json.load(datafile)
        self.query_widget = Input(
            placeholder="Data Query",
            validate_on=["changed"],
            validators=Function(self.is_jinja2_expression, "Is not valid jinja2 expression."),
        )
        self.expression_error = Label()
        self.data_widget = Pretty(self.data)
        self.jinja_env = jinja2.nativetypes.NativeEnvironment()

    def compose(self):
        yield Header()
        yield Label("data")
        yield self.query_widget
        yield self.expression_error
        yield self.data_widget
        yield Footer()

    def on_input_changed(self, event):
        if not event.validation_result.is_valid:
            return
        self.data_widget.update(self.render_expression(event.value, data=self.data))

    def render_expression(self, expr, **kwargs):
        jinja_expr = self.jinja_env.compile_expression(f"data{expr}", undefined_to_none=False)
        return jinja_expr(**kwargs)

    def is_jinja2_expression(self, text):
        try:
            self.expression_error.update("")
            if isinstance(self.render_expression(text, data=self.data), jinja2.runtime.Undefined):
                self.expression_error.update("Undefined variable")
                return False
            return True
        except jinja2.exceptions.TemplateError as e:
            self.expression_error.update(e.message)
            return False


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', type=argparse.FileType('r'))
    return parser


def main():
    args = cli_parser().parse_args()
    app = DataInspector(args.datafile)
    app.run()
    return 0
