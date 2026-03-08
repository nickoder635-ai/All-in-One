# 🛠️ All in One

![Uploading new.png…]()

**All in One** is a powerful desktop application that combines multiple tools, games, PDF utilities, and AI agents in a modern GUI with icons and animations. Every user action is logged in the **History** section.

---

## 🚀 Features

### 🧰 Tools

1. **Converter** – Supports 5 file types: Picture, Document, Subtitle, Video, Audio  
2. **File Organizer** – Automatically sorts messy files into categorized folders  
3. **Password Generator** – Character sets: `A-Z`, `a-z`, `0-9`, `#$%`, option to prevent repetition, max length 50 characters  
4. **World Dates** – Shows current date in Gregorian, Solar Hijri, and Lunar Hijri calendars, and converts custom dates between calendar types  

### 🎮 Games

1. **Tic Tac Toe (XO)** – Difficulty: Easy, Medium, Hard, Professional; Themes: Dark, Classic  
2. **Chess** – Difficulty: Easy, Medium, Hard; Themes: Classic, Dark  

### 📄 PDF Tools

- Rotate PDF  
- Delete Pages PDF  
- Protect PDF  
- Unlock PDF  
- Merge PDF  
- Split PDF  

### 🤖 AI Agents

**AI Research Agent** – Accepts a topic and automatically searches the web, summarizes, translates, and exports results. Supports 8 languages: English, Persian, French, German, Arabic, Spanish, Italian, Turkish. Outputs: TXT, MD, DOCX, PDF (PDF supports RTL languages).  

---

## 🛠 Tech Stack

Python 3.10+, PySide6, PyPDF2, Ollama, DDGS, Pillow, PySRT, WebVTT, Python-docx, Arabic Reshaper, ReportLab, Python-Bidi, Pathlib, dotenv, PikePDF, Chess  

---

## 📦 Installation

1. Clone the repository:  
`git clone https://github.com/Mahdi-Haqiqat/All-in-One.git`  
`cd All-in-One`  

2. Install dependencies using `requirements.txt`:  
`pip install -r requirements.txt`  

Or manually:  
`pip install PySide6 PyPDF2 ollama ddgs pillow pysrt webvtt docx python-docx arabic_reshaper reportlab python-bidi pathlib dotenv pikepdf chess`  

3. Ensure FFmpeg is installed next to the main application:  
`ffmpeg/bin/ffmpeg.exe`  

4. Run the application:  
`python run.py`  

---

## 🗂 Project Structure

All in One/  
├── run.py  
├── user_settings.json  
├── .env  
├── history.db  
├── app/  
│   ├── __init__.py  
│   ├── main.py  
│   └── window.py  
├── core/  
│   ├── __init__.py  
│   ├── tools/  
│   │   ├── __init__.py  
│   │   ├── converter/  
│   │   │   ├── __init__.py  
│   │   │   ├── picture.py  
│   │   │   ├── audio.py  
│   │   │   ├── document.py  
│   │   │   ├── subtitle.py  
│   │   │   ├── video.py  
│   │   │   └── DejaVuSans.ttf  
│   │   ├── organizer/  
│   │   │   ├── __init__.py  
│   │   │   └── logic.py  
│   │   └── password/  
│   │       ├── __init__.py  
│   │       └── generator.py  
│   ├── games/  
│   │   ├── __init__.py  
│   │   └── tic_tac_toe/  
│   │       ├── __init__.py  
│   │       └── engine.py  
│   ├── pdf_tools/  
│   │   ├── __init__.py  
│   │   ├── rotate/rotate.py  
│   │   ├── merge/merge.py  
│   │   ├── delete_pages/delete_pages.py  
│   │   ├── protect/protect.py  
│   │   └── unlock/unlock.py  
│   ├── ai_agents/  
│   │   ├── __init__.py  
│   │   └── researcher/  
│   │       ├── __init__.py  
│   │       ├── agent.py  
│   │       └── DejaVuSans.ttf  
│   ├── workers/  
│   │   ├── __init__.py  
│   │   ├── api_set_worker.py  
│   │   ├── research_worker.py  
│   │   └── convert_worker.py  
│   └── settings/  
│       ├── __init__.py  
│       ├── sidebar_connections.py  
│       ├── signals.py  
│       └── settings.py  
├── ffmpeg/  
│   └── bin/  
│       └── ffmpeg.exe  
├── ui/  
│   ├── __init__.py  
│   ├── animations/  
│   │   ├── __init__.py  
│   │   ├── home_animation.py  
│   │   └── sidebar_animation.py  
│   ├── footer/  
│   │   ├── __init__.py  
│   │   └── footer.py  
│   ├── views/  
│   │   ├── home/  
│   │   │   ├── __init__.py  
│   │   │   └── home_view.py  
│   │   ├── tools/  
│   │   │   ├── __init__.py  
│   │   │   ├── converter/  
│   │   │   │   ├── __init__.py  
│   │   │   │   ├── converter_view.py  
│   │   │   │   ├── type_buttons.py  
│   │   │   │   └── drag_drop.py  
│   │   │   ├── organizer_view.py  
│   │   │   ├── password_view.py  
│   │   │   └── date_view.py  
│   │   ├── games/  
│   │   │   ├── __init__.py  
│   │   │   └── tictactoe_view.py  
│   │   ├── pdf_tools/  
│   │   │   ├── __init__.py  
│   │   │   ├── rotate/rotate_view.py  
│   │   │   ├── delete_pages/delete_pages_view.py  
│   │   │   ├── merge/merge_view.py  
│   │   │   ├── protect/protect_view.py  
│   │   │   └── unlock/unlock_view.py  
│   │   ├── ai_agents/researcher/researcher_view.py  
│   │   └── history/history_view.py  
│   ├── icons/  
│   ├── settings/theme.py  
│   ├── sidebar/  
│   │   ├── __init__.py  
│   │   ├── sidebar.py  
│   │   └── sections/  
│   │       ├── __init__.py  
│   │       ├── tools_section.py  
│   │       ├── games_section.py  
│   │       ├── pdf_tools_section.py  
│   │       ├── ai_agents_section.py  
│   │       └── history_section.py  
│   └── stop/stop_manager.py  

---

## 📝 Logging System

All actions are recorded in the **History** section. Each operation stores: Date & Time, Operation type, Input/output details, Execution status.  

---

## ⚠️ Important Notes

- Internet connection is required for AI Agents  
- Ollama Cloud models must be accessible  
- Ensure `ffmpeg.exe` is executable  
- PDF export for RTL languages requires `DejaVuSans.ttf`  

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Mahdi-Haqiqat/All-in-One/tree/main?tab=MIT-1-ov-file) file for details.
