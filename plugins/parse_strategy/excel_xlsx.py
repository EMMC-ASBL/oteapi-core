# pylint: disable=W0613
""" Strategy class for workbook/xlsx """
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel, DirectoryPath

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


class XLSXParseDataModel(BaseModel):
    worksheet: str
    row_from: int = None
    col_from: int = None
    row_to: int = None
    col_to: int = None
    header_positions: List = []
    downloadDir: DirectoryPath = (  # move to ResourceConfig??
        os.environ["OTEAPI_downloadDir"] if "OTEAPI_downloadDir" in os.environ else "."
    )


def fetch_headers(model_object: XLSXParseDataModel, worksheet: Worksheet) -> List[str]:
    """
    Helper function returning the headers of the worksheet as a list of strings.
    If the list of headers is empty we assume the first row contains the headers
    """
    if len(model_object.header_positions) == 0:
        return [
            worksheet.cell(worksheet.min_row, col).value
            for col in range(worksheet.min_column, worksheet.max_column + 1)
        ]
    else:
        uppercase_codes = []
        for code in model_object.header_positions:
            uppercase_codes.append(code.upper())

        uppercase_codes.sort()
        return [worksheet[code].value for code in uppercase_codes]


@dataclass
@StrategyFactory.register(
    ("mediaType", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
)
class XLSXParseStrategy:

    resource_config: ResourceConfig

    def __post_init__(self):
        if self.resource_config.downloadUrl.scheme == "file":
            # Workaround for strange behaviour (bug?) in "file" scheme for AnyUrl
            self.path = Path(self.resource_config.downloadUrl.host)
        else:
            self.path = Path(self.resource_config.downloadUrl.path)

        if self.resource_config.configuration:
            self.config = self.resource_config.configuration
        else:
            self.config = {}

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        xlsx_parse_data = XLSXParseDataModel(**self.config)
        filename = Path(xlsx_parse_data.downloadDir) / self.path.name
        workbook = load_workbook(filename=filename, read_only=True, data_only=True)
        worksheet = workbook[xlsx_parse_data.worksheet]

        headers = fetch_headers(xlsx_parse_data, worksheet)
        if xlsx_parse_data.row_from is None:
            xlsx_parse_data.row_from = (
                worksheet.min_row + 1
            )  # We assume first row is headers
        if xlsx_parse_data.row_to is None:
            xlsx_parse_data.row_to = worksheet.max_row
        if xlsx_parse_data.col_from is None:
            xlsx_parse_data.col_from = worksheet.min_column
        if xlsx_parse_data.col_to is None:
            xlsx_parse_data.col_to = worksheet.max_column
        json_data = {}
        for row in worksheet.iter_rows(
            min_row=xlsx_parse_data.row_from,
            min_col=xlsx_parse_data.col_from,
            max_row=xlsx_parse_data.row_to
            if xlsx_parse_data.row_to
            else worksheet.max_row,
            max_col=xlsx_parse_data.col_to
            if xlsx_parse_data.col_to
            else worksheet.max_column,
        ):

            doc = {}
            data = []
            for cell in row:
                data.append(cell.value)

            if data[0] == None or data[-1] == None:
                continue

            for idx in range(1 + xlsx_parse_data.col_to - xlsx_parse_data.col_from):
                doc[headers[idx]] = data[idx]

            current_row = row[0].row
            json_data["Row " + str(current_row)] = doc

        return json_data

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return {}
