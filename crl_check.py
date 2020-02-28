# check certificate revocation list urls and download certificate serials
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
crl = x509.load_pem_x509_crl(pem_crl_data, default_backend())

for url in crllist:
    crl = requests.get(url)
    crl_obj = crypto.load_crl(crypto.FILETYPE_ASN1, crl.content)
    for revoked in crl_obj.get_revoked():
        print(revoked.get_serial())
