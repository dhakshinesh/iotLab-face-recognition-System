from google.cloud import texttospeech

def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Set the audio file format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # Save the audio to a file
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file 'output.mp3'")

text_to_speech("Hello! How can I assist you today?")
