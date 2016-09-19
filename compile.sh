#!/bin/bash

bibtex "$1" && pdflatex "$1"
