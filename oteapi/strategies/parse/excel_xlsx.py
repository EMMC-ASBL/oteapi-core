"""Strategy class for workbook/xlsx."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Union

from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter
from pydantic import BaseModel, Extra, Field

from oteapi.datacache import DataCache
from oteapi.plugins import create_strategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Iterable

    from openpyxl.worksheet.worksheet import Worksheet

    from oteapi.models import ResourceConfig


class XLSXParseDataModel(BaseModel):
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


def set_model_defaults(model: XLSXParseDataModel, worksheet: "Worksheet") -> None:
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
    model: XLSXParseDataModel, worksheet: "Worksheet"
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

    parse_config: "ResourceConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Parses selected region of an excel file.

        Returns:
            A dict with column-name/column-value pairs. The values are lists.

        """
        model = XLSXParseDataModel(
            **self.parse_config.configuration, extra=Extra.ignore
        )

        downloader = create_strategy("download", self.parse_config)
        output = downloader.get()
        cache = DataCache(self.parse_config.configuration)
        with cache.getfile(key=output["key"], suffix=".xlsx") as filename:
            workbook = load_workbook(filename=filename, read_only=True, data_only=True)
        worksheet = workbook[model.worksheet]
        set_model_defaults(model, worksheet)
        columns = get_column_indices(model, worksheet)

        data = []
        for row in worksheet.iter_rows(
            min_row=model.row_from,
            max_row=model.row_to,
            min_col=min(columns),
            max_col=max(columns),
        ):
            data.append([row[c - 1].value for c in columns])

        if model.header_row:
            row = worksheet.iter_rows(
                min_row=model.header_row,
                max_row=model.header_row,
                min_col=min(columns),
                max_col=max(columns),
            ).__next__()
            header = [row[c - 1].value for c in columns]
        else:
            header = None

        if model.new_header:
            nhead = len(header) if header else len(data[0]) if data else 0
            if len(model.new_header) != nhead:
                raise TypeError(
                    f"length of `new_header` (={len(model.new_header)}) "
                    f"doesn't match number of columns (={len(header) if header else 0})"
                )
            if header:
                for i, val in enumerate(model.new_header):
                    if val is not None:
                        header[i] = val
            elif data:
                header = model.new_header

        if header is None:
            header = [get_column_letter(col + 1) for col in range(len(data))]

        transposed = list(map(list, zip(*data)))
        return {k: v for k, v in zip(header, transposed)}
