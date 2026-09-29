# ComicCraft – AI Comic Story Creator

**Team ID:** SWTID-2026-8799  
**Team Name:** SnapHunters

ComicCraft is a web application that turns a story idea into a short comic. It uses Google Gemini to create a comic outline and panel dialogues, generates panel artwork, shows a comic preview, and exports the finished comic as a PDF.

## Team members

| Role | Name |
| --- | --- |
| Team Leader | NANDHINI A — 259F36CF6C592588A4A4219EF1BCF153 |
| Member | Shanjana N — E4413DCAF59A75EB3EF4534B5470B1AF |
| Member | PAVITHRA D — D5078C617E09F9AA13041B7683D8CEFF |
| Member | A Anisha — ECFC6F2BE0DB0EA91DC434C012867F6F |
| Member | Harini V — 767BB548150EA72B110448D80AB0164C |

## Features

- Enter a story prompt, genre, tone, and number of panels
- Generate a comic outline using the Gemini API
- Generate story text and dialogue for every panel
- Create AI comic-panel images
- Preview the completed comic in the browser
- Export the comic as a PDF

## Technology used

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, Jinja2 templates
- **AI story generation:** Google Gemini API
- **Image generation:** Diffusers, Transformers, PyTorch
- **PDF export:** FPDF2

## Run the project locally

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Create and activate a Python virtual environment.
4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Create a file called `.env` in the main project folder and add your Gemini key:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

6. Start the application:

   ```powershell
   uvicorn app.main:app --reload
   ```

7. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser.

## Note

The `.env` file is intentionally not included in this repository because it contains a private API key. Gemini may occasionally return a temporary high-demand error; try again after a few minutes if that happens.

