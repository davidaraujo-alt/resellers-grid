import csv, json

leads = []
with open(r'C:\Users\daviaraujo\resellers-grid\daily_leads.csv') as f:
    for row in csv.DictReader(f):
        if row.get('data','').startswith('2026'):
            leads.append({'data':row['data'],'nivel':row['nivel'],'cadastrados':int(row['cadastrados']),'convertidos':int(row['convertidos'])})
leads_json = json.dumps(leads)

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

<div style="background:#FFE600;padding:14px 32px;display:flex;align-items:center">
  <span style="font-size:20px;font-weight:900;color:#1A1F6B;letter-spacing:.06em;text-transform:uppercase">RESELLER 2026</span>
</div>

<div class="tabs">
  <div class="tab active" onclick="showTab('tabela',this)">&#128202; Tabela</div>
  <div class="tab" onclick="showTab('chart-tpv',this)">&#128200; TPV</div>
  <div class="tab" onclick="showTab('chart-devices',this)">&#128230; Devices / Mes</div>
  <div class="tab" onclick="showTab('diarizado',this)">&#128197; Diarizado</div>
  <div class="tab" onclick="showTab('niveis',this)">&#11014; Subidas de Nível</div>
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


<div class="pane" id="pane-chart-tpv">

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


</div>

<div class="pane" id="pane-chart-devices">
  <div class="chart-controls" id="nivel-filter-dev" style="margin-bottom:16px"></div>
  <div class="chart-wrap">
    <div class="chart-title">Pedidos por Modelo</div>
    <div class="chart-sub">Point Pro vs Point Smart - Jan-Abr/26</div>
    <canvas id="chartDevicesPedidos"></canvas>
  </div>
  <div class="chart-wrap">
    <div class="chart-title">Ativos por Modelo</div>
    <div class="chart-sub">Point Pro vs Point Smart - Jan-Abr/26</div>
    <canvas id="chartDevicesAtivos"></canvas>
  </div>
</div>

<!-- ── TAB DIARIZADO ── -->
<div class="pane" id="pane-diarizado">
  <div style="font-size:18px;font-weight:900;color:#1A1F6B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:20px;border-left:5px solid #FFE600;padding-left:14px">Diarizado</div>
  <div class="cards" id="cards-diarizado"></div>
  <div style="background:#fff;border-radius:12px;padding:14px 18px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.06)">
    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div>
        <div style="font-size:10px;color:#999;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">Mes</div>
        <div id="mes-filter-diar" style="display:flex;gap:6px;flex-wrap:wrap"></div>
      </div>
      <div>
        <div style="font-size:10px;color:#999;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">Nivel</div>
        <div id="nivel-filter-diar" style="display:flex;gap:6px;flex-wrap:wrap"></div>
      </div>
      <div style="margin-left:auto;align-self:flex-end">
        <input class="search-box" type="text" placeholder="Buscar data..." id="search-diar" style="margin-left:0"/>
      </div>
    </div>
  </div>
  <!-- Gráficos mensais -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px">
    <div class="chart-wrap" style="margin-bottom:0">
      <div class="chart-title">Cadastrados vs Convertidos — por Mês</div>
      <div class="chart-sub">Cadastros e conversões mensais acumuladas</div>
      <canvas id="chartDiarMensal"></canvas>
    </div>
    <div class="chart-wrap" style="margin-bottom:0">
      <div class="chart-title">1ª Compra por Mês</div>
      <div class="chart-sub">Parceiros que fizeram a 1ª compra no mês (independente do cadastro)</div>
      <canvas id="chartDiarPrimeira"></canvas>
    </div>
  </div>

  <div style="overflow-x:auto">
    <table id="table-diar" style="min-width:600px">
      <thead><tr id="thead-diar-row"></tr></thead>
      <tbody id="tbody-diar"></tbody>
    </table>
  </div>
</div>

<!-- ── TAB SUBIDAS DE NÍVEL ── -->
<div class="pane" id="pane-niveis">
  <div style="font-size:18px;font-weight:900;color:#1A1F6B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:20px;border-left:5px solid #FFE600;padding-left:14px">Subidas de Nível — 2026</div>
  <div class="cards" id="cards-niveis"></div>

  <!-- Filtros -->
  <div class="controls" style="margin-bottom:16px">
    <div id="mes-filter-niveis" style="display:flex;gap:6px;flex-wrap:wrap"></div>
    <div id="trans-filter-niveis" style="display:flex;gap:6px;flex-wrap:wrap"></div>
    <input class="search-box" type="text" placeholder="Buscar reseller..." id="search-niveis"/>
  </div>

  <!-- Tabela detalhada -->
  <div class="grid-wrapper" style="margin-bottom:24px">
    <table>
      <thead><tr>
        <th data-col-n="dt">Data</th>
        <th data-col-n="reseller">Reseller ID</th>
        <th data-col-n="transicao">Transição</th>
        <th data-col-n="nivel_atual">Nível Atual</th>
      </tr></thead>
      <tbody id="tbody-niveis"></tbody>
    </table>
  </div>

  <!-- Gráfico -->
  <div class="chart-wrap">
    <div class="chart-title">Subidas por Transição e Mês</div>
    <div class="chart-sub">Quantidade de resellers que subiram de nível — Jan–Abr/26</div>
    <canvas id="chartNiveis"></canvas>
  </div>
