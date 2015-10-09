__author__ = 'Alexander Felix'

import glob
import os
import json
import fnmatch
import re
from os import path
from flask import Flask, render_template, request, send_file


class Server():
    def __init__(self, config, pdf):
        self.pdf = pdf
        self.app = Flask(__name__)
        self.defaults = config.get("defaults", {})
        self.host = config.get("host", "127.0.0.1")
        self.port = config.get("port", 5000)
        self.path = config.get("path", "./")
        self.input_path = config.get("stored_configrations", "history/json")
        self.fonts = []
        self._regexp = re.compile("^([a-z]*)_*(.*)\.ttf$")

        for _, _, filenames in os.walk(self.path + "/fonts"):
            for filename in fnmatch.filter(filenames, '*.ttf'):
                self.add_font(filename)

    def add_font(self, filename):
        match = self._regexp.match(filename)
        name = match.group(1)
        style = match.group(2)

        # Add all fonts here
        self.pdf.add_font(name, style, self.path + "/fonts/" + filename, True)
        self.fonts.append({"name": name, "style": style})

    def run(self):
        self.app._static_folder = self.path + "/static"
        self.setupFlask()
        self.app.run(host=self.host, port=self.port)

    def setupFlask(self):
        @self.app.route('/', methods=['GET'])
        def page():
            old_configurations = []
            for x in glob.glob(self.input_path + "/*.json"):
                old_configurations.append(path.basename(x)[:-5])

            return render_template('index.html',
                                   old_configurations=old_configurations,
                                   **self.defaults)

        @self.app.route('/old/<selected_conf>', methods=['GET', 'POST'])
        def load_old(selected_conf):
            old_configurations = []
            active_conf = {}
            found = False

            for x in glob.glob(self.input_path + "/*.json"):
                config_name = path.basename(x)[:-5]
                old_configurations.append(config_name)
                if selected_conf == config_name:
                    active_conf = json.load(file(x))
                    found = True

            if not found:
                return page()

            return render_template('index.html',
                                   old_configurations=old_configurations,
                                   selected_conf=selected_conf,
                                   **active_conf)

        @self.app.route('/generate', methods=['POST'])
        def generate():
            post_data = request.get_json(force=True)

            try:
                if post_data.get("confname", None) and self.input_path != "":
                    with open(self.input_path + "/" + post_data['confname'] + ".json", "w") as fp:
                        json.dump(post_data, fp)
            except:
                pass

            post_data.pop("confname")
            try:
                filename = self.pdf.generate(**post_data)
                return "/download/" + filename
            except Exception, e:
                return render_template('error.html', error=str(e))

        @self.app.route("/download/<filename>", methods=['GET'])
        def download(filename):
            if path.dirname(filename) != "" or filename[-4:] != ".pdf":
                return render_template('error.html', filename=filename)

            return send_file(filename, mimetype='application/pdf', as_attachment=True)


        @self.app.route('/remove_config/<config>', methods=['POST'])
        def remove_config(config):
            for x in glob.glob(self.input_path + "/*.json"):
                if config == path.basename(x)[:-5]:
                    try:
                        os.remove(x)
                        return "Removed " + config
                    except IOError:
                        return "Failed to remove " + config

