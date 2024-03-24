#!/bin/python3

import argparse
import json

import jinja2
import jinja2.nativetypes
from textual.app import App
from textual.containers import Vertical
from textual.widgets import Header, Footer, Pretty, Label
#import yaml

from .widgets import QueryWidget, ExpressionError
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
        self.data_widget = Pretty(self.data)

    def compose(self):
        yield Header()
        with Vertical():
            yield self.query_widget
            with ScrollableContainer():
                yield self.data_widget
        yield Footer()

    def on_input_changed(self, event):
        if not event.validation_result.is_valid:
            return
        try:
            self.data_widget.update(self.query_widget.filter_data(self.data))
        except ExpressionError:
            pass


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', type=argparse.FileType('r'))
    return parser


def main():
    args = cli_parser().parse_args()
    app = DataInspector(args.datafile)
    app.run()
    return 0