</div>

</div>
<div class="footer">Mercado Pago - Programa Renda na Mao - Fonte: BD_CUST_RESELLER_INFO / BD_CUST_RESELLER_INFO_DAILY</div>

<script>
const RAW = [
  {mes:"Jan/26",nivel:"Aprendiz",        resellers:914, pedidos:2884, ativos:2392, tpv_m0:2211690, tpv_m1:null,      tpv_total:2211690,  pedidos_pro:2610, pedidos_smart:268, ativos_pro:2176, ativos_smart:211},
  {mes:"Jan/26",nivel:"Especialista",     resellers:113, pedidos:1397, ativos:1173, tpv_m0:2255581, tpv_m1:null,      tpv_total:2255581,  pedidos_pro:1245, pedidos_smart:152, ativos_pro:1038, ativos_smart:135},
  {mes:"Jan/26",nivel:"Empreendedor",     resellers:50,  pedidos:938,  ativos:830,  tpv_m0:2910252, tpv_m1:null,      tpv_total:2910252,  pedidos_pro:777,  pedidos_smart:161, ativos_pro:694,  ativos_smart:136},
  {mes:"Jan/26",nivel:"Top Empreendedor", resellers:38,  pedidos:1739, ativos:1650, tpv_m0:5931725, tpv_m1:null,      tpv_total:5931725,  pedidos_pro:1273, pedidos_smart:466, ativos_pro:1207, ativos_smart:443},
  {mes:"Fev/26",nivel:"Aprendiz",        resellers:983, pedidos:2834, ativos:2151, tpv_m0:1962846, tpv_m1:1940610,  tpv_total:3903456,  pedidos_pro:2576, pedidos_smart:257, ativos_pro:1974, ativos_smart:177},
  {mes:"Fev/26",nivel:"Especialista",     resellers:117, pedidos:1338, ativos:1111, tpv_m0:2751770, tpv_m1:3159259,  tpv_total:5911029,  pedidos_pro:1216, pedidos_smart:122, ativos_pro:1026, ativos_smart:85},
  {mes:"Fev/26",nivel:"Empreendedor",     resellers:52,  pedidos:1246, ativos:1003, tpv_m0:2537155, tpv_m1:4573078,  tpv_total:7110233,  pedidos_pro:1061, pedidos_smart:185, ativos_pro:856,  ativos_smart:147},
  {mes:"Fev/26",nivel:"Top Empreendedor", resellers:38,  pedidos:2111, ativos:1784, tpv_m0:5790677, tpv_m1:11683107, tpv_total:17473784, pedidos_pro:1331, pedidos_smart:780, ativos_pro:1129, ativos_smart:655},
  {mes:"Mar/26",nivel:"Aprendiz",        resellers:922, pedidos:2467, ativos:1493, tpv_m0:2268275, tpv_m1:812114,   tpv_total:4671474,  pedidos_pro:2163, pedidos_smart:301, ativos_pro:1305, ativos_smart:186},
  {mes:"Mar/26",nivel:"Especialista",     resellers:83,  pedidos:896,  ativos:531,  tpv_m0:2332724, tpv_m1:3047702,  tpv_total:7647216,  pedidos_pro:802,  pedidos_smart:94,  ativos_pro:472,  ativos_smart:59},
  {mes:"Mar/26",nivel:"Empreendedor",     resellers:48,  pedidos:1341, ativos:840,  tpv_m0:3745008, tpv_m1:4849151,  tpv_total:12815918, pedidos_pro:1113, pedidos_smart:228, ativos_pro:698,  ativos_smart:142},
  {mes:"Mar/26",nivel:"Top Empreendedor", resellers:39,  pedidos:1966, ativos:1421, tpv_m0:7637929, tpv_m1:10886088, tpv_total:30250150, pedidos_pro:1510, pedidos_smart:456, ativos_pro:1119, ativos_smart:302},
  {mes:"Abr/26",nivel:"Aprendiz",        resellers:700, pedidos:1506, ativos:561,  tpv_m0:2005313, tpv_m1:846887,   tpv_total:4005551,  pedidos_pro:1324, pedidos_smart:179, ativos_pro:493,  ativos_smart:66},
  {mes:"Abr/26",nivel:"Especialista",     resellers:77,  pedidos:555,  ativos:159,  tpv_m0:1698542, tpv_m1:2843066,  tpv_total:8610129,  pedidos_pro:449,  pedidos_smart:106, ativos_pro:130,  ativos_smart:29},
  {mes:"Abr/26",nivel:"Empreendedor",     resellers:37,  pedidos:579,  ativos:186,  tpv_m0:1916173, tpv_m1:4615107,  tpv_total:12503276, pedidos_pro:471,  pedidos_smart:108, ativos_pro:132,  ativos_smart:54},
  {mes:"Abr/26",nivel:"Top Empreendedor", resellers:41,  pedidos:1916, ativos:721,  tpv_m0:6039045, tpv_m1:13532350, tpv_total:39005237, pedidos_pro:1468, pedidos_smart:448, ativos_pro:575,  ativos_smart:146},
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
  if(id==='diarizado')renderDiarizado();
  if(id==='niveis')renderNiveis();
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
  // ── Graficos diarios ──
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

  // update subtitles
  document.getElementById('sub-m0').textContent='Sellers novos (M0) captados em '+activeMesTpvDaily+' - TPV por dia';
  document.getElementById('sub-m1').textContent='Sellers M0 de '+activeMesTpvDaily+' no mes seguinte - TPV por dia';

  // filtros
  document.getElementById('mes-filter-tpv-daily').innerHTML=MES_ORDER.map(m=>
    `<button class="filter-btn${activeMesTpvDaily===m?' active':''}" onclick="activeMesTpvDaily='${m}';renderChartTpv()">${m}</button>`).join('');
  document.getElementById('nivel-filter-tpv-daily').innerHTML=['Todos',...NIV_ORDER].map(n=>
    `<button class="filter-btn${activeNivelTpvDaily===n?' active':''}" onclick="activeNivelTpvDaily='${n}';renderChartTpv()">${n}</button>`).join('');
}

