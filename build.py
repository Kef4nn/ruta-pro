"""Genera web.html (artifact) y puerta.html (para PDF) desde semanas.tsv."""
import base64, csv, datetime as dt, html, json, pathlib

D = pathlib.Path(__file__).parent
rows = [r for r in csv.reader(open(D / "semanas.tsv"), delimiter="\t") if r and not r[0].startswith("#")]
FASES = [(1, 6, "Base técnica", "Python, GitHub y AI-900"), (7, 11, "Proyecto insignia", "Agente de reclamaciones de seguros"),
         (12, 16, "Stack Microsoft", "Copilot Studio + certificación asociada"), (17, 24, "Consultor y arquitecto", "ROI, oferta Dorevio, proyecto 2, empleo remoto")]
MES = "ene feb mar abr may jun jul ago sep oct nov dic".split()
def rango(ini, sig=None):
    a = dt.date.fromisoformat(ini); b = dt.date.fromisoformat(sig) - dt.timedelta(days=1) if sig else a + dt.timedelta(days=6)
    return f"{a.day} {MES[a.month-1]} – {b.day} {MES[b.month-1]}"
weeks = [dict(ini=r[0], n=int(r[1]), tema=r[2], dom=r[3], rec=r[4], rango=rango(r[0], rows[i+1][0] if i+1 < len(rows) else None)) for i, r in enumerate(rows)]
assert len(weeks) == 24 and [w["n"] for w in weeks] == list(range(1, 25))
logo = "data:image/webp;base64," + base64.b64encode(open("/home/kelrro/Proyectos/dorevio-automation/logo.webp", "rb").read()).decode()
e = html.escape
RUTINA = [("Lun", "5–8 AM", "Teoría + 30 min inglés + ejercicio"), ("Mar", "5–8 AM", "Práctica + 30 min inglés + ejercicio"), ("Mié", "5–8 AM", "Teoría 2 + 30 min inglés + cardio"), ("Jue", "5–8 AM", "Práctica 2 + 30 min inglés + ejercicio"),
          ("Vie", "5–8 AM", "1 h inglés + post LinkedIn + ejercicio"), ("Sáb", "7–8 AM", "Cardio largo · resto familia"), ("Dom", "7–11 AM", "Proyecto → GitHub")]
PRUEBAS = ["2 certificaciones oficiales de Microsoft (AI-900 + asociada)", "Certificado de inglés EF SET con nivel CEFR en LinkedIn", "~24 posts en LinkedIn, uno cada viernes",
           "GitHub activo cada domingo, con README en español e inglés", "2 casos de estudio con números reales",
           "Test físico en semanas 1, 8, 16 y 24: más flexiones y sentadillas cada vez", "Perfil: Automatización RPA + Agentes de IA para seguros y finanzas"]
fase_de = lambda n: next(i for i, f in enumerate(FASES) if f[0] <= n <= f[1])

# ---------- web ----------
fases_html = "".join(f'<li class="fase" data-a="{a}" data-b="{b}"><span class="fn">Semanas {a}–{b}</span><strong>{e(t)}</strong><span>{e(s)}</span><div class="bar"><i></i></div></li>' for a, b, t, s in FASES)
rut_html = "".join(f'<li class="dia{" off" if h=="Libre" else ""}" data-d="{i+1}"><b>{d}</b><span>{h}</span><em>{e(t)}</em></li>' for i, (d, h, t) in enumerate(RUTINA))
sem_html = []
for w in weeks:
    f = fase_de(w["n"])
    if w["n"] == FASES[f][0]:
        sem_html.append(f'<li class="sep">{e(FASES[f][2])}</li>')
    rec = "" if w["rec"] == "-" else f'<span class="rec">Recurso: {e(w["rec"])}</span>'
    sem_html.append(f'<li class="sem" id="s{w["n"]}" data-ini="{w["ini"]}"><span class="num">{w["n"]:02d}</span>'
                    f'<div class="cuerpo"><span class="fecha">{w["rango"]}</span><p class="tema">{e(w["tema"])}</p>'
                    f'<p class="dom"><b>Domingo:</b> {e(w["dom"])}</p>{rec}</div></li>')
