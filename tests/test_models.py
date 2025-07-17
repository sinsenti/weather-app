from unittest.mock import patch, Mock
import models
import pytest


# Goal is to verify that save_query and get_query_history works correctly(ensure execute work proprerly, etc)
@patch("models.psycopg2.connect")
def test_save_query_success(mock_connect):
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    models.save_query("TestCity", 10.5, "sunny", 50, 4.0)
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("models.psycopg2.connect")
def test_get_query_history_success(mock_connect):
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    expected = [("City", 10, "sunny", 50, 3, "2025-07-17T08:00:00Z")]
    mock_cursor.fetchall.return_value = expected

    results = models.get_query_history()
    assert results == expected