let chartDevPedidos=null,chartDevAtivos=null,activeNivelDev='Todos';
function renderChartDevices(){
  let data=[...RAW];
  if(activeNivelDev!=='Todos')data=data.filter(r=>r.nivel===activeNivelDev);
  const proData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.pedidos_pro,0));
  const smartData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.pedidos_smart,0));
  const ativProData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.ativos_pro,0));
  const ativSmartData=MES_ORDER.map(m=>data.filter(r=>r.mes===m).reduce((s,r)=>s+r.ativos_smart,0));

  const tooltipDev=(items,label)=>`${label}: `+fmtN(items.reduce((s,i)=>s+(i.raw||0),0));
  const devOpts=(footerLabel)=>({responsive:true,
    plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
      tooltip:{mode:'index',intersect:false,callbacks:{
        label:i=>`${i.dataset.label}: ${fmtN(i.raw)}`,
        footer:items=>tooltipDev(items,footerLabel)
      }}},
    scales:{x:{grid:{display:false}},y:{ticks:{font:{size:10}},grid:{color:'#f0f0f0'}}}});

  if(chartDevPedidos)chartDevPedidos.destroy();
  chartDevPedidos=new Chart(document.getElementById('chartDevicesPedidos').getContext('2d'),{
    type:'bar',data:{labels:MES_ORDER,datasets:[
      {label:'Point Pro',data:proData,backgroundColor:'#1A1F6B',borderRadius:4},
      {label:'Point Smart',data:smartData,backgroundColor:'#FFE600',borderRadius:4},
    ]},options:devOpts('TOTAL PEDIDOS')});

  if(chartDevAtivos)chartDevAtivos.destroy();
  chartDevAtivos=new Chart(document.getElementById('chartDevicesAtivos').getContext('2d'),{
    type:'bar',data:{labels:MES_ORDER,datasets:[
      {label:'Point Pro',data:ativProData,backgroundColor:'#1A1F6B',borderRadius:4},
      {label:'Point Smart',data:ativSmartData,backgroundColor:'#FFE600',borderRadius:4},
    ]},options:devOpts('TOTAL ATIVOS')});

  document.getElementById('nivel-filter-dev').innerHTML=['Todos',...NIV_ORDER].map(n=>`<button class="filter-btn${activeNivelDev===n?' active':''}" onclick="activeNivelDev='${n}';renderChartDevices()">${n}</button>`).join('');
}

// ── DIARIZADO ──
const LEADS = """ + leads_json + """;
const MES_PREFIX={"Jan/26":"2026-01","Fev/26":"2026-02","Mar/26":"2026-03","Abr/26":"2026-04"};
const PRIMEIRA_COMPRA={"2026-01-02":14,"2026-01-03":3,"2026-01-04":6,"2026-01-05":11,"2026-01-06":11,"2026-01-07":8,"2026-01-08":8,"2026-01-09":5,"2026-01-10":5,"2026-01-11":5,"2026-01-12":10,"2026-01-13":8,"2026-01-14":6,"2026-01-15":12,"2026-01-16":7,"2026-01-17":4,"2026-01-18":4,"2026-01-19":8,"2026-01-20":7,"2026-01-21":6,"2026-01-22":7,"2026-01-23":9,"2026-01-24":3,"2026-01-25":4,"2026-01-26":11,"2026-01-27":8,"2026-01-28":12,"2026-01-29":7,"2026-01-30":7,"2026-01-31":10,"2026-02-01":3,"2026-02-02":9,"2026-02-03":19,"2026-02-04":17,"2026-02-05":15,"2026-02-06":17,"2026-02-07":13,"2026-02-08":1,"2026-02-09":12,"2026-02-10":14,"2026-02-11":11,"2026-02-12":8,"2026-02-13":6,"2026-02-14":6,"2026-02-15":4,"2026-02-16":3,"2026-02-17":2,"2026-02-18":12,"2026-02-19":14,"2026-02-20":18,"2026-02-21":7,"2026-02-22":3,"2026-02-23":11,"2026-02-24":16,"2026-02-25":13,"2026-02-26":14,"2026-02-27":8,"2026-02-28":5,"2026-03-01":7,"2026-03-02":13,"2026-03-03":12,"2026-03-04":6,"2026-03-05":10,"2026-03-06":8,"2026-03-07":16,"2026-03-08":5,"2026-03-09":10,"2026-03-10":14,"2026-03-11":11,"2026-03-12":12,"2026-03-13":12,"2026-03-14":8,"2026-03-15":4,"2026-03-16":15,"2026-03-17":10,"2026-03-18":6,"2026-03-19":12,"2026-03-20":8,"2026-03-21":8,"2026-03-22":3,"2026-03-23":17,"2026-03-24":10,"2026-03-25":15,"2026-03-26":12,"2026-03-27":12,"2026-03-28":13,"2026-03-29":2,"2026-03-30":9,"2026-03-31":15,"2026-04-01":20,"2026-04-02":7,"2026-04-03":8,"2026-04-04":3,"2026-04-05":4,"2026-04-06":9,"2026-04-07":14,"2026-04-08":9,"2026-04-09":8,"2026-04-10":6,"2026-04-11":3,"2026-04-12":5,"2026-04-13":12,"2026-04-14":7,"2026-04-15":10,"2026-04-16":6,"2026-04-17":9,"2026-04-18":8,"2026-04-19":5,"2026-04-20":7,"2026-04-21":3,"2026-04-22":6,"2026-04-23":8,"2026-04-24":9,"2026-04-25":5,"2026-04-26":4,"2026-04-27":11,"2026-04-28":3};

