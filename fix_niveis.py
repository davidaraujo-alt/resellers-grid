import csv, json, io

TRANS_MAP = {
    'Aprendiz': 'Aprendiz -> Especialista',
    'Especialista': 'Especialista -> Empreendedor',
    'Empreendedor': 'Empreendedor -> Top Empreendedor',
}

def fix_trans(t):
    for k, v in TRANS_MAP.items():
        if k in t and '->' not in t and 'Empreendedor' in t.split(k)[-1] if k != 'Empreendedor' else 'Top' in t:
            return v
    for k, v in TRANS_MAP.items():
        if t.startswith(k):
            return v
    return t

rows = []
with open(r'C:\Users\daviaraujo\resellers-grid\niveis_detail.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r.get('reseller','').isdigit():
            rows.append({
                'reseller': r['reseller'],
                'nivel_atual': r['nivel_atual'] or '-',
                'dt': r['dt'],
                'transicao': fix_trans(r['transicao'])
            })

with open(r'C:\Users\daviaraujo\resellers-grid\niveis_detail.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=True)

print(f'{len(rows)} rows saved')
print(rows[0])
print(rows[-1])
