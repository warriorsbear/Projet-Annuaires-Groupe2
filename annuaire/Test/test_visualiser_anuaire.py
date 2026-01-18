"""
Tests unitaires pour la fonction visualiser_annuaire()
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import visualiser_annuaire


class TestVisualiserAnnuaire(unittest.TestCase):
    """Classe de tests pour la fonction visualiser_annuaire()"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_client = Mock()
    
    @patch('main.menu_actions')
    def test_annuaire_vide(self, mock_menu):
        """Test: Affichage d'un message quand l'annuaire est vide"""
        # Arrange
        self.mock_client.lister_contacts.return_value = []
        self.mock_client.mail = "test@example.com"
        
        # Act
        with patch('builtins.print') as mock_print:
            visualiser_annuaire(self.mock_client)
        
        # Assert
        mock_print.assert_called()
        print_calls = [str(call) for call in mock_print.call_args_list]
        
        # Vérifier qu'un message indique "Aucun contact"
        self.assertTrue(
            any("Aucun contact dans l'annuaire" in str(call) for call in print_calls),
            f"Le message 'Aucun contact' n'a pas été trouvé. Appels: {print_calls}"
        )
        # Vérifier que menu_actions a été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    def test_annuaire_avec_un_contact(self, mock_menu):
        """Test: Affichage correct avec un seul contact"""
        # Arrange
        contact = {
            'id_contact': 1,
            'prenom': 'Jean',
            'nom': 'Dupont',
            'email': 'jean@example.com',
            'adresse': '123 Rue de la Paix',
            'telephone': '0123456789'
        }
        self.mock_client.lister_contacts.return_value = [contact]
        self.mock_client.mail = "user@example.com"
        
        # Act
        with patch('builtins.print') as mock_print:
            visualiser_annuaire(self.mock_client)
        
        # Assert
        mock_print.assert_called()
        print_calls = [str(call) for call in mock_print.call_args_list]
        
        # Vérifier que les informations du contact sont affichées
        self.assertTrue(
            any("Jean" in str(call) and "Dupont" in str(call) for call in print_calls),
            f"Les informations du contact n'ont pas été trouvées. Appels: {print_calls}"
        )
        self.assertTrue(
            any("1 contact" in str(call) for call in print_calls),
            f"Le compteur de contact n'a pas été trouvé. Appels: {print_calls}"
        )
        # Vérifier que menu_actions a été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    def test_annuaire_avec_plusieurs_contacts(self, mock_menu):
        """Test: Affichage correct avec plusieurs contacts"""
        # Arrange
        contacts = [
            {
                'id_contact': 1,
                'prenom': 'Jean',
                'nom': 'Dupont',
                'email': 'jean@example.com',
                'adresse': '123 Rue de la Paix',
                'telephone': '0123456789'
            },
            {
                'id_contact': 2,
                'prenom': 'Marie',
                'nom': 'Martin',
                'email': 'marie@example.com',
                'adresse': '456 Avenue de Paris',
                'telephone': '0987654321'
            },
            {
                'id_contact': 3,
                'prenom': 'Paul',
                'nom': 'Bernard',
                'email': 'paul@example.com',
                'adresse': '789 Boulevard du Sud',
                'telephone': '0555555555'
            }
        ]
        self.mock_client.lister_contacts.return_value = contacts
        self.mock_client.mail = "admin@example.com"
        
        # Act
        with patch('builtins.print') as mock_print:
            visualiser_annuaire(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        
        # Vérifier que le nombre de contacts est correct
        self.assertTrue(
            any("3 contact" in str(call) for call in print_calls),
            f"Le compteur '3 contacts' n'a pas été trouvé. Appels: {print_calls}"
        )
        
        # Vérifier que tous les contacts sont affichés
        for contact in contacts:
            self.assertTrue(
                any(contact['prenom'] in str(call) and contact['nom'] in str(call) 
                    for call in print_calls),
                f"Le contact {contact['prenom']} {contact['nom']} n'a pas été trouvé"
            )
        
        # Vérifier que menu_actions a été appelé
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    def test_annuaire_emails_telephones_affiches(self, mock_menu):
        """Test: Vérification que les emails et téléphones sont affichés"""
        # Arrange
        contact = {
            'id_contact': 1,
            'prenom': 'Luc',
            'nom': 'Renaud',
            'email': 'luc.renaud@company.com',
            'adresse': '999 Rue Principale',
            'telephone': '+33612345678'
        }
        self.mock_client.lister_contacts.return_value = [contact]
        self.mock_client.mail = "user@example.com"
        
        # Act
        with patch('builtins.print') as mock_print:
            visualiser_annuaire(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        
        # Vérifier que l'email et le téléphone sont affichés
        self.assertTrue(
            any('luc.renaud@company.com' in str(call) for call in print_calls),
            f"L'email n'a pas été trouvé. Appels: {print_calls}"
        )
        self.assertTrue(
            any('+33612345678' in str(call) for call in print_calls),
            f"Le téléphone n'a pas été trouvé. Appels: {print_calls}"
        )
    
    @patch('main.menu_actions')
    def test_menu_actions_appele_apres_affichage(self, mock_menu):
        """Test: Vérification que menu_actions est toujours appelé après affichage"""
        # Arrange
        self.mock_client.lister_contacts.return_value = []
        self.mock_client.mail = "test@example.com"
        
        # Act
        with patch('builtins.print'):
            visualiser_annuaire(self.mock_client)
        
        # Assert
        mock_menu.assert_called_once_with(self.mock_client)
    
    @patch('main.menu_actions')
    def test_affichage_nom_utilisateur(self, mock_menu):
        """Test: Vérification que le nom de l'utilisateur est affiché"""
        # Arrange
        contact = {
            'id_contact': 1,
            'prenom': 'Sophie',
            'nom': 'Lefevre',
            'email': 'sophie@example.com',
            'adresse': '321 Rue Louise',
            'telephone': '0111111111'
        }
        self.mock_client.lister_contacts.return_value = [contact]
        self.mock_client.mail = "sophie.lefevre@email.com"
        
        # Act
        with patch('builtins.print') as mock_print:
            visualiser_annuaire(self.mock_client)
        
        # Assert
        print_calls = [str(call) for call in mock_print.call_args_list]
        
        # Vérifier que l'email de l'utilisateur est affiché
        self.assertTrue(
            any("sophie.lefevre@email.com" in str(call) for call in print_calls),
            f"L'email utilisateur n'a pas été trouvé. Appels: {print_calls}"
        )
    
    @patch('main.menu_actions')
    def test_lister_contacts_appele_une_fois(self, mock_menu):
        """Test: Vérification que lister_contacts() est appelé une seule fois"""
        # Arrange
        self.mock_client.lister_contacts.return_value = []
        self.mock_client.mail = "test@example.com"
        
        # Act
        with patch('builtins.print'):
            visualiser_annuaire(self.mock_client)
        
        # Assert
        self.mock_client.lister_contacts.assert_called_once()
    
    @patch('main.menu_actions')
    def test_contact_sans_certains_champs(self, mock_menu):
        """Test: Gestion des contacts avec certains champs manquants"""
        # Arrange
        contact = {
            'id_contact': 1,
            'prenom': 'Marc',
            'nom': 'Blanc'
            # email, adresse, telephone manquants
        }
        self.mock_client.lister_contacts.return_value = [contact]
        self.mock_client.mail = "test@example.com"
        
        # Act
        with patch('builtins.print') as mock_print:
            visualiser_annuaire(self.mock_client)
        
        # Assert
        # La fonction doit s'exécuter sans erreur même si certains champs manquent
        mock_print.assert_called()
        # Vérifier que le nom et prénom sont toujours affichés
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("Marc" in str(call) and "Blanc" in str(call) for call in print_calls),
            f"Les champs disponibles n'ont pas été trouvés. Appels: {print_calls}"
        )


if __name__ == '__main__':
    unittest.main()
