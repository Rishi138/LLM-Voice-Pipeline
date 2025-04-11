# LLM-Voice-Pipeline
A multi-model pipeline integrating LLM and voice processing that creates a fully voice-controlled LLM. The program utilizes state-of-the-art LLMs, TTS models, STT models, and VAD, resulting in a responsive voice assistant capable of fluid conversation with users. 

## Table of Contents
1. [Features](#features)
2. [OpenAI Setup](#openai-setup)
3. [Installation](#installation)

## Features
  - **OpenAI Model Integration**: Converse and talk with powerful LLMs from OpenAI such as gpt-4o and gpt4o-mini.
  - **Voice Activity Detection**: Employs VAD to ensure dynamic and low-latency interactions.
  - **Real-time speech streaming**: Streams audio to TTS and STT models offered by OpenAI for instant conversation.
  - **Context-aware modeling**: Provides memory to LLM to remember context and past messages.

## OpenAI Setup
1. **Setup Your API Key**
   - Follow [setup](https://platform.openai.com/docs/libraries) in the OpenAI Quickstart guide to configure your API key.

3. **Add Enviromental Variable**
   - Based on the environment being used, follow according setup for environmental variables to add your OpenAI API key
    
## Installation
1. **Clone Repository**
```sh
git clone https://github.com/Rishi138/LLM-Voice-Pipeline.git
cd gmail-agent
```

2. **Install Dependencies**
```sh
pip3 install -r requirements.txt
```

3. **Run Voice Assistant**
```sh
python3 LLM_with_voice_control.py
```
