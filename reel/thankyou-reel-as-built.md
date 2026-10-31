# Full Size Run — thank-you Reel, as built

Deliverables in this folder:

- `FSR-thankyou-reel.mp4` — the finished Reel, 1080×1920, 30 fps, H.264 High, AAC 320 kbps 48 kHz stereo, 67.8 s, −14 LUFS integrated, true peak −1 dBTP. The posting master (CRF 15, veryslow, about 30 Mbps, 258 MB) was delivered in the session and exceeds GitHub's file limit; the copy stored here is the same picture re-encoded at CRF 18 (about 80 MB) with the master's audio copied unchanged.
- `FSR-thankyou-reel.srt` — the burned-in captions as a separate subtitle file, for re-use or correction.
- `FSR-thankyou-reel-cover.jpg` — suggested cover frame (helper's thumbs-up).

Unused photographs: the Nike queue (not customers), the Dunk bags on the floor, the adidas bags, the TJ Kicks shipping box and the hospital screenshot.
- `thankyou-reel-build/` — the scripts that produced the file (ffmpeg + Python), so the edit can be regenerated after any change.

Source: `37d28814-…MP4` (88.6 s, 576×1024). The Reel is an upscale of that footage (Lanczos, no sharpening), so it is softer than the photographs by design. A faint temporal grain is applied to the whole picture track to unify the upscaled video with the photos.

## Timeline (Reel time → source)

| Reel | Dur | Picture | Audio (source) | Spoken words |
|---|---|---|---|---|
| 0:00.00 | 1.93 | Photo: owner behind the TJ Kicks pop-up stall (push-in). Title "BEFORE ALL OF THIS" fades in at 0:00.45 and out by 0:03.3, top of frame. | 28.92–36.05 | "I was a teenager when I started this business." |
| 0:01.93 | 2.93 | Photo: Yeezy boxes stacked in the living room | ↑ | "I used to sell three to five shoes a month," |
| 0:04.87 | 2.27 | Photo: Jordan 4 boxes in bags on the parking-lot floor | ↑ | "with the sole purpose of, you know, just making money." |
| 0:07.13 | 4.53 | Video two-shot (hard cut — the reveal of the warehouse) | 0.00–4.53 | "Hi guys, I'm just at the warehouse. It's about 9:15 p.m." |
| 0:11.67 | 6.00 | Video two-shot | 6.40–16.60 | "And just a quick video. This is nothing. Koi vlog nahi, koi stock update nahi. Just to thank you all." |
| 0:17.67 | 0.90 | Photo: owner with the dog and boxes at home (L-cut, blurred fill) | ↑ | "Thank my family," |
| 0:18.57 | 1.00 | Photo: selfie with a friend (L-cut, his voice continues) | ↑ | "thank my friends," |
| 0:19.57 | 0.97 | Photo: three friends in the mall with Nike bags | ↑ | "thank God" |
| 0:20.53 | 1.33 | Video two-shot | ↑ | "that they have taken me this far." |
| 0:21.87 | 4.00 | Video: handheld pan across the warehouse shelves (picture from source 76.9–80.9, its own audio muted) | 39.20–49.80 | "Like, five years later, we're at this warehouse where in just three months" |
| 0:25.87 | 6.60 | Video two-shot | ↑ | "we are numbering our 4,200th pair, which is insane for me. I know people sell much more and much higher." |
| 0:32.47 | 7.77 | Video two-shot | 49.95–73.32 | "But this is just, like, a very big moment for me, which is where I realised that gratitude is very important. So I just want to thank all of my buyers, my…" |
| 0:40.23 | 2.27 | Photo: three at the TJ Kicks stall | ↑ | "everyone who has supported me in this journey." |
| 0:42.50 | 13.33 | Video two-shot, no overlays (held for the heartfelt section) | ↑ | "Sumit bhaiya, like, everyone who has always been there. And I think we're just getting started, and… just, like, thank you so much everyone, and God is great, and I just love you all so much. Thank you." |
| 0:55.83 | 7.10 | Video: helper close-up, smile, thumbs-up, speaks into the mic; owner leans back in for the last word | 81.45–88.55 | "So thank you everyone, and love you, keep supporting us." Helper: "Thank you. Thank you, thank you." Owner: "Thank you." |
| 1:02.33 | 0.60 | Fade from the last frame to the closing card | — | — |
| 1:02.93 | 2.50 | Card 1: "THANK YOU FOR BEING PART OF OUR JOURNEY." / "FULL SIZE RUN" / short red rule, near-black background. | — | — |
| 1:05.43 | 0.50 | Crossfade to card 2 | — | — |
| 1:05.93 | 2.50 | Card 2: "WE'RE JUST GETTING STARTED." / "@fullsizerun.in" / red rule. Fades to black over the final 0.6 s. | — | — |

Removed from the source: 4.53–6.40 ("Say hello" and the greeting), 16.60–28.92 (the first mention of the 4,200 figure and the filler lead-in), 36.05–39.20 ("I always had an act of making money"), 73.32–81.45 (repeated thank-yous and camera moves; the pan is reused as picture only), 88.55–end.

## Audio

- Dialogue: original voices, high-pass at 80 Hz, light spectral noise reduction (afftdn, about 9 dB), gentle 2:1 compression above −20 dB. Segments joined with 12 ms fade-in and 30 ms fade-out at each cut, on word boundaries.
- Music (through the helper close-up): a warm, gently lively synthesised bed in C major (I–V–vi–IV at 96 BPM), soft pad plus a plucked eighth-note arpeggio, with a soft kick entering under the helper's close-up (0:55.8). Side-chain ducked by the dialogue (4:1 above −29 dBFS, 40 ms attack, 900 ms release), about −36 LUFS under speech. It fades out at 1:02.3, where the closing stem takes over on the same beat grid.
- Closing music (`make_ending.py`, mixed without ducking): a soft noise swell rises under the owner's last "Thank you" (1:01.6), then a fuller groove lands on the first card at 1:02.5 with an F(add9) chord, a soft crash, kick, claps on 2 and 4, hats, a bass line and piano stabs. A brighter C(add9) bar lands on "WE'RE JUST GETTING STARTED." at 1:05.0, and a high piano note rings into the fade to black. Around −16 LUFS over the cards.
- Shutter: a real recorded camera shutter (Android Open Source Project `camera_click_48k.ogg`, Apache-2.0) on every cut-in to a photograph (0:00, 0:01.9, 0:04.9, 0:17.7, 0:18.6, 0:19.6, 0:40.2). Light 150 Hz high-pass, peak about −12 dBFS, and a ±2 % pitch variation per click so repeats don't sound identical. Mixed outside the ducking.
- Mix: two-pass linear loudness normalisation to −14 LUFS, −1 dBTP.

If you prefer a licensed track, drop it in place of `music_bed.wav` at the same level and re-run the build; the ducking is automatic.

## Subtitles

Word timings came from a CTC speech model aligned to the verified transcript; captions are grouped by sentence, at most two lines of about 26 characters, Inter Medium 54 px, white with a soft dark outline, bottom-centred with the baseline 420 px above the bottom edge (clear of Instagram's bottom UI). Hinglish kept as spoken.

Two transcript items to confirm by ear before posting: "Koi **vlog** nahi" (the model heard "blog"; "vlog" is the more likely word), and the spelling of "Sumit bhaiya".

## Export settings used

```
ffmpeg … -c:v libx264 -crf 15 -preset veryslow -profile:v high -level 4.2 -x264-params aq-mode=3:ref=5 \
       -r 30 -pix_fmt yuv420p -c:a aac -b:a 320k -ar 48000 -movflags +faststart
```
