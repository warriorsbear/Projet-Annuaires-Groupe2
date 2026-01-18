"""
Tests unitaires pour la fonction modifier_utilisateur()
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import csv
import tempfile
import os
import hashlib

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import modifier_utilisateur, ADMIN_EMAIL


class TestModifierUtilisateur(unittest.TestCase):
    """Classe de tests pour la fonction modifier_utilisateur()"""
    
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
    def test_modifier_utilisateur_email_succes(self, mock_input, mock_data_dir, mock_menu):
        """Test: Modification du nouvel email d'un utilisateur avec succès"""
        # Arrange
        mock_input.side_effect = [
            'user@example.com',  # Email de l'utilisateur à modifier
            'newemail@example.com',  # Nouvel email
            ''  # Pas de modification du mot de passe
        ]
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec des données
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": "uuid-user",
                "email": "user@example.com",
                "hash_mdp": "hash_user",
                "chemin_annuaire": "data/user.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        modifier_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que l'email a été modifié
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 1)
            self.assertEqual(lignes[0]['email'], 'newemail@example.com')
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_modifier_utilisateur_mdp_succes(self, mock_input, mock_data_dir, mock_menu):
        """Test: Modification du mot de passe d'un utilisateur avec succès"""
        # Arrange
        nouveau_mdp = "newpassword123"
        nouveau_hash = hashlib.sha256(nouveau_mdp.encode()).hexdigest()
        
        mock_input.side_effect = [
            'user@example.com',  # Email de l'utilisateur à modifier
            '',  # Pas de modification du nouvel email
            nouveau_mdp  # Nouveau mot de passe
        ]
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec des données
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": "uuid-user",
                "email": "user@example.com",
                "hash_mdp": "old_hash",
                "chemin_annuaire": "data/user.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        modifier_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que le mot de passe a été modifié
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 1)
            self.assertEqual(lignes[0]['hash_mdp'], nouveau_hash)
            self.assertEqual(lignes[0]['email'], 'user@example.com')
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_modifier_utilisateur_email_et_mdp(self, mock_input, mock_data_dir, mock_menu):
        """Test: Modification du nouvel email ET du mot de passe d'un utilisateur"""
        # Arrange
        nouveau_mdp = "newpassword123"
        nouveau_hash = hashlib.sha256(nouveau_mdp.encode()).hexdigest()
        
        mock_input.side_effect = [
            'user@example.com',  # Email de l'utilisateur à modifier
            'newemail@example.com',  # Nouvel email
            nouveau_mdp  # Nouveau mot de passe
        ]
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec des données
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": "uuid-user",
                "email": "user@example.com",
                "hash_mdp": "old_hash",
                "chemin_annuaire": "data/user.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        modifier_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que l'email et le mot de passe ont été modifiés
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 1)
            self.assertEqual(lignes[0]['email'], 'newemail@example.com')
            self.assertEqual(lignes[0]['hash_mdp'], nouveau_hash)
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_modifier_utilisateur_inexistant(self, mock_print, mock_input, mock_data_dir, mock_menu):
        """Test: Modification d'un utilisateur qui n'existe pas"""
        # Arrange
        mock_input.side_effect = [
            'inexistant@example.com',  # Email de l'utilisateur à modifier
            '',
            ''
        ]
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec un seul utilisateur
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": "uuid-admin",
                "email": ADMIN_EMAIL,
                "hash_mdp": "hash_admin",
                "chemin_annuaire": "data/admin.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        modifier_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que le fichier n'a pas changé
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 1)
            self.assertEqual(lignes[0]['email'], ADMIN_EMAIL)
        
        # Vérifier que le message d'erreur a été affiché
        error_message = mock_print.call_args_list
        self.assertTrue(any("n'existe pas" in str(call) for call in error_message))
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_modifier_utilisateur_fichier_inexistant(self, mock_print, mock_input, mock_data_dir, mock_menu):
        """Test: Modification quand le fichier clients.csv n'existe pas"""
        # Arrange
        mock_input.return_value = 'user@example.com'
        
        # Créer un chemin vers un fichier qui n'existe pas
        csv_path = Path(self.temp_dir) / "clients_inexistant.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Act
        modifier_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que le message d'erreur approprié a été affiché
        error_message = mock_print.call_args_list
        self.assertTrue(any("Aucun utilisateur trouvé" in str(call) for call in error_message))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_modifier_utilisateur_sans_changement(self, mock_input, mock_data_dir, mock_menu):
        """Test: Modification d'un utilisateur sans effectuer de changement"""
        # Arrange
        mock_input.side_effect = [
            'user@example.com',  # Email de l'utilisateur à modifier
            '',  # Pas de nouvel email
            ''  # Pas de nouveau mot de passe
        ]
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec des données
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": "uuid-user",
                "email": "user@example.com",
                "hash_mdp": "hash_user",
                "chemin_annuaire": "data/user.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        modifier_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que l'utilisateur reste inchangé
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 1)
            self.assertEqual(lignes[0]['email'], 'user@example.com')
            self.assertEqual(lignes[0]['hash_mdp'], 'hash_user')
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    def test_modifier_utilisateur_parmi_plusieurs(self, mock_input, mock_data_dir, mock_menu):
        """Test: Modification d'un utilisateur parmi plusieurs"""
        # Arrange
        mock_input.side_effect = [
            'user2@example.com',  # Email de l'utilisateur à modifier
            'updated@example.com',  # Nouvel email
            ''  # Pas de modification du mot de passe
        ]
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec plusieurs utilisateurs
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": "uuid-user1",
                "email": "user1@example.com",
                "hash_mdp": "hash_user1",
                "chemin_annuaire": "data/user1.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
            writer.writerow({
                "id_client": "uuid-user2",
                "email": "user2@example.com",
                "hash_mdp": "hash_user2",
                "chemin_annuaire": "data/user2.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
            writer.writerow({
                "id_client": "uuid-user3",
                "email": "user3@example.com",
                "hash_mdp": "hash_user3",
                "chemin_annuaire": "data/user3.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        modifier_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que seul user2 a été modifié
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 3)
            # Vérifier les emails
            emails = [row['email'] for row in lignes]
            self.assertIn('user1@example.com', emails)
            self.assertIn('updated@example.com', emails)  # user2 modifié
            self.assertIn('user3@example.com', emails)
            self.assertNotIn('user2@example.com', emails)


if __name__ == '__main__':
    unittest.main()
