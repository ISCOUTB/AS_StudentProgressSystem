from unittest.mock import MagicMock
from uuid import uuid4

from backend.app.repositories.estudiante_logro import create


class FakeData:
    def __init__(self, id_estudiante, id_logromateria, status):
        self.id_estudiante = id_estudiante
        self.id_logromateria = id_logromateria
        self.status = status


def test_create_estudiante_logro():
    mock_session = MagicMock()

    data = FakeData(uuid4(), uuid4(), "activo")

    resultado = create(mock_session, data)

    mock_session.add.assert_called()
    mock_session.commit.assert_called()
    mock_session.refresh.assert_called()

    assert resultado is not None