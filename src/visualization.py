"""教师提供科学绘图，图中英文标注避免环境缺少中文字体。"""
def plot_results(rows,traces,output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    scenarios=list(dict.fromkeys(r['scenario'] for r in rows));x=np.arange(len(scenarios))
    fig,axs=plt.subplots(1,3,figsize=(14,4.6))
    for mode,offset,color in [('circuit',-.18,'#27638b'),('packet',.18,'#d27a35')]:
        subset=[next(r for r in rows if r['scenario']==s and r['mode']==mode) for s in scenarios]
        for ax,key,title in zip(axs,['payload_utilization','mean_delay_ms','loss_ratio'],['Payload utilization','Mean completion delay (ms)','Payload loss ratio']):
            ax.bar(x+offset,[np.nan if r[key] is None else r[key] for r in subset],.36,label=mode,color=color)
            ax.set_title(title);ax.set_xticks(x,scenarios,rotation=25,ha='right');ax.legend();ax.grid(axis='y',alpha=.2)
    fig.tight_layout();fig.savefig(output/'comparison_metrics.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4))
    for mode in ('circuit','packet'):
        tr=traces['staggered_burst/'+mode]['trace'];ax.plot([v['tick'] for v in tr],[v['buffer_payload_bits'] for v in tr],label=mode)
    ax.set(xlabel='Simulation tick (1 ms)',ylabel='Reserved payload buffer (bits)',title='Staggered burst buffer occupancy');ax.legend();fig.tight_layout();fig.savefig(output/'queue_occupancy.png',dpi=150);plt.close(fig)
    from .utils import pack_pcm
    frames=pack_pcm(np.array([[10+i,40+i,70+i,100+i] for i in range(8)]),[1,2,3,4])
    fig,ax=plt.subplots(figsize=(11,3));im=ax.imshow(frames,aspect='auto',vmin=0,vmax=255,cmap='viridis');ax.set(xlabel='PCM timeslot',ylabel='Frame',title='Provided PCM helper: idle code 255, TS0/TS16 reserved');fig.colorbar(im,ax=ax,label='PCM byte');fig.tight_layout();fig.savefig(output/'pcm_frame_view.png',dpi=150);plt.close(fig)
