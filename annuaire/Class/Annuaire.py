"""
Classe Annuaire - Conteneur des contacts associé à un utilisateur.
Aucune logique réseau intégrée : modélisation stricte des données et des opérations.
"""

import os
import csv
from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .Client import Client


class Annuaire:
    """
    Conteneur des contacts associé à un utilisateur.
    """
    
    def __init__(self, proprietaire: 'Client', fichier_csv: str):
        """
        Initialise un annuaire.
        
        Args:
            proprietaire: Utilisateur propriétaire de l'annuaire
            fichier_csv: Chemin vers le fichier CSV de l'annuaire
        """
        self.proprietaire = proprietaire
        self.fichier_csv = fichier_csv
        self.contacts: List[Dict] = []
    
    def charger(self):
        """
        Charge les contacts depuis le fichier CSV.
        """
        self.contacts = []
        if os.path.exists(self.fichier_csv):
            try:
                with open(self.fichier_csv, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Conversion de l'id_contact en int
                        if row.get('id_contact'):
                            row['id_contact'] = int(row['id_contact'])
                        self.contacts.append(row)
            except Exception as e:
                # En cas d'erreur, on démarre avec une liste vide
                self.contacts = []
    
    def sauvegarder(self):
        """
        Sauvegarde les contacts dans le fichier CSV.
        """
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(self.fichier_csv) if os.path.dirname(self.fichier_csv) else '.', exist_ok=True)
        
        try:
            with open(self.fichier_csv, 'w', encoding='utf-8', newline='') as f:
                if self.contacts:
                    fieldnames = ['id_contact', 'nom', 'prenom', 'email', 'telephone', 'adresse']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for contact in self.contacts:
                        writer.writerow(contact)
                else:
                    # Écrire juste l'en-tête si aucun contact
                    writer = csv.DictWriter(f, fieldnames=['id_contact', 'nom', 'prenom', 'email', 'telephone', 'adresse'])
                    writer.writeheader()
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde de l'annuaire : {e}")
    
    def ajouter(self, contact: Dict):
        """
        Ajoute un contact à l'annuaire.
        
        Args:
            contact: Dictionnaire contenant les données du contact
        """
        # Vérifier que le contact a les champs obligatoires
        if not all(k in contact for k in ['nom', 'prenom', 'email']):
            raise ValueError("Le contact doit contenir au minimum : nom, prenom, email")

        # Générer automatiquement un nouvel id_contact si nécessaire
        if self.contacts:
            # Récupérer le max des id existants (en supposant des entiers)
            max_id = max(int(c.get('id_contact', 0) or 0) for c in self.contacts)
        else:
            max_id = 0

        contact['id_contact'] = max_id + 1

        self.contacts.append(contact)
    
    def supprimer(self, id_contact: int):
        """
        Supprime un contact de l'annuaire.
        
        Args:
            id_contact: Identifiant du contact à supprimer
        """
        if not any(c['id_contact'] == id_contact for c in self.contacts):
            raise ValueError(f"Aucun contact avec l'ID {id_contact} trouvé")
        self.contacts = [c for c in self.contacts if c['id_contact'] != id_contact]
    
    def rechercher(self, criteres: Dict) -> List[Dict]:
        """
        Recherche des contacts selon des critères.
        
        Args:
            criteres: Dictionnaire de critères de recherche
            
        Returns:
            Liste des contacts correspondant aux critères
        """
        resultats = self.contacts.copy()
        
        for critere, valeur in criteres.items():
            if critere == 'id_contact':
                resultats = [c for c in resultats if c.get('id_contact') == valeur]
            elif critere == 'nom':
                resultats = [c for c in resultats if valeur.lower() in c.get('nom', '').lower()]
            elif critere == 'prenom':
                resultats = [c for c in resultats if valeur.lower() in c.get('prenom', '').lower()]
            elif critere == 'email':
                resultats = [c for c in resultats if valeur.lower() in c.get('email', '').lower()]
            elif critere == 'telephone':
                resultats = [c for c in resultats if valeur in c.get('telephone', '')]
            elif critere == 'adresse':
                resultats = [c for c in resultats if valeur.lower() in c.get('adresse', '').lower()]
        
        return resultats
    
    def lister(self) -> List[Dict]:
        """
        Liste tous les contacts de l'annuaire.
        
        Returns:
            Liste de tous les contacts
        """
        return self.contacts.copy()
    
    