import streamlit as st
import pandas as pd
import re
import os
from datetime import date

st.set_page_config(
    page_title="Dashboard Tickets — iGreen",
    page_icon="🌿",
    layout="wide",
)

st.markdown("""
<style>
body,[data-testid="stAppViewContainer"]{background:#f4f6f4!important;}
.header-bar{background:#1a3a2a;color:#fff;padding:14px 24px;border-radius:8px;
  display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;}
.header-title{font-size:20px;font-weight:700;}
.header-meta{font-size:12px;color:#a8c9b0;}
.section-label{font-size:11px;font-weight:700;color:#2d6a40;
  letter-spacing:.07em;text-transform:uppercase;margin:18px 0 8px 0;}
.card{border-radius:8px;padding:14px 16px;color:#fff;margin-bottom:4px;}
.card-red{background:#8b1c1c;}.card-dark{background:#1a3a2a;}
.card-title{font-size:13px;font-weight:600;margin-bottom:4px;}
.card-num{font-size:34px;font-weight:700;margin-bottom:8px;line-height:1;}
.card-row{display:flex;justify-content:space-between;font-size:12px;
  padding:3px 0;border-top:1px solid rgba(255,255,255,0.15);}
.card-lbl{color:rgba(255,255,255,0.75);}
.card-val{font-weight:600;}.red-v{color:#ffaaaa;}
.card-val-sub{display:flex;justify-content:space-between;font-size:11px;
  padding:3px 0;border-top:1px solid rgba(255,255,255,0.08);color:rgba(255,255,255,0.6);}
.card-val-hl{display:flex;justify-content:space-between;font-size:12px;
  padding:3px 0;border-top:1px solid rgba(255,255,255,0.25);color:#fff;font-weight:600;}
.top5-card{background:#fff;border-radius:8px;padding:12px;
  border-left:4px solid #8b1c1c;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:4px;}
.top5-rank{font-size:11px;font-weight:700;color:#999;}
.top5-nome{font-size:14px;font-weight:700;color:#222;margin:2px 0;}
.top5-fam{display:inline-block;padding:1px 7px;border-radius:3px;
  font-size:10px;font-weight:700;color:#fff;margin-bottom:8px;}
.bg-e{background:#2d6a40;}.bg-a{background:#b8860b;}.bg-i{background:#1a5c8a;}
.top5-stat{display:flex;justify-content:space-between;
  font-size:11px;padding:3px 0;border-top:1px solid #eee;}
.t5-lbl{color:#777;}.t5-val{font-weight:700;color:#c0392b;}
.t5-val-ok{font-weight:700;color:#2d6a40;}
.progress-bar{background:#f0f0f0;border-radius:3px;height:6px;margin-top:6px;overflow:hidden;}
.progress-fill{height:100%;border-radius:3px;background:#8b1c1c;}
table.main-table{width:100%;border-collapse:collapse;font-size:12px;}
table.main-table thead tr{background:#1a3a2a;color:#fff;}
table.main-table th{padding:8px;font-size:11px;text-align:center;
  font-weight:600;line-height:1.3;}
table.main-table th:first-child{text-align:left;}
table.main-table td{padding:6px 8px;border-bottom:1px solid #eee;text-align:center;}
table.main-table td:first-child{text-align:left;}
table.main-table tr.fam-row td{background:#e8f0eb;font-weight:600;}
table.main-table tr.forn-row td:first-child{padding-left:24px;color:#555;}
table.main-table tr.total-row td{background:#1a3a2a;color:#fff;font-weight:700;border:none;}
.n-red{color:#c0392b;font-weight:600;}.n-grn{color:#2d6a40;font-weight:600;}
.n-brn{color:#7a5820;font-weight:600;}.n-grey{color:#555;font-weight:600;}
.v-sub{font-size:10px;color:#888;display:block;}
.v-sub-wht{font-size:10px;color:#a8c9b0;display:block;}
.zero{color:#bbb;}
.legend{display:flex;flex-wrap:wrap;gap:12px;font-size:11px;color:#555;margin:8px 0 12px 0;}
.leg-item{display:flex;align-items:center;gap:5px;}
.leg-sq{width:10px;height:10px;border-radius:2px;display:inline-block;}
.date-btn{
  background:#1a3a2a;color:#fff;border:none;border-radius:6px;
  padding:8px 20px;font-size:13px;font-weight:600;cursor:pointer;
  margin-right:8px;
}
.date-btn-active{background:#2d6a40;}
</style>
""", unsafe_allow_html=True)

