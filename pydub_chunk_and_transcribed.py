#!/usr/bin/env python

from pydub import AudioSegment
from pydub.utils import make_chunks
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import io

# 1. read those wav files _xx.wav and 

audiofilename = sys.argv[1]

myaudio = AudioSegment.from_file(audiofilename, "wav")
myaudio = myaudio.set_channels(1)
chunk_length_ms = 59000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 59 sec

#Export all of the individual chunks as wav files
chunk_names = []
for i, chunk in enumerate(chunks):
    output_name = os.path.splitext(audiofilename)[0]
    chunk_name = str(output_name) + '_{0:02}.wav'.format(i)
    print ("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")
    chunk_names.append(chunk_name)
    
# 2. Do the speech to text transcription and output those texts into a single text file 

client = speech.SpeechClient()

# [START speech_python_migration_sync_request]
# [START speech_python_migration_config]
text = ""
for speech_file in chunk_names:
  
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        #sample_rate_hertz=44100,
        language_code='en-US',
        use_enhanced=True,
        model='phone_call')
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config, audio)
    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        text += (result.alternatives[0].transcript)
           
#print(text)
file = open(str(output_name) + '.txt', "w") 
file.write(text) 
file.close() 