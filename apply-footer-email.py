#!/usr/bin/env python3
"""apply-footer-email.py — homepage footer shows the TGI email instead of the signup form (17 Oct 2026).
Lenny: "Let's change the contact form to show our email". The footer form posted to FormSubmit, which was never
activated, so signups failed. It is replaced by the same-shaped box: the address on the left, an Email button on
the right (mailto). The old submit handler is guarded so it no-ops when the form is absent. Idempotent; runs after
paginate-feed in Deploy so a feed re-split cannot bring the form back. Dry run without --apply."""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "index.html"
EMAIL = "Lenny@thegrassyissue.com"
NEW = ('<div class="mailing mailing-contact" data-tgi="footer-email">'
       f'<a class="mailing-addr" href="mailto:{EMAIL}">{EMAIL}</a>'
       f'<a class="mailing-btn" href="mailto:{EMAIL}">Email &rarr;</a></div>')
CSS = ('<style data-tgi="footer-email-css">.footer-brand .mailing-contact{align-items:stretch}'
       '.footer-brand .mailing-contact .mailing-addr{flex:1;padding:11px 12px;font-family:var(--sans);font-size:13px;color:var(--ink);text-decoration:none;border-bottom:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
       '.footer-brand .mailing-contact .mailing-btn{display:flex;align-items:center;padding:0 16px;background:var(--ink);color:var(--paper);font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;border-bottom:none;transition:background .2s}'
       '.footer-brand .mailing-contact .mailing-btn:hover{background:var(--grass)}</style>\n')
t = F.read_text(encoding="utf-8"); u = t
u = re.sub(r'<form class="mailing" id="mailingForm">.*?</form>', NEW, u, flags=re.S)
u = u.replace("document.getElementById('mailingForm').addEventListener(",
              "(document.getElementById('mailingForm') || document.createElement('form')).addEventListener(")
if 'data-tgi="footer-email-css"' not in u:
    u = u.replace("</head>", CSS + "</head>", 1)
changed = u != t
if changed and "--apply" in sys.argv: F.write_text(u, encoding="utf-8")
print(f"apply-footer-email: {'updated' if changed else 'unchanged'}{'' if '--apply' in sys.argv or not changed else ' (dry run)'}")
