# Warm, gently lively bed: C major I-V-vi-IV at 96 BPM, soft pad + plucked 8th-note arpeggio;
# from the helper close-up a soft kick comes in, and over the closing cards it opens up (kick on every beat, shaker, octave plucks, +6 dB).
import numpy as np, wave, sys
sr=48000; dur=72.0; N=int(sr*dur); t=np.arange(N)/sr
BPM=96; beat=60/BPM; bar=4*beat
LIFT=float(sys.argv[1]) if len(sys.argv)>1 else 62.3   # reel time where the cards begin
SOFT=float(sys.argv[2]) if len(sys.argv)>2 else 55.8   # helper close-up: first soft pulse
rng=np.random.default_rng(11)
f=lambda m: 440*2**((m-69)/12)
chords=[[48,55,60,64],[47,55,59,62],[45,52,57,60],[41,48,53,57]]
arp_pat=[0,1,2,3,2,1,3,2]
pad=np.zeros(N); pluck=np.zeros(N); perc=np.zeros(N)
def add(buf,start,sig):
    i=int(start*sr); j=min(N,i+len(sig)); 
    if i<N: buf[i:j]+=sig[:j-i]
nb=int(np.ceil(dur/bar))
for b in range(nb):
    ch=chords[b%4]; s=b*bar
    # pad
    L=int((bar+1.2)*sr); tt=np.arange(L)/sr
    env=np.clip(tt/0.9,0,1)*np.clip((bar+1.2-tt)/1.2,0,1)
    v=np.zeros(L)
    for m in ch:
        fr=f(m)*(1+rng.normal(0,0.001))
        v+=np.sin(2*np.pi*fr*tt)+0.3*np.sin(2*np.pi*2*fr*tt)+0.1*np.sin(2*np.pi*3*fr*tt)+0.05*np.sin(2*np.pi*5*fr*tt)
    add(pad,s,env*v*0.07)
    # plucks (8ths)
    for k in range(8):
        st=s+k*beat/2; m=ch[arp_pat[k]]+12
        if st>=LIFT: m+=12 if k%2==0 else 0
        L2=int(0.5*sr); tt2=np.arange(L2)/sr; fr=f(m)
        e=np.exp(-tt2*7)*np.clip(tt2/0.004,0,1)
        w=np.sin(2*np.pi*fr*tt2)+0.4*np.sin(2*np.pi*2*fr*tt2)*np.exp(-tt2*10)+0.15*np.sin(2*np.pi*3*fr*tt2)*np.exp(-tt2*14)
        vel=0.09 if st<LIFT else 0.14
        if k in (0,4): vel*=1.25
        add(pluck,st,e*w*vel)
    # percussion
    for k in range(4):
        st=s+k*beat
        on = (st>=LIFT) or (st>=SOFT and k in (0,2))
        if on:
            L3=int(0.3*sr); tt3=np.arange(L3)/sr
            ph=2*np.pi*(50*tt3+ (150-50)*(1-np.exp(-tt3*25))/25)
            kick=np.sin(ph)*np.exp(-tt3*12)*(0.42 if st>=LIFT else 0.22)
            add(perc,st,kick)
    if s>=LIFT:
        for k in range(8):
            st=s+k*beat/2; L4=int(0.05*sr); n=rng.normal(0,1,L4)*np.exp(-np.arange(L4)/sr*90)
            # crude high-pass
            n=n-np.convolve(n,np.ones(24)/24,mode="same")
            add(perc,st+0.01,n*(0.05 if k%2 else 0.03))
mix=pad+pluck+perc
# reverb
ir=rng.normal(0,1,int(sr*1.4))*np.exp(-np.arange(int(sr*1.4))/sr*3.2); ir[0]=1.0; ir/=np.abs(ir).sum()*0.07
wet=np.convolve(pad+pluck,ir)[:N]
out=0.8*mix+0.35*wet
# soft lowpass one-pole at ~5 kHz
a=np.exp(-2*np.pi*5000/sr); y=np.zeros(N); acc=0.0
for i in range(N):
    acc=a*acc+(1-a)*out[i]; y[i]=acc
# gain automation: +6 dB from LIFT with 1 s ramp
g=np.ones(N); i0=int(LIFT*sr); r=int(1.0*sr)
g[i0:i0+r]=np.linspace(1,2.0,r); g[i0+r:]=2.0
y*=g
y/=np.max(np.abs(y))*1.25
fi=int(sr*1.5); y[:fi]*=np.linspace(0,1,fi)
st=np.stack([y,y],1); w=wave.open("music_bed.wav","w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close(); print("music v2 ok")
