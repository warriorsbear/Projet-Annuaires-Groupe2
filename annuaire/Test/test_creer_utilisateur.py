"""
Tests unitaires pour la fonction creer_utilisateur()
"""

import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock
import sys
from pathlib import Path
import csv
import tempfile
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import creer_utilisateur


class TestCreerUtilisateur(unittest.TestCase):
    """Classe de tests pour la fonction creer_utilisateur()"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_admin = Mock()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        # Nettoyer les fichiers temporaires
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_creer_utilisateur_succes(self, mock_input, mock_data_dir, mock_menu):
        """Test: Création d'un utilisateur avec succès"""
        # Arrange
        mock_input.side_effect = ['nouveau@example.com', 'motdepasse123']
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec l'en-tête
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=["id_client", "email", "hash_mdp", "chemin_annuaire"]
            )
            writer.writeheader()
        
        # Configurer le mock admin.creer_utilisateur()
        self.mock_admin.creer_utilisateur.return_value = {
            'identifiant': 'uuid-1234-5678',
            'mail': 'nouveau@example.com',
            'hash_mot_de_passe': 'hash_abcd1234',
            'chemin_annuaire': 'data/uuid-1234-5678.csv'
        }
        
        # Act
        with patch('builtins.print') as mock_print:
            creer_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que creer_utilisateur a été appelé
        self.mock_admin.creer_utilisateur.assert_called_once_with('nouveau@example.com', 'motdepasse123')
        
        # Vérifier que le message de succès a été affiché
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("créé avec succès" in str(call) for call in print_calls),
            f"Le message de succès n'a pas été trouvé. Appels: {print_calls}"
        )
        
        # Vérifier que l'utilisateur a été ajouté au CSV
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['email'], 'nouveau@example.com')
            self.assertEqual(rows[0]['hash_mdp'], 'hash_abcd1234')
        
        # Vérifier que le menu admin a été rappelé
        mock_menu.assert_called_once_with(self.mock_admin)
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_creer_utilisateur_email_existant(self, mock_input, mock_data_dir, mock_menu):
        """Test: Tentative de création avec un email existant"""
        # Arrange
        mock_input.side_effect = ['existant@example.com', 'motdepasse123']
        
        # Créer un fichier CSV temporaire avec un utilisateur existant
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=["id_client", "email", "hash_mdp", "chemin_annuaire"]
            )
            writer.writeheader()
            writer.writerow({
                'id_client': 'uuid-existing',
                'email': 'existant@example.com',
                'hash_mdp': 'hash_existing',
                'chemin_annuaire': 'data/uuid-existing.csv'
            })
        
        # Act
        with patch('builtins.print') as mock_print:
            creer_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que le message d'erreur a été affiché
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(
            any("existe déjà" in str(call) for call in print_calls),
            f"Le message d'erreur n'a pas été trouvé. Appels: {print_calls}"
        )
        
        # Vérifier que creer_utilisateur n'a pas été appelé
        self.mock_admin.creer_utilisateur.assert_not_called()
        
        # Vérifier que le menu admin a quand même été rappelé
        mock_menu.assert_called_once_with(self.mock_admin)
    
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_creer_utilisateur_multiple(self, mock_input, mock_data_dir, mock_menu):
        """Test: Création de plusieurs utilisateurs successivement"""
        # Arrange
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=["id_client", "email", "hash_mdp", "chemin_annuaire"]
            )
            writer.writeheader()
        
        # Créer le premier utilisateur
        mock_input.side_effect = ['user1@example.com', 'pass1']
        self.mock_admin.creer_utilisateur.return_value = {
            'identifiant': 'uuid-user1',
            'mail': 'user1@example.com',
            'hash_mot_de_passe': 'hash_user1',
            'chemin_annuaire': 'data/uuid-user1.csv'
        }
        
        with patch('builtins.print'):
            creer_utilisateur(self.mock_admin)
        
        # Créer le deuxième utilisateur
        mock_input.side_effect = ['user2@example.com', 'pass2']
        self.mock_admin.creer_utilisateur.return_value = {
            'identifiant': 'uuid-user2',
            'mail': 'user2@example.com',
            'hash_mot_de_passe': 'hash_user2',
            'chemin_annuaire': 'data/uuid-user2.csv'
        }
        
        with patch('builtins.print'):
            creer_utilisateur(self.mock_admin)
        
        # Assert
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['email'], 'user1@example.com')
            self.assertEqual(rows[1]['email'], 'user2@example.com')
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_creer_utilisateur_donnees_csv(self, mock_input, mock_data_dir, mock_menu):
        """Test: Vérification que toutes les données sont correctement écrites dans le CSV"""
        # Arrange
        mock_input.side_effect = ['test@example.com', 'secure_pass']
        
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f, 
                fieldnames=["id_client", "email", "hash_mdp", "chemin_annuaire"]
            )
            writer.writeheader()
        
        self.mock_admin.creer_utilisateur.return_value = {
            'identifiant': 'test-uuid-1234',
            'mail': 'test@example.com',
            'hash_mot_de_passe': 'hash_secure_pass',
            'chemin_annuaire': 'data/test-uuid-1234.csv'
        }
        
        # Act
        with patch('builtins.print'):
            creer_utilisateur(self.mock_admin)
        
        # Assert
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            row = next(reader)
            
            self.assertEqual(row['id_client'], 'test-uuid-1234')
            self.assertEqual(row['email'], 'test@example.com')
            self.assertEqual(row['hash_mdp'], 'hash_secure_pass')
            self.assertEqual(row['chemin_annuaire'], 'data/test-uuid-1234.csv')


if __name__ == '__main__':
    unittest.main()
