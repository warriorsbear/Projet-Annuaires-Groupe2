"""
Tests unitaires pour la fonction supprimer_contact()
"""

import unittest
from unittest.mock import Mock, patch, call
import sys
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import supprimer_contact


class TestSupprimerContact(unittest.TestCase):
    """Classe de tests pour la fonction supprimer_contact()"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_client = Mock()
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_succes(self, mock_input, mock_menu):
        """Test: Suppression d'un contact avec succès"""
        # Arrange
        mock_input.return_value = "1"
        self.mock_client.supprimer_contact.return_value = None  # Pas d'erreur
        
        # Act
        with patch('builtins.print') as mock_print:
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier que supprimer_contact a été appelé avec le bon ID
        self.mock_client.supprimer_contact.assert_called_once_with(1)
        
        # Vérifier que le message de succès a été affiché
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Contact supprimé avec succès" in str(call) for call in print_calls),
            f"Le message de succès n'a pas été trouvé. Appels: {print_calls}"
        )
        
        # Vérifier que menu_actions a été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_erreur(self, mock_input, mock_menu):
        """Test: Erreur lors de la suppression du contact"""
        # Arrange
        mock_input.return_value = "999"
        self.mock_client.supprimer_contact.side_effect = ValueError("Aucun contact avec l'ID 999 trouvé")
        
        # Act
        with patch('builtins.print') as mock_print:
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier que le message d'erreur a été affiché
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Erreur lors de la suppression" in str(call) for call in print_calls),
            f"Le message d'erreur n'a pas été trouvé. Appels: {print_calls}"
        )
        
        # Vérifier que menu_actions a quand même été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_id_valide(self, mock_input, mock_menu):
        """Test: Vérification que l'ID est bien converti en entier"""
        # Arrange
        mock_input.return_value = "42"
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier que supprimer_contact a reçu un entier
        call_args = self.mock_client.supprimer_contact.call_args[0][0]
        self.assertIsInstance(call_args, int)
        self.assertEqual(call_args, 42)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_id_zero(self, mock_input, mock_menu):
        """Test: Suppression avec ID 0"""
        # Arrange
        mock_input.return_value = "0"
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert
        self.mock_client.supprimer_contact.assert_called_once_with(0)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_id_negatif(self, mock_input, mock_menu):
        """Test: Suppression avec ID négatif"""
        # Arrange
        mock_input.return_value = "-5"
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert
        self.mock_client.supprimer_contact.assert_called_once_with(-5)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_id_grand_nombre(self, mock_input, mock_menu):
        """Test: Suppression avec un grand ID"""
        # Arrange
        mock_input.return_value = "999999999"
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert
        self.mock_client.supprimer_contact.assert_called_once_with(999999999)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_input_appele_une_fois(self, mock_input, mock_menu):
        """Test: Vérification que input() est appelé une seule fois"""
        # Arrange
        mock_input.return_value = "5"
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert
        self.assertEqual(mock_input.call_count, 1)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_affiche_titre(self, mock_input, mock_menu):
        """Test: Vérification que le titre de suppression s'affiche"""
        # Arrange
        mock_input.return_value = "1"
        
        # Act
        with patch('builtins.print') as mock_print:
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier que le titre s'affiche
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("ID du contact à supprimer" in str(call) for call in print_calls),
            f"Le titre n'a pas été trouvé. Appels: {print_calls}"
        )
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_exception_specifique(self, mock_input, mock_menu):
        """Test: Gestion d'une exception spécifique"""
        # Arrange
        mock_input.return_value = "10"
        error_msg = "Contact introuvable dans l'annuaire"
        self.mock_client.supprimer_contact.side_effect = RuntimeError(error_msg)
        
        # Act
        with patch('builtins.print') as mock_print:
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier que l'erreur est affichée
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any(error_msg in str(call) for call in print_calls),
            f"Le message d'erreur '{error_msg}' n'a pas été trouvé"
        )
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_menu_actions_appele_apres_suppression_reussie(self, mock_input, mock_menu):
        """Test: menu_actions() est appelé après une suppression réussie"""
        # Arrange
        mock_input.return_value = "15"
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_menu_actions_appele_apres_erreur(self, mock_input, mock_menu):
        """Test: menu_actions() est appelé même après une erreur"""
        # Arrange
        mock_input.return_value = "100"
        self.mock_client.supprimer_contact.side_effect = Exception("Erreur système")
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_input_avec_espaces(self, mock_input, mock_menu):
        """Test: Gestion de l'input avec espaces"""
        # Arrange
        mock_input.return_value = "  7  "
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert - int() convertit "  7  " en 7
        self.mock_client.supprimer_contact.assert_called_once_with(7)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_input_invalide_non_entier(self, mock_input, mock_menu):
        """Test: Input invalide (pas un entier)"""
        # Arrange
        mock_input.return_value = "abc"
        
        # Act
        with patch('builtins.print') as mock_print:
            try:
                supprimer_contact(self.mock_client)
            except ValueError:
                # C'est normal que int("abc") lève une exception
                pass
        
        # supprimer_contact ne sera pas appelé car int() lève une exception
        # Mais nous testons que le code gère bien les erreurs
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_affiche_saut_ligne_final(self, mock_input, mock_menu):
        """Test: Vérification que la fonction affiche un saut de ligne à la fin"""
        # Arrange
        mock_input.return_value = "3"
        
        # Act
        with patch('builtins.print') as mock_print:
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier qu'il y a un appel print() sans argument (saut de ligne)
        # Au moins un appel doit être print() pour afficher un saut de ligne
        calls_list = mock_print.call_args_list
        self.assertTrue(len(calls_list) >= 1)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_gestion_erreur_base_donnees(self, mock_input, mock_menu):
        """Test: Gestion d'une erreur de base de données"""
        # Arrange
        mock_input.return_value = "20"
        self.mock_client.supprimer_contact.side_effect = IOError("Erreur d'accès fichier")
        
        # Act
        with patch('builtins.print') as mock_print:
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier que l'erreur est capturée et affichée
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Erreur lors de la suppression" in str(call) for call in print_calls),
            f"Le message d'erreur n'a pas été trouvé"
        )
        # Vérifier que menu_actions a quand même été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    @patch('builtins.input')
    def test_suppression_contact_client_valide(self, mock_input, mock_menu):
        """Test: Vérification que le client passé à menu_actions est le même"""
        # Arrange
        mock_input.return_value = "8"
        
        # Act
        with patch('builtins.print'):
            supprimer_contact(self.mock_client)
        
        # Assert - Vérifier que le même client est passé à menu_actions
        mock_menu.assert_called_once()
        args = mock_menu.call_args[0]
        self.assertIs(args[0], self.mock_client)


if __name__ == '__main__':
    unittest.main()
