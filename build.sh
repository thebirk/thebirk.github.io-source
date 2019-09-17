#!/bin/bash
pandoc -s -o test.html --katex --template html_template.html --css markdown.css test.md
