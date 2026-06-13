from app.core.security import encrypt_phone, decrypt_phone

encripted_phone = encrypt_phone("9988776655")
print(encripted_phone)
print(decrypt_phone(encripted_phone))