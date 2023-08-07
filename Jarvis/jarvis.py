from .assistant import Assistant
from .commands import *
from .gpt import GPT

class Jarvis(Assistant):
    def __init__(self) -> None:
        super().__init__()
        self.assystent_name = 'джарвис'
        self.gpt = GPT()

    def check_command(self, cmd) -> None:
        find_true = False
        for key, value in commands.items():
            if cmd in value:
                find_true = True
                self.tts(globals()[key]())
                break
        if not find_true:
            self.tts(self.gpt.request(cmd))

    def run(self) -> None:
        for task in self.listen():
            if self.assystent_name in task or self.empty_ww:
                cmd = task if self.empty_ww else task[task.index(self.assystent_name) + 1:]

                if len(cmd) > 0:
                    print('JARVIS:', cmd)

                if len(cmd) < 1 and self.assystent_name in task:
                    self.tts('слушаю вас')
                    self.empty_ww = True
                else:
                    if 'выход' in cmd[:2]:
                        self.tts('завершаю работу')
                        exit(0)
                    else:
                        if len(cmd) > 0:
                            self.check_command(' '.join(cmd))
                            self.empty_ww = False
