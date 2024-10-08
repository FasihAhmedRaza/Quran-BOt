import streamlit as st
from pydub import AudioSegment
import os
import speech_recognition as sr
import arabic_reshaper
from bidi.algorithm import get_display

def transcribe_audio(file_path):
    """Transcribes the given audio file and returns the transcribed text."""
    try:
        # Convert any audio format to wav
        sound = AudioSegment.from_file(file_path)  # Automatically handles various formats
        wav_file_path = file_path.rsplit('.', 1)[0] + '.wav'  # Change extension to .wav
        sound.export(wav_file_path, format='wav')
        
        # Initialize recognizer
        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio_data, language='ar-SA')
        
        os.remove(wav_file_path)  # Clean up the wav file after processing
        return transcribed_text
    except sr.UnknownValueError:
        return "خطأ: لم يتمكن النظام من التعرف على الكلام."
    except sr.RequestError as e:
        return f"خطأ في الاتصال بالخدمة: {e}"
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

def main():
    # Streamlit app title
    st.title("Quran Speech to Text")

    # Add custom CSS for Arabic font
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');

            .arabic-text {
                font-family: 'Amiri', serif;  /* Use a nice Arabic font */
                font-size: 28px;              /* Increased font size for better readability */
                direction: rtl;               /* Right to left direction */
                text-align: right;            /* Align text to right */
                line-height: 1.6;             /* Increase line height for better spacing */
            }
        </style>
        """, unsafe_allow_html=True)

    # File uploader for audio files
    uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "flac", "ogg", "aac", "wma"])
    
    # Initialize a variable to store the audio file path
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp_audio_file", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Create a button to proceed with transcription
        if st.button("Proceed Audio"):
            # Transcribe the audio file
            transcribed_text = transcribe_audio("temp_audio_file")
            
            # Reshape and display the text
            reshaped_text = arabic_reshaper.reshape(transcribed_text)
            bidi_text = get_display(reshaped_text)

            # Check if the transcription indicates an error
            if "خطأ" in transcribed_text:
                # Display error text in red
                st.markdown(f"<p class='arabic-text' style='color:red;'>{bidi_text}</p>", unsafe_allow_html=True)
            else:
                # Display correct transcription in green
                st.markdown(f"<p class='arabic-text' style='color:green;'>{bidi_text}</p>", unsafe_allow_html=True)

if _name_ == "_main_":
    main()