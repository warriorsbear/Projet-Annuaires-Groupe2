"""
Tests unitaires pour la fonction ajouter_contact()
"""

import unittest
from unittest.mock import Mock, patch, call
import sys
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import ajouter_contact


class TestAjouterContact(unittest.TestCase):
    """Classe de tests pour la fonction ajouter_contact()"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_client = Mock()
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_succes(self, mock_input, mock_menu):
        """Test: Ajout d'un contact avec succès"""
        # Arrange
        mock_input.side_effect = ['Dupont', 'Jean', 'jean@example.com', '0123456789', '123 Rue de la Paix']
        self.mock_client.ajouter_contact.return_value = None  # Pas d'erreur
        
        # Act
        with patch('builtins.print') as mock_print:
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier que ajouter_contact a été appelé avec les bons paramètres
        expected_contact = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean@example.com',
            'telephone': '0123456789',
            'adresse': '123 Rue de la Paix'
        }
        self.mock_client.ajouter_contact.assert_called_once_with(expected_contact)
        
        # Vérifier que le message de succès a été affiché
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Contact ajouté avec succès" in str(call) for call in print_calls),
            f"Le message de succès n'a pas été trouvé. Appels: {print_calls}"
        )
        
        # Vérifier que menu_actions a été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_erreur(self, mock_input, mock_menu):
        """Test: Erreur lors de l'ajout du contact"""
        # Arrange
        mock_input.side_effect = ['Martin', 'Marie', 'marie@example.com', '0987654321', '456 Avenue de Paris']
        self.mock_client.ajouter_contact.side_effect = Exception("Erreur de base de données")
        
        # Act
        with patch('builtins.print') as mock_print:
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier que le message d'erreur a été affiché
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Erreur lors de l'ajout du contact" in str(call) for call in print_calls),
            f"Le message d'erreur n'a pas été trouvé. Appels: {print_calls}"
        )
        
        # Vérifier que menu_actions a quand même été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_tous_champs_remplis(self, mock_input, mock_menu):
        """Test: Vérification que tous les champs sont bien récupérés"""
        # Arrange
        nom_test = "Bernard"
        prenom_test = "Paul"
        email_test = "paul.bernard@company.com"
        telephone_test = "+33612345678"
        adresse_test = "789 Boulevard du Sud"
        
        mock_input.side_effect = [nom_test, prenom_test, email_test, telephone_test, adresse_test]
        
        # Act
        with patch('builtins.print'):
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier les paramètres passés à ajouter_contact
        call_args = self.mock_client.ajouter_contact.call_args[0][0]
        self.assertEqual(call_args['nom'], nom_test)
        self.assertEqual(call_args['prenom'], prenom_test)
        self.assertEqual(call_args['email'], email_test)
        self.assertEqual(call_args['telephone'], telephone_test)
        self.assertEqual(call_args['adresse'], adresse_test)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_champs_vides(self, mock_input, mock_menu):
        """Test: Ajout d'un contact avec des champs vides"""
        # Arrange
        mock_input.side_effect = ['', 'Lefevre', '', '', '']
        
        # Act
        with patch('builtins.print') as mock_print:
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier que le contact est quand même créé (même vide)
        call_args = self.mock_client.ajouter_contact.call_args[0][0]
        self.assertEqual(call_args['nom'], '')
        self.assertEqual(call_args['prenom'], 'Lefevre')
        self.assertEqual(call_args['email'], '')
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_input_appele_cinq_fois(self, mock_input, mock_menu):
        """Test: Vérification que input() est appelé 5 fois (nom, prénom, email, tél, adresse)"""
        # Arrange
        mock_input.side_effect = ['Renaud', 'Luc', 'luc@example.com', '0555555555', '999 Rue Principale']
        
        # Act
        with patch('builtins.print'):
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier que input() a été appelé 5 fois
        self.assertEqual(mock_input.call_count, 5)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_avec_caracteres_speciaux(self, mock_input, mock_menu):
        """Test: Ajout d'un contact avec des caractères spéciaux"""
        # Arrange
        mock_input.side_effect = ['D\'Amour', 'François', 'françois@élève.fr', '+33 6 12-34.56.78', '123 rue l\'Église']
        
        # Act
        with patch('builtins.print'):
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier que les caractères spéciaux sont conservés
        call_args = self.mock_client.ajouter_contact.call_args[0][0]
        self.assertEqual(call_args['nom'], 'D\'Amour')
        self.assertEqual(call_args['prenom'], 'François')
        self.assertIn('élève', call_args['email'])
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_affiche_titre(self, mock_input, mock_menu):
        """Test: Vérification que le titre d'ajout de contact s'affiche"""
        # Arrange
        mock_input.side_effect = ['Blanc', 'Marc', 'marc@example.com', '0111111111', '321 Rue Louise']
        
        # Act
        with patch('builtins.print') as mock_print:
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier que le titre s'affiche
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Ajout d'un contact" in str(call) for call in print_calls),
            f"Le titre n'a pas été trouvé. Appels: {print_calls}"
        )
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_avec_espaces_aux_extremites(self, mock_input, mock_menu):
        """Test: Gestion des espaces aux extrémités des inputs"""
        # Arrange
        mock_input.side_effect = ['  Dupont  ', '  Jean  ', '  jean@test.com  ', '  0123456789  ', '  123 Rue  ']
        
        # Act
        with patch('builtins.print'):
            ajouter_contact(self.mock_client)
        
        # Assert - Les inputs sont utilisés tels quels (pas de strip)
        call_args = self.mock_client.ajouter_contact.call_args[0][0]
        # Vérifier qu'ils sont bien passés (même avec espaces)
        self.assertEqual(call_args['nom'], '  Dupont  ')
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_ajout_contact_exception_specifique(self, mock_input, mock_menu):
        """Test: Gestion d'une exception spécifique"""
        # Arrange
        mock_input.side_effect = ['Gautier', 'Sophie', 'sophie@example.com', '0666666666', '555 Rue Sophie']
        error_msg = "Email invalide"
        self.mock_client.ajouter_contact.side_effect = ValueError(error_msg)
        
        # Act
        with patch('builtins.print') as mock_print:
            ajouter_contact(self.mock_client)
        
        # Assert - Vérifier que l'erreur est affichée
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any(error_msg in str(call) for call in print_calls),
            f"Le message d'erreur '{error_msg}' n'a pas été trouvé"
        )
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_menu_actions_appele_apres_ajout_reussi(self, mock_input, mock_menu):
        """Test: menu_actions() est appelé après un ajout réussi"""
        # Arrange
        mock_input.side_effect = ['Test', 'User', 'test@example.com', '0123456789', 'Test Address']
        
        # Act
        with patch('builtins.print'):
            ajouter_contact(self.mock_client)
        
        # Assert
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_menu_actions_appele_apres_erreur(self, mock_input, mock_menu):
        """Test: menu_actions() est appelé même après une erreur"""
        # Arrange
        mock_input.side_effect = ['Test', 'User', 'test@example.com', '0123456789', 'Test Address']
        self.mock_client.ajouter_contact.side_effect = RuntimeError("Erreur système")
        
        # Act
        with patch('builtins.print'):
            ajouter_contact(self.mock_client)
        
        # Assert
        mock_menu.assert_called_once_with(self.mock_client)


if __name__ == '__main__':
    unittest.main()
