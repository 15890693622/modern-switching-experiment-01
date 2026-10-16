"""可信分支运行；不执行学生代码。真实名单本地保留，云端输出匿名化。"""
import csv,json,os,re,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS=['序号','学号','姓名','GitHub用户名','是否提交代码','PR数量','提交次数','最新PR','最新PR状态','最新评分','评分状态','最近提交时间','备注']
MARKER='<!-- homework-tracker:managed -->'
def api(path,method='GET',data=None):
    req=urllib.request.Request('https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']+path,
        data=None if data is None else json.dumps(data).encode(),method=method,
        headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as f:return json.load(f)
def pages(path):
    out=[];page=1
    while True:
        a=api(path+('&' if '?' in path else '?')+f'per_page=100&page={page}');out.extend(a)
        if len(a)<100:return out
        page+=1
def match(student,prs):
    login=student.get('GitHub用户名','').lstrip('@').lower();sid=student.get('学号','');name=student.get('姓名','')
    if login:return [p for p in prs if p['user']['login'].lower()==login]
    bybranch=[p for p in prs if sid and sid in p['head']['ref']]
    if bybranch:return bybranch
    byid=[p for p in prs if sid and sid in p['title']]
    if byid:return byid
    return [p for p in prs if name and name in p['title']]
def parse_grade(comments,sha):
    result=''
    for c in comments:
        if c.get('user',{}).get('login')!='github-actions[bot]':continue
        body=c.get('body','')
        if '自动评分结果' not in body or '<!-- graded-sha:'+sha+' -->' not in body:continue
        m=re.search(r'总分[:：]\s*(\d+(?:\.\d+)?)/100',body)
        if m and 0<=float(m[1])<=70:result=m[1]+'/100（自动70，人工待评）'
    return result

def build_rows(students,prs):
    rows=[]
    for s in students:
        matches=sorted(match(s,prs),key=lambda p:p.get('updated_at',''),reverse=True);p=matches[0] if matches else None
        row={k:'' for k in FIELDS};row.update({k:s.get(k,'') for k in ('序号','学号','姓名','GitHub用户名','备注')})
        row.update({'是否提交代码':'是' if p else '否','PR数量':str(len(matches)),'提交次数':str(sum(int(x.get('commits',0)) for x in matches)),
                    '评分状态':'已评分' if p and p.get('parsed_grade') else ('未评分' if p else '待提交')})
        if p:row.update({'最新PR':p.get('html_url',''),'最新PR状态':'merged' if p.get('merged_at') else p['state'],'最新评分':p.get('parsed_grade',''),'最近提交时间':p['updated_at']})
        rows.append(row)
    return rows

def render(rows,live=False):
    lines=[MARKER,'# 现代交换实验01作业实时跟踪表','',f'- 学生总数：{len(rows)}',f'- 已提交代码：{sum(r["是否提交代码"]=="是" for r in rows)}',f'- 已获得自动评分：{sum(r["评分状态"]=="已评分" for r in rows)}',
           '- 数据模式：'+('GitHub查询' if live else '本地待提交基线，未查询GitHub'),'', '| '+' | '.join(FIELDS)+' |','| '+' | '.join(['---']*len(FIELDS))+' |']
    for r in rows:lines.append('| '+' | '.join(str(r.get(k,'')).replace('|','/').replace('\n',' ') for k in FIELDS)+' |')
    return '\n'.join(lines)+'\n'

def main():
    live=bool(os.getenv('GITHUB_TOKEN') and os.getenv('GITHUB_REPOSITORY'));prs=[]
    if live:
        prs=pages('/pulls?state=all&sort=updated&direction=desc')
        for p in prs:
            detail=api('/pulls/'+str(p['number']));p['commits']=detail['commits'];p['head']=detail['head']
            p['parsed_grade']=parse_grade(pages('/issues/'+str(p['number'])+'/comments'),p['head']['sha'])
    roster=ROOT/'course_management/students.csv'
    if roster.exists():
        with roster.open(encoding='utf-8-sig',newline='') as f:students=list(csv.DictReader(f))
    elif live:
        logins=sorted({p['user']['login'] for p in prs});students=[{'序号':str(i+1),'GitHub用户名':u} for i,u in enumerate(logins)]
    else:students=[]
    rows=build_rows(students,prs)
    if os.getenv('GITHUB_ACTIONS')=='true':
        for r in rows:r['学号']='';r['姓名']='';r['备注']=''
    out=ROOT/'course_management';out.mkdir(exist_ok=True)
    with (out/'homework_tracking.csv').open('w',encoding='utf-8-sig',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=FIELDS);wr.writeheader();wr.writerows(rows)
    text=render(rows,live);(out/'HOMEWORK_TRACKING.md').write_text(text,encoding='utf-8')
    if os.getenv('GITHUB_STEP_SUMMARY'):Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(text,encoding='utf-8')
    number=os.getenv('TRACKING_ISSUE_NUMBER','')
    if live and number:
        try:
            comments=pages('/issues/'+str(int(number))+'/comments')
            old=next((c for c in comments if c.get('user',{}).get('login')=='github-actions[bot]' and MARKER in c.get('body','')),None)
            api('/issues/comments/'+str(old['id']) if old else '/issues/'+str(int(number))+'/comments','PATCH' if old else 'POST',{'body':text})
        except Exception as e:print('Issue更新未完成，Summary和Artifact仍可用：'+type(e).__name__)
    print('Tracking rows:',len(rows),'live:',live)
if __name__=='__main__':main()
