import pytest
from unittest.mock import patch, MagicMock

# Импорт сервиса после того, как PYTHONPATH будет корректно настроен
from services.auth_stud_service import studregister, checkstudreg

# ------------------- studregister -------------------

@patch("services.auth_stud_service.sqlite3.connect")
@patch("services.auth_stud_service.create_id", return_value="12345")
def test_studregister_success(mock_create_id, mock_connect):
    """Проверяем успешную регистрацию студента с mock"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    studregister("John", "Doe", "10", "jdoe", "pass123")

    mock_connect.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO students (student_id, first_name, last_name, grade, login, password) VALUES (?, ?, ?, ?, ?, ?)",
        ("12345", "John", "Doe", "10", "jdoe", "pass123")
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("services.auth_stud_service.sqlite3.connect")
@patch("services.auth_stud_service.create_id", return_value="12345")
def test_studregister_exception(mock_create_id, mock_connect):
    """Проверяем обработку исключения при insert"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("DB error")

    with pytest.raises(Exception) as exc_info:
        studregister("John", "Doe", "10", "jdoe", "pass123")

    assert str(exc_info.value) == "DB error"
    mock_conn.close.assert_called_once()

# ------------------- checkstudreg -------------------

@patch("services.auth_stud_service.sqlite3.connect")
def test_checkstudreg_found(mock_connect):
    """Проверяем успешный поиск студента"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, "John", "Doe", "10", "jdoe", "pass123")]

    result = checkstudreg("jdoe", "pass123")
    assert result is True
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM students WHERE login = ? AND password = ?",
        ("jdoe", "pass123")
    )
    mock_conn.close.assert_called_once()


@patch("services.auth_stud_service.sqlite3.connect")
def test_checkstudreg_not_found(mock_connect):
    """Проверяем поиск, когда студента нет"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    result = checkstudreg("unknown", "nopass")
    assert result is False
    mock_conn.close.assert_called_once()


@patch("services.auth_stud_service.sqlite3.connect")
def test_checkstudreg_exception(mock_connect):
    """Проверка обработки ошибки при select"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.side_effect = Exception("DB select error")

    with pytest.raises(Exception) as exc_info:
        checkstudreg("jdoe", "pass123")

    assert str(exc_info.value) == "DB select error"
    mock_conn.close.assert_called_once()
