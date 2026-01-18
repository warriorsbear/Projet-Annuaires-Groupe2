"""
Tests unitaires pour la fonction rechercher_contact()
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import rechercher_contact


class TestRechercherContact(unittest.TestCase):
    """Classe de tests pour la fonction rechercher_contact()"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_client = Mock()
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_avec_resultats(self, mock_input, mock_menu):
        """Test: Recherche réussie avec résultats"""
        # Arrange
        mock_input.side_effect = ['Dupont', '', '']
        resultats = [
            {'id_contact': 1, 'prenom': 'Jean', 'nom': 'Dupont', 'email': 'jean@example.com'},
            {'id_contact': 2, 'prenom': 'Pierre', 'nom': 'Dupont', 'email': 'pierre@example.com'}
        ]
        self.mock_client.rechercher_contact.return_value = resultats
        
        # Act
        with patch('builtins.print') as mock_print:
            rechercher_contact(self.mock_client)
        
        # Assert
        self.mock_client.rechercher_contact.assert_called_once_with({'nom': 'Dupont'})
        
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("2 contact(s) trouvé(s)" in str(call) for call in print_calls),
            f"Message du nombre de résultats non trouvé"
        )
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_sans_resultats(self, mock_input, mock_menu):
        """Test: Recherche sans résultats"""
        # Arrange
        mock_input.side_effect = ['Martin', '', '']
        self.mock_client.rechercher_contact.return_value = []
        
        # Act
        with patch('builtins.print') as mock_print:
            rechercher_contact(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Aucun contact trouvé" in str(call) for call in print_calls),
            f"Message 'Aucun contact trouvé' non trouvé"
        )
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_avec_un_critere(self, mock_input, mock_menu):
        """Test: Recherche avec un seul critère (nom)"""
        # Arrange
        mock_input.side_effect = ['Bernard', '', '']
        resultats = [{'id_contact': 5, 'prenom': 'Paul', 'nom': 'Bernard', 'email': 'paul@example.com'}]
        self.mock_client.rechercher_contact.return_value = resultats
        
        # Act
        with patch('builtins.print'):
            rechercher_contact(self.mock_client)
        
        # Assert
        self.mock_client.rechercher_contact.assert_called_once_with({'nom': 'Bernard'})
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_avec_plusieurs_criteres(self, mock_input, mock_menu):
        """Test: Recherche avec plusieurs critères"""
        # Arrange
        mock_input.side_effect = ['Lefevre', 'Sophie', '']
        resultats = [{'id_contact': 8, 'prenom': 'Sophie', 'nom': 'Lefevre', 'email': 'sophie@example.com'}]
        self.mock_client.rechercher_contact.return_value = resultats
        
        # Act
        with patch('builtins.print'):
            rechercher_contact(self.mock_client)
        
        # Assert
        expected_criteres = {'nom': 'Lefevre', 'prenom': 'Sophie'}
        self.mock_client.rechercher_contact.assert_called_once_with(expected_criteres)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_avec_tous_criteres(self, mock_input, mock_menu):
        """Test: Recherche avec tous les critères remplis"""
        # Arrange
        mock_input.side_effect = ['Gautier', 'Marie', 'marie.gautier@example.com']
        resultats = [{'id_contact': 10, 'prenom': 'Marie', 'nom': 'Gautier', 'email': 'marie.gautier@example.com'}]
        self.mock_client.rechercher_contact.return_value = resultats
        
        # Act
        with patch('builtins.print'):
            rechercher_contact(self.mock_client)
        
        # Assert
        expected_criteres = {'nom': 'Gautier', 'prenom': 'Marie', 'email': 'marie.gautier@example.com'}
        self.mock_client.rechercher_contact.assert_called_once_with(expected_criteres)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_tous_criteres_vides(self, mock_input, mock_menu):
        """Test: Recherche avec tous les critères vides"""
        # Arrange
        mock_input.side_effect = ['', '', '']
        self.mock_client.rechercher_contact.return_value = []
        
        # Act
        with patch('builtins.print'):
            rechercher_contact(self.mock_client)
        
        # Assert
        # Doit appeler avec un dictionnaire vide
        self.mock_client.rechercher_contact.assert_called_once_with({})
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_erreur(self, mock_input, mock_menu):
        """Test: Erreur lors de la recherche"""
        # Arrange
        mock_input.side_effect = ['Test', '', '']
        self.mock_client.rechercher_contact.side_effect = Exception("Erreur base de données")
        
        # Act
        with patch('builtins.print') as mock_print:
            rechercher_contact(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Erreur lors de la recherche" in str(call) for call in print_calls),
            f"Message d'erreur non trouvé"
        )
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_input_appele_trois_fois(self, mock_input, mock_menu):
        """Test: Vérification que input() est appelé 3 fois"""
        # Arrange
        mock_input.side_effect = ['Renaud', 'Luc', 'luc@example.com']
        self.mock_client.rechercher_contact.return_value = []
        
        # Act
        with patch('builtins.print'):
            rechercher_contact(self.mock_client)
        
        # Assert
        self.assertEqual(mock_input.call_count, 3)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_affiche_resultats_formattes(self, mock_input, mock_menu):
        """Test: Vérification que les résultats s'affichent correctement"""
        # Arrange
        mock_input.side_effect = ['', 'François', '']
        resultats = [
            {'id_contact': 15, 'prenom': 'François', 'nom': 'Blanc', 'email': 'francois@example.com'}
        ]
        self.mock_client.rechercher_contact.return_value = resultats
        
        # Act
        with patch('builtins.print') as mock_print:
            rechercher_contact(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("François" in str(call) and "Blanc" in str(call) and "francois@example.com" in str(call) 
                for call in print_calls),
            f"Les informations du contact n'ont pas été affichées"
        )
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_recherche_menu_actions_toujours_appele(self, mock_input, mock_menu):
        """Test: menu_actions() est toujours appelé"""
        # Arrange
        mock_input.side_effect = ['NonExistent', '', '']
        self.mock_client.rechercher_contact.return_value = []
        
        # Act
        with patch('builtins.print'):
            rechercher_contact(self.mock_client)
        
        # Assert
        mock_menu.assert_called_once_with(self.mock_client)


if __name__ == '__main__':
    unittest.main()
