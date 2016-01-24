# PEMetrator
OpenVPN PKI management web application.

## What is this project about ?
Have you ever tried to setup a [PKI](https://en.wikipedia.org/wiki/Public_key_infrastructure) to use with [OpenVPN](https://openvpn.net/) ?

As the documentation suggests you might have used easy-rsa to manage your keys and certificates. But this solution is quite unsatisfying in the way that it requires you to SSH on the server to perform actions, and there is no easy way for the users of your VPN to request or revoke a certificate for instance.

This is what this project is about: *make the use of OpenVPN PKI easy for everyone.*

## What does this project allow you to do ?
### Disclaimer
This project is quite young, and I plan on coding on it a lot. So this documentation is very likely to change in the next days :)

### Create CAs
CAs (Certification Authorities) are the components that will establish the *trust* between your OpenVPN server and your clients. It is the CA that signs the certificates for both of them, and provides the Certificate Revocation List which is used to check if a certificate has been compomized or not.

PEMetrator allows you to to create certifications authorities, that your users will be able to use in
order to request certificates.

A CA possesses three important attributes :
 * A certificate, that the client and servers must know in order to identify each other
 * A private key, used to sign certificate requests
 * A certificate revocation list used to let people know if a certificate has been revoked.

All these components (except the private key obviously!) are freely accessible to the clients so that they can configure their VPN accesses.

### Create certificate requests
This enables the users to request certificates.

An administrator then has to sign them to make them
valid.

### Revoke certificates
A certificate can be revoked at any time by an administrator. The CRL is available to anyone.

### Create client and server certificate
Both of them are supported :)

### Email notifications
When you create a certificate request, and when it
is signed, the system sends the requester email notifications that allow him to keep tracks of his certificate requests.

## Technologies used
This webapplication is built using the following technologies :
 * Python.
 * Django.
 * Celery for all the asynchronous tasks such as certificate signing.
 * Bootstrap for the swag.

## Deploy it for a test
To test the application please download this repo, create the appropriate database, in mysql, or edit settings.py to enable the sqlite backend. (**warning**: the SQLite backend caused me headaches during developpement because it has an annoying tendency of deadlocking shit. Use MySQL or PostgreSQL !)

Run the following commands :
```bash
$ sudo service redis star # Mandatory for Celery
$ pip install -r requirements.txt # Install deps
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
# And in a second shell
$ python manage.py python manage.py celeryd -v 2 -B -s celery -E -l INFO
```

## Feedbacks
I accept feedbacks, you can let me know what you think through issues, pull requests and [twitter](https://twitter.com/thomas_maurice).
