
from watchdog.events import FileSystemEventHandler
from antiweb_lib.write import write
from antiweb_lib.write import create_write_string
import time

#@start()
"""
.. _label-filechangehandler:

###################
FileChangeHandler
###################

#@include(FileChangeHandler doc)

#@include(process_event doc)

-   events 'created', 'modified', 'moved' and 'deleted' are handled by the process_event method
-   event 'moved' is triggered when a subdirectory of the monitored source directory
    contains monitored files and the subdirectory is renamed
-   note that when a file is modified/created watchdog may get multiple events
-   note that when the monitored source directory and the output directory are the same events are triggered for
    the created documentation files - this causes antiweb to process the documentation files

#@include(file_events)

"""

#@cstart(FileChangeHandler)
class FileChangeHandler(FileSystemEventHandler):
    #@start(FileChangeHandler doc)
    """
    .. py:class:: FileChangeHandler(directory, extensions, options)

       This handler is responsible for handling changed file events in antiweb's daemon mode.

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
        self._event_counter = 0

#@cstart(process_event)

    def process_event(self, event):
#@start(process_event doc)
        """
.. py:method:: process_event(self, event)

   Handles the file events: 'modified' | 'created' | 'moved' | 'deleted'.

   The events trigger an update of the corresponding documentation file.
   Ignored events are: deleted files, changed directories, files without a handled extension.

   :param event: The file event that should be handled. Possible event types: 'modified' | 'created' | 'moved' | 'deleted'
        """

#@include(process_event)
#@(process_event doc)

        self._event_counter += 1
        time_stamp = "[" + time.strftime('%H:%M:%S') + " " + str(self._event_counter).zfill(5) + "] "

        changed_file = event.src_path

        if event.event_type == "moved":
            #moved event has to be handled differently:
            #the file has been moved so it is now located in event.dest_path
            changed_file = event.dest_path

        if changed_file.endswith(self._handled_extensions) and not event.is_directory and \
                not event.event_type =="deleted":
            try:
                could_write, created_file = write(self._directory, changed_file, self._options)
                event_string = create_write_string(could_write, changed_file, created_file)

            except SystemExit:
                #sys.exit is called when an input file cannot be opened/found
                #hence we catch the exception to let the daemon continue working
                event_string = "Catched SysExit: File: " + created_file + " could not be generated"
        else:
            #ignored event
            event_string = "Ignored change: " + changed_file + " [" + event.event_type + "]"

        print(time_stamp + event_string)

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
        self.process_event(event)

#@(file_events)

#@