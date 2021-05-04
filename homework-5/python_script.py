import apache_log_parser
import json
import re
import sys
import os
from pprint import pprint


# Функция сортировки словаря по значениям
def sort_dict_by_values(dictionary, reverse=True, count=5):
    sorted_results = {}
    result = {}
    keys = sorted(dictionary, key=dictionary.get, reverse=reverse)
    for k in keys:
        sorted_results[k] = dictionary[k]
    for k, v in sorted_results.items():
        if count == 0:
            break
        else:
            result[k] = v
            count -= 1
    return result


# Общее количество запросов
def get_count_of_requests(target_list):
    return {'Count of all requests:': len(target_list)}


# Количество запросов по типу
def get_count_of_typed_requests(target_list):
    all_requests = []
    result = {}

    for string in target_list:
        all_requests.append(string['request_first_line'].split()[0])

    unique_request = list(set(all_requests))

    for type_req in unique_request:
        result[type_req] = all_requests.count(type_req)
    return result


# Топ 10 самых частых запросов
def get_most_frequent_requests(target_list, count=10):
    all_urls = []
    all_results = {}

    for string in target_list:
        all_urls.append(string['request_first_line'].split()[1])

    unique_urls = list(set(all_urls))

    for url in unique_urls:
        all_results[url] = all_urls.count(url)

    return sort_dict_by_values(all_results, True, count=count)


# Топ запросов по объему с ошибкой 4xx
def get_biggest_requests(target_list, count=5):
    all_sizes = []
    result = {}

    for i, string in enumerate(target_list):
        if re.match(r'^4', string['status']):
            all_sizes.append((i, int(string['response_bytes_clf'])))

    sorted_sizes = sorted(all_sizes, key=lambda tup: tup[1])
    result_strings = [target_list[sorted_sizes[i][0]] for i in range(len(sorted_sizes) - 1,
                                                                     len(sorted_sizes) - count - 1, -1)]
    for i, s in enumerate(result_strings):
        result[i] = {'url': s['request_first_line'].split()[1],
                     'code': s['status'],
                     'size': s['response_bytes_clf'],
                     'ip': s['remote_ip']}

    return result


# Топ пользователей по запросам с ошибками 5xx
def get_users_with_frequent_request(target_list, count=5):
    all_ip = []
    all_results = {}

    for string in target_list:
        if re.match(r'^5', string['status']):
            all_ip.append(string['remote_ip'])

    unique_ip = list(set(all_ip))

    for u in unique_ip:
        all_results[u] = all_ip.count(u)

    return sort_dict_by_values(all_results, True, count=count)


# Запись строк в список
def get_lines_from_log(file_name):
    root = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(root, file_name)
    with open(file_dir, 'r') as f:
        lines = f.readlines()
    return lines


# Парсинг строк в список
def parse_lines_to_data(template, lines):
    line_parser = apache_log_parser.make_parser(template)
    data = [line_parser(line) for line in lines]
    return data


# Запись результата в json
def write_results_to_json(result, folder, file_name):
    root = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(root, folder, file_name)
    with open(file_dir, 'w') as f:
        json.dump(result, f, indent=4)


def main():
    lines = get_lines_from_log('access.log')
    template = "%a - - %t \"%r\" %s %b"
    data = parse_lines_to_data(template, lines)

    result = {
        'Count': get_count_of_requests(target_list=data),
        'TypedCount': get_count_of_typed_requests(target_list=data),
        'MostFrequent': get_most_frequent_requests(target_list=data),
        'Biggest4xx': get_biggest_requests(target_list=data),
        'UsersFrequent5xx': get_users_with_frequent_request(target_list=data),
    }

    return result


if '--json' in sys.argv:
    result = main()
    write_results_to_json(result, 'python_results', 'result.json')
else:
    pprint(main())
