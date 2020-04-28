import inspect


class Logger:
    """docstring for Logger"""

    def __init__(self, debug_file):
        self.debug_file = debug_file
        self.log("\n\nBeginning of logging.\n\n")

    def log(self, message):
        with open(self.debug_file, "a") as debug_file:
            debug_file.write(str(message))
            debug_file.write("\n")

    def log_function_calls(self, called_function):
        def print_called_function_name(*args, **kwargs):
            fct_calls = [
                f"{frameInfo[1]}->{frameInfo[3]}" for frameInfo in inspect.stack() if 'print_called_function_name' not in frameInfo[3]
            ]
            # fct_calls.pop(0)
            # fct_calls.pop(len(fct_calls)-1)
            self.log(f"Following function has been called: {called_function.__name__}")
            self.log(fct_calls)
            self.log("------")
            called_function(*args, **kwargs)

        return print_called_function_name



def test():
    logger = Logger("debug_file.txt")


    @logger.log_function_calls
    def say_whee():
        logger.log("wheeeee")


    @logger.log_function_calls
    def call_say_whee():
        say_whee()

    @logger.log_function_calls
    def call_call_say_whee():
        call_say_whee()


    call_call_say_whee()

if __name__ == '__main__':
    test()