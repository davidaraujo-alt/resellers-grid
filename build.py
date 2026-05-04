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
th span[title]{border-bottom:1px dotted #FFE600;padding:0 2px;font-size:10px}
.btn-export{padding:5px 14px;border-radius:20px;border:1.5px solid #1A1F6B;background:#fff;color:#1A1F6B;font-size:12px;font-weight:700;cursor:pointer;margin-left:auto}
.btn-export:hover{background:#1A1F6B;color:#FFE600}
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
  <div class="tab" onclick="showTab('aprendiz',this)">&#127891; Aprendiz &amp; Especialista</div>
</div>

<div class="body">

<div class="pane active" id="pane-tabela">

  <!-- Funil visual -->
  <div style="margin-bottom:24px">
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:14px">
      <div>
        <div style="font-size:10px;color:#999;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">Mês</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap" id="funil-mes-filter"></div>
      </div>
      <div>
        <div style="font-size:10px;color:#999;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">Nível</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap" id="funil-nivel-filter"></div>
      </div>
    </div>
    <div id="funil-visual"></div>
  </div>

  <div class="cards" id="cards-tabela"></div>
  <div class="controls">
    <div id="mes-filters" style="display:flex;gap:6px;flex-wrap:wrap"></div>
    <div id="nivel-filters" style="display:flex;gap:6px;flex-wrap:wrap"></div>
    <input class="search-box" type="text" placeholder="Buscar..." id="search-input"/>
    <button class="btn-export" onclick="exportCSV()">&#8595; CSV</button>
  </div>
  <div class="grid-wrapper">
    <table>
      <thead><tr>
        <th data-col="mes">Mês</th>
        <th data-col="nivel">Nível</th>
        <th data-col="resellers">Resellers <span title="Resellers com pelo menos 1 pedido de device no mês" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="pedidos">Dev. Pedidos <span title="Total de devices pedidos no mês" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="ativos">Dev. Ativos <span title="Devices ativados (com transação) no mês" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="tpv_m0">TPV M0 <span title="TPV dos sellers captados no mês (M0 = mês de entrada)" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="tpv_m1">TPV M1 <span title="TPV desses mesmos sellers no mês seguinte" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="tpv_total">TPV Total <span title="TPV total da carteira do reseller no mês (todos os sellers, todas as safras)" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="ticket">Ticket Médio <span title="TPV M0 ÷ Resellers com compra — qualidade média do novo reseller" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="mom_resellers">MoM Resellers <span title="Variação % vs mês anterior" style="cursor:help;opacity:.6">?</span></th>
        <th data-col="mom_tpv">MoM TPV M0 <span title="Variação % do TPV M0 vs mês anterior" style="cursor:help;opacity:.6">?</span></th>
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
  <!-- Funil mensal transposto -->
  <div style="font-size:16px;font-weight:900;color:#1A1F6B;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px;border-left:5px solid #FFE600;padding-left:14px">Funil Mensal</div>
  <div class="controls" style="margin-bottom:12px">
    <div id="nivel-filter-funil" style="display:flex;gap:6px;flex-wrap:wrap"></div>
  </div>
  <div style="overflow-x:auto;margin-bottom:28px">
    <table id="table-funil" style="min-width:500px">
      <thead><tr id="thead-funil-row"></tr></thead>
      <tbody id="tbody-funil"></tbody>
    </table>
  </div>

  <!-- TPV Diário transposto -->
  <div style="font-size:16px;font-weight:900;color:#1A1F6B;text-transform:uppercase;letter-spacing:.06em;margin:28px 0 14px;border-left:5px solid #009EE3;padding-left:14px">TPV Diário</div>
  <div style="background:#fff;border-radius:12px;padding:12px 18px;margin-bottom:14px;box-shadow:0 2px 8px rgba(0,0,0,.06)">
    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div>
        <div style="font-size:10px;color:#999;margin-bottom:6px">MÊS</div>
        <div id="mes-filter-tpv-dia" style="display:flex;gap:6px;flex-wrap:wrap"></div>
      </div>
      <div>
        <div style="font-size:10px;color:#999;margin-bottom:6px">NÍVEL</div>
        <div id="nivel-filter-tpv-dia" style="display:flex;gap:6px;flex-wrap:wrap"></div>
      </div>
    </div>
  </div>
  <div style="overflow-x:auto;margin-bottom:28px">
    <table style="min-width:600px">
      <thead><tr id="thead-tpv-dia-row"></tr></thead>
      <tbody id="tbody-tpv-dia"></tbody>
    </table>
  </div>

  <!-- Gráficos mensais -->
  <div style="font-size:16px;font-weight:900;color:#1A1F6B;text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px;border-left:5px solid #FFE600;padding-left:14px">Visão Mensal</div>
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

<!-- ── TAB APRENDIZ ── -->
<div class="pane" id="pane-aprendiz">
  <div style="font-size:18px;font-weight:900;color:#1A1F6B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:20px;border-left:5px solid #FFE600;padding-left:14px">Aprendiz — Distribuição de Devices</div>
  <div class="cards" id="cards-aprendiz"></div>
  <div class="grid-wrapper" style="margin-bottom:24px">
    <table>
      <thead><tr>
        <th>Mês</th>
        <th style="text-align:right">1 Device</th>
        <th style="text-align:right">2 Devices</th>
        <th style="text-align:right">3 Devices</th>
        <th style="text-align:right">4+ Devices</th>
        <th style="text-align:right">Total</th>
      </tr></thead>
      <tbody id="tbody-aprendiz"></tbody>
    </table>
  </div>
  <div class="chart-wrap">
    <div class="chart-title">Distribuição de Devices por Mês — Aprendiz</div>
    <div class="chart-sub">Quantidade de resellers Aprendiz por faixa de devices (acumulado no mês)</div>
    <canvas id="chartAprendiz"></canvas>
  </div>

  <!-- ESPECIALISTA -->
  <div style="font-size:18px;font-weight:900;color:#3b82f6;text-transform:uppercase;letter-spacing:.08em;margin:32px 0 20px;border-left:5px solid #3b82f6;padding-left:14px">Especialista — Distribuição de Devices</div>
  <div class="cards" id="cards-especialista"></div>
  <div class="grid-wrapper" style="margin-bottom:24px">
    <table>
      <thead><tr>
        <th>Mês</th>
        <th style="text-align:right">Até 4</th>
        <th style="text-align:right">5 a 10</th>
        <th style="text-align:right">11 a 15</th>
        <th style="text-align:right">20+</th>
        <th style="text-align:right">Total</th>
      </tr></thead>
      <tbody id="tbody-especialista"></tbody>
    </table>
  </div>
  <div class="chart-wrap">
    <div class="chart-title">Distribuição de Devices por Mês — Especialista</div>
    <div class="chart-sub">Quantidade de resellers Especialista por faixa de devices (acumulado no mês)</div>
    <canvas id="chartEspecialista"></canvas>
  </div>
</div>

</div>
<div class="footer">
  Mercado Pago · Programa Renda na Mão · Fonte: BD_CUST_RESELLER_INFO / BD_CUST_RESELLER_INFO_DAILY
  <span style="margin-left:16px;color:#bbb">&#128197; Última atualização: 04/05/2026 — TPV M0 corrigido</span>
</div>

<script>
const RAW = [
  {mes:"Jan/26",nivel:"Aprendiz",        resellers:914, pedidos:2884, ativos:2408, tpv_m0:5907164,  tpv_m1:null,      tpv_total:5907164,   pedidos_pro:2610, pedidos_smart:268, ativos_pro:2192, ativos_smart:211},
  {mes:"Jan/26",nivel:"Especialista",     resellers:113, pedidos:1397, ativos:1184, tpv_m0:3043182,  tpv_m1:null,      tpv_total:3043182,   pedidos_pro:1245, pedidos_smart:152, ativos_pro:1048, ativos_smart:136},
  {mes:"Jan/26",nivel:"Empreendedor",     resellers:50,  pedidos:938,  ativos:838,  tpv_m0:3138861,  tpv_m1:null,      tpv_total:3138861,   pedidos_pro:777,  pedidos_smart:161, ativos_pro:699,  ativos_smart:139},
  {mes:"Jan/26",nivel:"Top Empreendedor", resellers:38,  pedidos:1739, ativos:1656, tpv_m0:6646997,  tpv_m1:null,      tpv_total:6646997,   pedidos_pro:1273, pedidos_smart:466, ativos_pro:1213, ativos_smart:443},
  {mes:"Fev/26",nivel:"Aprendiz",        resellers:983, pedidos:2834, ativos:2177, tpv_m0:5641087,  tpv_m1:8592273,  tpv_total:14233360,  pedidos_pro:2576, pedidos_smart:257, ativos_pro:1998, ativos_smart:179},
  {mes:"Fev/26",nivel:"Especialista",     resellers:117, pedidos:1338, ativos:1126, tpv_m0:3643734,  tpv_m1:4613736,  tpv_total:8257469,   pedidos_pro:1216, pedidos_smart:122, ativos_pro:1038, ativos_smart:88},
  {mes:"Fev/26",nivel:"Empreendedor",     resellers:52,  pedidos:1246, ativos:1017, tpv_m0:2681090,  tpv_m1:4726280,  tpv_total:7407369,   pedidos_pro:1061, pedidos_smart:185, ativos_pro:869,  ativos_smart:148},
  {mes:"Fev/26",nivel:"Top Empreendedor", resellers:38,  pedidos:2111, ativos:1803, tpv_m0:6183877,  tpv_m1:12285399, tpv_total:18469277,  pedidos_pro:1331, pedidos_smart:780, ativos_pro:1140, ativos_smart:663},
  {mes:"Mar/26",nivel:"Aprendiz",        resellers:922, pedidos:2467, ativos:1553, tpv_m0:6655918,  tpv_m1:7923691,  tpv_total:22599539,  pedidos_pro:2163, pedidos_smart:301, ativos_pro:1362, ativos_smart:189},
  {mes:"Mar/26",nivel:"Especialista",     resellers:83,  pedidos:896,  ativos:548,  tpv_m0:3397338,  tpv_m1:4822342,  tpv_total:12453465,  pedidos_pro:802,  pedidos_smart:94,  ativos_pro:485,  ativos_smart:63},
  {mes:"Mar/26",nivel:"Empreendedor",     resellers:48,  pedidos:1341, ativos:884,  tpv_m0:4061846,  tpv_m1:5389169,  tpv_total:14354871,  pedidos_pro:1113, pedidos_smart:228, ativos_pro:738,  ativos_smart:146},
  {mes:"Mar/26",nivel:"Top Empreendedor", resellers:39,  pedidos:1966, ativos:1461, tpv_m0:7804816,  tpv_m1:11023520, tpv_total:30662581,  pedidos_pro:1510, pedidos_smart:456, ativos_pro:1147, ativos_smart:314},
  {mes:"Abr/26",nivel:"Aprendiz",        resellers:768, pedidos:1643, ativos:663,  tpv_m0:6296783,  tpv_m1:8248703,  tpv_total:29353889,  pedidos_pro:1443, pedidos_smart:194, ativos_pro:589,  ativos_smart:71},
  {mes:"Abr/26",nivel:"Especialista",     resellers:83,  pedidos:643,  ativos:232,  tpv_m0:3018150,  tpv_m1:4928603,  tpv_total:15786386,  pedidos_pro:518,  pedidos_smart:125, ativos_pro:193,  ativos_smart:39},
  {mes:"Abr/26",nivel:"Empreendedor",     resellers:38,  pedidos:630,  ativos:217,  tpv_m0:2605479,  tpv_m1:6136579,  tpv_total:17093142,  pedidos_pro:512,  pedidos_smart:118, ativos_pro:154,  ativos_smart:63},
  {mes:"Abr/26",nivel:"Top Empreendedor", resellers:44,  pedidos:2379, ativos:936,  tpv_m0:7409872,  tpv_m1:15294971, tpv_total:44996865,  pedidos_pro:1890, pedidos_smart:489, ativos_pro:750,  ativos_smart:186},
  {mes:"Mai/26",nivel:"Aprendiz",        resellers:9,   pedidos:20,   ativos:0,    tpv_m0:82158,    tpv_m1:709871,   tpv_total:2472188,   pedidos_pro:15,   pedidos_smart:5,   ativos_pro:0,    ativos_smart:0},
  {mes:"Mai/26",nivel:"Especialista",     resellers:1,   pedidos:2,    ativos:0,    tpv_m0:30454,    tpv_m1:408829,   tpv_total:1383201,   pedidos_pro:2,    pedidos_smart:0,   ativos_pro:0,    ativos_smart:0},
  {mes:"Mai/26",nivel:"Empreendedor",     resellers:2,   pedidos:15,   ativos:0,    tpv_m0:25784,    tpv_m1:456397,   tpv_total:1800006,   pedidos_pro:15,   pedidos_smart:0,   ativos_pro:0,    ativos_smart:0},
  {mes:"Mai/26",nivel:"Top Empreendedor", resellers:2,   pedidos:55,   ativos:0,    tpv_m0:46980,    tpv_m1:1074650,  tpv_total:3848387,   pedidos_pro:43,   pedidos_smart:12,  ativos_pro:0,    ativos_smart:0},
];

const DAILY = """ + daily_json + """;

const MES_ORDER=["Jan/26","Fev/26","Mar/26","Abr/26","Mai/26"];
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
  if(id==='aprendiz')renderAprendiz();
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

// MoM helper — busca valor do mês anterior para o mesmo nível
function getMoM(nivel, mes, field){
  const idx=MES_ORDER.indexOf(mes);
  if(idx<=0) return null;
  const prev=RAW.find(r=>r.mes===MES_ORDER[idx-1]&&r.nivel===nivel);
  return prev?prev[field]:null;
}
function momBadge(cur, prev){
  if(prev==null||prev===0) return '';
  const d=((cur-prev)/prev*100);
  const color=d>=0?'#16a34a':'#dc2626';
  const arrow=d>=0?'▲':'▼';
  return `<span style="font-size:10px;font-weight:700;color:${color};margin-left:4px">${arrow}${Math.abs(d).toFixed(1)}%</span>`;
}

function renderTabela(){
  const data=getData();
  let html='';
  data.forEach((r,i)=>{
    const isLast=i===data.length-1||data[i+1].mes!==r.mes;
    const t=totals[r.mes]||{};
    const bp=Math.round((r.tpv_m0/maxTPV)*100);
    const ticket=r.resellers?r.tpv_m0/r.resellers:0;
    const prevRes=getMoM(r.nivel,r.mes,'resellers');
    const prevTpv=getMoM(r.nivel,r.mes,'tpv_m0');
    html+=`<tr>
      <td><span class="mes-badge">${r.mes}</span></td>
      <td><span class="nivel-badge ${NIV_CLASS[r.nivel]||''}"><span class="nivel-dot"></span>${r.nivel}</span></td>
      <td>${fmtN(r.resellers)}${pct(r.resellers,t.resellers)}</td>
      <td>${fmtN(r.pedidos)}${pct(r.pedidos,t.pedidos)}</td>
      <td>${fmtN(r.ativos)}${pct(r.ativos,t.ativos)}</td>
      <td><div class="bar-cell">${fmt(r.tpv_m0)}${pct(r.tpv_m0,t.tpv_m0)}<div class="bar-bg"><div class="bar-fill" style="width:${bp}%"></div></div></div></td>
      <td>${fmt(r.tpv_m1)}${r.tpv_m1!=null&&t.haM1?pct(r.tpv_m1,t.tpv_m1):''}</td>
      <td>${fmt(r.tpv_total)}${pct(r.tpv_total,t.tpv_total)}</td>
      <td style="text-align:right">${ticket>=1e6?'R$ '+(ticket/1e6).toFixed(2).replace('.',',')+'M':'R$ '+fmtN(Math.round(ticket))}</td>
      <td style="text-align:center">${fmtN(r.resellers)}${momBadge(r.resellers,prevRes)}</td>
      <td style="text-align:center">${fmt(r.tpv_m0)}${momBadge(r.tpv_m0,prevTpv)}</td>
    </tr>`;
    if(isLast&&!activeMes&&!sortCol){
      const totTicket=t.resellers?t.tpv_m0/t.resellers:0;
      html+=`<tr class="group-total"><td><span class="mes-badge">${r.mes}</span></td><td style="font-size:11px">TOTAL</td>
        <td>${fmtN(t.resellers)}</td><td>${fmtN(t.pedidos)}</td><td>${fmtN(t.ativos)}</td>
        <td>${fmt(t.tpv_m0)}</td><td>${t.haM1?fmt(t.tpv_m1):fmt(null)}</td><td>${fmt(t.tpv_total)}</td>
        <td style="text-align:right">${totTicket>=1e6?'R$ '+(totTicket/1e6).toFixed(2).replace('.',',')+'M':'R$ '+fmtN(Math.round(totTicket))}</td>
        <td></td><td></td></tr>`;
    }
  });
  document.getElementById('tbody').innerHTML=html||'<tr><td colspan="11" style="text-align:center;color:#ccc;padding:32px">Sem resultados</td></tr>';
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

function exportCSV(){
  const data=getData();
  const header=['Mes','Nivel','Resellers','Dev.Pedidos','Dev.Ativos','TPV_M0','TPV_M1','TPV_Total','Ticket_Medio'];
  const rows=data.map(r=>[r.mes,r.nivel,r.resellers,r.pedidos,r.ativos,r.tpv_m0,r.tpv_m1||0,r.tpv_total,r.resellers?Math.round(r.tpv_m0/r.resellers):0].join(';'));
  const csv=[header.join(';'),...rows].join('\\n');
  const a=document.createElement('a');
  a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(csv);
  a.download='resellers_'+new Date().toISOString().slice(0,10)+'.csv';
  a.click();
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
const MES_PREFIX={"Jan/26":"2026-01","Fev/26":"2026-02","Mar/26":"2026-03","Abr/26":"2026-04","Mai/26":"2026-05"};
const PRIMEIRA_COMPRA={"2026-01-02":14,"2026-01-03":3,"2026-01-04":6,"2026-01-05":11,"2026-01-06":11,"2026-01-07":8,"2026-01-08":8,"2026-01-09":5,"2026-01-10":5,"2026-01-11":5,"2026-01-12":10,"2026-01-13":8,"2026-01-14":6,"2026-01-15":12,"2026-01-16":7,"2026-01-17":4,"2026-01-18":4,"2026-01-19":8,"2026-01-20":7,"2026-01-21":6,"2026-01-22":7,"2026-01-23":9,"2026-01-24":3,"2026-01-25":4,"2026-01-26":11,"2026-01-27":8,"2026-01-28":12,"2026-01-29":7,"2026-01-30":7,"2026-01-31":10,"2026-02-01":3,"2026-02-02":9,"2026-02-03":19,"2026-02-04":17,"2026-02-05":15,"2026-02-06":17,"2026-02-07":13,"2026-02-08":1,"2026-02-09":12,"2026-02-10":14,"2026-02-11":11,"2026-02-12":8,"2026-02-13":6,"2026-02-14":6,"2026-02-15":4,"2026-02-16":3,"2026-02-17":2,"2026-02-18":12,"2026-02-19":14,"2026-02-20":18,"2026-02-21":7,"2026-02-22":3,"2026-02-23":11,"2026-02-24":16,"2026-02-25":13,"2026-02-26":14,"2026-02-27":8,"2026-02-28":5,"2026-03-01":7,"2026-03-02":13,"2026-03-03":12,"2026-03-04":6,"2026-03-05":10,"2026-03-06":8,"2026-03-07":16,"2026-03-08":5,"2026-03-09":10,"2026-03-10":14,"2026-03-11":11,"2026-03-12":12,"2026-03-13":12,"2026-03-14":8,"2026-03-15":4,"2026-03-16":15,"2026-03-17":10,"2026-03-18":6,"2026-03-19":12,"2026-03-20":8,"2026-03-21":8,"2026-03-22":3,"2026-03-23":17,"2026-03-24":10,"2026-03-25":15,"2026-03-26":12,"2026-03-27":12,"2026-03-28":13,"2026-03-29":2,"2026-03-30":9,"2026-03-31":15,"2026-04-01":20,"2026-04-02":7,"2026-04-03":8,"2026-04-04":3,"2026-04-05":4,"2026-04-06":9,"2026-04-07":14,"2026-04-08":9,"2026-04-09":8,"2026-04-10":6,"2026-04-11":3,"2026-04-12":5,"2026-04-13":12,"2026-04-14":7,"2026-04-15":10,"2026-04-16":6,"2026-04-17":9,"2026-04-18":8,"2026-04-19":5,"2026-04-20":7,"2026-04-21":3,"2026-04-22":6,"2026-04-23":8,"2026-04-24":9,"2026-04-25":5,"2026-04-26":4,"2026-04-27":11,"2026-04-28":3};

let activeMesDiar=null,activeNivelDiar='Todos',searchDiar='',sortColD=null,sortDirD=1,funilActiveNivel='Todos',tpvDiaMes='Fev/26',tpvDiaNivel='Todos';

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

  // ── Funil mensal transposto ──
  const funilNivel=funilActiveNivel||'Todos';
  const funilData=MES_ORDER.map(m=>{
    const rows=RAW.filter(r=>r.mes===m&&(funilNivel==='Todos'||r.nivel===funilNivel));
    return {
      mes:m,
      pedidos:   rows.reduce((s,r)=>s+r.pedidos,0),
      ativos:    rows.reduce((s,r)=>s+r.ativos,0),
      tpv_m0:   rows.reduce((s,r)=>s+r.tpv_m0,0),
      tpv_m1:   rows.reduce((s,r)=>s+(r.tpv_m1||0),0),
      tpv_total:rows.reduce((s,r)=>s+r.tpv_total,0),
    };
  });

  const thFS='background:#1A1F6B;color:#FFE600;padding:10px 14px;font-size:11px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap;text-align:right';
  document.getElementById('thead-funil-row').innerHTML=
    `<th style="${thFS};text-align:left">Métrica</th>`+
    MES_ORDER.map(m=>`<th style="${thFS}">${m}</th>`).join('')+
    `<th style="${thFS};background:#FFE600;color:#1A1F6B;font-weight:900">TOTAL</th>`;

  function funilRow(label,nums,fmt,totFmt){
    const colors=colorScale(nums);
    const tot=nums.reduce((s,v)=>s+v,0);
    return `<tr>
      <td style="padding:10px 14px;font-weight:700;color:#1A1F6B;background:#f9f9ff;white-space:nowrap;font-size:12px;border-bottom:1px solid #f0f0f0">${label}</td>
      ${nums.map((v,i)=>`<td style="padding:10px 14px;text-align:right;font-size:12px;border-bottom:1px solid #f0f0f0;${colors[i]}">${fmt(v)}</td>`).join('')}
      <td style="padding:10px 14px;text-align:right;font-size:12px;border-bottom:1px solid #f0f0f0;background:#fffde7;font-weight:800;color:#1A1F6B">${totFmt?totFmt(tot):fmt(tot)}</td>
    </tr>`;
  }

  document.getElementById('tbody-funil').innerHTML=[
    funilRow('Pedidos de Device', funilData.map(r=>r.pedidos),   v=>fmtN(v)),
    funilRow('Devices Ativos',    funilData.map(r=>r.ativos),    v=>fmtN(v)),
    funilRow('TPV M0',            funilData.map(r=>r.tpv_m0),    v=>fmt(v),  _=>fmt(funilData.reduce((s,r)=>s+r.tpv_m0,0))),
    funilRow('TPV M1',            funilData.map(r=>r.tpv_m1),    v=>fmt(v),  _=>fmt(funilData.reduce((s,r)=>s+r.tpv_m1,0))),
    funilRow('TPV Total',         funilData.map(r=>r.tpv_total), v=>fmt(v),  _=>fmt(funilData.reduce((s,r)=>s+r.tpv_total,0))),
  ].join('');

  document.getElementById('nivel-filter-funil').innerHTML=['Todos',...NIV_ORDER].map(n=>
    `<button class="filter-btn${funilNivel===n?' active':''}" onclick="funilActiveNivel='${n}';renderDiarizado()">${n}</button>`).join('');

  // ── TPV Diário transposto ──
  const prefDiario=MES_PREFIX[tpvDiaMes]||'2026-02';
  const tpvDiaNiv=tpvDiaNivel;
  const diasTpv=[...new Set(DAILY.filter(d=>d.data.startsWith(prefDiario)).map(d=>d.data))].sort();
  const shortD=d=>d.slice(8)+'/'+d.slice(5,7);
  const thTD='background:#009EE3;color:#fff;padding:10px 12px;font-size:11px;text-transform:uppercase;white-space:nowrap;text-align:right';
  document.getElementById('thead-tpv-dia-row').innerHTML=
    `<th style="${thTD};text-align:left">Métrica</th>`+
    diasTpv.map(d=>`<th style="${thTD}">${shortD(d)}</th>`).join('')+
    `<th style="${thTD};background:#FFE600;color:#1A1F6B;font-weight:900">TOTAL</th>`;

  function tpvDiaRow(label,field){
    const vals=diasTpv.map(d=>{
      const rows=DAILY.filter(r=>r.data===d&&(tpvDiaNiv==='Todos'||r.nivel===tpvDiaNiv));
      return rows.reduce((s,r)=>s+(r[field]||0),0);
    });
    const colors=colorScale(vals);
    const tot=vals.reduce((s,v)=>s+v,0);
    return `<tr>
      <td style="padding:10px 12px;font-weight:700;color:#1A1F6B;background:#f9f9ff;white-space:nowrap;font-size:12px;border-bottom:1px solid #f0f0f0">${label}</td>
      ${vals.map((v,i)=>`<td style="padding:10px 12px;text-align:right;font-size:11px;border-bottom:1px solid #f0f0f0;${colors[i]}">${fmt(v)}</td>`).join('')}
      <td style="padding:10px 12px;text-align:right;font-size:11px;border-bottom:1px solid #f0f0f0;background:#fffde7;font-weight:800;color:#1A1F6B">${fmt(tot)}</td>
    </tr>`;
  }

  document.getElementById('tbody-tpv-dia').innerHTML=[
    tpvDiaRow('TPV M0',    'tpv_m0'),
    tpvDiaRow('TPV M1',    'tpv_m1'),
    tpvDiaRow('TPV Total', 'tpv_total'),
  ].join('');

  document.getElementById('mes-filter-tpv-dia').innerHTML=MES_ORDER.map(m=>
    `<button class="filter-btn${tpvDiaMes===m?' active':''}" onclick="tpvDiaMes='${m}';renderDiarizado()">${m}</button>`).join('');
  document.getElementById('nivel-filter-tpv-dia').innerHTML=['Todos',...NIV_ORDER].map(n=>
    `<button class="filter-btn${tpvDiaNivel===n?' active':''}" onclick="tpvDiaNivel='${n}';renderDiarizado()">${n}</button>`).join('');

  // Gráfico 1 — Cadastrados vs Convertidos por mês
  const mesesDiar=["Jan/26","Fev/26","Mar/26","Abr/26"];
  const prefDiar={"Jan/26":"2026-01","Fev/26":"2026-02","Mar/26":"2026-03","Abr/26":"2026-04","Mai/26":"2026-05"};
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
  const aprendizPrimeira=[213,282,313,235,7];
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

// ── APRENDIZ DEVICES ──
const APR_DEVICES = [
  {mes:"Jan/26", d1:133, d2:549, d3:3,  d4:229},
  {mes:"Fev/26", d1:166, d2:595, d3:0,  d4:222},
  {mes:"Mar/26", d1:159, d2:588, d3:5,  d4:170},
  {mes:"Abr/26", d1:241, d2:432, d3:0,  d4:95 },
  {mes:"Mai/26", d1:0,   d2:8,   d3:0,  d4:1  },
];
const DEV_COLORS = ["#e0e7ff","#6366f1","#1A1F6B","#FFE600"];

let chartAprendiz=null;
function renderAprendiz(){
  const pctFmt=(v,t)=>t?` (${(v/t*100).toFixed(1)}%)`:'';
  const tdA='padding:11px 16px;text-align:right;font-size:13px;border-bottom:1px solid #f0f0f0';

  let html='';
  APR_DEVICES.forEach(r=>{
    const total=r.d1+r.d2+r.d3+r.d4;
    html+=`<tr>
      <td><span class="mes-badge">${r.mes}</span></td>
      <td style="${tdA}">${fmtN(r.d1)}<span class="pct">${pctFmt(r.d1,total)}</span></td>
      <td style="${tdA}">${fmtN(r.d2)}<span class="pct">${pctFmt(r.d2,total)}</span></td>
      <td style="${tdA}">${r.d3||'—'}${r.d3?`<span class="pct">${pctFmt(r.d3,total)}</span>`:''}</td>
      <td style="${tdA}">${fmtN(r.d4)}<span class="pct">${pctFmt(r.d4,total)}</span></td>
      <td style="${tdA};font-weight:700;color:#1A1F6B">${fmtN(total)}</td>
    </tr>`;
  });
  document.getElementById('tbody-aprendiz').innerHTML=html;

  // Cards
  const totGeral=APR_DEVICES.reduce((s,r)=>s+r.d1+r.d2+r.d3+r.d4,0);
  document.getElementById('cards-aprendiz').innerHTML=`
    <div class="card"><div class="card-label">Total Aprendiz c/ Compra</div><div class="card-value">${fmtN(totGeral)}</div><div class="card-sub">Jan–Abr/26</div></div>
    <div class="card" style="border-left-color:#e0e7ff"><div class="card-label">1 Device</div><div class="card-value">${fmtN(APR_DEVICES.reduce((s,r)=>s+r.d1,0))}</div><div class="card-sub">${(APR_DEVICES.reduce((s,r)=>s+r.d1,0)/totGeral*100).toFixed(1)}% do total</div></div>
    <div class="card" style="border-left-color:#6366f1"><div class="card-label">2 Devices</div><div class="card-value">${fmtN(APR_DEVICES.reduce((s,r)=>s+r.d2,0))}</div><div class="card-sub">${(APR_DEVICES.reduce((s,r)=>s+r.d2,0)/totGeral*100).toFixed(1)}% do total</div></div>
    <div class="card" style="border-left-color:#1A1F6B"><div class="card-label">3 Devices</div><div class="card-value">${fmtN(APR_DEVICES.reduce((s,r)=>s+r.d3,0))}</div><div class="card-sub">${(APR_DEVICES.reduce((s,r)=>s+r.d3,0)/totGeral*100).toFixed(1)}% do total</div></div>
    <div class="card" style="border-left-color:#FFE600"><div class="card-label">4+ Devices</div><div class="card-value">${fmtN(APR_DEVICES.reduce((s,r)=>s+r.d4,0))}</div><div class="card-sub">${(APR_DEVICES.reduce((s,r)=>s+r.d4,0)/totGeral*100).toFixed(1)}% do total</div></div>`;

  // Gráfico empilhado
  renderEspecialista();
  if(chartAprendiz)chartAprendiz.destroy();
  chartAprendiz=new Chart(document.getElementById('chartAprendiz').getContext('2d'),{
    type:'bar',
    data:{labels:APR_DEVICES.map(r=>r.mes),datasets:[
      {label:'1 Device', data:APR_DEVICES.map(r=>r.d1),backgroundColor:'#fed7aa',borderRadius:0},
      {label:'2 Devices',data:APR_DEVICES.map(r=>r.d2),backgroundColor:'#fb923c',borderRadius:0},
      {label:'3 Devices',data:APR_DEVICES.map(r=>r.d3),backgroundColor:'#ea580c',borderRadius:0},
      {label:'4+ Devices',data:APR_DEVICES.map(r=>r.d4),backgroundColor:'#9a3412',borderRadius:4},
    ]},
    options:{responsive:true,plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
      tooltip:{mode:'index',intersect:false,callbacks:{
        label:i=>`${i.dataset.label}: ${fmtN(i.raw)}`,
        footer:items=>'TOTAL: '+fmtN(items.reduce((s,i)=>s+(i.raw||0),0))
      }}},
      scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,ticks:{font:{size:10}},grid:{color:'#f0f0f0'}}}}
  });
}

// ── ESPECIALISTA DEVICES ──
const ESP_DEVICES = [
  {mes:"Jan/26", d4:37, d10:50, d15:10, d20:16},
  {mes:"Fev/26", d4:37, d10:38, d15:14, d20:28},
  {mes:"Mar/26", d4:27, d10:33, d15:9,  d20:14},
  {mes:"Abr/26", d4:39, d10:29, d15:9,  d20:6 },
  {mes:"Mai/26", d4:1,  d10:0,  d15:0,  d20:0 },
];
const ESP_COLORS = ["#dbeafe","#93c5fd","#3b82f6","#1e3a8a"];

function renderEspecialista(){
  const pctFmt=(v,t)=>t?` (${(v/t*100).toFixed(1)}%)`:'';
  const tdE='padding:11px 16px;text-align:right;font-size:13px;border-bottom:1px solid #f0f0f0';

  let html='';
  ESP_DEVICES.forEach(r=>{
    const total=r.d4+r.d10+r.d15+r.d20;
    html+=`<tr>
      <td><span class="mes-badge">${r.mes}</span></td>
      <td style="${tdE}">${fmtN(r.d4)}<span class="pct">${pctFmt(r.d4,total)}</span></td>
      <td style="${tdE}">${fmtN(r.d10)}<span class="pct">${pctFmt(r.d10,total)}</span></td>
      <td style="${tdE}">${fmtN(r.d15)}<span class="pct">${pctFmt(r.d15,total)}</span></td>
      <td style="${tdE}">${fmtN(r.d20)}<span class="pct">${pctFmt(r.d20,total)}</span></td>
      <td style="${tdE};font-weight:700;color:#3b82f6">${fmtN(total)}</td>
    </tr>`;
  });
  document.getElementById('tbody-especialista').innerHTML=html;

  const totG=ESP_DEVICES.reduce((s,r)=>s+r.d4+r.d10+r.d15+r.d20,0);
  document.getElementById('cards-especialista').innerHTML=`
    <div class="card" style="border-left-color:#3b82f6"><div class="card-label">Total Especialista c/ Compra</div><div class="card-value" style="color:#3b82f6">${fmtN(totG)}</div><div class="card-sub">Jan–Abr/26</div></div>
    <div class="card" style="border-left-color:#dbeafe"><div class="card-label">Até 4 devices</div><div class="card-value">${fmtN(ESP_DEVICES.reduce((s,r)=>s+r.d4,0))}</div><div class="card-sub">${(ESP_DEVICES.reduce((s,r)=>s+r.d4,0)/totG*100).toFixed(1)}% do total</div></div>
    <div class="card" style="border-left-color:#93c5fd"><div class="card-label">5 a 10 devices</div><div class="card-value">${fmtN(ESP_DEVICES.reduce((s,r)=>s+r.d10,0))}</div><div class="card-sub">${(ESP_DEVICES.reduce((s,r)=>s+r.d10,0)/totG*100).toFixed(1)}% do total</div></div>
    <div class="card" style="border-left-color:#3b82f6"><div class="card-label">11 a 15 devices</div><div class="card-value">${fmtN(ESP_DEVICES.reduce((s,r)=>s+r.d15,0))}</div><div class="card-sub">${(ESP_DEVICES.reduce((s,r)=>s+r.d15,0)/totG*100).toFixed(1)}% do total</div></div>
    <div class="card" style="border-left-color:#1e3a8a"><div class="card-label">20+ devices</div><div class="card-value">${fmtN(ESP_DEVICES.reduce((s,r)=>s+r.d20,0))}</div><div class="card-sub">${(ESP_DEVICES.reduce((s,r)=>s+r.d20,0)/totG*100).toFixed(1)}% do total</div></div>`;

  const existingE=Chart.getChart('chartEspecialista');if(existingE)existingE.destroy();
  new Chart(document.getElementById('chartEspecialista').getContext('2d'),{
    type:'bar',
    data:{labels:ESP_DEVICES.map(r=>r.mes),datasets:[
      {label:'Até 4',   data:ESP_DEVICES.map(r=>r.d4), backgroundColor:'#dbeafe',borderRadius:0},
      {label:'5 a 10',  data:ESP_DEVICES.map(r=>r.d10),backgroundColor:'#93c5fd',borderRadius:0},
      {label:'11 a 15', data:ESP_DEVICES.map(r=>r.d15),backgroundColor:'#3b82f6',borderRadius:0},
      {label:'20+',     data:ESP_DEVICES.map(r=>r.d20),backgroundColor:'#1e3a8a',borderRadius:4},
    ]},
    options:{responsive:true,plugins:{legend:{position:'top',labels:{font:{size:11},usePointStyle:true}},
      tooltip:{mode:'index',intersect:false,callbacks:{
        label:i=>`${i.dataset.label}: ${fmtN(i.raw)}`,
        footer:items=>'TOTAL: '+fmtN(items.reduce((s,i)=>s+(i.raw||0),0))
      }}},
      scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,ticks:{font:{size:10}},grid:{color:'#f0f0f0'}}}}
  });
}