web = f"""<title>Ruta Pro 24 Semanas</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<style>
/* Layout: una columna estrecha tipo consola de Dorevio; "esta semana" arriba, la ruta completa abajo como línea de circuito. Tema único oscuro de marca. */
:root {{
  --bg:#0c111b; --surface:#131a27; --line:#223047; --fg:#e7edf6; --muted:#8c99ad; --green:#14f08a; --green-dim:#0f8f55;
  --display:"Outfit",system-ui,sans-serif; --body:"Plus Jakarta Sans",system-ui,sans-serif;
  color-scheme:dark;
}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font:400 15px/1.55 var(--body)}}
.wrap{{max-width:760px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:36px}}
header{{display:flex;gap:14px;align-items:center}}
header img{{width:52px;height:52px;border-radius:12px}}
h1{{font:800 clamp(26px,6vw,36px)/1.05 var(--display);margin:0;letter-spacing:-.01em;text-wrap:balance}}
h1 span{{color:var(--green)}}
.sub{{color:var(--muted);margin:4px 0 0;font-size:14px}}
h2{{font:700 13px/1 var(--display);text-transform:uppercase;letter-spacing:.14em;color:var(--green);margin:0 0 14px}}
.hoy{{background:var(--surface);border:1px solid var(--green-dim);border-radius:16px;padding:22px;box-shadow:0 0 0 1px rgba(20,240,138,.08),0 0 40px -12px rgba(20,240,138,.35)}}
.hoy .k{{font:600 12px/1 var(--display);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
.hoy .t{{font:700 22px/1.25 var(--display);margin:8px 0 10px;text-wrap:balance}}
.hoy p{{margin:6px 0 0;color:var(--fg)}}
.hoy .meta{{color:var(--muted);font-size:13px;margin-top:12px}}
.prog{{height:6px;background:var(--line);border-radius:3px;margin-top:16px;overflow:hidden}}
.prog i{{display:block;height:100%;background:var(--green);width:0}}
.rutina{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(7,1fr);gap:6px}}
.dia{{border:1px solid var(--line);border-radius:10px;padding:10px 6px;text-align:center;display:grid;gap:3px;min-width:0}}
.dia b{{font:700 14px var(--display)}} .dia span{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}} .dia em{{font-style:normal;font-size:12px;line-height:1.3}}
.dia.off{{opacity:.55}} .dia.now{{border-color:var(--green);background:rgba(20,240,138,.07)}}
@media (max-width:560px){{.rutina{{grid-template-columns:repeat(4,1fr)}}}}
.fases{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}
@media (max-width:560px){{.fases{{grid-template-columns:1fr}}}}
.fase{{border:1px solid var(--line);border-radius:12px;padding:14px;display:grid;gap:2px;min-width:0}}
.fase .fn{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}} .fase strong{{font:700 17px var(--display)}} .fase>span:not(.fn){{font-size:13px;color:var(--muted)}}
.bar{{height:4px;background:var(--line);border-radius:2px;margin-top:8px;overflow:hidden}} .bar i{{display:block;height:100%;width:0;background:var(--green)}}
.ruta{{list-style:none;margin:0;padding:0;position:relative}}
.ruta::before{{content:"";position:absolute;left:19px;top:8px;bottom:8px;width:2px;background:var(--line)}}
.sep{{font:700 12px var(--display);text-transform:uppercase;letter-spacing:.14em;color:var(--green);padding:18px 0 8px 52px}}
.sem{{display:grid;grid-template-columns:40px 1fr;gap:12px;padding:10px 0;position:relative}}
.num{{width:40px;height:40px;border-radius:50%;background:var(--bg);border:2px solid var(--line);display:grid;place-items:center;font:700 14px var(--display);font-variant-numeric:tabular-nums;z-index:1}}
.cuerpo{{min-width:0}}
.fecha{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}}
.tema{{margin:2px 0 4px;font-weight:600}} .dom{{margin:0;font-size:14px;color:var(--muted)}} .dom b{{color:var(--fg);font-weight:600}}
.rec{{display:inline-block;margin-top:6px;font-size:12px;color:var(--green);opacity:.85}}
.sem.done .num{{background:var(--green-dim);border-color:var(--green-dim);color:var(--bg)}} .sem.done .tema,.sem.done .dom{{opacity:.6}}
.sem.now .num{{border-color:var(--green);color:var(--green);box-shadow:0 0 14px rgba(20,240,138,.5)}}
.sem.now .cuerpo{{background:var(--surface);border:1px solid var(--green-dim);border-radius:12px;padding:12px 14px;margin:-4px 0}}
.pruebas{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.pruebas li{{padding-left:22px;position:relative}} .pruebas li::before{{content:"";position:absolute;left:0;top:.55em;width:10px;height:10px;border-radius:3px;border:2px solid var(--green)}}
footer{{color:var(--muted);font-size:13px}}
a{{color:var(--green)}} a:focus-visible{{outline:2px solid var(--green);outline-offset:2px}}
@media (prefers-reduced-motion:no-preference){{.prog i,.bar i{{transition:width .8s ease}}}}
</style>
<div class="wrap">
<header><img src="{logo}" alt="Logo de Dorevio"><div><h1>Ruta Pro <span>24 semanas</span></h1><p class="sub">24 nov 2026 → 9 may 2027 · Automatización RPA + Agentes de IA</p></div></header>
<section class="hoy" id="hoy" aria-live="polite"><span class="k" id="hoy-k">Hoy</span><div class="t" id="hoy-t">Cargando…</div><p id="hoy-p"></p><p class="meta" id="hoy-m"></p><div class="prog"><i id="prog"></i></div></section>
<section><h2>Tu semana</h2><ul class="rutina">{rut_html}</ul></section>
<section><h2>Fases</h2><ul class="fases">{fases_html}</ul></section>
<section><h2>Las 24 semanas</h2><ol class="ruta">{''.join(sem_html)}</ol></section>
<section><h2>Lo que verán de ti en mayo</h2><ul class="pruebas">{''.join(f'<li>{e(p)}</li>' for p in PRUEBAS)}</ul></section>
<footer>Inglés: 30 min de lunes a jueves (6:30–7:00) + 1 h el viernes. EF SET en las semanas 2, 12 y 23. Recordatorio diario por WhatsApp a las 4:50 AM (domingo 6:50 AM). Ejercicio 7–8 AM de lunes a sábado, en casa y sin equipo. Sábado (después de las 8) y noches: familia.</footer>
</div>
<script>
const W = {json.dumps([{k: w[k] for k in ("ini","n","tema","dom","rec")} for w in weeks], ensure_ascii=False)};
const hoyISO = new Intl.DateTimeFormat("en-CA",{{timeZone:"America/Santo_Domingo"}}).format(new Date());
const dias = (a,b)=>Math.round((Date.parse(b)-Date.parse(a))/864e5);
const dow = new Date(hoyISO+"T12:00:00Z").getUTCDay() || 7;
let cur = null; for (const w of W) if (w.ini <= hoyISO) cur = w;
if (cur && dias(cur.ini, hoyISO) >= 7) cur = null;
const K=document.getElementById("hoy-k"),T=document.getElementById("hoy-t"),P=document.getElementById("hoy-p"),M=document.getElementById("hoy-m");
if (!cur && hoyISO < W[0].ini) {{ K.textContent="Mañana empieza"; T.textContent="El plan arranca el martes 24 de noviembre a las 5 AM"; P.textContent=W[0].tema; }}
else if (!cur) {{ T.textContent="Plan completado. Toca la revisión y el siguiente semestre."; }}
else {{
  const ING={{1:"6:30–7:00 inglés: escucha un episodio de 6 Minute English (BBC) y anota 5 frases.",2:"6:30–7:00 inglés: graba 2 min explicando en inglés lo que practicaste.",3:"6:30–7:00 inglés: escucha 6 Minute English y repite en voz alta (shadowing).",4:"6:30–7:00 inglés: graba 2 min explicando el tema de la semana."}};
  const tareas={{1:["Teoría · 5–6:30 AM",cur.tema+" — "+ING[1]],2:["Práctica · 5–6:30 AM","Ejercicios de lo de ayer: "+cur.tema+" — "+ING[2]],3:["Teoría 2 · 5–6:30 AM",cur.tema+" — "+ING[3]],
    4:["Práctica 2 · 5–6:30 AM","Cierra el tema y prepara lo del domingo: "+cur.dom+" — "+ING[4]],5:["Inglés + LinkedIn · 5–7 AM","5–6: conversación en inglés de 30 min (voz con IA o un compañero de Tandem) + repaso de errores. 6–7: escribe y publica tu post semanal."],
    6:["Sábado","Día libre. Familia."],7:["Proyecto · 7–11 AM",cur.dom+". Súbelo a GitHub al terminar."]}};
  const dt_=(cur.n===1&&hoyISO===cur.ini)?1:dow;
  K.textContent="Semana "+cur.n+" de 24 · Hoy"; T.textContent=tareas[dt_][0]; P.textContent=tareas[dt_][1];
  M.textContent=cur.rec!=="-"?"Recurso: "+cur.rec:"";
  document.getElementById("s"+cur.n).classList.add("now");
  W.forEach(w=>{{ if (w.n<cur.n) document.getElementById("s"+w.n).classList.add("done"); }});
  const pct=Math.min(100,Math.max(0,(dias(W[0].ini,hoyISO)+1)/(dias(W[0].ini,W[W.length-1].ini)+7)*100));
  requestAnimationFrame(()=>document.getElementById("prog").style.width=pct+"%");
  document.querySelectorAll(".fase").forEach(f=>{{ const a=+f.dataset.a,b=+f.dataset.b;
    const v = cur.n>b?100:cur.n<a?0:((cur.n-a)+dow/7)/(b-a+1)*100;
    requestAnimationFrame(()=>f.querySelector("i").style.width=v+"%"); }});
}}
const d=document.querySelector('.dia[data-d="'+dow+'"]'); if (d) d.classList.add("now");
</script>
"""
(D / "web.html").write_text(web)

