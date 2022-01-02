import requests
from requests import RequestException

class SIEBanxico():
    """
    A python class for the Economic Information System (SIE) API of Banco de México.

    Args:
        token (str): A query token from Banco de México
        id_series (list): A list with the economic series id or with the series id range to query.  ** A list must be given even though only one serie is consulted.
        language (str): Language of the obtained information. 'en' (default) for english or 'es' for spanish

    Attributes:
        token (str): Current query token
        series (str): Current series id

    Methods:
        set_token: Change the current query token
        set_id_series: Allows to change the series to query
        append_id_series: Allows to update the series to query
        get_metadata: Allows to consult metadata of the series
        get_lastdata: Returns the most recent published data
        get_timeseries: Allows to consult time series data
        get_timeseries_range: Returns the data for the period defined

    Notes: 
        (1) In order to retrive information from the SIE API, a query token is required. The token can be requested at https://www.banxico.org.mx/SieAPIRest/service/v1/token?locale=en

        (2) Each economic serie is related to an unique ID. The full series catalogue can be consulted at https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries?locale=en

        (3) The full API documentation can be consulted at https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en

    Disclaimer:
        This module was developed as a personal contribution project to the data community, with the sole objective of facilitating access to the information provided by Banco de México through its public API.

    """
    def __init__(self, token: str, id_series: list , language: str = 'en') -> None:
        """Instantiate a SIEBanxico API object.

        Args:
            token (str): A query token from Banco de México
            id_series (list): A list with the economic series id or with the series id range to query.  ** A list must be given even though only one serie is consulted.
            language (str): Language of the obtained information. 'en' (default) for english or 'es' for spanish.
        """
        self.token = None
        self.set_token(token = token)
        self.series = None
        self.set_id_series(id_series = id_series)
        self.__url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
        self.__headers = {'Bmx-Token': self.token}
        self.__params = {}
        self.__language = language
        self.__set_language()        

    def set_token(self, token: str) -> None:
        """Change the current query token.

        Args:
            token (str): A query token from Banco de México

        Returns:
            None
        """
        if type(token) != str:
            raise TypeError('"token" must be a string.')
        
        self.token = token

    def set_id_series(self, id_series: list) -> None:
        """Allows to change the series to query.
        Note: This method replaces the current series. To add new series to the query, use the "append_id_series" method instead.

        Args:
            id_series (list): A list with the economic series id or with the series id range to query.  ** A list must be given even though only one serie is consulted.

        Returns:
            None
        """
        if not isinstance(id_series, (list, str)):
            raise TypeError('"id_series" must be a list with strings or a single string.')
        elif isinstance(id_series, list):
            self.series = ','.join(id_series)
        else:
            self.series = id_series

    def append_id_series(self, id_series: list) -> None:
        """Allows to update the series to query.
        Note: New series ranges are not allowed (e.g. 'SF311408-SF311410'); use the "set_id_series" method instead.

        Args:
            id_series (list):  A list with the economic series id to append as strings. ** A list must be given even though only one serie is appended.
        
        Returns:
            None
        """
        if not isinstance(id_series, list):
            raise TypeError('"id_series" must be a list with strings.')
        self.series += ',' + ','.join(id_series)
    

    def get_metadata(self) -> dict:
        """Allows to consult metadata of the series.

        Returns:
            dict: json response format
        """
        self.__set_pct_change(pct_change = None)
        url_metadata = self.__url + self.series
        response = requests.get(url_metadata, headers = self.__headers, params = self.__params)
        if response.status_code != 200:
            raise RequestException(f'Something go wrong with the request. Review the token or series id.\nStatus code: {response.status_code}')
        return response.json()

    def get_lastdata(self, pct_change: str = None) -> dict:
        """Returns the most recent published data for the requested series.

        Args:
            pct_change (str, optional): None (default) for levels, "PorcObsAnt" for change rate compared to the previous observation, "PorcAnual" for anual change rate, "PorcAcumAnual" for annual acummulated change rate.

        Returns:
            dict: json response format
        """
        self.__set_pct_change(pct_change = pct_change)
        url_lastdata = self.__url + self.series + '/datos/oportuno'
        response = requests.get(url_lastdata, headers = self.__headers, params = self.__params)
        if response.status_code != 200:
            raise RequestException(f'Something go wrong with the request. Review the token or series id.\nStatus code: {response.status_code}')
        return response.json()

    def get_timeseries(self, pct_change:str = None) -> dict:
        """Allows to consult the whole time series data, corresponding to the period defined between the initial date and the final date in the metadata.

        Args:
            pct_change (str, optional): None (default) for levels, "PorcObsAnt" for change rate compared to the previous observation, "PorcAnual" for anual change rate, "PorcAcumAnual" for annual acummulated change rate.

        Returns:
            dict: json response format
        """
        self.__set_pct_change(pct_change = pct_change)
        url_timeseries = self.__url + self.series + '/datos'
        response = requests.get(url_timeseries, headers = self.__headers, params = self.__params)
        if response.status_code != 200:
            raise RequestException(f'Something go wrong with the request. Review the token or series id.\nStatus code: {response.status_code}')
        return response.json()
    
    def get_timeseries_range(self, init_date: str, end_date: str, pct_change:str = None) -> dict:
        """Returns the data of the requested series, for the defined period.

        Args:
            init_date (str): The date on which the period of obtained data starts. The date must be sent in the format yyyy-mm-dd. If the given date is out of the metadata time range, the oldest value is returned.
            end_date (str): The date on which the period of obtained data concludes. The date must be sent in the format yyyy-mm-dd. If the given date is out of the metadata time range, the most recent value is returned.
            pct_change (str, optional): None (default) for levels, "PorcObsAnt" for change rate compared to the previous observation, "PorcAnual" for anual change rate, "PorcAcumAnual" for annual acummulated change rate.
        
        Returns:
            dict: json response format
        """
        self.__set_pct_change(pct_change = pct_change)
        if (type(init_date) != str) or (type(end_date) != str):
            raise TypeError('"init_date" and "end_date" must be a string in the format yyyy-mm-dd')
        url_timeseries_range = self.__url + self.series + '/datos/' + init_date + '/' + end_date
        response = requests.get(url_timeseries_range, headers = self.__headers, params = self.__params )
        if response.status_code != 200:
            raise RequestException(f'Something go wrong with the request. Review the token, series id or date format.\nStatus code: {response.status_code}')
        return response.json()

    def __set_language(self) -> None:
        """Set language parameter for the request.
        ** Not callable.
        """
        if type(self.__language) != str:
            raise TypeError('"language" must be a string.')
        elif (self.__language == 'en') or (self.__language == 'es'):
            self.__params['locale'] = self.__language
        else:
            raise ValueError(f'"{self.__language}" is not defined.\nTry "en" for english or "es" for spanish.')
    
    def __set_pct_change(self, pct_change: str) -> None:
        """Set change parameter for the request.
        ** Not callable.
        """
        if (pct_change != None) and (type(pct_change) != str):
            raise TypeError('"pct_change" must be None or a string.')
        elif pct_change not in [None, 'PorcObsAnt', 'PorcAnual', 'PorcAcumAnual']:
            raise ValueError(f'"{pct_change}" is not defined.\nTry None for levels, "PorcObsAnt" for change rate compared to the previous observation, "PorcAnual" for anual change rate, "PorcAcumAnual" for annual acummulated change rate.')
        else:
            self.__params['incremento'] = pct_change