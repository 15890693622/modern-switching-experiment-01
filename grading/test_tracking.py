from grading.update_homework_tracking import build_rows,parse_grade,render,FIELDS,is_demo_pr

def pr():return {'number':1,'user':{'login':'demo'},'head':{'ref':'lab-DEMO01','sha':'abc'},'title':'实验01-DEMO01','updated_at':'2026-10-16','state':'open','html_url':'https://github.com/x/y/pull/1','commits':3}
def test_tracking_states():
    s=[{'序号':'1','学号':'DEMO01','姓名':'演示'}];p=pr()
    assert build_rows(s,[])[0]['评分状态']=='待提交'
    assert build_rows(s,[p])[0]['评分状态']=='未评分'
    p['parsed_grade']='65/100';r=build_rows(s,[p])[0];assert r['评分状态']=='已评分' and r['提交次数']=='3' and set(r)==set(FIELDS)
    assert '<!-- homework-tracker:managed -->' in render([r])
def test_comment_author_and_revision():
    c={'user':{'login':'student'},'body':'自动评分结果 总分: 70/100 <!-- graded-sha:abc -->'}
    assert parse_grade([c],'abc')=='';c['user']['login']='github-actions[bot]'
    assert parse_grade([c],'old')=='';assert parse_grade([c],'abc').startswith('70/100')
def test_login_priority():
    p=pr();assert build_rows([{'GitHub用户名':'other','学号':'DEMO01'}],[p])[0]['是否提交代码']=='否'

def test_latest_revision_replaces_old_score():
    comments=[{'user':{'login':'github-actions[bot]'},'body':'自动评分结果 总分: 5/100 <!-- graded-sha:old -->'},
              {'user':{'login':'github-actions[bot]'},'body':'自动评分结果 总分: 10/100 <!-- graded-sha:new -->'}]
    assert parse_grade(comments,'new').startswith('10/100')
    assert parse_grade(comments,'pending')==''

def test_teacher_demo_is_separate_from_real_students():
    p=pr();p['title']='[流程测试] 现代交换实验01-模拟学生-LAB01-DEMO-2026';p['head']['ref']='e2e-demo/LAB01-DEMO-2026'
    assert is_demo_pr(p)
    students=[{'学号':'DEMO01','GitHub用户名':'demo'}]
    assert build_rows(students,[x for x in [p] if not is_demo_pr(x)])[0]['是否提交代码']=='否'
    p['title']='普通学生提交';assert not is_demo_pr(p)
