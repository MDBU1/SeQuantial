import os
import pandas as pd

from src.setup.logfile import ClassLogFile
from pydantic import BaseModel, field_validator


# %%




class ClassRefSequence(ClassLogFile):
    def __init__(self, input_fasta, input_str_sequence_name=None):
        super().__init__()
        self.str_header = self.meth_parse_fasta_header(input_fasta)
        self.str_dna = self.meth_parse_fasta_seq(input_fasta)
        self.int_length_dna = self.meth_calc_length_sequence(self.str_dna)
        self.dict_dna_composition = self.meth_calc_sequence_composition(self.str_dna)
        self.meth_calc_no_stop_codons_and_positions(self.str_dna)

    def meth_parse_fasta_header(self, seq) -> str:
        sequence = open(seq, 'r')
        for seqID, line in enumerate(sequence):
            if line.startswith(">"):
                header = line.strip()
                self.logger.info(f"reference sequence loaded: " + header.replace(">", ""))
                return header

    def meth_parse_fasta_seq(self, seq) -> str:
        sequence = open(seq, 'r')
        for seqID, line in enumerate(sequence):
            if line.startswith(">"):
                header = line.strip()
            else:
                dna = line.strip("\n")
                self.logger.info(f"reference sequence: {dna}")
                return dna

    def meth_calc_length_sequence(self, seq) -> int:
        int_length_sequence = len(seq)
        self.logger.info(f"reference sequence length: {int_length_sequence}")
        return int_length_sequence

    def meth_calc_sequence_composition(self, seq) -> dict:
        dict_seq = dict.fromkeys(seq, 0)
        for i in seq:
            dict_seq[i] += 1
        self.logger.info(f"sequence base composition: {dict_seq}")
        return dict_seq

    def meth_calc_no_stop_codons_and_positions(self, seq) -> dict:
        list_stop_codons = ["TAA", "TAG", "TGA"]
        ref_seq_codons = [seq[i:i + 3] for i in range(0, len(seq), 3)]
        self.logger.debug(f"reference sequence as codons: {ref_seq_codons}")
        # print(ref_codon)
        list_int_stop_codons = []
        for i in list_stop_codons:
            int_stop_codons = i, ref_seq_codons.count(i)
            list_int_stop_codons.append(int_stop_codons)
        self.logger.debug(f"reference sequence no stop codons: {list_int_stop_codons}")
        # create dictionary of positions of stop codons -> swap in when randomising
