import os
import pickle

# Mot de passe codé en dur (vulnérabilité critique)
password = "admin1234"
db_password = "secret123"

# Injection SQL (vulnérabilité critique)
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return query

# Utilisation dangereuse de eval
def calculate(expression):
    return eval(expression)

# Désérialisation non sécurisée
def load_data(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

# Variable non utilisée
def bad_function():
    unused_variable = 42
    x=1
    y=2
    return x+y

# Commande système dangereuse
def run_command(cmd):
    os.system(cmd)
