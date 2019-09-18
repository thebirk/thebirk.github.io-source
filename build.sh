#!/bin/bash

pandoc -s -o index.html --section-divs -B navbar.html --mathjax --template html_template.html --css markdown.css index.md
pandoc -s -f markdown -t html --template html_template_metadata.html -o index.json index.md