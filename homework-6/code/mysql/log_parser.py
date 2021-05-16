import apache_log_parser
import re


class LogParser:
    def __init__(self, file_name, template):
        self.data = self.parse_lines_to_data(template, self.get_lines_from_log(file_name=file_name))

    @staticmethod
    def get_lines_from_log(file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()
        return lines

    @staticmethod
    def parse_lines_to_data(template, lines):
        line_parser = apache_log_parser.make_parser(template)
        data = [line_parser(line) for line in lines]
        return data

    def get_count_of_requests(self, target_list=None):
        if target_list is None:
            target_list = self.data
        return {'Count': len(target_list)}

    def get_count_of_typed_requests(self, target_list=None):
        if target_list is None:
            target_list = self.data

        all_requests = []
        result = {}

        for string in target_list:
            all_requests.append(string['request_first_line'].split()[0])

        unique_request = list(set(all_requests))

        for type_req in unique_request:
            result[type_req] = all_requests.count(type_req)
        return result

    @staticmethod
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

    def get_most_frequent_requests(self, target_list=None, count=10):
        if target_list is None:
            target_list = self.data

        all_urls = []
        all_results = {}

        for string in target_list:
            all_urls.append(string['request_first_line'].split()[1])

        unique_urls = list(set(all_urls))

        for url in unique_urls:
            all_results[url] = all_urls.count(url)

        return self.sort_dict_by_values(all_results, True, count=count)

    def get_biggest_requests(self, target_list=None, count=5):
        if target_list is None:
            target_list = self.data

        all_sizes = []
        result = []

        for i, string in enumerate(target_list):
            if re.match(r'^4', string['status']):
                all_sizes.append((i, int(string['response_bytes_clf'])))

        sorted_sizes = sorted(all_sizes, key=lambda tup: tup[1])
        result_strings = [target_list[sorted_sizes[i][0]] for i in range(len(sorted_sizes) - 1,
                                                                         len(sorted_sizes) - count - 1, -1)]
        for s in result_strings:
            result.append([s['request_first_line'].split()[1],
                           s['status'],
                           s['response_bytes_clf'],
                           s['remote_ip']])
        return result

    def get_users_with_frequent_request(self, target_list=None, count=5):
        if target_list is None:
            target_list = self.data
        all_ip = []
        all_results = {}

        for string in target_list:
            if re.match(r'^5', string['status']):
                all_ip.append(string['remote_ip'])

        unique_ip = list(set(all_ip))

        for u in unique_ip:
            all_results[u] = all_ip.count(u)

        return self.sort_dict_by_values(all_results, True, count=count)
