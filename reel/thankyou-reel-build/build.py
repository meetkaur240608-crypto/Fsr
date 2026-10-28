import json, subprocess, os, re, math
FPS=30
W=os.getcwd(); os.makedirs("build/pieces_v2",exist_ok=True)
def fr(t): return int(round(t*FPS))
# ---- timeline: sections with audio spans (source seconds) and picture pieces (kind, src, start, frames)
sections=[
 {"id":"A","a0":28.92,"pieces":[("photo","p04",0,58),("photo","p03",0,88),("photo","p07",0,68)]},
 {"id":"B","a0":0.00,"pieces":[("vid","src",0.00,136)]},
 {"id":"C","a0":6.40,"pieces":[("vid","src",6.40,180),("photo","p05",0,27),("photo","p08",0,30),("photo","p09",0,29),("vid","src",15.2667,40)]},
 {"id":"D","a0":39.20,"pieces":[("vid","src",76.90,120),("vid","src",43.20,198)]},
 {"id":"E","a0":49.95,"pieces":[("vid","src",49.95,233),("photo","p02",0,68),("vid","src",59.9833,400)]},
 {"id":"F","a0":81.45,"pieces":[("vid","src",81.45,213)]},
]
CARD_DUR=3.0; CARD2_DUR=3.0; XF=0.6; XF2=0.5
# ---- render pieces
plist=[]; reel=0; n=0; sec_reel={}
for s in sections:
    s["r0"]=reel; sec_reel[s["id"]]=reel; frames=0
    for kind,srcn,st,nf in s["pieces"]:
        out=f"build/pieces_v2/{n:02d}_{s['id']}_{kind}_{srcn}.mp4"
        if not os.path.exists(out):
            if kind=="vid":
                cmd=["ffmpeg","-v","error","-y","-ss",f"{st:.4f}","-i","src.mp4","-frames:v",str(nf),"-vf",f"scale=1080:1920:flags=lanczos,fps={FPS},setsar=1,format=yuv420p","-an","-c:v","libx264","-crf","12","-preset","medium",out]
            else:
                cmd=["ffmpeg","-v","error","-y","-i",f"build/photos/{srcn}.mp4","-frames:v",str(nf),"-vf",f"fps={FPS},setsar=1,format=yuv420p","-an","-c:v","libx264","-crf","12","-preset","medium",out]
            subprocess.run(cmd,check=True)
        got=int(subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v:0","-show_entries","stream=nb_read_frames","-of","csv=p=0",out],capture_output=True,text=True).stdout.strip())
        assert got==nf,(out,got,nf)
        plist.append(out); frames+=nf; n+=1
    s["frames"]=frames; s["dur"]=frames/FPS; reel+=s["dur"]
TOTAL_SPEECH=reel
open("build/concat.txt","w").write("".join(f"file '{W}/{p}'\n" for p in plist))
print("speech timeline s:",TOTAL_SPEECH, {s['id']:(round(s['r0'],3),round(s['dur'],3)) for s in sections})
# ---- subtitles (ASS)
words=json.load(open("words.json"))
def reel_time(seg,t):
    s=[x for x in sections if x["id"]==seg][0]; return s["r0"]+(t-s["a0"])
caps=[]  # chunks
MAXC=46
def split_sentence(ws):
    # DP partition of a sentence into chunks <= MAXC chars, balanced, preferring comma breaks, no 1-word chunks
    n=len(ws); INF=1e18
    L=[len(w["w"]) for w in ws]
    def clen(i,j): return sum(L[i:j])+(j-i-1)
    best=[INF]*(n+1); prev=[-1]*(n+1); best[0]=0
    for j in range(1,n+1):
        for i in range(j):
            c=clen(i,j)
            if c>MAXC: continue
            cost=(max(0,30-c))**2*1.5 + (c-34)**2*0.15
            if j-i==1 and n>1: cost+=4000
            if j<n and ws[j-1]["w"].endswith(","): cost-=120
            if best[i]+cost<best[j]: best[j]=best[i]+cost; prev[j]=i
    out=[]; j=n
    while j>0: out.append(ws[prev[j]:j]); j=prev[j]
    return out[::-1]
for s in sections:
    ws=[w for w in words if w["seg"]==s["id"] and s["a0"]-0.05<=w["s"]<=s["a0"]+s["dur"]+0.05]
    sent=[]
    for w in ws:
        sent.append(w)
        if re.search(r"[.!?…]$",w["w"]): caps.extend(split_sentence(sent)); sent=[]
    if sent: caps.extend(split_sentence(sent))
def two_lines(ws):
    t=" ".join(w["w"] for w in ws)
    if len(t)<=24: return t
    best=None
    for i in range(1,len(ws)):
        a=" ".join(w["w"] for w in ws[:i]); b=" ".join(w["w"] for w in ws[i:])
        score=abs(len(a)-len(b)) - (6 if a.endswith((",",".","…")) else 0)
        if max(len(a),len(b))<=26 and (best is None or score<best[0]): best=(score,a,b)
    if best is None:
        i=len(ws)//2; return " ".join(w["w"] for w in ws[:i])+"\\N"+" ".join(w["w"] for w in ws[i:])
    return best[1]+"\\N"+best[2]
def ts(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
lines=[]
for i,ch in enumerate(caps):
    seg=ch[0]["seg"]; st=reel_time(seg,ch[0]["s"])-0.08
    last=ch[-1]; en=reel_time(seg,last["s"])+max(0.55,0.09*len(last["w"])+0.3)
    if i+1<len(caps):
        nst=reel_time(caps[i+1][0]["seg"],caps[i+1][0]["s"])-0.08
        if nst-st<8: en=min(max(en,nst-0.04),nst-0.04) if nst>st else en
    lines.append(f"Dialogue: 0,{ts(st)},{ts(en)},Sub,,0,0,0,,{two_lines(ch)}")
title=f"Dialogue: 1,{ts(0.45)},{ts(3.3)},Title,,0,0,0,,{{\\fad(500,500)\\fsp7}}BEFORE ALL OF THIS"
ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Medium,54,&H00FFFFFF,&H00FFFFFF,&H5A000000,&H80000000,0,0,0,0,100,100,0,0,1,2.4,1.2,2,100,100,420,1
Style: Title,Inter SemiBold,42,&H00FFFFFF,&H00FFFFFF,&H70000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1,8,100,100,290,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
{title}
"""+"\n".join(lines)+"\n"
open("build/subs.ass","w").write(ass)
print("captions:",len(lines)); print("\n".join(lines[:6]))
# ---- audio
TOTAL=TOTAL_SPEECH-XF+CARD_DUR-XF2+CARD2_DUR
af=[]; concat_in=[]
for i,s in enumerate(sections):
    af.append(f"[0:a]atrim=start={s['a0']:.4f}:end={s['a0']+s['dur']:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={s["dur"]-0.03:.4f}:d=0.03[d{i}]")
    concat_in.append(f"[d{i}]")
af.append(f"{''.join(concat_in)}concat=n={len(sections)}:v=0:a=1,apad=whole_dur={TOTAL:.3f}[dlg]")
af.append(f"[1:a]atrim=0:{TOTAL:.3f},volume=0.30,afade=t=out:st={TOTAL-3.2:.3f}:d=3.2[m0]")
af.append("[dlg]asplit[dlg1][sc]")
af.append("[m0][sc]sidechaincompress=threshold=0.035:ratio=4:attack=40:release=900:makeup=1:level_sc=1[md]")
af.append("[dlg1][md]amix=inputs=2:normalize=0:duration=first[mix]")
subprocess.run(["ffmpeg","-v","error","-y","-i","dialogue_clean.wav","-i","music_bed.wav","-filter_complex",";".join(af),"-map","[mix]","-ar","48000","build/mix_raw.wav"],check=True)
# two-pass loudnorm to -14 LUFS (linear)
meas=subprocess.run(["ffmpeg","-hide_banner","-i","build/mix_raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
j=json.loads(meas[meas.rindex("{"):])
ln=f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true:print_format=summary"
subprocess.run(["ffmpeg","-v","error","-y","-i","build/mix_raw.wav","-af",ln,"-ar","48000","build/mix_final.wav"],check=True)
print("loudness measured:",j["input_i"],"LUFS -> -14 target")
# ---- final video
FONT_M="/usr/share/fonts/opentype/inter/Inter-Medium.otf"; FONT_B="/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
card=(f"drawtext=fontfile={FONT_M}:text='THANK YOU FOR BEING PART OF OUR JOURNEY.':fontcolor=white@0.88:fontsize=38:x=(w-text_w)/2:y=872,"
      f"drawtext=fontfile={FONT_B}:text='FULL SIZE RUN':fontcolor=white:fontsize=104:x=(w-text_w)/2:y=940,"
      f"drawbox=x=(iw-140)/2:y=1082:w=140:h=7:color=0xD0021B@1:t=fill")
offset=TOTAL_SPEECH-XF
offset2=TOTAL_SPEECH-XF+CARD_DUR-XF2
card2=(f"drawtext=fontfile={FONT_B}:textfile=build/card2a.txt:fontcolor=white:fontsize=92:x=(w-text_w)/2:y=820,"
       f"drawtext=fontfile={FONT_B}:textfile=build/card2b.txt:fontcolor=white:fontsize=92:x=(w-text_w)/2:y=930,"
       f"drawtext=fontfile={FONT_M}:text='@fullsizerun.in':fontcolor=white@0.7:fontsize=36:x=(w-text_w)/2:y=1070,"
       f"drawbox=x=(iw-140)/2:y=1150:w=140:h=7:color=0xD0021B@1:t=fill")
fc=(f"[0:v]fps={FPS},settb=1/{FPS},ass=build/subs.ass,noise=alls=5:allf=t+u[v0];"
    f"[1:v]settb=1/{FPS},{card}[card];"
    f"[2:v]settb=1/{FPS},{card2}[card2];"
    f"[v0][card]xfade=transition=fade:duration={XF}:offset={offset:.4f}[v1];"
    f"[v1][card2]xfade=transition=fade:duration={XF2}:offset={offset2:.4f},fade=t=out:st={TOTAL-0.6:.3f}:d=0.6,format=yuv420p[v]")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","build/concat.txt",
  "-f","lavfi","-i",f"color=c=0x0a0a0a:s=1080x1920:r={FPS}:d={CARD_DUR}",
  "-f","lavfi","-i",f"color=c=0x0a0a0a:s=1080x1920:r={FPS}:d={CARD2_DUR}",
  "-i","build/mix_final.wav",
  "-filter_complex",fc,"-map","[v]","-map","3:a","-c:v","libx264","-crf","19","-preset","slow","-profile:v","high","-level","4.1","-r",str(FPS),"-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart","-shortest","build/FSR-thankyou-reel.mp4"],check=True)
print("TOTAL",TOTAL)
json.dump({"sections":[{k:v for k,v in s.items()} for s in sections],"total":TOTAL,"speech":TOTAL_SPEECH},open("build/timeline.json","w"),indent=1)
