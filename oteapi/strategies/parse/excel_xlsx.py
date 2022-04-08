"""Strategy class for workbook/xlsx."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter
from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Iterable

    from openpyxl.worksheet.worksheet import Worksheet


class SessionUpdateXLSXParse(SessionUpdate):
    """Class for returning values from XLSXParse."""

    data: Dict[str, list] = Field(
        ...,
        description="A dict with column-name/column-value pairs. The values are lists.",
    )


class XLSXParseConfig(AttrDict):
    """Data model for retrieving a rectangular section of an Excel sheet."""

    worksheet: str = Field(..., description="Name of worksheet to load.")
    row_from: Optional[int] = Field(
        None,
        description="Excel row number of first row. Defaults to first assigned row.",
    )
    col_from: Optional[Union[int, str]] = Field(
        None,
        description=(
            "Excel column number or label of first column. Defaults to first assigned "
            "column."
        ),
    )
    row_to: Optional[int] = Field(
        None, description="Excel row number of last row. Defaults to last assigned row."
    )
    col_to: Optional[Union[int, str]] = Field(
        None,
        description=(
            "Excel column number or label of last column. Defaults to last assigned "
            "column."
        ),
    )
    header_row: Optional[int] = Field(
        None,
        description=(
            "Row number with the headers. Defaults to `1` if header is given, "
            "otherwise `None`."
        ),
    )
    header: Optional[List[str]] = Field(
        None,
        description=(
            "Optional list of column names, specifying the columns to return. "
            "These names they should match cells in `header_row`."
        ),
    )
    new_header: Optional[List[str]] = Field(
        None,
        description=(
            "Optional list of new column names replacing `header` in the output."
        ),
    )
    download_config: AttrDict = Field(
        AttrDict(),
        description="Configurations provided to a download strategy.",
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configurations for the data cache for retrieving the downloaded content.",
    )


class XLSXParseResourceConfig(ResourceConfig):
    """XLSX parse strategy resource config."""

    mediaType: str = Field(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        const=True,
        description=ResourceConfig.__fields__["mediaType"].field_info.description,
    )
    configuration: XLSXParseConfig = Field(
        ..., description="SQLite parse strategy-specific configuration."
    )


def set_model_defaults(model: XLSXParseConfig, worksheet: "Worksheet") -> None:
    """Update data model `model` with default values obtained from `worksheet`.

    Parameters:
        model: The parsed data model.
        worksheet: Excel worksheet, from which the default values will be obtained.

    """
    if model.row_from is None:
        if model.header:
            # assume that data starts on the first row after the header
            model.row_from = model.header_row + 1 if model.header_row else 1
        else:
            model.row_from = worksheet.min_row

    if model.row_to is None:
        model.row_to = worksheet.max_row

    if model.col_from is None:
        model.col_from = worksheet.min_column
    elif isinstance(model.col_from, str):
        model.col_from = column_index_from_string(model.col_from)

    if model.col_to is None:
        model.col_to = worksheet.max_column
    elif isinstance(model.col_to, str):
        model.col_to = column_index_from_string(model.col_to)

    if model.header and not model.header_row:
        model.header_row = 1


def get_column_indices(
    model: XLSXParseConfig, worksheet: "Worksheet"
) -> "Iterable[int]":
    """Helper function returning a list of column indices.

    Parameters:
        model: The parsed data model.
        worksheet: Excel worksheet, from which the header values will be retrieved.

    Returns:
        A list of column indices.

    """
    if not isinstance(model.col_from, int) or not isinstance(model.col_to, int):
        raise TypeError("Expected `model.col_from` and `model.col_to` to be integers.")

    if model.header:
        header_dict = {
            worksheet.cell(model.header_row, col).value: col
            for col in range(model.col_from, model.col_to + 1)
        }
        return [header_dict[h] for h in model.header]
    return range(model.col_from, model.col_to + 1)


@dataclass
class XLSXParseStrategy:
    """Parse strategy for Excel XLSX files.

    **Registers strategies**:

    - `("mediaType", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")`

    """

    parse_config: XLSXParseResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateXLSXParse:
        """Parses selected region of an excel file.

        Returns:
            A dict with column-name/column-value pairs. The values are lists.

        """

        cache = DataCache(self.parse_config.configuration.datacache_config)
        if session is None:
            raise ValueError("Missing session")
        with cache.getfile(key=session["key"], suffix=".xlsx") as filename:
            # Note that we have to set read_only=False to ensure that
            # load_workbook() properly closes the xlsx file after reading.
            # Otherwise Windows will fail when the temporary file is removed
            # when leaving the with statement.
            workbook = load_workbook(filename=filename, read_only=False, data_only=True)

        worksheet = workbook[self.parse_config.configuration.worksheet]
        set_model_defaults(self.parse_config.configuration, worksheet)
        columns = get_column_indices(self.parse_config.configuration, worksheet)

        data = []
        for row in worksheet.iter_rows(
            min_row=self.parse_config.configuration.row_from,
            max_row=self.parse_config.configuration.row_to,
            min_col=min(columns),
            max_col=max(columns),
        ):
            data.append([row[c - 1].value for c in columns])

        if self.parse_config.configuration.header_row:
            row = worksheet.iter_rows(
                min_row=self.parse_config.configuration.header_row,
                max_row=self.parse_config.configuration.header_row,
                min_col=min(columns),
                max_col=max(columns),
            ).__next__()
            header = [row[c - 1].value for c in columns]
        else:
            header = None

        if self.parse_config.configuration.new_header:
            nhead = len(header) if header else len(data[0]) if data else 0
            if len(self.parse_config.configuration.new_header) != nhead:
                raise TypeError(
                    f"length of `new_header` (={len(self.parse_config.configuration.new_header)}) "
                    f"doesn't match number of columns (={len(header) if header else 0})"
                )
            if header:
                for i, val in enumerate(self.parse_config.configuration.new_header):
                    if val is not None:
                        header[i] = val
            elif data:
                header = self.parse_config.configuration.new_header

        if header is None:
            header = [get_column_letter(col + 1) for col in range(len(data))]

        transposed = [list(datum) for datum in zip(*data)]
        return SessionUpdateXLSXParse(
            data={key: value for key, value in zip(header, transposed)}
        )
