#!/bin/python3

import argparse
import json

import jinja2
import jinja2.nativetypes
from textual.app import App
from textual.containers import Vertical
from textual.widgets import Header, Footer, Pretty, Label
#import yaml

from .widgets import QueryWidget
from textual.containers import ScrollableContainer


class DataInspector(App):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit")
    ]

    def __init__(self, datafile):
        super().__init__()
        self.data = json.load(datafile)
        self.query_widget = QueryWidget()
        self.expression_error = Label()
        self.data_widget = Pretty(self.data)

    def compose(self):
        yield Header()
        yield self.query_widget
        yield self.expression_error
        with ScrollableContainer():
            yield self.data_widget
        yield Footer()

    def on_input_changed(self, event):
        self.expression_error.update(self.query_widget.expression_error)
        if not event.validation_result.is_valid:
            return
        result = self.render_expression(data=self.data)
        if isinstance(result, jinja2.Undefined):
            self.expression_error.update('Undefined variable')
            return
        self.data_widget.update(result)

    def render_expression(self, **kwargs):
        return self.query_widget.query_template(**kwargs)


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', type=argparse.FileType('r'))
    return parser


def main():
    args = cli_parser().parse_args()
    app = DataInspector(args.datafile)
    app.run()
    return 0
