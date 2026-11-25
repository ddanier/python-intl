from python_intl import Locale


def test_repr() -> None:
    assert repr(Locale("de")) == "Locale(tag='de')"
