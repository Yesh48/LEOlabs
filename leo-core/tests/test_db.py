from leo.db import Database


def test_database_initialises_sqlite(tmp_path, monkeypatch):
    db_path = tmp_path / "leo-test.db"
    monkeypatch.setenv("LEO_DB_ENGINE", "sqlite")
    monkeypatch.setenv("LEO_DB_PATH", str(db_path))

    database = Database()
    database.init()
    database.record_score("https://example.com", 80.0, "2024-01-01T00:00:00")

    recent = database.recent_scores(limit=1)
    assert recent[0]["url"] == "https://example.com"
    summary = database.summary()
    assert summary["count"] >= 1
    assert summary["engine"] == "sqlite"
