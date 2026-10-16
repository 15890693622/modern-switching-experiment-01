import pytest,numpy as np
from src.models import Config,Arrival
from src.utils import simulate,make_traffic,pack_pcm

def test_pcm():
    a=np.array([[1,2],[3,4]]);f=pack_pcm(a,[1,31]);assert f.shape==(2,32);assert np.array_equal(f[:,[1,31]],a);assert (f[:,16]==255).all()
    with pytest.raises(ValueError):pack_pcm(a,[1,1])
    with pytest.raises(ValueError):pack_pcm(a,[0,1])

def test_invalid():
    with pytest.raises(ValueError):Config(users=0)
    with pytest.raises(ValueError):simulate([Arrival(-1,0,10)],Config(),'circuit',lambda q,t,c:(0,[]))

def test_fair_admission():
    cfg=Config(ticks=2,buffer_payload_bits=100);traffic=[Arrival(0,0,80),Arrival(0,1,40)]
    for mode in ('circuit','packet'):
        r=simulate(traffic,cfg,mode,lambda q,t,c:(0,[]));assert r['generated_payload_bits']==120 and r['dropped_payload_bits']==40 and r['backlog_payload_bits']==80

def test_repeatability():assert make_traffic('light_random',Config(),7)==make_traffic('light_random',Config(),7)
