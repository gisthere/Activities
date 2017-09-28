#/bin/bash
PACKAGE_NAME=django-bootstrap3-datetimepicker
FILE_PATH="$(pip show $PACKAGE_NAME | sed -n -e 's/^Location: \(.*\)/\1/p')/bootstrap3_datetime/widgets.py"
sed -i 's/from django\.forms\.util/from django\.forms\.utils/' $FILE_PATH

