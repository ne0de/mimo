import sys, pickle

from os import walk
from time import sleep
from cornelius import Cursor, Keyboard

from .sequence import Sequence
from .step import Step

class Mimo:
    def __init__(self):
        self.__sequences = []  
        self.cursor = Cursor()
        self.keyboard = Keyboard()
        self.velocity = 0.1
        self.running = False
        self.recording = False
        self.current_sequence = None
    
    def log(self, text: str, **kwargs) -> None:
        type = kwargs.get('type', 'LOG')
        print(f'({type}) {text}')
        return

    def add_sequence(self, sequence: Sequence) -> None:
        self.__sequences.append(sequence)
        return

    def record(self) -> None:
        position = self.cursor.get()
        clickid = 0
        if cursor.is_pressed(1):
          clickid = 1
        elif cursor.is_pressed(2):
          clickid = 2
        step = Step(cursor_position=position, clickid=clickid)
        self.current_sequence.add_step(step)
        sleep(self.velocity)
        return

    def execute_sequence(self, sequence: Sequence) -> None:
        self.log(f'Executing sequence {sequence.name} ...')
        for step in sequence.steps:
            x, y, _ = step.cursor_position # 3 argument unused.
            self.cursor.set(x, y)
            sleep(sequence.velocity)
            if step.clickid != 0:
                self.cursor.press(button=step.clickid)
                self.cursor.release(button=step.clickid)
            sleep(sequence.velocity)
            
        self.log(f'Sequence {sequence.name} executed.')
        return
    
    def load_sequences(self):
        for (dirpath, dirnames, filenames) in walk('.'):
            for filename in filenames:
                if filename.endswith('.mimo'):
                    try:
                        with open(f'{filename}', 'rb') as sequence_file:
                            sequence = pickle.load(sequence_file)
                            self.add_sequence(sequence)
                    except Exception as e:
                        self.log(f'Error loading sequence {filename}.')
                        self.log(f'{e}', type='ERROR')
        return

    def check_events(self) -> None:
        if self.keyboard.is_pressed('1') and not self.recording:
            self.log('Recording started.')
            self.current_sequence = Sequence()
            self.recording = True
        
        elif self.keyboard.is_pressed('2') and self.recording:
            self.log('Recording stopped.')
            self.save_sequence()
            self.recording = False

        elif self.keyboard.is_pressed('3') and not self.recording:
            self.log('Your sequences:')
            self.show_sequences()
            sleep(1)
        
        elif self.keyboard.is_pressed('4') and not self.recording:
            if not self.show_sequences():
                sleep(1)
                return
            sequence = None
            self.log('-1 to exit.', type='INFO')
            while True:
                sequence_id = int(input('Select a sequence to execute:'))
                if sequence_id == -1:
                    return
                if sequence_id < 0 or sequence_id >= len(self.__sequences):
                    self.log('Invalid sequence id.')
                    continue
                sequence = self.__sequences[sequence_id]
                break
            self.execute_sequence(sequence)
            sleep(1)
        
        elif self.keyboard.is_pressed('f5'):
            self.log('Stopping mimo.')
            self.stop()

        if self.recording:
            self.record()
    
    
    def save_sequence(self) -> None: 
        name = str(input('Enter the name of the sequence: '))
        if not name or name.isspace():
            self.log('No name given.')
        elif self.sequence_exists(name):
            self.log(f'Sequence {name} already exists.')
        else:
            self.current_sequence.set_name(name)
        self.current_sequence.velocity = self.velocity
        self.add_sequence(self.current_sequence)
        try:
            with open(f'{self.current_sequence.name}.mimo', 'wb') as sequence_file:
                pickle.dump(self.current_sequence, sequence_file)
        except Exception as e:
            self.log('Error saving sequence.')
            self.log(f'{e}', type='ERROR')
        self.current_sequence = None
        self.log('Sequence saved.')
        return
    
    def sequence_exists(self, name: str) -> bool:
        for sequence in self.__sequences:
            if sequence.name == name:
                return True
        return False

    def show_sequences(self) -> bool:
        if len(self.__sequences) == 0:
            self.log('No sequences found.')
            return False
        cont = 0
        for sequence in self.__sequences:
            self.log(sequence.name, type=f'{cont} - ')
            cont += 1
        return True

    def stop(self) -> None:
        self.running = False
        return
    
    def run(self) -> None:
        """
            Run mimo.
        """
        self.running = True
        self.load_sequences()
        self.log('Mimo beta started.')
        self.log('Press 1 to start a new sequence.', type='INFO')
        self.log('Press 2 to stop a new sequence.', type='INFO')
        self.log('Press 3 to show all sequences.', type='INFO')
        self.log('Press 4 to execute a sequence.', type='INFO')
        self.log('Press F5 to stop mimo.', type='INFO')
        while self.running:
            self.check_events()
        return
    
    
