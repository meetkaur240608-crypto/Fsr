# Restrained warm instrumental bed: slow sustained chords (soft, filtered), a sparse felt-piano style melody, light reverb.
import numpy as np, wave
sr=48000; dur=72.0; t=np.arange(int(sr*dur))/sr
rng=np.random.default_rng(7)
def note(f):  # frequency of midi note
    return 440*2**((f-69)/12)
# Progression in D major, 8 s per chord, warm voicings (midi)
chords=[[50,57,61,66],[47,54,57,62],[43,50,54,59],[45,52,57,61]]  # D, Bm, G, A (low voicings)
pad=np.zeros_like(t)
chord_len=8.0
for i in range(int(np.ceil(dur/chord_len))):
    ch=chords[i%4]; s=i*chord_len; e=min(dur,s+chord_len)
    idx=(t>=s)&(t<e+1.5)
    tt=t[idx]-s
    env=np.clip(tt/2.0,0,1)*np.clip((e+1.5-t[idx])/1.5,0,1)   # slow attack, soft release
    for m in ch:
        f=note(m)
        detune=1+rng.normal(0,0.0015)
        v=(np.sin(2*np.pi*f*detune*tt)+0.35*np.sin(2*np.pi*2*f*tt)+0.12*np.sin(2*np.pi*3*f*tt))
        v*=(1+0.03*np.sin(2*np.pi*0.2*tt))
        pad[idx]+=env*v*0.11
# Sparse melody (felt-piano-like plucks), pentatonic over D, roughly every 2-4 s, quiet
mel_notes=[74,78,81,78,74,69,71,74,78,81,83,81,78,74,71,69,74,78,81,78]
times=np.cumsum(rng.uniform(2.2,4.2,size=len(mel_notes)))+3.0
mel=np.zeros_like(t)
for m,st in zip(mel_notes,times):
    if st>dur-4: break
    f=note(m); idx=(t>=st)&(t<st+3.0); tt=t[idx]-st
    env=np.exp(-tt*1.6)*np.clip(tt/0.012,0,1)
    v=np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*4)+0.08*np.sin(2*np.pi*3*f*tt)*np.exp(-tt*6)
    mel[idx]+=env*v*0.16
mix=pad+mel
# simple reverb: convolve with decaying noise IR (1.8 s)
ir=rng.normal(0,1,int(sr*1.8))*np.exp(-np.arange(int(sr*1.8))/sr*2.6); ir[0]=1.0; ir/=np.abs(ir).sum()*0.08
wet=np.convolve(mix,ir)[:len(mix)]
out=0.75*mix+0.45*wet
# gentle lowpass (one-pole) to keep it soft
a=np.exp(-2*np.pi*3200/sr); y=np.zeros_like(out); acc=0.0
for i in range(len(out)):
    acc=a*acc+(1-a)*out[i]; y[i]=acc
y/=np.max(np.abs(y))*1.6
# fade in/out
fi=int(sr*2); fo=int(sr*4); y[:fi]*=np.linspace(0,1,fi); y[-fo:]*=np.linspace(1,0,fo)
st=np.stack([y,y],1); w=wave.open("music_bed.wav","w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close(); print("music ok")
