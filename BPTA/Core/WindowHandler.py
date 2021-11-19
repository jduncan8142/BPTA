import win32con
import win32gui

from typing import Any, Optional


class WindowHandler:
    def __init__(self, window_description: Optional[str] = None) -> None:
        self.window_handle_list = []
        self.window_handle: str = None
        self.window_description: str = window_description if window_description is not None else ""
        if len(self.window_handle_list) == 0:
            self.gather_window_list()
    
    def winEnumHandler(self, hwnd: str, ctx: Any) -> None:
        if win32gui.IsWindowVisible(hwnd):
            self.window_handle_list.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    def window_list_display(self, window_list: Optional[list] = None) -> None:
        _win_list = window_list if window_list is not None else self.window_handle_list
        import PySimpleGUI as sg
        layout = [[sg.Listbox(values=_win_list, size=(30, 6), enable_events=True, bind_return_key=True)]]
        window = sg.Window('Select Window', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            else:
                window.close()
                if len(values) == 1:
                    v = values[0]
                    if len(v) == 1:
                        return v[0]
                    else:
                        return v
                else:
                    return values
    
    def gather_window_list(self) -> None:
        win32gui.EnumWindows(self.winEnumHandler, None)
    
    def close_window(self) -> None:
        self.window_handle = None
        for win in self.window_handle_list:
            if self.window_description == win[1]:
                self.window_handle = win[0]
            elif self.window_description in win[1]:
                self.window_handle = win[0] 
        if self.window_handle is not None:
            win32gui.PostMessage(self.window_handle, win32con.WM_CLOSE, 0, 0)
