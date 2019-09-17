#!/bin/bash
pandoc -s -o test.html --mathjax --template html_template.html --css markdown.css test.md
