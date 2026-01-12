import sys
import os
import socket
import threading
import json
import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

# Ajouter le dossier parent (annuaire) au chemin Python pour les imports de classes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Class import Client, Administrateur  # type: ignore


# Répertoires et constantes
ANNUAIRE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTILISATEURS_PATH = os.path.join(ANNUAIRE_DIR, "data", "utilisateurs.json")
HOST = os.environ.get("ANNUAIRE_HOST", "127.0.0.1")
PORT = int(os.environ.get("ANNUAIRE_PORT", "5000"))


# Etat serveur (en mémoire)
utilisateurs: Dict[str, Client] = {}  # email -> Client/Administrateur
sessions: Dict[str, Client] = {}      # token(session_id) -> Client


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def charger_utilisateurs() -> None:
    """Charge les utilisateurs depuis le fichier JSON local."""
    utilisateurs.clear()
    if not os.path.exists(UTILISATEURS_PATH):
        print(f"Aucun fichier utilisateurs trouvé: {UTILISATEURS_PATH}")
        return
    try:
        with open(UTILISATEURS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for user_data in data:
            cls = Administrateur if user_data.get("est_admin") else Client
            u = cls(user_data["mail"], user_data["hash_mot_de_passe"])  # type: ignore
            u.identifiant = user_data.get("identifiant", u.identifiant)
            u.chemin_annuaire = user_data.get("chemin_annuaire", u.chemin_annuaire)
            utilisateurs[u.mail] = u
        print(f"{len(utilisateurs)} utilisateur(s) chargé(s) depuis {UTILISATEURS_PATH}.")
    except Exception as e:
        print(f"Erreur lors du chargement des utilisateurs: {e}")


def _build_response(
    req: Dict,
    *,
    action: str,
    statut: str,
    contenu: Dict,
    utilisateur: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict:
    return {
        "version": req.get("version", "1.0"),
        "message_ID": str(uuid.uuid4()),
        "type": "REPONSE",
        "action": action,
        "horodatage": _now_iso(),
        "correlation_ID": req.get("message_ID"),
        "statut": statut,
        "authentification": {
            "utilisateur": utilisateur,
            "token": token,
        },
        "contenu": contenu,
    }


def _handle_auth_connexion(req: Dict) -> Dict:
    """Gère l'action AUTH_CONNEXION selon le PDU fourni."""
    contenu = req.get("contenu") or {}
    email = contenu.get("email")
    mot_de_passe_hash = contenu.get("mot_de_passe")

    if not email or not mot_de_passe_hash:
        return _build_response(
            req,
            action="AUTH_CONNEXION",
            statut="ERREUR",
            contenu={"erreur": "email et mot_de_passe requis"},
        )

    user = utilisateurs.get(email)
    if not user:
        return _build_response(
            req,
            action="AUTH_CONNEXION",
            statut="ERREUR",
            contenu={"erreur": "identifiants invalides"},
        )

    if not user.verifier_mot_de_passe(mot_de_passe_hash):
        return _build_response(
            req,
            action="AUTH_CONNEXION",
            statut="ERREUR",
            contenu={"erreur": "identifiants invalides"},
        )

    token = str(uuid.uuid4())
    sessions[token] = user

    return _build_response(
        req,
        action="AUTH_CONNEXION",
        statut="SUCCES",
        contenu={
            "est_admin": isinstance(user, Administrateur),
            "identifiant": user.identifiant,
        },
        utilisateur=user.mail,
        token=token,
    )


def traiter_pdu(req: Dict) -> Dict:
    """Routeur d'actions pour les PDUs reçues."""
    if not isinstance(req, dict):
        return _build_response(
            {"version": "1.0", "message_ID": None},
            action="INCONNU",
            statut="ERREUR",
            contenu={"erreur": "PDU non valide"},
        )

    action = req.get("action")
    type_ = req.get("type")
    if type_ != "REQUETE":
        return _build_response(
            req,
            action=action or "INCONNU",
            statut="ERREUR",
            contenu={"erreur": "type PDU attendu: REQUETE"},
        )

    if action == "AUTH_CONNEXION":
        return _handle_auth_connexion(req)

    return _build_response(
        req,
        action=action or "INCONNU",
        statut="ERREUR",
        contenu={"erreur": "action non supportee"},
    )


def _recv_lines(sock: socket.socket) -> str:
    sock.settimeout(0.5)
    chunks: list[bytes] = []
    while True:
        try:
            data = sock.recv(4096)
        except socket.timeout:
            break
        if not data:
            break
        chunks.append(data)
        if b"\n" in data:
            break
    return b"".join(chunks).decode("utf-8", errors="ignore")


def _client_thread(conn: socket.socket, addr: Tuple[str, int]) -> None:
    peer = f"{addr[0]}:{addr[1]}"
    try:
        buffer = ""
        while True:
            snippet = _recv_lines(conn)
            if not snippet:
                break
            buffer += snippet
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    req = json.loads(line)
                except json.JSONDecodeError:
                    resp = _build_response(
                        {"version": "1.0", "message_ID": None},
                        action="INCONNU",
                        statut="ERREUR",
                        contenu={"erreur": "JSON invalide"},
                    )
                else:
                    resp = traiter_pdu(req)

                payload = (json.dumps(resp, ensure_ascii=False) + "\n").encode("utf-8")
                conn.sendall(payload)
    except Exception as e:
        # Log minimal et ferme la connexion
        try:
            err_payload = json.dumps({
                "type": "REPONSE",
                "action": "INCONNU",
                "statut": "ERREUR",
                "horodatage": _now_iso(),
                "contenu": {"erreur": f"Exception serveur: {e}"}
            }) + "\n"
            conn.sendall(err_payload.encode("utf-8"))
        except Exception:
            pass
    finally:
        conn.close()


def creer_serveur(host: str = HOST, port: int = PORT) -> None:
    charger_utilisateurs()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Serveur en écoute sur {host}:{port} (PDU JSON par ligne)")
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=_client_thread, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nArrêt du serveur demandé (Ctrl+C).")


def main() -> None:
    creer_serveur()


if __name__ == "__main__":
    main()
