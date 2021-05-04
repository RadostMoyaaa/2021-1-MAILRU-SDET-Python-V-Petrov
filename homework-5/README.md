# Цель домашнего задания

    Анализировать nginx логи
    Освоить написание bash скриптов в одну строчку
    Научиться писать bash/python скрипты

# BASH SCRIPTS

[**Access.log**](access.log)

1. Общее количество запросов
-  [**Скрипт**](bash_scripts/bash_1)
   ```bash
    echo 'Общее количество запросов' > bash_results/res1.txt | cat access.log | wc -l >> bash_results/res1.txt
   ```
-  Описание работы
   ```
    1. В результативный файл res1.text записывается заголовок
    2. С помощью утилиты cat, считывается access.log
    3. Поток вывода направляется в утилиту wc с флагом -l для подсчета общего количества строк
    4. Вывод результата предыдущего шага записывается в результативный файл res1.txt
   ```
-  Результат [**res1.txt**](bash_results/res1.txt)

______
2. Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д.
-  [**Скрипт**](bash_scripts/bash_2)
   ```bash
   echo 'Общее количество запросов по типу' > bash_results/res2.txt | cat access.log | awk '{print $6}' | sort | uniq -c | sort | awk '{print $2, $1}' | column -t >> bash_results/res2.txt
   ```
- Описание работы
  ```
    1. В результативный файл res2.txt записывается заголовок
    2. С помощью утилиты cat, считывается access.log
    3. С помощью языка awk собираются строки, включающие столбец с типом запроса
    4. Все строки отправляются на сортировку sort
    5. Собираются уникальные строки uniq, а также подсчитывается количество каждого уникального элемента -c
    6. Результат утилиты uniq передается на дополнительную сортировку по количеству элементов
    7. С помощью языка awk меняется порядок столбцов, сначала идет количество, потом тип запроса
    8. Столбцы проходят форматирование и итоговый результат записывается в res2.txt
  ```
-  Результат [**res2.txt**](bash_results/res2.txt)
______
3. Топ 10 самых частых запросов 
-  [**Скрипт**](bash_scripts/bash_3)
   ```bash
    echo 'Топ 10 запросов по url' > bash_results/res3.txt | cat access.log | awk '{print $7}' | sort | uniq -c | sort -nr | head -n10 | awk '{print $2, $1}' | column -t >> bash_results/res3.txt
   ```
-  Описание работы
   ```
    1. В результативный файл res3.txt записывается заголовок
    2. С помощью утилиты cat, считывается access.log
    3. С помощью языка awk собираются строки, включающие столбец с записью url
    4. Все строки отправляются на сортировку sort
    5. Собираются уникальные строки uniq, а также подсчитывается количество каждого уникального элемента -c
    6. Все строки отправляются на сортировку sort по количеству с флагом -nr по убыванию
    7. От всего результата срезаются первые 10 строк
    8. С помощью языка awk меняется порядок столбцов: количество, url
    9. Столбцы проходят форматирование и итоговый результат записывается в res3.txt
   ```
-  Результат [**res3.txt**](bash_results/res3.txt)



______
4. Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой
-  [**Скрипт**](bash_scripts/bash_4)
   ```bash
    echo 'Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой' > bash_results/res4.txt | cat access.log | awk '$9 ~ /^4[0-9][0-9]/ {print $0}'| sort -k10n | tail -n5 | awk '{ print $7,$9,$10,$1}' | column -t >> bash_results/res4.txt
   ```
-  Описание работы
   ```
    1. В результативный файл res4.txt записывается заголовок
    2. С помощью утилиты cat, считывается access.log
    3. С помощью языка awk собираются строки, по регулярному выражению - столбец с записью статус кода, которые начинаются на 4
    4. Все записи сортируются через sort по 10 столбцу, то есть по объему данных
    5. Срезаются 5 последних строк 
    6. С помощью языка awk меняется порядок столбцов: url, статус код, объем данных, ip-адрес
    7. Столбцы проходят форматирование и итоговый результат записывается в res4.txt
   ```
-  Результат [**res4.txt**](bash_results/res4.txt)
______
5. Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой
-  [**Скрипт**](bash_scripts/bash_5)
   ```bash
    echo 'Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой' > bash_results/res5.txt | cat access.log | awk '$9 ~ /^5[0-9][0-9]/ {print $1}'| uniq -c | sort -nr | head -n5 | awk '{print $2, $1}' | column -t >> bash_results/res5.txt 
   ```
-  Описание работы
   ```
    1. В результативный файл res4.txt записывается заголовок
    2. С помощью утилиты cat, считывается access.log
    3. С помощью языка awk собираются строки, включающие столбец с ip-адресом, по регулярному выражению - столбец с записью статус кода, которые начинаются на 5
    4. Собираются уникальные строки uniq, а также подсчитывается количество каждого уникального элемента -c
    5. Все строки отправляются на сортировку sort по количеству с флагом -nr по убыванию
    6. От всего результата срезаются первые 5 строк
    7. С помощью языка awk меняется порядок столбцов: ip-адрес,количество
    8. Столбцы проходят форматирование и итоговый результат записывается в res5.txt
   ```
-  Результат [**res5.txt**](bash_results/res5.txt)
