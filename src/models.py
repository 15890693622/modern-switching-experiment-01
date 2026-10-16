"""教师提供的数据类型；时间以tick计，每tick可发送slot_bits个线速比特。"""
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class Config:
    users: int = 4
    ticks: int = 256
    slot_bits: int = 128
    tick_ms: float = 1.0
    header_bits: int = 32
    buffer_payload_bits: int = 4096
    def __post_init__(self):
        for name in ('users','ticks','slot_bits','buffer_payload_bits'):
            value=getattr(self,name)
            if isinstance(value,bool) or not isinstance(value,int) or value<=0:
                raise ValueError(name+' must be a positive integer')
        if isinstance(self.header_bits,bool) or not isinstance(self.header_bits,int) or self.header_bits<0:
            raise ValueError('header_bits must be a nonnegative integer')
        if self.tick_ms<=0:
            raise ValueError('tick_ms must be positive')

@dataclass(frozen=True)
class Arrival:
    tick: int
    user: int
    payload_bits: int

@dataclass
class Pending:
    user: int
    arrival_tick: int
    payload_bits: int
    remaining_wire_bits: int

def new_queues(users):
    return [deque() for _ in range(users)]
