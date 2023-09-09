import pytest

from parse_json import (
    ParseColon,
    ParseComma,
    ParseWhiteSpace,
    ParseCurlyBrackets,
    ParseDictionary,
    ParseJson,
    ParseKeyValuePair,
    ParseList,
    ParseMinus,
    ParseNumber,
    ParsePositiveNumber,
    ParseQuotes,
    ParseSquareBrackets,
    Result,
    result_from_tuple,
)


class TestQuotesParser:
    parser = ParseQuotes()

    def test_parse_correctly(self):
        assert self.parser.parse('"abc"') == result_from_tuple(True, "abc", "")
        assert self.parser.parse(r'"\"abc"') == result_from_tuple(True, r"\"abc", "")
        assert self.parser.parse(r'""') == result_from_tuple(True, "", "")
        assert self.parser.parse(r'"abc", "bcd"') == result_from_tuple(
            True, r"abc", r', "bcd"'
        )

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse('"ab')
        with pytest.raises(Exception):
            self.parser.parse('"')

    def test_parser_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)


class TestCurlyBracketsParser:
    parser = ParseCurlyBrackets()

    def test_parses_correctly(self):
        assert self.parser.parse("{}") == result_from_tuple(True, "", "")
        assert self.parser.parse('{"abc": 123}, {"def" : 354}') == result_from_tuple(
            True, '"abc": 123', ', {"def" : 354}'
        )

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse("{")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)


class TestSquareBracketsParser:
    parser = ParseSquareBrackets()

    def test_parses_correctly(self):
        assert self.parser.parse("[]") == result_from_tuple(True, "", "")
        assert self.parser.parse('["abc"], ["def"]') == result_from_tuple(
            True, '"abc"', ', ["def"]'
        )

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse("[")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)


class TestConseqSpacesParser:
    parser = ParseWhiteSpace()

    def test_parses_correctly(self):
        assert self.parser.parse("  ") == result_from_tuple(True, "", "")
        assert self.parser.parse("        abc") == result_from_tuple(True, "", "abc")
        assert self.parser.parse("        abc  ") == result_from_tuple(
            True, "", "abc  "
        )
        assert self.parser.parse("        abc") == result_from_tuple(True, "", "abc")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)


class TestPositiveNumberParser:
    parser = ParsePositiveNumber()

    def test_parses_correctly(self):
        assert self.parser.parse("1") == result_from_tuple(True, 1, "")
        assert self.parser.parse("123") == result_from_tuple(True, 123, "")
        assert self.parser.parse("0") == result_from_tuple(True, 0, "")
        assert self.parser.parse("56.05") == result_from_tuple(True, 56.05, "")
        assert self.parser.parse("123.45") == result_from_tuple(True, 123.45, "")
        assert self.parser.parse("123.45,56") == result_from_tuple(True, 123.45, ",56")
        assert self.parser.parse("123, 89") == result_from_tuple(True, 123, ", 89")

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse("13.")

        with pytest.raises(Exception):
            self.parser.parse("0.")
        with pytest.raises(Exception):
            self.parser.parse("0..1")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)
        assert self.parser.parse(r"{}") == result_from_tuple(False)
        assert self.parser.parse(r'"123"') == result_from_tuple(False)


class TestMinusParser:
    parser = ParseMinus()

    def test_parses_correctly(self):
        assert self.parser.parse("-") == result_from_tuple(True, "-", "")
        assert self.parser.parse("-20") == result_from_tuple(True, "-", "20")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)
        assert self.parser.parse(r"{}") == result_from_tuple(False)
        assert self.parser.parse(r'"123"') == result_from_tuple(False)


class TestNumberParser:
    parser = ParseNumber()

    def test_parses_correctly(self):
        assert self.parser.parse("1") == result_from_tuple(True, 1, "")
        assert self.parser.parse("123") == result_from_tuple(True, 123, "")
        assert self.parser.parse("0") == result_from_tuple(True, 0, "")
        assert self.parser.parse("56.05") == result_from_tuple(True, 56.05, "")
        assert self.parser.parse("123.45") == result_from_tuple(True, 123.45, "")
        assert self.parser.parse("123.45,56") == result_from_tuple(True, 123.45, ",56")
        assert self.parser.parse("123, 89") == result_from_tuple(True, 123, ", 89")
        assert self.parser.parse("-123") == result_from_tuple(True, -123, "")
        assert self.parser.parse("-123.05, ") == result_from_tuple(True, -123.05, ", ")
        assert self.parser.parse("0") == result_from_tuple(True, 0, "")

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse("13.")

        with pytest.raises(Exception):
            self.parser.parse("0.")
        with pytest.raises(Exception):
            self.parser.parse("0..1")

        with pytest.raises(Exception):
            self.parser.parse("-a")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)
        assert self.parser.parse(r"{}") == result_from_tuple(False)


