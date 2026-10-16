from collections import deque
from src.models import Config,Pending
from src.part1_circuit import serve_circuit

def p(user,bits):return Pending(user,0,bits,bits)
def test_idle():
    q=[deque(),deque()];assert serve_circuit(q,0,Config(users=2))==(0,[])
def test_reserved_user_only():
    a=p(1,32);q=[deque(),deque([a])];assert serve_circuit(q,0,Config(users=2))==(0,[]);assert len(q[1])==1
    n,done=serve_circuit(q,1,Config(users=2));assert n==32 and done==[a] and not q[1]
def test_partial():
    a=p(0,200);q=[deque([a])];n,d=serve_circuit(q,0,Config(users=1));assert n==128 and d==[] and a.remaining_wire_bits==72
    n,d=serve_circuit(q,1,Config(users=1));assert n==72 and d==[a]
def test_fifo_budget():
    a,b=p(0,32),p(0,200);q=[deque([a,b])];n,d=serve_circuit(q,0,Config(users=1));assert n==128 and d==[a] and b.remaining_wire_bits==104
