from collections import deque
from src.models import Config,Pending
from src.part2_packet import serve_packet

def test_idle():assert serve_packet(deque(),0,Config())==(0,[])
def test_header_once():
    a=Pending(2,0,96,128);q=deque([a]);n,d=serve_packet(q,0,Config());assert n==128 and d==[a] and not q

def test_fifo_no_interleave():
    a,b=Pending(2,0,200,232),Pending(0,0,32,64);q=deque([a,b]);n,d=serve_packet(q,0,Config());assert n==128 and not d and a.remaining_wire_bits==104 and b.remaining_wire_bits==64
    n,d=serve_packet(q,1,Config());assert n==128 and d==[a] and b.remaining_wire_bits==40

def test_shared_capacity():
    a,b=Pending(3,0,16,48),Pending(3,0,16,48);q=deque([a,b]);n,d=serve_packet(q,0,Config());assert n==96 and d==[a,b]