FAMILIA_MAP = {
    'COMERC':'Energizados','VANTAGE':'AZA','MATO GROSSO ENERGIA':'AZA',
    'COTESA-MOVE':'AZA','SUNCLICK':'AZA','FARO':'AZA','ULTRA':'AZA',
    'SUNNE':'iVolt','SOLATIO':'iVolt','EDP':'iVolt',
    'FIT':'iVolt','GV':'iVolt','BC':'iVolt'
}
FORN_BY_FAM = {
    'Energizados':['COMERC'],
    'AZA':['VANTAGE','MATO GROSSO ENERGIA','COTESA-MOVE','SUNCLICK','FARO','ULTRA'],
    'iVolt':['SUNNE','SOLATIO','EDP','FIT','GV','BC']
}
FAM_BADGE = {'Energizados':'bg-e','AZA':'bg-a','iVolt':'bg-i'}
SLA_DAYS  = 3

def parse_valor(v):
    if pd.isna(v) or str(v).strip() in ['-','']: return 0.0
    v = str(v).replace('R$','').replace(' ','').replace('.','').replace(',','.')
    try: return float(v)
    except: return 0.0

def fmt_r(v):
    if v == 0: return 'R$ 0'
    return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.',',').replace('X','.')

def pct(n, t): return f'{n/t*100:.1f}%' if t else '0.0%'

# ── Listar planilhas disponíveis na pasta dados/ ──────────────────────────────
def listar_planilhas():
    pasta = 'dados'
    if not os.path.exists(pasta):
        return {}
    arquivos = sorted([f for f in os.listdir(pasta) if f.endswith('.xlsx')], reverse=True)
    datas = {}
    for arq in arquivos:
        # Extrai data do nome: Tickets_13mai2026.xlsx → "13/05/2026"
        m = re.search(r'(\d{1,2})([a-z]{3})(\d{4})', arq, re.IGNORECASE)
        if m:
            dia, mes_str, ano = m.group(1), m.group(2).lower(), m.group(3)
            meses = {'jan':'01','fev':'02','mar':'03','abr':'04','mai':'05','jun':'06',
                     'jul':'07','ago':'08','set':'09','out':'10','nov':'11','dez':'12'}
            mes = meses.get(mes_str, '00')
            label = f"{dia.zfill(2)}/{mes}/{ano}"
        else:
            label = arq.replace('.xlsx','').replace('Tickets_','')
        datas[label] = os.path.join(pasta, arq)
    return datas

@st.cache_data
def load_data(filepath):
    xl = pd.ExcelFile(filepath)
    sheets = [s for s in xl.sheet_names if s != 'Resumo por Tipo']
    dfs = []
    for sheet in sheets:
        df = pd.read_excel(filepath, sheet_name=sheet)
        forn = sheet.replace('Tickets - ', '')
        df['_Fornecedora'] = forn
        df['_Familia'] = FAMILIA_MAP.get(forn, 'Outros')
        dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)
    bko_cols = [c for c in data.columns if c.startswith('BKO') and 'Atribuído em' not in c]
    def tem_bko(row):
        for col in bko_cols:
            if str(row[col]).strip() not in ['-','nan','','NaT']: return True
        return False
    data['_Atribuido']    = data.apply(tem_bko, axis=1)
    data['_Valor']        = data['Valor Total'].apply(parse_valor)
    data['_CriadoTS']     = pd.to_datetime(data['Criado Em'], errors='coerce')
    data['_FinalizadoTS'] = pd.to_datetime(data['Data Finalização'], errors='coerce')
    return data

