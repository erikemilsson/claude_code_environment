# Todo API

A REST API for managing todo items with user authentication.

## Features

- User registration and login
- JWT-based authentication
- CRUD operations for todos
- Filter and search todos
- Mark todos as complete

## Quick Start

```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env

# Run database migrations
npm run migrate

# Start development server
npm run dev
```

## API Endpoints

### Auth
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT

### Todos
- `GET /todos` - List user's todos
- `POST /todos` - Create todo
- `GET /todos/:id` - Get single todo
- `PUT /todos/:id` - Update todo
- `DELETE /todos/:id` - Delete todo

## Development

This project uses a Claude Code environment for task management. See `.claude/` folder for:
- Task tracking in `.claude/tasks/`
- Project context in `.claude/context/overview.md`

## License

MIT
