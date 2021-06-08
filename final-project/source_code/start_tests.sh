#! /bin/bash
echo $PYTHONPATH
pytest -s -v -m  "${TYPE}" -n"${N}" --device="${DEV}" /tmp/source_code/test --alluredir=/tmp/allure/