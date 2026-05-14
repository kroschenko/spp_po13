"""Tests for zadanie1 and zadanie2."""
import pytest
from task import zadanie1, zadanie2


class TestZadanie1:
    """Tests for zadanie1 function."""

    def test_triwialnye_odnoznachnye(self, monkeypatch):
        """Test single digit numbers."""
        monkeypatch.setattr('builtins.input', lambda _: "1 2 3")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 3
        assert b == 0
        assert c == 0

    def test_triwialnye_dvuznachnye(self, monkeypatch):
        """Test double digit numbers."""
        monkeypatch.setattr('builtins.input', lambda _: "10 20 30")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 0
        assert b == 3
        assert c == 0

    def test_triwialnye_trehznachnye(self, monkeypatch):
        """Test three digit numbers."""
        monkeypatch.setattr('builtins.input', lambda _: "100 200 300")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 0
        assert b == 0
        assert c == 3

    def test_granichnye_9_i_10(self, monkeypatch):
        """Test boundary 9 and 10."""
        monkeypatch.setattr('builtins.input', lambda _: "9 10")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 1
        assert b == 1
        assert c == 0

    def test_granichnye_minus9_i_minus10(self, monkeypatch):
        """Test boundary -9 and -10."""
        monkeypatch.setattr('builtins.input', lambda _: "-9 -10")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 1
        assert b == 1
        assert c == 0

    def test_granichnye_99_i_100(self, monkeypatch):
        """Test boundary 99 and 100."""
        monkeypatch.setattr('builtins.input', lambda _: "99 100")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 0
        assert b == 1
        assert c == 1

    def test_granichnye_minus99_i_minus100(self, monkeypatch):
        """Test boundary -99 and -100."""
        monkeypatch.setattr('builtins.input', lambda _: "-99 -100")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 0
        assert b == 1
        assert c == 1

    def test_nol(self, monkeypatch):
        """Test zero."""
        monkeypatch.setattr('builtins.input', lambda _: "0")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 1
        assert b == 0
        assert c == 0

    def test_otricatelnye_chisla(self, monkeypatch):
        """Test negative numbers."""
        monkeypatch.setattr('builtins.input', lambda _: "-5 -50 -500")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 1
        assert b == 1
        assert c == 1

    def test_smeshannye_chisla(self, monkeypatch):
        """Test mixed numbers."""
        monkeypatch.setattr('builtins.input', lambda _: "5 -5 10 -10 100 -100")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 2
        assert b == 2
        assert c == 2

    def test_chisla_vne_diapazona(self, monkeypatch):
        """Test numbers outside range."""
        monkeypatch.setattr('builtins.input', lambda _: "1000 10000 -1000")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 0
        assert b == 0
        assert c == 0

    def test_pustoy_vvod(self, monkeypatch):
        """Test empty input."""
        monkeypatch.setattr('builtins.input', lambda _: "")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        a, b, c = zadanie1()
        assert a == 0
        assert b == 0
        assert c == 0

    def test_isklyuchitelnaya_situaciya_ne_chislo(self, monkeypatch):
        """Test exception on non-number."""
        monkeypatch.setattr('builtins.input', lambda _: "abc 10")
        monkeypatch.setattr('builtins.print', lambda *x: None)
        with pytest.raises(ValueError):
            zadanie1()


class TestZadanie2:
    """Tests for zadanie2 function."""

    def test_trivialnye_5(self, monkeypatch):
        """Test number 5."""
        inputs = iter(["5", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [2]

    def test_trivialnye_0(self, monkeypatch):
        """Test number 0."""
        inputs = iter(["0", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [0]

    def test_trivialnye_1(self, monkeypatch):
        """Test number 1."""
        inputs = iter(["1", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [1]

    def test_granichnye_stepeni_dvoyki(self, monkeypatch):
        """Test powers of two."""
        inputs = iter(["2", "4", "8", "16", "32", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [1, 1, 1, 1, 1]

    def test_granichnye_vse_edinicy(self, monkeypatch):
        """Test all ones."""
        inputs = iter(["7", "15", "31", "63", "127", "255", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [3, 4, 5, 6, 7, 8]

    def test_otricatelnye_chisla(self, monkeypatch):
        """Test negative numbers."""
        inputs = iter(["-1", "-2", "-3", "-5", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [1, 1, 2, 2]

    def test_bolshie_chisla(self, monkeypatch):
        """Test large numbers."""
        inputs = iter(["1023", "1024", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [10, 1]

    def test_neskolko_chisel_podryad(self, monkeypatch):
        """Test multiple numbers in a row."""
        inputs = iter(["5", "10", "15", "0", "7", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [2, 2, 4, 0, 3]

    def test_pustoy_vvod_srazu(self, monkeypatch):
        """Test empty input immediately."""
        inputs = iter([""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert not results

    def test_isklyuchitelnaya_situaciya_ne_chislo(self, monkeypatch):
        """Test exception on non-number."""
        inputs = iter(["abc", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        with pytest.raises(ValueError):
            zadanie2()

    def test_isklyuchitelnaya_situaciya_pustaya_stroka_v_seredine(self, monkeypatch):
        """Test empty string in middle."""
        inputs = iter(["5", "", "10"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        results = zadanie2()
        assert results == [2]

    def test_isklyuchitelnaya_situaciya_float(self, monkeypatch):
        """Test exception on float."""
        inputs = iter(["3.14", ""])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('builtins.print', lambda *x: None)
        with pytest.raises(ValueError):
            zadanie2()
