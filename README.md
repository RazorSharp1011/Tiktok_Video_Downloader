# TikTok Video Downloader

A Python script that helps you download all your TikTok videos from your data export, including both active and deleted videos.

## Complete Setup Guide (Step by Step)

### 1. Install Required Software

#### Install Visual Studio Code (VS Code)
1. Go to https://code.visualstudio.com/
2. Click the big blue download button
3. Open the downloaded file
4. Follow installation steps (use all default settings)
5. Open VS Code after installation

#### Install Python
1. Go to https://www.python.org/downloads/
2. Click "Download Python" (latest version)
3. Open the downloaded file
4. **VERY IMPORTANT**: Check the box that says "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete
7. Click "Close"

#### Set up VS Code for Python
1. Open VS Code
2. Click the Extensions icon on the left sidebar (looks like 4 squares)
3. Type "Python" in the search bar
4. Find "Python" by Microsoft (should be the first result)
5. Click "Install"
6. Wait for installation to complete
7. Click "Reload" if asked

### 2. Get Your TikTok Files Ready

#### Request Your TikTok Data
1. Go to TikTok in your web browser
2. Click your profile picture
3. Click "Settings and privacy"
4. Under "Account", find and click "Download your data"
5. Make sure "JSON" format is selected
6. Click "Request data"
7. Wait for email from TikTok (can take several days)
8. When you get the email, click the download link
9. Download and unzip the file
10. Find "user_data_tiktok.json" in the unzipped files
11. Keep this file handy - you'll need it later

#### Get Your Cookies File
1. Install Cookie Editor extension:
   - For Chrome:
     * Go to Chrome Web Store https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?pli=1
     * Click "Add to Chrome"
     * Click "Add extension"
    - For Edge:
     * Go to Edge Web Store https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi
     * Click "Add to Chrome"
     * Click "Add extension"
   - For Firefox:
     * Go to Firefox Add-ons
     * Search for "Cookie Editor"
     * Click "Add to Firefox"
     * Click "Add"

2. Export your cookies:
   * Go to TikTok.com
   * Make sure you're logged in
   * Click the Cookie Editor extension icon (looks like a cookie)
   * Click "Export" in the bottom right
   * Click "Netscape" format (IMPORTANT: must be Netscape)
   * It will copy to your clipboard
   * Open Notepad (or any text editor)
   * Paste the cookies
   * Save the file as "Cookies.txt"
   * Remember where you saved it

### 3. Get the Script and Set It Up

#### Download the Script
1. Go to the script file (tiktok_downloader.py) in this repository
2. Click on the file to view it
3. Click the "Raw" button (top right of code)
4. Right-click anywhere on the page
5. Click "Save as" or "Save page as"
6. Name it "tiktok_downloader.py"
   - Make sure it saves as .py (not .txt)
   - If using Windows, choose "All Files" in the save type dropdown
7. Choose where to save it (pick a folder you can find easily)

#### Organize Your Files
1. Create a new folder on your computer (name it something like "TikTok Downloader")
2. Put these three files in that folder:
   - tiktok_downloader.py (the script you just downloaded)
   - user_data_tiktok.json (from your TikTok data)
   - Cookies.txt (from Cookie Editor)
3. Double check the names are exactly correct:
   - No extra spaces
   - Correct capitalization
   - Correct file extensions

#### Install Python Packages
1. Open VS Code
2. Click "File" → "Open Folder"
3. Find and select the folder you created
4. Click "Terminal" at the top
5. Click "New Terminal"
6. Type these commands (one at a time):
```bash
pip install yt-dlp
pip install tqdm
```
7. Press Enter after each command and wait for installation to complete
8. If unable to download packages using those commands try the following commands
```bash
python -m pip install yt-dlp
python -m pip install tqdm
```

### 4. Run the Script
1. In VS Code, click on tiktok_downloader.py in the left sidebar
2. Click the Play button (triangle) in the top right, OR
3. Right-click in the code and select "Run Python File in Terminal"

The script will:
- Create a 'tiktok_videos' folder
- Download active videos to 'tiktok_videos/active_videos'
- Download deleted videos to 'tiktok_videos/deleted_videos'
- Create a list of any failed downloads

### Common Problems and Solutions

#### "Python is not recognized..."
- Restart your computer
- Reinstall Python (remember to check "Add Python to PATH")

#### "No module named yt-dlp" or "No module named tqdm"
Run these commands again:
```bash
pip install yt-dlp
pip install tqdm
```

#### "Cookie file not found" or "JSON file not found"
- Check file names are exactly correct
- Make sure files are in the same folder as the script
- Make sure you're opening the right folder in VS Code

#### If Downloads Fail
- Check your internet connection
- Make sure you're still logged into TikTok
- Try getting fresh cookies from Cookie Editor

### Need More Help?
- Check if someone else had the same problem in the Issues tab
- Create a new Issue if you can't find a solution
- Describe exactly what's happening and what you've tried

### Script Features
- Downloads both active and deleted videos
- Skips videos you already downloaded
- Names files with the original upload date
- Creates separate folders for active and deleted videos
- Logs any failed downloads
- Automatically retries failed downloads

### Important Notes
- The script only works with your own videos (from your data export)
- Keep your Cookies.txt file private
- Some videos might fail if they were deleted by TikTok
- Large files might take time to download
- The script will create all needed folders automatically
