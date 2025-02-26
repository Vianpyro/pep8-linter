import re
import sys
import glob


class PepLinter:
    def __init__(self):
        # Instructions matching the highlighter
        self.instruction_pattern = re.compile(
            r"\b(ADD(A|SP|X)|AND(A|X)|ASL(A|X)|ASR(A|X)|"
            r"BR|BR(C|EQ|GE|GT|LE|LT|NE|V)|CALL|CHAR(I|O)|"
            r"CP(A|X)|DEC(I|O)|LD(A|X|BYTEA|BYTEX)|MOV(FLGA|SPA)|"
            r"NEG(A|X)|NOP(0|1|2|3)?|NOT(A|X)|OR(A|X)|"
            r"RET(0|1|2|3|4|5|6|7|TR)|ROL(A|X)|ROR(A|X)|"
            r"ST(A|X|BYTEA|BYTEX)|STOP|STRO|STX|SUB(A|X|SP))\b",
            re.IGNORECASE,
        )

        # Directives matching the highlighter
        self.directive_pattern = re.compile(
            r"^[.]\b(EQUATE|ASCII|BLOCK|BURN|BYTE|END|WORD|ADDRSS)\b", re.IGNORECASE
        )

        # Label pattern
        self.label_pattern = re.compile(r"^([A-Za-z_]\w*):")

        # Comment pattern
        self.comment_pattern = re.compile(r";.*")

        # Warning and error patterns
        self.warning_pattern = re.compile(r";WARNING:[\s].*$", re.IGNORECASE)
        self.error_pattern = re.compile(r";ERROR:[\s].*$", re.IGNORECASE)

        self.defined_labels = set()
        self.errors = []

    def lint(self, code):
        """Runs linting on the provided PEP8 assembly code."""
        self.errors.clear()
        self.defined_labels.clear()
        lines = code.split("\n")

        for line_number, line in enumerate(lines):
            line = line.strip()
            if not line or self.comment_pattern.match(
                line
            ):  # Ignore empty lines and comments
                continue
            self.check_line(line, line_number)

        return self.errors  # Returns list of (line, message) tuples

    def check_line(self, line, line_number):
        # Remove inline comments
        line = re.sub(self.comment_pattern, "", line).strip()
        tokens = line.split()
        if not tokens:
            return

        first_token = tokens[0]

        # Check for label definition
        label_match = self.label_pattern.match(first_token)
        if label_match:
            label = label_match.group(1)
            if label in self.defined_labels:
                self.errors.append((line_number, f"Duplicate label: {label}"))
            else:
                self.defined_labels.add(label)
            tokens.pop(0)  # Remove label from processing

        if not tokens:
            return

        first_token = tokens[0].upper()

        # Regex pattern for instructions that do not require an operand
        no_operand_instructions_pattern = re.compile(
            r"^(ASL(A|X)|ASR(A|X)|STOP|(RET|NOP)0?)$", re.IGNORECASE
        )

        # Check for valid directives using regex
        if self.directive_pattern.match(first_token):
            if len(tokens) < 2 and first_token != ".END":
                self.errors.append(
                    (line_number, f"Directive {first_token} requires an argument.")
                )

        # Check for valid instructions using regex
        elif self.instruction_pattern.match(first_token):
            # If the instruction requires an operand, but none is provided, flag it
            if len(tokens) < 2 and not no_operand_instructions_pattern.match(
                first_token
            ):
                self.errors.append(
                    (line_number, f"Instruction {first_token} requires an operand.")
                )

        # Unknown instruction or directive
        else:
            self.errors.append(
                (line_number, f"Unknown instruction or directive: {first_token}")
            )


def main():
    if len(sys.argv) < 2:
        print("Usage: python peplinter.py <file1> <file2> ...")
        sys.exit(1)

    file_patterns = sys.argv[1:]
    filenames = []

    for pattern in file_patterns:
        filenames.extend(glob.glob(pattern))

    if not filenames:
        print("Error: No matching files found.")
        sys.exit(1)

    linter = PepLinter()
    error_found = False

    for filename in filenames:
        try:
            with open(filename, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            error_found = True
            continue

        errors = linter.lint(code)

        if errors:
            print(f"Linting errors in {filename}:")
            for line, message in errors:
                print(f"  Line {line + 1}: {message}")
            error_found = True
        else:
            print(f"No linting errors found in {filename}.")

    sys.exit(1 if error_found else 0)


if __name__ == "__main__":
    main()
