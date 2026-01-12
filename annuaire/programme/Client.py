import socket, json, hashlib, uuid, datetime

HOST, PORT = "127.0.0.1", 5000

def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# Replace with your password; the example user has password "password123"
email = "test@example.com"
password = "password123"
hashed = hashlib.sha256(password.encode()).hexdigest()

pdu = {
  "version": "1.0",
  "message_ID": str(uuid.uuid4()),
  "type": "REQUETE",
  "action": "AUTH_CONNEXION",
  "horodatage": now(),
  "authentification": {
    "utilisateur": email,
    "token": None
  },
  "contenu": {
    "email": email,
    "mot_de_passe": hashed
  }
}

with socket.create_connection((HOST, PORT)) as s:
    s.sendall((json.dumps(pdu) + "\n").encode("utf-8"))
    data = s.recv(4096).decode("utf-8")
    print("Reçu:", data)