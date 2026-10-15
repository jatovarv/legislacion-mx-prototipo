#!/usr/bin/env python3
"""Coteja la estructura del Código Civil para el Distrito Federal contra el PDF oficial del Congreso de la CDMX.

Uso: python3 cotejar_estructura_ccdf_pdf.py ccdf_congreso.pdf [salida.json]

Extrae del PDF (PyMuPDF) los encabezados LIBRO / PARTE / TÍTULO / CAPÍTULO (líneas en mayúsculas), su epígrafe (líneas
siguientes) y cada «ARTICULO N» (con Bis/Ter/letras), y escribe un JSON con: `nodes` (encabezados, página y primer
artículo) y `arts` (cada artículo con el Libro/Parte/Título/Capítulo bajo el que aparece). Con esa salida se construyó
la `estructura` de ccdf.json (rango = primer y último artículo bajo cada encabezado). No extrae ni guarda texto normativo.
Fuente cotejada: PDF «CÓDIGO CIVIL PARA EL DF ACTUALIZADO 02-09-26» (SHA-256 985e3bfa…), 381 páginas, 3,074 numerales.
"""
import pymupdf, re, json, sys
doc=pymupdf.open(sys.argv[1])
HDR=re.compile(r'^(I N S T I T U T O|CÓDIGO CIVIL PARA EL DISTRITO FEDERAL\s*$)')
RX_H=re.compile(r'^(LIBRO (?:PRIMERO|SEGUNDO|TERCERO|CUARTO)|T[IÍ]TULO [A-ZÁÉÍÓÚ ]+?(?: BIS)?|CAP[IÍ]TULO [IVXLA-ZÁÉÍÓÚ ]+?|PRIMERA PARTE|PARTE SEGUNDA|SEGUNDA PARTE|TERCERA PARTE|CUARTA PARTE)\s*$')
RX_A=re.compile(r'(?i)^ART[IÍ]CULO\s+(\d+)[°º]?\s*(?:([A-Z](?:\b|\.)|Bis|Ter|Qu[aá]ter|Quintus|Quintos|Sextus|S[eé]ptimus|Octavus|Nonus|Nonies|Decimus|D[eé]cies)\b)?\s*[\.\-–:]')
lines=[]
for pno,page in enumerate(doc, start=1):
    for ln in page.get_text().split('\n'):
        s=ln.strip()
        if s and not HDR.match(s): lines.append((pno,s))
# fin de los artículos: primera línea "TRANSITORIOS" / "T R A N S I T O R I O S" tras el último artículo numérico alto
ctx={'libro':None,'parte':None,'titulo':None,'capitulo':None}
nodes=[]  # (kind, nombre, epigrafe, page, primer_art)
arts=[]   # (num, sufijo, page, libro, parte, titulo, capitulo, derogado)
i=0; stop=None
while i<len(lines):
    p,s=lines[i]
    if s in ('Disposiciones preliminares',) and ctx['libro'] is None:
        nodes.append(('preliminar','Disposiciones preliminares','',p,None)); ctx['titulo']=('Disposiciones preliminares',''); i+=1; continue
    m=RX_H.match(s)
    if m and s.upper()==s:
        kind='libro' if s.startswith('LIBRO') else 'parte' if 'PARTE' in s else 'titulo' if s.startswith(('TITULO','TÍTULO')) else 'capitulo'
        # epígrafe: líneas siguientes hasta ARTICULO / otro encabezado / nota de editor
        ep=[]; j=i+1
        while j<len(lines) and j<i+5:
            t=lines[j][1]
            if RX_A.match(t) or (RX_H.match(t) and t.upper()==t) or t.startswith('N. DE E.') or t.startswith('ARTICULO') or t.startswith('ARTÍCULO'): break
            ep.append(t); j+=1
        epig=' '.join(ep).strip()
        if kind=='libro': ctx.update(libro=(s,epig),parte=None,titulo=None,capitulo=None)
        elif kind=='parte': ctx.update(parte=(s,epig),titulo=None,capitulo=None)
        elif kind=='titulo': ctx.update(titulo=(s,epig),capitulo=None)
        else:
            prev=ctx['capitulo']
            if prev and prev[0].upper()==s.upper() and prev[1].upper()==epig.upper(): i=j; continue
            ctx['capitulo']=(s,epig)
        nodes.append((kind,s,epig,p,None)); i=j; continue
    a=RX_A.match(s)
    if a and ctx['libro'] is not None or (a and ctx['titulo']):
        num=int(a.group(1)); suf=a.group(2) or ''
        if num>3200: break
        derog='DEROGAD' in s.upper() or 'SE DEROGA' in s.upper()
        upper=s.startswith(('ARTICULO','ARTÍCULO'))
        last=arts[-1][0] if arts else 0
        if not ((upper and num>=last-1) or (last<=num<=last+5)):
            i+=1; continue
        arts.append((num,suf,p,ctx['libro'],ctx['parte'],ctx['titulo'],ctx['capitulo'],derog,s[:60]))
        for n in reversed(nodes):
            if n[4] is None: nodes[nodes.index(n)]=n[:4]+(f"{num}{(' '+suf) if suf else ''}",)
            else: break
    if re.match(r'^T\s*R\s*A\s*N\s*S\s*I\s*T\s*O\s*R\s*I\s*O\s*S?\s*$',s) and arts and arts[-1][0]>3000:
        stop=(p,s); break
    i+=1
json.dump({'nodes':nodes,'arts':arts,'stop':stop}, open(sys.argv[2] if len(sys.argv) > 2 else 'ccdf_parse.json','w'), ensure_ascii=False, indent=1)
print(len(nodes), len(arts), 'stop', stop, 'último art', arts[-1][:3])
