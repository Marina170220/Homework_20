import pytest
from unittest.mock import MagicMock

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    dir_1 = Director(id=1, name='Test_1')
    dir_2 = Director(id=2, name='Test_2')
    dir_3 = Director(id=3, name='Test_3')

    director_dict = {1: dir_1, 2: dir_2, 3: dir_3}
    director_dao.get_one = MagicMock(side_effect=director_dict.get)
    director_dao.get_all = MagicMock(return_value=director_dict)
    director_dao.create = MagicMock(return_value=Director(id=1))
    director_dao.delete = MagicMock(side_effect=director_dict.pop)
    director_dao.update = MagicMock()
    director_dao.partially_update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) == 3
        assert len(directors) > 0

    def test_create(self):
        data = {'id': 4,
                'name': 'Test_4'}
        director = self.director_service.create(data)

        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)
        director = self.director_service.get_one(1)

        assert director is None

    def test_update(self):
        data = {'id': 4,
                'name': 'Test_4'}
        director = self.director_service.update(data)

        assert director.id is not None
