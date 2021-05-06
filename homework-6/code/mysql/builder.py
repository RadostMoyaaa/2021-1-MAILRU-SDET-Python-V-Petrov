from mysql.models import CountRequests, CountTyped, BiggestRequestsError


class MySqlBuilder:

    def __init__(self, client):
        self.client = client

    def create_count_requests(self, count):
        count_model = CountRequests(count=count)
        self.client.session.add(count_model)
        self.client.session.commit()
        return count_model

    def create_count_typed_request(self, name, count):
        typed_model = CountTyped(name=name, count=count)
        self.client.session.add(typed_model)
        self.client.session.commit()
        return typed_model

    def create_biggest_request(self, url, code, size, ip):
        biggest_model = BiggestRequestsError(url=url, code=code, size=size, ip=ip)
        self.client.session.add(biggest_model)
        self.client.session.commit()
        return biggest_model

