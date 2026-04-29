import csv, json

daily = []
with open(r'C:\Users\daviaraujo\resellers-grid\daily_tpv.csv') as f:
    for row in csv.DictReader(f):
        daily.append({
            'nivel': row['nivel'], 'data': row['data'],
            'tpv_m0': int(float(row['tpv_m0'] or 0)),
            'tpv_m1': int(float(row['tpv_m1'] or 0)),
            'tpv_total': int(float(row['tpv_total'] or 0))
        })

daily_json = json.dumps(daily)

html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Renda na Mao - Resellers 2026</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',sans-serif;background:#f4f4f4;color:#1a1a2e}
.header{background:#FFE600;padding:24px 40px 44px}
.header-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px}
.mp-logo{height:34px}
.programa-badge{display:inline-flex;align-items:center;background:#1A1F6B;color:#fff;border-radius:20px;padding:6px 18px;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.programa-badge span{color:#FFE600;margin-left:4px}
.header-body{display:flex;align-items:flex-end;gap:24px}
.renda-badge{background:#1A1F6B;border-radius:50% 50% 50% 0;padding:18px 26px;color:#fff;line-height:1.1;flex-shrink:0}
.renda-linha{display:flex;align-items:baseline;gap:5px}
.word-big{font-size:34px;font-weight:900;letter-spacing:-1px}
.word-na{font-size:13px;font-weight:700;color:#FFE600}
.header-sub{padding-bottom:4px}
.header-sub h2{font-size:12px;font-weight:800;color:#1A1F6B;text-transform:uppercase;letter-spacing:.07em;background:rgba(255,255,255,.65);display:inline-block;padding:5px 14px;border-radius:20px;margin-bottom:6px}
.header-sub p{font-size:12px;color:#1A1F6B;opacity:.65}
.tabs{display:flex;background:#1A1F6B;padding:0 32px}
.tab{padding:12px 22px;font-size:12px;font-weight:700;color:#aac;text-transform:uppercase;letter-spacing:.06em;cursor:pointer;border-bottom:3px solid transparent;transition:all .15s}
.tab:hover{color:#FFE600}
.tab.active{color:#FFE600;border-bottom-color:#FFE600}
.body{padding:28px 32px 40px}
.pane{display:none}
.pane.active{display:block}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:12px;margin-bottom:22px}
.card{background:#fff;border-radius:12px;padding:14px 18px;border-left:4px solid #1A1F6B;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.card-label{font-size:10px;color:#999;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}
.card-value{font-size:20px;font-weight:800;color:#1A1F6B}
.card-sub{font-size:10px;color:#bbb;margin-top:2px}
.controls{display:flex;gap:7px;margin-bottom:14px;flex-wrap:wrap;align-items:center}
.filter-btn{padding:5px 14px;border-radius:20px;border:1.5px solid #ddd;background:#fff;color:#666;font-size:12px;font-weight:600;cursor:pointer;transition:all .15s}
.filter-btn:hover{border-color:#1A1F6B;color:#1A1F6B}
.filter-btn.active{background:#1A1F6B;border-color:#1A1F6B;color:#FFE600}
.search-box{padding:5px 14px;border-radius:20px;border:1.5px solid #ddd;background:#fff;color:#333;font-size:12px;outline:none;width:160px;margin-left:auto}
.search-box:focus{border-color:#1A1F6B}
.grid-wrapper{border-radius:12px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.08)}
table{width:100%;border-collapse:collapse;font-size:13px}
thead th{background:#1A1F6B;padding:12px 16px;text-align:left;font-weight:700;color:#FFE600;font-size:11px;text-transform:uppercase;letter-spacing:.06em;cursor:pointer;user-select:none;white-space:nowrap}
thead th:hover{background:#22287a}
thead th.sorted-asc::after{content:' ↑';color:#fff}
thead th.sorted-desc::after{content:' ↓';color:#fff}
thead th:not(:first-child):not(:nth-child(2)){text-align:right}
tbody tr{border-bottom:1px solid #f0f0f0;background:#fff;transition:background .1s}
tbody tr:hover{background:#fffde6}
tbody tr.group-total{background:#f5f5ff}
tbody tr.group-total td{font-weight:700;color:#1A1F6B}
td{padding:10px 16px;color:#333}
td:not(:first-child):not(:nth-child(2)){text-align:right;font-variant-numeric:tabular-nums}
.mes-badge{display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;background:#FFE600;color:#1A1F6B}
.nivel-badge{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600}
.nivel-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.nivel-aprendiz .nivel-dot{background:#9ca3af}
.nivel-especialista .nivel-dot{background:#3b82f6}
.nivel-empreendedor .nivel-dot{background:#f59e0b}
.nivel-top .nivel-dot{background:#1A1F6B}
.tpv-value{color:#1A1F6B;font-weight:600}
.tpv-zero{color:#ccc}
.pct{font-size:10px;color:#aaa;font-weight:500;margin-left:4px}
.pct-high{color:#1A1F6B;font-weight:700}
.bar-cell{display:flex;align-items:center;gap:7px;justify-content:flex-end}
.bar-bg{width:50px;height:4px;background:#eee;border-radius:2px;overflow:hidden}
.bar-fill{height:100%;border-radius:2px;background:#FFE600}
.chart-wrap{background:#fff;border-radius:12px;padding:22px;box-shadow:0 2px 12px rgba(0,0,0,.07);margin-bottom:20px}
.chart-title{font-size:13px;font-weight:700;color:#1A1F6B;margin-bottom:4px}
.chart-sub{font-size:11px;color:#aaa;margin-bottom:14px}
.chart-controls{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}
canvas{max-height:320px}
.footer{text-align:center;padding:20px;font-size:11px;color:#bbb}
</style>
</head>
<body>

<div class="header">
  <div class="header-top">
    <svg class="mp-logo" viewBox="0 0 190 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="20" fill="#009EE3"/>
      <text x="20" y="26" text-anchor="middle" font-family="Segoe UI,sans-serif" font-weight="900" font-size="15" fill="#fff">mp</text>
      <text x="50" y="16" font-family="Segoe UI,sans-serif" font-weight="700" font-size="13" fill="#1A1F6B">mercado</text>
      <text x="50" y="32" font-family="Segoe UI,sans-serif" font-weight="400" font-size="13" fill="#1A1F6B">pago</text>
    </svg>
    <div class="programa-badge">Programa de<span>Revenda</span></div>
  </div>
  <div class="header-body">
    <div class="renda-badge">
      <div class="renda-linha"><span class="word-big">RENDA</span></div>
      <div class="renda-linha"><span class="word-na">na</span><span class="word-big">MAO</span></div>
    </div>
    <div class="header-sub">
      <h2>Resultado por Nivel &middot; 2026</h2>
      <p>Jan - Abr/26 &middot; null = Aprendiz</p>
    </div>
  </div>
</div>

<div class="tabs">
  <div class="tab active" onclick="showTab('tabela',this)">&#128202; Tabela</div>
  <div class="tab" onclick="showTab('modelos',this)">&#128424; Modelos</div>
  <div class="tab" onclick="showTab('chart-tpv',this)">&#128200; TPV Diario</div>
  <div class="tab" onclick="showTab('chart-devices',this)">&#128230; Devices / Mes</div>
</div>

<div class="body">

<div class="pane active" id="pane-tabela">
  <div class="cards" id="cards-tabela"></div>
  <div class="controls">
    <div id="mes-filters" style="display:flex;gap:6px;flex-wrap:wrap"></div>
    <div id="nivel-filters" style="display:flex;gap:6px;flex-wrap:wrap"></div>
    <input class="search-box" type="text" placeholder="Buscar..." id="search-input"/>
  </div>
  <div class="grid-wrapper">
    <table>
      <thead><tr>
        <th data-col="mes">Mes</th>
        <th data-col="nivel">Nivel</th>
        <th data-col="resellers">Resellers</th>
        <th data-col="pedidos">Dev. Pedidos</th>
        <th data-col="ativos">Dev. Ativos</th>
        <th data-col="tpv_m0">TPV M0</th>
        <th data-col="tpv_m1">TPV M1</th>
        <th data-col="tpv_total">TPV Total</th>
      </tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
</div>

<div class="pane" id="pane-modelos">
  <div class="cards" id="cards-modelos"></div>
  <div class="controls">
    <div id="mes-filters-mod" style="display:flex;gap:6px;flex-wrap:wrap"></div>
  </div>
  <div class="grid-wrapper">
    <table>
      <thead><tr>
        <th>Mes</th><th>Nivel</th>
        <th style="text-align:right">Pro Pedidos</th>
        <th style="text-align:right">Pro Ativos</th>
        <th style="text-align:right">Smart Pedidos</th>
        <th style="text-align:right">Smart Ativos</th>
        <th style="text-align:right">% Pro</th>
        <th style="text-align:right">% Smart</th>
      </tr></thead>
      <tbody id="tbody-modelos"></tbody>
    </table>
  </div>
</div>

<div class="pane" id="pane-chart-tpv">

  <!-- Grafico 1: Mensal overview -->
  <div class="chart-wrap">
    <div class="chart-title">TPV Total do Canal por Mes</div>
    <div class="chart-sub">Visao geral Jan-Abr/26 - M0 + M1 + Total portfolio empilhado por nivel</div>
    <div class="chart-controls" id="nivel-filter-tpv-bar"></div>
    <canvas id="chartTpvBar"></canvas>
  </div>

  <!-- Filtros compartilhados para os graficos diarios -->
  <div style="background:#fff;border-radius:12px;padding:16px 20px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.06)">
    <div style="font-size:11px;font-weight:700;color:#1A1F6B;text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px">Filtros para graficos diarios</div>
    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div>
        <div style="font-size:10px;color:#999;margin-bottom:6px">MES</div>
        <div id="mes-filter-tpv-daily" style="display:flex;gap:6px;flex-wrap:wrap"></div>
      </div>
      <div>
        <div style="font-size:10px;color:#999;margin-bottom:6px">NIVEL</div>
        <div id="nivel-filter-tpv-daily" style="display:flex;gap:6px;flex-wrap:wrap"></div>
      </div>
    </div>
  </div>

  <!-- Grafico 2: TPV M0 diario -->
  <div class="chart-wrap">
    <div class="chart-title">TPV M0 por Dia</div>
    <div class="chart-sub" id="sub-m0">TPV dos sellers novos (M0) captados no mes selecionado</div>
    <canvas id="chartDailyM0"></canvas>
  </div>

  <!-- Grafico 3: TPV M1 diario -->
  <div class="chart-wrap">
    <div class="chart-title">TPV M1 por Dia</div>
    <div class="chart-sub" id="sub-m1">TPV dos sellers M0 no mes seguinte (M1 disponivel a partir de Fev/26)</div>
    <canvas id="chartDailyM1"></canvas>
  </div>

  <!-- Grafico 4: TPV Total diario -->
  <div class="chart-wrap">
    <div class="chart-title">TPV Total Portfolio por Dia</div>
    <div class="chart-sub" id="sub-total">TPV total da carteira do reseller no mes selecionado</div>
    <canvas id="chartDailyTotal"></canvas>
  </div>

</div>

<div class="pane" id="pane-chart-devices">
  <div class="chart-wrap">
    <div class="chart-title">Pedidos e Ativacoes por Modelo e Mes</div>
    <div class="chart-sub">Point Pro vs Point Smart - Jan-Abr/26</div>
    <div class="chart-controls" id="nivel-filter-dev"></div>
    <canvas id="chartDevices"></canvas>
  </div>
  <div class="chart-wrap">
    <div class="chart-title">Mix de Modelos - % de Pedidos</div>
    <div class="chart-sub">Participacao Point Pro vs Smart por mes (empilhado 100%)</div>
    <canvas id="chartMix"></canvas>
  </div>
</div>

</div>
<div class="footer">Mercado Pago - Programa Renda na Mao - Fonte: BD_CUST_RESELLER_INFO / BD_CUST_RESELLER_INFO_DAILY</div>

<script>
const RAW = [
  {mes:"Jan/26",nivel:"Aprendiz",resellers:914,pedidos:2884,ativos:2391,tpv_m0:5904529,tpv_m1:null,tpv_total:2190087,pedidos_pro:2610,pedidos_smart:268,ativos_pro:2175,ativos_smart:211},
  {mes:"Jan/26",nivel:"Especialista",resellers:113,pedidos:1397,ativos:1170,tpv_m0:3045114,tpv_m1:null,tpv_total:2268030,pedidos_pro:1245,pedidos_smart:152,ativos_pro:1036,ativos_smart:134},
  {mes:"Jan/26",nivel:"Empreendedor",resellers:50,pedidos:938,ativos:830,tpv_m0:3139062,tpv_m1:null,tpv_total:2909063,pedidos_pro:777,pedidos_smart:161,ativos_pro:694,ativos_smart:136},
  {mes:"Jan/26",nivel:"Top Empreendedor",resellers:38,pedidos:1739,ativos:1648,tpv_m0:6647500,tpv_m1:null,tpv_total:5934960,pedidos_pro:1273,pedidos_smart:466,ativos_pro:1205,ativos_smart:443},
  {mes:"Fev/26",nivel:"Aprendiz",resellers:983,pedidos:2834,ativos:2149,tpv_m0:5455402,tpv_m1:8589250,tpv_total:3865778,pedidos_pro:2576,pedidos_smart:257,ativos_pro:1972,ativos_smart:177},
  {mes:"Fev/26",nivel:"Especialista",resellers:117,pedidos:1338,ativos:1102,tpv_m0:3811769,tpv_m1:4598512,tpv_total:5983828,pedidos_pro:1216,pedidos_smart:122,ativos_pro:1018,ativos_smart:84},
  {mes:"Fev/26",nivel:"Empreendedor",resellers:52,pedidos:1246,ativos:996,tpv_m0:2698795,tpv_m1:4720787,tpv_total:7119633,pedidos_pro:1061,pedidos_smart:185,ativos_pro:849,ativos_smart:147},
  {mes:"Fev/26",nivel:"Top Empreendedor",resellers:38,pedidos:2111,ativos:1772,tpv_m0:6183822,tpv_m1:12309138,tpv_total:17484241,pedidos_pro:1331,pedidos_smart:780,ativos_pro:1123,ativos_smart:649},
  {mes:"Mar/26",nivel:"Aprendiz",resellers:922,pedidos:2467,ativos:1478,tpv_m0:6653238,tpv_m1:7695710,tpv_total:4619592,pedidos_pro:2163,pedidos_smart:301,ativos_pro:1290,ativos_smart:186},
  {mes:"Mar/26",nivel:"Especialista",resellers:83,pedidos:896,ativos:523,tpv_m0:3397338,tpv_m1:5027261,tpv_total:7873138,pedidos_pro:802,pedidos_smart:94,ativos_pro:466,ativos_smart:57},
  {mes:"Mar/26",nivel:"Empreendedor",resellers:48,pedidos:1341,ativos:837,tpv_m0:4084953,tpv_m1:5424752,tpv_total:12847334,pedidos_pro:1113,pedidos_smart:228,ativos_pro:697,ativos_smart:140},
  {mes:"Mar/26",nivel:"Top Empreendedor",resellers:39,pedidos:1966,ativos:1409,tpv_m0:7784389,tpv_m1:11010999,tpv_total:30224110,pedidos_pro:1510,pedidos_smart:456,ativos_pro:1111,ativos_smart:298},
  {mes:"Abr/26",nivel:"Aprendiz",resellers:675,pedidos:1448,ativos:530,tpv_m0:5294588,tpv_m1:7556262,tpv_total:3606439,pedidos_pro:1276,pedidos_smart:169,ativos_pro:467,ativos_smart:61},
  {mes:"Abr/26",nivel:"Especialista",resellers:77,pedidos:549,ativos:148,tpv_m0:2316205,tpv_m1:4682157,tpv_total:8287688,pedidos_pro:443,pedidos_smart:106,ativos_pro:122,ativos_smart:26},
  {mes:"Abr/26",nivel:"Empreendedor",resellers:36,pedidos:547,ativos:173,tpv_m0:2400932,tpv_m1:5836200,tpv_total:11838473,pedidos_pro:450,pedidos_smart:97,ativos_pro:122,ativos_smart:51},
  {mes:"Abr/26",nivel:"Top Empreendedor",resellers:41,pedidos:1843,ativos:664,tpv_m0:5803605,tpv_m1:13406624,tpv_total:37531873,pedidos_pro:1409,pedidos_smart:434,ativos_pro:530,ativos_smart:134},
];

const DAILY = """ + daily_json + """;

const MES_ORDER=["Jan/26","Fev/26","Mar/26","Abr/26"];
const NIV_ORDER=["Aprendiz","Especialista","Empreendedor","Top Empreendedor"];
const NIV_CLASS={"Aprendiz":"nivel-aprendiz","Especialista":"nivel-especialista","Empreendedor":"nivel-empreendedor","Top Empreendedor":"nivel-top"};
const NIV_COLOR={"Aprendiz":"#9ca3af","Especialista":"#3b82f6","Empreendedor":"#f59e0b","Top Empreendedor":"#1A1F6B"};
const maxTPV=Math.max(...RAW.map(r=>r.tpv_m0));

const fmt=n=>n==null?'<span class="tpv-zero">-</span>':n>=1e6?`<span class="tpv-value">R$ ${(n/1e6).toFixed(2).replace('.',',')}M</span>`:`<span class="tpv-value">R$ ${n.toLocaleString('pt-BR')}</span>`;
const fmtN=n=>(n||0).toLocaleString('pt-BR');
const pct=(v,t)=>{if(!t||v==null)return '';const p=v/t*100;return `<span class="pct${p>=40?' pct-high':''}">${p.toFixed(1)}%</span>`;};

const totals={};
RAW.forEach(r=>{
  if(!totals[r.mes])totals[r.mes]={resellers:0,pedidos:0,ativos:0,tpv_m0:0,tpv_m1:0,haM1:false,tpv_total:0};
  totals[r.mes].resellers+=r.resellers;totals[r.mes].pedidos+=r.pedidos;totals[r.mes].ativos+=r.ativos;
  totals[r.mes].tpv_m0+=r.tpv_m0;totals[r.mes].tpv_total+=r.tpv_total;
  if(r.tpv_m1!=null){totals[r.mes].tpv_m1+=r.tpv_m1;totals[r.mes].haM1=true;}
});

function showTab(id,el){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('pane-'+id).classList.add('active');
  if(id==='chart-tpv')renderChartTpv();
  if(id==='chart-devices')renderChartDevices();
}

let sortCol=null,sortDir=1,activeMes=null,activeNivel=null,searchTerm='';

function getData(){
  let d=[...RAW];
  if(activeMes)d=d.filter(r=>r.mes===activeMes);
  if(activeNivel)d=d.filter(r=>r.nivel===activeNivel);
  if(searchTerm)d=d.filter(r=>Object.values(r).join(' ').toLowerCase().includes(searchTerm));
  if(sortCol)d.sort((a,b)=>{let av=a[sortCol]??-Infinity,bv=b[sortCol]??-Infinity;return(typeof av==='string'?av.localeCompare(bv):av-bv)*sortDir;});
  else d.sort((a,b)=>MES_ORDER.indexOf(a.mes)-MES_ORDER.indexOf(b.mes)||NIV_ORDER.indexOf(a.nivel)-NIV_ORDER.indexOf(b.nivel));
  return d;
}

function renderTabela(){
  const data=getData();
  let html='';
  data.forEach((r,i)=>{
    const isLast=i===data.length-1||data[i+1].mes!==r.mes;
    const t=totals[r.mes]||{};
    const bp=Math.round((r.tpv_m0/maxTPV)*100);
    html+=`<tr>
      <td><span class="mes-badge">${r.mes}</span></td>
      <td><span class="nivel-badge ${NIV_CLASS[r.nivel]||''}"><span class="nivel-dot"></span>${r.nivel}</span></td>
      <td>${fmtN(r.resellers)}${pct(r.resellers,t.resellers)}</td>
      <td>${fmtN(r.pedidos)}${pct(r.pedidos,t.pedidos)}</td>
      <td>${fmtN(r.ativos)}${pct(r.ativos,t.ativos)}</td>
      <td><div class="bar-cell">${fmt(r.tpv_m0)}${pct(r.tpv_m0,t.tpv_m0)}<div class="bar-bg"><div class="bar-fill" style="width:${bp}%"></div></div></div></td>
      <td>${fmt(r.tpv_m1)}${r.tpv_m1!=null&&t.haM1?pct(r.tpv_m1,t.tpv_m1):''}</td>
      <td>${fmt(r.tpv_total)}${pct(r.tpv_total,t.tpv_total)}</td>
    </tr>`;
    if(isLast&&!activeMes&&!sortCol){
      html+=`<tr class="group-total"><td><span class="mes-badge">${r.mes}</span></td><td style="font-size:11px">TOTAL</td>
        <td>${fmtN(t.resellers)}</td><td>${fmtN(t.pedidos)}</td><td>${fmtN(t.ativos)}</td>
        <td>${fmt(t.tpv_m0)}</td><td>${t.haM1?fmt(t.tpv_m1):fmt(null)}</td><td>${fmt(t.tpv_total)}</td></tr>`;
    }
  });
  document.getElementById('tbody').innerHTML=html||'<tr><td colspan="8" style="text-align:center;color:#ccc;padding:32px">Sem resultados</td></tr>';
}

function renderFiltersTabela(){
  document.getElementById('mes-filters').innerHTML=['Todos',...MES_ORDER].map(m=>`<button class="filter-btn${(!activeMes&&m==='Todos')||activeMes===m?' active':''}" data-mes="${m}">${m}</button>`).join('');
  document.getElementById('nivel-filters').innerHTML=['Todos',...NIV_ORDER].map(n=>`<button class="filter-btn${(!activeNivel&&n==='Todos')||activeNivel===n?' active':''}" data-nivel="${n}">${n}</button>`).join('');
}

function renderCardTabela(){
  const tp=RAW.reduce((s,r)=>s+r.pedidos,0),ta=RAW.reduce((s,r)=>s+r.ativos,0);
  const tm=RAW.reduce((s,r)=>s+r.tpv_m0,0),tm1=RAW.filter(r=>r.tpv_m1).reduce((s,r)=>s+r.tpv_m1,0);
  const tt=RAW.reduce((s,r)=>s+r.tpv_total,0);
  document.getElementById('cards-tabela').innerHTML=`
    <div class="card"><div class="card-label">Devices Pedidos</div><div class="card-value">${fmtN(tp)}</div><div class="card-sub">Jan-Abr/26</div></div>
    <div class="card"><div class="card-label">Devices Ativos</div><div class="card-value">${fmtN(ta)}</div><div class="card-sub">Jan-Abr/26</div></div>
    <div class="card"><div class="card-label">TPV M0</div><div class="card-value">R$ ${(tm/1e6).toFixed(1).replace('.',',')}M</div><div class="card-sub">Jan-Abr/26</div></div>
    <div class="card"><div class="card-label">TPV M1</div><div class="card-value">R$ ${(tm1/1e6).toFixed(1).replace('.',',')}M</div><div class="card-sub">Fev-Abr/26</div></div>
    <div class="card"><div class="card-label">TPV Total Portfolio</div><div class="card-value">R$ ${(tt/1e6).toFixed(1).replace('.',',')}M</div><div class="card-sub">Jan-Abr/26</div></div>`;
}

document.getElementById('mes-filters').addEventListener('click',e=>{if(!e.target.classList.contains('filter-btn'))return;activeMes=e.target.dataset.mes==='Todos'?null:e.target.dataset.mes;renderFiltersTabela();renderTabela();});
document.getElementById('nivel-filters').addEventListener('click',e=>{if(!e.target.classList.contains('filter-btn'))return;activeNivel=e.target.dataset.nivel==='Todos'?null:e.target.dataset.nivel;renderFiltersTabela();renderTabela();});
document.getElementById('search-input').addEventListener('input',e=>{searchTerm=e.target.value.toLowerCase().trim();renderTabela();});
document.querySelector('thead').addEventListener('click',e=>{const th=e.target.closest('th');if(!th)return;sortDir=sortCol===th.dataset.col?sortDir*-1:1;sortCol=th.dataset.col;document.querySelectorAll('thead th').forEach(t=>t.classList.remove('sorted-asc','sorted-desc'));th.classList.add(sortDir===1?'sorted-asc':'sorted-desc');renderTabela();});

let activeMesMod=null;
function renderModelos(){
  let data=[...RAW];
  if(activeMesMod)data=data.filter(r=>r.mes===activeMesMod);
  data.sort((a,b)=>MES_ORDER.indexOf(a.mes)-MES_ORDER.indexOf(b.mes)||NIV_ORDER.indexOf(a.nivel)-NIV_ORDER.indexOf(b.nivel));
  const mt={};
  data.forEach(r=>{if(!mt[r.mes])mt[r.mes]={pro:0,smart:0};mt[r.mes].pro+=r.pedidos_pro;mt[r.mes].smart+=r.pedidos_smart;});
  const totalPro=RAW.reduce((s,r)=>s+r.pedidos_pro,0),totalSmart=RAW.reduce((s,r)=>s+r.pedidos_smart,0);
  let html='';
  data.forEach((r,i)=>{
    const tot=(r.pedidos_pro+r.pedidos_smart)||1;
    const isLast=i===data.length-1||data[i+1]?.mes!==r.mes;
    html+=`<tr>
      <td><span class="mes-badge">${r.mes}</span></td>
      <td><span class="nivel-badge ${NIV_CLASS[r.nivel]||''}"><span class="nivel-dot"></span>${r.nivel}</span></td>
      <td style="text-align:right">${fmtN(r.pedidos_pro)}${pct(r.pedidos_pro,mt[r.mes]?.pro)}</td>
      <td style="text-align:right">${fmtN(r.ativos_pro)}</td>
      <td style="text-align:right">${fmtN(r.pedidos_smart)}${pct(r.pedidos_smart,mt[r.mes]?.smart)}</td>
      <td style="text-align:right">${fmtN(r.ativos_smart)}</td>
      <td style="text-align:right"><b>${(r.pedidos_pro/tot*100).toFixed(1)}%</b></td>
      <td style="text-align:right"><b>${(r.pedidos_smart/tot*100).toFixed(1)}%</b></td>
    </tr>`;
    if(isLast&&!activeMesMod){const t=mt[r.mes]||{pro:0,smart:0};const tot2=(t.pro+t.smart)||1;
      html+=`<tr class="group-total"><td><span class="mes-badge">${r.mes}</span></td><td style="font-size:11px">TOTAL</td><td style="text-align:right">${fmtN(t.pro)}</td><td></td><td style="text-align:right">${fmtN(t.smart)}</td><td></td><td style="text-align:right"><b>${(t.pro/tot2*100).toFixed(1)}%</b></td><td style="text-align:right"><b>${(t.smart/tot2*100).toFixed(1)}%</b></td></tr>`;}
  });
  document.getElementById('tbody-modelos').innerHTML=html;
  document.getElementById('cards-modelos').innerHTML=`
    <div class="card"><div class="card-label">Point Pro Pedidos</div><div class="card-value">${fmtN(totalPro)}</div><div class="card-sub">Jan-Abr/26</div></div>
    <div class="card"><div class="card-label">Point Smart Pedidos</div><div class="card-value">${fmtN(totalSmart)}</div><div class="card-sub">Jan-Abr/26</div></div>
    <div class="card"><div class="card-label">Mix Pro</div><div class="card-value">${(totalPro/(totalPro+totalSmart)*100).toFixed(1)}%</div><div class="card-sub">do total</div></div>
    <div class="card"><div class="card-label">Mix Smart</div><div class="card-value">${(totalSmart/(totalPro+totalSmart)*100).toFixed(1)}%</div><div class="card-sub">do total</div></div>`;
  document.getElementById('mes-filters-mod').innerHTML=['Todos',...MES_ORDER].map(m=>`<button class="filter-btn${(!activeMesMod&&m==='Todos')||activeMesMod===m?' active':''}" data-mes="${m}">${m}</button>`).join('');
}
document.getElementById('mes-filters-mod').addEventListener('click',e=>{if(!e.target.classList.contains('filter-btn'))return;activeMesMod=e.target.dataset.mes==='Todos'?null:e.target.dataset.mes;renderModelos();});

// ── HELPERS ──
const MES_TO_YYYYMM={"Jan/26":"2026-01","Fev/26":"2026-02","Mar/26":"2026-03","Abr/26":"2026-04"};
const MES_LABEL={"2026-01":"Jan/26","2026-02":"Fev/26","2026-03":"Mar/26","2026-04":"Abr/26"};

const tooltipTotal=(items,yFmt)=>'TOTAL: '+yFmt(items.reduce((s,i)=>s+(i.raw||0),0));

function makeLineChart(canvasId,labels,datasets,yFmt){
  const existing=Chart.getChart(canvasId);if(existing)existing.destroy();
  return new Chart(document.getElementById(canvasId).getContext('2d'),{
    type:'line',data:{labels,datasets},
    options:{responsive:true,
      plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
        tooltip:{mode:'index',intersect:false,callbacks:{
          label:i=>`${i.dataset.label}: ${yFmt(i.raw)}`,
          footer:items=>tooltipTotal(items,yFmt)
        }}},
      scales:{x:{ticks:{maxRotation:45,font:{size:10},maxTicksLimit:25},grid:{display:false}},
        y:{ticks:{callback:v=>yFmt(v),font:{size:10}},grid:{color:'#f0f0f0'}}},
      interaction:{mode:'index',intersect:false}}
  });
}

function makeBarsChart(canvasId,labels,datasets,yFmt){
  const existing=Chart.getChart(canvasId);if(existing)existing.destroy();
  return new Chart(document.getElementById(canvasId).getContext('2d'),{
    type:'bar',data:{labels,datasets},
    options:{responsive:true,
      plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
        tooltip:{mode:'index',intersect:false,callbacks:{
          label:i=>`${i.dataset.label}: ${yFmt(i.raw)}`,
          footer:items=>tooltipTotal(items,yFmt)
        }}},
      scales:{x:{grid:{display:false}},y:{ticks:{callback:v=>yFmt(v),font:{size:10}},grid:{color:'#f0f0f0'}}}}
  });
}

const fmtK=v=>v>=1e6?'R$ '+(v/1e6).toFixed(2).replace('.',',')+'M':'R$ '+(v/1000).toFixed(1)+'K';

let activeMesTpvDaily='Fev/26',activeNivelTpvBar='Todos',activeNivelTpvDaily='Todos';

function renderChartTpv(){
  // ── Grafico 1: mensal bar ──
  const niv=activeNivelTpvBar==='Todos'?NIV_ORDER:[activeNivelTpvBar];
  const barDatasets=[];
  niv.forEach(n=>{
    barDatasets.push({
      label:n+' M0',
      data:MES_ORDER.map(m=>RAW.filter(r=>r.mes===m&&r.nivel===n).reduce((s,r)=>s+r.tpv_m0,0)),
      backgroundColor:NIV_COLOR[n],borderRadius:3,stack:n
    });
    barDatasets.push({
      label:n+' Total',
      data:MES_ORDER.map(m=>RAW.filter(r=>r.mes===m&&r.nivel===n).reduce((s,r)=>s+r.tpv_total,0)),
      backgroundColor:NIV_COLOR[n]+'55',borderRadius:3,stack:n
    });
  });
  makeBarsChart('chartTpvBar',MES_ORDER,barDatasets,fmtK);

  // filtro nivel barra
  document.getElementById('nivel-filter-tpv-bar').innerHTML=['Todos',...NIV_ORDER].map(n=>
    `<button class="filter-btn${activeNivelTpvBar===n?' active':''}" onclick="activeNivelTpvBar='${n}';renderChartTpv()">${n}</button>`).join('');

  // ── Graficos 2-4: diarios ──
  const prefix=MES_TO_YYYYMM[activeMesTpvDaily];
  const diasMes=DAILY.filter(d=>d.data.startsWith(prefix));
  const dates=[...new Set(diasMes.map(d=>d.data))].sort();
  const niv2=activeNivelTpvDaily==='Todos'?NIV_ORDER:[activeNivelTpvDaily];

  function dailyDatasets(field){
    return niv2.map(n=>{
      const map=Object.fromEntries(diasMes.filter(d=>d.nivel===n).map(d=>[d.data,d]));
      return {label:n,data:dates.map(d=>map[d]?.[field]||0),borderColor:NIV_COLOR[n],backgroundColor:NIV_COLOR[n]+'22',borderWidth:2,pointRadius:2,fill:false,tension:.3};
    });
  }

  makeLineChart('chartDailyM0',dates,dailyDatasets('tpv_m0'),fmtK);
  makeLineChart('chartDailyM1',dates,dailyDatasets('tpv_m1'),fmtK);
  makeLineChart('chartDailyTotal',dates,dailyDatasets('tpv_total'),fmtK);

  // update subtitles
  document.getElementById('sub-m0').textContent='Sellers novos (M0) captados em '+activeMesTpvDaily+' - TPV por dia';
  document.getElementById('sub-m1').textContent='Sellers M0 de '+activeMesTpvDaily+' no mes seguinte - TPV por dia';
  document.getElementById('sub-total').textContent='TPV total da carteira em '+activeMesTpvDaily+' - por dia';

  // filtros
  document.getElementById('mes-filter-tpv-daily').innerHTML=MES_ORDER.map(m=>
    `<button class="filter-btn${activeMesTpvDaily===m?' active':''}" onclick="activeMesTpvDaily='${m}';renderChartTpv()">${m}</button>`).join('');
  document.getElementById('nivel-filter-tpv-daily').innerHTML=['Todos',...NIV_ORDER].map(n=>
    `<button class="filter-btn${activeNivelTpvDaily===n?' active':''}" onclick="activeNivelTpvDaily='${n}';renderChartTpv()">${n}</button>`).join('');
}

let chartDev=null,chartMix=null,activeNivelDev='Todos';
function renderChartDevices(){
  let data=[...RAW];
  if(activeNivelDev!=='Todos')data=data.filter(r=>r.nivel===activeNivelDev);
  const proData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.pedidos_pro,0));
  const smartData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.pedidos_smart,0));
  const ativProData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.ativos_pro,0));
  const ativSmartData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.ativos_smart,0));
  if(chartDev)chartDev.destroy();
  chartDev=new Chart(document.getElementById('chartDevices').getContext('2d'),{
    type:'bar',data:{labels:MES_ORDER,datasets:[
      {label:'Pro - Pedidos',data:proData,backgroundColor:'#1A1F6B',borderRadius:4},
      {label:'Smart - Pedidos',data:smartData,backgroundColor:'#FFE600',borderRadius:4},
      {label:'Pro - Ativos',data:ativProData,backgroundColor:'#1A1F6B44',borderRadius:4},
      {label:'Smart - Ativos',data:ativSmartData,backgroundColor:'#FFE60044',borderRadius:4},
    ]},options:{responsive:true,plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}}},scales:{x:{grid:{display:false}},y:{ticks:{font:{size:10}},grid:{color:'#f0f0f0'}}}}
  });
  if(chartMix)chartMix.destroy();
  const mixData=MES_ORDER.map((m,i)=>{const t=proData[i]+smartData[i];return t?Math.round(proData[i]/t*100):0;});
  chartMix=new Chart(document.getElementById('chartMix').getContext('2d'),{
    type:'bar',data:{labels:MES_ORDER,datasets:[
      {label:'% Pro',data:mixData,backgroundColor:'#1A1F6B',borderRadius:4},
      {label:'% Smart',data:mixData.map(v=>100-v),backgroundColor:'#FFE600',borderRadius:4},
    ]},options:{responsive:true,plugins:{legend:{position:'top',labels:{font:{size:11}}}},scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,max:100,ticks:{callback:v=>v+'%',font:{size:10}},grid:{color:'#f0f0f0'}}}}
  });
  document.getElementById('nivel-filter-dev').innerHTML=['Todos',...NIV_ORDER].map(n=>`<button class="filter-btn${activeNivelDev===n?' active':''}" onclick="activeNivelDev='${n}';renderChartDevices()">${n}</button>`).join('');
}

renderCardTabela();renderFiltersTabela();renderTabela();renderModelos();
</script>
</body>
</html>"""

with open(r'C:\Users\daviaraujo\resellers-grid\index.html','w',encoding='utf-8') as f:
    f.write(html)
print('OK - arquivo gerado')
