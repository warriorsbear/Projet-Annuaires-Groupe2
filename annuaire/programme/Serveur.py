import sys
import os
import getpass
import hashlib
import uuid
# Ajouter le dossier parent (annuaire) au chemin Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from typing import Dict, Optional, List
from Class import Client, Administrateur, Annuaire


# Variables globales du serveur
utilisateurs: Dict[str, Client] = {}  # mail -> Client/Administrateur
sessions: Dict[str, Client] = {}  # session_id -> Client


def charger_utilisateurs():
    """Charge les utilisateurs existants depuis un fichier."""
    global utilisateurs
    if os.path.exists("annuaire/data/utilisateurs.json"):
        try:
            with open("annuaire/data/utilisateurs.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                for user_data in data:
                    if user_data.get('est_admin'):
                        user = Administrateur(user_data['mail'], user_data['hash_mot_de_passe'])
                    else:
                        user = Client(user_data['mail'], user_data['hash_mot_de_passe'])
                    user.identifiant = user_data['identifiant']
                    user.chemin_annuaire = user_data['chemin_annuaire']
                    utilisateurs[user.mail] = user
            print(f"{len(utilisateurs)} utilisateur(s) chargé(s).")
        except Exception as e:
            print(f"Erreur lors du chargement des utilisateurs : {e}")


def sauvegarder_utilisateurs():
    """Sauvegarde les utilisateurs dans un fichier."""
    os.makedirs("data", exist_ok=True)
    try:
        data = []
        for user in utilisateurs.values():
            data.append({
                'mail': user.mail,
                'hash_mot_de_passe': user.hash_mot_de_passe,
                'identifiant': user.identifiant,
                'chemin_annuaire': user.chemin_annuaire,
                'est_admin': isinstance(user, Administrateur)
            })
        with open("annuaire/data/utilisateurs.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des utilisateurs : {e}")


def traiter_PDU(pdu: Dict) -> Dict:
    """
    Traite une PDU reçue et retourne une réponse.
    
    Args:
        pdu: Dictionnaire représentant la PDU
        
    Returns:
        Dictionnaire contenant la réponse
    """
    action = pdu.get('action')
    session_id = pdu.get('session_id')
    
    # Actions ne nécessitant pas de session
    if action == 'inscription':
        return traiter_inscription(pdu)
    elif action == 'connexion':
        return traiter_connexion(pdu)
    
    # Vérification de la session pour les autres actions
    if session_id not in sessions:
        return {'status': 'error', 'message': 'Session invalide ou expirée'}
    
    utilisateur = sessions[session_id]
    
    # Actions nécessitant une session
    if action == 'deconnexion':
        return traiter_deconnexion(pdu)
    elif action == 'ajouter_contact':
        return traiter_ajouter_contact(pdu, utilisateur)
    elif action == 'supprimer_contact':
        return traiter_supprimer_contact(pdu, utilisateur)
    elif action == 'modifier_contact':
        return traiter_modifier_contact(pdu, utilisateur)
    elif action == 'rechercher_contact':
        return traiter_rechercher_contact(pdu, utilisateur)
    elif action == 'lister_contacts':
        return traiter_lister_contacts(pdu, utilisateur)
    else:
        return {'status': 'error', 'message': f'Action inconnue : {action}'}


def traiter_inscription(pdu: Dict) -> Dict:
    """Traite une demande d'inscription."""
    mail = pdu.get('mail')
    mot_de_passe = pdu.get('mot_de_passe')
    
    if not mail or not mot_de_passe:
        return {'status': 'error', 'message': 'Mail et mot de passe requis'}
    
    if mail in utilisateurs:
        return {'status': 'error', 'message': 'Cet email est déjà utilisé'}
    
    # Création du nouvel utilisateur
    hash_mdp = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    nouveau_client = Client(mail, hash_mdp)
    utilisateurs[mail] = nouveau_client
    sauvegarder_utilisateurs()
    
    return {'status': 'success', 'message': 'Inscription réussie', 'identifiant': nouveau_client.identifiant}


def traiter_connexion(pdu: Dict) -> Dict:
    """Traite une demande de connexion."""
    mail = pdu.get('mail')
    mot_de_passe = pdu.get('mot_de_passe')
    
    if not mail or not mot_de_passe:
        return {'status': 'error', 'message': 'Mail et mot de passe requis'}
    
    if mail not in utilisateurs:
        return {'status': 'error', 'message': 'Email ou mot de passe incorrect'}
    
    utilisateur = utilisateurs[mail]
    hash_mdp = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    
    if not utilisateur.verifier_mot_de_passe(hash_mdp):
        return {'status': 'error', 'message': 'Email ou mot de passe incorrect'}
    
    # Création de la session
    session_id = str(uuid.uuid4())
    sessions[session_id] = utilisateur
    
    return {
        'status': 'success',
        'message': 'Connexion réussie',
        'session_id': session_id,
        'est_admin': isinstance(utilisateur, Administrateur)
    }


def traiter_deconnexion(pdu: Dict) -> Dict:
    """Traite une demande de déconnexion."""
    session_id = pdu.get('session_id')
    if session_id in sessions:
        del sessions[session_id]
        return {'status': 'success', 'message': 'Déconnexion réussie'}
    return {'status': 'error', 'message': 'Session non trouvée'}


def traiter_ajouter_contact(pdu: Dict, utilisateur: Client) -> Dict:
    """Traite une demande d'ajout de contact."""
    contact = pdu.get('contact')
    if not contact:
        return {'status': 'error', 'message': 'Contact requis'}
    
    try:
        utilisateur.ajouter_contact(contact)
        return {'status': 'success', 'message': 'Contact ajouté'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def traiter_supprimer_contact(pdu: Dict, utilisateur: Client) -> Dict:
    """Traite une demande de suppression de contact."""
    id_contact = pdu.get('id_contact')
    if id_contact is None:
        return {'status': 'error', 'message': 'ID du contact requis'}
    
    try:
        utilisateur.supprimer_contact(id_contact)
        return {'status': 'success', 'message': 'Contact supprimé'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def traiter_modifier_contact(pdu: Dict, utilisateur: Client) -> Dict:
    """Traite une demande de modification de contact."""
    id_contact = pdu.get('id_contact')
    champs = pdu.get('champs')
    
    if id_contact is None or not champs:
        return {'status': 'error', 'message': 'ID et champs requis'}
    
    try:
        utilisateur.modifier_contact(id_contact, champs)
        return {'status': 'success', 'message': 'Contact modifié'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def traiter_rechercher_contact(pdu: Dict, utilisateur: Client) -> Dict:
    """Traite une demande de recherche de contact."""
    criteres = pdu.get('criteres')
    if not criteres:
        return {'status': 'error', 'message': 'Critères de recherche requis'}
    
    try:
        resultats = utilisateur.rechercher_contact(criteres)
        return {'status': 'success', 'contacts': resultats}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def traiter_lister_contacts(pdu: Dict, utilisateur: Client) -> Dict:
    """Traite une demande de listage des contacts."""
    try:
        contacts = utilisateur.lister_contacts()
        return {'status': 'success', 'contacts': contacts}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# Fonctions de communication réseau (simulées)
def creer_serveur():
    """Crée et démarre le serveur."""
    charger_utilisateurs()
    print("Serveur démarré et en écoute...")


def connecter_serveur():
    """Simule la connexion d'un client au serveur."""
    print("Client connecté au serveur.")


def deconnecter_serveur():
    """Simule la déconnexion d'un client du serveur."""
    print("Client déconnecté du serveur.")


def envoyer_PDU(pdu: Dict):
    """
    Simule l'envoi d'une PDU au serveur.
    
    Args:
        pdu: Dictionnaire contenant les données de la PDU
    """
    print(f"PDU envoyée : {json.dumps(pdu, indent=2)}")


def recevoir_PDU() -> Optional[Dict]:
    """
    Simule la réception d'une PDU du serveur.
    
    Returns:
        Dictionnaire contenant les données de la PDU reçue
    """
    # Dans un vrai serveur, cela attendrait une PDU du réseau
    return None


def main() -> None:
    """Point d'entrée principal du serveur."""
    creer_serveur()
    
    # Exemple d'utilisation avec des PDU
    print("\n=== Exemple de traitement de PDU ===\n")
    
    # Inscription
    pdu_inscription = {
        'action': 'inscription',
        'mail': 'test@example.com',
        'mot_de_passe': 'password123'
    }
    reponse = traiter_PDU(pdu_inscription)
    print(f"Inscription : {reponse}\n")
    
    # Connexion
    pdu_connexion = {
        'action': 'connexion',
        'mail': 'test@example.com',
        'mot_de_passe': 'password123'
    }
    reponse = traiter_PDU(pdu_connexion)
    print(f"Connexion : {reponse}\n")
    
    if reponse['status'] == 'success':
        session_id = reponse['session_id']
        
        # Ajouter un contact
        pdu_ajout = {
            'action': 'ajouter_contact',
            'session_id': session_id,
            'contact': {
                'id_contact': 1,
                'nom': 'Dupont',
                'prenom': 'Jean',
                'email': 'jean.dupont@mail.com',
                'telephone': '0612345678',
                'adresse': '123 rue de Paris'
            }
        }
        reponse = traiter_PDU(pdu_ajout)
        print(f"Ajout contact : {reponse}\n")
        
        # Lister les contacts
        pdu_liste = {
            'action': 'lister_contacts',
            'session_id': session_id
        }
        reponse = traiter_PDU(pdu_liste)
        print(f"Liste contacts : {reponse}\n")









if __name__ == "__main__":
    main()