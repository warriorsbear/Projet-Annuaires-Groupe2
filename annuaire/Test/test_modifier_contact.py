"""
Tests unitaires pour la fonction modifier_contact()
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import modifier_contact


class TestModifierContact(unittest.TestCase):
    """Classe de tests pour la fonction modifier_contact()"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_client = Mock()
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_tous_champs(self, mock_input, mock_menu):
        """Test: Modification réussie avec tous les champs"""
        # Arrange
        mock_input.side_effect = ['1', 'Dupont', 'Jean', 'jean.new@example.com', '0123456789', '123 Rue Nouvelle']
        
        # Act
        with patch('builtins.print') as mock_print:
            modifier_contact(self.mock_client)
        
        # Assert
        expected_champs = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean.new@example.com',
            'telephone': '0123456789',
            'adresse': '123 Rue Nouvelle'
        }
        self.mock_client.modifier_contact.assert_called_once_with(1, expected_champs)
        
        # Vérifier le message de succès
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Contact modifié avec succès" in str(call) for call in print_calls),
            f"Message de succès non trouvé"
        )
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_un_seul_champ(self, mock_input, mock_menu):
        """Test: Modification avec un seul champ"""
        # Arrange
        mock_input.side_effect = ['5', '', 'Marie', '', '', '']
        
        # Act
        with patch('builtins.print'):
            modifier_contact(self.mock_client)
        
        # Assert - Seul le prénom doit être modifié
        expected_champs = {'prenom': 'Marie'}
        self.mock_client.modifier_contact.assert_called_once_with(5, expected_champs)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_aucun_champ(self, mock_input, mock_menu):
        """Test: Modification sans aucun changement (tous les champs vides)"""
        # Arrange
        mock_input.side_effect = ['3', '', '', '', '', '']
        
        # Act
        with patch('builtins.print'):
            modifier_contact(self.mock_client)
        
        # Assert - Aucun champ à modifier
        expected_champs = {}
        self.mock_client.modifier_contact.assert_called_once_with(3, expected_champs)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_erreur(self, mock_input, mock_menu):
        """Test: Erreur lors de la modification"""
        # Arrange
        mock_input.side_effect = ['99', 'Test', '', '', '', '']
        self.mock_client.modifier_contact.side_effect = ValueError("Contact introuvable")
        
        # Act
        with patch('builtins.print') as mock_print:
            modifier_contact(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Erreur lors de la modification" in str(call) for call in print_calls),
            f"Message d'erreur non trouvé"
        )
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_partielle(self, mock_input, mock_menu):
        """Test: Modification partielle (certains champs vides)"""
        # Arrange
        mock_input.side_effect = ['2', '', '', 'paul@example.com', '0987654321', '']
        
        # Act
        with patch('builtins.print'):
            modifier_contact(self.mock_client)
        
        # Assert - Seuls email et téléphone doivent être modifiés
        expected_champs = {
            'email': 'paul@example.com',
            'telephone': '0987654321'
        }
        self.mock_client.modifier_contact.assert_called_once_with(2, expected_champs)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_id_converti_en_entier(self, mock_input, mock_menu):
        """Test: Vérification que l'ID est converti en entier"""
        # Arrange
        mock_input.side_effect = ['42', 'Nouveau', '', '', '', '']
        
        # Act
        with patch('builtins.print'):
            modifier_contact(self.mock_client)
        
        # Assert - L'ID doit être un entier
        call_args = self.mock_client.modifier_contact.call_args[0]
        self.assertIsInstance(call_args[0], int)
        self.assertEqual(call_args[0], 42)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_input_appele_six_fois(self, mock_input, mock_menu):
        """Test: Vérification que input() est appelé 6 fois (ID + 5 champs)"""
        # Arrange
        mock_input.side_effect = ['1', 'A', 'B', 'C', 'D', 'E']
        
        # Act
        with patch('builtins.print'):
            modifier_contact(self.mock_client)
        
        # Assert
        self.assertEqual(mock_input.call_count, 6)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_affiche_titre(self, mock_input, mock_menu):
        """Test: Vérification que le titre s'affiche"""
        # Arrange
        mock_input.side_effect = ['1', '', '', '', '', '']
        
        # Act
        with patch('builtins.print') as mock_print:
            modifier_contact(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Entrez les nouveaux champs" in str(call) for call in print_calls),
            f"Le titre n'a pas été trouvé"
        )
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_avec_caracteres_speciaux(self, mock_input, mock_menu):
        """Test: Modification avec caractères spéciaux"""
        # Arrange
        mock_input.side_effect = ['10', 'D\'Amour', 'François', 'françois@élève.fr', '+33612345678', '123 rue l\'Église']
        
        # Act
        with patch('builtins.print'):
            modifier_contact(self.mock_client)
        
        # Assert
        expected_champs = {
            'nom': 'D\'Amour',
            'prenom': 'François',
            'email': 'françois@élève.fr',
            'telephone': '+33612345678',
            'adresse': '123 rue l\'Église'
        }
        self.mock_client.modifier_contact.assert_called_once_with(10, expected_champs)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_modification_menu_actions_toujours_appele(self, mock_input, mock_menu):
        """Test: menu_actions() toujours appelé (succès ou erreur)"""
        # Arrange
        mock_input.side_effect = ['7', 'Test', '', '', '', '']
        self.mock_client.modifier_contact.side_effect = RuntimeError("Erreur système")
        
        # Act
        with patch('builtins.print'):
            modifier_contact(self.mock_client)
        
        # Assert
        mock_menu.assert_called_once_with(self.mock_client)


if __name__ == '__main__':
    unittest.main()
