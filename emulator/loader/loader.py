import abc


class MatrixLoader(abc.ABC):

    @abc.abstractmethod
    def load_matrix_values(self, emulator):
        pass
