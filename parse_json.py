from dataclasses import dataclass
from typing import Any, Protocol

result_type = str | float | int | list[Any] | dict[Any, Any] | tuple[str, Any] | None


def result_from_tuple(
    success, parsed: result_type = None, remainder: str | None = None
):
    return Result(success=success, parsed=parsed, remainder=remainder)


@dataclass
class Result:
    success: bool
    parsed: result_type
    remainder: str | None

    def __iter__(self):
        return iter((self.success, self.parsed, self.remainder))


class Parser(Protocol):
    def parse(self, string: str) -> Result:
        ...


def safe_parse(parser: type[Parser], string: str) -> Result:
    if not string:
        return result_from_tuple(False)

    return parser().parse(string)


def safe_parse_with_whitespace(parser: type[Parser], string: str) -> Result:
    success, _, remainder = safe_parse(ParseWhiteSpace, string)

    if success and not remainder:
        return result_from_tuple(False)

    return safe_parse(parser, remainder if success else string)


def try_parsers(
    data_to_parse: str, parsers: list[type[Parser]]
) -> tuple[str | float | int | list[Any] | dict[Any, Any], str]:
    for parser in parsers:
        child_success, child_parsed, child_remainder = safe_parse_with_whitespace(
            parser, data_to_parse
        )

        if child_success:
            data_to_parse = child_remainder
            return child_parsed, data_to_parse

    raise Exception("Failed to parse")


def get_rid_of_comma_and_whitespaces(data_to_parse: str):
    sucess_no_spaces, _, data_to_parse_no_whitespace = safe_parse(
        ParseWhiteSpace, data_to_parse
    )

    if sucess_no_spaces:
        data_to_parse = data_to_parse_no_whitespace

    if not data_to_parse:
        return ""

    comma_success, _, data_to_parse = safe_parse_with_whitespace(
        ParseComma, data_to_parse
    )

    # if there is something that is not a comma between last element and closing bracket eg [1,3 414]
    if not comma_success:
        raise Exception("Failed to parse")

    # if ends with comma [2, ]
    if not data_to_parse:
        raise Exception("Failed to parse")

    return data_to_parse


class ParseQuotes:
    def parse(self, string: str) -> Result:
        if string[0] == '"':
            string = string[1:]
            end_quote_ind = -1
            for i, l in enumerate(string):
                if l == '"' and (i == 0 or string[i - 1] != "\\"):
                    end_quote_ind = i
                    break
            if end_quote_ind == -1:
                raise Exception("Parsing error. Unclosed quote")

            return result_from_tuple(
                True, string[:end_quote_ind], string[end_quote_ind + 1 :]
            )
        return result_from_tuple(False)


class ParseCurlyBrackets:
    def parse(self, string: str) -> Result:
        if string[0] == "{":
            open_number = 0

            end_bracket_ind = -1

            for i, char in enumerate(string):
                if char == "{":
                    open_number += 1

                if char == "}":
                    open_number -= 1

                if open_number == 0:
                    end_bracket_ind = i
                    break

            if open_number != 0:
                raise Exception("Parsing error. Unclosed curly bracket")

            return result_from_tuple(
                True, string[1:end_bracket_ind], string[end_bracket_ind + 1 :]
            )
        return result_from_tuple(False)


class ParseSquareBrackets:
    def parse(self, string: str) -> Result:
        if string[0] == "[":
            open_number = 0

            end_bracket_ind = -1

            for i, char in enumerate(string):
                if char == "[":
                    open_number += 1

                if char == "]":
                    open_number -= 1

                if open_number == 0:
                    end_bracket_ind = i
                    break

            if open_number != 0:
                raise Exception("Parsing error. Unclosed square bracket")

            return result_from_tuple(
                True, string[1:end_bracket_ind], string[end_bracket_ind + 1 :]
            )
        return result_from_tuple(False)


class ParseWhiteSpace:
    def parse(self, string: str) -> Result:
        if string[0].isspace():
            last_conseq_space = 0
            for i, l in enumerate(string):
                if l.isspace():
                    last_conseq_space = i
                else:
                    break

            return result_from_tuple(True, "", string[last_conseq_space + 1 :])
        return result_from_tuple(False)


