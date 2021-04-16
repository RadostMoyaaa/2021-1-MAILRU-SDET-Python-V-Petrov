from test_api.base import ApiBase


class TestSegments(ApiBase):  # Тесты на создание и удаление сегмента
    SYMBOLS_COUNT = 10

    def test_create_segment(self):
        name = self.random_text(self.SYMBOLS_COUNT)
        created_id = self.create_segment(name=name, pass_condition=1, obj_type='remarketing_player')
        self.check_segment(segment_id=created_id, exp_status=200)

    def test_delete_segment(self):
        name = self.random_text(self.SYMBOLS_COUNT)
        created_id = self.create_segment(name=name, pass_condition=1, obj_type='remarketing_player')
        self.check_segment(segment_id=created_id, exp_status=200)
        deleted_id = self.delete_segment(segment_id=created_id)
        self.check_segment(segment_id=deleted_id, exp_status=404)


