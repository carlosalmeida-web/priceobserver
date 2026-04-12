"""
Testes automatizados
"""

import unittest
from funcoes_auxiliares import validar_nome, extrair_numero, verifica_mudanca

class Testador(unittest.TestCase):

    def test_validar_nome_valido(self):
        self.assertTrue(validar_nome("Joao"))
        self.assertTrue(validar_nome("Marina Silva"))

    def test_validar_nome_invalido(self):
        self.assertFalse(validar_nome("Jo"))
        self.assertFalse(validar_nome("J0ao"))
        self.assertFalse(validar_nome(""))

    def test_extrair_numero_inteiro(self):
        self.assertEqual(extrair_numero("Preço: 500"), 500.0)
        self.assertEqual(extrair_numero("R$ 1299,90"), 1299.90)
        self.assertEqual(extrair_numero("R$ 1.299,90"), 1299.90)

    def test_extrair_numero_sem_numero(self):
        self.assertIsNone(extrair_numero("Sem preço"))

    def test_verifica_mudanca_true(self):
        self.assertTrue(verifica_mudanca(10.0, 12.0))

    def test_verifica_mudanca_false(self):
        self.assertFalse(verifica_mudanca(10.0, 10.0))

if __name__ == "__main__":
    unittest.main()