class TestColonParser:
    parser = ParseColon()

    def test_parses_correctly(self):
        assert self.parser.parse(":") == result_from_tuple(True, ":", "")
        assert self.parser.parse(":56") == result_from_tuple(True, ":", "56")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)
        assert self.parser.parse(r"{}") == result_from_tuple(False)
        assert self.parser.parse(r'"123"') == result_from_tuple(False)


class TestCommaParser:
    parser = ParseComma()

    def test_parses_correctly(self):
        assert self.parser.parse(",") == result_from_tuple(True, ",", "")
        assert self.parser.parse(",56") == result_from_tuple(True, ",", "56")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)
        assert self.parser.parse(r"{}") == result_from_tuple(False)
        assert self.parser.parse(r'"123"') == result_from_tuple(False)


class TestListParser:
    parser = ParseList()

    def test_parses_correctly(self):
        assert self.parser.parse("[]") == result_from_tuple(True, [], "")
        assert self.parser.parse('["a", 1, 2]') == result_from_tuple(
            True, ["a", 1, 2], ""
        )
        assert self.parser.parse('[ "a" , 1 ,  2 ]') == result_from_tuple(
            True, ["a", 1, 2], ""
        )
        assert self.parser.parse('[ "a" , [1] ,  2 ]') == result_from_tuple(
            True, ["a", [1], 2], ""
        )
        assert self.parser.parse('[ "a" ,[[[1]]] ,  2 ]') == result_from_tuple(
            True, ["a", [[[1]]], 2], ""
        )
        assert self.parser.parse('[ "a" , 1 ,  2, "abc" ]') == result_from_tuple(
            True, ["a", 1, 2, "abc"], ""
        )
        assert self.parser.parse("[ [],[],[],[[[]]] ]") == result_from_tuple(
            True, [[], [], [], [[[]]]], ""
        )
        # TODO: add dictionary

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse("[[][]")

        with pytest.raises(Exception):
            self.parser.parse("[asdasd]")

        with pytest.raises(Exception):
            self.parser.parse("[1,2 abc]")

        with pytest.raises(Exception):
            self.parser.parse("[1,2,]")

    def test_did_not_find(self):
        assert self.parser.parse(r"a") == result_from_tuple(False)
        assert self.parser.parse(r"{}") == result_from_tuple(False)
        assert self.parser.parse(r'"123"') == result_from_tuple(False)


class TestKeyValuePairParser:
    parser = ParseKeyValuePair()

    def test_parses_correctly(self):
        assert self.parser.parse('"a": 1') == result_from_tuple(True, ("a", 1), "")
        assert self.parser.parse('"abc": "123"') == result_from_tuple(
            True, ("abc", "123"), ""
        )
        assert self.parser.parse('"a": [1,2,[3]]') == result_from_tuple(
            True, ("a", [1, 2, [3]]), ""
        )
        assert self.parser.parse('"a":{}') == result_from_tuple(True, ("a", {}), "")
        # TODO: add dictionary

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse('1: "abc"')

        with pytest.raises(Exception):
            self.parser.parse('"abc","def"')

        with pytest.raises(Exception):
            self.parser.parse('"abc":')


class TestDictionaryParser:
    parser = ParseDictionary()

    def test_parses_correctly(self):
        assert self.parser.parse("{}") == result_from_tuple(True, {}, "")
        assert self.parser.parse('{"a": 1}') == result_from_tuple(True, {"a": 1}, "")
        assert self.parser.parse('{"abc": "123", "bce": [123]}') == result_from_tuple(
            True, {"abc": "123", "bce": [123]}, ""
        )
        assert self.parser.parse('{"a": [1,2,[3]]}') == result_from_tuple(
            True, {"a": [1, 2, [3]]}, ""
        )
        assert self.parser.parse(
            '{"a": [1,2,[{"cdg": 123, "gasd": {}}]]}'
        ) == result_from_tuple(True, {"a": [1, 2, [{"cdg": 123, "gasd": {}}]]}, "")

    def test_throws_if_unclosed(self):
        with pytest.raises(Exception):
            self.parser.parse('{1: "abc"}')

        with pytest.raises(Exception):
            self.parser.parse('{"abc","def"}')

        with pytest.raises(Exception):
            self.parser.parse('{"abc":}')


