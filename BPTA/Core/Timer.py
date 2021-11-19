import time


class Timer:
    """
    A basic timer to user when waiting some amount of time for a action or step to complete. 
    """
    def __init__(self) -> None:
        """
        Generates and starts a new timer
        """
        self.start_time = time.time()

    def elapsed(self) -> float:
        """
        Get the elapsed time since the timer was started/created in seconds

        Returns:
            float -- Seconds since timer was created and started
        """
        return time.time() - self.start_time
