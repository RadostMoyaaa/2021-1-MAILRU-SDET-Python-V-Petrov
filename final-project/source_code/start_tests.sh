#! /bin/bash
echo $PYTHONPATH
pytest -s -v -m "${TYPE}" -n"${N}" /tmp/source_code/test/test.py --alluredir=/tmp/allure/