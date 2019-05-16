from unittest import TestCase, mock

from vitrinedynamique.domain.annonce import Annonce
from vitrinedynamique.shared.responseobj import ResponseFailure, ResponseSuccess
from vitrinedynamique.usecases.getannonce import GetAnnonceRequest, GetAnnonceUseCase
from vitrinedynamique.shared.repository import Repository

ANNONCE_ID = 'MT0137111'


class TestGetAnnonceRequest(TestCase):
    def test_get_annonce_request_no_parameter(self):
        with self.assertRaises(TypeError):
            GetAnnonceRequest()

    def test_get_annonce_request_with_parameter(self):
        request = GetAnnonceRequest(ANNONCE_ID)
        assert request.annonce_id == ANNONCE_ID
        assert bool(request) is True

    def test_get_annonce_request_create_with_parameter(self):
        request = GetAnnonceRequest.create(ANNONCE_ID)
        assert request.annonce_id == ANNONCE_ID
        assert bool(request) is True

    def test_get_annonce_request_create_none_parameter(self):
        request = GetAnnonceRequest.create(None)
        assert request.has_errors()
        assert bool(request) is False


class TestGetAnnonceUseCase(TestCase):
    def test_get_annonce_usecase_no_parameter(self):
        with self.assertRaises(TypeError):
            GetAnnonceUseCase()

    def test_get_annonce_usecase_with_repo(self):
        repo = mock.Mock(Repository)
        uc = GetAnnonceUseCase(repo)
        assert uc.repo == repo

    def test_get_annonce_usecase_with_invalid_request(self):
        repo = mock.Mock(Repository)
        invalid_request = mock.MagicMock()
        invalid_request.__bool__.return_value = False

        uc = GetAnnonceUseCase(repo)
        response = uc.execute(invalid_request)
        assert type(response) is ResponseFailure

    def test_get_annonce_usecase_with_valid_request(self):
        annonce = Annonce(ANNONCE_ID)
        repo = mock.Mock()
        repo.get.return_value = annonce
        valid_request = mock.MagicMock()
        valid_request.__bool__.return_value = True
        valid_request.annonce_id = ANNONCE_ID

        uc = GetAnnonceUseCase(repo)
        response = uc.execute(valid_request)

        repo.get.assert_called_once_with(ANNONCE_ID)
        assert response.payload == annonce
        assert type(response) is ResponseSuccess
