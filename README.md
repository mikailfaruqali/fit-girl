# 🔗 Link Grabber

A powerful and user-friendly Windows desktop application for extracting download links from fuckingfast.co URLs. Built with Python and Tkinter, featuring a modern dark-themed interface.

![Link Grabber](https://img.shields.io/badge/version-1.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎯 **Batch Processing** - Extract multiple download links at once
- 🚀 **Fast & Reliable** - Multi-threaded link extraction with retry logic
- 💾 **Export to File** - Save extracted links as .txt file for IDM import
- 🎨 **Modern UI** - Clean, dark-themed interface with progress tracking
- ⏸️ **Pause/Resume** - Stop extraction anytime and save partial results
- 📊 **Real-time Progress** - Visual progress bar and detailed activity log
- 🖥️ **Standalone** - No Python installation required

## 📥 Download & Installation

### Option 1: Download Installer (Recommended)

1. **Download the latest release:**
   - [**Download LinkGrabber.exe**](https://github.com/YOUR_USERNAME/fit-girl/releases/latest/download/LinkGrabber.exe)

2. **Run the installer:**
   - Double-click `LinkGrabber.exe`
   - Follow the installation wizard
   - Choose installation location
   - Optionally create desktop shortcut

3. **Launch the app:**
   - Find "Link Grabber" in Start Menu or Desktop

### Option 2: Portable Version

Download the portable `.exe` from the [Releases](https://github.com/YOUR_USERNAME/fit-girl/releases) page and run directly without installation.

## 🚀 How to Use

### Step 1: Paste URLs
Copy your fuckingfast.co URLs and paste them into the text area. URLs can be in any format:
```
https://fuckingfast.co/xxxxxx#filename.zip
https://fuckingfast.co/xxxxxx#game-setup.exe
- https://fuckingfast.co/xxxxxx#file1.rar
* https://fuckingfast.co/xxxxxx#file2.rar
```

### Step 2: Extract Links
- Click the **"Start"** button to begin extraction
- Watch real-time progress in the activity log
- The app will process each URL and extract the direct download link

### Step 3: Save Links
- Click **"Save"** to export extracted links to a .txt file
- Choose your desired location and filename

### Step 4: Import to IDM (Internet Download Manager)
1. Open IDM
2. Go to **Tasks → Import → Import from text file**
3. Select your saved `.txt` file
4. All links will be added to IDM for downloading

## 📸 Screenshots

```
┌─────────────────────────────────────┐
│         🔗 Link Grabber             │
│  Extract fuckingfast.co links       │
├─────────────────────────────────────┤
│  Paste URLs Here                    │
│  ┌───────────────────────────────┐  │
│  │ https://fuckingfast.co/...    │  │
│  │ https://fuckingfast.co/...    │  │
│  └───────────────────────────────┘  │
│                                     │
│  [Start]  [Stop]  [Save]            │
│                                     │
│  ████████░░░░░░░░░ 45%              │
│                                     │
│  Activity Log                       │
│  ┌───────────────────────────────┐  │
│  │ ✓ [1/10] game-part1.rar       │  │
│  │ ✓ [2/10] game-part2.rar       │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## 🛠️ For Developers

### Prerequisites
```bash
pip install pyinstaller requests
```

### Building from Source

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/fit-girl.git
cd fit-girl
```

2. **Install dependencies:**
```bash
pip install requests
```

3. **Create the icon (optional):**
```bash
python create_icon.py
```

4. **Build the executable:**
```bash
python -m PyInstaller --onefile --noconsole --icon=icon.ico --name LinkGrabber link-grabber.py
```

5. **Find your executable:**
```
dist/LinkGrabber.exe
```

### Creating Installer

1. **Install Inno Setup:**
   - Download from [jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php)

2. **Compile installer:**
   - Open `installer.iss` with Inno Setup Compiler
   - Click **"Compile"**
   - Get installer from `output/LinkGrabber_Setup.exe`

## 📋 Requirements

- **For Users:** Windows 7/8/10/11 (64-bit)
- **For Developers:** Python 3.7+ with `requests` library

## 🔧 Technical Details

### How It Works
1. Parses input text for fuckingfast.co URLs
2. Sends HTTP requests with proper headers to avoid blocks
3. Extracts direct download links using regex pattern matching
4. Displays results in real-time with success/failure indicators
5. Exports links in IDM-compatible format

### Features in Detail
- **Multi-threaded Processing:** Uses Python threading for non-blocking UI
- **Error Handling:** Gracefully handles connection errors and timeouts
- **Smart Parsing:** Extracts URLs from various formats (plain, markdown lists, etc.)
- **Progress Tracking:** Real-time visual and text-based progress updates

## ❓ FAQ

**Q: Do I need Python installed?**  
A: No! The `.exe` version is standalone and works without Python.

**Q: Is this safe to use?**  
A: Yes! The source code is open and available for review. The app only extracts links from URLs you provide.

**Q: What if a link fails to extract?**  
A: The app will continue processing other URLs and show which ones failed. Common causes: invalid URL, server timeout, or link expired.

**Q: Can I use this with download managers other than IDM?**  
A: Yes! The exported `.txt` file contains one link per line, which works with most download managers.

**Q: Why are some links not found?**  
A: The website may have changed its structure, the link might be expired, or there might be network issues.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Users are responsible for complying with all applicable laws and website terms of service. The developers assume no liability for misuse of this software.

## 🐛 Issues & Support

If you encounter any issues or have questions:
- Open an [Issue](https://github.com/YOUR_USERNAME/fit-girl/issues)
- Check existing issues for solutions
- Provide details: error messages, screenshots, steps to reproduce

## 📊 Changelog

### Version 1.0 (November 2025)
- Initial release
- Batch URL processing
- Modern dark UI
- IDM integration
- Real-time progress tracking
- Export to text file

---

**Made with ❤️ for the gaming community**

*Note: Replace `YOUR_USERNAME` in the download links with your actual GitHub username before publishing.*
