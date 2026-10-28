#!/bin/bash
# Render each photo as a 5 s 1080x1920 clip with a gentle push-in. Portrait photos: cover-crop. Landscape/3:4-wide: blurred fill.
set -e
mkdir -p build/photos
Z="zoompan=z='1+0.00040*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30"
cover() { # $1 in $2 out
  ffmpeg -v error -y -loop 1 -i "$1" -t 5 -vf "scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,$Z,format=yuv420p" -r 30 -c:v libx264 -crf 12 -preset medium "$2"
}
blurfill() {
  ffmpeg -v error -y -loop 1 -i "$1" -t 5 -filter_complex "[0:v]split[a][b];[a]scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,gblur=sigma=45,eq=brightness=-0.12:saturation=0.85[bg];[b]scale=2160:3840:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,$Z,format=yuv420p" -r 30 -c:v libx264 -crf 12 -preset medium "$2"
}
cover photos/p01_nike_bags_floor.jpg build/photos/p01.mp4
cover photos/p02_three_at_stall.jpg build/photos/p02.mp4
blurfill photos/p03_yeezy_livingroom.jpg build/photos/p03.mp4
cover photos/p04_owner_stall.jpg build/photos/p04.mp4
blurfill photos/p05_dog_home.jpg build/photos/p05.mp4
cover photos/p06_adidas_bags.jpg build/photos/p06.mp4
cover photos/p07_jordan4_lot.jpg build/photos/p07.mp4
cover photos/p08_selfie.jpg build/photos/p08.mp4
blurfill photos/p09_mall_friends.jpg build/photos/p09.mp4
cover photos/p10_queue.jpg build/photos/p10.mp4
echo photos-done
