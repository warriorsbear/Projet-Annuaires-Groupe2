"""
Tests unitaires pour la fonction supprimer_utilisateur()
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import csv
import tempfile
import os

# Ajouter le chemin pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "Class"))
sys.path.insert(0, str(Path(__file__).parent.parent / "programme"))

from main import supprimer_utilisateur, ADMIN_EMAIL


class TestSupprimerUtilisateur(unittest.TestCase):
    """Classe de tests pour la fonction supprimer_utilisateur()"""
    
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
    def test_supprimer_utilisateur_succes(self, mock_input, mock_data_dir, mock_menu):
        """Test: Suppression d'un utilisateur avec succès"""
        # Arrange
        mock_input.return_value = 'user@example.com'
        
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
                "id_client": "uuid-admin",
                "email": ADMIN_EMAIL,
                "hash_mdp": "hash_admin",
                "chemin_annuaire": "data/admin.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
            writer.writerow({
                "id_client": "uuid-user",
                "email": "user@example.com",
                "hash_mdp": "hash_user",
                "chemin_annuaire": "data/user.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        supprimer_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que le fichier a été modifié
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            # Il ne doit rester que l'admin
            self.assertEqual(len(lignes), 1)
            self.assertEqual(lignes[0]['email'], ADMIN_EMAIL)
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_supprimer_admin_echoue(self, mock_print, mock_input, mock_data_dir, mock_menu):
        """Test: Tentative de suppression de l'admin devrait échouer"""
        # Arrange
        mock_input.return_value = ADMIN_EMAIL  # Essayer de supprimer l'admin
        
        # Créer un fichier CSV temporaire
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV
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
        supprimer_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que l'admin est toujours dans le fichier
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 1)
            self.assertEqual(lignes[0]['email'], ADMIN_EMAIL)
        
        # Vérifier que le message d'erreur a été affiché
        error_message = mock_print.call_args_list
        self.assertTrue(any("Impossible de supprimer" in str(call) for call in error_message))
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_supprimer_utilisateur_inexistant(self, mock_print, mock_input, mock_data_dir, mock_menu):
        """Test: Suppression d'un utilisateur qui n'existe pas"""
        # Arrange
        mock_input.return_value = 'inexistant@example.com'
        
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
        supprimer_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que le fichier n'a pas changé
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 1)
        
        # Vérifier que le message d'erreur a été affiché
        error_message = mock_print.call_args_list
        self.assertTrue(any("n'existe pas" in str(call) for call in error_message))
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_supprimer_utilisateur_fichier_inexistant(self, mock_print, mock_input, mock_data_dir, mock_menu):
        """Test: Suppression quand le fichier clients.csv n'existe pas"""
        # Arrange
        mock_input.return_value = 'user@example.com'
        
        # Créer un chemin vers un fichier qui n'existe pas
        csv_path = Path(self.temp_dir) / "clients_inexistant.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Act
        supprimer_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que le message d'erreur approprié a été affiché
        error_message = mock_print.call_args_list
        self.assertTrue(any("Aucun utilisateur trouvé" in str(call) for call in error_message))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_supprimer_utilisateur_multiple(self, mock_print, mock_input, mock_data_dir, mock_menu):
        """Test: Suppression d'un utilisateur parmi plusieurs"""
        # Arrange
        mock_input.return_value = 'user2@example.com'
        
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
                "id_client": "uuid-admin",
                "email": ADMIN_EMAIL,
                "hash_mdp": "hash_admin",
                "chemin_annuaire": "data/admin.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
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
        
        # Act
        supprimer_utilisateur(self.mock_admin)
        
        # Assert
        # Vérifier que seul user2 a été supprimé
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes = list(reader)
            self.assertEqual(len(lignes), 2)
            emails = [row['email'] for row in lignes]
            self.assertIn(ADMIN_EMAIL, emails)
            self.assertIn('user1@example.com', emails)
            self.assertNotIn('user2@example.com', emails)
        
        # Vérifier le message de succès
        success_message = mock_print.call_args_list
        self.assertTrue(any("supprimé avec succès" in str(call) for call in success_message))


if __name__ == '__main__':
    unittest.main()
