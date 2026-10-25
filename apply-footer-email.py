#!/usr/bin/env python3
"""apply-footer-email.py — homepage footer shows the TGI email instead of the signup form (17 Oct 2026).
25 Oct 2026, Lenny: "we need to bring back the newsletter sign up, can it then auto sign someone up for our substack?" -> the footer
box is now a signup that posts straight to Substack (thegrassyissue.substack.com, free subscription; Substack sends its own
confirmation email), with the TGI email kept as a line underneath.
Lenny: "Let's change the contact form to show our email". The footer form posted to FormSubmit, which was never
activated, so signups failed. It is replaced by the same-shaped box: the address on the left, an Email button on
the right (mailto). The old submit handler is guarded so it no-ops when the form is absent. Idempotent; runs after
paginate-feed in Deploy so a feed re-split cannot bring the form back. Dry run without --apply."""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "index.html"
EMAIL = "Lenny@thegrassyissue.com"
SUB = "https://thegrassyissue.substack.com/api/v1/free?nojs=true"
NEW = ('<div data-tgi="footer-email"><form class="mailing" data-tgi="footer-substack" action="' + SUB + '" method="post" target="_blank" rel="noopener">'
       '<input type="email" name="email" placeholder="Your email" required aria-label="Email address" />'
       '<button type="submit">Subscribe &rarr;</button></form>'
       f'<div class="mailing-note">New posts by email, via our Substack. Or write to <a href="mailto:{EMAIL}">{EMAIL}</a></div></div>')
CSS = ('<style data-tgi="footer-email-css">.footer-brand .mailing-contact{align-items:stretch}'
       '.footer-brand .mailing-contact .mailing-addr{flex:1;padding:11px 12px;font-family:var(--sans);font-size:13px;color:var(--ink);text-decoration:none;border-bottom:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
       '.footer-brand .mailing-contact .mailing-btn{display:flex;align-items:center;padding:0 16px;background:var(--ink);color:var(--paper);font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;border-bottom:none;transition:background .2s}'
       '.footer-brand .mailing-contact .mailing-btn:hover{background:var(--grass)}'
       '.footer-brand .mailing-note{font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.6;margin-top:10px;line-height:1.6;max-width:380px}.footer-brand .mailing-note a{border-bottom:1px solid currentColor;text-transform:none;letter-spacing:0;font-family:var(--sans);font-size:11px}</style>\n')
t = F.read_text(encoding="utf-8"); u = t
u = re.sub(r'<form class="mailing" id="mailingForm">.*?</form>', NEW, u, flags=re.S)
u = re.sub(r'<div class="mailing mailing-contact" data-tgi="footer-email">.*?</div>', NEW, u, count=1, flags=re.S)
u = re.sub(r'<div data-tgi="footer-email">.*?</div></div>', NEW, u, count=1, flags=re.S)
u = u.replace("document.getElementById('mailingForm').addEventListener(",
              "(document.getElementById('mailingForm') || document.createElement('form')).addEventListener(")
u = re.sub(r'<style data-tgi="footer-email-css">.*?</style>\n?', '', u, flags=re.S)
u = u.replace("</head>", CSS + "</head>", 1)
changed = u != t
if changed and "--apply" in sys.argv: F.write_text(u, encoding="utf-8")
print(f"apply-footer-email: {'updated' if changed else 'unchanged'}{'' if '--apply' in sys.argv or not changed else ' (dry run)'}")
