"""
Classe Contact - Représente un contact dans l'annuaire.
Aucune logique réseau intégrée : modélisation stricte des données.
"""


class Contact:
    """
    Représente un contact dans l'annuaire.
    """
    
    def __init__(self, id_contact: int, nom: str, prenom: str, email: str, 
                 telephone: str, adresse: str):
        """
        Initialise un contact avec ses informations.
        
        Args:
            id_contact: Identifiant unique du contact
            nom: Nom du contact
            prenom: Prénom du contact
            email: Adresse email du contact
            telephone: Numéro de téléphone du contact
            adresse: Adresse postale du contact
        """
        self.id_contact = id_contact
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
    
    def valider(self) -> bool:
        """
        Valide les données du contact.
        
        Returns:
            True si le contact est valide, False sinon
        """
        if not self.nom or not self.nom.strip():
            return False
        if not self.email or '@' not in self.email:
            return False
        if self.id_contact is None or self.id_contact < 0:
            return False
        return True
    
    def mettre_a_jour(self, champs: dict):
        """
        Met à jour les champs du contact avec les nouvelles valeurs.
        
        Args:
            champs: Dictionnaire contenant les champs à mettre à jour
        """
        if 'nom' in champs:
            self.nom = champs['nom']
        if 'prenom' in champs:
            self.prenom = champs['prenom']
        if 'email' in champs:
            self.email = champs['email']
        if 'telephone' in champs:
            self.telephone = champs['telephone']
        if 'adresse' in champs:
            self.adresse = champs['adresse']
    
    def to_dict(self) -> dict:
        """
        Convertit le contact en dictionnaire.
        
        Returns:
            Dictionnaire contenant les données du contact
        """
        return {
            'id_contact': self.id_contact,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'telephone': self.telephone,
            'adresse': self.adresse
        }
    
    @classmethod
    def from_dict(cls, donnees: dict) -> 'Contact':
        """
        Crée un contact à partir d'un dictionnaire.
        
        Args:
            donnees: Dictionnaire contenant les données du contact
            
        Returns:
            Instance de Contact
        """
        return cls(
            id_contact=donnees.get('id_contact', 0),
            nom=donnees.get('nom', ''),
            prenom=donnees.get('prenom', ''),
            email=donnees.get('email', ''),
            telephone=donnees.get('telephone', ''),
            adresse=donnees.get('adresse', '')
        )

