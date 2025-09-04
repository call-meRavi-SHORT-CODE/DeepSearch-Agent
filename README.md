[![DeepSeek R1](https://img.shields.io/badge/DeepSeek--R1-%23000000.svg?style=flat&logo=ai&logoColor=white)](https://deepseek.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-%23009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js%2014-%23000000.svg?style=flat&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-%2306B6D4.svg?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Tavily](https://img.shields.io/badge/Tavily-%23333.svg?style=flat&logo=search&logoColor=white)](https://tavily.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-%233776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-%23339933.svg?style=flat&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-%23181717.svg?style=flat&logo=github&logoColor=white)](https://github.com/<your-org>/<your-repo>/pulls)



# DeepVision Research AI Agent

Advanced AI-powered deep research agent that conducts comprehensive analysis through multiple AI agents, web search integration, and iterative reflection cycles to generate detailed research reports.

## 🎯 **Project Purpose**

DeepVision is a sophisticated research automation system that:
- **Automates Research Workflows**: From initial query to comprehensive report generation
- **Multi-Agent Architecture**: Uses specialized AI agents for different research phases
- **Web Search Integration**: Powered by Tavily for real-time information gathering
- **Iterative Refinement**: Multiple reflection cycles for improved accuracy and depth
- **Professional Output**: Generates structured markdown reports ready for academic/professional use

## 🏗️ **System Architecture**

### **Backend (FastAPI)**
- **Research Engine**: Multi-agent research pipeline
- **Search Integration**: Tavily API for comprehensive source gathering
- **Agent Orchestration**: Coordinates 6 specialized AI agents
- **RESTful API**: Clean endpoints for frontend integration

### **Frontend (Next.js)**
- **Modern UI**: Professional research interface
- **Real-time Updates**: Loading states and completion animations
- **Markdown Rendering**: Beautiful display of research reports
- **Responsive Design**: Works on all devices

### **AI Agents**
1. **ReportStructureAgent**: Creates research outline and structure
2. **FirstSearchAgent**: Generates optimized search queries
3. **FirstSummaryAgent**: Creates initial content summaries
4. **ReflectionAgent**: Identifies areas for improvement
5. **ReflectionSummaryAgent**: Refines summaries based on reflection
6. **ReportFormattingAgent**: Generates final formatted report

## 🚀 **Quick Start**

### **Option 1: Automated Startup (Recommended)**
```bash
# Windows
start.bat

# PowerShell
.\start.ps1
```

### **Option 2: Manual Setup**
```bash
# 1. Clone and navigate to project
cd "DeepSearch Agent"

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start FastAPI backend
python app.py

# 4. In new terminal, start frontend
cd DeepVision
npm install
npm run dev
```

## 🔑 **API Key Setup**

### **Required API Keys**

#### **1. Tavily API Key (Required)**
- **Purpose**: Web search and content retrieval
- **Get it here**: [https://tavily.com/](https://tavily.com/)
- **Cost**: Free tier available, paid plans for higher usage
- **Setup**: 
  1. Visit [Tavily](https://tavily.com/)
  2. Sign up for free account
  3. Go to API Keys section
  4. Copy your API key

#### **2. AI Model API Keys (Required)**
- **Purpose**: AI agent reasoning and content generation
- **Options**: OpenAI, Anthropic, or other compatible providers
- **Setup**: Configure in your `config.py` file

### **Configuration File Setup**

Create `config.py` in your project root:

```python
class config:
    # Tavily Search API
    TAVILY_API_KEY = "your_tavily_api_key_here"
    
    # AI Model Configuration
    OPENAI_API_KEY = "your_openai_api_key_here"  # or your preferred provider
    OPENAI_BASE_URL = "https://api.openai.com/v1"  # adjust as needed
    
    # Model Names
    LLM_REASONING = "gpt-4"  # for complex reasoning tasks
    LLM_REGULAR = "gpt-3.5-turbo"  # for general tasks
```

## 📋 **Requirements**

### **System Requirements**
- **Python**: 3.8+ (3.9+ recommended)
- **Node.js**: 18+ (20+ recommended)
- **RAM**: 4GB+ (8GB+ recommended)
- **Storage**: 2GB+ free space

### **Python Dependencies**
```
fastapi==0.104.1          # Web framework
uvicorn[standard]==0.24.0 # ASGI server
pydantic==2.5.0           # Data validation
tavily-python==0.3.1      # Search API client
python-multipart==0.0.6   # File upload support
requests==2.31.0           # HTTP library
```

### **Node.js Dependencies**
```
Next.js 14                 # React framework
React 18                   # UI library
Tailwind CSS               # Styling
Framer Motion              # Animations
Radix UI                   # Component library
```

## 🔧 **Installation Steps**

### **1. Environment Setup**
```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### **2. Frontend Setup**
```bash
# Navigate to frontend directory
cd DeepVision

# Install Node.js dependencies
npm install
# or
yarn install
# or
pnpm install
```

### **3. Configuration**
```bash
# 1. Copy config template
cp config.example.py config.py

# 2. Edit config.py with your API keys
# 3. Ensure all required keys are set
```

## 🏃‍♂️ **How to Run**

### **Development Mode**
```bash
# Terminal 1: Backend
python app.py
# Backend will be available at: http://localhost:8000

# Terminal 2: Frontend
cd DeepVision
npm run dev
# Frontend will be available at: http://localhost:3000
```

### **Production Mode**
```bash
# Backend
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
cd DeepVision
npm run build
npm start
```

## 🌐 **API Endpoints**

### **Core Endpoints**
- **`POST /api/research`**: Submit research queries
- **`GET /api/health`**: System health check
- **`GET /docs`**: Interactive API documentation

### **Research Request Format**
```json
{
  "query": "Your research question here",
  "num_reflections": 2,
  "num_results_per_search": 3,
  "cap_search_length": 40000
}
```

### **Response Format**
```json
{
  "status": "completed",
  "message": "Research completed successfully",
  "final_report": "# Your Research Report\n\n## Section 1...",
  "error": ""
}
```

## 📊 **Research Process**

### **1. Query Processing**
- User submits research question
- AI analyzes and structures the query
- Research outline generated

### **2. Information Gathering**
- Multiple search iterations
- Source evaluation and filtering
- Content extraction and analysis

### **3. Content Analysis**
- AI agents process information
- Summaries created and refined
- Multiple reflection cycles

### **4. Report Generation**
- Structured markdown output
- Professional formatting
- Ready for academic/professional use

## 🎨 **Customization**

### **Modifying Research Parameters**
```python
# In app.py, adjust these values:
NUM_REFLECTIONS = 3              # More reflection cycles
NUM_RESULTS_PER_SEARCH = 5       # More search results
CAP_SEARCH_LENGTH = 50000        # Longer content processing
```

### **Adding New AI Agents**
1. Create agent class in `agents.py`
2. Add to research pipeline in `app.py`
3. Update response handling

### **UI Customization**
- Modify `DeepVision/components/hero.tsx`
- Update `DeepVision/app/globals.css`
- Customize Tailwind classes

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Backend Won't Start**
```bash
# Check if port 8000 is free
netstat -an | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# Kill process using port
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # macOS/Linux
```

#### **Frontend Won't Start**
```bash
# Check if port 3000 is free
netstat -an | findstr :3000   # Windows
lsof -i :3000                 # macOS/Linux

# Clear Next.js cache
cd DeepVision
rm -rf .next
npm run dev
```

#### **API Key Errors**
```bash
# Verify config.py exists and has correct keys
# Check API key validity
# Ensure virtual environment is activated
```

#### **Module Import Errors**
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check Python path
python -c "import agents; print('OK')"
```

### **Debug Mode**
```bash
# Backend with debug logging
uvicorn app:app --reload --log-level debug

# Frontend with verbose output
cd DeepVision
DEBUG=* npm run dev
```

## 📚 **Documentation & Resources**

### **API Documentation**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### **Useful Links**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Tavily API Docs](https://docs.tavily.com/)

## 🤝 **Contributing**

### **Development Setup**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test thoroughly
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Submit pull request

### **Code Style**
- **Python**: Follow PEP 8 guidelines
- **JavaScript/TypeScript**: Use ESLint configuration
- **CSS**: Follow Tailwind conventions

## 📄 **License**

This project is part of the DeepSearch Agent system. All rights reserved.

## 🆘 **Support**

### **Getting Help**
1. Check this README and troubleshooting section
2. Review console output for error messages
3. Check API documentation at `/docs`
4. Verify all dependencies are installed
5. Ensure API keys are correctly configured

### **Reporting Issues**
When reporting issues, include:
- Operating system and version
- Python and Node.js versions
- Error messages and stack traces
- Steps to reproduce the issue
- Expected vs actual behavior

---

**Happy Researching! 🚀**

*DeepVision - Where AI meets deep research*



