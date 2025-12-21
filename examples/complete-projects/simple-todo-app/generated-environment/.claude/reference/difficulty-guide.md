# Task Difficulty Guide

## Difficulty Scoring (1-10 Scale)

### 1-2: Trivial
- Fix typos or update text
- Change colors or basic styles
- Update configuration values
- Add console logs

### 3-4: Low
- Basic CRUD operations
- Simple UI components
- Form validation
- API endpoint integration

### 5-6: Moderate
- Complex forms with validation
- Multi-step workflows
- State management
- Error handling
- Testing implementation

### 7-8: High (Must Break Down)
- Authentication setup
- Database migrations
- Complex algorithms
- Performance optimization
- Security implementation

### 9-10: Extreme (Must Break Down)
- Architecture changes
- System integration
- Distributed systems
- Complex refactoring
- Infrastructure setup

## Breaking Down High-Difficulty Tasks

Tasks with difficulty >= 7 MUST be broken down into subtasks with difficulty <= 6.

Example breakdown:
- Parent Task (difficulty 8): "Implement authentication system"
  - Subtask 1 (difficulty 4): "Set up auth library"
  - Subtask 2 (difficulty 5): "Create login form"
  - Subtask 3 (difficulty 6): "Implement JWT handling"
  - Subtask 4 (difficulty 5): "Add auth guards to routes"