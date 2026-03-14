import sys


from Lab2.main import Main


def test_main_run_with_cli_argument_success(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "a|b"])

    code = Main().run()
    out = capsys.readouterr().out

    assert code == 0
    assert "Формула: a|b" in out


def test_main_run_with_empty_input(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog"])
    monkeypatch.setattr("builtins.input", lambda _: "   ")

    code = Main().run()
    out = capsys.readouterr().out

    assert code == 1
    assert "Пустая формула не поддерживается." in out


def test_main_run_with_parser_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "a+1"])

    code = Main().run()
    out = capsys.readouterr().out

    assert code == 1
    assert "Ошибка:" in out


def test_main_read_expression_from_input(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    monkeypatch.setattr("builtins.input", lambda _: "a&b")
    assert Main()._read_expression() == "a&b"