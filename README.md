# 🕵️‍♂️ Stegnography Web App

A powerful and simple-to-use web application to hide or extract **secret data** (text or files) inside **images, audio, or video** files using **AES encryption** and **modern steganography techniques**.

Built with ❤️ for students, cybersecurity learners, and privacy enthusiasts.

---

## 🌟 Features

- 🔐 Encrypt payload using:
  - Password-based encryption (PBKDF2 + AES)
  - Randomly generated encryption key (AES)
- 🖼️ Hide data inside:
  - Images (`.png`, `.jpg`, `.jpeg`)
  - Audio files (`.wav`, `.mp3`)
  - Video files (`.mp4`, `.avi`)
- 🔍 Extract and decrypt hidden data with ease
- 🧠 Automatically detects and decrypts using password or key
- 📦 Outputs a clean ZIP package with the stego file and encryption key (if random key used)
- 🎨 Clean UI built with Flask and HTML/CSS

---

## ⚙️ Installation

> Tested on **Kali Linux**, **Python 3.10+**, and **virtual environments**.

### 1. Clone the Repository

```bash
git clone https://github.com/Kar213/Stegnography-webapp.git
cd Stegnography-webapp
