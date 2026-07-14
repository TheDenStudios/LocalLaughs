# LocalLaughs

The private, local‑first joke engine for your machine

No cloud, no data selling – just endless free laughs generated right here on your device.

## What is LocalLaughs?

LocalLaughs is a lightweight, open‑source command‑line application that delivers jokes straight from your own computer. It stores a curated database of jokes locally and can generate new punchlines using simple pattern matching or optional AI models, all while keeping your data private.

Zero external dependencies – runs on any machine with Python 3.8+ (or Rust binary for faster execution).\nNo internet required – every joke is generated locally.

## 🚀 Features

| Feature | Description |
|---------|-------------|
| ⚡️ Fast | Pre‑compiled binary (Rust) runs in <10 ms per joke. |
| 🤖 AI‑powered (optional) | Plug in a local LLM (e.g., GPT‑Neo, Llama) to generate creative punchlines. |
| 🔒 Privacy first | No telemetry, no cloud sync, no data collection. |
| 🎨 Customizable output | Colorized terminal output, Markdown support for sharing. |

## 📥 Installation

### Python (recommended)

```bash
# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .\.venv\Scripts\activate

```

### Rust binary (for maximum speed)

```bash
git clone https://github.com/TheDenStudios/LocalLaughs.git
cd LocalLaughs
cargo build --release
./target/release/locallaughs
```

Tip: If you want the AI‑powered mode, set the environment variable `LLM_PATH` to point at your local model.

## 🎯 Usage



The output will look something like:

```text
🤖 LocalLaughs:
  Setup: Why did the scarecrow win an award?
  Punchline: Because he was outstanding in his field!
```

Place the file in the `jokes/` directory of your LocalLaughs installation or specify its path with `--file`.

Restart (or re‑run) to see your jokes integrated.

Pro tip: Use categories by adding a "category" field and run `locallaughs --category <name>`.

## 🤝 Contributing

We love contributions! Here’s how you can help:

1. Fork the repo & clone locally.
2. Make your changes (add jokes, fix bugs, improve docs).
3. Run tests:
   ```bash
   pytest tests/
   ```
4. Open a pull request with a clear description.

Code of Conduct: Please refer to `CODE_OF_CONDUCT.md` before contributing.

## 📜 License

This project is licensed under the MIT License – see the LICENSE file for details.

## 📞 Need Help?

Open an issue on GitHub if you run into bugs or have feature requests.\nDiscord/Slack: Join our community at #locallaughs (invite link in README).\nEmail: contact@example.com

Enjoy the laughs, keep them local! 😄
