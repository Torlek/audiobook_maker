# tts_engines.py

import os

from tortoise_tts_api.inference.load import load_tts as load_tortoise_engine
from tortoise_tts_api.inference.generate import generate

def generate_audio(tts_engine, sentence, voice_parameters, tts_engine_name, audio_path):
    match tts_engine_name:
        case 'pyttsx3':
            return generate_with_pyttsx3(tts_engine, sentence, voice_parameters, audio_path)
        case 'styletts2':
            return generate_with_styletts2(tts_engine, sentence, voice_parameters, audio_path)
        case 'tortoise':
            return generate_with_tortoise(tts_engine, sentence, voice_parameters, audio_path)
        case 'xtts':
            return generate_with_xtts(tts_engine, sentence, voice_parameters, audio_path)
        case _:
            # Handle unknown engine
            return False

def generate_with_pyttsx3(sentence, voice_parameters, audio_path):
    import pyttsx3
    engine = pyttsx3.init()
    # Optionally set voice parameters here using voice_parameters
    # e.g., engine.setProperty('rate', voice_parameters.get('rate', 200))
    # Save the spoken sentence to an audio file
    engine.save_to_file(sentence, audio_path)
    engine.runAndWait()
    return os.path.exists(audio_path)

def generate_with_styletts2(sentence, voice_parameters, audio_path):
    # noop
    pass

def generate_with_tortoise(tts_engine, sentence, voice_parameters, audio_path):
    if tts_engine is None:
        return False
    voice = voice_parameters.get('voice', 'random')
    sample_size = voice_parameters.get('sample_size', 4)
    use_hifigan = voice_parameters.get('use_hifigan', False)
    num_autoregressive_samples = sample_size

    result = generate(
        tts=tts_engine,
        text=sentence,
        voice=voice,
        use_hifigan=use_hifigan,
        num_autoregressive_samples=num_autoregressive_samples,
        audio_path=audio_path
    )
    return os.path.exists(audio_path)

def generate_with_xtts(sentence, voice_parameters, audio_path):
    # noop
    pass

# Add more TTS engine implementations as needed

##### Loading stuff below                           

def load_tts_engine(tts_engine_name, **kwargs):
    try:
        match tts_engine_name:
            case 'pyttsx3':
                return None  # pyttsx3 doesn't require loading
            case 'styletts2':
                return load_with_styletts2(**kwargs)
            case 'tortoise':
                return load_with_tortoise(**kwargs)
            case 'xtts':
                return load_with_xtts(**kwargs)
            case _:
                # Handle unknown engine
                raise ValueError(f"Unknown TTS engine: {tts_engine_name}")
    except Exception as e:
        # Re-raise the exception to be caught by the worker thread
        raise e
        
def load_with_styletts2():
    #noop
    pass
    
def load_with_tortoise(**kwargs):
    # Parameters needed to load the tortoise engine
    autoregressive_model_path = kwargs.get("autoregressive_model_path", None)
    diffusion_model_path = kwargs.get("diffusion_model_path", None)
    vocoder_name = kwargs.get("vocoder_name", None)
    tokenizer_json_path = kwargs.get("tokenizer_json_path", None)
    use_deepspeed = kwargs.get("use_deepspeed", False)
    use_hifigan = kwargs.get("use_hifigan", False)

    tts = load_tortoise_engine(
        autoregressive_model_path=autoregressive_model_path,
        diffusion_model_path=diffusion_model_path,
        vocoder_name=vocoder_name,
        tokenizer_json_path=tokenizer_json_path,
        use_deepspeed=use_deepspeed,
        use_hifigan=use_hifigan
    )
    return tts

def load_with_xtts():
    #noop
    pass