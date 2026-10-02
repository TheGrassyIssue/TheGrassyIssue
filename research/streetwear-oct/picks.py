import json,glob,re,urllib.request,html
SEL={
 'students':('studentsgolf.com',['obispo-nylon-jacket','riverview-knit-ls-polo-sweater','stockton-work-pants','ridgewood-s-s-polo-shirt','presidio-camo-nylon-pants','cardiff-sherpa-jacket']),
 'malbon':('malbon.com',['dornoch-gore-tex-terrain-anorak-moss-khaki','m-script-sweater-forest','malbon-samba-linen-green','links-windshirt-forest','arsham-fairway-monogram-polo-arsham-green','bermuda-palms-tee-green-tint']),
 'eastside':('eastsidegolf.com',['el2021157-410-midnight-navy-cranberry-corduroy-shi','el2040861-961-multi-color-scenic-pique-polo','el2070752-317-prime-green-fairway-knit-crew','eo2030410-410-midnight-navy-signature-hoodie-camo-','ep2060301-517-wild-grape-links-sweater','el2041358-317-prime-green-midnight-navy-polo-sweat']),
 'publicdrip':('publicdrip.com',['triborough-waffle-knit-polo-coffee','the-herringbone-half-zip-coffee','anywhere-pleated-pants-pinstripe','public-athlete-long-sleeve-mock-cream','p-script-denim-snapback-indigo','public-athlete-polo-storm']),
 'midiron':('midiron.shop',['research-polo-bush-camo','detour-stripe-polo','tour-spec-polo-tree-camo','m-star-golf-cap-trad-camo','results-cap-black','camo-headcover']),
 'ald':('aimeleondore.com',['ald-the-north-face-fair-isle-knit-polo','crest-rugby','fleece-lined-sport-windbreaker','quarter-zip-pavilion-cashmere-pullover','crest-logo-hat-4','chalk-stripe-logo-hat']),
 'hls':('hiddenlinkssociety.com',['the-society-overshirt-charcoal-1','the-play-faster-tee-ivory','play-faster-hat-walnut','early-access-bud-chenille-bucket-hat-white','the-society-tee-light-grey','single-prong-pitch-mark-tool-aged-brass']),
}
out={}
for k,(d,hs) in SEL.items():
  ps={}
  for f in sorted(glob.glob(d+'-*.json')):
    try:
      for p in json.load(open(f))['products']: ps[p['handle']]=p
    except: pass
  rows=[]
  for h in hs:
    h=next(x for x in ps if x.startswith(h)); p=ps[h]; av=any(v['available'] for v in p['variants'])
    rows.append(dict(handle=h,t=p['title'],price=p['variants'][0]['price'],avail=av,url=f"https://{d}/products/{h}",imgs=[i['src'] for i in p['images']][:8],body=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',p['body_html'] or '')))[:600],ptype=p['product_type']))
  out[k]=rows
json.dump(out,open('picks.json','w'),indent=1)
for k,r in out.items():
  print('\n##',k)
  for x in r: print(' ',x['avail'],x['price'],len(x['imgs']),x['t'],'::',x['body'][:230])
