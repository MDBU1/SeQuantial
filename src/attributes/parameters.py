from dataclasses import dataclass
from pydantic import BaseModel, field_validator
import datetime as dt

class Order(BaseModel):
    id: int
    item_name: str
    quantity: int
    created_at: dt.datetime
    delivered_to: dt.datetime | None = None

    @field_validator("quantity")
    def validate_quantity(cls, value, int) -> int:
        if value < 1:
            raise ValueError("Quantity must be greater than 0")
        return value


class ClassParameterRandomizer(BaseModel):
    _list_bases_known: list = ["A, G, C, T"]
    _list_bases_ambiguous: list = ["N, -"]
    _list_bases_mixed: list = ["R, Y, B, D, K, M, H, V, S, W, N"]
    str_ref_dna: str
    int_ref_dna_length: int
    int_number_synthetic: int
    dict_segment_weightings: dict = None
    dict_codon_conversion_weighting: dict = None
    bool_dict_weightings: bool = False
    bool_ambiguous: bool = False
    bool_mixed: bool = False
    bool_deletions: bool = False
    bool_nonsense: bool = True

    @field_validator("str_ref_dna")
    def validate_str_ref_dna(cls, value, str) -> str:
        chars = set('qeiopfjlz,')
        if any((c.casefold() in chars) for c in value.casefold()):
            raise ValueError("Unidentified base character")
        return value






# @dataclass
# class ClassParameterRandomiser:
#     """
#     Description:
#     """
#     str_ref_dna: str
#     int_ref_length_dna: int
#     int_number_synthetic: int = 2
#     dict_segment_weightings: dict = None
#     dict_base_conversion_weighting: dict = None,
#     dict_codon_conversion_weighting: dict = None
#     bool_dict_weighting: bool = False
#     boolean_ambiguous: bool = False
#     boolean_mixed: bool = False
#     boolean_deletions: bool = False
#     boolean_nonsense: bool = True