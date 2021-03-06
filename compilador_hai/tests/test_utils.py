import sys
sys.path.append("..")
import unittest
import utils
import maquina

class TestCountBrackets(unittest.TestCase):
    def test_count_brackets(self):
        self.assertEqual(3,utils.count_brackets("test[1][3][a]"))
        self.assertEqual(2,utils.count_brackets("a[1][2]"))
        self.assertEqual(2,utils.count_brackets("a[][2]"))
        self.assertEqual(0,utils.count_brackets("a"))
        self.assertEqual(0,utils.count_brackets(""))

class TestRepeatBrackets(unittest.TestCase):
    def test_repeat_brackets(self):
        # self.assertEqual(expected, repeat_brackets(times))
        self.assertEqual(None,utils.repeat_brackets(0))
        self.assertEqual(["[","]"],utils.repeat_brackets(1))
        self.assertEqual(["[","]","[","]"],utils.repeat_brackets(2))

class TestGetBracketsDecl(unittest.TestCase):
    def test_get_brackets_decl(self):
        # self.assertEqual(expected, get_brackets_decl(string))
        self.assertEqual(None,utils.get_brackets_decl("probando"))
        self.assertEqual(["[","]"],utils.get_brackets_decl("probando[]"))
        self.assertEqual(["[","]"],utils.get_brackets_decl("probando[a]"))
        self.assertEqual(["[","]"],utils.get_brackets_decl("probando[1]"))




class TestGetDeclTotal(unittest.TestCase):
    def test_get_decl_total(self):
        self.assertEqual(["Entero"], utils.get_decl_total("Entero", "t"))
        self.assertEqual(["Entero",["[","]"]],utils.get_decl_total("Entero","t[3]"))
        self.assertEqual(["Real",["[","]","[","]"]],utils.get_decl_total("Real","probando_[3][]"))
class TestDeleteBrackets(unittest.TestCase):
    def test_delete_brackets(self):
        self.assertEqual("bla",utils.delete_brackets("bla"))
        self.assertEqual("bla",utils.delete_brackets("bla[][][][][][][][][][a]"))
        self.assertEqual("bla",utils.delete_brackets("bla[][][][][][1][][1][][]"))
        self.assertEqual("bla",utils.delete_brackets("bla[][][][][][][][][][]"))



class TestStripDelBrackets(unittest.TestCase):
    def test_strip_del_brackets(self):
        self.assertEqual("hola",utils.strip_del_brackets(" hola"))
class TestNumerosBracket(unittest.TestCase):
    def test_numeros_bracket(self):
        self.assertEqual(["2","3"],utils.numeros_bracket("hola[2][3]"))
        self.assertEqual(["2","3"],utils.numeros_bracket(" hola[2][3]"))
        self.assertEqual([],utils.numeros_bracket(" hola[][]"))
        self.assertEqual([],utils.numeros_bracket(" hola[a][b]"))
        self.assertEqual([],utils.numeros_bracket(" hola"))


class TestIdsBracket(unittest.TestCase):
    def test_ids_bracket(self):
        self.assertEqual(["2","ab","a"],utils.ids_bracket("a[2][ab][a]"))
        self.assertEqual([],utils.ids_bracket(""))
        self.assertEqual([],utils.ids_bracket("a"))
        self.assertEqual(["2"],utils.ids_bracket("a[][][2]"))

class TestTieneBrackets(unittest.TestCase):
    def test_tiene_brackets(self):
        self.assertTrue(utils.tiene_brackets("hola[]"))
        self.assertTrue(utils.tiene_brackets(" hola[]"))
        self.assertTrue(utils.tiene_brackets("hola[2]"))
        self.assertTrue(utils.tiene_brackets("hola[][3]"))
        self.assertTrue(utils.tiene_brackets("hola[a][3]"))
        self.assertTrue(utils.tiene_brackets("hola[2][3]"))
        self.assertFalse(utils.tiene_brackets(""))
        self.assertFalse(utils.tiene_brackets(" "))
        self.assertFalse(utils.tiene_brackets("hola"))
        self.assertFalse(utils.tiene_brackets("hola["))


class TestEstaEnLimites(unittest.TestCase):
    def test_esta_en_limites(self):
        self.assertTrue(utils.esta_en_limites((2,3),(3,4)))
        self.assertTrue(utils.esta_en_limites((2,2),(3,3)))
        self.assertTrue(utils.esta_en_limites((0,0),(3,3)))
        self.assertFalse(utils.esta_en_limites((0,0),(0,0)))
        self.assertFalse(utils.esta_en_limites((1,0,4),(2,2,3)))
        self.assertFalse(utils.esta_en_limites((0,),(0,)))
        self.assertTrue(utils.esta_en_limites((1,),(3,)))
        self.assertFalse(utils.esta_en_limites((2,),(3,1)))
        self.assertFalse(utils.esta_en_limites((),(3,)))




class TestTipo(unittest.TestCase):
    def test_tipo(self):
        self.assertEqual(maquina.CARACTER, utils.tipo("a"))
        self.assertEqual(maquina.CARACTER, utils.tipo(""))
        self.assertEqual(maquina.CARACTER, utils.tipo("a"))
        self.assertEqual(maquina.REAL, utils.tipo(2.3))
        self.assertEqual(maquina.ENTERO,utils.tipo(2))


class TestValInput(unittest.TestCase):
    def test_val_input(self):
        # self.assertEqual(expected, val_input())
        assert True # TODO: implement your test here

class TestIsSequence(unittest.TestCase):
    def test_is_sequence(self):
        self.assertTrue(utils.is_sequence(()))
        self.assertFalse(utils.is_sequence(""))
        self.assertFalse(utils.is_sequence("asa"))
        self.assertTrue(utils.is_sequence([]))

if __name__ == '__main__':
    unittest.main()
