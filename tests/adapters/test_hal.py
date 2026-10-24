from conftest import check_adapter


def test_fixture(tmp_path):
    check_adapter("hal", tmp_path)