class ParsePositiveNumber:
    def __is_number(self, char: str) -> bool:
        try:
            _ = int(char)
            return True
        except ValueError:
            return False

    # does not match fancy "1e40"  floats
    def parse(self, string: str) -> Result:
        if not self.__is_number(string[0]):
            return result_from_tuple(False)

        full_number = ""
        is_float = False

        for _, char in enumerate(string):
            if self.__is_number(char):
                full_number += char
            elif char == ".":
                if is_float:
                    raise Exception("Parsing error. Invalid number")

                is_float = True
                full_number += "."

            else:
                break
        if full_number[-1] == ".":
            raise Exception("Parsing error. Invalid number")

        return result_from_tuple(
            True, (float if is_float else int)(full_number), string[len(full_number) :]
        )


class ParseMinus:
    def parse(self, string: str) -> Result:
        if string[0] == "-":
            return result_from_tuple(True, "-", string[1:])

        return result_from_tuple(False)


class ParseColon:
    def parse(self, string: str) -> Result:
        if string[0] == ":":
            return result_from_tuple(True, ":", string[1:])

        return result_from_tuple(False)


class ParseComma:
    def parse(self, string: str) -> Result:
        if string[0] == ",":
            return result_from_tuple(True, ",", string[1:])

        return result_from_tuple(False)


class ParseNumber:
    def parse(self, string: str) -> Result:
        negative_success, _, remainder = ParseMinus().parse(string)
        remainder = remainder if negative_success else string

        success, parsed, remainder = safe_parse_with_whitespace(
            ParsePositiveNumber, remainder
        )

        if not success and negative_success:
            raise Exception("Failed to parse a number")
        if success and negative_success:
            parsed = -parsed
        return result_from_tuple(success, parsed, remainder)


class ParseList:
    def parse(self, string: str) -> Result:
        success, data_to_parse, remainder = safe_parse_with_whitespace(
            ParseSquareBrackets, string
        )

        result = []
        if success:
            while data_to_parse:
                child_parsed, data_to_parse = try_parsers(
                    data_to_parse,
                    [ParseQuotes, ParseNumber, ParseList, ParseDictionary],
                )
                result.append(child_parsed)

                sucess_no_spaces, _, data_to_parse_no_whitespace = safe_parse(
                    ParseWhiteSpace, data_to_parse
                )

                if sucess_no_spaces:
                    data_to_parse = data_to_parse_no_whitespace

                if not data_to_parse:
                    break

                comma_success, _, data_to_parse = safe_parse_with_whitespace(
                    ParseComma, data_to_parse
                )

                # if there is something that is not a comma between last element and closing bracket eg [1,3 414]
                if not comma_success:
                    raise Exception("Failed to parse a list")

                # if ends with comma [2, ]
                if not data_to_parse:
                    raise Exception("Failed to parse a list")

            return result_from_tuple(True, result, remainder)
        return result_from_tuple(False)


class ParseKeyValuePair:
    def parse(self, string: str) -> Result:
        # key can only be a string
        child_success, key, data_to_parse = safe_parse_with_whitespace(
            ParseQuotes, string
        )

        if not child_success:
            raise Exception("Failed to parse a key-value pair")

        child_success, _, data_to_parse = safe_parse_with_whitespace(
            ParseColon, data_to_parse
        )
        if not child_success:
            raise Exception("Failed to parse a key-value pair")

        value, remainder = try_parsers(
            data_to_parse, [ParseQuotes, ParseNumber, ParseList, ParseDictionary]
        )

        result: tuple[str, Any] = (key, value)

        return result_from_tuple(True, result, remainder)


class ParseDictionary:
    def parse(self, string: str) -> Result:
        success, data_to_parse, remainder = safe_parse_with_whitespace(
            ParseCurlyBrackets, string
        )

        result: dict[str, Any] = {}

        if success:
            while data_to_parse:
                success, parsed, data_to_parse = safe_parse_with_whitespace(
                    ParseKeyValuePair, data_to_parse
                )
                key, value = parsed
                if key in result:
                    raise Exception("Failed to parse a dictionary")

                result[key] = value

                data_to_parse = get_rid_of_comma_and_whitespaces(data_to_parse)

            return result_from_tuple(True, result, remainder)

        return result_from_tuple(False)


class ParseJson:
    def parse(self, string: str) -> list[Any] | dict[Any, Any]:
        parsers: list[type[Parser]] = [ParseDictionary, ParseList]
        for parser in parsers:
            try:
                _, result, _ = parser().parse(string)

                if result is not None:
                    return result
            except Exception:
                pass

        raise Exception("Invalid JSON provided.")