def calc_on_date(data, cutoff_date):
    cut   = pd.Timestamp(cutoff_date).replace(hour=23, minute=59, second=59)
    sla_s = SLA_DAYS * 24 * 3600
    rows  = []
    for _, r in data[data['_CriadoTS'] <= cut].iterrows():
        c    = r['_CriadoTS']
        f    = r['_FinalizadoTS']
        enc  = pd.notna(f) and f <= cut
        secs = int((f-c).total_seconds()) if enc else int((cut-c).total_seconds())
        at   = secs >= sla_s
        rows.append({
            'Fornecedora': r['_Fornecedora'], 'Familia': r['_Familia'],
            'Atribuido':   r['_Atribuido'],   'Valor':   r['_Valor'],
            'Atraso':  not enc and at,  'NoPrazo': not enc and not at,
            'EncAtraso':   enc and at,  'EncPrazo': enc and not at,
        })
    return pd.DataFrame(rows)

def agg(df):
    def s(mask): return df[mask]['Valor'].sum()
    ap = df['Atribuido'] & df['NoPrazo']
    aa = df['Atribuido'] & df['Atraso']
    np_ = ~df['Atribuido'] & df['NoPrazo']
    na = ~df['Atribuido'] & df['Atraso']
    return {
        'total':len(df), 'valor':df['Valor'].sum(),
        'atraso_n':df['Atraso'].sum(), 'atraso_v':s(df['Atraso']),
        'atr_atrib':(df['Atribuido']&df['Atraso']).sum(),
        'atr_natrib':(~df['Atribuido']&df['Atraso']).sum(),
        'atr_prazo':ap.sum(),  'atr_prazo_v':s(ap),
        'atr_atraso':aa.sum(), 'atr_atraso_v':s(aa),
        'nat_prazo':np_.sum(), 'nat_prazo_v':s(np_),
        'nat_atraso':na.sum(), 'nat_atraso_v':s(na),
        'enc_prazo':df['EncPrazo'].sum(),  'enc_prazo_v':s(df['EncPrazo']),
        'enc_atraso':df['EncAtraso'].sum(),'enc_atraso_v':s(df['EncAtraso']),
    }

def cel(n, v, cls):
    vs = f'<span class="v-sub">{fmt_r(v)}</span>' if v > 0 else ''
    return f'<td class="{cls}">{"—" if n==0 else n}{vs}</td>'

def cel_t(n, v, wht=False):
    vc  = 'v-sub-wht' if wht else 'v-sub'
    vs  = f'<span class="{vc}">{fmt_r(v)}</span>' if v > 0 else ''
    num = f'<strong>{n}</strong>' if wht else str(n)
    return f'<td>{num}{vs}</td>'

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('### 🌿 iGreen Energy')
    st.markdown('**Dashboard de Tickets**')
    st.divider()
    st.markdown('**Como atualizar:**')
    st.markdown('Suba a nova planilha na pasta `dados/` do GitHub com o nome:\n\n`Tickets_DDmesAAAA.xlsx`\n\nExemplo: `Tickets_20mai2026.xlsx`')
    st.divider()
    st.markdown('**SLA:** 3 dias úteis')

# ── SELECIONAR DATA (planilha) ─────────────────────────────────────────────────
planilhas = listar_planilhas()

if not planilhas:
    st.error('Nenhuma planilha encontrada na pasta dados/. Suba um arquivo .xlsx no formato Tickets_DDmesAAAA.xlsx')
    st.stop()

st.markdown('<div class="section-label">Selecionar data base</div>', unsafe_allow_html=True)

datas_disponiveis = list(planilhas.keys())
if 'data_selecionada' not in st.session_state:
    st.session_state.data_selecionada = datas_disponiveis[0]

cols_btn = st.columns(min(len(datas_disponiveis), 6))
for i, label in enumerate(datas_disponiveis):
    with cols_btn[i % 6]:
        ativo = st.session_state.data_selecionada == label
        if st.button(label, key=f'btn_{label}',
                     type='primary' if ativo else 'secondary',
                     use_container_width=True):
            st.session_state.data_selecionada = label
            st.rerun()

data_sel = st.session_state.data_selecionada
filepath = planilhas[data_sel]

# ── CARREGAR E CALCULAR ────────────────────────────────────────────────────────
with st.spinner('Carregando dados...'):
    data = load_data(filepath)

