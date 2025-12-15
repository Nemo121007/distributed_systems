#!/bin/bash
cd /var/lib/boinc/iris_project

# Создание задания
./bin/create_work \
  -appname iris_classifier \
  -wu_name iris_task_$(date +%s) \
  -wu_template /var/lib/boinc/templates/iris_wu.xml \
  -result_template /var/lib/boinc/templates/iris_result.xml \
  /dev/null