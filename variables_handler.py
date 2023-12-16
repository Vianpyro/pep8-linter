"""
This module defines a set of PseudoInstructions as an Enum and provides utility functions to work \
    with variable definitions in assembly-like code.

The PseudoInstructions Enum contains symbolic representations of pseudo-instructions found in Pep8 \
    code, which are: ADDRSS, ASCII, BLOCK, BYTE, EQUATE, and WORD.

Functions:
- is_variable_definition(line: str) -> bool:
    Determines whether a given line contains a variable definition by checking for the presence of \
        a colon ':' and any of the pseudo-instructions defined in `PseudoInstructions` Enum.

- get_all_variables(lines: list[str]) -> list[str]:
    Retrieves all lines from a list of strings that represent variable definitions by using the \
        `is_variable_definition` function.

Usage:
    TODO
"""
from enum import Enum


class PseudoInstructions(Enum):
    """
    Represents symbolic representations of pseudo-instructions found in Pep8 code.
    """
    ADDRSS = ".ADDRSS"
    ASCII = ".ASCII"
    BLOCK = ".BLOCK"
    BYTE = ".BYTE"
    EQUATE = ".EQUATE"
    WORD = ".WORD"


def is_variable_definition(line: str) -> bool:
    """
    Determines whether a given line contains a variable definition by checking for the presence of \
        a colon ':' and any of the pseudo-instructions defined in `PseudoInstructions` Enum.
    Args:
        line (str): A string representing a line of code to check.
    Returns:
        bool: True if the line contains a variable definition, False otherwise.
    """
    if not ":" in line:
        return False

    if not any(instruction.value in line for instruction in PseudoInstructions):
        return False

    return True


def get_all_variables(lines: list[str]) -> list[str]:
    """
    Retrieves all lines from a list of strings that represent variable definitions by using the \
        `is_variable_definition` function.
    Args:
        lines (list[str]): A list of strings representing lines of code.
    Returns:
        list[str]: A list containing all lines that define variables.
    """
    return [line for line in lines if is_variable_definition(line)]
