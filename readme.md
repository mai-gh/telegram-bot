



### Generate `hook_token`
```
LC_ALL=C tr -dc 'A-Za-z0-9_-'</dev/urandom | head -c 64 ; echo
```

### Generate certificate and key files
```
openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out public.pem -subj "/"
```
