#!/bin/python3

import argparse
import json

import jinja2
import jinja2.nativetypes
from textual.app import App
from textual.containers import Vertical
from textual.widgets import Header, Footer, Pretty, Label
#import yaml

from .widgets import InputWidget, ExpressionError
from textual.containers import ScrollableContainer


class DataInspector(App):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+s", "save_selection", "Save/query")
    ]

    def __init__(self, datafile):
        super().__init__()
        data = json.load(datafile)
        self.data_widget = Pretty(data)
        self.data_widget.full_data = data
        self.input_widget = InputWidget(self.data_widget)

    def compose(self):
        yield Header()
        with Vertical():
            yield self.input_widget
            with ScrollableContainer():
                yield self.data_widget
        yield Footer()

    def action_save_selection(self):
        self.input_widget.switch()


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', type=argparse.FileType('r'))
    return parser


def main():
    args = cli_parser().parse_args()
    app = DataInspector(args.datafile)
    app.run()
    return 0