let activeMesDiar=null,activeNivelDiar='Todos',searchDiar='',sortColD=null,sortDirD=1;

function getDataDiar(){
  let d=[...LEADS];
  if(activeMesDiar) d=d.filter(r=>r.data.startsWith(MES_PREFIX[activeMesDiar]));
  if(activeNivelDiar!=='Todos') d=d.filter(r=>r.nivel===activeNivelDiar);
  if(searchDiar) d=d.filter(r=>r.data.includes(searchDiar));
  // Agrupa por data
  const byDate={};
  d.forEach(r=>{
    if(!byDate[r.data]) byDate[r.data]={data:r.data,cadastrados:0,convertidos:0};
    byDate[r.data].cadastrados+=r.cadastrados;
    byDate[r.data].convertidos+=r.convertidos;
  });
  let rows=Object.values(byDate);
  if(sortColD) rows.sort((a,b)=>{
    const av=sortColD==='taxa'?(a.cadastrados?a.convertidos/a.cadastrados*100:0):a[sortColD];
    const bv=sortColD==='taxa'?(b.cadastrados?b.convertidos/b.cadastrados*100:0):b[sortColD];
    return (typeof av==='string'?av.localeCompare(bv):av-bv)*sortDirD;
  });
  else rows.sort((a,b)=>a.data.localeCompare(b.data));
  return rows;
}

