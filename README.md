
# Media Aspect Ratio Automation

Automated Python tool to convert vertical or non-standard videos (e.g. 9:16) into 16:9 horizontal format, applying a custom background image and automatic centralization — ideal for TV, YouTube, and professional video workflows.

---

## 🎯 Purpose

This project was created to solve a common media problem:

> How to automatically adapt vertical videos to a 16:9 format without cropping, keeping the original video centered and visually consistent.

The tool:

* Preserves the original aspect ratio
* Applies a 16:9 background image
* Automatically centers the video
* Processes files continuously from a monitored folder

---

## 🧠 How It Works (High-Level)

* Monitors an input folder for new video files
* Reads video metadata (resolution, rotation, duration)
* Creates a 16:9 background canvas
* Resizes the video proportionally
* Centers the video on the background
* Exports the final video in MP4 (H.264)

---

## 📁 Project Structure

```text
media-aspect-ratio-automation/
│
├── entrada/                # Input videos (watch folder)
├── saida/                  # Processed videos (output)
├── assets/
│   └── background.jpg      # Background image (16:9)
│
├── src/
│   ├── monitor.py          # Folder monitoring logic
│   ├── video_processor.py  # Video processing logic
│   ├── logger.py           # Logging configuration
│   └── main.py             # Application entry point
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠️ Technologies Used

* Python 3.10+
* MoviePy 2.x
* FFmpeg
* Pathlib
* Logging (standard library)

---

## ⚠️ Important: MoviePy 2.x Compatibility

This project is fully compatible with MoviePy 2.x, which introduced breaking API changes.

### Key differences from MoviePy 1.x:

| Old (❌)        | New (✅)         |
| -------------- | --------------- |
| moviepy.editor | moviepy         |
| set_position() | with_position() |
| Mutable clips  | Immutable clips |

### Example:

```python
# ❌ Old
clip.set_position((x, y))

# ✅ New
clip = clip.with_position((x, y))
```

All imports and methods in this project follow the new MoviePy API.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/media-aspect-ratio-automation.git
cd media-aspect-ratio-automation
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

FFmpeg must be available in your system PATH.

**Windows:**
[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

**Linux:**

```bash
sudo apt install ffmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

---

## ▶️ How to Use

Place your 16:9 background image inside:

```text
assets/background.jpg
```

Start the application:

```bash
python src/main.py
```

Drop any video into the `entrada/` folder

The processed video will appear in `saida/`

---

## 📐 Default Output Settings

* Resolution: 1280×720 (16:9)
* Codec: H.264 (libx264)
* Audio: AAC
* FPS: 30
* Pixel Format: yuv420p

These values can be adjusted in `video_processor.py`.

---

## 🧩 Supported Inputs

* Vertical videos (9:16)
* Horizontal videos (any resolution)
* Videos with rotation metadata (auto-corrected)

---

## 🚀 Possible Improvements

* Blur or color-average background
* Batch processing statistics
* Support for multiple output formats (Full HD, 4K)
* CLI arguments
* Docker version
* GPU encoding (NVENC)

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👤 Author

**Geilson Ferreira**
Computer Science student and automation enthusiast
Focused on Python, media automation, and data-driven workflows

---

# Media Aspect Ratio Automation

Ferramenta em Python para automatizar a conversão de **vídeos verticais ou fora do padrão** (ex.: 9:16) para o formato **horizontal 16:9**, aplicando uma imagem de fundo e centralização automática — ideal para TV, YouTube e fluxos profissionais de mídia.

---

## 🎯 Objetivo do Projeto

Este projeto resolve um problema comum em produção de conteúdo audiovisual:

> Como adaptar vídeos verticais para 16:9 **sem cortar o conteúdo**, mantendo qualidade e padronização visual.

A automação:

* Preserva a proporção original do vídeo
* Aplica um fundo em 16:9
* Centraliza automaticamente o conteúdo
* Processa arquivos de forma contínua a partir de uma pasta monitorada

---

## 🧠 Como Funciona (Visão Geral)

1. Monitora uma pasta de entrada em busca de novos vídeos
2. Lê metadados do vídeo (resolução, rotação, duração)
3. Cria uma base 16:9 a partir de uma imagem de fundo
4. Redimensiona o vídeo mantendo a proporção
5. Centraliza o vídeo no fundo
6. Exporta o resultado final em MP4

---

## 📁 Estrutura do Projeto

```text
media-aspect-ratio-automation/
│
├── entrada/                # Vídeos de entrada (pasta monitorada)
├── saida/                  # Vídeos processados
├── assets/
│   └── background.jpg      # Imagem de fundo (16:9)
│
├── src/
│   ├── monitor.py          # Monitoramento da pasta
│   ├── video_processor.py  # Lógica de processamento de vídeo
│   ├── image_processor.py  # (Opcional) processamento de imagens
│   ├── logger.py           # Configuração de logs
│   └── main.py             # Ponto de entrada da aplicação
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **MoviePy 2.x**
* **FFmpeg**
* **Pathlib**
* **Logging (biblioteca padrão do Python)**

---

## ⚠️ Atenção: Compatibilidade com MoviePy 2.x

Este projeto foi desenvolvido **exclusivamente para MoviePy 2.x**, que introduziu mudanças importantes na API.

### Principais diferenças em relação à versão 1.x:

| MoviePy 1.x (❌)  | MoviePy 2.x (✅)   |
| ---------------- | ----------------- |
| `moviepy.editor` | `moviepy`         |
| `set_position()` | `with_position()` |
| Objetos mutáveis | Objetos imutáveis |

### Exemplo:

```python
# ❌ Antigo
clip.set_position((x, y))

# ✅ Atual
clip = clip.with_position((x, y))
```

Todas as importações e métodos deste projeto seguem o **novo padrão oficial do MoviePy**.

---

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/media-aspect-ratio-automation.git
cd media-aspect-ratio-automation
```

### 2. Criar e ativar um ambiente virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar o FFmpeg

O FFmpeg precisa estar disponível no PATH do sistema.

* **Windows**: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
* **Linux**:

```bash
sudo apt install ffmpeg
```

* **macOS**:

```bash
brew install ffmpeg
```

---

## ▶️ Como Usar

1. Adicione sua **imagem de fundo 16:9** em:

```text
assets/background.jpg
```

2. Inicie a aplicação:

```bash
python src/main.py
```

3. Copie qualquer vídeo para a pasta `entrada/`

4. O vídeo final será gerado automaticamente em `saida/`

---

## 📐 Configurações Padrão de Saída

* Resolução: **1280×720 (16:9)**
* Codec: **H.264 (libx264)**
* Áudio: **AAC**
* FPS: **30**
* Formato de pixel: **yuv420p**

Esses parâmetros podem ser ajustados no arquivo `video_processor.py`.

---

## 🧩 Tipos de Vídeo Suportados

* Vídeos verticais (9:16)
* Vídeos horizontais (qualquer resolução)
* Vídeos com metadados de rotação (correção automática)

---

## 🚀 Possíveis Evoluções

* Fundo desfocado (blur)
* Estatísticas de processamento
* Múltiplas resoluções de saída (Full HD, 4K)
* Interface via linha de comando (CLI)
* Container Docker
* Aceleração por GPU (NVENC)

---

## 📄 Licença

Este projeto é open-source e está disponível sob a licença **MIT**.

---

## 👤 Autor

**Geilson Ferreira**
Estudante de Ciência da Computação
Foco em Python, automações de mídia e soluções escaláveis

---
