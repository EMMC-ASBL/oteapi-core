from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlparse
from uuid import uuid4
import tempfile
import pandas as pd
import requests
import pysftp

cache='/app/data'

class DownloadStrategy(ABC):
    """
    """
    @abstractmethod
    def read(self, uri: str):
        pass

    
class ParseStrategy(ABC):
    """
    """
    @abstractmethod
    def read(self, uri: str):
        pass

class GenerateDataModelStrategy(ABC):
    """
    """
    @abstractmethod
    def generate(self, uri: str):
        pass

    
class SFTPStrategy(DownloadStrategy):
    def read(self, uri : str):
        o = urlparse(uri)

        # Download via sftp
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(host=o.hostname, username=o.username, password=o.password, cnopts=cnopts) as sftp:    
            sftp.cwd('/upload')
            sftp.get(o.path, f'{cache}/file.csv')

class HTTPStrategy(DownloadStrategy):
    def read(self, uri: str):
        o = urlparse(uri)
        
        # Download via http
        r = requests.get(uri, allow_redirects=True)    
        open (f'{cache}/file.csv', 'wb').write(r.content)
        return f'{cache}/file.csv'
        
class CSVParseStrategy(ParseStrategy):
    def read(self, file: str):
        df = pd.read_csv(file)
        # Move stuff into dataspace
        return df
    
class GenerateDataModelStrategyFromCSV(GenerateDataModelStrategy):
    def generate(self, file: str):
        df = pd.read_csv(file)
        entity = {    
            "uri": f"com.sintef.soft/ontology/v1/generated_from_csv{str(uuid4()).replace('-','_')}",
            "dimensions": {"nrows":"Number of elements"},
            "properties": {}
        }    
        for col in df.columns:                
            entity['properties'][str(col)] = {
                'type': str(df[col].dtype),
                'label': str(col),
                'description': '',
                'unit': '',
                'shape': ['nrows']}
            
        return entity

    
download_strategy = {
    'sftp': SFTPStrategy,
    'http': HTTPStrategy,
    'https': HTTPStrategy
}

parser_strategy = {
    'text/csv': CSVParseStrategy
}

model_generation_strategy = {
    'text/csv': GenerateDataModelStrategyFromCSV
}

class DataSourceContext():
    def __init__(self, uri: str, mediaType: str) -> None:
        self._uri = uri
        self._mediaType = mediaType
        self._dlstrategy = None
        self._parsestrategy = None
        self._modelgenstrategy = None
        
        o = urlparse(uri)
        if o.scheme in download_strategy:
            self._dlstrategy = download_strategy[o.scheme]()
        
        if mediaType in parser_strategy:
            self._parsestrategy = parser_strategy[mediaType]()

        if mediaType in model_generation_strategy:
            self._modelgenstrategy = model_generation_strategy[mediaType]()

    @property
    def strategy(self) -> DownloadStrategy:
        return self._dlstrategy

    @strategy.setter
    def strategy(self, strategy: DownloadStrategy) -> None:
        self._dlstrategy = strategy

    def read(self) -> None:
        file = self._dlstrategy.read(self._uri)
        return self._parsestrategy.read(file)

    def datamodel(self) -> None:
        file = self._dlstrategy.read(self._uri)
        return self._modelgenstrategy.generate(file)
        
    