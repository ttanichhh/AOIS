from Lab2.src.Analyzer import Analyzer
from Lab2.src.ReportBuilder import ReportBuilder


def test_report_builder_contains_main_sections():
    result = Analyzer().analyze("a|b")
    report = ReportBuilder().build(result)

    assert "Формула: a|b" in report
    assert "Таблица истинности:" in report
    assert "СДНФ и СКНФ:" in report
    assert "Индексная форма:" in report
    assert "Классы Поста:" in report
    assert "Полином Жегалкина:" in report
    assert "Фиктивные переменные:" in report
    assert "Булевы производные:" in report
    assert "Минимизация СДНФ (расчетный метод):" in report
    assert "Минимизация СКНФ (расчетный метод):" in report
    assert "Минимизация СДНФ (расчетно-табличный метод):" in report
    assert "Минимизация СКНФ (расчетно-табличный метод):" in report
    assert "Минимизация СДНФ (карта Карно):" in report
    assert "Минимизация СКНФ (карта Карно):" in report


def test_report_builder_handles_no_fictitious_variables_and_derivatives():
    result = Analyzer().analyze("1")
    report = ReportBuilder().build(result)

    assert "Фиктивные переменные:\nнет" in report
    assert "Булевы производные:\nнет переменных для дифференциации" in report
    assert "склеивание не выполнялось" in report