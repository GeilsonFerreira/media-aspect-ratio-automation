# 🎬 Media Aspect Ratio Automation (Any Ratio → 16:9)

Este projeto é uma **automação em Python** que transforma **imagens e vídeos de qualquer proporção** (9:16, 1:1, 4:3, 21:9, etc.) no formato **16:9**, aplicando **preenchimento de fundo e centralização automática**, conforme padrões de **exibição televisiva e broadcast**.

A solução foi desenvolvida com foco em **ambientes reais de produção audiovisual**, como emissoras de TV, produtoras de conteúdo e fluxos profissionais de mídia digital.

---

## 🎯 Objetivo do projeto

Padronizar automaticamente mídias de diferentes formatos para **16:9**, eliminando retrabalho manual e garantindo compatibilidade com:

* Televisão aberta e fechada
* Portais de vídeo
* Exibição institucional e corporativa

---

## 🚀 Funcionalidades

* ✅ Conversão de **imagens e vídeos de qualquer proporção** para 16:9
* ✅ Detecção automática do formato de entrada
* ✅ Preenchimento inteligente de fundo (letterbox / pillarbox)
* ✅ Centralização automática do conteúdo original
* ✅ Processamento em lote (batch processing)
* ✅ Estrutura preparada para automação contínua (watch folders)
* ✅ Saída compatível com padrões de broadcast

---

## 🧠 Decisões técnicas

* O projeto prioriza **automação e previsibilidade**, evitando ajustes manuais
* A lógica de enquadramento é **flexível**, baseada no tamanho real da mídia de entrada
* O pipeline foi pensado para **escala**, podendo ser integrado a:

  * Rotinas de ingest
  * Fluxos de pós-produção
  * Sistemas de monitoramento de pastas

---

## 🛠️ Tecnologias utilizadas

* **Python**
* Processamento de imagens
* Processamento de vídeo
* Manipulação de arquivos e diretórios
* Arquitetura modular (separação de responsabilidades)

---

## 📂 Estrutura do projeto (visão geral)

```text
src/
├── main.py              # Ponto de entrada da aplicação
├── monitor.py           # Monitoramento de pastas
├── image_processor.py   # Conversão de imagens para 16:9
├── video_processor.py   # Conversão de vídeos para 16:9
├── config.py            # Configurações e caminhos
└── utils.py             # Funções auxiliares
```

---

## 📌 Casos de uso reais

* 📺 Telejornais e programas de TV
* 📱 Adaptação de vídeos verticais e quadrados para TV
* 🗂️ Padronização de acervo audiovisual
* 🎥 Conteúdos produzidos para redes sociais reaproveitados em broadcast

---

## 📈 Diferencial para recrutadores

Este projeto demonstra:

* ✔️ Pensamento de **engenharia aplicada a problemas reais**
* ✔️ Automação de processos manuais
* ✔️ Organização de código e modularização
* ✔️ Conhecimento de **mídia, vídeo e padrões de exibição**
* ✔️ Capacidade de unir **tecnologia e produção audiovisual**

---

## 🚧 Status do projeto

🟡 Em desenvolvimento contínuo

---

# Media Aspect Ratio Automation (Any Ratio → 16:9)

This project is a **Python-based automation** that converts **images and videos of any aspect ratio** (9:16, 1:1, 4:3, 21:9, etc.) into **16:9 format**, applying **automatic background filling and content centering**, following **TV and broadcast standards**.

It was designed for **real-world audiovisual production workflows**, especially in television and professional media environments.

---

## 🎯 Project goal

Automatically standardize media assets into **16:9**, reducing manual work and ensuring compatibility with:

* Broadcast TV
* Video platforms
* Corporate and institutional displays

---

## 🚀 Features

* Convert images and videos from **any aspect ratio** to 16:9
* Automatic input format detection
* Intelligent background filling
* Automatic content centering
* Batch processing support
* Folder monitoring–ready architecture
* Broadcast-compatible output

---

## 🛠️ Tech stack

* Python
* Image processing
* Video processing
* File system automation
* Modular architecture

---

## 🚧 Project status

Under continuous development.

---