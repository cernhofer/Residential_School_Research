import argparse
import io
import time
import re
import pandas 


def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech
    speech_client = speech.Client()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate_hertz=16000)

    operation = audio_sample.long_running_recognize('en-US')

    retry_count = 100
    while retry_count > 0 and not operation.complete:
        retry_count -= 1
        time.sleep(2)
        operation.poll()

    if not operation.complete:
        print('Operation not complete and retry limit reached.')
        return

    alternatives = operation.results
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))


def transcribe_gcs(gcs_uri, write_file):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    speech_client = speech.Client()

    audio_sample = speech_client.sample(
        content=None,
        source_uri=gcs_uri,
        encoding='LINEAR16',
        sample_rate=44100)

    operation = audio_sample.async_recognize('en-US')

    retry_count = 100
    while retry_count > 0 and not operation.complete:
        retry_count -= 1
        time.sleep(2)
        operation.poll()

    if not operation.complete:
        print('Operation not complete and retry limit reached.')
        return

    alternatives = operation.results
    results = ''
    t_sum = 0
    t_num = 0
    for alternative in alternatives:
        results += alternative.transcript

        t_num += 1
        t_sum += alternative.confidence

    
    av_confidence = t_sum/t_num
    if av_confidence < .75:
        write_file.write("CHECK TRANSCRIPT\n\n")
    write_file.write(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    #print(args.path)
    test = 'Transcripts/'
    file_name = test + args.path.split('/')[-1][:-4] + '.txt'
    write_file = open(file_name, 'w')
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path, write_file)
    else:
        transcribe_file(args.path)






