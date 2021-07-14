#!/bin/bash

jupyter nbconvert analytics.ipynb --to html --TemplateExporter.exclude_input=True --no-promp
cp analytics.html ../docs/
