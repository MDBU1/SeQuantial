import itertools
import random
import re
from tqdm import tqdm

from src.setup.logfile import ClassLogFile


# %%

class ClassRandomizer(ClassLogFile):
    def __init__(self, str_ref_dna: str, int_ref_length_dna: int, int_number_synthetic: int = 2,
                 dict_segment_weightings: dict = None, dict_base_conversion_weighting: dict = None,
                 dict_codon_conversion_weighting: dict = None, boolean_ambiguous: bool = False,
                 boolean_mixed: bool = False, boolean_deletions: bool = False, boolean_nonsense: bool = False):
        super().__init__()
        self.meth_weightings_is_true(dict_segment_weightings, int_number_synthetic)
        self.list_dna_bases = self.meth_return_base_options(boolean_ambiguous, boolean_mixed, boolean_deletions,
                                                            boolean_nonsense)
        self.dict_synthetic_dna = self.meth_generate_synthetic_dna(length=int_ref_length_dna,
                                                                   int_number_synthetic=int_number_synthetic,
                                                                   boolean_nonsense=boolean_nonsense,
                                                                   list_str_letters=self.list_dna_bases)
        self.meth_amend_for_nonsense_mutations_v2()
        self.meth_add_ref_sequence_to_dict(str_ref_dna, self.dict_synthetic_dna)

    def meth_return_fixed_codons(self) -> tuple[str, list[str]]:
        str_start_codon = "ATG"
        list_str_stop_codon = ["TAA", "TAG", "TGA"]  # x3 options of stop codons
        self.logger.debug(f"start codon: {str_start_codon}")
        self.logger.debug(f"stop codons: {list_str_stop_codon}")
        return str_start_codon, list_str_stop_codon

    def meth_return_base_options(self, boolean_ambiguous, boolean_mixed, boolean_deletions, boolean_nonsense) \
            -> list[str]:
        # bases
        list_str_letters = ["A", "C", "G", "T"]
        # process ambiguous bases option
        if boolean_ambiguous is True:
            list_str_letters.append("N")
            self.logger.debug(f"including ambiguous bases as boolean_mixed is True")
        # process mixed bases option
        if boolean_mixed is True:
            list_str_letters.append("M")
            self.logger.debug(f"including mixed bases as boolean_mixed is True")
        # process deletions option
        if boolean_deletions is True:
            list_str_letters.append("-")
            self.logger.debug(f"including deletions as boolean_deletions is True")
        if boolean_nonsense is True:
            self.logger.debug(f"including nonsense mutations as boolean_nonsense is True")
        if boolean_nonsense is False:
            self.logger.debug(f"including nonsense mutations as boolean_nonsense is False")
        return list_str_letters

    # def meth_generate_synthetic_dna(self, length: int, int_number_synthetic: int, list_str_letters: list[str]) ->
    # dict: # Todo split into sub functions # list_str_letters = self.meth_return_base_options() self.logger.debug(
    #  f"potential bases: {list_str_letters}") str_start_codon, list_str_stop_codons = self.meth_return_fixed_codons()
    #
    #     dict_synthetic_dna = {"seq_number": [], "str_dna_original": [], "str_dna_modified": []}  # create empty
    #     # dictionary with key of sequence number and value of synthetic dna sequence (original and modified)
    #     range_seqs = range(0, int_number_synthetic)
    #     for val in tqdm(range_seqs):
    #         if self.boolean_nonsense is True:
    #             str_synthetic_dna = ''.join(random.choice(list_str_letters) for i in range(length - 6))  # take 6
    #             # bases from length to (x3 start, x3 end) to account for start and stop codons
    #             str_synthetic_dna = str_start_codon + str_synthetic_dna + random.choice(list_str_stop_codons)
    #             self.logger.debug(f"synthetic dna {val + 1} of length, {length} \ndna sequence: {str_synthetic_dna}")
    #             dict_synthetic_dna["seq_number"].append(val + 1)
    #             dict_synthetic_dna["str_dna_original"].append(str_synthetic_dna)
    #         if self.boolean_nonsense is False:
    #             list_str_codons = [letter for letter in itertools.product(list_str_letters, repeat=3)]
    #             # Todo create string -> codon function
    #             list_str_codons = list(map("".join, list_str_codons))
    #             self.logger.debug(f"list of codon options: {list_str_codons}")
    #             list_str_codons_no_stop = [codon for codon in list_str_codons if codon not in list_str_stop_codons]
    #             self.logger.debug(f"list of codon options (excl. stop codons): {list_str_codons_no_stop}")
    #             int_codon_length = int((length / 3))
    #             self.logger.debug(f"length codon to produce: {int_codon_length}")
    #             # TODO above -> new separate method then call and set parameters before loop
    #             list_str_synthetic_dna_codons = list(random.choice(list_str_codons_no_stop) for i in range((
    #                     int_codon_length - 2)))  # take 2 codons from length (to account for stop and start codons)
    #             # self.logger.debug(f"length of codons in synthetic dna sequence: {list_str_synthetic_dna_codons}")
    #             str_synthetic_dna = "".join(list_str_synthetic_dna_codons)
    #             str_synthetic_dna = str_start_codon + str_synthetic_dna + random.choice(list_str_stop_codons)
    #             self.logger.debug(f"synthetic dna {val + 1} of length, {length} \ndna sequence: {str_synthetic_dna}")
    #             dict_synthetic_dna["seq_number"].append(val + 1)
    #             dict_synthetic_dna["str_dna_original"].append(str_synthetic_dna)
    #     return dict_synthetic_dna

    def meth_boolean_nonsense_is_true(self, list_str_letters: list[str], length: int, dict_synthetic_dna: dict,
                                      val: int):
        str_start_codon, list_str_stop_codons = self.meth_return_fixed_codons()
        str_synthetic_dna = ''.join(random.choice(list_str_letters) for i in range(length - 6))  # take 6
        # bases from length to (x3 start, x3 end) to account for start and stop codons
        str_synthetic_dna = str_start_codon + str_synthetic_dna + random.choice(list_str_stop_codons)
        self.logger.debug(f"synthetic dna {val + 1} of length, {length} \ndna sequence: {str_synthetic_dna}")
        dict_synthetic_dna["seq_number"].append(val + 1)
        dict_synthetic_dna["str_dna_original"].append(str_synthetic_dna)
        return dict_synthetic_dna

    def meth_boolean_nonsense_is_false(self, list_str_letters: list[str], length: int, dict_synthetic_dna: dict,
                                       val: int):
        str_start_codon, list_str_stop_codons = self.meth_return_fixed_codons()

        list_str_codons = [letter for letter in itertools.product(list_str_letters, repeat=3)]
        # Todo create string -> codon function
        list_str_codons = list(map("".join, list_str_codons))
        self.logger.debug(f"list of codon options: {list_str_codons}")
        list_str_codons_no_stop = [codon for codon in list_str_codons if codon not in list_str_stop_codons]
        self.logger.debug(f"list of codon options (excl. stop codons): {list_str_codons_no_stop}")
        int_codon_length = int((length / 3))
        self.logger.debug(f"length codon to produce: {int_codon_length}")
        list_str_synthetic_dna_codons = list(random.choice(list_str_codons_no_stop) for i in range((
                int_codon_length - 2)))  # take 2 codons from length (to account for stop and start codons)
        str_synthetic_dna = "".join(list_str_synthetic_dna_codons)
        str_synthetic_dna = str_start_codon + str_synthetic_dna + random.choice(list_str_stop_codons)
        self.logger.debug(f"synthetic dna {val + 1} of length, {length} \ndna sequence: {str_synthetic_dna}")
        dict_synthetic_dna["seq_number"].append(val + 1)
        dict_synthetic_dna["str_dna_original"].append(str_synthetic_dna)
        return dict_synthetic_dna

    def meth_generate_synthetic_dna(self, length: int, int_number_synthetic: int, boolean_nonsense: bool,
                                    list_str_letters: list[str]) -> dict:
        self.logger.debug(f"potential bases: {list_str_letters}")
        # str_start_codon, list_str_stop_codons = self.meth_return_fixed_codons()

        dict_synthetic_dna = {"seq_number": [], "str_dna_original": [], "str_dna_modified": []}  # create empty
        # dictionary with key of sequence number and value of synthetic dna sequence (original and modified)
        range_seqs = range(0, int_number_synthetic)
        if boolean_nonsense is True:
            for val in tqdm(range_seqs):
                dict_synthetic_dna = self.meth_boolean_nonsense_is_true(list_str_letters=list_str_letters,
                                                                        dict_synthetic_dna=dict_synthetic_dna,
                                                                        length=length, val=val)
        elif boolean_nonsense is False:
            for val in tqdm(range_seqs):
                dict_synthetic_dna = self.meth_boolean_nonsense_is_false(list_str_letters=list_str_letters,
                                                                         dict_synthetic_dna=dict_synthetic_dna,
                                                                         length=length, val=val)
        return dict_synthetic_dna

    # def meth_amend_for_nonsense_mutations_old(self, dict_synthetic_dna):
    # introduction of stop codons
    # list_str_stop_codon = self.meth_return_fixed_codons()[1]  # take second return parameter = stop codon list
    # # loop through synthetic dan dictionary if stop mutations found before the end delete remaining str
    # for i, v in enumerate(dict_synthetic_dna["str_dna_original"].copy()):
    #     # print(i)
    #     str_dna = self.dict_synthetic_dna["str_dna_original"][i]
    #     # print(str_dna)
    #     str_dna_minus_start = str_dna[3:]
    #     self.logger.debug(f"dna minus start codon: {str_dna_minus_start}")
    #     self.logger.debug(f"type var str_dna_minus_start: {type(str_dna_minus_start)}")
    #     str_stop_codons_pipe = '|'.join(list_str_stop_codon)
    #     res = re.search(fr'{str_stop_codons_pipe}', str_dna_minus_start)
    #     int_first_nonsense = int(res.end())  # use end to keep first stop codon match as part of sequence
    #     str_nonsense_dna = str_dna_minus_start[:int_first_nonsense]
    #     #print(str_nonsense_dna)
    #     self.dict_synthetic_dna["str_dna_modified"].append(str_nonsense_dna)
    # line_format = '%s : %s'
    # br = "\n".join([line_format % (key, str(value)) for key, value in self.dict_synthetic_dna.items()])
    # self.logger.info(f"dna sequence: {br}")

    def meth_amend_for_nonsense_mutations(self):
        # introduction of stop codons
        list_str_stop_codon = self.meth_return_fixed_codons()[1]  # take second return parameter = stop codon list
        # loop through synthetic dan dictionary if stop mutations found before the end delete remaining str
        for i, v in enumerate(self.dict_synthetic_dna["str_dna_original"].copy()):
            str_dna = self.dict_synthetic_dna["str_dna_original"][i]
            # TODO convert to codons currently detecting any position is string
            str_dna_minus_start = str_dna[3:]
            self.logger.debug(f"dna minus start codon: {str_dna_minus_start}")
            self.logger.debug(f"type var str_dna_minus_start: {type(str_dna_minus_start)}")
            str_stop_codons_pipe = '|'.join(list_str_stop_codon)
            x = 3
            # list_str_dna_minus_start_codons = [str_dna_minus_start[y - x:y] for y in
            #                                    range(x, len(str_dna_minus_start) + x, x)]
            res = re.search(fr'{str_stop_codons_pipe}', str_dna_minus_start)
            int_first_nonsense = int(res.end())  # use end to keep first stop codon match as part of sequence
            str_nonsense_dna = str_dna_minus_start[:int_first_nonsense]
            self.dict_synthetic_dna["str_dna_modified"].append(str_nonsense_dna)
        line_format = '%s : %s'
        br = "\n".join([line_format % (key, str(value)) for key, value in self.dict_synthetic_dna.items()])
        self.logger.info(f"dna sequence: {br}")

    def meth_amend_for_nonsense_mutations_v2(self):
        list_str_stop_codons = self.meth_return_fixed_codons()[1]  # take second return parameter = stop codon list
        for i, v in enumerate(self.dict_synthetic_dna["str_dna_original"].copy()):
            str_dna = self.dict_synthetic_dna["str_dna_original"][i]
            # str_stop_codons_pipe =
            # convert str -> list of x3 string i.e. codons
            x = 3
            list_str_codons = [str_dna[i:i + x] for i in range(0, len(str_dna), x)]
            self.logger.debug(f"codons of dna sequence minus start codon: {list_str_codons}")
            self.logger.debug(f"no. codons in dna sequence minus start codon: {len(list_str_codons)}")
            list_res = [codon for codon in list_str_codons if (codon in list_str_stop_codons)]  # searches for stop
            # codons in dna sequence list of codons
            self.logger.debug(f'no of stop codons found in sequence: {len(list_res)}')
            self.logger.debug(f"first stop codon found: {list_res[0]}")
            self.logger.debug(
                f"position of first codon in list of codons:{list_str_codons.index(str(list_res[0])) + 1}")
            list_str_nonsense_dna = list_str_codons[:list_str_codons.index(str(list_res[0])) + 1]
            # join list codons-> dna string
            str_nonsense_dna = ''.join(list_str_nonsense_dna)
            self.dict_synthetic_dna["str_dna_modified"].append(str_nonsense_dna)
        line_format = '%s : %s'
        br = "\n".join([line_format % (key, str(value)) for key, value in self.dict_synthetic_dna.items()])
        self.logger.info(f"dna sequence: {br}")

    def meth_add_ref_sequence_to_dict(self, str_ref_dna: str, dict_synthetic_dna: dict):
        """remove repetitions and/or junk from earlier methods"""
        update_dict = {"ref": str_ref_dna}
        dict_synthetic_dna.pop("str_dna_original", None)
        dict_synthetic_dna.update(update_dict)  # TODO change so doesn't create new key
        self.dict_synthetic_dna = dict_synthetic_dna
        self.logger.debug(f"adding reference to synthetic dictionary")
        self.logger.debug(f"{dict_synthetic_dna}")

    def meth_weightings_is_true(self, dict_segment_weightings: dict, int_number_synthetic: int):
        if dict_segment_weightings:
            random.choices(population=list(dict_segment_weightings.items()),
                           weights=list(dict_segment_weightings.keys()),
                           k=int_number_synthetic)
        else:
            pass

