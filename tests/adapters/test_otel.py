from conftest import check_adapter


def test_fixture(tmp_path):
    check_adapter("otel", tmp_path)
