"""
Module pour les fonctions et menus liés aux clients.
"""

from Class import Client  # type: ignore


def menu_actions(client: Client):
    """
    Affiche le menu d'actions et gère les interactions avec le client connecté.
    
    Args:
        client: Instance du Client connecté
    """
    print("--------------------------------")
    print("Menu Client - Choisir une action :")
    print("1. visualiser l'annuaire")
    print("2. ajouter un contact")
    print("3. supprimer un contact")
    print("4. modifier un contact")
    print("5. rechercher un contact")
    print("6. accorder une permission")
    print("7. retirer une permission")
    print("8. exporter l'annuaire")
    print("9. Se déconnecter")
    choix = input("Choisir une action : ")
    if choix == "1":
        visualiser_annuaire(client)
    elif choix == "2":
        ajouter_contact(client)
    elif choix == "3":
        supprimer_contact(client)
    elif choix == "4":
        modifier_contact(client)
    elif choix == "5":
        rechercher_contact(client)
    elif choix == "6":
        accorder_permission(client)
    elif choix == "7":
        retirer_permission(client)
    elif choix == "8":
        exporter_annuaire(client)
    elif choix == "9":
        deconnecter_serveur()
        exit()
    else:
        print("Choix invalide")
        menu_actions(client)


def visualiser_annuaire(client: Client):
    """Visualise l'annuaire du client."""
    contacts = client.lister_contacts()
    if not contacts:
        print("Aucun contact dans l'annuaire.")
    else:
        print(f"\nAnnuaire de {client.mail} ({len(contacts)} contact(s)):")
        for contact in contacts:
            print(f"  - ID: {contact.get('id_contact')}, {contact.get('prenom')} {contact.get('nom')}, Email: {contact.get('email')}, Adresse: {contact.get('adresse')}, Téléphone: {contact.get('telephone')}")
    print()
    menu_actions(client)


def ajouter_contact(client: Client):
    """Ajoute un contact à l'annuaire."""
    print("Ajout d'un contact :")
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    email = input("Email : ")
    telephone = input("Téléphone : ")
    adresse = input("Adresse : ")
    
    contact = {
        'nom': nom,
        'prenom': prenom,
        'email': email,
        'telephone': telephone,
        'adresse': adresse
    }
    try:
        client.ajouter_contact(contact)
        print("Contact ajouté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du contact : {e}")
    print()
    menu_actions(client)


def supprimer_contact(client: Client):
    """Supprime un contact de l'annuaire."""
    id_contact = int(input("ID du contact à supprimer : "))
    try:
        client.supprimer_contact(id_contact)
        print("Contact supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")
    print()
    menu_actions(client)


def modifier_contact(client: Client):
    """Modifie un contact de l'annuaire."""
    id_contact = int(input("ID du contact à modifier : "))
    print("Entrez les nouveaux champs (laisser vide pour ne pas modifier) :")
    champs = {}
    nom = input("Nom : ")
    if nom:
        champs['nom'] = nom
    prenom = input("Prénom : ")
    if prenom:
        champs['prenom'] = prenom
    email = input("Email : ")
    if email:
        champs['email'] = email
    telephone = input("Téléphone : ")
    if telephone:
        champs['telephone'] = telephone
    adresse = input("Adresse : ")
    if adresse:
        champs['adresse'] = adresse
    
    try:
        client.modifier_contact(id_contact, champs)
        print("Contact modifié avec succès.")
    except Exception as e:
        print(f"Erreur lors de la modification : {e}")
    print()
    menu_actions(client)


def rechercher_contact(client: Client):
    """Recherche des contacts dans l'annuaire."""
    print("Critères de recherche (laisser vide pour ignorer) :")
    criteres = {}
    nom = input("Nom : ")
    if nom:
        criteres['nom'] = nom
    prenom = input("Prénom : ")
    if prenom:
        criteres['prenom'] = prenom
    email = input("Email : ")
    if email:
        criteres['email'] = email
    
    try:
        resultats = client.rechercher_contact(criteres)
        if not resultats:
            print("Aucun contact trouvé.")
        else:
            print(f"\n{len(resultats)} contact(s) trouvé(s) :")
            for contact in resultats:
                print(f"  - ID: {contact.get('id_contact')}, {contact.get('prenom')} {contact.get('nom')}, Email: {contact.get('email')}")
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
    print()
    menu_actions(client)


def accorder_permission(client: Client):
    """Accorde une permission à un autre utilisateur."""
    email_utilisateur = input("Email de l'utilisateur à qui accorder la permission : ")
    try:
        client.accorder_permission(email_utilisateur)
        print(f"Permission accordée à {email_utilisateur}.")
    except Exception as e:
        print(f"Erreur : {e}")
    print()
    menu_actions(client)


def retirer_permission(client: Client):
    """Retire une permission à un autre utilisateur."""
    email_utilisateur = input("Email de l'utilisateur à qui retirer la permission : ")
    try:
        client.retirer_permission(email_utilisateur)
        print(f"Permission retirée à {email_utilisateur}.")
    except Exception as e:
        print(f"Erreur : {e}")
    print()
    menu_actions(client)


def exporter_annuaire(client: Client):
    """Exporte l'annuaire au format CSV."""
    try:
        chemin = client.exporter_csv()
        print(f"Annuaire exporté vers : {chemin}")
    except Exception as e:
        print(f"Erreur lors de l'export : {e}")
    print()
    menu_actions(client)


def deconnecter_serveur():
    """Déconnecte le client."""
    print("Déconnexion réussie.")
    exit()
