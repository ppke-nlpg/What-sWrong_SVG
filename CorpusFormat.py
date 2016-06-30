from abc import ABCMeta, abstractmethod

# The CorpusFormat interface describes objects that can load a list of NLPInstances from a file. The Corpus can also
# provide a GUI element that allows the user to configure how the file is to be loaded.

# @author Sebastian Riedel

class CorpusFormat(metaclass=ABCMeta):

    # Returns the name of this format.

    # @return the name of this format.
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    # Returns a longer name that may contain information about the configuration of this format.

    # @return the long name of this format.
    @property
    @abstractmethod
    def longName(self):
        pass

    @longName.setter
    @abstractmethod
    def longName(self, value):
        pass
    # Returns the GUI element that controls how this format is to be loaded.

    # @return the GUI element that controls how this format is to be loaded.
    @property
    @abstractmethod
    def accessory(self):
        pass

    @accessory.setter
    @abstractmethod
    def accessory(self, value):
        pass
    # Sets the objects that monitors the progress of this format when loading a file.

    # @param monitor the monitor for this format.
    @abstractmethod
    def setMonitor(self, monitor):
        pass

    # Loads a configuration for this format from the given Properties object.

    # @param properties the Properties object to load from.
    # @param prefix     the prefix that properties for this format have in the Properties object.
    @abstractmethod
    def loadProperties(self, properties, prefix):
        pass

    # Saves the configuration of this format to a Properties object.
    #
    # @param properties the Properties object to store this configuration of this format to.
    # @param prefix     the prefix that the properties should have.
    @abstractmethod
    def saveProperties(self, properties, prefix):
        pass


    # Loads a corpus from a file, starting at instance <code>from</code> and ending at instance <code>to</code>
    # (exclusive). This method is required to call {@link com.googlecode.whatswrong.io.CorpusFormat.Monitor#progressed(int)}
    # after each instance that was processed.

    # @param file the file to load the corpus from.
    # @param from the starting instance index.
    # @param to   the end instance index.
    # @return a list of NLP instances loaded from the given file in the given interval.
    # @throws IOException if I/O goes wrong.
    @abstractmethod
    def load(self, file, From, to):
        pass

    # A Monitor monitors the progress of the {@link com.googlecode.whatswrong.io.CorpusFormat#load(java.io.File, int,
    # int)} method.
    class Monitor(metaclass=ABCMeta):

        # Called whenever one instance was processed in loading of the file.

        # @param index the index of the processed instance.
        @abstractmethod
        def progressed(self, index):
            pass