class TestJsonParser:
    parser = ParseJson()

    def test_parses_correctly(self):
        assert self.parser.parse("{}") == {}

        # Taken from https://json.org/example.html
        assert (
            self.parser.parse(
                """{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}"""
            )
            == {
                "glossary": {
                    "title": "example glossary",
                    "GlossDiv": {
                        "title": "S",
                        "GlossList": {
                            "GlossEntry": {
                                "ID": "SGML",
                                "SortAs": "SGML",
                                "GlossTerm": "Standard Generalized Markup Language",
                                "Acronym": "SGML",
                                "Abbrev": "ISO 8879:1986",
                                "GlossDef": {
                                    "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                    "GlossSeeAlso": ["GML", "XML"],
                                },
                                "GlossSee": "markup",
                            }
                        },
                    },
                }
            }
        )
        # all of the following are taken from https://opensource.adobe.com/Spry/samples/data_region/JSONDataSetSample.html
        assert self.parser.parse("[ 100, 500, 300, 200, 400 ]") == [
            100,
            500,
            300,
            200,
            400,
        ]

        # Changed color and value to "color" and "value" because my implementation does not support unquoted strings
        assert (
            self.parser.parse(
                """[
	{
		"color": "red",
		"value": "#f00"
	},
	{
		"color": "green",
		"value": "#0f0"
	},
	{
		"color": "blue",
		"value": "#00f"
	},
	{
		"color": "cyan",
		"value": "#0ff"
	},
	{
		"color": "magenta",
		"value": "#f0f"
	},
	{
		"color": "yellow",
		"value": "#ff0"
	},
	{
		"color": "black",
		"value": "#000"
	}
]
"""
            )
            == [
                {"color": "red", "value": "#f00"},
                {"color": "green", "value": "#0f0"},
                {"color": "blue", "value": "#00f"},
                {"color": "cyan", "value": "#0ff"},
                {"color": "magenta", "value": "#f0f"},
                {"color": "yellow", "value": "#ff0"},
                {"color": "black", "value": "#000"},
            ]
        )

        assert (
            self.parser.parse(
                """{
	"id": "0001",
	"type": "donut",
	"name": "Cake",
	"ppu": 0.55,
	"batters":
		{
			"batter":
				[
					{ "id": "1001", "type": "Regular" },
					{ "id": "1002", "type": "Chocolate" },
					{ "id": "1003", "type": "Blueberry" },
					{ "id": "1004", "type": "Devil's Food" }
				]
		},
	"topping":
		[
			{ "id": "5001", "type": "None" },
			{ "id": "5002", "type": "Glazed" },
			{ "id": "5005", "type": "Sugar" },
			{ "id": "5007", "type": "Powdered Sugar" },
			{ "id": "5006", "type": "Chocolate with Sprinkles" },
			{ "id": "5003", "type": "Chocolate" },
			{ "id": "5004", "type": "Maple" }
		]
}"""
            )
            == {
                "id": "0001",
                "type": "donut",
                "name": "Cake",
                "ppu": 0.55,
                "batters": {
                    "batter": [
                        {"id": "1001", "type": "Regular"},
                        {"id": "1002", "type": "Chocolate"},
                        {"id": "1003", "type": "Blueberry"},
                        {"id": "1004", "type": "Devil's Food"},
                    ]
                },
                "topping": [
                    {"id": "5001", "type": "None"},
                    {"id": "5002", "type": "Glazed"},
                    {"id": "5005", "type": "Sugar"},
                    {"id": "5007", "type": "Powdered Sugar"},
                    {"id": "5006", "type": "Chocolate with Sprinkles"},
                    {"id": "5003", "type": "Chocolate"},
                    {"id": "5004", "type": "Maple"},
                ],
            }
        )

        assert (
            self.parser.parse(
                """[
	{
		"id": "0001",
		"type": "donut",
		"name": "Cake",
		"ppu": 0.55,
		"batters":
			{
				"batter":
					[
						{ "id": "1001", "type": "Regular" },
						{ "id": "1002", "type": "Chocolate" },
						{ "id": "1003", "type": "Blueberry" },
						{ "id": "1004", "type": "Devil's Food" }
					]
			},
		"topping":
			[
				{ "id": "5001", "type": "None" },
				{ "id": "5002", "type": "Glazed" },
				{ "id": "5005", "type": "Sugar" },
				{ "id": "5007", "type": "Powdered Sugar" },
				{ "id": "5006", "type": "Chocolate with Sprinkles" },
				{ "id": "5003", "type": "Chocolate" },
				{ "id": "5004", "type": "Maple" }
			]
	},
	{
		"id": "0002",
		"type": "donut",
		"name": "Raised",
		"ppu": 0.55,
		"batters":
			{
				"batter":
					[
						{ "id": "1001", "type": "Regular" }
					]
			},
		"topping":
			[
				{ "id": "5001", "type": "None" },
				{ "id": "5002", "type": "Glazed" },
				{ "id": "5005", "type": "Sugar" },
				{ "id": "5003", "type": "Chocolate" },
				{ "id": "5004", "type": "Maple" }
			]
	},
	{
		"id": "0003",
		"type": "donut",
		"name": "Old Fashioned",
		"ppu": 0.55,
		"batters":
			{
				"batter":
					[
						{ "id": "1001", "type": "Regular" },
						{ "id": "1002", "type": "Chocolate" }
					]
			},
		"topping":
			[
				{ "id": "5001", "type": "None" },
				{ "id": "5002", "type": "Glazed" },
				{ "id": "5003", "type": "Chocolate" },
				{ "id": "5004", "type": "Maple" }
			]
	}
]"""
            )
            == [
                {
                    "id": "0001",
                    "type": "donut",
                    "name": "Cake",
                    "ppu": 0.55,
                    "batters": {
                        "batter": [
                            {"id": "1001", "type": "Regular"},
                            {"id": "1002", "type": "Chocolate"},
                            {"id": "1003", "type": "Blueberry"},
                            {"id": "1004", "type": "Devil's Food"},
                        ]
                    },
                    "topping": [
                        {"id": "5001", "type": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5005", "type": "Sugar"},
                        {"id": "5007", "type": "Powdered Sugar"},
                        {"id": "5006", "type": "Chocolate with Sprinkles"},
                        {"id": "5003", "type": "Chocolate"},
                        {"id": "5004", "type": "Maple"},
                    ],
                },
                {
                    "id": "0002",
                    "type": "donut",
                    "name": "Raised",
                    "ppu": 0.55,
                    "batters": {"batter": [{"id": "1001", "type": "Regular"}]},
                    "topping": [
                        {"id": "5001", "type": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5005", "type": "Sugar"},
                        {"id": "5003", "type": "Chocolate"},
                        {"id": "5004", "type": "Maple"},
                    ],
                },
                {
                    "id": "0003",
                    "type": "donut",
                    "name": "Old Fashioned",
                    "ppu": 0.55,
                    "batters": {
                        "batter": [
                            {"id": "1001", "type": "Regular"},
                            {"id": "1002", "type": "Chocolate"},
                        ]
                    },
                    "topping": [
                        {"id": "5001", "type": "None"},
                        {"id": "5002", "type": "Glazed"},
                        {"id": "5003", "type": "Chocolate"},
                        {"id": "5004", "type": "Maple"},
                    ],
                },
            ]
        )

        assert (
            self.parser.parse(
                """{
	"id": "0001",
	"type": "donut",
	"name": "Cake",
	"image":
		{
			"url": "images/0001.jpg",
			"width": 200,
			"height": 200
		},
	"thumbnail":
		{
			"url": "images/thumbnails/0001.jpg",
			"width": 32,
			"height": 32
		}
}"""
            )
            == {
                "id": "0001",
                "type": "donut",
                "name": "Cake",
                "image": {"url": "images/0001.jpg", "width": 200, "height": 200},
                "thumbnail": {
                    "url": "images/thumbnails/0001.jpg",
                    "width": 32,
                    "height": 32,
                },
            }
        )

        assert self.parser.parse(
            '{"abc":"d}[[{}{{{}}}}}}}}{}{[][][][[[][][][][][][][][[[[[[[]]][][][][]]]]]]]}"}'
        ) == {
            "abc": "d}[[{}{{{}}}}}}}}{}{[][][][[[][][][][][][][][[[[[[[]]][][][][]]]]]]]}"
        }
        assert self.parser.parse('["[","{]"]') == ["[", "{]"]
        assert self.parser.parse('["[[["]') == ["[[["]
        assert self.parser.parse('["{{{"]') == ["{{{"]
        assert self.parser.parse(r'["\"{{{"]') == [r"\"{{{"]
