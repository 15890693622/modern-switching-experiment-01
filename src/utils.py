"""教师提供：一致的业务、缓存准入、时钟和仿真框架。"""
from collections import deque
from dataclasses import asdict
import random
from .models import Arrival, Pending, Config, new_queues

def make_traffic(scenario,cfg,seed=2026):
    if scenario=='continuous':
        return [Arrival(t,u,128) for t in range(0,cfg.ticks,cfg.users) for u in range(cfg.users)]
    if scenario=='staggered_burst':
        return [Arrival(t,(t//64)%cfg.users,96) for t in range(cfg.ticks)]
    if scenario=='synchronized_burst':
        return [Arrival(t,u,96) for t in range(0,cfg.ticks,80) for u in range(cfg.users) for _ in range(8)]
    if scenario=='light_random':
        rng=random.Random(seed)
        return [Arrival(t,u,96) for t in range(cfg.ticks) for u in range(cfg.users) if rng.random()<0.08]
    raise ValueError('unknown traffic scenario: '+scenario)

def simulate(arrivals,cfg,mode,service=None):
    if mode not in ('circuit','packet'): raise ValueError('mode')
    if service is None:
        if mode=='circuit':
            from .part1_circuit import serve_circuit as service
        else:
            from .part2_packet import serve_packet as service
    arrivals=list(arrivals);events={}
    for a in arrivals:
        if not isinstance(a,Arrival) or any(isinstance(v,bool) or not isinstance(v,int) for v in (a.tick,a.user,a.payload_bits)):
            raise ValueError('arrival fields must be integers')
        if not (0<=a.tick<cfg.ticks and 0<=a.user<cfg.users and a.payload_bits>0):raise ValueError('invalid arrival')
        events.setdefault(a.tick,[]).append(a)
    queues=new_queues(cfg.users) if mode=='circuit' else deque()
    raw=dict(generated_payload_bits=0,delivered_payload_bits=0,dropped_payload_bits=0,
             backlog_payload_bits=0,wire_sent_bits=0,completed=[],trace=[])
    reserved=0
    for tick in range(cfg.ticks):
        for a in events.get(tick,[]):
            raw['generated_payload_bits']+=a.payload_bits
            # 两模型均按“未完成记录的原始payload”占据同样的总缓存，包含在传记录。
            if reserved+a.payload_bits>cfg.buffer_payload_bits:
                raw['dropped_payload_bits']+=a.payload_bits;continue
            rec=Pending(a.user,a.tick,a.payload_bits,a.payload_bits+(cfg.header_bits if mode=='packet' else 0))
            (queues[a.user] if mode=='circuit' else queues).append(rec)
            reserved+=a.payload_bits
        wire,done=service(queues,tick,cfg)
        if not isinstance(wire,int) or not 0<=wire<=cfg.slot_bits:raise ValueError('service exceeded link budget')
        raw['wire_sent_bits']+=wire
        for rec in done:
            if rec.remaining_wire_bits!=0:raise ValueError('incomplete record reported as delivered')
            reserved-=rec.payload_bits
            raw['delivered_payload_bits']+=rec.payload_bits
            raw['completed'].append(dict(user=rec.user,payload_bits=rec.payload_bits,delay_ticks=tick+1-rec.arrival_tick))
        if reserved<0:raise ValueError('negative buffer occupancy')
        raw['trace'].append(dict(tick=tick,wire_bits=wire,buffer_payload_bits=reserved))
    raw['backlog_payload_bits']=reserved
    return raw

def pack_pcm(channels,slot_map,idle_code=255):
    """预置PCM工具：四路比较仿真与32时隙PCM不是同一个速率模型。"""
    import numpy as np
    a=np.asarray(channels)
    if a.ndim!=2 or a.shape[1]!=len(slot_map) or not np.issubdtype(a.dtype,np.integer) or np.any((a<0)|(a>255)):
        raise ValueError('channels must be integer byte matrix matching slot_map')
    if len(set(slot_map))!=len(slot_map) or any(not isinstance(s,int) or s in (0,16) or not 0<=s<32 for s in slot_map):
        raise ValueError('invalid slot_map')
    if not isinstance(idle_code,int) or not 0<=idle_code<=255:raise ValueError('idle_code')
    frames=np.full((len(a),32),idle_code,dtype=np.uint8)
    frames[:,slot_map]=a
    return frames
