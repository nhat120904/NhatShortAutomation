#!/usr/bin/env python3
"""
Script to clean m3u8 URLs from the content database
"""

import json
import os

def cleanup_content_database():
    """Remove m3u8 URLs from content database entries"""
    db_file = '.database/content_db.json'
    
    if not os.path.exists(db_file):
        print(f"Database file {db_file} not found.")
        return
    
    # Backup the original file
    backup_file = db_file + '.backup'
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy2(db_file, backup_file)
        print(f"Created backup: {backup_file}")
    
    # Load the database
    with open(db_file, 'r') as f:
        db_content = json.load(f)
    
    # Check if the database has a content_documents wrapper
    if 'content_documents' in db_content:
        content_docs = db_content['content_documents']
    else:
        content_docs = db_content
    
    cleaned_count = 0
    total_entries = len(content_docs)
    
    print(f"Processing {total_entries} database entries...")
    
    for entry_id, entry_data in content_docs.items():
        modified = False
        
        # Check for background_video_url with m3u8
        if 'background_video_url' in entry_data and entry_data['background_video_url'].endswith('index.m3u8'):
            print(f"Entry {entry_id}: Removing m3u8 background_video_url")
            del entry_data['background_video_url']
            modified = True
        
        # Check for background_video_duration that might be associated with m3u8
        if modified and 'background_video_duration' in entry_data:
            print(f"Entry {entry_id}: Removing associated background_video_duration")
            del entry_data['background_video_duration']
        
        # Check for background_trimmed that might be associated with m3u8
        if modified and 'background_trimmed' in entry_data:
            trimmed_file = entry_data['background_trimmed']
            if os.path.exists(trimmed_file):
                print(f"Entry {entry_id}: Removing trimmed background file: {trimmed_file}")
                try:
                    os.remove(trimmed_file)
                except Exception as e:
                    print(f"Warning: Could not remove {trimmed_file}: {e}")
            del entry_data['background_trimmed']
        
        if modified:
            cleaned_count += 1
    
    # Save the cleaned database
    with open(db_file, 'w') as f:
        json.dump(db_content, f, indent=2)
    
    print(f"\nCleaned {cleaned_count} out of {total_entries} entries.")
    print(f"Database updated: {db_file}")

if __name__ == "__main__":
    print("Content Database M3U8 Cleanup")
    print("=" * 40)
    
    response = input("This will remove m3u8 URLs from the database. Continue? (y/N): ")
    if response.lower() == 'y':
        cleanup_content_database()
        print("\nDone!")
    else:
        print("Operation cancelled.") 