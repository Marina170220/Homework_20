import pytest
from unittest.mock import MagicMock

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    gen_1 = Genre(id=1, name='Test_1')
    gen_2 = Genre(id=2, name='Test_2')
    gen_3 = Genre(id=3, name='Test_3')

    genre_dict = {1: gen_1, 2: gen_2, 3: gen_3}
    genre_dao.get_one = MagicMock(side_effect=genre_dict.get)
    genre_dao.get_all = MagicMock(return_value=genre_dict)
    genre_dao.create = MagicMock(return_value=Genre(id=1))
    genre_dao.delete = MagicMock(side_effect=genre_dict.pop)
    genre_dao.update = MagicMock()
    genre_dao.partially_update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres) == 3
        assert len(genres) > 0

    def test_create(self):
        data = {'id': 4,
                'name': 'Test_4'}
        genre = self.genre_service.create(data)

        assert genre.id is not None

    def test_delete(self):
        self.genre_service.delete(1)
        genre = self.genre_service.get_one(1)

        assert genre is None

    def test_update(self):
        data = {'id': 4,
                'name': 'Test_4'}
        genre = self.genre_service.update(data)

        assert genre.id is not None
