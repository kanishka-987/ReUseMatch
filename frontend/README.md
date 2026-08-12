# ♻️ ReUseMatch Frontend SPA

An interactive, high-performance React + Vite + Tailwind CSS single page application (SPA) prototype for **ReUseMatch**, an autonomous multi-agent platform for circular item reuse.

## 🚀 Quick Start

### Prerequisites
- Node.js (v18.x or higher recommended)
- npm (v9.x or higher)

### Setup & Run
1. Navigate into the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser at `http://localhost:3000`.

---

## 💻 Tech Stack
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS, Glassmorphism, CSS Custom Utilities
- **Icons**: Lucide React
- **Routing**: React Router DOM v6
- **Data & Mocking**: Custom Promises API service, localStorage persistence

---

## 🛠️ Connecting to FastAPI Backend Later

When ready to connect to the real FastAPI backend:
1. Update `src/services/api.js` to replace mock delay handlers with `axios` HTTP calls targeting `import.meta.env.VITE_API_BASE_URL`.
2. Configure CORS in `backend/app.py` to permit requests from `http://localhost:3000`.
3. Set `VITE_USE_MOCK_DATA="false"` in your local `.env` file.
