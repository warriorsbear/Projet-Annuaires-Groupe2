"""
Tests unitaires pour la fonction lister_utilisateurs()
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

from main import lister_utilisateurs, ADMIN_EMAIL


class TestListerUtilisateurs(unittest.TestCase):
    """Classe de tests pour la fonction lister_utilisateurs()"""
    
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
    @patch('builtins.print')
    def test_lister_utilisateurs_succes_multiple(self, mock_print, mock_data_dir, mock_menu):
        """Test: Listing de plusieurs utilisateurs avec succès"""
        # Arrange
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
        lister_utilisateurs(self.mock_admin)
        
        # Assert
        # Vérifier que les utilisateurs ont été affichés
        printed_output = mock_print.call_args_list
        output_str = ''.join([str(call) for call in printed_output])
        
        self.assertTrue(any("Liste des utilisateurs" in str(call) for call in printed_output))
        self.assertTrue(any(ADMIN_EMAIL in str(call) for call in printed_output))
        self.assertTrue(any("user1@example.com" in str(call) for call in printed_output))
        self.assertTrue(any("user2@example.com" in str(call) for call in printed_output))
        self.assertTrue(any("Administrateur" in str(call) for call in printed_output))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.print')
    def test_lister_utilisateurs_seul_admin(self, mock_print, mock_data_dir, mock_menu):
        """Test: Listing quand seul l'admin existe"""
        # Arrange
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Initialiser le fichier CSV avec seulement l'admin
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
        lister_utilisateurs(self.mock_admin)
        
        # Assert
        printed_output = mock_print.call_args_list
        
        self.assertTrue(any("Liste des utilisateurs" in str(call) for call in printed_output))
        self.assertTrue(any("1 utilisateur" in str(call) for call in printed_output))
        self.assertTrue(any(ADMIN_EMAIL in str(call) for call in printed_output))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.print')
    def test_lister_utilisateurs_fichier_inexistant(self, mock_print, mock_data_dir, mock_menu):
        """Test: Listing quand le fichier clients.csv n'existe pas"""
        # Arrange
        csv_path = Path(self.temp_dir) / "clients_inexistant.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        # Act
        lister_utilisateurs(self.mock_admin)
        
        # Assert
        printed_output = mock_print.call_args_list
        
        self.assertTrue(any("Aucun utilisateur trouvé" in str(call) for call in printed_output))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.print')
    def test_lister_utilisateurs_affichage_roles(self, mock_print, mock_data_dir, mock_menu):
        """Test: Vérifier que les rôles sont correctement affichés"""
        # Arrange
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
            writer.writerow({
                "id_client": "uuid-client",
                "email": "client@example.com",
                "hash_mdp": "hash_client",
                "chemin_annuaire": "data/client.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        lister_utilisateurs(self.mock_admin)
        
        # Assert
        printed_output = mock_print.call_args_list
        output_str = ''.join([str(call) for call in printed_output])
        
        # Vérifier que les rôles sont affichés
        self.assertTrue(any("Administrateur" in str(call) for call in printed_output))
        self.assertTrue(any("Client" in str(call) for call in printed_output))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.print')
    def test_lister_utilisateurs_affiche_identifiants(self, mock_print, mock_data_dir, mock_menu):
        """Test: Vérifier que les identifiants sont affichés"""
        # Arrange
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        user_id = "uuid-12345"
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": user_id,
                "email": "user@example.com",
                "hash_mdp": "hash_user",
                "chemin_annuaire": "data/user.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        lister_utilisateurs(self.mock_admin)
        
        # Assert
        printed_output = mock_print.call_args_list
        
        # Vérifier que l'ID est affiché
        self.assertTrue(any(user_id in str(call) for call in printed_output))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.print')
    def test_lister_utilisateurs_format_output(self, mock_print, mock_data_dir, mock_menu):
        """Test: Vérifier le format de sortie"""
        # Arrange
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id_client": "uuid-user",
                "email": "test@example.com",
                "hash_mdp": "hash",
                "chemin_annuaire": "data/test.csv",
                "liste_permissions_accordees": "[]",
                "liste_permissions_recues": "[]"
            })
        
        # Act
        lister_utilisateurs(self.mock_admin)
        
        # Assert
        printed_output = mock_print.call_args_list
        
        # Vérifier que les éléments clés sont présents
        self.assertTrue(any("Email:" in str(call) for call in printed_output))
        self.assertTrue(any("ID:" in str(call) for call in printed_output))
        self.assertTrue(any("Rôle:" in str(call) for call in printed_output))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()
    
    @patch('main.menu_actions_admin')
    @patch('main.data_dir')
    @patch('builtins.print')
    def test_lister_utilisateurs_plusieurs_clients(self, mock_print, mock_data_dir, mock_menu):
        """Test: Listing avec plusieurs clients (pas d'admin parmi eux)"""
        # Arrange
        csv_path = Path(self.temp_dir) / "clients.csv"
        mock_data_dir.__truediv__ = Mock(return_value=csv_path)
        
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(1, 4):
                writer.writerow({
                    "id_client": f"uuid-client{i}",
                    "email": f"client{i}@example.com",
                    "hash_mdp": f"hash_client{i}",
                    "chemin_annuaire": f"data/client{i}.csv",
                    "liste_permissions_accordees": "[]",
                    "liste_permissions_recues": "[]"
                })
        
        # Act
        lister_utilisateurs(self.mock_admin)
        
        # Assert
        printed_output = mock_print.call_args_list
        output_str = ''.join([str(call) for call in printed_output])
        
        # Vérifier que tous les clients sont affichés
        self.assertTrue(any("client1@example.com" in str(call) for call in printed_output))
        self.assertTrue(any("client2@example.com" in str(call) for call in printed_output))
        self.assertTrue(any("client3@example.com" in str(call) for call in printed_output))
        self.assertTrue(any("3 utilisateur" in str(call) for call in printed_output))
        
        # Vérifier que menu_actions_admin a été appelé
        mock_menu.assert_called_once()


if __name__ == '__main__':
    unittest.main()