// ── FUNIL ABA 1 ──
let funilMesTab = 'Todos', funilNivelTab = 'Todos';

function renderFunilTab(){
  const rows = RAW
    .filter(r => funilMesTab === 'Todos' || r.mes === funilMesTab)
    .filter(r => funilNivelTab === 'Todos' || r.nivel === funilNivelTab);

  const pedidos  = rows.reduce((s,r) => s + r.pedidos, 0);
  const ativos   = rows.reduce((s,r) => s + r.ativos, 0);
  const tpvM0    = rows.reduce((s,r) => s + r.tpv_m0, 0);
  const pctAtiv  = pedidos ? (ativos/pedidos*100).toFixed(1) : 0;

  const tpvFmt = v => v>=1e6 ? 'R$ '+(v/1e6).toFixed(2).replace('.',',')+'M' : 'R$ '+fmtN(v);

  const funnelStage = (pct, bg, textColor, label, value, sub, connector) => {
    const margin = (100 - pct) / 2;
    return `
      <div style="width:100%;display:flex;flex-direction:column;align-items:center">
        <div style="width:${pct}%;background:${bg};padding:18px 20px;text-align:center;
          clip-path:polygon(5% 0%,95% 0%,100% 100%,0% 100%);margin:0 auto">
          <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:${textColor}99;margin-bottom:4px">${label}</div>
          <div style="font-size:22px;font-weight:900;color:${textColor};line-height:1.1">${value}</div>
          ${sub?`<div style="font-size:11px;color:${textColor}88;margin-top:3px">${sub}</div>`:''}
        </div>
        ${connector?`<div style="font-size:11px;color:#999;font-weight:700;padding:6px 0;letter-spacing:.04em">${connector}</div>`:''}
      </div>`;
  };

  document.getElementById('funil-visual').innerHTML =
    `<div style="width:100%;max-width:520px;margin:0 auto;display:flex;flex-direction:column;align-items:center">` +
    funnelStage(100, '#1A1F6B', '#ffffff', 'Devices Pedidos', fmtN(pedidos),  funilMesTab==='Todos'?'Jan–Abr/26':funilMesTab, `${pctAtiv}% foram ativados ▼`) +
    funnelStage(78,  '#FFE600', '#1A1F6B', 'Devices Ativos',  fmtN(ativos),  `${pctAtiv}% dos pedidos`, `TPV dos sellers M0 ▼`) +
    funnelStage(58,  '#009EE3', '#ffffff', 'TPV M0',          tpvFmt(tpvM0), 'sellers captados no mês', '') +
    `</div>`;

  document.getElementById('funil-mes-filter').innerHTML =
    ['Todos', ...MES_ORDER].map(m =>
      `<button class="filter-btn${funilMesTab===m?' active':''}" onclick="funilMesTab='${m}';renderFunilTab()">${m}</button>`
    ).join('');
  document.getElementById('funil-nivel-filter').innerHTML =
    ['Todos', ...NIV_ORDER].map(n =>
      `<button class="filter-btn${funilNivelTab===n?' active':''}" onclick="funilNivelTab='${n}';renderFunilTab()">${n}</button>`
    ).join('');
}

try {
  renderCardTabela();renderFiltersTabela();renderTabela();renderFunilTab();
} catch(e) {
  document.body.innerHTML = '<div style="padding:40px;font-family:monospace;color:red;background:#fff"><h2>Erro JS detectado:</h2><pre>'+e.message+'\\n'+e.stack+'</pre></div>';
}
</script>
</body>
</html>"""

with open(r'C:\Users\daviaraujo\resellers-grid\index.html','w',encoding='utf-8') as f:
    f.write(html)
print('OK - arquivo gerado')
