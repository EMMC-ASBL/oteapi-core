"""Strategy class for text/csv."""

import csv
from collections import defaultdict
from collections.abc import Hashable
from enum import Enum
from typing import Any, Literal, Optional, Type, Union

from pydantic import BaseModel, Field, field_validator
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig
from oteapi.plugins import create_strategy


class QuoteConstants(str, Enum):
    """CSV module `QUOTE_*` constants."""

    QUOTE_ALL = "QUOTE_ALL"
    QUOTE_MINIMAL = "QUOTE_MINIMAL"
    QUOTE_NONUMERIC = "QUOTE_NONNUMERIC"
    QUOTE_NONE = "QUOTE_NONE"

    def csv_constant(self) -> int:
        """Return the CSV lib equivalent constant."""
        return {
            self.QUOTE_ALL: csv.QUOTE_ALL,
            self.QUOTE_MINIMAL: csv.QUOTE_MINIMAL,
            self.QUOTE_NONUMERIC: csv.QUOTE_NONNUMERIC,
            self.QUOTE_NONE: csv.QUOTE_NONE,
        }[self]


# mypy is unable to recognize a DictComprehension for the 2nd arg.
CSVDialect: Type[Enum] = Enum(  # type: ignore[misc]
    value="CSVDialect",
    names={dialect.upper(): dialect for dialect in csv.list_dialects()},
    module=__name__,
    type=str,
)
"""CSV dialects.

All available dialects are retrieved through the `csv.list_dialects()` function,
and will thus depend on the currently loaded and used Python interpreter.
"""


class DialectFormatting(BaseModel):
    """Dialect and formatting parameters for CSV.

    See [the Python docs](https://docs.python.org/3/library/csv.html#csv-fmt-params)
    for more information.

    Note:
        As `Dialect.lineterminator` is hardcoded in `csv.reader`, it is left out of
        this model.

    """

    base: Optional[CSVDialect] = Field(
        None,
        description=(
            "A specific CSV dialect, e.g., 'excel'. Any other parameters here will "
            "overwrite the preset dialect parameters for the specified dialect."
        ),
    )
    delimiter: Optional[str] = Field(
        None,
        description=(
            "A one-character string used to separate fields. "
            "See [the Python docs entry](https://docs.python.org/3/library/csv.html"
            "#csv.Dialect.delimiter) for more information."
        ),
        min_length=1,
        max_length=1,
    )
    doublequote: Optional[bool] = Field(
        None,
        description=(
            "Controls how instances of [`quotechar`]"
            "[oteapi.strategies.parse.text_csv.DialectFormatting.quotechar] "
            "appearing inside a field should themselves be quoted. When `True`, the "
            "character is doubled. When `False`, the [`escapechar`]"
            "[oteapi.strategies.parse.text_csv.DialectFormatting.escapechar] "
            "is used as a prefix to the [`quotechar`]"
            "[oteapi.strategies.parse.text_csv.DialectFormatting.quotechar]. "
            "See [the Python docs entry]"
            "(https://docs.python.org/3/library/csv.html#csv.Dialect.doublequote) "
            "for more information."
        ),
    )
    escapechar: Optional[str] = Field(
        None,
        description=(
            "A one-character string used by the writer to escape the [`delimiter`]"
            "[oteapi.strategies.parse.text_csv.DialectFormatting.delimiter] if "
            "[`quoting`][oteapi.strategies.parse.text_csv.DialectFormatting.quoting] "
            "is set to [`QUOTE_NONE`]"
            "[oteapi.strategies.parse.text_csv.QuoteConstants.QUOTE_NONE] and the "
            "[`quotechar`][oteapi.strategies.parse.text_csv.DialectFormatting."
            "quotechar] if [`doublequote`][oteapi.strategies.parse.text_csv."
            "DialectFormatting.doublequote] is `False`. On reading, the "
            "[`escapechar`][oteapi.strategies.parse.text_csv.DialectFormatting."
            "escapechar] removes any special meaning from the following character. "
            "See [the Python docs entry]"
            "(https://docs.python.org/3/library/csv.html#csv.Dialect.escapechar) "
            "for more information."
        ),
        min_length=1,
        max_length=1,
    )
    quotechar: Optional[str] = Field(
        None,
        description=(
            "A one-character string used to quote fields containing special "
            "characters, such as the [`delimiter`]"
            "[oteapi.strategies.parse.text_csv.DialectFormatting.delimiter] or "
            "[`quotechar`][oteapi.strategies.parse.text_csv.DialectFormatting."
            "quotechar], or which contain new-line characters. See "
            "[the Python docs entry](https://docs.python.org/3/library/csv.html"
            "#csv.Dialect.quotechar) for more information."
        ),
        min_length=1,
        max_length=1,
    )
    quoting: Optional[QuoteConstants] = Field(
        None,
        description=(
            "Controls when quotes should be generated by the writer and recognised by "
            "the reader. It can take on any of the `QUOTE_*` constants (see section "
            "[Module Contents](https://docs.python.org/3/library/csv.html"
            "#csv-contents)). See [the Python docs entry]"
            "(https://docs.python.org/3/library/csv.html#csv.Dialect.quoting) "
            "for more information."
        ),
    )
    skipinitialspace: Optional[bool] = Field(
        None,
        description=(
            "When `True`, whitespace immediately following the [`delimiter`]"
            "[oteapi.strategies.parse.text_csv.DialectFormatting.delimiter] is "
            "ignored. See [the Python docs entry]"
            "(https://docs.python.org/3/library/csv.html#csv.Dialect.skipinitialspace)"
            " for more information."
        ),
    )
    strict: Optional[bool] = Field(
        None,
        description=(
            "When `True`, raise exception [Error]"
            "(https://docs.python.org/3/library/csv.html#csv.Error) on bad CSV input. "
            "See [the Python docs entry](https://docs.python.org/3/library/csv.html"
            "#csv.Dialect.strict) for more information."
        ),
    )

    @field_validator("base")
    @classmethod
    def validate_dialect_base(cls, value: str) -> str:
        """Ensure the given `base` dialect is registered locally."""
        if value not in csv.list_dialects():
            raise ValueError(
                f"{value!r} is not a known registered CSV dialect. "
                f"Registered dialects: {', '.join(csv.list_dialects())}."
            )
        return value


