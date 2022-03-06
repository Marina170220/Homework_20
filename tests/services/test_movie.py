import pytest
from unittest.mock import MagicMock

from dao.movie import MovieDAO
from dao.model.movie import Movie
from dao.model.genre import Genre
from dao.model.director import Director
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    mov_1 = Movie(id=1, title='Test_1', year=2020)
    mov_2 = Movie(id=2, title='Test_2', year=1980)
    mov_3 = Movie(id=3, title='Test_3', year=None)

    movie_dict = {1: mov_1, 2: mov_2, 3: mov_3}
    movie_dao.get_one = MagicMock(side_effect=movie_dict.get)
    movie_dao.get_all = MagicMock(return_value=movie_dict)
    movie_dao.create = MagicMock(return_value=Movie(id=4, title='Test_4'))
    movie_dao.delete = MagicMock(side_effect=movie_dict.pop)
    movie_dao.update = MagicMock()
    movie_dao.partially_update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) == 3
        assert len(movies) > 0

    def test_create(self):
        data = {'title': 'Test_4'}
        movie = self.movie_service.create(data)

        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)
        movie = self.movie_service.get_one(1)

        assert movie is None

    def test_update(self):
        data = {'id': 6,
                'title': 'Test_6',
                'year': 1955}
        movie = self.movie_service.update(data)

        assert movie.id is not None
