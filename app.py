import streamlit as st
import pandas as pd
import re
import os
import io
import plotly.graph_objects as go

st.set_page_config(page_title="SLA de Tickets — iGreen Energy", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
    background:#0f0f0f!important;color:#d0d0d0!important;font-family:'Inter',sans-serif!important;}
[data-testid="stSidebar"]{background:#141414!important;border-right:1px solid #1e1e1e!important;}
[data-testid="stSidebar"] *{color:#888!important;font-size:13px!important;}
.block-container{padding:1.5rem 2rem!important;}
button[kind="primary"]{background:#2e7d52!important;color:#fff!important;font-weight:700!important;border:none!important;border-radius:6px!important;}
button[kind="secondary"]{background:#1a1a1a!important;color:#777!important;font-weight:500!important;border:1px solid #252525!important;border-radius:6px!important;}
button[kind="secondary"]:hover{border-color:#2e7d52!important;color:#5aad7e!important;}
hr{border-color:#1e1e1e!important;}
.ig-header{background:#141414;border:1px solid #1e1e1e;border-radius:10px;padding:16px 22px;
  display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;border-left:3px solid #2e7d52;}
.ig-hl{display:flex;align-items:center;gap:12px;}
.ig-logo{width:36px;height:36px;background:#2e7d52;border-radius:8px;display:flex;
  align-items:center;justify-content:center;font-size:18px;font-weight:800;color:#fff;}
.ig-title{font-size:16px;font-weight:700;color:#e8e8e8;}
.ig-sub{font-size:10px;color:#5aad7e;letter-spacing:.08em;text-transform:uppercase;margin-top:2px;}
.ig-meta{font-size:12px;color:#777;text-align:right;line-height:1.8;}
.ig-meta b{color:#888;}
.sec-label{font-size:10px;font-weight:600;color:#5aad7e;letter-spacing:.08em;
  text-transform:uppercase;margin:16px 0 10px 0;display:flex;align-items:center;gap:8px;}
.sec-label::after{content:'';flex:1;height:1px;background:#1e1e1e;}
.card{background:#141414;border:1px solid #1e1e1e;border-radius:10px;padding:16px;position:relative;overflow:hidden;}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.card-alert::before{background:#c62828;}
.card-total::before{background:#2e7d52;}
.card-cancel::before{background:#555;}
.card-fam{font-size:11px;font-weight:600;color:#888;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;}
.card-num{font-size:34px;font-weight:800;line-height:1;margin-bottom:10px;}
.num-red{color:#ef5350;}.num-grn{color:#5aad7e;}.num-gray{color:#666;}
.card-row{display:flex;justify-content:space-between;font-size:12px;padding:4px 0;border-top:1px solid #1e1e1e;}
.c-lbl{color:#888;}.c-val{font-weight:500;color:#ccc;}.c-red{font-weight:600;color:#ef5350;}
.card-hl{display:flex;justify-content:space-between;font-size:12px;padding:5px 0;border-top:1px solid #252525;margin-top:3px;}
.hl-lbl{color:#888;font-size:12px;}.hl-val{font-weight:600;color:#5aad7e;}
.t5-card{background:#141414;border:1px solid #1e1e1e;border-radius:10px;padding:14px;border-left:3px solid #c62828;}
.t5-rank{font-size:10px;font-weight:600;color:#444;margin-bottom:3px;}
.t5-nome{font-size:14px;font-weight:700;color:#e0e0e0;margin-bottom:4px;}
.t5-fam{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600;margin-bottom:10px;}
.f-e{background:#1a2e1a;color:#5aad7e;border:1px solid #2e7d5230;}
.f-a{background:#2b2200;color:#ffa726;border:1px solid #ffa72630;}
.f-i{background:#00192b;color:#42a5f5;border:1px solid #42a5f530;}
.t5-row{display:flex;justify-content:space-between;font-size:11px;padding:4px 0;border-top:1px solid #1e1e1e;}
.t5-lbl{color:#888;}.t5-val{font-weight:600;color:#ef5350;}
.t5-med{font-weight:500;color:#42a5f5;}
.bar-bg{background:#1e1e1e;border-radius:3px;height:3px;margin-top:10px;}
.bar-fg{height:100%;border-radius:3px;background:#c62828;}
table.igt{width:100%;border-collapse:collapse;font-size:13px;}
table.igt thead tr{border-bottom:1px solid #252525;}
table.igt th{padding:10px 8px;font-size:11px;font-weight:600;color:#888;text-align:center;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;}
table.igt th:first-child{text-align:left;}
table.igt th.th-med{color:#42a5f5!important;}
table.igt td{padding:8px;border-bottom:1px solid #1e1e1e;text-align:center;color:#aaa;font-size:13px;white-space:nowrap;}
table.igt td:first-child{text-align:left;white-space:normal;}
table.igt tr.fr td{background:#161616;font-weight:600;color:#ccc;}
table.igt tr.fr:hover td{background:#1a1a1a;}
table.igt tr.dr td{background:#111;}
table.igt tr.dr td:first-child{padding-left:28px;color:#aaa;font-size:13px;}
table.igt tr.tr td{background:#162516;font-weight:700;font-size:13px;border-top:1px solid #2e7d5230;border-bottom:none;}
.ng{color:#5aad7e!important;font-weight:600!important;}
.nr{color:#ef5350!important;font-weight:600!important;}
.na{color:#ffa726!important;font-weight:600!important;}
.ns{color:#777!important;}
.nt{color:#5aad7e!important;font-weight:700!important;}
.vm{color:#42a5f5!important;font-size:11px!important;font-weight:500!important;}
.vs{font-size:11px;color:#666;display:block;}
.z{color:#333!important;}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600;margin-right:6px;}
.be{background:#1a2e1a;color:#5aad7e;border:1px solid #2e7d5225;}
.ba{background:#2b2200;color:#ffa726;border:1px solid #ffa72625;}
.bi{background:#00192b;color:#42a5f5;border:1px solid #42a5f525;}
.leg{display:flex;flex-wrap:wrap;gap:14px;font-size:11px;color:#555;margin:6px 0 10px 0;}
.li{display:flex;align-items:center;gap:5px;}
.ls{width:8px;height:8px;border-radius:2px;}
.med-note{font-size:11px;color:#42a5f5;background:#00192b30;border:1px solid #42a5f520;
  border-radius:5px;padding:5px 12px;display:inline-block;margin-bottom:12px;}
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
FAM_BADGE = {'Energizados':'be','AZA':'ba','iVolt':'bi'}
FAM_T5    = {'Energizados':'f-e','AZA':'f-a','iVolt':'f-i'}
SLA_DAYS  = 3

SETORES_VALIDOS = [
    'Inadimplência',
    'Suporte ao Cliente',
    'Meet Call',
    'Experiência do Cliente',
    'Ouvidoria',
]

def parse_valor(v):
    if pd.isna(v) or str(v).strip() in ['-','']: return 0.0
    v = str(v).replace('R$','').replace(' ','').replace('.','').replace(',','.')
    try: return float(v)
    except: return 0.0

def fmt_r(v):
    if v == 0: return '-'
    return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.',',').replace('X','.')

def pct(n,t): return f'{n/t*100:.1f}%' if t else '0%'

def listar_planilhas():
    pasta = 'dados'
    if not os.path.exists(pasta): return {}
    arquivos = sorted([f for f in os.listdir(pasta) if f.endswith('.xlsx')], reverse=True)
    datas = {}
    for arq in arquivos:
        m = re.search(r'(\d{1,2})([a-z]{3})(\d{4})', arq, re.IGNORECASE)
        if m:
            dia,mes_str,ano = m.group(1),m.group(2).lower(),m.group(3)
            meses = {'jan':'01','fev':'02','mar':'03','abr':'04','mai':'05','jun':'06',
                     'jul':'07','ago':'08','set':'09','out':'10','nov':'11','dez':'12'}
            label = f"{dia.zfill(2)}/{meses.get(mes_str,'00')}/{ano}"
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
        forn = sheet.replace('Tickets - ','')
        df['_Fornecedora'] = forn
        df['_Familia'] = FAMILIA_MAP.get(forn, 'Outros')
        dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)
    bko_cols = [c for c in data.columns if c.startswith('BKO') and 'Atribuido em' not in c and 'Atribuído em' not in c]
    def tem_bko(row):
        for col in bko_cols:
            if str(row[col]).strip() not in ['-','nan','','NaT']: return True
        return False
    data['_Atribuido']    = data.apply(tem_bko, axis=1)
    data['_Valor']        = data['Valor Total'].apply(parse_valor)
    data['_CriadoTS']     = pd.to_datetime(data['Criado Em'], errors='coerce')
    data['_FinalizadoTS'] = pd.to_datetime(data['Data Finalização'], errors='coerce')
    for col,dest in [('Média 1ª Resposta (Fornecedora)','_MediaResp'),
                     ('Média até Finalização (Fornecedora)','_MediaFin')]:
        if col in data.columns:
            data[dest] = data[col].apply(lambda x: str(x).strip() if str(x).strip() not in ['-','nan',''] else '-')
        else:
            data[dest] = '-'
    if 'Setor' in data.columns:
        data['_Setor'] = data['Setor'].apply(lambda x: str(x).strip() if pd.notna(x) else '')
    else:
        data['_Setor'] = ''
    return data

def get_medias(data, forn):
    fd = data[data['_Fornecedora']==forn]
    def fv(col):
        v = fd[col][fd[col]!='-']
        return v.iloc[0] if len(v)>0 else '-'
    return fv('_MediaResp'), fv('_MediaFin')

def calc_on_date(data, cutoff_date):
    cut   = pd.Timestamp(cutoff_date).replace(hour=23,minute=59,second=59)
    sla_s = SLA_DAYS*24*3600
    rows  = []
    for _,r in data[data['_CriadoTS']<=cut].iterrows():
        status = str(r.get('Status','')).strip()
        if status == 'Cancelado':
            rows.append({
                'Fornecedora':r['_Fornecedora'],'Familia':r['_Familia'],'Setor':r['_Setor'],
                'Atribuido':r['_Atribuido'],'Valor':r['_Valor'],
                'Atraso':False,'NoPrazo':False,'EncAtraso':False,'EncPrazo':False,'Cancelado':True,
            })
            continue
        c=r['_CriadoTS']; f=r['_FinalizadoTS']
        enc = status == 'Finalizado'
        if enc:
            if pd.isna(f) or f > cut:
                rows.append({
                    'Fornecedora':r['_Fornecedora'],'Familia':r['_Familia'],'Setor':r['_Setor'],
                    'Atribuido':r['_Atribuido'],'Valor':r['_Valor'],
                    'Atraso':False,'NoPrazo':False,'EncAtraso':False,'EncPrazo':True,'Cancelado':False,
                })
            else:
                secs = int((f-c).total_seconds())
                at   = secs >= sla_s
                rows.append({
                    'Fornecedora':r['_Fornecedora'],'Familia':r['_Familia'],'Setor':r['_Setor'],
                    'Atribuido':r['_Atribuido'],'Valor':r['_Valor'],
                    'Atraso':False,'NoPrazo':False,'EncAtraso':at,'EncPrazo':not at,'Cancelado':False,
                })
        else:
            secs = int((cut-c).total_seconds())
            at   = secs >= sla_s
            rows.append({
                'Fornecedora':r['_Fornecedora'],'Familia':r['_Familia'],'Setor':r['_Setor'],
                'Atribuido':r['_Atribuido'],'Valor':r['_Valor'],
                'Atraso':at,'NoPrazo':not at,'EncAtraso':False,'EncPrazo':False,'Cancelado':False,
            })
    return pd.DataFrame(rows)

def agg(df):
    df = df[~df['Cancelado']]
    def s(mask): return df[mask]['Valor'].sum() if mask.any() else 0
    ap=df['Atribuido']&df['NoPrazo']; aa=df['Atribuido']&df['Atraso']
    np_=~df['Atribuido']&df['NoPrazo']; na=~df['Atribuido']&df['Atraso']
    return{
        'total':len(df),'valor':df['Valor'].sum(),
        'atraso_n':int(df['Atraso'].sum()),'atraso_v':s(df['Atraso']),
        'atr_atrib':int((df['Atribuido']&df['Atraso']).sum()),
        'atr_natrib':int((~df['Atribuido']&df['Atraso']).sum()),
        'atr_prazo':int(ap.sum()),'atr_prazo_v':s(ap),
        'atr_atraso':int(aa.sum()),'atr_atraso_v':s(aa),
        'nat_prazo':int(np_.sum()),'nat_prazo_v':s(np_),
        'nat_atraso':int(na.sum()),'nat_atraso_v':s(na),
        'enc_prazo':int(df['EncPrazo'].sum()),'enc_prazo_v':s(df['EncPrazo']),
        'enc_atraso':int(df['EncAtraso'].sum()),'enc_atraso_v':s(df['EncAtraso']),
    }

def cel(n,v,cls):
    vs = '<span class="vs">' + fmt_r(v) + '</span>' if v>0 else ''
    inner = '<span class="z">—</span>' if n==0 else str(n)
    return '<td class="' + cls + '">' + inner + vs + '</td>'

def render_dashboard(tickets, data, titulo, subtitulo):
    m          = agg(tickets)
    total      = m['total']
    cancelados = int(tickets['Cancelado'].sum())

    st.markdown(
        '<div class="ig-header"><div class="ig-hl"><div class="ig-logo">G</div>'
        '<div><div class="ig-title">' + titulo + '</div>'
        '<div class="ig-sub">' + subtitulo + '</div></div></div>'
        '<div class="ig-meta">iGreen Energy &nbsp;·&nbsp; <b>SLA: ' + str(SLA_DAYS) + ' dias úteis</b></div></div>',
        unsafe_allow_html=True)

    # Cards por família
    fam_data = {}
    for fam in ['Energizados','AZA','iVolt']:
        ft  = tickets[tickets['Familia']==fam]
        fm  = agg(ft)
        byf = ft[ft['Atraso']].groupby('Fornecedora').size()
        maior   = byf.idxmax() if len(byf)>0 else '-'
        maior_n = int(byf.max()) if len(byf)>0 else 0
        fam_data[fam] = {'m':fm,'maior':maior,'maior_n':maior_n}

    st.markdown('<div class="sec-label">Não resolvidos em atraso — apenas abertos</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, fam in enumerate(['Energizados','AZA','iVolt']):
        fd = fam_data[fam]; fm = fd['m']
        sub_lbl = 'Fornecedora' if fam=='Energizados' else 'Maior atraso'
        sub_val = 'COMERC' if fam=='Energizados' else fd['maior'] + ' (' + str(fd['maior_n']) + ')'
        with cols[i]:
            st.markdown(
                '<div class="card card-alert">'
                '<div class="card-fam">' + fam + '</div>'
                '<div class="card-num num-red">' + str(fm['atraso_n']) + '</div>'
                '<div class="card-row"><span class="c-lbl">Atribuído (BKO)</span><span class="c-red">' + str(fm['atr_atrib']) + '</span></div>'
                '<div class="card-row"><span class="c-lbl">Não atribuído</span><span class="c-val">' + str(fm['atr_natrib']) + '</span></div>'
                '<div class="card-row"><span class="c-lbl">' + sub_lbl + '</span><span class="c-val">' + sub_val + '</span></div>'
                '<div class="card-row"><span class="c-lbl">Valor em atraso</span><span class="c-val">' + fmt_r(fm['atraso_v']) + '</span></div>'
                '<div class="card-hl"><span class="hl-lbl">Valor total família</span><span class="hl-val">' + fmt_r(fm['valor']) + '</span></div>'
                '</div>', unsafe_allow_html=True)

    with cols[3]:
        st.markdown(
            '<div class="card card-total">'
            '<div class="card-fam">Total geral</div>'
            '<div class="card-num num-grn">' + str(m['atraso_n']) + '</div>'
            '<div class="card-row"><span class="c-lbl">Atribuído (BKO)</span><span class="c-red">' + str(m['atr_atrib']) + '</span></div>'
            '<div class="card-row"><span class="c-lbl">Não atribuído</span><span class="c-val">' + str(m['atr_natrib']) + '</span></div>'
            '<div class="card-row"><span class="c-lbl">% do total</span><span class="c-val">' + pct(m['atraso_n'],total) + '</span></div>'
            '<div class="card-row"><span class="c-lbl">Valor em atraso</span><span class="c-val">' + fmt_r(m['atraso_v']) + '</span></div>'
            '<div class="card-hl"><span class="hl-lbl">Valor total geral</span><span class="hl-val">' + fmt_r(m['valor']) + '</span></div>'
            '</div>', unsafe_allow_html=True)

    with cols[4]:
        st.markdown(
            '<div class="card card-cancel">'
            '<div class="card-fam">Cancelados</div>'
            '<div class="card-num num-gray">' + str(cancelados) + '</div>'
            '<div class="card-row"><span class="c-lbl">Fora de todos os cálculos</span></div>'
            '<div class="card-row"><span class="c-lbl">Não impactam SLA</span></div>'
            '</div>', unsafe_allow_html=True)

    st.divider()

    # Top 5
    st.markdown('<div class="sec-label">Top 5 fornecedoras em atraso</div>', unsafe_allow_html=True)
    top5 = (tickets[tickets['Atraso']]
            .groupby(['Fornecedora','Familia'])
            .agg(n=('Atraso','count'), v=('Valor','sum'))
            .reset_index().sort_values('n',ascending=False).head(5))

    max_n  = int(top5['n'].max()) if len(top5)>0 else 1
    ords   = ['1o','2o','3o','4o','5o']
    t5cols = st.columns(5)
    for i, row in enumerate(top5.itertuples()):
        badge = FAM_T5.get(row.Familia,'f-e')
        mr, mf = get_medias(data, row.Fornecedora)
        pct_bar = int(row.n / max_n * 100)
        with t5cols[i]:
            st.markdown(
                '<div class="t5-card">'
                '<div class="t5-rank">' + ords[i] + ' lugar</div>'
                '<div class="t5-nome">' + row.Fornecedora + '</div>'
                '<span class="t5-fam ' + badge + '">' + row.Familia + '</span>'
                '<div class="t5-row"><span class="t5-lbl">Em atraso</span><span class="t5-val">' + str(row.n) + '</span></div>'
                '<div class="t5-row"><span class="t5-lbl">Valor</span><span class="t5-val">' + fmt_r(row.v) + '</span></div>'
                '<div class="t5-row"><span class="t5-lbl">Media 1a resp. (forn.)</span><span class="t5-med">' + mr + '</span></div>'
                '<div class="t5-row"><span class="t5-lbl">Media finaliz. (forn.)</span><span class="t5-med">' + mf + '</span></div>'
                '<div class="bar-bg"><div class="bar-fg" style="width:' + str(pct_bar) + '%"></div></div>'
                '</div>', unsafe_allow_html=True)

    st.divider()

    # Tabela completa
    st.markdown('<div class="sec-label">Visao completa — ' + str(total) + ' tickets · clique na familia para expandir</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="leg">'
        '<span class="li"><span class="ls" style="background:#5aad7e"></span>Atribuido no prazo</span>'
        '<span class="li"><span class="ls" style="background:#ef5350"></span>Atribuido em atraso</span>'
        '<span class="li"><span class="ls" style="background:#ffa726"></span>Nao atribuido no prazo</span>'
        '<span class="li"><span class="ls" style="background:#ef5350"></span>Nao atribuido em atraso</span>'
        '<span class="li"><span class="ls" style="background:#2e7d5260"></span>Encerrado no prazo</span>'
        '<span class="li"><span class="ls" style="background:#333"></span>Encerrado em atraso</span>'
        '</div>'
        '<div class="med-note">Colunas em azul = medias calculadas pela fornecedora</div>',
        unsafe_allow_html=True)

    exp_key = 'expanded_' + subtitulo.replace(' ','_')
    if exp_key not in st.session_state:
        st.session_state[exp_key] = set()

    exp_cols = st.columns(3)
    for i, fam in enumerate(['Energizados','AZA','iVolt']):
        with exp_cols[i]:
            is_open = fam in st.session_state[exp_key]
            lbl = ('Recolher ' if is_open else 'Expandir ') + fam
            if st.button(lbl, key='exp_'+fam+'_'+subtitulo.replace(' ','_'),
                         type='primary' if is_open else 'secondary',
                         use_container_width=True):
                if is_open: st.session_state[exp_key].discard(fam)
                else:       st.session_state[exp_key].add(fam)
                st.rerun()

    keys_n = ['atr_prazo','atr_atraso','nat_prazo','nat_atraso','enc_prazo','enc_atraso']
    keys_v = ['atr_prazo_v','atr_atraso_v','nat_prazo_v','nat_atraso_v','enc_prazo_v','enc_atraso_v']
    clss   = ['ng','nr','na','nr','ng','ns']

    tbl = (
        '<table class="igt"><thead><tr>'
        '<th style="text-align:left">Familia / Fornecedora</th>'
        '<th>Atrib.<br>Prazo</th><th>Atrib.<br>Atraso</th>'
        '<th>N.Atrib.<br>Prazo</th><th>N.Atrib.<br>Atraso</th>'
        '<th>Enc.<br>Prazo</th><th>Enc.<br>Atraso</th>'
        '<th>Total</th>'
        '<th class="th-med">Media 1a Resp.<br>(Fornecedora)</th>'
        '<th class="th-med">Media Finaliz.<br>(Fornecedora)</th>'
        '</tr></thead><tbody>'
    )

    t6n = [0]*6; t6v = [0]*6
    for fam in ['Energizados','AZA','iVolt']:
        ft  = tickets[tickets['Familia']==fam]
        fm  = agg(ft)
        ns  = [fm[k] for k in keys_n]
        vs  = [fm[k] for k in keys_v]
        for i in range(6): t6n[i]+=ns[i]; t6v[i]+=vs[i]
        badge = FAM_BADGE[fam]
        cells = ''.join(cel(ns[i],vs[i],clss[i]) for i in range(6))
        vt = '<span class="vs">' + fmt_r(fm['valor']) + '</span>' if fm['valor']>0 else ''
        tbl += '<tr class="fr"><td><span class="badge ' + badge + '">' + fam + '</span></td>' + cells + '<td class="nt">' + str(fm['total']) + vt + '</td><td>—</td><td>—</td></tr>'

        if fam in st.session_state[exp_key]:
            forns_fam = FORN_BY_FAM.get(fam,[])
            # inclui fornecedoras novas que não estão no mapa fixo
            forns_extra = [f for f in tickets[tickets['Familia']==fam]['Fornecedora'].unique() if f not in forns_fam]
            for forn in forns_fam + forns_extra:
                fd2 = tickets[tickets['Fornecedora']==forn]
                if not len(fd2): continue
                fm2  = agg(fd2)
                ns2  = [fm2[k] for k in keys_n]
                vs2  = [fm2[k] for k in keys_v]
                c2   = ''.join(cel(ns2[i],vs2[i],clss[i]) for i in range(6))
                vt2  = '<span class="vs">' + fmt_r(fm2['valor']) + '</span>' if fm2['valor']>0 else ''
                mr, mf = get_medias(data, forn)
                mr_h = '<span class="vm">' + mr + '</span>' if mr!='-' else '<span class="z">—</span>'
                mf_h = '<span class="vm">' + mf + '</span>' if mf!='-' else '<span class="z">—</span>'
                tbl += '<tr class="dr"><td>' + forn + '</td>' + c2 + '<td>' + str(fm2['total']) + vt2 + '</td><td>' + mr_h + '</td><td>' + mf_h + '</td></tr>'

    tc = ''.join(cel(t6n[i],t6v[i],clss[i]) for i in range(6))
    vt_tot = '<span class="vs">' + fmt_r(m['valor']) + '</span>' if m['valor']>0 else ''
    tbl += '<tr class="tr"><td>TOTAL GERAL</td>' + tc + '<td class="nt">' + str(total) + vt_tot + '</td><td>—</td><td>—</td></tr>'
    tbl += '</tbody></table>'
    st.markdown(tbl, unsafe_allow_html=True)

    st.divider()

    # Detalhe tickets em atraso
    st.markdown('<div class="sec-label">Detalhe dos tickets em atraso — clique para ver</div>', unsafe_allow_html=True)

    det_key = 'detail_forn_' + subtitulo.replace(' ','_')
    if det_key not in st.session_state:
        st.session_state[det_key] = None

    for fam in ['Energizados','AZA','iVolt']:
        forns_fam = FORN_BY_FAM.get(fam,[])
        forns_extra = [f for f in tickets[tickets['Familia']==fam]['Fornecedora'].unique() if f not in forns_fam]
        todas = forns_fam + forns_extra
        forns_com_atraso = [f for f in todas if len(tickets[(tickets['Fornecedora']==f) & tickets['Atraso']]) > 0]
        if not forns_com_atraso: continue
        badge_cls = FAM_BADGE.get(fam,'be')
        st.markdown('<span class="badge ' + badge_cls + '" style="font-size:11px;padding:3px 10px">' + fam + '</span>', unsafe_allow_html=True)
        btn_row = st.columns(min(len(forns_com_atraso), 6))
        for i, forn in enumerate(forns_com_atraso):
            n_atraso = len(tickets[(tickets['Fornecedora']==forn) & tickets['Atraso']])
            with btn_row[i]:
                ativo = st.session_state[det_key] == forn
                if st.button(forn + ' (' + str(n_atraso) + ')', key='det_'+forn+'_'+subtitulo.replace(' ','_'),
                             type='primary' if ativo else 'secondary',
                             use_container_width=True):
                    st.session_state[det_key] = None if ativo else forn
                    st.rerun()

    if st.session_state[det_key]:
        forn_sel = st.session_state[det_key]
        bko_cols = [c for c in data.columns if c.startswith('BKO') and 'Atribuido em' not in c and 'Atribuído em' not in c]

        def get_bko(row):
            vals = []
            for col in bko_cols:
                v = str(row[col]).strip()
                if v not in ['-','nan','']: vals.append(v)
            return ', '.join(vals) if vals else '-'

        cut   = pd.Timestamp(data['_CriadoTS'].max().date()).replace(hour=23,minute=59,second=59)
        sla_s = SLA_DAYS*24*3600

        base_forn = data[data['_Fornecedora']==forn_sel]
        # filtra setor se não for consolidado
        if subtitulo != 'Consolidado — todos os setores':
            base_forn = base_forn[base_forn['_Setor']==subtitulo]

        detail_rows = []
        for _, r in base_forn.iterrows():
            status = str(r.get('Status','')).strip()
            if status in ('Cancelado','Finalizado'): continue
            c = r['_CriadoTS']
            if pd.isna(c): continue
            secs = int((cut-c).total_seconds())
            if secs < sla_s: continue
            dias_atraso = secs // 86400
            horas_rest  = (secs % 86400) // 3600
            detail_rows.append({
                'Código':          str(r['Código']),
                'Tipo':            str(r['Tipo']),
                'Status':          str(r['Status']),
                'Atribuição':      get_bko(r),
                'Criado em':       r['_CriadoTS'].strftime('%d/%m/%Y') if pd.notna(r['_CriadoTS']) else '-',
                'Tempo em atraso': str(dias_atraso) + 'd ' + str(horas_rest) + 'h em atraso',
                'Dias úteis':      str(r.get('Tempo em Aberto (Dias Úteis)','-')),
                'Valor':           str(r['Valor Total']) if str(r['Valor Total']) not in ['-','nan'] else '-',
            })

        df_detail = pd.DataFrame(detail_rows)

        st.markdown(
            '<div style="background:#141414;border:1px solid #1e1e1e;border-radius:10px;padding:16px;margin-top:12px;">'
            '<div style="margin-bottom:12px;">'
            '<span style="font-size:15px;font-weight:700;color:#e0e0e0">' + forn_sel + '</span>'
            '<span style="font-size:12px;color:#ef5350;margin-left:10px;font-weight:600">' + str(len(df_detail)) + ' tickets em atraso</span>'
            '</div>', unsafe_allow_html=True)

        if len(df_detail) > 0:
            det_tbl = (
                '<table class="igt"><thead><tr>'
                '<th style="text-align:left">Código</th>'
                '<th style="text-align:left">Tipo</th>'
                '<th>Status</th><th>Atribuição</th>'
                '<th>Criado em</th><th>Tempo em atraso</th>'
                '<th>Dias úteis</th><th>Valor</th>'
                '</tr></thead><tbody>'
            )
            for _, row in df_detail.iterrows():
                atrib_color = '#5aad7e' if row['Atribuição'] != '-' else '#ef5350'
                det_tbl += (
                    '<tr class="dr" style="display:table-row">'
                    '<td style="text-align:left;color:#42a5f5;font-weight:600">' + row['Código'] + '</td>'
                    '<td style="text-align:left;color:#ccc">' + row['Tipo'] + '</td>'
                    '<td style="color:#aaa">' + row['Status'] + '</td>'
                    '<td style="color:' + atrib_color + ';font-weight:500">' + row['Atribuição'] + '</td>'
                    '<td style="color:#888">' + row['Criado em'] + '</td>'
                    '<td style="color:#ef5350;font-weight:600">' + row['Tempo em atraso'] + '</td>'
                    '<td style="color:#888">' + row['Dias úteis'] + '</td>'
                    '<td style="color:#5aad7e;font-weight:500">' + row['Valor'] + '</td>'
                    '</tr>'
                )
            det_tbl += '</tbody></table>'
            st.markdown(det_tbl, unsafe_allow_html=True)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_detail.to_excel(writer, index=False, sheet_name='Tickets em Atraso')
            output.seek(0)
            st.download_button(
                label='Baixar Excel — ' + forn_sel,
                data=output,
                file_name='Atraso_' + forn_sel.replace(' ','_') + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                key='dl_'+forn_sel+'_'+subtitulo.replace(' ','_')
            )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br><div style="text-align:right;font-size:10px;color:#2a2a2a">iGreen Energy · ' + subtitulo + '</div>', unsafe_allow_html=True)


# ── SIDEBAR
with st.sidebar:
    st.markdown('### iGreen Energy')
    st.markdown('SLA de Tickets')
    st.divider()

    if 'pagina' not in st.session_state:
        st.session_state.pagina = 'consolidado'

    planilhas_sb = listar_planilhas()
    datas_sb = list(planilhas_sb.keys()) if planilhas_sb else []
    if 'data_sel' not in st.session_state and datas_sb:
        st.session_state.data_sel = datas_sb[0]

    st.markdown('<p style="font-size:11px;font-weight:600;color:#5aad7e;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px">Base de dados</p>', unsafe_allow_html=True)
    for label in datas_sb:
        ativo = st.session_state.get('data_sel') == label
        if st.button(label, key='sb_btn_'+label,
                     type='primary' if ativo else 'secondary',
                     use_container_width=True):
            st.session_state.data_sel = label
            st.rerun()

    st.divider()
    st.markdown('<p style="font-size:11px;font-weight:600;color:#5aad7e;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px">Visão geral</p>', unsafe_allow_html=True)
    if st.button('Consolidado', key='btn_consolidado',
                 type='primary' if st.session_state.pagina=='consolidado' else 'secondary',
                 use_container_width=True):
        st.session_state.pagina = 'consolidado'
        st.rerun()

    st.divider()
    st.markdown('<p style="font-size:11px;font-weight:600;color:#5aad7e;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px">Setores</p>', unsafe_allow_html=True)
    for setor in SETORES_VALIDOS:
        if st.button(setor, key='btn_setor_'+setor,
                     type='primary' if st.session_state.pagina==setor else 'secondary',
                     use_container_width=True):
            st.session_state.pagina = setor
            st.rerun()

    st.divider()
    st.markdown('<p style="font-size:11px;font-weight:600;color:#5aad7e;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px">Análise</p>', unsafe_allow_html=True)
    if st.button('Evolução por período', key='btn_evolucao',
                 type='primary' if st.session_state.pagina=='evolucao' else 'secondary',
                 use_container_width=True):
        st.session_state.pagina = 'evolucao'
        st.rerun()

    st.divider()
    st.markdown('**Atualizar:**\nSuba em `dados/` no GitHub:\n`Tickets_DDmesAAAA.xlsx`')
    st.divider()
    st.caption('SLA: 3 dias úteis · 13 fornecedoras')


# ── ROTEAMENTO
planilhas = listar_planilhas()

if st.session_state.get('pagina') == 'evolucao':
    st.markdown(
        '<div class="ig-header"><div class="ig-hl"><div class="ig-logo">G</div>'
        '<div><div class="ig-title">Evolução por Período</div>'
        '<div class="ig-sub">Análise histórica de atrasos</div></div></div>'
        '<div class="ig-meta">iGreen Energy &nbsp;·&nbsp; <b>SLA: 3 dias úteis</b></div></div>',
        unsafe_allow_html=True)

    if len(planilhas) < 2:
        st.info('Adicione mais de uma planilha na pasta dados/ para ver a evolução.')
    else:
        @st.cache_data
        def calc_evolucao(keys_tuple):
            resultados = []
            for label in keys_tuple:
                filepath = planilhas[label]
                try:
                    xl = pd.ExcelFile(filepath)
                    sheets = [s for s in xl.sheet_names if s != 'Resumo por Tipo']
                    dfs = []
                    for sheet in sheets:
                        df = pd.read_excel(filepath, sheet_name=sheet)
                        forn = sheet.replace('Tickets - ','')
                        df['_Fornecedora'] = forn
                        df['_Familia'] = FAMILIA_MAP.get(forn,'Outros')
                        dfs.append(df)
                    d = pd.concat(dfs, ignore_index=True)
                    if 'Setor' in d.columns:
                        d['_Setor'] = d['Setor'].apply(lambda x: str(x).strip() if pd.notna(x) else '')
                    else:
                        d['_Setor'] = ''
                    # Filtra apenas setores válidos
                    d = d[d['_Setor'].isin(SETORES_VALIDOS)]
                    d['_Valor'] = d['Valor Total'].apply(parse_valor)
                    d['_CriadoTS'] = pd.to_datetime(d['Criado Em'], errors='coerce')
                    d['_FinalizadoTS'] = pd.to_datetime(d['Data Finalização'], errors='coerce')
                    cut = d['_CriadoTS'].max()
                    sla_s = SLA_DAYS * 24 * 3600
                    total_at = 0; valor_at = 0.0
                    en_at = 0; az_at = 0; iv_at = 0
                    for _, r in d[d['_CriadoTS']<=cut].iterrows():
                        status = str(r.get('Status','')).strip()
                        if status in ('Cancelado','Finalizado'): continue
                        c=r['_CriadoTS']
                        secs = int((cut-c).total_seconds())
                        if secs>=sla_s:
                            total_at += 1
                            valor_at += float(r.get('_Valor',0))
                            fam = r['_Familia']
                            if fam=='Energizados': en_at+=1
                            elif fam=='AZA': az_at+=1
                            elif fam=='iVolt': iv_at+=1
                    resultados.append({
                        'Data':label,'Em Atraso':total_at,'Valor em Atraso':valor_at,
                        'Energizados':en_at,'AZA':az_at,'iVolt':iv_at
                    })
                except:
                    pass
            return pd.DataFrame(resultados)

        df_evo = calc_evolucao(tuple(sorted(planilhas.keys())))

        if len(df_evo) >= 2:
            var = int(df_evo['Em Atraso'].iloc[-1]) - int(df_evo['Em Atraso'].iloc[-2])
            sinal = '+' if var > 0 else ''
            cor = '#ef5350' if var > 0 else '#5aad7e'

            c1,c2,c3,c4 = st.columns(4)
            with c1:
                st.markdown('<div class="card card-total"><div class="card-fam">Variação período</div><div class="card-num" style="color:'+cor+'">'+sinal+str(var)+'</div><div class="card-row"><span class="c-lbl">'+df_evo["Data"].iloc[-2]+' → '+df_evo["Data"].iloc[-1]+'</span></div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="card card-alert"><div class="card-fam">Total atual</div><div class="card-num num-red">'+str(df_evo["Em Atraso"].iloc[-1])+'</div><div class="card-row"><span class="c-lbl">tickets em atraso</span></div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown('<div class="card card-alert"><div class="card-fam">Período anterior</div><div class="card-num num-red">'+str(df_evo["Em Atraso"].iloc[-2])+'</div><div class="card-row"><span class="c-lbl">tickets em atraso</span></div></div>', unsafe_allow_html=True)
            with c4:
                st.markdown('<div class="card card-alert"><div class="card-fam">Valor em atraso atual</div><div class="card-num num-red" style="font-size:22px">'+fmt_r(df_evo["Valor em Atraso"].iloc[-1])+'</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="sec-label" style="margin-top:20px">Evolução total de tickets em atraso</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_evo['Data'],y=df_evo['Em Atraso'],mode='lines+markers+text',name='Total em atraso',line={'color':'#ef5350','width':2},marker={'size':10,'color':'#ef5350'},text=[str(v) for v in df_evo['Em Atraso']],textposition='top center',textfont={'color':'#ef5350','size':13}))
            fig.update_layout(paper_bgcolor='#0f0f0f',plot_bgcolor='#141414',height=280,margin={'l':20,'r':20,'t':10,'b':20},xaxis={'gridcolor':'#1e1e1e','tickfont':{'color':'#888','size':12}},yaxis={'gridcolor':'#1a1a1a','tickfont':{'color':'#aaa','size':11}})
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="sec-label">Evolução por família</div>', unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df_evo['Data'],y=df_evo['Energizados'],mode='lines+markers',name='Energizados',line={'color':'#5aad7e','width':2},marker={'size':8}))
            fig2.add_trace(go.Scatter(x=df_evo['Data'],y=df_evo['AZA'],mode='lines+markers',name='AZA',line={'color':'#ffa726','width':2},marker={'size':8}))
            fig2.add_trace(go.Scatter(x=df_evo['Data'],y=df_evo['iVolt'],mode='lines+markers',name='iVolt',line={'color':'#42a5f5','width':2},marker={'size':8}))
            fig2.update_layout(paper_bgcolor='#0f0f0f',plot_bgcolor='#141414',height=260,margin={'l':20,'r':20,'t':10,'b':20},legend={'orientation':'h','x':0,'y':1.2,'font':{'color':'#888','size':11},'bgcolor':'rgba(0,0,0,0)'},xaxis={'gridcolor':'#1e1e1e','tickfont':{'color':'#888','size':12}},yaxis={'gridcolor':'#1a1a1a','tickfont':{'color':'#aaa','size':11}})
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown('<div class="sec-label">Histórico completo</div>', unsafe_allow_html=True)
            tbl_evo = '<table class="igt"><thead><tr><th style="text-align:left">Data base</th><th>Total em atraso</th><th>Energizados</th><th>AZA</th><th>iVolt</th><th>Valor em atraso</th></tr></thead><tbody>'
            for _, row in df_evo.iterrows():
                tbl_evo += '<tr class="dr" style="display:table-row"><td style="text-align:left;color:#ccc;font-weight:600">'+str(row['Data'])+'</td><td class="nr">'+str(int(row['Em Atraso']))+'</td><td class="ng">'+str(int(row['Energizados']))+'</td><td class="na">'+str(int(row['AZA']))+'</td><td style="color:#42a5f5;font-weight:600">'+str(int(row['iVolt']))+'</td><td class="ng">'+fmt_r(row['Valor em Atraso'])+'</td></tr>'
            tbl_evo += '</tbody></table>'
            st.markdown(tbl_evo, unsafe_allow_html=True)

else:
    if not planilhas:
        st.error('Nenhuma planilha em dados/.')
        st.stop()

    datas = list(planilhas.keys())
    if 'data_sel' not in st.session_state:
        st.session_state.data_sel = datas[0]

    with st.spinner('Carregando...'):
        data         = load_data(planilhas[st.session_state.data_sel])
        cutoff       = data['_CriadoTS'].max().date()
        tickets_todos = calc_on_date(data, cutoff)
        # Filtra apenas os 5 setores válidos para TODOS os cálculos
        tickets_base  = tickets_todos[tickets_todos['Setor'].isin(SETORES_VALIDOS)]

    pagina = st.session_state.get('pagina', 'consolidado')

    if pagina == 'consolidado':
        render_dashboard(
            tickets_base, data,
            titulo='Dashboard de Tickets — Consolidado',
            subtitulo='Consolidado — todos os setores'
        )
    elif pagina in SETORES_VALIDOS:
        tickets_setor = tickets_base[tickets_base['Setor'] == pagina]
        render_dashboard(
            tickets_setor, data,
            titulo='Dashboard de Tickets — ' + pagina,
            subtitulo=pagina
        )
