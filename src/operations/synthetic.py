from src.operations.randomiser2 import ClassRandomizer2
from src.operations.reference import ClassRefSequence
from src.operations.randomiser import ClassRandomizer


# %%

class ClassSyntheticGenerator(ClassRefSequence):
    def __init__(self, input_fasta=None):
        super().__init__(input_fasta)
        self.meth_return_synthetic_dna()

    def meth_return_synthetic_dna(self):
        parameters_synthetic_dna = ClassRandomizer2(self.str_dna, self.int_length_dna)
