#!/bin/bash
pandoc -s -o test.html -B navbar.html --mathjax --template html_template.html --css markdown.css test.md
