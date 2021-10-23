#! /bin/bash
echo $PYTHONPATH
pytest -s -v -m  "${TYPE}" -n"${N}" /tmp/source_code/myapp_tests --alluredir=/tmp/allure/