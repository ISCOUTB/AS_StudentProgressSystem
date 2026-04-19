from unittest.mock import MagicMock
from uuid import uuid4

from app.repositories.estudiante_materia import create, update, delete


class FakeData:
    def __init__(self):
        self.id_estudiante = uuid4()
        self.id_materia = uuid4()
        self.status = "activo"

    def model_dump(self, exclude_unset=True):
        return {"status": self.status}


def test_create_estudiante_materia():
    mock_session = MagicMock()
    data = FakeData()

    resultado = create(mock_session, data)

    mock_session.add.assert_called()
    mock_session.commit.assert_called()
    mock_session.refresh.assert_called()

    assert resultado is not None


def test_update_estudiante_materia():
    mock_session = MagicMock()
    fake_obj = MagicMock()

    mock_session.exec.return_value.first.return_value = fake_obj

    data = FakeData()

    resultado = update(mock_session, uuid4(), uuid4(), data)

    mock_session.add.assert_called()
    mock_session.commit.assert_called()

    assert resultado is not None


def test_delete_estudiante_materia():
    mock_session = MagicMock()
    fake_obj = MagicMock()

    mock_session.exec.return_value.first.return_value = fake_obj

    resultado = delete(mock_session, uuid4(), uuid4())

    mock_session.delete.assert_called()
    mock_session.commit.assert_called()

    assert resultado is True