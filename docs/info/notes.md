# Notes

Here you can find some useful things we should remember.

## Generating keys

```bash
openssl genpkey -algorithm RSA -out private_key.pem -aes256 -pass pass:vulsy -pkeyopt rsa_keygen_bits:4096
openssl rsa -pubout -in private_key.pem -out public_key.pem -passin pass:vulsy
```