# Usar a data máxima da planilha como cutoff
cutoff = data['_CriadoTS'].max().date()
tickets = calc_on_date(data, cutoff)
m       = agg(tickets)
total   = m['total']

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header-bar">
  <span class="header-title">Dashboard de Tickets — Famílias iGreen</span>
  <span class="header-meta">Base: {data_sel} &nbsp;|&nbsp; SLA: {SLA_DAYS} dias úteis &nbsp;|&nbsp; {total:,} tickets</span>
</div>
""", unsafe_allow_html=True)

# ── FAM METRICS ───────────────────────────────────────────────────────────────
fam_data = {}
for fam in ['Energizados','AZA','iVolt']:
    ft  = tickets[tickets['Familia']==fam]
    fm  = agg(ft)
    byf = ft[ft['Atraso']].groupby('Fornecedora').size()
    maior   = byf.idxmax() if len(byf) > 0 else '-'
    maior_n = int(byf.max()) if len(byf) > 0 else 0
    fam_data[fam] = {'m':fm,'maior':maior,'maior_n':maior_n}

# ── CARDS ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">NÃO RESOLVIDOS EM ATRASO — abertos que ultrapassaram 3 dias úteis</div>', unsafe_allow_html=True)
cols = st.columns(4)
for i, fam in enumerate(['Energizados','AZA','iVolt']):
    fd = fam_data[fam]; fm = fd['m']
    sub_lbl = 'Fornecedora' if fam=='Energizados' else 'Maior atraso'
    sub_val = 'COMERC' if fam=='Energizados' else f"{fd['maior']} ({fd['maior_n']})"
    with cols[i]:
        st.markdown(f"""
        <div class="card card-red">
          <div class="card-title">{fam}</div>
          <div class="card-num">{fm['atraso_n']}</div>
          <div class="card-row"><span class="card-lbl">Atribuído (BKO)</span><span class="card-val red-v">{fm['atr_atrib']}</span></div>
          <div class="card-row"><span class="card-lbl">Não atribuído</span><span class="card-val">{fm['atr_natrib']}</span></div>
          <div class="card-row"><span class="card-lbl">{sub_lbl}</span><span class="card-val">{sub_val}</span></div>
          <div class="card-val-sub"><span>Valor em atraso</span><span>{fmt_r(fm['atraso_v'])}</span></div>
          <div class="card-val-hl"><span>Valor total família</span><span>{fmt_r(fm['valor'])}</span></div>
        </div>""", unsafe_allow_html=True)

with cols[3]:
    st.markdown(f"""
    <div class="card card-dark">
      <div class="card-title">Total geral</div>
      <div class="card-num">{m['atraso_n']}</div>
      <div class="card-row"><span class="card-lbl">Atribuído (BKO)</span><span class="card-val red-v">{m['atr_atrib']}</span></div>
      <div class="card-row"><span class="card-lbl">Não atribuído</span><span class="card-val">{m['atr_natrib']}</span></div>
      <div class="card-row"><span class="card-lbl">% do total</span><span class="card-val">{pct(m['atraso_n'],total)}</span></div>
      <div class="card-val-sub"><span>Valor em atraso</span><span>{fmt_r(m['atraso_v'])}</span></div>
      <div class="card-val-hl"><span>Valor total geral</span><span>{fmt_r(m['valor'])}</span></div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── TOP 5 ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">TOP 5 FORNECEDORAS COM MAIS TICKETS EM ATRASO</div>', unsafe_allow_html=True)
top5 = (tickets[tickets['Atraso']]
        .groupby(['Fornecedora','Familia'])
        .agg(n=('Atraso','count'), v=('Valor','sum'))
        .reset_index().sort_values('n',ascending=False).head(5))

max_n  = int(top5['n'].max()) if len(top5) > 0 else 1
ords   = ['1º','2º','3º','4º','5º']
t5cols = st.columns(5)
for i, row in enumerate(top5.itertuples()):
    badge = FAM_BADGE.get(row.Familia,'bg-e')
    v_cls = 't5-val' if row.v > 0 else 't5-val-ok'
    with t5cols[i]:
        st.markdown(f"""
        <div class="top5-card">
          <div class="top5-rank">{ords[i]} lugar</div>
          <div class="top5-nome">{row.Fornecedora}</div>
          <span class="top5-fam {badge}">{row.Familia}</span>
          <div class="top5-stat"><span class="t5-lbl">Tickets em atraso</span><span class="t5-val">{row.n}</span></div>
          <div class="top5-stat"><span class="t5-lbl">Valor afetado</span><span class="{v_cls}">{fmt_r(row.v)}</span></div>
          <div class="progress-bar"><div class="progress-fill" style="width:{int(row.n/max_n*100)}%"></div></div>
        </div>""", unsafe_allow_html=True)

