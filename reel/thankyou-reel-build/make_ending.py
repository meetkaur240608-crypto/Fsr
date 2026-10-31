# Closing-cards music stem (reel time). Same 96 BPM grid as music_bed.wav (beats at multiples of 0.625 s).
# Bar A 62.5-65.0 (card 1): F(add9) groove.  Bar B 65.0-67.5 (card 2): C(add9), brighter, rings into the fade.
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
sr=48000; TOTAL=float(sys.argv[1]) if len(sys.argv)>1 else 67.8333
N=int(sr*(TOTAL+0.5)); out=np.zeros((N,2))
beat=60/96; A=62.5; B=65.0
rng=np.random.default_rng(21)
f=lambda m: 440*2**((m-69)/12)
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],btype="band",fs=sr,output="sos"),x)
def hp(x,c): return sosfilt(butter(2,c,btype="high",fs=sr,output="sos"),x)
def lp(x,c): return sosfilt(butter(2,c,btype="low",fs=sr,output="sos"),x)
def add(t0,sig,pan=0.0,g=1.0):
    i=int(t0*sr); j=min(N,i+len(sig))
    if i>=N or j<=0: return
    s=sig[:j-i]*g; out[i:j,0]+=s*np.sqrt((1-pan)/2); out[i:j,1]+=s*np.sqrt((1+pan)/2)
def tone(fr,L,decay,harm=(1,0.35,0.12,0.05)):
    tt=np.arange(int(L*sr))/sr
    s=sum(a*np.sin(2*np.pi*fr*(k+1)*tt)*np.exp(-tt*decay*(1+0.6*k)) for k,a in enumerate(harm))
    return s*np.clip(tt/0.003,0,1)
# --- swell into card 1 (61.55 -> 62.5): filtered noise riser, quiet under the last "Thank you"
L=int((A-61.55)*sr); tt=np.arange(L)/sr; n=rng.normal(0,1,L)
riser=hp(n,2500)*((tt/tt[-1])**3)*0.22
add(61.55,riser,-0.2); add(61.55,hp(rng.normal(0,1,L),2500)*((tt/tt[-1])**3)*0.22,0.2)
# --- crashes (soft) on the two downbeats
for t0,g in [(A,0.20),(B,0.15)]:
    L=int(2.4*sr); tt=np.arange(L)/sr
    c=lp(hp(rng.normal(0,1,L),4500),13000)*np.exp(-tt*1.6)*np.clip(tt/0.002,0,1)
    add(t0,c,-0.3,g); add(t0+0.004,lp(hp(rng.normal(0,1,L),4500),13000)*np.exp(-tt*1.6),0.3,g)
# --- harmony
bars=[(A,[53,60,65,67,69],41),(B,[48,55,64,67,74],48)]  # F add9 voicing / C add9 voicing ; bass root midi
for t0,ch,root in bars:
    # warm pad (whole bar + ring)
    L=2.5+(1.6 if t0==B else 0.3); tt=np.arange(int(L*sr))/sr
    env=np.clip(tt/0.25,0,1)*np.clip((L-tt)/0.6,0,1)
    pad=sum(np.sin(2*np.pi*f(m)*(1+rng.normal(0,0.0012))*tt)+0.25*np.sin(2*np.pi*2*f(m)*tt) for m in ch)
    add(t0,lp(pad*env,4200)*0.045,-0.15); add(t0,lp(pad*env,4200)*0.045,0.15)
    # piano chord stabs: beat 1 and the "and" of 2, beat 4-and pickup
    for off,vel in [(0,1.0),(1.5*beat,0.7),(3.5*beat,0.55)]:
        for m in ch[1:]:
            add(t0+off,tone(f(m+12),1.6,3.2)*0.05*vel,rng.uniform(-0.4,0.4))
    # 8th-note arp, an octave up, bright
    pat=[1,2,3,4,3,2,4,3]
    for k in range(8):
        m=ch[pat[k]]+12; add(t0+k*beat/2,tone(f(m),0.5,7.5)*(0.07 if k%2 else 0.09),0.35 if k%2 else -0.35)
    # bass: root 8ths, octave on offbeats, round and short
    for k in range(8):
        m=root+(12 if k%2 else 0); L=0.28; tt=np.arange(int(L*sr))/sr
        b=np.tanh(1.6*np.sin(2*np.pi*f(m)*tt))*np.exp(-tt*6)*np.clip(tt/0.004,0,1)
        add(t0+k*beat/2,lp(b,900)*0.20)
    # kick on 1 and 3, plus a pickup on 4-and in bar A
    for kb in ([0,2,3.5] if t0==A else [0,2]):
        L=0.35; tt=np.arange(int(L*sr))/sr
        ph=2*np.pi*(48*tt+(140-48)*(1-np.exp(-tt*28))/28)
        add(t0+kb*beat,np.sin(ph)*np.exp(-tt*10)*0.42)
    # claps on 2 and 4 (three bursts, band-passed, small room)
    for cb in [1,3]:
        L=0.25; tt=np.arange(int(L*sr))/sr; clap=np.zeros(len(tt))
        for d in (0.0,0.011,0.022):
            i=int(d*sr); e=np.exp(-np.clip(tt[i:]-tt[i],0,None)*(55 if d<0.02 else 18))
            clap[i:]+=rng.normal(0,1,len(tt)-i)*e
        add(t0+cb*beat,bp(clap,900,2600)*0.11,0.1)
    # hats: 8ths, offbeats open-ish
    for k in range(8):
        L=0.06 if k%2==0 else 0.14; tt=np.arange(int(L*sr))/sr
        h=hp(rng.normal(0,1,len(tt)),7500)*np.exp(-tt*(80 if k%2==0 else 28))
        add(t0+k*beat/2,h*(0.035 if k%2==0 else 0.05),0.45)
# --- final ring: high C piano note at the last downbeat-and-a-half for a light finish
add(B+3*beat,tone(f(84),2.0,1.8)*0.05,0.2)
# --- reverb send
ir=rng.normal(0,1,int(sr*1.6))*np.exp(-np.arange(int(sr*1.6))/sr*3.0); ir[0]=0; ir/=np.abs(ir).sum()*0.06
for c in range(2): out[:,c]+=0.30*np.convolve(out[:,c],ir)[:N]
# --- fade with the picture (video fades to black from TOTAL-0.6)
fs=int((TOTAL-0.75)*sr); fe=int(TOTAL*sr); out[fs:fe]*=np.linspace(1,0,fe-fs)[:,None]; out[fe:]=0
out/=np.abs(out).max()*1.12
w=wave.open("ending_stem.wav","w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
print("ending stem ok", round(len(out)/sr,2),"s")