function renderDiarizado(){
  const data=getDataDiar();
  const totCad=data.reduce((s,r)=>s+r.cadastrados,0);
  const totConv=data.reduce((s,r)=>s+r.convertidos,0);
  document.getElementById('cards-diarizado').innerHTML=`
    <div class="card"><div class="card-label">Cadastrados</div><div class="card-value">${fmtN(totCad)}</div><div class="card-sub">no filtro selecionado</div></div>
    <div class="card"><div class="card-label">Convertidos</div><div class="card-value">${fmtN(totConv)}</div><div class="card-sub">fizeram 1a venda</div></div>
    <div class="card"><div class="card-label">Taxa Conversao</div><div class="card-value">${totCad?(totConv/totCad*100).toFixed(2)+'%':'—'}</div><div class="card-sub">convertidos / cadastrados</div></div>`;

  // Cabeçalho: Métrica | dia1 | dia2 | ...
  const dates=data.map(r=>r.data);
  const shortDate=d=>d.slice(8)+'/'+d.slice(5,7); // dd/mm
  const thStyle='background:#1A1F6B;color:#FFE600;padding:10px 12px;text-align:right;font-size:11px;white-space:nowrap';
  document.getElementById('thead-diar-row').innerHTML=
    `<th style="${thStyle};text-align:left;letter-spacing:.05em;text-transform:uppercase">Metrica</th>`+
    dates.map(d=>`<th style="${thStyle}">${shortDate(d)}</th>`).join('')+
    `<th style="${thStyle};background:#FFE600;color:#1A1F6B;font-weight:900">TOTAL</th>`;

  // Escala de cor por terciis (ruim=vermelho, medio=amarelo, bom=verde)
  function colorScale(nums){
    const sorted=[...nums].sort((a,b)=>a-b);
    const p33=sorted[Math.floor(sorted.length*0.33)];
    const p66=sorted[Math.floor(sorted.length*0.66)];
    return nums.map(v=>v<=p33?'background:#ffe5e5':v<=p66?'background:#fffde7':'background:#e6f9ec');
  }

  const tdTotal='padding:10px 12px;text-align:right;font-size:12px;border-bottom:1px solid #f0f0f0;background:#fffde7;font-weight:800;color:#1A1F6B';

  function colorRow(label, nums, fmt, total){
    const colors=colorScale(nums);
    return `<tr>
      <td style="padding:10px 14px;font-weight:600;color:#1A1F6B;background:#f9f9ff;white-space:nowrap;font-size:12px;border-bottom:1px solid #f0f0f0">${label}</td>
      ${nums.map((v,i)=>`<td style="padding:10px 12px;text-align:right;font-size:12px;border-bottom:1px solid #f0f0f0;${colors[i]}">${fmt(v)}</td>`).join('')}
      <td style="${tdTotal}">${total}</td>
    </tr>`;
  }

  const cadNums      = data.map(r=>r.cadastrados);
  const convNums     = data.map(r=>r.convertidos);
  const taxaNums     = data.map(r=>r.cadastrados?r.convertidos/r.cadastrados*100:0);
  const primeiroNums = data.map(r=>PRIMEIRA_COMPRA[r.data]||0);
  const totCadAll    = cadNums.reduce((s,v)=>s+v,0);
  const totConvAll   = convNums.reduce((s,v)=>s+v,0);
  const totPrimeiro  = primeiroNums.reduce((s,v)=>s+v,0);

  document.getElementById('tbody-diar').innerHTML = data.length ? [
    colorRow('Cadastrados',   cadNums,      v=>fmtN(v),          fmtN(totCadAll)),
    colorRow('Convertidos',   convNums,     v=>fmtN(v),          fmtN(totConvAll)),
    colorRow('1ª Compra',     primeiroNums, v=>fmtN(v),          fmtN(totPrimeiro)),
    colorRow('Taxa Conv. %',  taxaNums,     v=>v.toFixed(2)+'%', (totCadAll?totConvAll/totCadAll*100:0).toFixed(2)+'%'),
  ].join('') : `<tr><td colspan="${dates.length+2}" style="text-align:center;color:#ccc;padding:32px">Sem resultados</td></tr>`;

  // Gráfico 1 — Cadastrados vs Convertidos por mês
  const mesesDiar=["Jan/26","Fev/26","Mar/26","Abr/26"];
  const prefDiar={"Jan/26":"2026-01","Fev/26":"2026-02","Mar/26":"2026-03","Abr/26":"2026-04"};
  const cadMes=mesesDiar.map(m=>LEADS.filter(r=>r.data.startsWith(prefDiar[m])).reduce((s,r)=>s+r.cadastrados,0));
  const convMes=mesesDiar.map(m=>LEADS.filter(r=>r.data.startsWith(prefDiar[m])).reduce((s,r)=>s+r.convertidos,0));
  const primMes=mesesDiar.map(m=>Object.entries(PRIMEIRA_COMPRA).filter(([d])=>d.startsWith(prefDiar[m])).reduce((s,[,v])=>s+v,0));

  const ex1=Chart.getChart('chartDiarMensal');if(ex1)ex1.destroy();
  new Chart(document.getElementById('chartDiarMensal').getContext('2d'),{
    type:'bar',data:{labels:mesesDiar,datasets:[
      {label:'Cadastrados',data:cadMes,backgroundColor:'#1A1F6B',borderRadius:4},
      {label:'Convertidos',data:convMes,backgroundColor:'#FFE600',borderRadius:4},
    ]},options:{responsive:true,plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
      tooltip:{mode:'index',intersect:false,callbacks:{label:i=>`${i.dataset.label}: ${fmtN(i.raw)}`,footer:items=>'TOTAL: '+fmtN(items.reduce((s,i)=>s+(i.raw||0),0))}}},
      scales:{x:{grid:{display:false}},y:{ticks:{font:{size:10}},grid:{color:'#f0f0f0'}}}}
  });

  // Gráfico 2 — Aprendiz com compra no mês vs 1ª compra
  const aprendizComCompra=mesesDiar.map(m=>RAW.find(r=>r.mes===m&&r.nivel==='Aprendiz')?.resellers||0);
  const aprendizPrimeira=[226,281,315,209];
  const ex2=Chart.getChart('chartDiarPrimeira');if(ex2)ex2.destroy();
  const pctNovos=aprendizComCompra.map((v,i)=>v?+(aprendizPrimeira[i]/v*100).toFixed(1):0);
  new Chart(document.getElementById('chartDiarPrimeira').getContext('2d'),{
    type:'bar',
    data:{labels:mesesDiar,datasets:[
      {label:'Aprendiz c/ Compra no Mês',data:aprendizComCompra,backgroundColor:'#1A1F6B',borderRadius:4,yAxisID:'y'},
      {label:'Aprendiz c/ 1ª Compra',data:aprendizPrimeira,backgroundColor:'#009EE3',borderRadius:4,yAxisID:'y'},
      {label:'% Novos no Mês',data:pctNovos,type:'line',borderColor:'#f59e0b',backgroundColor:'transparent',borderWidth:2.5,pointRadius:6,pointBackgroundColor:'#f59e0b',pointBorderColor:'#fff',pointBorderWidth:2,fill:false,tension:.3,yAxisID:'y2',order:0},
    ]},
    options:{responsive:true,plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
      tooltip:{mode:'index',intersect:false,callbacks:{
        label:i=>i.dataset.yAxisID==='y2'?`% Novos: ${i.raw}%`:`${i.dataset.label}: ${fmtN(i.raw)}`,
      }}},
      scales:{
        x:{grid:{display:false}},
        y:{ticks:{font:{size:10}},grid:{color:'#f0f0f0'},position:'left'},
        y2:{ticks:{callback:v=>v+'%',font:{size:10}},grid:{display:false},position:'right',min:0,max:100}
      }}
  });

  document.getElementById('mes-filter-diar').innerHTML=['Todos',...MES_ORDER].map(m=>
    `<button class="filter-btn${(!activeMesDiar&&m==='Todos')||activeMesDiar===m?' active':''}" onclick="activeMesDiar='${m}';renderDiarizado()">${m}</button>`).join('');
  document.getElementById('nivel-filter-diar').innerHTML=['Todos',...NIV_ORDER].map(n=>
    `<button class="filter-btn${activeNivelDiar===n?' active':''}" onclick="activeNivelDiar='${n}';renderDiarizado()">${n}</button>`).join('');
}

