#! /bin/bash
echo $PYTHONPATH
pytest -s -v -m  "${TYPE}" -n"${N}" /tmp/source_code/test --alluredir=/tmp/allure/