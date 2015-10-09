#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Felix'

import json
import sys
from pdf import PDF
from optparse import OptionParser
from server import Server


def main(config=None, label=None):
    fonts = []
    # Setup PDF Generator
    pdf = PDF("A4")

    # Add all fonts here
    pdf.add_font("cambria", "", "fonts/cambria.ttf", True)
    pdf.add_font("cambria", "B", "fonts/cambria-bold.ttf", True)
    fonts.append(["cambria", "cambria bold"])

    # Start initial page, always one
    pdf.add_page()

    # Command run from console with label input
    # Generate label and exit
    if label:
        pdf.generate(**label)
        return

    if config:
        server = Server(config, pdf)
        server.run()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="label", help="Generate label based on <file>")
    parser.add_option("-c", "--config", dest="config", help="Start as web server with config")

    (options, args) = parser.parse_args()

    if not options.label and not options.config:
        parser.print_help()
        print "Please choose either -f or -c"
        sys.exit(1)

    if options.label:
        try:
            with open(options.label) as fp:
                label_json = json.load(fp)
        except Exception:
            print "Failed to open/json parse " + options.label + " as label file."
            sys.exit(1)

        main(label=label_json)
    else:
        config = {}
        try:
            with open(options.config) as fp:
                config = json.load(fp)
        except Exception, e:
            print "Failed to open/json parse " + options.config + " as configuration file." + " " + str(e)

        main(config=config)
