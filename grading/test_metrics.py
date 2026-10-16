import pytest
from src.models import Config
from src.metrics import summarize

def raw():return dict(generated_payload_bits=400,delivered_payload_bits=200,dropped_payload_bits=100,backlog_payload_bits=100,wire_sent_bits=320,completed=[dict(user=0,payload_bits=100,delay_ticks=1),dict(user=1,payload_bits=100,delay_ticks=3)])
def test_exact():
    r=summarize(raw(),Config(ticks=10,slot_bits=64,tick_ms=2));assert r['payload_utilization']==pytest.approx(200/640);assert r['wire_utilization']==pytest.approx(.5);assert r['mean_delay_ms']==4 and r['max_delay_ms']==6;assert r['loss_ratio']==.25;assert r['backlog_payload_bits']==100

def test_empty():
    a=raw();a.update(generated_payload_bits=0,delivered_payload_bits=0,dropped_payload_bits=0,backlog_payload_bits=0,wire_sent_bits=0,completed=[])
    r=summarize(a,Config());assert r['mean_delay_ms'] is None and r['max_delay_ms'] is None and r['loss_ratio']==0 and r['payload_utilization']==0

def test_conservation():
    a=raw();a['backlog_payload_bits']=99
    with pytest.raises(ValueError):summarize(a,Config())
