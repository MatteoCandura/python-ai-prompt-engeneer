# AI Prompt Consultant 🤖✨

**AI Prompt Consultant** is a powerful CLI (Command Line Interface) tool written in Python that acts as a **Senior Prompt Engineer**. It leverages Google Gemini's AI to help you refine, structure, and optimize your prompts through an interactive interview process.

## 🚀 Key Features

- **Assisted Prompt Engineering**: An expert AI asks targeted questions to improve your initial idea.
- **Multilingual**: Full support for **English** and **Italian** (defaults to system preference or prompts on first run). The interface and AI adapt to the chosen language.
- **Zero-Config Setup**: No complex `.env` files. On first run, the tool guides you through configuring your API Key and preferences.
- **Persistence**: Automatically saves your API Key, preferred model, and language in `config.json`.
- **Next-Gen Model Support**: Compatible with the latest Google models (`gemini-2.5-flash`, `gemini-2.5-pro`, and others).
- **Slash Commands**: Quick commands to change settings on the fly during the conversation.

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher.
- A Google AI Studio API Key (get it [here](https://aistudio.google.com/)).

### Setup

1.  Clone the repository (or download the files).
2.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

## 💻 Usage

Run the program from your terminal:

```bash
python3 main.py
```

### First Run

If it's your first time running it, the tool will ask for:

1.  Your preferred language (IT/EN).
2.  Your Google Gemini API Key.
3.  The model to use (e.g., `gemini-2.5-flash`).

This information will be saved for future use.

### Workflow

1.  **Initial Idea**: Briefly describe what you want to achieve (e.g., "I want a prompt to write an SEO article").
2.  **Interview**: The AI will ask you 1-3 questions at a time to clarify context, target audience, tone, and constraints.
3.  **Generation**: Once enough details are gathered, the AI will generate an **Optimized Prompt** ready for you to copy and paste.

## ⚡ Available Commands (Slash Commands)

During the conversation, you can use the following special commands:

| Command         | Description                                                               |
| :-------------- | :------------------------------------------------------------------------ |
| `/set-model`    | Change the AI model used (e.g., from Flash to Pro).                       |
| `/set-apikey`   | Update your saved API Key.                                                |
| `/set-language` | Change the interface and AI language (IT 🇮🇹 / EN 🇬🇧).                     |
| `/reset`        | Clear **all** saved settings and exit the program. Useful to start fresh. |
| `/exit`         | End the session and close the program.                                    |

## ⚙️ Advanced Configuration

All preferences are saved in the local `config.json` file.
You don't need to edit it manually, but here is how it looks:

```json
{
	"model": "gemini-2.5-flash",
	"api_key": "AIzaSy...",
	"language": "en"
}
```

To launch the program ignoring saved preferences (without deleting them):

```bash
python3 main.py --reset
```

_(Note: The `--reset` flag only affects the current session. To permanently delete settings, use the `/reset` command inside the app)._

## 🐞 Troubleshooting

- **404 Error (Model not found)**: Ensure you are using a valid model name (e.g., `gemini-1.5-flash`, `gemini-2.5-flash`). Use `/set-model` to change it.
- **Unknown Command**: Make sure to type the command correctly (e.g., `/exit` and not `exit` or `/quit`).
- **API Key Issues**: If your key has expired, use `/set-apikey` to enter a new one.

---

_Created with ❤️ and 🤖_
