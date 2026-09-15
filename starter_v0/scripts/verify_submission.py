"""Offline submission audit: real evidence, links, artifact hashes and excluded files."""
from __future__ import annotations
import csv,hashlib,json,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'starter_v0'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def check():
    checked=[]
    def require(ok,label):
        if not ok:raise AssertionError(label)
        checked.append(label)
    for file in ['TEAM.md','README.md','starter_v0/artifacts/REPORT.md','starter_v0/artifacts/system_prompt.md','starter_v0/artifacts/tools.yaml','starter_v0/artifacts/version_log.csv','starter_v0/ui_server.py','starter_v0/chat_runtime.py','starter_v0/ui/index.html']:
        require((ROOT/file).is_file(),'Required file: '+file)
    for suite,number,multi in [('base',30,10),('adversarial',12,2),('group',10,5)]:
        p=LAB/'data'/('eval_'+suite+'.json');d=json.loads(p.read_text())
        require(len(d['cases'])==number and sum('turns' in c for c in d['cases'])==multi,'Dataset counts: '+suite)
        revision='f703a98' if suite=='group' else 'cb20072'
        frozen=subprocess.check_output(['git','show',revision+':'+str(p.relative_to(ROOT))],cwd=ROOT)
        require(hashlib.sha256(frozen).hexdigest()==sha(p),'Frozen dataset unchanged: '+suite)
    rows=list(csv.DictReader((LAB/'artifacts/version_log.csv').open()))
    require([x['version'] for x in rows]==['v0','v1','v2','v3'],'Four ordered versions in log')
    for row,commit in zip(rows,['cb20072','186faee','99321c2','6eaaf8c']):
        d=json.loads((LAB/row['run_file']).read_text());summary=d['summary']
        require(summary['total_cases']==summary['measured_cases']==30 and summary['provider_error_cases']==0,'Valid base run: '+row['version'])
        require(float(row['metric_after'])==summary['case_accuracy'],'CSV metric: '+row['version'])
        for field,file in [('prompt_hash','system_prompt.md'),('tools_hash','tools.yaml')]:
            raw=subprocess.check_output(['git','show',commit+':starter_v0/artifacts/'+file],cwd=ROOT)
            require(hashlib.sha256(raw).hexdigest()==d[field]==row[field],'Commit/artifact hash: '+row['version']+'/'+file)
    for suite,n in [('adversarial',12),('group',10)]:
        d=json.loads(sorted((LAB/'runs').glob('v3_B_'+suite+'_*.json'))[-1].read_text())
        require(d['summary']['total_cases']==d['summary']['measured_cases']==n and d['summary']['provider_error_cases']==0,'Valid '+suite+' run')
    m=json.loads((LAB/'artifacts/analysis/ui_demo_manifest.json').read_text())
    require(len(m['scenarios'])==5,'Five live demo scenarios')
    for scenario in m['scenarios']:
        d=json.loads((LAB/scenario['transcript']).read_text())
        require(bool(d['turns']) and all(t['status']!='provider_error' for t in d['turns']),'Live transcript: '+scenario['scenario'])
        require(d['runtime_code_hash']==sha(LAB/'chat_runtime.py'),'Runtime hash: '+scenario['scenario'])
    for doc in ['TEAM.md','README.md','starter_v0/artifacts/REPORT.md']:
        p=ROOT/doc
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('http://','https://','#')):continue
            require((p.parent/target.split('#')[0]).exists(),'Local link: '+doc+' -> '+target)
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    prohibited=re.compile(r'(^|/)(\.env|\.venv|__pycache__|tickets)(/|$)|\.pyc$')
    require(not any(prohibited.search(f) for f in tracked),'No forbidden tracked files')
    secret=re.compile(rb'(?:sk-(?:proj-|or-v1-)?[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
    for file in tracked:
        p=ROOT/file
        if p.is_file():require(not secret.search(p.read_bytes()),'No credential pattern: '+file)
    return {'checked_at':datetime.now(timezone.utc).isoformat(),'status':'passed','checks':len(checked),'details':checked,'limitations':'Pattern scan cannot prove absence of every possible secret. Synthetic adversarial fixtures retained; no new live API calls made.'}
if __name__=='__main__':
    result=check();out=LAB/'artifacts/analysis/final_submission_check.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(f"PASS: {result['checks']} checks; {out}")
