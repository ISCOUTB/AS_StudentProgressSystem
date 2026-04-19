from unittest.mock import MagicMock
from uuid import uuid4

from app.repositories.malla import create, update, delete


class FakeData:
    def __init__(self):
        self.nombre = "malla test"

    def model_dump(self, exclude_unset=True):
        return {"nombre": self.nombre}


def test_create_malla():
    mock_session = MagicMock()
    data = FakeData()

    resultado = create(mock_session, data)

    mock_session.add.assert_called()
    mock_session.commit.assert_called()
    mock_session.refresh.assert_called()

    assert resultado is not None


def test_update_malla():
    mock_session = MagicMock()
    fake_obj = MagicMock()

    mock_session.exec.return_value.first.return_value = fake_obj

    data = FakeData()

    resultado = update(mock_session, uuid4(), data)

    mock_session.add.assert_called()
    mock_session.commit.assert_called()

    assert resultado is not None


def test_delete_malla():
    mock_session = MagicMock()
    fake_obj = MagicMock()

    mock_session.exec.return_value.first.return_value = fake_obj

    resultado = delete(mock_session, uuid4())

    mock_session.delete.assert_called()
    mock_session.commit.assert_called()

    assert resultado is True