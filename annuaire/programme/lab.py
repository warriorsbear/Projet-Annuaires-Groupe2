import hashlib
mdp = hashlib.sha256("123456".encode()).hexdigest()
print(mdp)