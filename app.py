import streamlit as st
import pandas as pd
import re
import os

st.set_page_config(page_title="SLA de Tickets — iGreen Energy", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#0a0a0a!important;color:#fff!important;font-family:'Inter',sans-serif!important;}
[data-testid="stSidebar"]{background:#111!important;border-right:1px solid #1a1a1a!important;}
[data-testid="stSidebar"] *{color:#aaa!important;}
.block-container{padding:1.5rem 2rem!important;}
button[kind="primary"]{background:#39FF14!important;color:#000!important;font-weight:700!important;border:none!important;border-radius:6px!important;}
button[kind="secondary"]{background:#111!important;color:#39FF14!important;font-weight:600!important;border:1px solid #39FF1440!important;border-radius:6px!important;}
hr{border-color:#1a1a1a!important;}
.ig-header{background:linear-gradient(135deg,#0d1f0d 0%,#0a0a0a 100%);border:1px solid #39FF1420;border-radius:12px;padding:18px 24px;display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;}
.ig-logo{width:40px;height:40px;background:#39FF14;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;color:#000;margin-right:12px;flex-shrink:0;}
.ig-hl{display:flex;align-items:center;}
.ig-title{font-size:17px;font-weight:700;color:#fff;}
.ig-sub{font-size:10px;color:#39FF14;letter-spacing:.1em;text-transform:uppercase;margin-top:2px;}
.ig-meta{font-size:11px;color:#444;text-align:right;line-height:1.7;}
.ig-meta span{color:#39FF14;font-weight:600;}
.sec-label{font-size:10px;font-weight:700;color:#39FF14;letter-spacing:.1em;text-transform:uppercase;margin:18px 0 10px 0;display:flex;align-items:center;gap:8px;}
.sec-label::after{content:'';flex:1;height:1px;background:#1a1a1a;}
.card{background:#111;border:1px solid #1a1a1a;border-radius:10px;padding:16px;position:relative;overflow:hidden;}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.card-alert::before{background:#ff3b3b;}.card-total::before{background:#39FF14;}
.card-fam{font-size:10px;font-weight:700;color:#39FF14;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;}
.card-num{font-size:36px;font-weight:900;line-height:1;margin-bottom:10px;}
.num-red{color:#ff3b3b;}.num-grn{color:#39FF14;}
.card-row{display:flex;justify-content:space-between;font-size:11px;padding:4px 0;border-top:1px solid #1a1a1a;}
.c-lbl{color:#555;}.c-val{font-weight:600;color:#fff;}.c-red{font-weight:700;color:#ff3b3b;}.c-grn{font-weight:700;color:#39FF14;}
.card-hl{display:flex;justify-content:space-between;font-size:12px;padding:5px 0;border-top:1px solid #222;margin-top:2px;}
.hl-lbl{color:#666;}.hl-val{font-weight:700;color:#39FF14;}
.t5-card{background:#111;border:1px solid #1a1a1a;border-radius:10px;padding:14px;border-left:3px solid #ff3b3b;}
.t5-rank{font-size:10px;font-weight:700;color:#444;letter-spacing:.06em;}
.t5-nome{font-size:14px;font-weight:800;color:#fff;margin:3px 0;}
.t5-fam{display:inline-block;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700;margin-bottom:8px;}
.f-e{background:#0d2b0d;color:#39FF14;border:1px solid #39FF1430;}
.f-a{background:#2b1f00;color:#ffaa00;border:1px solid #ffaa0030;}
.f-i{background:#001b2b;color:#00aaff;border:1px solid #00aaff30;}
.t5-row{display:flex;justify-content:space-between;font-size:11px;padding:3px 0;border-top:1px solid #1a1a1a;}
.t5-lbl{color:#555;}.t5-val{font-weight:700;color:#ff3b3b;}.t5-ok{font-weight:600;color:#555;}
.bar-bg{background:#1a1a1a;border-radius:3px;height:4px;margin-top:8px;}
.bar-fg{height:100%;border-radius:3px;background:#ff3b3b;}
table.igt{width:100%;border-collapse:collapse;font-size:12px;}
table.igt thead tr{border-bottom:1px solid #39FF1425;}
table.igt th{padding:10px 8px;font-size:10px;font-weight:700;color:#39FF14;text-align:center;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;}
table.igt th:first-child{text-align:left;}
table.igt td{padding:7px 8px;border-bottom:1px solid #111;text-align:center;color:#888;white-space:nowrap;}
table.igt td:first-child{text-align:left;white-space:normal;}
table.igt tr.fr td{background:#0f0f0f;font-weight:700;cursor:pointer;}
table.igt tr.fr:hover td{background:#141414;}
table.igt tr.dr td{background:#0a0a0a;}
table.igt tr.dr td:first-child{padding-left:28px;color:#555;font-size:11px;}
table.igt tr.tr td{background:#0d1f0d;font-weight:700;border-top:1px solid #39FF1425;border-bottom:none;}
.ng{color:#39FF14!important;font-weight:700!important;}.nr{color:#ff3b3b!important;font-weight:700!important;}
.na{color:#ffaa00!important;font-weight:700!important;}.ns{color:#444!important;}
.nt{color:#39FF14!important;font-weight:800!important;}.vm{color:#00aaff!important;font-size:11px!important;}
.vs{font-size:10px;color:#333;display:block;}.z{color:#222!important;}
.badge{display:inline-block;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700;margin-right:6px;}
.be{background:#0d2b0d;color:#39FF14;border:1px solid #39FF1425;}
.ba{background:#2b1f00;color:#ffaa00;border:1px solid #ffaa0025;}
.bi{background:#001b2b;color:#00aaff;border:1px solid #00aaff25;}
.leg{display:flex;flex-wrap:wrap;gap:12px;font-size:11px;color:#444;margin:6px 0 14px 0;}
.li{display:flex;align-items:center;gap:5px;}.ls{width:8px;height:8px;border-radius:2px;}
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
FAM_BADGE={'Energizados':'be','AZA':'ba','iVolt':'bi'}
FAM_T5={'Energizados':'f-e','AZA':'f-a','iVolt':'f-i'}
SLA_DAYS=3

def parse_valor(v):
    if pd.isna(v) or str(v).strip() in ['-','']: return 0.0
    v=str(v).replace('R$','').replace(' ','').replace('.','').replace(',','.')
    try: return float(v)
    except: return 0.0

def fmt_r(v):
    if v==0: return '-'
    return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.',',').replace('X','.')

def pct(n,t): return f'{n/t*100:.1f}%' if t else '0%'

def listar_planilhas():
    pasta='dados'
    if not os.path.exists(pasta): return {}
    arquivos=sorted([f for f in os.listdir(pasta) if f.endswith('.xlsx')],reverse=True)
    datas={}
    for arq in arquivos:
        m=re.search(r'(\d{1,2})([a-z]{3})(\d{4})',arq,re.IGNORECASE)
        if m:
            dia,mes_str,ano=m.group(1),m.group(2).lower(),m.group(3)
            meses={'jan':'01','fev':'02','mar':'03','abr':'04','mai':'05','jun':'06','jul':'07','ago':'08','set':'09','out':'10','nov':'11','dez':'12'}
            label=f"{dia.zfill(2)}/{meses.get(mes_str,'00')}/{ano}"
        else:
            label=arq.replace('.xlsx','').replace('Tickets_','')
        datas[label]=os.path.join(pasta,arq)
    return datas

@st.cache_data
def load_data(filepath):
    xl=pd.ExcelFile(filepath)
    sheets=[s for s in xl.sheet_names if s!='Resumo por Tipo']
    dfs=[]
    for sheet in sheets:
        df=pd.read_excel(filepath,sheet_name=sheet)
        forn=sheet.replace('Tickets - ','')
        df['_Fornecedora']=forn
        df['_Familia']=FAMILIA_MAP.get(forn,'Outros')
        dfs.append(df)
    data=pd.concat(dfs,ignore_index=True)
    bko_cols=[c for c in data.columns if c.startswith('BKO') and 'Atribuído em' not in c]
    def tem_bko(row):
        for col in bko_cols:
            if str(row[col]).strip() not in ['-','nan','','NaT']: return True
        return False
    data['_Atribuido']=data.apply(tem_bko,axis=1)
    data['_Valor']=data['Valor Total'].apply(parse_valor)
    data['_CriadoTS']=pd.to_datetime(data['Criado Em'],errors='coerce')
    data['_FinalizadoTS']=pd.to_datetime(data['Data Finalização'],errors='coerce')
    for col,dest in [('Média 1ª Resposta (Fornecedora)','_MediaResp'),('Média até Finalização (Fornecedora)','_MediaFin')]:
        if col in data.columns:
            data[dest]=data[col].apply(lambda x: str(x).strip() if str(x).strip() not in ['-','nan',''] else '-')
        else:
            data[dest]='-'
    return data

def get_medias(data,forn):
    fd=data[data['_Fornecedora']==forn]
    def fv(col):
        v=fd[col][fd[col]!='-']
        return v.iloc[0] if len(v)>0 else '-'
    return fv('_MediaResp'),fv('_MediaFin')

def calc_on_date(data,cutoff_date):
    cut=pd.Timestamp(cutoff_date).replace(hour=23,minute=59,second=59)
    sla_s=SLA_DAYS*24*3600
    rows=[]
    for _,r in data[data['_CriadoTS']<=cut].iterrows():
        c=r['_CriadoTS']; f=r['_FinalizadoTS']
        enc=pd.notna(f) and f<=cut
        secs=int((f-c).total_seconds()) if enc else int((cut-c).total_seconds())
        at=secs>=sla_s
        rows.append({'Fornecedora':r['_Fornecedora'],'Familia':r['_Familia'],
            'Atribuido':r['_Atribuido'],'Valor':r['_Valor'],
            'Atraso':not enc and at,'NoPrazo':not enc and not at,
            'EncAtraso':enc and at,'EncPrazo':enc and not at})
    return pd.DataFrame(rows)

def agg(df):
    def s(mask): return df[mask]['Valor'].sum() if mask.any() else 0
    ap=df['Atribuido']&df['NoPrazo']; aa=df['Atribuido']&df['Atraso']
    np_=~df['Atribuido']&df['NoPrazo']; na=~df['Atribuido']&df['Atraso']
    return{'total':len(df),'valor':df['Valor'].sum(),
        'atraso_n':int(df['Atraso'].sum()),'atraso_v':s(df['Atraso']),
        'atr_atrib':int((df['Atribuido']&df['Atraso']).sum()),
        'atr_natrib':int((~df['Atribuido']&df['Atraso']).sum()),
        'atr_prazo':int(ap.sum()),'atr_prazo_v':s(ap),
        'atr_atraso':int(aa.sum()),'atr_atraso_v':s(aa),
        'nat_prazo':int(np_.sum()),'nat_prazo_v':s(np_),
        'nat_atraso':int(na.sum()),'nat_atraso_v':s(na),
        'enc_prazo':int(df['EncPrazo'].sum()),'enc_prazo_v':s(df['EncPrazo']),
        'enc_atraso':int(df['EncAtraso'].sum()),'enc_atraso_v':s(df['EncAtraso'])}

def cel(n,v,cls):
    vs=f'<span class="vs">{fmt_r(v)}</span>' if v>0 else ''
    return f'<td class="{cls}">{"<span class=z>—</span>" if n==0 else n}{vs}</td>'

with st.sidebar:
    st.markdown('### ⚡ iGreen Energy')
    st.markdown('**SLA de Tickets**')
    st.divider()
    st.markdown('**Como atualizar:**\nSuba a planilha em `dados/` no GitHub:\n\n`Tickets_DDmesAAAA.xlsx`')
    st.divider()
    st.caption('SLA: 3 dias úteis · 13 fornecedoras · 3 famílias')

planilhas=listar_planilhas()
if not planilhas:
    st.error('Nenhuma planilha em dados/. Suba um arquivo Tickets_DDmesAAAA.xlsx no GitHub.')
    st.stop()

datas=list(planilhas.keys())
if 'data_sel' not in st.session_state: st.session_state.data_sel=datas[0]
if 'expanded' not in st.session_state: st.session_state.expanded=set()

st.markdown(f"""
<div class="ig-header">
  <div class="ig-hl">
    <div class="ig-logo">G</div>
    <div><div class="ig-title">Dashboard de Tickets</div><div class="ig-sub">Setor Inadimplência Comercial</div></div>
  </div>
  <div class="ig-meta">iGreen Energy &nbsp;·&nbsp; <span>SLA: {SLA_DAYS} dias úteis</span></div>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="sec-label">Base de dados</div>', unsafe_allow_html=True)
btn_cols=st.columns(min(len(datas),8))
for i,label in enumerate(datas):
    with btn_cols[i%8]:
        ativo=st.session_state.data_sel==label
        if st.button(label,key=f'btn_{label}',type='primary' if ativo else 'secondary',use_container_width=True):
            st.session_state.data_sel=label; st.session_state.expanded=set(); st.rerun()

with st.spinner(''):
    data=load_data(planilhas[st.session_state.data_sel])
    cutoff=data['_CriadoTS'].max().date()
    tickets=calc_on_date(data,cutoff)
    m=agg(tickets); total=m['total']

fam_data={}
for fam in ['Energizados','AZA','iVolt']:
    ft=tickets[tickets['Familia']==fam]; fm=agg(ft)
    byf=ft[ft['Atraso']].groupby('Fornecedora').size()
    maior=byf.idxmax() if len(byf)>0 else '-'
    maior_n=int(byf.max()) if len(byf)>0 else 0
    fam_data[fam]={'m':fm,'maior':maior,'maior_n':maior_n}

st.markdown('<div class="sec-label">Não resolvidos em atraso — apenas abertos</div>', unsafe_allow_html=True)
cols=st.columns(4)
for i,fam in enumerate(['Energizados','AZA','iVolt']):
    fd=fam_data[fam]; fm=fd['m']
    sub_lbl='Fornecedora' if fam=='Energizados' else 'Maior atraso'
    sub_val='COMERC' if fam=='Energizados' else f"{fd['maior']} ({fd['maior_n']})"
    with cols[i]:
        st.markdown(f"""
        <div class="card card-alert">
          <div class="card-fam">{fam}</div><div class="card-num num-red">{fm['atraso_n']}</div>
          <div class="card-row"><span class="c-lbl">Atribuído (BKO)</span><span class="c-red">{fm['atr_atrib']}</span></div>
          <div class="card-row"><span class="c-lbl">Não atribuído</span><span class="c-val">{fm['atr_natrib']}</span></div>
          <div class="card-row"><span class="c-lbl">{sub_lbl}</span><span class="c-val">{sub_val}</span></div>
          <div class="card-row"><span class="c-lbl">Valor em atraso</span><span class="c-val">{fmt_r(fm['atraso_v'])}</span></div>
          <div class="card-hl"><span class="hl-lbl">Valor total família</span><span class="hl-val">{fmt_r(fm['valor'])}</span></div>
        </div>""", unsafe_allow_html=True)
with cols[3]:
    st.markdown(f"""
    <div class="card card-total">
      <div class="card-fam">Total geral</div><div class="card-num num-grn">{m['atraso_n']}</div>
      <div class="card-row"><span class="c-lbl">Atribuído (BKO)</span><span class="c-red">{m['atr_atrib']}</span></div>
      <div class="card-row"><span class="c-lbl">Não atribuído</span><span class="c-val">{m['atr_natrib']}</span></div>
      <div class="card-row"><span class="c-lbl">% do total</span><span class="c-val">{pct(m['atraso_n'],total)}</span></div>
      <div class="card-row"><span class="c-lbl">Valor em atraso</span><span class="c-val">{fmt_r(m['atraso_v'])}</span></div>
      <div class="card-hl"><span class="hl-lbl">Valor total geral</span><span class="hl-val">{fmt_r(m['valor'])}</span></div>
    </div>""", unsafe_allow_html=True)

st.divider()
st.markdown('<div class="sec-label">Top 5 fornecedoras em atraso</div>', unsafe_allow_html=True)
top5=(tickets[tickets['Atraso']].groupby(['Fornecedora','Familia']).agg(n=('Atraso','count'),v=('Valor','sum')).reset_index().sort_values('n',ascending=False).head(5))
max_n=int(top5['n'].max()) if len(top5)>0 else 1
ords=['1º','2º','3º','4º','5º']; t5cols=st.columns(5)
for i,row in enumerate(top5.itertuples()):
    badge=FAM_T5.get(row.Familia,'f-e'); mr,mf=get_medias(data,row.Fornecedora)
    with t5cols[i]:
        st.markdown(f"""
        <div class="t5-card">
          <div class="t5-rank">{ords[i]} lugar</div><div class="t5-nome">{row.Fornecedora}</div>
          <span class="t5-fam {badge}">{row.Familia}</span>
          <div class="t5-row"><span class="t5-lbl">Em atraso</span><span class="t5-val">{row.n}</span></div>
          <div class="t5-row"><span class="t5-lbl">Valor</span><span class="t5-val">{fmt_r(row.v)}</span></div>
          <div class="t5-row"><span class="t5-lbl">Média 1ª resp.</span><span class="t5-ok">{mr}</span></div>
          <div class="t5-row"><span class="t5-lbl">Média finaliz.</span><span class="t5-ok">{mf}</span></div>
          <div class="bar-bg"><div class="bar-fg" style="width:{int(row.n/max_n*100)}%"></div></div>
        </div>""", unsafe_allow_html=True)

st.divider()
st.markdown(f'<div class="sec-label">Visão completa — {total:,} tickets</div>', unsafe_allow_html=True)
st.markdown("""<div class="leg">
  <span class="li"><span class="ls" style="background:#39FF14"></span>Atribuído · no prazo</span>
  <span class="li"><span class="ls" style="background:#ff3b3b"></span>Atribuído · em atraso</span>
  <span class="li"><span class="ls" style="background:#ffaa00"></span>Não atribuído · no prazo</span>
  <span class="li"><span class="ls" style="background:#ff3b3b"></span>Não atribuído · em atraso</span>
  <span class="li"><span class="ls" style="background:#39FF1440"></span>Encerrado · no prazo</span>
  <span class="li"><span class="ls" style="background:#333"></span>Encerrado · em atraso</span>
</div>""", unsafe_allow_html=True)

exp_cols=st.columns(3)
for i,fam in enumerate(['Energizados','AZA','iVolt']):
    with exp_cols[i]:
        is_open=fam in st.session_state.expanded
        if st.button(f"{{'▼' if is_open else '▶'}}  {fam}",key=f'exp_{fam}',type='primary' if is_open else 'secondary',use_container_width=True):
            if is_open: st.session_state.expanded.discard(fam)
            else: st.session_state.expanded.add(fam)
            st.rerun()

keys_n=['atr_prazo','atr_atraso','nat_prazo','nat_atraso','enc_prazo','enc_atraso']
keys_v=['atr_prazo_v','atr_atraso_v','nat_prazo_v','nat_atraso_v','enc_prazo_v','enc_atraso_v']
clss=['ng','nr','na','nr','ng','ns']

tbl="""<table class="igt"><thead><tr>
  <th style="text-align:left">Família / Fornecedora</th>
  <th>Atrib.<br>Prazo</th><th>Atrib.<br>Atraso</th>
  <th>N.Atrib.<br>Prazo</th><th>N.Atrib.<br>Atraso</th>
  <th>Enc.<br>Prazo</th><th>Enc.<br>Atraso</th>
  <th>Total</th><th>Média<br>1ª Resp.</th><th>Média<br>Finaliz.</th>
</tr></thead><tbody>"""

t6n=[0]*6; t6v=[0]*6
for fam in ['Energizados','AZA','iVolt']:
    ft=tickets[tickets['Familia']==fam]; fm=agg(ft)
    ns=[fm[k] for k in keys_n]; vs=[fm[k] for k in keys_v]
    for i in range(6): t6n[i]+=ns[i]; t6v[i]+=vs[i]
    badge=FAM_BADGE[fam]
    cells=''.join(cel(ns[i],vs[i],clss[i]) for i in range(6))
    vt=f'<span class="vs">{fmt_r(fm["valor"])}</span>' if fm["valor"]>0 else ''
    tbl+=f'<tr class="fr"><td><span class="badge {badge}">{fam}</span></td>{cells}<td class="nt">{fm["total"]}{vt}</td><td>—</td><td>—</td></tr>'
    if fam in st.session_state.expanded:
        for forn in FORN_BY_FAM[fam]:
            fd2=tickets[tickets['Fornecedora']==forn]
            if not len(fd2): continue
            fm2=agg(fd2); ns2=[fm2[k] for k in keys_n]; vs2=[fm2[k] for k in keys_v]
            c2=''.join(cel(ns2[i],vs2[i],clss[i]) for i in range(6))
            vt2=f'<span class="vs">{fmt_r(fm2["valor"])}</span>' if fm2["valor"]>0 else ''
            mr,mf=get_medias(data,forn)
            mr_h=f'<span class="vm">{mr}</span>' if mr!='-' else '<span class="z">—</span>'
            mf_h=f'<span class="vm">{mf}</span>' if mf!='-' else '<span class="z">—</span>'
            tbl+=f'<tr class="dr"><td>{forn}</td>{c2}<td>{fm2["total"]}{vt2}</td><td>{mr_h}</td><td>{mf_h}</td></tr>'

tc=''.join(cel(t6n[i],t6v[i],clss[i]) for i in range(6))
vt_tot=f'<span class="vs">{fmt_r(m["valor"])}</span>' if m["valor"]>0 else ''
tbl+=f'<tr class="tr"><td>TOTAL GERAL</td>{tc}<td class="nt">{total}{vt_tot}</td><td>—</td><td>—</td></tr>'
tbl+='</tbody></table>'
st.markdown(tbl,unsafe_allow_html=True)
st.markdown('<br><div style="text-align:right;font-size:10px;color:#222">iGreen Energy · Setor Inadimplência Comercial</div>',unsafe_allow_html=True)
