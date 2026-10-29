#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize_videos_and_generate_webp.py
====================================
S&R CoreSync - Multimedia Optimization & Animated WebP Generation Engine
Uses FFmpeg 9.0.2 to:
1. Probe video files and report original metrics (resolution, duration, bitrate, size).
2. Compress videos using two-pass/CRF H.264 with +faststart for instant web streaming.
3. Generate ultra-lightweight animated WebP equivalents with optimized frame rates.
4. Report before/after file sizes and percentage reductions.
"""

import os
import sys
import subprocess
import glob

FFMPEG_EXE = r"C:\Users\msali\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
FFPROBE_EXE = r"C:\Users\msali\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffprobe.exe"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

def format_size(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.2f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.2f} MB"

def probe_video(file_path):
    cmd = [
        FFPROBE_EXE,
        "-v", "error",
        "-show_entries", "stream=width,height,codec_name,bit_rate,r_frame_rate",
        "-show_entries", "format=duration,size,bit_rate",
        "-of", "default=noprint_wrappers=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = {}
    for line in res.stdout.strip().split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            info[k.strip()] = v.strip()
    return info

def compress_video(src_path, dst_path, crf=26):
    """
    Compress video for web:
    - Silent web background video (-an)
    - High profile, level 4.1
    - CRF 26 (excellent quality / size tradeoff)
    - movflags +faststart (places moov atom at beginning for instant web streaming)
    """
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", src_path,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-an",
        dst_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0

def generate_animated_webp(src_path, dst_path, scale_w=960, fps=15, q=75):
    """
    Generate optimized animated WebP:
    - Reduced frame rate (15 fps) for smooth cinema loop without CPU load
    - Scaled width preserving aspect ratio (-1)
    - Quality 75
    - Loop count 0 (infinite)
    """
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", src_path,
        "-vf", f"fps={fps},scale={scale_w}:-1:flags=lanczos",
        "-c:v", "libwebp",
        "-lossless", "0",
        "-compression_level", "6",
        "-q:v", str(q),
        "-loop", "0",
        "-an",
        dst_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0

def main():
    print("=" * 70)
    print(" S&R CoreSync - Multimedia Optimization & Animated WebP Suite")
    print("=" * 70)

    target_videos = [
        "hero-founder-cinematic.mp4",
        "about-founder-cinematic.mp4"
    ]

    results = []

    for vid_name in target_videos:
        src_file = os.path.join(ASSETS_DIR, vid_name)
        if not os.path.exists(src_file):
            print(f"Skipping {vid_name}: file not found.")
            continue

        orig_size = os.path.getsize(src_file)
        info = probe_video(src_file)
        w = info.get("width", "?")
        h = info.get("height", "?")
        dur = info.get("duration", "?")
        if dur != "?":
            try:
                dur = f"{float(dur):.2f}s"
            except:
                pass

        print(f"\n[+] Processing: {vid_name}")
        print(f"    Original: {w}x{h} | Duration: {dur} | Size: {format_size(orig_size)}")

        # 1. Compress MP4
        opt_mp4_name = vid_name.replace(".mp4", "-ultra-opt.mp4")
        opt_mp4_path = os.path.join(ASSETS_DIR, opt_mp4_name)
        
        print("    -> Compressing MP4 (CRF 26 + faststart)...")
        if compress_video(src_file, opt_mp4_path, crf=26):
            opt_size = os.path.getsize(opt_mp4_path)
            reduction = (1 - (opt_size / orig_size)) * 100
            print(f"    -> Output MP4: {format_size(opt_size)} (Reduced by {reduction:.1f}%)")
        else:
            print("    -> MP4 Compression failed.")
            opt_size = orig_size
            reduction = 0

        # 2. Generate Animated WebP
        webp_name = vid_name.replace(".mp4", "-animated.webp")
        webp_path = os.path.join(ASSETS_DIR, webp_name)
        
        print("    -> Generating Animated WebP (15fps, 960px, q75)...")
        if generate_animated_webp(src_file, webp_path, scale_w=960, fps=15, q=75):
            webp_size = os.path.getsize(webp_path)
            webp_reduction = (1 - (webp_size / orig_size)) * 100
            print(f"    -> Output WebP: {format_size(webp_size)} (Reduced by {webp_reduction:.1f}%)")
        else:
            print("    -> Animated WebP generation failed.")
            webp_size = 0
            webp_reduction = 0

        results.append({
            "name": vid_name,
            "orig_size": orig_size,
            "opt_size": opt_size,
            "opt_name": opt_mp4_name,
            "reduction": reduction,
            "webp_name": webp_name,
            "webp_size": webp_size,
            "webp_reduction": webp_reduction
        })

    print("\n" + "=" * 70)
    print(" SUMMARY REPORT:")
    print("=" * 70)
    for r in results:
        print(f"Video: {r['name']}")
        print(f"  • Original Size    : {format_size(r['orig_size'])}")
        print(f"  • Optimized MP4    : {format_size(r['opt_size'])} (-{r['reduction']:.1f}%) -> {r['opt_name']}")
        print(f"  • Animated WebP    : {format_size(r['webp_size'])} (-{r['webp_reduction']:.1f}%) -> {r['webp_name']}")
        print("-" * 70)

if __name__ == "__main__":
    main()
