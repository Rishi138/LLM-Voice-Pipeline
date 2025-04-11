import openai
import webrtcvad
import pyaudio
import wave
from playsound import playsound
import os

model = openai.OpenAI()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Frequency in Khz
CHUNK = 320  # 320 frames per chunk so 320 frames per 16000 khz which is 20 ms of audio per chunk

vad = webrtcvad.Vad(1)  # aggressiveness of VAD

model_description = "You are a voice agent for Rishi Mohanty. You make calls on his behalf. This means your responses" \
                    " should be concise, deliberate, natural, and without needing any extra formatting or characters." \
                    " Rishi wants you to schedule a reservation anytime between 6:00 AM and 9:00 AM with the ideal " \
                    "time being 8:00 AM, with outdoor seating, and for four people. He would also like to know if " \
                    "they serve alfredo pasta. Make sure you specify that you are an AI Agent. You need to take " \
                    "charge of the conversation so be direct and to the point "

messages = [{
    "role": "developer",
    "content": "You are a voice assistant, this means your responses should be concise, deliberate, natural, "
               "and without needing any extra formatting or characters. "
}]


def add_message(role, content):
    messages.append({
        "role": role,
        "content": content
    })


def get_audio():
    audio = []
    silence_counter = 0

    stream = pyaudio.PyAudio().open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    while True:
        frame = stream.read(CHUNK)
        is_speech = vad.is_speech(frame, RATE)
        if is_speech:
            audio.append(frame)
            silence_counter = 0
        else:
            silence_counter += CHUNK / RATE
            if silence_counter >= 1.2:
                break
    stream.stop_stream()
    stream.close()
    print("Done recording.")

    wav_file = "audio.wav"
    with wave.open(wav_file, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(b"".join(audio))


def ask(prompt):
    add_message("user", prompt)
    response = model.responses.create(
        model="gpt-4o-mini-2024-07-18",
        input=messages
    )
    add_message("assistant", response.output_text)
    return response.output_text


def speak(text):
    speech_file_path = "C:/Users/rajal/PycharmProjects/VoiceAgent/Basic Implementations/speech.mp3"
    if os.path.exists(speech_file_path):
        os.remove(speech_file_path)
    with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=text
    ) as response:
        response.stream_to_file(speech_file_path)

    playsound(speech_file_path)


def wav_file_to_text():
    text = []
    audio_file = open("audio.wav", "rb")
    try:
        stream = model.audio.transcriptions.create(
            file=audio_file,
            model="gpt-4o-mini-transcribe",
            stream=True
        )
    except openai.BadRequestError:
        return "Sorry, could you repeat that quicker", True

    for event in stream:
        try:
            text.append(event.delta)
        except AttributeError:
            pass

    return ''.join(text), False


print("Event Log:")
while True:
    print("Listening...")
    get_audio()
    print("STT...")
    transcription, listen_again = wav_file_to_text()
    if not listen_again:
        print("Replying...")
        reply = ask(
            transcription+". If our conversation is over then reply without punctuation just the text: "
                          "goodbye see you later"
                    )
        if reply == "goodbye see you later":
            speak("Goodbye, see you later!")
            break
        print("TTS...")
        speak(reply)
    else:
        print("Replying...")
        print("TTS...")
        speak(transcription)
