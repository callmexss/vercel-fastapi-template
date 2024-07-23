from app.services import memos


def test_memos_create_memo():
    r = memos.save_to_memos("test #from_code_space")
    assert r.status_code == 200
