import torch
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from queue import Queue
import json, os
from num2words import num2words

class Assistant(object):
    def __init__(self) -> None:
        self.queue = Queue()
        self.vosk_path = 'models/vosk'
        self.silero_path = 'models/silero.pt'

        if not os.path.isfile(self.silero_path):
            print('AssystentError: ' + self.silero_path + ' not found!')
            exit(1)
        if not os.path.isdir(self.vosk_path):
            print('AssystentError: ' + self.vosk_path + ' not found!')
            exit(1)

        self.silero_model = torch.package.PackageImporter(self.silero_path).load_pickle('tts_models', 'model')
        self.silero_model.to(torch.device('cpu'))
        self.vosk_model = Model(self.vosk_path)
        self.sample_rate_tts = 48000
        self.sample_rate_stt = 16000
        self.process = None
        self.empty_ww = False
        self.assystent_name = ''
        self.gpt = None

    def callback(self, indata, frames, time, status) -> None:
        if not status:
            self.queue.put(bytes(indata))

    def listen(self) -> str:
        with sd.RawInputStream(samplerate=self.sample_rate_stt, blocksize=8000, device=None, dtype="int16", channels=1, callback=self.callback) as procces:
            rec = KaldiRecognizer(self.vosk_model, self.sample_rate_stt)
            self.process = procces
            self.tts('начинаю работу')
            while True:
                data = self.queue.get()
                if rec.AcceptWaveform(data):
                    yield str(json.loads(rec.Result())['text']).split()

    def format_string(self, text: str):
        res = text.lower().split()

        for word in res:
            if word.isnumeric():
                res[res.index(word)] = num2words(int(word), lang='ru')

        result = ' '.join(res)

        if not result.endswith('.'):
            result += '.'

        return result

    def tts(self, text: str) -> None:
        self.process.stop()
        audio = self.silero_model.apply_tts(text=self.format_string(text),
                            speaker='baya',
                            sample_rate=self.sample_rate_tts)
        sd.play(audio, self.sample_rate_tts, blocking=True)
        sd.stop()
        self.process.start()