if len(top5) == 0:
    st.info('Nenhum ticket em atraso nesta data.')

st.divider()

# ── TABELA ────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="section-label">VISÃO COMPLETA — {total:,} tickets por categoria</div>', unsafe_allow_html=True)
st.markdown("""
<div class="legend">
  <span class="leg-item"><span class="leg-sq" style="background:#2d6a40"></span>Atribuído · no prazo</span>
  <span class="leg-item"><span class="leg-sq" style="background:#c0392b"></span>Atribuído · em atraso</span>
  <span class="leg-item"><span class="leg-sq" style="background:#7a5820"></span>Não atribuído · no prazo</span>
  <span class="leg-item"><span class="leg-sq" style="background:#8b1c1c"></span>Não atribuído · em atraso</span>
  <span class="leg-item"><span class="leg-sq" style="background:#1f6b47"></span>Encerrado · no prazo</span>
  <span class="leg-item"><span class="leg-sq" style="background:#555"></span>Encerrado · em atraso</span>
</div>""", unsafe_allow_html=True)

tbl = """<table class="main-table"><thead><tr>
  <th style="text-align:left">Família / Fornecedora</th>
  <th>Atribuído<br>no prazo</th><th>Atribuído<br>em atraso</th>
  <th>Não atrib.<br>no prazo</th><th>Não atrib.<br>em atraso</th>
  <th>Encerrado<br>no prazo</th><th>Encerrado<br>em atraso</th><th>Total</th>
</tr></thead><tbody>"""

t6n=[0]*6; t6v=[0]*6
clss=['n-grn','n-red','n-brn','n-red','n-grn','n-grey']
keys_n=['atr_prazo','atr_atraso','nat_prazo','nat_atraso','enc_prazo','enc_atraso']
keys_v=['atr_prazo_v','atr_atraso_v','nat_prazo_v','nat_atraso_v','enc_prazo_v','enc_atraso_v']

for fam in ['Energizados','AZA','iVolt']:
    ft  = tickets[tickets['Familia']==fam]
    fm  = agg(ft)
    ns  = [fm[k] for k in keys_n]
    vs  = [fm[k] for k in keys_v]
    for i in range(6): t6n[i]+=ns[i]; t6v[i]+=vs[i]
    badge = FAM_BADGE[fam]
    cells = ''.join(cel(ns[i],vs[i],clss[i]) for i in range(6))
    tbl  += f'<tr class="fam-row"><td><span class="top5-fam {badge}" style="margin-right:6px">{fam}</span></td>{cells}{cel_t(fm["total"],fm["valor"])}</tr>'
    for forn in FORN_BY_FAM[fam]:
        fd2 = tickets[tickets['Fornecedora']==forn]
        if not len(fd2): continue
        fm2 = agg(fd2)
        ns2 = [fm2[k] for k in keys_n]; vs2 = [fm2[k] for k in keys_v]
        c2  = ''.join(cel(ns2[i],vs2[i],clss[i]) for i in range(6))
        tbl += f'<tr class="forn-row"><td>{forn}</td>{c2}{cel_t(fm2["total"],fm2["valor"])}</tr>'

tc = ''.join(cel(t6n[i],t6v[i],'n-grey') for i in range(6))
tbl += f'<tr class="total-row"><td><strong>Total geral</strong></td>{tc}{cel_t(total,m["valor"],wht=True)}</tr>'
tbl += '</tbody></table>'
st.markdown(tbl, unsafe_allow_html=True)
st.markdown('<br><div style="text-align:right;font-size:10px;color:#aaa">iGreen Energy · Setor Inadimplência Comercial</div>', unsafe_allow_html=True)
