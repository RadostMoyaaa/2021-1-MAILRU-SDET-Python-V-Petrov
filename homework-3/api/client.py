from urllib.parse import urljoin

import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.csrf_token = None
        self.session = requests.Session()

    def post_auth(self, login, password):
        location = "https://auth-ac.my.com:443/auth"
        headers = {
            "Referer": "https://account.my.com/",
        }
        data = {
                "email": login,
                "password": password,
                "continue": "https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F",
                "failure": "https://account.my.com/login/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F",
                "nosavelogin": "0"
                }
        self.session.post(url=location, headers=headers, data=data)
        self.csrf_token = self.get_csrf_token()

    def get_csrf_token(self):
        location = '/csrf/'
        url = urljoin(self.base_url, location)
        headers = self.session.get(url).headers['set-cookie'].split(';')
        cookies = [c for c in headers if 'csrftoken' in c]
        csrf_token = cookies[0].split('=')[-1]
        return csrf_token

    def post_create_segment(self, name, pass_condition, object_type):
        location = "/api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags"
        url = urljoin(self.base_url, location)
        headers = {"X-CSRFToken": f'{self.csrf_token}'}
        json = {
            "name": f"{name}",
            "pass_condition": pass_condition,
            "relations": [{"object_type": object_type, "params": {"left": 365, "right": 0, "type": "positive"}}]
        }
        response = self.session.post(url, headers=headers, json=json)
        return response

    def post_delete_segment(self, segment_id):
        location = "/api/v1/remarketing/mass_action/delete.json"
        url = urljoin(self.base_url, location)
        headers = {"X-CSRFToken": self.csrf_token}
        json = [{"source_id": segment_id, "source_type": "segment"}]
        response = self.session.post(url, headers=headers, json=json)
        return response

    def get_check_segment(self, segment_id):
        location = f"/api/v2/remarketing/segments/{segment_id}.json"
        url = urljoin(self.base_url, location)
        response = self.session.get(url=url)
        return response

    def post_create_campaing(self):
        pass
