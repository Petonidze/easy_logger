# easy_logger
This logger is easier to use than the standard one, since it will already be configured and all that remains is to import its instance. 
The settings can be used by default from DefaultLoggerSettings, or your own. 
Thanks to the formatter, the output to the console will be more attractive.

What settings can be customized:
1) TO_FILE - writing to file
2) TO_CONSOLE - writing to console
3) LEVEL_DEV - log level for development enviroment
4) LEVEL_PROD - log level for production enviroment
5) LOG_FILENAME - log filename. For example: app1.log
6) SAVE_PATH - change if you want to place the directory for storing log files in a different location than the place where the logger is located
7) MAX_FILE_SIZE - max log file size in bytes 
8) BACKUP_COUNT - count of log files
9) FORMAT - for more details about customizing: https://docs.python.org/3/library/logging.html#formatter-objects
