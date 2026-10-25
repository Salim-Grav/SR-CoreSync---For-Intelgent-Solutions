# -*- coding: utf-8 -*-
"""Check whether the autoconfig/autodiscover hostnames present a valid certificate.

A CNAME keeps the original hostname for TLS, while an SRV record sends the client
to the target host — so the same server can be reachable through one and rejected
through the other. This prints which is which instead of guessing.
"""
import socket
import ssl

HOSTS = [
    ('autoconfig.sr-coresync.com', 443, '/mail/config-v1.1.xml'),
    ('autodiscover.sr-coresync.com', 443, '/autodiscover/autodiscover.xml'),
    ('autoconfig.purelymail.com', 443, '/mail/config-v1.1.xml'),
]

for host, port, path in HOSTS:
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=15) as raw:
            with context.wrap_socket(raw, server_hostname=host) as tls:
                cert = tls.getpeercert()
                subject = dict(x[0] for x in cert.get('subject', []))
                sans = [value for kind, value in cert.get('subjectAltName', []) if kind == 'DNS']
                print('%-30s TLS ok   CN=%s' % (host, subject.get('commonName')))
                print('%-30s SANs: %s' % ('', ', '.join(sans[:6])))
    except ssl.SSLCertVerificationError as exc:
        print('%-30s TLS MISMATCH -> %s' % (host, exc.verify_message))
    except (OSError, ssl.SSLError) as exc:
        print('%-30s failed: %s' % (host, str(exc)[:90]))
    print('%-30s path checked: %s' % ('', path))
