
from watchdog.events import FileSystemEventHandler
from antiweb_lib.write import write

#@start()
"""
.. _label-filechangehandler:

###################
FileChangeHandler
###################

#@include(FileChangeHandler doc)

#@include(process_event doc)

-   events 'created', 'modified' and 'moved' are handled by the process_event method
-   event 'moved' is triggered when a subdirectory of the monitored source directory
    contains monitored files and the subdirectory is renamed
-   event 'delete' is not handled as for a deleted file no documentation file can be created
-   note that when a file is modified/created watchdog may get multiple events

#@include(file_events)

This method prints the absolute path of the file and type of event that is currently processed.
#@include(print_event)

"""

#@cstart(FileChangeHandler)
class FileChangeHandler(FileSystemEventHandler):
    #@start(FileChangeHandler doc)
    """
    .. py:class:: FileChangeHandler(directory, extensions, options)

       This handler is responsible for handling changed file events on antiweb's daemon mode.

       :param string directory: absolute path to the monitored source directory
       :param tuple<string> extensions: contains all handled file extensions ("*.cs", "*.py", etc)
       :param options: antiweb commandline options

    """
    #@include(FileChangeHandler)

    #@(FileChangeHandler doc)

    def __init__(self, directory, extensions, options):
        self._directory = directory
        #antiweb commandline options
        self._options = options
        self._handled_extensions = extensions

#@cstart(process_event)

    def process_event(self, event):
#@start(process_event doc)
        """
.. py:method:: process_event(self, event)

   Handles the file events: 'modified' | 'created' | 'moved'.
   For each file event the corresponding documentation file is automatically updated with the new content.

   :param event: The file event that should be handled. Possible event types: 'modified' | 'created' | 'moved'
        """

#@include(process_event)
#@(process_event doc)

        changed_file = event.src_path

        if event.event_type == "moved":
            #moved event has to be handled different:
            #the file has been moved so it is now located in event.dest_path
            changed_file = event.dest_path

        if changed_file.endswith(self._handled_extensions):
            self.print_event(event)

            try:
                write(self._directory, changed_file , self._options)
            except SystemExit:
                #sys.exit is called when an input file cannot be opened/found
                #hence we catch the exception to let the daemon continue working
                print("could not process file: ", changed_file)

#@(process_event)


#@cstart(file_events)

    def on_modified(self, event):
        self.process_event(event)

    def on_created(self, event):
        self.process_event(event)

    def on_moved(self, event):
        #this event is triggered when a src directory contains a subdirectory with some files
        #and the subdirectory is renamed. the event is then triggered for all files within
        #the subdirectory and the subdirectory itself
        self.process_event(event)

    def on_deleted(self, event):
        #no file processing should be performed for deleted files
        self.print_event(event)

#@(file_events)

#@cstart(print_event)
    def print_event(self, event):
        print("\n---------------------------------")
        print(event.src_path, event.event_type)
#@(print_event)

#@