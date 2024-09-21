import itertools
import random
import re
import logging
from tqdm import tqdm

from src.setup.logfile import ClassLogFile


# %%

class ClassRandomizer2:
    def __init__(self, str_ref_dna: str, int_ref_length_dna: int, int_number_synthetic: int = 2,
                 dict_segment_weightings: dict = None, dict_base_conversion_weighting: dict = None,
                 dict_codon_conversion_weighting: dict = None, bool_dict_weighting: bool = False,
                 boolean_ambiguous: bool = False, boolean_mixed: bool = False, boolean_deletions: bool = False,
                 boolean_nonsense: bool = True):
        super().__init__()
        self.list_str_dna_bases = self.meth_return_base_options(boolean_ambiguous, boolean_mixed, boolean_deletions,
                                                                boolean_nonsense)
        self.list_str_codons = self.meth_return_codon_options(self.list_str_dna_bases, boolean_nonsense)
        self.dict_active_weighting = self.meth_return_dict_weighting_option(
            bool_dict_weighting=bool_dict_weighting,
            dict_segment_weightings=dict_segment_weightings,
            dict_base_conversion_weighting=dict_base_conversion_weighting,
            dict_codon_conversion_weighting=dict_codon_conversion_weighting
        )
        self.dict_synthetic_dna = self.meth_generate_synthetic_dna_choice(
            int_length_ref_dna=int_ref_length_dna,
            int_number_synthetic=int_number_synthetic,
            list_str_possible_codons=self.list_str_codons,
            bool_dict_weighting=bool_dict_weighting,
            dict_selected_weighting=self.dict_active_weighting
        )
        self.meth_amend_for_nonsense_mutations()
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

    def meth_remove_stop_codons(self, list_str_codons: list):
        str_start_codon, list_str_stop_codons = self.meth_return_fixed_codons()
        list_str_codons_no_stop = [codon for codon in list_str_codons if codon not in list_str_stop_codons]
        self.logger.debug(f"list of codon options (excl. stop codons): {list_str_codons_no_stop}")
        return list_str_codons_no_stop

    def meth_return_codon_options(self, list_str_possible_bases: list, boolean_nonsense):  # boolean flags :(
        list_str_codons = [letter for letter in itertools.product(list_str_possible_bases, repeat=3)]
        list_str_codons = list(map("".join, list_str_codons))
        if boolean_nonsense is False:
            list_str_codons = self.meth_remove_stop_codons(list_str_codons)
        else:
            list_str_codons = list_str_codons
        self.logger.debug(f"list of codon options: {list_str_codons}")
        return list_str_codons

    def meth_return_dict_weighting_option(self, bool_dict_weighting, dict_segment_weightings: dict,
                                          dict_base_conversion_weighting: dict,
                                          dict_codon_conversion_weighting: dict):
        if bool_dict_weighting is True:
            if dict_segment_weightings:
                dict_active_weighting_type = dict_segment_weightings
                self.logger(f"active weighting type is segment")
                return dict_active_weighting_type
            elif dict_base_conversion_weighting:
                dict_active_weighting_type = dict_base_conversion_weighting
                self.logger(f"active weighting type is base")
                return dict_active_weighting_type
            elif dict_codon_conversion_weighting:
                dict_active_weighting_type = dict_codon_conversion_weighting
                self.logger(f"active weighting type is codon")
                return dict_active_weighting_type
            else:
                print("Error: Unknown weighting type, please check weightings supplied")

    def meth_generate_synthetic_dna_weighted(self, int_codon_length: int, dict_weighting_selected: dict):

        list_str_synthetic_dna_codons = random.choices(population=list(dict_weighting_selected.items()),
                                                       weights=list(dict_weighting_selected.keys()),
                                                       k=int_codon_length)
        str_synthetic_dna = "".join(list_str_synthetic_dna_codons)
        print(str_synthetic_dna)
        pass

    def meth_generate_synthetic_dna_non_weighted(self, dict_synthetic_dna: dict, list_str_possible_codons: list,
                                                 int_codon_length: int, int_val_synthetic: int):
        str_start_codon, list_str_stop_codons = self.meth_return_fixed_codons()
        list_str_synthetic_dna_codons = list(random.choice(list_str_possible_codons) for i in range((
                int_codon_length - 2)))  # take 2 codons from length (to account for stop and start codons)
        str_synthetic_dna = "".join(list_str_synthetic_dna_codons)
        str_synthetic_dna = str_start_codon + str_synthetic_dna + random.choice(list_str_stop_codons)
        self.logger.debug(f"synthetic dna {int_val_synthetic + 1} of length, {int_codon_length} \ndna sequence: "
                          f"{str_synthetic_dna}")
        dict_synthetic_dna["seq_number"].append(int_val_synthetic + 1)
        dict_synthetic_dna["str_dna_original"].append(str_synthetic_dna)
        return dict_synthetic_dna

    def meth_generate_synthetic_dna_choice(self, int_length_ref_dna: int, int_number_synthetic: int,
                                           list_str_possible_codons: list[str], bool_dict_weighting: bool,
                                           dict_selected_weighting):
        dict_synthetic_dna = {"seq_number": [], "str_dna_original": [], "str_dna_modified": []}  # create empty
        # dictionary with key of sequence number and value of synthetic dna sequence (original and modified)
        range_seqs = range(0, int_number_synthetic)
        int_codon_length = int((int_length_ref_dna / 3))
        self.logger.debug(f"length codon to produce: {int_codon_length}")
        range_seqs = range(0, int_number_synthetic)

        if bool_dict_weighting is True:
            print("is true")
            self.meth_generate_synthetic_dna_weighted(int_codon_length=int_codon_length,
                                                      dict_weighting_selected=dict_selected_weighting)
            dict_synthetic_dna = None
        else:
            for val in tqdm(range_seqs):
                dict_synthetic_dna = self.meth_generate_synthetic_dna_non_weighted(
                    dict_synthetic_dna=dict_synthetic_dna, list_str_possible_codons=list_str_possible_codons,
                    int_codon_length=int_codon_length, int_val_synthetic=val)
        return dict_synthetic_dna

    def meth_amend_for_nonsense_mutations(self):
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
                f"position of first stop codon in list of codons: {list_str_codons.index(str(list_res[0])) + 1}")
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
