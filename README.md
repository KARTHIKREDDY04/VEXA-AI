# ✳ Vexa AI — Your Intelligent AI Assistant

**Vexa AI** is a modern, Gemini-powered AI chatbot built with Python and Streamlit. It features a clean, ChatGPT-inspired interface, conversational interactions, multiple Gemini model options, and a simple user experience.

Ask questions, explore ideas, learn technical concepts, and generate content through one intuitive AI workspace.

## ✨ Features

- 🤖 **Gemini AI Integration** — Generate responses using Google's Gemini API.
- 🎨 **Modern UI** — Clean, responsive interface inspired by modern AI chat applications.
- 💬 **Conversational Chat** — Send messages and receive contextual responses.
- 🗂️ **Chat History** — Switch between conversations during your session.
- 🧠 **Model Selection** — Choose from configured Gemini model options.
- 💡 **Suggested Prompts** — Get started quickly with predefined prompts.
- 🔐 **Secure API Configuration** — Keep API credentials outside your source code.
- ☁️ **Cloud Deployment** — Deploy the application using Streamlit Community Cloud.
- 🐍 **Python-Based** — Built using Python and Streamlit.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application and user interface |
| Google Gen AI SDK | Gemini API integration |
| Google Gemini API | AI-generated responses |
| Git & GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

## 📁 Project Structure

```text
vexa-ai-chatbot/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/vexa-ai-chatbot.git
cd vexa-ai-chatbot
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey).

For local development, create a file at `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your actual API key.

**Security:** Never commit `secrets.toml`, your API key, or other credentials to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

## ☁️ Deployment

Deploy Vexa AI using Streamlit Community Cloud:

1. Push the project files to a GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create a new app and select your repository.
4. Set the main file path to `app.py`.
5. Add your Gemini API key under the app's **Secrets** settings:

   ```toml
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
   ```

6. Deploy the application and open the generated public URL.

## 🔑 API Configuration

Vexa AI requires a valid Gemini API key and a model ID supported by your Google API account.

The configured model list can be customized in `app.py`. If a selected model is unavailable, choose another supported model.

API availability, quotas, and usage limits depend on Google's current API policies and your account.

## 🔮 Future Enhancements

- [ ] Persistent chat history using a database
- [ ] User authentication and individual profiles
- [ ] Markdown and code syntax enhancements
- [ ] File uploads and document question answering
- [ ] Voice input and text-to-speech
- [ ] Streaming AI responses
- [ ] More AI model integrations
- [ ] Customizable themes and preferences

## 🔒 Security

- Store API keys in environment variables or platform secrets.
- Do not expose credentials in source code or screenshots.
- Apply usage limits and appropriate access controls before offering the app publicly.
- Review the API provider's terms and privacy policies before processing sensitive information.

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork this repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request describing your contribution.

## 📄 License

This project is currently provided without an explicit license. Add a `LICENSE` file if you intend to grant others permission to use, modify, and distribute the code.

## 👨‍💻 Author

**YOUR NAME**

- GitHub: https://github.com/KARTHIKREDDY04

---

*Vexa AI — Think smarter. Create faster.* ✳
