from src.models import Config,Arrival
from src.utils import make_traffic,simulate
from src.metrics import summarize

def test_continuous_overhead():
    cfg=Config();a=make_traffic('continuous',cfg);c=summarize(simulate(a,cfg,'circuit'),cfg);p=summarize(simulate(a,cfg,'packet'),cfg)
    assert c['payload_utilization']==1;assert p['payload_utilization']<c['payload_utilization']

def test_bursty_sharing():
    cfg=Config();a=make_traffic('staggered_burst',cfg);c=summarize(simulate(a,cfg,'circuit'),cfg);p=summarize(simulate(a,cfg,'packet'),cfg)
    assert p['loss_ratio']==0;assert p['payload_utilization']>c['payload_utilization'];assert p['mean_delay_ms']<c['mean_delay_ms']

def test_large_packet_and_window():
    cfg=Config(ticks=1);r=simulate([Arrival(0,0,200)],cfg,'packet');m=summarize(r,cfg)
    assert m['payload_utilization']==0 and m['backlog_payload_bits']==200 and m['mean_delay_ms'] is None
