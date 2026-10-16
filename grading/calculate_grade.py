"""自动70分 + 教师复核30分。JUnit是pytest内置格式，无额外插件。"""
import sys,subprocess,json,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_score(name,points):
    dest=ROOT/('.pytest-'+name+'.xml')
    try:
        r=subprocess.run([sys.executable,'-m','pytest',str(ROOT/'grading'/('test_'+name+'.py')),'-q','--junitxml='+str(dest)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60)
        output=r.stdout+'\n'+r.stderr
        (ROOT/('.pytest-'+name+'.log')).write_text(output,encoding='utf-8')
        if r.returncode not in (0,1):return dict(score=0,max=points,status='评分基础设施错误',detail=output[-1500:])
        cases=ET.parse(dest).findall('.//testcase')
        if not cases:return dict(score=0,max=points,status='未找到测试用例')
        passed=sum(not any(c.find(k) is not None for k in ('failure','error','skipped')) for c in cases)
        return dict(score=round(points*passed/len(cases),2),max=points,status=f'{passed}/{len(cases)} passed')
    except (subprocess.TimeoutExpired,ET.ParseError,OSError) as e:
        return dict(score=0,max=points,status='评分未完成',detail=str(e))

def artifacts():
    root=ROOT/'results';points=0;notes=[]
    try:
        obj=json.loads((root/'comparison.json').read_text(encoding='utf-8'))
        if len(obj['rows'])==8 and len(obj['traces'])==8:
            for raw in obj['traces'].values():
                assert raw['generated_payload_bits']==raw['delivered_payload_bits']+raw['dropped_payload_bits']+raw['backlog_payload_bits']
            points+=5
    except (OSError,ValueError,KeyError,TypeError,AssertionError):notes.append('缺少完整的8组结果或守恒不成立')
    names=('comparison_metrics.png','queue_occupancy.png','pcm_frame_view.png')
    if all((root/n).is_file() and (root/n).stat().st_size>1000 for n in names):points+=5
    else:notes.append('尚未生成全部3张结果图')
    return dict(score=points,max=10,status='；'.join(notes) or '结果齐全，内容仍需教师复核')

def main():
    sys.path.insert(0,str(ROOT));parts={}
    try:
        from src.test_environment import check
        check();parts['environment']=dict(score=5,max=5,status='pass')
    except Exception as e:parts['environment']=dict(score=0,max=5,status=str(e))
    for name,points in [('circuit',20),('packet',20),('metrics',15)]:parts[name]=test_score(name,points)
    parts['artifacts']=artifacts();score=round(sum(x['score'] for x in parts.values()),2)
    infrastructure=any(x['status'] in ('评分基础设施错误','未找到测试用例','评分未完成') for x in parts.values())
    report=dict(schema_version=1,automatic_score=score,automatic_max=70,manual_pending=30,parts=parts,status='infrastructure_error' if infrastructure else 'ok')
    (ROOT/'grade_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['自动评分结果',f'总分: {score}/100（自动项最高70分；教师复核30分待评，非最终成绩）']+[f'{k}: {v["score"]}/{v["max"]} {v["status"]}' for k,v in parts.items()]
    text='\n'.join(lines);print(text);(ROOT/'grade_result.txt').write_text(text,encoding='utf-8')
    return 2 if infrastructure else 0
if __name__=='__main__':sys.exit(main())
