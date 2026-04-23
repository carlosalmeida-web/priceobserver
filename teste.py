"""
Testes automatizados das funcoes auxiliares.
"""

import unittest
from funcoes_auxiliares import validar_nome, extrair_numero, validar_url


class Testador(unittest.TestCase):

    def test_validar_nome_valido(self):
        self.assertTrue(validar_nome("Joao"))
        self.assertTrue(validar_nome("Marina Silva"))

    def test_validar_nome_invalido(self):
        self.assertFalse(validar_nome("Jo"))
        self.assertFalse(validar_nome("J0ao"))
        self.assertFalse(validar_nome(""))

    def test_extrair_numero_inteiro(self):
        self.assertEqual(extrair_numero("Preco: 500"), 500.0)
        self.assertEqual(extrair_numero("R$ 1299,90"), 1299.90)
        self.assertEqual(extrair_numero("R$ 1.299,90"), 1299.90)
        self.assertEqual(extrair_numero("R$ 43.677,00"), 43677.00)
        self.assertEqual(extrair_numero("200,00"), 200.00)

    def test_extrair_numero_sem_decimal(self):
        self.assertEqual(extrair_numero("R$ 1000"), 1000.0)
        self.assertEqual(extrair_numero("R$ 10090"), 10090.0)

    def test_extrair_numero_grande(self):
        self.assertEqual(extrair_numero("R$ 1.000.000,00"), 1000000.0)
    
    def test_extrair_numero_sem_numero(self):
        self.assertIsNone(extrair_numero("Sem preco"))

    def test_validar_url(self):
        # URLs válidas
        self.assertTrue(validar_url("http://example.com"))
        self.assertTrue(validar_url("https://example.com"))
        self.assertTrue(validar_url("https://www.google.com"))
        self.assertTrue(validar_url("http://localhost:8000"))

        # URLs inválidas
        self.assertFalse(validar_url("example.com"))  # Sem esquema
        self.assertFalse(validar_url("ftp://example.com"))  # Esquema não suportado
        self.assertFalse(validar_url("http://"))  # Sem netloc
        self.assertFalse(validar_url("https://"))  # Sem netloc

if __name__ == "__main__":
    unittest.main()
