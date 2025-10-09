# TaskFlow: Task Management Workshops

Series of hands-on workshops for learning CI/CD methods through building a modern task management application.

## 🎯 Project: TaskFlow
A collaborative task management platform where you build a full-stack application from scratch, learning modern development practices at each step.

**Final Result**: A production-ready Kanban-style task manager with team collaboration, real-time updates, and automated deployment.

## 📚 Workshop Series Overview

### **Workshop 1: Python Backend & Testing Fundamentals**
- **Focus**: TDD, FastAPI, pytest, UV environment management
- **Domain**: Core task management API (CRUD operations)
- **Skills**: RESTful APIs, automated testing, error handling
- **Deliverable**: Complete backend service with 95%+ test coverage

### **Workshop 2: TypeScript Frontend & Integration**
- **Focus**: React development, cross-service testing, real-time UI
- **Domain**: Interactive Kanban boards, task visualization
- **Skills**: Component testing, API integration, responsive design
- **Deliverable**: Full-stack application with synchronized frontend/backend

### **Workshop 3: Production & Advanced CI/CD**
- **Focus**: DevOps, monitoring, scaling, multi-environment deployment
- **Domain**: User authentication, team features, performance optimization
- **Skills**: Production deployments, containerization, advanced workflows
- **Deliverable**: Production-ready platform with automated DevOps

## 🏗️ Project Architecture

```
taskflow/
├── backend/               # FastAPI Python service
│   ├── src/              # Application code
│   ├── tests/            # Backend tests
│   ├── pyproject.toml    # UV dependencies
│   └── Dockerfile        # Containerization
├── frontend/             # React TypeScript service
│   ├── src/              # Component code
│   ├── tests/            # Frontend tests
│   ├── package.json      # Node dependencies
│   └── Dockerfile        # Containerization
├── docs/                 # Workshop documentation
├── .github/workflows/    # CI/CD pipelines
└── docker-compose.yml    # Multi-service orchestration
```

## 🚀 Learning Path

### **Red-Green-Refactor Cycle**
1. **Write failing tests (Red)** → Define expected behavior
2. **Implement minimal code (Green)** → Make tests pass
3. **Refactor and optimize** → Improve code quality
4. **Commit and CI/CD** → Automate testing and deployment

### **Technical Stack**
- **Backend**: FastAPI + Python 3.11+ + UV package management
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Testing**: pytest + Jest + React Testing Library
- **Database**: In-memory → SQLite → PostgreSQL progression
- **CI/CD**: GitHub Actions with multi-service pipelines
- **Containerization**: Docker + docker-compose

## 📋 Prerequisites

- **Python 3.11+** and **uv** package manager
- **Node.js 18+** and **npm** or **yarn**
- **Git** and **GitHub account**
- **Code editor** (VS Code recommended)
- Basic knowledge of Python and JavaScript

## 🎯 Workshop Milestones

### **Workshop 1 Objectives**
- [ ] Set up UV environment and project structure
- [ ] Implement RESTful API for task management
- [ ] Write comprehensive unit tests with mocking
- [ ] Configure automated testing with GitHub Actions
- [ ] Practice TDD methodology and error handling

### **Workshop 2 Objectives**
- [ ] Build responsive React/TypeScript frontend
- [ ] Implement Kanban board drag-and-drop interface
- [ ] Write integration tests across services
- [ ] Add real-time synchronization features
- [ ] Deploy multi-service application

### **Workshop 3 Objectives**
- [ ] Add user authentication and permissions
- [ ] Implement database persistence
- [ ] Set up production CI/CD pipelines
- [ ] Add monitoring and error tracking
- [ ] Deploy to production environment

## 📖 Workshop Documentation

Detailed instructions for each workshop:

- **[Workshop 1: Backend & Testing](docs/workshop-1-backend.md)** - FastAPI fundamentals
- **[Workshop 2: Frontend & Integration](docs/workshop-2-frontend.md)** - React development
- **[Workshop 3: Production & DevOps](docs/workshop-3-production.md)** - Advanced CI/CD

## 🛠️ Getting Started

### **Installation**
```bash
# Clone repository
git clone https://github.com/umons-ig/edl-tp-1.git
cd edl-tp-1

# Choose your workshop branch
git checkout workshop-1  # For backend fundamentals
```

### **Quick Setup**
```bash
# Workshop 1: Backend setup
cd backend
uv sync  # Install dependencies
uv run pytest  # Run tests

# Workshop 2: Frontend setup (coming soon)
cd frontend
npm install  # Install dependencies
npm test     # Run tests
```

## 🤝 Learning Approach

Each workshop follows a **guided discovery** format:
- **Starter code** with intentional gaps and TODOs
- **Test-driven development** approach
- **Progressive disclosure** - learn one concept at a time
- **Practical exercises** with immediate feedback
- **Real-world challenges** and edge cases

## 📊 Assessment Criteria

### **Technical Excellence**
- Code follows modern best practices
- Comprehensive test coverage maintained
- Proper error handling and validation
- Clean, readable code structure

### **CI/CD Implementation**
- Automated testing on every commit
- Consistent code quality checks
- Successful automated deployments
- Proper environment management

### **Problem-Solving**
- Effective use of available resources
- Creative solutions to requirements
- Proper debugging techniques
- Collaboration and communication

## 🏆 Final Deliverables

By the end of Workshop 3, you will have built:

✅ **Functional task management application**
✅ **Automated CI/CD pipelines**
✅ **Production deployment capabilities**
✅ **Comprehensive test suite**
✅ **Modern full-stack architecture**
✅ **Team collaboration features**

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)
- [UV Package Manager](https://docs.astral.sh/uv/)

## 🤝 Contributing

Found an issue or have an improvement suggestion? Please open an issue or submit a pull request.

## 📄 License

Educational workshop materials - see individual workshop documentation for licensing details.

---

**Ready to start building?** Head to [Workshop 1: Backend Fundamentals](docs/workshop-1-backend.md) to begin your journey!