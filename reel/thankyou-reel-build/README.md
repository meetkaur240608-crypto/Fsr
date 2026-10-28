# Rebuilding the thank-you Reel

Inputs expected in the working directory: `src.mp4` (the original 88.6 s warehouse video), `photos/p01…p11.jpg` (the uploaded photographs, named as in `make_photo_clips.sh`), `dialogue_clean.wav` and `audio_norm.wav` (derived from `src.mp4`, see below).

```
ffmpeg -i src.mp4 -vn -ac 1 -ar 16000 audio.wav
ffmpeg -i audio.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 16000 audio_norm.wav      # for the aligner
ffmpeg -i src.mp4 -vn -af "highpass=f=80,afftdn=nr=9:nf=-45:tn=1,acompressor=threshold=-20dB:ratio=2:attack=8:release=250:makeup=2" -ar 48000 -ac 2 dialogue_clean.wav
python3 make_music.py            # synthesised bed -> music_bed.wav (replace with a licensed track if preferred)
./make_photo_clips.sh            # 5 s push-in clips -> build/photos/
python3 align_words.py           # word timings -> words.json (needs sherpa-onnx + the NeMo conformer-small CTC model)
python3 build.py                 # pieces, subtitles, ducked mix, final encode -> build/FSR-thankyou-reel.mp4
```

`words.json` and `subs.ass` are included, so `build.py` can be re-run without the speech model if only picture or audio settings change.
