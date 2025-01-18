import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import yt_dlp
from urllib.parse import unquote

# File paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(SCRIPT_DIR, "user_data_tiktok.json")
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "tiktok_videos")
DELETED_FOLDER = os.path.join(OUTPUT_FOLDER, "deleted_videos")
ACTIVE_FOLDER = os.path.join(OUTPUT_FOLDER, "active_videos")
COOKIE_FILE = os.path.join(SCRIPT_DIR, "Cookies.txt")
FAILED_LOG = os.path.join(OUTPUT_FOLDER, "failed_downloads.json")

def extract_video_url(link):
    try:
        if 'redirect_url=' in link:
            return unquote(link.split('redirect_url=')[1])
        return link
    except Exception:
        return link

def download_video(video_data, output_dir, video_type="video", max_retries=3):
    """Download a single video with retries"""
    retries = 0
    while retries < max_retries:
        try:
            video_url = extract_video_url(video_data.get('Link', ''))
            if not video_url:
                print(f"No video URL found in data")
                return False, None
                
            date = video_data.get('Date', '').replace(':', '-').replace(' ', '_')
            if not date:
                date = 'unknown_date'
                
            if video_type == "deleted":
                date_deleted = video_data['DateDeleted'].replace(':', '-').replace(' ', '_')
                filename = f"deleted_{date}_removed_{date_deleted}.mp4"
            else:
                filename = f"video_{date}.mp4"
            
            filepath = os.path.join(output_dir, filename)
            
            if os.path.exists(filepath):
                print(f"Video already exists: {filename}")
                return True, None
                
            # yt-dlp options with increased timeout
            ydl_opts = {
                'outtmpl': filepath,
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'cookiefile': COOKIE_FILE,
                'socket_timeout': 30,  # Increased timeout
                'retries': 5,  # Internal retries
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                        
            print(f"Successfully downloaded: {filename}")
            return True, None
            
        except Exception as e:
            retries += 1
            if retries < max_retries:
                print(f"Attempt {retries} failed, retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying
            else:
                error_info = {
                    'url': video_data.get('Link', ''),
                    'date': video_data.get('Date', ''),
                    'error': str(e),
                    'type': video_type
                }
                return False, error_info

def process_videos(videos, output_dir, video_type="video"):
    """Process a list of videos"""
    if not videos:
        return 0, 0, []
        
    print(f"\nProcessing {len(videos)} {video_type} videos...")
    failed_downloads = []
    
    with ThreadPoolExecutor(max_workers=2) as executor:  # Reduced workers to avoid overload
        futures = []
        for video in videos:
            futures.append(executor.submit(download_video, video, output_dir, video_type))
        
        successful = 0
        failed = 0
        
        for future in tqdm(futures, desc=f"Downloading {video_type} videos"):
            success, error_info = future.result()
            if success:
                successful += 1
            else:
                failed += 1
                if error_info:
                    failed_downloads.append(error_info)
    
    return successful, failed, failed_downloads

def save_failed_downloads(failed_downloads):
    """Save failed download information to a JSON file"""
    if failed_downloads:
        with open(FAILED_LOG, 'w', encoding='utf-8') as f:
            json.dump(failed_downloads, f, indent=2)
        print(f"\nFailed download information saved to: {FAILED_LOG}")

def download_all_tiktok_videos():
    """Main function to download all videos"""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(DELETED_FOLDER, exist_ok=True)
    os.makedirs(ACTIVE_FOLDER, exist_ok=True)
    
    print(f"Reading JSON file from: {JSON_FILE_PATH}")
    print(f"Using cookies from: {COOKIE_FILE}")
    print(f"Videos will be saved to:")
    print(f"- Deleted videos: {DELETED_FOLDER}")
    print(f"- Active videos: {ACTIVE_FOLDER}")
    
    all_failed_downloads = []
    
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_successful = 0
        total_failed = 0
        
        # Process deleted videos
        if 'Video' in data:
            deleted_videos = data['Video'].get('RecentlyDeletedPosts', {}).get('PostList', [])
            if deleted_videos:
                print(f"\nFound {len(deleted_videos)} deleted videos")
                successful, failed, failed_downloads = process_videos(deleted_videos, DELETED_FOLDER, "deleted")
                total_successful += successful
                total_failed += failed
                all_failed_downloads.extend(failed_downloads)
            
            # Process active videos
            active_videos = data['Video'].get('Videos', {}).get('VideoList', [])
            if active_videos:
                print(f"\nFound {len(active_videos)} active videos")
                successful, failed, failed_downloads = process_videos(active_videos, ACTIVE_FOLDER, "active")
                total_successful += successful
                total_failed += failed
                all_failed_downloads.extend(failed_downloads)
            else:
                print("\nNo active videos found in Videos.VideoList")
        
        # Save failed download information
        save_failed_downloads(all_failed_downloads)
        
        print(f"\nDownload complete!")
        print(f"Total successfully downloaded: {total_successful} videos")
        print(f"Total failed downloads: {total_failed} videos")
        if total_failed > 0:
            print(f"Check {FAILED_LOG} for details about failed downloads")
        
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file - Invalid JSON format: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp is not installed. Installing it now...")
        import subprocess
        subprocess.check_call(["pip", "install", "yt-dlp"])
        print("yt-dlp has been installed successfully!")
    
    # Verify files exist
    if not os.path.exists(COOKIE_FILE):
        print(f"Error: Cookie file not found at {COOKIE_FILE}")
        print("Please make sure Cookies.txt is in the same folder as this script.")
        exit(1)
        
    if not os.path.exists(JSON_FILE_PATH):
        print(f"Error: TikTok data file not found at {JSON_FILE_PATH}")
        print("Please make sure user_data_tiktok.json is in the same folder as this script.")
        exit(1)
        
    download_all_tiktok_videos()