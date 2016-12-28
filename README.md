# crypt-kms

## Usage

Encrypt given `foo.txt`.

```sh
% cat foo.txt
foo
% ./app.py --armor --encrypt foo.txt
```

This will generate `foo.txt.enc` and `foo.txt.key` which we need to store on persistent storage.

```sh
% cat foo.txt.enc
zW5doCPsQUJG4JGCXSSLUoy4bv0EKObG8IPGeBz8WtI=
% cat foo.txt.key
AQEDAHjMkg5lQdMX21Yuk9WbUzVwL4GORsOd56NTHRB5ZZEh8gAAAH4wfAYJKoZIhvcNAQcGoG8wbQIBADBoBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDEVYRmxSQGa2+hSjwAIBEIA7sMTVH+wfVUfn8/18ONivANM9IfU5ZsBRC033MHvDmf0qiwTokAO13FytCyzEljxlhSKT3VDUcD53ECY=
```

Remove the original file, and then restore the file from CMK and encrypted data.

```sh
% rm -f foo.txt
% ./app.py --armor --decrypt foo.txt
% cat foo.txt
foo
```
