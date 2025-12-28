# ♔ Chess AI Solver

A complete full-stack chess application with AI opponent, online multiplayer, and ELO ranking system.

## 🎯 Features

### Chess Engine
- ✅ Complete implementation of all official chess rules
- ✅ All piece movements (King, Queen, Rook, Bishop, Knight, Pawn)
- ✅ Special moves: Castling (kingside and queenside), En passant, Pawn promotion
- ✅ Game state detection: Check, Checkmate, Stalemate
- ✅ Draw conditions: Threefold repetition, 50-move rule, Insufficient material
- ✅ FEN (Forsyth-Edwards Notation) support

### Artificial Intelligence
- ✅ Minimax algorithm with Alpha-Beta pruning
- ✅ Advanced evaluation function (material, position, pawn structure, king safety)
- ✅ 3 difficulty levels (Easy, Medium, Hard)
- ✅ Opening book integration
- ✅ Performance optimized

### Backend API (FastAPI)
- ✅ RESTful API
- ✅ WebSocket support for real-time games
- ✅ PostgreSQL database for persistence
- ✅ Redis for sessions and matchmaking
- ✅ JWT authentication
- ✅ ELO rating system

### Frontend (React + TypeScript)
- ✅ Modern and responsive UI
- ✅ Interactive chess board
- ✅ Move highlighting
- ✅ Game history
- ✅ Multiple themes

### Game Modes
- ✅ **Local 2 Players**: Play with a friend on the same device
- ✅ **vs AI**: Play against the computer with adjustable difficulty
- ✅ **Online**: Play against players worldwide (WebSocket)
- ✅ **Matchmaking**: Automatic opponent matching by ELO rating

### User System
- ✅ Registration and authentication
- ✅ User profiles
- ✅ Game history
- ✅ Statistics tracking
- ✅ ELO ranking by time control (Blitz, Rapid, Classical)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Walluttt/chess_ai_solver.git
cd chess_ai_solver
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export DATABASE_URL="postgresql://chess_user:chess_password@localhost:5432/chess_db"
export REDIS_URL="redis://localhost:6379/0"
export SECRET_KEY="your-secret-key"
```

5. Start PostgreSQL and Redis:
```bash
# Using Docker
docker run -d -p 5432:5432 -e POSTGRES_USER=chess_user -e POSTGRES_PASSWORD=chess_password -e POSTGRES_DB=chess_db postgres:15
docker run -d -p 6379:6379 redis:7
```

6. Run the backend:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

4. Access the application at http://localhost:5173

## 📚 API Documentation

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user info

### Games

- `POST /api/games/create` - Create a new game
- `GET /api/games/{game_id}` - Get game state
- `POST /api/games/{game_id}/move` - Make a move
- `GET /api/games/user/history` - Get user's game history

### Users

- `GET /api/users/me` - Get current user profile
- `GET /api/users/{user_id}` - Get user profile
- `PUT /api/users/me` - Update profile

### Rankings

- `GET /api/rankings/leaderboard` - Get leaderboard
- `GET /api/rankings/user/{user_id}` - Get user ranking details

### WebSocket

- `WS /ws/game/{game_id}` - Real-time game updates

## 🏗️ Project Structure

```
chess_ai_solver/
├── backend/
│   ├── app/
│   │   ├── api/                  # API routes and WebSocket
│   │   ├── core/
│   │   │   ├── chess_engine/    # Chess logic
│   │   │   └── ai/              # AI implementation
│   │   ├── models/              # Database models
│   │   ├── services/            # Business logic
│   │   ├── database/            # Database connection
│   │   ├── config.py            # Configuration
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API and WebSocket clients
│   │   ├── context/             # React context providers
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🎮 How to Play

1. **Register/Login**: Create an account or login to access all features

2. **Start a Game**:
   - **Local**: Play against a friend on the same device
   - **vs AI**: Choose difficulty (Easy/Medium/Hard) and play against the computer
   - **Online**: Find an opponent through matchmaking

3. **Making Moves**:
   - Click on a piece to select it
   - Click on a highlighted square to move
   - Special moves (castling, en passant) are handled automatically

4. **Track Progress**:
   - View your profile for statistics
   - Check the leaderboard to see top players
   - Review your game history

## 🧪 Technologies Used

### Backend
- **Python 3.11+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **PostgreSQL** - Relational database
- **Redis** - Caching and sessions
- **JWT** - Authentication
- **WebSockets** - Real-time communication

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Socket.io** - WebSocket client

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 🎯 ELO Rating System

The application implements a standard ELO rating system:

- **Starting Rating**: 1200
- **K-Factor**: 32
- **Time Controls**:
  - Blitz: Fast-paced games
  - Rapid: Standard games
  - Classical: Longer, strategic games

Each time control has separate ratings and statistics.

## 🤖 AI Difficulty Levels

- **Easy (Depth 2)**: Good for beginners, makes basic moves
- **Medium (Depth 3)**: Intermediate level, considers tactics
- **Hard (Depth 4)**: Advanced level, strong strategic play

## 📝 Environment Variables

### Backend
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://host:port/db
SECRET_KEY=your-secret-key-here
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### Frontend
```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000
```

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS configured for security
- SQL injection protection via SQLAlchemy ORM
- Input validation with Pydantic

## 🚧 Future Enhancements

- [ ] OAuth integration (Google, GitHub)
- [ ] PGN import/export
- [ ] Game analysis with engine suggestions
- [ ] Tournament system
- [ ] Mobile app (React Native)
- [ ] Chess puzzles
- [ ] Friends system
- [ ] Chat functionality

## 📄 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Bug Reports

If you find a bug, please open an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Enjoy playing chess! ♔♕♖♗♘♙**