# ---------- puerta (A4 imprimible) ----------
filas = []
for w in weeks:
    f = fase_de(w["n"])
    if w["n"] == FASES[f][0]:
        filas.append(f'<tr class="ph"><td colspan="4">{e(FASES[f][2])} · {e(FASES[f][3])}</td></tr>')
    filas.append(f'<tr><td class="c">☐</td><td class="n">{w["n"]}</td><td class="f">{w["rango"]}</td><td><b>{e(w["tema"])}</b><br><span>Dom: {e(w["dom"])}</span></td></tr>')
puerta = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Ruta Pro 24 semanas</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap">
<style>
@page{{size:A4;margin:8mm 10mm}}
:root{{--ink:#0c111b;--muted:#5b6678;--green:#0a9a5a;--line:#d5dce6}}
body{{margin:0;font:7.3pt/1.27 "Plus Jakarta Sans",sans-serif;color:var(--ink)}}
header{{display:flex;align-items:center;gap:10px;background:var(--ink);color:#fff;border-radius:8px;padding:9px 12px}}
header img{{width:34px;height:34px;border-radius:7px}}
h1{{font:800 19pt/1 Outfit,sans-serif;margin:0}} h1 span{{color:#14f08a}} header p{{margin:2px 0 0;color:#aab6c8;font-size:8pt}}
.rut{{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:6px 0}}
.rut div{{border:1.2px solid var(--line);border-radius:6px;padding:4px;text-align:center}} .rut b{{font:600 9pt Outfit,sans-serif;display:block}}
.rut .x{{background:#f1f4f8;color:var(--muted)}} .rut .g{{border-color:var(--green)}}
table{{width:100%;border-collapse:collapse}}
td{{border-bottom:.6pt solid var(--line);padding:2px 4px;vertical-align:top}}
td span{{color:var(--muted)}} .c{{width:12px;font-size:10pt;line-height:1;color:var(--green)}} .n{{width:14px;font:600 9pt Outfit,sans-serif;color:var(--green)}} .f{{width:68px;color:var(--muted);white-space:nowrap}}
.ph td{{background:var(--ink);color:#14f08a;font:600 8pt Outfit,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:3px 6px;border:0}}
footer{{margin-top:7px;display:flex;gap:10px;font-size:7.4pt}} footer div{{flex:1;border:1.2px solid var(--green);border-radius:6px;padding:5px 7px}} footer b{{font-family:Outfit,sans-serif;color:var(--green)}}
</style></head><body>
<header><img src="{logo}" alt=""><div><h1>Ruta Pro <span>24 semanas</span></h1><p>24 nov 2026 → 9 may 2027 · Automatización RPA + Agentes de IA · Dorevio</p></div></header>
<div class="rut">{''.join(f'<div class="{"x" if h=="Libre" else ("g" if d=="Dom" else "")}"><b>{d}</b>{h}<br>{e(t)}</div>' for d,h,t in RUTINA)}</div>
<table>{''.join(filas)}</table>
<footer><div><b>En mayo tendrás:</b> {e(" · ".join(PRUEBAS[:6]))}</div><div><b>Regla:</b> sábado después del ejercicio y las noches son de la familia. Si fallas un día, no lo recuperes de noche: sigue al día siguiente.</div></footer>
</body></html>"""
(D / "puerta.html").write_text(puerta)
print("ok", len(web), len(puerta))

# ---------- index.html independiente para GitHub Pages ----------
(D / "index.html").write_text('<!doctype html>\n<html lang="es"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}</style>\n'
    + web + "\n</html>\n")
