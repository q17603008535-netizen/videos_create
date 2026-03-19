#!/usr/bin/env python3
"""
Video Re-creation Pipeline
Run: python backend/pipeline.py <video_filename>
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.video_reader import list_videos
from services.transcriber import transcribe
from services.analyzer import analyze_content
from services.rewriter import rewrite_content
from services.reviewer import review_content
from services.script_generator import generate_script

VIDEOS_DIR = "data/videos"
OUTPUT_DIR = "data/outputs"


def process_video(video_filename: str):
    """Process a single video through the complete SOP"""
    video_path = os.path.join(VIDEOS_DIR, video_filename)
    
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return None
    
    print(f"📁 Processing: {video_filename}")
    
    transcript = transcribe(video_path)
    print(f"🎤 Step 1/6: Transcribed ({len(transcript['text'])} chars)")
    
    analysis = analyze_content(transcript["text"])
    print(f"🔍 Step 2/6: Analyzed (Topic: {analysis['main_topic']})")
    
    rewrites = rewrite_content(transcript["text"], analysis)
    print(f"✍️  Step 3/6: Generated {len(rewrites)} versions")
    
    print("📊 Step 4/6: Reviewing versions...")
    reviewed_versions = []
    for i, version in enumerate(rewrites):
        review = review_content(version["content"])
        reviewed_versions.append({
            **version,
            "review": review
        })
        print(f"   ✓ Version {i+1} scored: {review['originality_score']}/100")
    
    print("📝 Step 5/6: Generating final script...")
    best_version = max(reviewed_versions, key=lambda v: v["review"]["originality_score"])
    script = generate_script(best_version["content"])
    print(f"   ✓ Script generated")
    
    print("💾 Step 6/6: Saving output...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_name = Path(video_filename).stem
    
    script_path = os.path.join(OUTPUT_DIR, f"{output_name}_script.md")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script["markdown"])
    
    result_path = os.path.join(OUTPUT_DIR, f"{output_name}_result.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump({
            "transcript": transcript,
            "analysis": analysis,
            "versions": reviewed_versions,
            "final_script": script,
            "best_version_index": reviewed_versions.index(best_version) + 1
        }, f, ensure_ascii=False, indent=2)
    
    print(f"   ✓ Saved to {OUTPUT_DIR}/")
    print(f"\n✅ Complete! Best version: #{reviewed_versions.index(best_version) + 1}")
    print(f"📄 Script: {script_path}")
    
    return {
        "script_path": script_path,
        "best_version": reviewed_versions.index(best_version) + 1,
        "versions": reviewed_versions
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python backend/pipeline.py <video_filename>")
        print("\nAvailable videos:")
        videos = list_videos()
        for v in videos:
            print(f"  - {v['filename']}")
        sys.exit(1)
    
    video_filename = sys.argv[1]
    process_video(video_filename)


if __name__ == "__main__":
    main()
