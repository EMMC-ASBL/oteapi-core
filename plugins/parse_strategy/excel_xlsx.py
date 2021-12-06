# pylint: disable=W0613
""" Strategy class for workbook/xlsx """

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


class XLSXParseDataModel(BaseModel):
    worksheet: str
    row_from: int = 1
    col_from: int = 1
    row_to: int = None
    col_to: int = None
    header_positions: List = []


def fetch_headers(model_object: XLSXParseDataModel, worksheet: Worksheet) -> List[str]:
    """
    Helper function returning the headers of the worksheet as a list of strings.
    """
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
        self.localpath = "/ote-data"
        self.filename = self.resource_config.downloadUrl.path.rsplit("/", 1)[-1]
        if self.resource_config.configuration:
            self.config = self.resource_config.configuration
        else:
            self.config = {}

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        xlsx_parse_data = XLSXParseDataModel(**self.config)
        filename = f"{self.localpath}/{self.filename}"
        workbook = load_workbook(filename=filename, read_only=True, data_only=True)
        worksheet = workbook[xlsx_parse_data.worksheet]

        headers = fetch_headers(xlsx_parse_data, worksheet)
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
