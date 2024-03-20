#!/bin/python3

import argparse
import contextlib
from io import BytesIO
import json

import jinja2
import jinja2.nativetypes
import requests
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
        with Vertical():
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


@contextlib.contextmanager
def open_datafile(location, location_type='auto'):
    if location_type in ('auto', 'url'):
        try:
            response = requests.get(location)
            response.raise_for_status()
            yield BytesIO(response.content)
            return
        except requests.exceptions.RequestException:
            if location_type == 'url':
                raise
    if location_type in ('auto', 'file'):
        with open(location) as datafile:
            yield datafile
        return
    raise Exception(f"Could not open location: '{location}' as '{location_type}'")


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'datafile',
        help='Path to file or URL of the data to be inspected.',
    )
    parser.add_argument(
        '--data-type',
        choices=['auto', 'file', 'url'],
        default='auto',
        help='Instruct how to treat the datafile argument. Default is auto which tries to treat the datafile as URL and if not successful tries to treat it as file.'
    )
    return parser


def main():
    args = cli_parser().parse_args()
    with open_datafile(args.datafile, args.data_type) as datafile:
        app = DataInspector(datafile)
    app.run()
    return 0
