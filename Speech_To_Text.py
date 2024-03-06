from huggingsound import SpeechRecognitionModel
import librosa



def read_mp3(filename: str):
    y, sr = librosa.load(filename)
    return y, sr


def audio_to_text_HUN(filename: str) -> str:

    # https://github.com/jonatasgrosman/huggingsound/blob/main/huggingsound/speech_recognition/model.py
    base_model_path = "jonatasgrosman/wav2vec2-large-xlsr-53-hungarian"

    # after base model finetuned
    finetuned_model_path = ""

    # device = cpu (cpu), cuda (gpu)
    huggingsound_model_1 = SpeechRecognitionModel(model_path = base_model_path, letter_case ='lowercase', device='cpu')
    translation = huggingsound_model_1.transcribe([filename])
    return translation[0]['transcription']

    #model_name_1 = "jonatasgrosman/wav2vec2-large-xlsr-53-hungarian"
    #huggingsound_model_1 = SpeechRecognitionModel(model_name_1)
    #df['huggingsound_1'] = huggingsound_model_1.transcribe(list(df['filename']))
