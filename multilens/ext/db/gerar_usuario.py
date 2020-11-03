from werkzeug.security import generate_password_hash
password = input("Coloque sua senha")
hash_passwd = generate_password_hash(password)
print(hash_passwd)