from Lab2.src.KarnaughMap import KarnaughMap
from Lab2.src.TruthTable import TruthTable


def test_karnaugh_map_minimize_sdnf():
    table = TruthTable().from_vector(("a", "b"), [0, 0, 1, 1])  # f = a
    result = KarnaughMap().minimize(table, "sdnf")

    assert result.normal_form == "sdnf"
    assert result.expression == "a"
    assert result.selected_implicants == ("1-",)
    assert result.groups == ((2, 3),)
    assert "[map]" in result.rendered_map


def test_karnaugh_map_build_layers_for_constant():
    table = TruthTable().from_vector((), [1])
    layers = KarnaughMap().build_layers(table)

    assert len(layers) == 1
    assert layers[0].title == "const"
    assert layers[0].values == ((1,),)
    assert layers[0].indexes == ((0,),)


def test_karnaugh_map_render():
    table = TruthTable().from_vector(("a", "b"), [0, 1, 1, 0])
    layers = KarnaughMap().build_layers(table)
    rendered = KarnaughMap().render(layers)

    assert "[map]" in rendered
    assert "00" in rendered or "0" in rendered


def test_karnaugh_map_for_five_variables_has_layers():
    vector = [0] * 32
    vector[31] = 1
    table = TruthTable().from_vector(("a", "b", "c", "d", "e"), vector)
    layers = KarnaughMap().build_layers(table)

    assert len(layers) == 2
    assert all(len(layer.values) == 4 for layer in layers)
    assert all(len(layer.values[0]) == 4 for layer in layers)