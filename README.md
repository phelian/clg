# clg - Clean Label Generator

Tool for homebrewers to generate simple beer labels.

Two Modes

1) Run as a Web Server
run with -c <path to config>

# Example configuration
{
    "host": "127.0.0.1",
    "port": 5000,
    "defaults": {
	    "brewery": "",
	    "labels_x": 3,
	    "labels_y": 4,
	    "cell_width": 60
    },
    "stored_configrations": "/opt/clg/history"
}

2) Run on command line
run with -f <path to json input>

# Example input
{
        "labels_x": 3,
        "labels_y": 4,
        "brewery": "Test Brewery",
        "name": "- Cacao Nibs -",
        "cell_width": 65,
        "abv": "11,6",
        "style": "Imperial Porter",
        "og": "120",
        "fg": "30",
        "ibu": "67,8",
        "ebc": "120",
        "batch": 1,
        "date": "2015-08-22"
 }

Upcoming Features:
* Option to only show stored configurations from caller IP
* Reload Page after file download
* Automatic PDF Cleaner
* Statistics
* Upload new fonts
* Select font / input
