class Step:
    
    def __init__(self, **kwargs):
        self.clickid = kwargs.get('clickid', 0)
        self.cursor_position = kwargs.get('cursor_position', (0, 0, 0))
    
    def set_click(self, clickid: int) -> None:
        self.clickid = clickid
        return
    
    def set_cursor_position(self, cursor_position: tuple) -> None:
        self.cursor_position = cursor_position
        return