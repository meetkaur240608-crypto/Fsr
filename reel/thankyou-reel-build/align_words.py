import json, wave, re, difflib, numpy as np, sherpa_onnx
d="models/sherpa-onnx-nemo-ctc-en-conformer-small/"
rec=sherpa_onnx.OfflineRecognizer.from_nemo_ctc(model=d+"model.onnx", tokens=d+"tokens.txt", num_threads=4)
w=wave.open("audio_norm.wav"); sr=w.getframerate(); data=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
cuts=[0,15.0,25.0,38.4,50.0,58.0,67.6,80.5,88.6]
rw=[]  # recognized words: (text, start, end)
for a,b in zip(cuts[:-1],cuts[1:]):
    s=rec.create_stream(); s.accept_waveform(sr,data[int(a*sr):int(b*sr)]); rec.decode_stream(s); r=s.result
    toks=list(zip(r.tokens,r.timestamps))
    cur=None
    for t,ts in toks:
        ts=a+ts
        if t.startswith(" ") or t.startswith("▁"):
            if cur: rw.append(cur)
            cur=[t[1:],ts,ts+0.08]
        else:
            if cur is None: cur=[t,ts,ts+0.08]
            else: cur[0]+=t; cur[2]=ts+0.08
    if cur: rw.append(cur)
print("recognized:", " ".join(f"{x[0]}@{x[1]:.2f}" for x in rw))
segs=json.load(open("ref_segments.json"))
out=[]
for seg in segs:
    words=seg["text"].split()
    norm=lambda s: re.sub(r"[^a-z0-9]","",s.lower())
    cand=[x for x in rw if seg["start"]-0.3<=x[1]<=seg["end"]+0.3]
    sm=difflib.SequenceMatcher(a=[norm(x) for x in words], b=[norm(x[0]) for x in cand], autojunk=False)
    times=[None]*len(words)
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=="equal":
            for k in range(i2-i1): times[i1+k]=(cand[j1+k][1],cand[j1+k][2])
    # interpolate unmatched: find runs of None first, then fill each run evenly (weighted by word length)
    i=0
    while i<len(times):
        if times[i] is not None: i+=1; continue
        j=i
        while j<len(times) and times[j] is None: j+=1
        lo=times[i-1][1] if i>0 else seg["start"]
        hi=times[j][0] if j<len(times) else seg["end"]
        lens=[max(2,len(re.sub(r"[^A-Za-z0-9]","",wd))) for wd in words[i:j]]
        tot=sum(lens); cur=lo
        for k,L in enumerate(lens):
            d=(hi-lo)*L/tot
            times[i+k]=(cur, cur+d-0.02); cur+=d
        i=j
    for wd,(s,e) in zip(words,times):
        out.append({"w":wd,"s":round(s,2),"e":round(e,2),"seg":seg["id"]})
json.dump(out,open("words.json","w"),indent=0)
for seg in segs:
    print(f"--- {seg['id']} {seg['start']}-{seg['end']}")
    print(" ".join(f"{o['w']}@{o['s']}" for o in out if o['seg']==seg['id']))
