#!/bin/bash
pandoc -s -o index.html -B navbar.html --mathjax --template html_template.html --css markdown.css index.md