class ReaderConfig(BaseModel):
    """CSV DictReader configuration parameters.

    See [the Python docs](https://docs.python.org/3/library/csv.html#csv.DictReader)
    for more information.
    """

    fieldnames: Optional[list[str]] = Field(
        None,
        description=(
            "List of headers. If not set, the values in the first row of the CSV file "
            "will be used as the field names."
        ),
    )
    restkey: Optional[Hashable] = Field(
        None,
        description=(
            "If a row has more fields than [`fieldnames`]"
            "[oteapi.strategies.parse.text_csv.ReaderConfig.fieldnames], the "
            "remaining data is put in a list and stored with the field name specified "
            "by [`restkey`][oteapi.strategies.parse.text_csv.ReaderConfig.restkey]."
        ),
    )
    restval: Optional[Any] = Field(
        None,
        description=(
            "If a non-blank row has fewer fields than the length of [`fieldnames`]"
            "[oteapi.strategies.parse.text_csv.ReaderConfig.fieldnames], the missing "
            "values are filled-in with the value of [`restval`]"
            "[oteapi.strategies.parse.text_csv.ReaderConfig.restval]."
        ),
    )
    encoding: str = Field(
        "utf8",
        description="The file encoding.",
    )


class CSVConfig(AttrDict):
    """CSV parse-specific Configuration Data Model."""

    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description=(
            "Configurations for the data cache for storing the downloaded file "
            "content."
        ),
    )
    dialect: DialectFormatting = Field(
        DialectFormatting(),
        description=(
            "Dialect and formatting parameters. See [the Python docs]"
            "(https://docs.python.org/3/library/csv.html#csv-fmt-params) for more "
            "information."
        ),
    )
    reader: ReaderConfig = Field(
        ReaderConfig(),
        description=(
            "CSV DictReader configuration parameters. See [the Python docs]"
            "(https://docs.python.org/3/library/csv.html#csv.DictReader) for more "
            "information."
        ),
    )


class CSVResourceConfig(ResourceConfig):
    """CSV parse strategy filter config."""

    mediaType: Literal["text/csv"] = Field(
        "text/csv",
        description=ResourceConfig.model_fields["mediaType"].description,
    )
    configuration: CSVConfig = Field(
        CSVConfig(), description="CSV parse strategy-specific configuration."
    )


class AttrDictCSVParse(AttrDict):
    """Class for returning values from CSV Parse."""

    content: dict[Union[str, None], list[Any]] = Field(
        ..., description="Content of the CSV document."
    )


@dataclass
class CSVParseStrategy:
    """Parse strategy for CSV files.

    **Registers strategies**:

    - `("mediaType", "text/csv")`

    """

    parse_config: CSVResourceConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDictCSVParse:
        """Parse CSV."""
        downloader = create_strategy("download", self.parse_config)
        output = downloader.get()
        cache = DataCache(self.parse_config.configuration.datacache_config)

        with cache.getfile(output["key"]) as csvfile_path:
            kwargs = self.parse_config.configuration.dialect.model_dump(
                exclude={"base", "quoting"}, exclude_unset=True
            )

            dialect = self.parse_config.configuration.dialect.base
            if dialect:
                kwargs["dialect"] = dialect.value
            quoting = self.parse_config.configuration.dialect.quoting
            if quoting:
                kwargs["quoting"] = quoting.csv_constant()

            kwargs.update(
                self.parse_config.configuration.reader.model_dump(exclude_unset=True)
            )

            with open(
                csvfile_path,
                newline="",
                encoding=self.parse_config.configuration.reader.encoding,
            ) as csvfile:
                csvreader = csv.DictReader(csvfile, **kwargs)
                content: dict[Union[str, None], list[Any]] = defaultdict(list)
                for row in csvreader:
                    for field, value in row.items():
                        if (
                            csvreader.reader.dialect.quoting == csv.QUOTE_NONNUMERIC
                            and isinstance(value, float)
                            and value.is_integer()
                        ):
                            value = int(value)
                        content[field].append(value)
            for key in list(content):
                if any(isinstance(value, float) for value in content[key]):
                    content[key] = [
                        (
                            float(value)
                            if (value or value == 0.0 or value == 0)
                            and value != csvreader.restval
                            else float("nan")
                        )
                        for value in content[key]
                    ]
                    continue
                if any(isinstance(value, int) for value in content[key]):
                    content[key] = [
                        (
                            int(value)
                            if (value or value == 0) and value != csvreader.restval
                            else csvreader.restval
                        )
                        for value in content[key]
                    ]

            return AttrDictCSVParse(content=content)