document.getElementById('search-diar').addEventListener('input',e=>{searchDiar=e.target.value.trim();renderDiarizado();});
document.getElementById('search-niveis').addEventListener('input',e=>{searchNiv=e.target.value.trim();renderNiveis();});
document.querySelectorAll('[data-col-n]').forEach(th=>th.addEventListener('click',()=>{
  const col=th.dataset.colN;
  sortDirN=sortColN===col?sortDirN*-1:-1;sortColN=col;
  document.querySelectorAll('[data-col-n]').forEach(t=>t.classList.remove('sorted-asc','sorted-desc'));
  th.classList.add(sortDirN===1?'sorted-asc':'sorted-desc');
  renderNiveis();
}));
document.querySelectorAll('[data-col-d]').forEach(th=>th.addEventListener('click',()=>{
  const col=th.dataset.colD;
  sortDirD=sortColD===col?sortDirD*-1:1;sortColD=col;
  document.querySelectorAll('[data-col-d]').forEach(t=>t.classList.remove('sorted-asc','sorted-desc'));
  th.classList.add(sortDirD===1?'sorted-asc':'sorted-desc');
  renderDiarizado();
}));

// ── SUBIDAS DE NÍVEL ──
const SUBIDAS_DETAIL = [{"reseller": "2087174154", "nivel_atual": "Top Empreendedor", "dt": "2026-04-27", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "1532390983", "nivel_atual": "Empreendedor", "dt": "2026-04-26", "transicao": "Especialista -> Empreendedor"}, {"reseller": "186371630", "nivel_atual": "Especialista", "dt": "2026-04-26", "transicao": "Aprendiz -> Especialista"}, {"reseller": "203850521", "nivel_atual": "Especialista", "dt": "2026-04-26", "transicao": "Aprendiz -> Especialista"}, {"reseller": "730679045", "nivel_atual": "Especialista", "dt": "2026-04-25", "transicao": "Aprendiz -> Especialista"}, {"reseller": "2619742737", "nivel_atual": "Especialista", "dt": "2026-04-24", "transicao": "Aprendiz -> Especialista"}, {"reseller": "2385034802", "nivel_atual": "Top Empreendedor", "dt": "2026-04-23", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "258795582", "nivel_atual": "-", "dt": "2026-04-23", "transicao": "Aprendiz -> Especialista"}, {"reseller": "72563541", "nivel_atual": "-", "dt": "2026-04-22", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1226761249", "nivel_atual": "Empreendedor", "dt": "2026-04-21", "transicao": "Especialista -> Empreendedor"}, {"reseller": "2176828104", "nivel_atual": "Top Empreendedor", "dt": "2026-04-21", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "153688180", "nivel_atual": "Empreendedor", "dt": "2026-04-21", "transicao": "Especialista -> Empreendedor"}, {"reseller": "1615066500", "nivel_atual": "Top Empreendedor", "dt": "2026-04-15", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "246343377", "nivel_atual": "Especialista", "dt": "2026-04-14", "transicao": "Aprendiz -> Especialista"}, {"reseller": "241572613", "nivel_atual": "Empreendedor", "dt": "2026-04-14", "transicao": "Especialista -> Empreendedor"}, {"reseller": "2445794092", "nivel_atual": "Empreendedor", "dt": "2026-04-12", "transicao": "Especialista -> Empreendedor"}, {"reseller": "2191289064", "nivel_atual": "Especialista", "dt": "2026-04-09", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1009968348", "nivel_atual": "Especialista", "dt": "2026-04-07", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1173220866", "nivel_atual": "-", "dt": "2026-04-06", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1339892065", "nivel_atual": "Especialista", "dt": "2026-04-02", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1388425394", "nivel_atual": "Empreendedor", "dt": "2026-03-31", "transicao": "Especialista -> Empreendedor"}, {"reseller": "20970977", "nivel_atual": "Especialista", "dt": "2026-03-31", "transicao": "Aprendiz -> Especialista"}, {"reseller": "149177824", "nivel_atual": "Empreendedor", "dt": "2026-03-29", "transicao": "Especialista -> Empreendedor"}, {"reseller": "42318297", "nivel_atual": "Top Empreendedor", "dt": "2026-03-24", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "241222977", "nivel_atual": "Top Empreendedor", "dt": "2026-03-17", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "2087174154", "nivel_atual": "Top Empreendedor", "dt": "2026-03-16", "transicao": "Especialista -> Empreendedor"}, {"reseller": "656772499", "nivel_atual": "Especialista", "dt": "2026-03-16", "transicao": "Aprendiz -> Especialista"}, {"reseller": "3140181270", "nivel_atual": "-", "dt": "2026-03-10", "transicao": "Especialista -> Empreendedor"}, {"reseller": "134179496", "nivel_atual": "Especialista", "dt": "2026-03-06", "transicao": "Aprendiz -> Especialista"}, {"reseller": "2445794092", "nivel_atual": "Empreendedor", "dt": "2026-03-05", "transicao": "Aprendiz -> Especialista"}, {"reseller": "42318297", "nivel_atual": "Top Empreendedor", "dt": "2026-03-01", "transicao": "Especialista -> Empreendedor"}, {"reseller": "1430493190", "nivel_atual": "Empreendedor", "dt": "2026-02-27", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "1226761249", "nivel_atual": "Empreendedor", "dt": "2026-02-26", "transicao": "Aprendiz -> Especialista"}, {"reseller": "242763116", "nivel_atual": "Empreendedor", "dt": "2026-02-25", "transicao": "Especialista -> Empreendedor"}, {"reseller": "1288797521", "nivel_atual": "Aprendiz", "dt": "2026-02-23", "transicao": "Aprendiz -> Especialista"}, {"reseller": "497552313", "nivel_atual": "Especialista", "dt": "2026-02-21", "transicao": "Aprendiz -> Especialista"}, {"reseller": "3118113625", "nivel_atual": "Especialista", "dt": "2026-02-19", "transicao": "Aprendiz -> Especialista"}, {"reseller": "3140181270", "nivel_atual": "-", "dt": "2026-02-17", "transicao": "Aprendiz -> Especialista"}, {"reseller": "3057984821", "nivel_atual": "Empreendedor", "dt": "2026-02-17", "transicao": "Especialista -> Empreendedor"}, {"reseller": "342576897", "nivel_atual": "Empreendedor", "dt": "2026-02-16", "transicao": "Especialista -> Empreendedor"}, {"reseller": "299222705", "nivel_atual": "Aprendiz", "dt": "2026-02-15", "transicao": "Aprendiz -> Especialista"}, {"reseller": "190822347", "nivel_atual": "Especialista", "dt": "2026-02-11", "transicao": "Aprendiz -> Especialista"}, {"reseller": "624974985", "nivel_atual": "Especialista", "dt": "2026-02-10", "transicao": "Aprendiz -> Especialista"}, {"reseller": "42318297", "nivel_atual": "Top Empreendedor", "dt": "2026-02-07", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1615066500", "nivel_atual": "Top Empreendedor", "dt": "2026-02-01", "transicao": "Aprendiz -> Especialista"}, {"reseller": "2176828104", "nivel_atual": "Top Empreendedor", "dt": "2026-02-01", "transicao": "Aprendiz -> Especialista"}, {"reseller": "2685466379", "nivel_atual": "-", "dt": "2026-02-01", "transicao": "Aprendiz -> Especialista"}, {"reseller": "2272438961", "nivel_atual": "Especialista", "dt": "2026-01-31", "transicao": "Aprendiz -> Especialista"}, {"reseller": "381728218", "nivel_atual": "Top Empreendedor", "dt": "2026-01-31", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "387319387", "nivel_atual": "Top Empreendedor", "dt": "2026-01-30", "transicao": "Empreendedor -> Top Empreendedor"}, {"reseller": "1532390983", "nivel_atual": "Empreendedor", "dt": "2026-01-30", "transicao": "Aprendiz -> Especialista"}, {"reseller": "149177824", "nivel_atual": "Empreendedor", "dt": "2026-01-25", "transicao": "Aprendiz -> Especialista"}, {"reseller": "438097380", "nivel_atual": "Empreendedor", "dt": "2026-01-22", "transicao": "Especialista -> Empreendedor"}, {"reseller": "3146784575", "nivel_atual": "Aprendiz", "dt": "2026-01-21", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1742983151", "nivel_atual": "Aprendiz", "dt": "2026-01-21", "transicao": "Aprendiz -> Especialista"}, {"reseller": "140888320", "nivel_atual": "Aprendiz", "dt": "2026-01-21", "transicao": "Aprendiz -> Especialista"}, {"reseller": "1615066500", "nivel_atual": "Top Empreendedor", "dt": "2026-01-21", "transicao": "Especialista -> Empreendedor"}, {"reseller": "2176828104", "nivel_atual": "Top Empreendedor", "dt": "2026-01-21", "transicao": "Especialista -> Empreendedor"}, {"reseller": "2685466379", "nivel_atual": "-", "dt": "2026-01-21", "transicao": "Especialista -> Empreendedor"}, {"reseller": "2599471034", "nivel_atual": "Especialista", "dt": "2026-01-19", "transicao": "Aprendiz -> Especialista"}, {"reseller": "3057984821", "nivel_atual": "Empreendedor", "dt": "2026-01-18", "transicao": "Aprendiz -> Especialista"}, {"reseller": "300594879", "nivel_atual": "Empreendedor", "dt": "2026-01-16", "transicao": "Especialista -> Empreendedor"}, {"reseller": "628247144", "nivel_atual": "Empreendedor", "dt": "2026-01-14", "transicao": "Especialista -> Empreendedor"}, {"reseller": "502170173", "nivel_atual": "Especialista", "dt": "2026-01-12", "transicao": "Aprendiz -> Especialista"}];

const TRANS_ORDER = ["Aprendiz -> Especialista","Especialista -> Empreendedor","Empreendedor -> Top Empreendedor"];
const TRANS_COLOR = {"Aprendiz -> Especialista":"#3b82f6","Especialista -> Empreendedor":"#f59e0b","Empreendedor -> Top Empreendedor":"#1A1F6B"};
const TRANS_LABEL = {"Aprendiz -> Especialista":"Aprendiz → Esp.","Especialista -> Empreendedor":"Esp. → Empreendedor","Empreendedor -> Top Empreendedor":"Empreendedor → Top"};
const MESES_NIVEIS = ["2026-01","2026-02","2026-03","2026-04"];
const MES_LABEL_N  = {"2026-01":"Jan/26","2026-02":"Fev/26","2026-03":"Mar/26","2026-04":"Abr/26"};
const NIV_COLOR_MAP = {"Aprendiz":"#9ca3af","Especialista":"#3b82f6","Empreendedor":"#f59e0b","Top Empreendedor":"#1A1F6B","—":"#ddd"};

let activeMesNiv=null, activeTransNiv=null, searchNiv='', sortColN='dt', sortDirN=-1, chartNiveis=null;

function getDataNiv(){
  let d=[...SUBIDAS_DETAIL];
  if(activeMesNiv) d=d.filter(r=>r.dt.startsWith(activeMesNiv));
  if(activeTransNiv) d=d.filter(r=>r.transicao===activeTransNiv);
  if(searchNiv) d=d.filter(r=>r.reseller.includes(searchNiv)||r.transicao.toLowerCase().includes(searchNiv.toLowerCase())||r.nivel_atual.toLowerCase().includes(searchNiv.toLowerCase()));
  d.sort((a,b)=>{
    const av=a[sortColN]||'', bv=b[sortColN]||'';
    return (typeof av==='string'?av.localeCompare(bv):av-bv)*sortDirN;
  });
  return d;
}

let chartNiveis2=null;
function renderNiveis(){
  const data=getDataNiv();
  const total=SUBIDAS_DETAIL.length;
  const totByTrans={};
  TRANS_ORDER.forEach(t=>totByTrans[t]=SUBIDAS_DETAIL.filter(r=>r.transicao===t).length);

  document.getElementById('cards-niveis').innerHTML=`
    <div class="card"><div class="card-label">Total Subidas</div><div class="card-value">${total}</div><div class="card-sub">Jan–Abr/26</div></div>
    ${TRANS_ORDER.map(t=>`<div class="card" style="border-left-color:${TRANS_COLOR[t]}">
      <div class="card-label" style="font-size:9px">${t.replace(' -> ',' → ')}</div>
      <div class="card-value" style="color:${TRANS_COLOR[t]}">${totByTrans[t]}</div>
      <div class="card-sub">Jan–Abr/26</div></div>`).join('')}`;

  // Tabela filtrada
  let html='';
  data.forEach(r=>{
    const cor=TRANS_COLOR[r.transicao]||'#999';
    const nc=NIV_COLOR_MAP[r.nivel_atual]||'#999';
    html+=`<tr>
      <td>${r.dt}</td>
      <td style="font-family:monospace;font-size:12px;color:#555">${r.reseller}</td>
      <td><span style="display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;background:${cor}22;color:${cor};border:1px solid ${cor}44">${r.transicao.replace(' -> ',' → ')}</span></td>
      <td><span class="nivel-badge"><span class="nivel-dot" style="background:${nc}"></span>${r.nivel_atual}</span></td>
    </tr>`;
  });
  document.getElementById('tbody-niveis').innerHTML=html||'<tr><td colspan="4" style="text-align:center;color:#ccc;padding:32px">Sem resultados</td></tr>';

  // Filtros
  document.getElementById('mes-filter-niveis').innerHTML=['Todos',...MESES_NIVEIS].map(m=>
    `<button class="filter-btn${(!activeMesNiv&&m==='Todos')||activeMesNiv===m?' active':''}" onclick="activeMesNiv='${m==='Todos'?'':m}';renderNiveis()">${m==='Todos'?'Todos':MES_LABEL_N[m]}</button>`).join('');
  document.getElementById('trans-filter-niveis').innerHTML=['Todos',...TRANS_ORDER].map(t=>
    `<button class="filter-btn${(!activeTransNiv&&t==='Todos')||activeTransNiv===t?' active':''}" onclick="activeTransNiv='${t==='Todos'?'':t}';renderNiveis()">${t==='Todos'?'Todos':TRANS_LABEL[t]}</button>`).join('');

  // Gráfico
  if(chartNiveis2)chartNiveis2.destroy();
  chartNiveis2=new Chart(document.getElementById('chartNiveis').getContext('2d'),{
    type:'bar',
    data:{labels:MESES_NIVEIS.map(m=>MES_LABEL_N[m]),
      datasets:TRANS_ORDER.map(t=>({label:t.replace(' -> ',' → '),
        data:MESES_NIVEIS.map(m=>SUBIDAS_DETAIL.filter(r=>r.transicao===t&&r.dt.startsWith(m)).length),
        backgroundColor:TRANS_COLOR[t],borderRadius:4}))},
    options:{responsive:true,plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
      tooltip:{mode:'index',intersect:false,callbacks:{label:i=>`${i.dataset.label}: ${i.raw}`,footer:items=>'TOTAL: '+items.reduce((s,i)=>s+(i.raw||0),0)}}},
      scales:{x:{grid:{display:false}},y:{ticks:{font:{size:11},stepSize:1},grid:{color:'#f0f0f0'}}}}
  });
}

renderCardTabela();renderFiltersTabela();renderTabela();
</script>
</body>
</html>"""

with open(r'C:\Users\daviaraujo\resellers-grid\index.html','w',encoding='utf-8') as f:
    f.write(html)
print('OK - arquivo gerado')
