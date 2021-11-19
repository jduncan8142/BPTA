import logging
import os
from typing import Optional


class Logger:
    def __init__(self, log_name: Optional[str] = "default", log_path: Optional[str] = "output", verbosity: Optional[int] = 3, format: Optional[str] = "%(asctime)s - %(levelname)s - %(message)s", mode: Optional[str] = "a") -> None:
        self.enabled: bool = True
        self.log_name: str = log_name
        self.log_path: str = log_path
        self.log_file: str = f"{self.log_name}.log"
        self.format: str = format
        self.mode: str = mode
        __log_dir: str = os.path.join(os.getcwd(), self.log_path) 
        if not os.path.exists(__log_dir):
            try:
                os.mkdir(__log_dir)
            except Exception as err:
                raise FileNotFoundError(f"Directory {__log_dir} does not exist and was unable to be created automatically. Make sure you have the required access.")
        if not os.path.isfile(self.log_file):
            with open(self.log_file, "w") as f:
                pass
        __log_file: str = os.path.join(__log_dir, self.log_file)
        if not os.path.isfile(__log_file):
            try:
                with open(self.log_file, "w") as f:
                    pass
            except Exception as err:
                raise FileNotFoundError(f"File {__log_file} does not exist and was unable to be created automatically. Make sure you have the required access.")
        
        # Create custom logging level for screenshots
        SCREENSHOT_LEVELV_NUM = 25 
        logging.addLevelName(SCREENSHOT_LEVELV_NUM, "SHOT")
        def shot(self, message, *args, **kws):
            if self.isEnabledFor(SCREENSHOT_LEVELV_NUM):
                # Yes, logger takes its '*args' as 'args'.
                self._log(SCREENSHOT_LEVELV_NUM, message, args, **kws)
        logging.Logger.shot = shot

        # Create custom logging level for status
        STATUS_LEVELV_NUM = 55 
        logging.addLevelName(STATUS_LEVELV_NUM, "STATUS")
        def status(self, message, *args, **kws):
            if self.isEnabledFor(STATUS_LEVELV_NUM):
                # Yes, logger takes its '*args' as 'args'.
                self._log(STATUS_LEVELV_NUM, message, args, **kws)
        logging.Logger.status = status

        # Create custom logging level for documentation
        DOUMENTATION_LEVELV_NUM = 60 
        logging.addLevelName(DOUMENTATION_LEVELV_NUM, "DOCUMENTATION")
        def documentation(self, message, *args, **kws):
            if self.isEnabledFor(DOUMENTATION_LEVELV_NUM):
                # Yes, logger takes its '*args' as 'args'.
                self._log(DOUMENTATION_LEVELV_NUM, message, args, **kws)
        logging.Logger.documentation = documentation

        self.log: logging.Logger = logging.getLogger(__log_file)
        self.formatter: logging.Formatter = logging.Formatter(self.format)
        self.file_handler: logging.FileHandler = logging.FileHandler(__log_file, mode=self.mode)
        self.file_handler.setFormatter(self.formatter)
        self.stream_handler: logging.StreamHandler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.verbosity: int = verbosity
        match self.verbosity:
            case 5:
                self.log.setLevel(10)
                self.file_handler.setLevel(10)
                self.stream_handler.setLevel(10)
            case 4:
                self.log.setLevel(20)
                self.file_handler.setLevel(20)
                self.stream_handler.setLevel(20)
            case 3:
                self.log.setLevel(25)
                self.file_handler.setLevel(25)
                self.stream_handler.setLevel(30)
            case 2:
                self.log.setLevel(25)
                self.file_handler.setLevel(25)
                self.stream_handler.setLevel(40)
            case 1:
                self.log.setLevel(25)
                self.file_handler.setLevel(25)
                self.stream_handler.setLevel(50)
            case _:
                self.log.setLevel(25)
                self.file_handler.setLevel(25)
                self.stream_handler.setLevel(90)
        self.log.addHandler(self.file_handler)
        self.log.addHandler(self.stream_handler)
