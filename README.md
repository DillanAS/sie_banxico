# sie_banxico #

[![PyPi Version](https://img.shields.io/badge/Pypi-0.0.1-blue)](https://pypi.org/project/sie-banxico/)

A python class for the Economic Information System (SIE) [API of Banco de México](https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en).

Args:
    token (str): A query token from Banco de México
    id_series (list): A list with the economic series id or with the series id range to query.  ** A list must be given even though only one serie is consulted.
    language (str): Language of the obtained information. 'en' (default) for english or 'es' for spanish

Notes: 
    (1) In order to retrive information from the SIE API, a query token is required. The token can be requested [here](https://www.banxico.org.mx/SieAPIRest/service/v1/token)
    (2) Each economic serie is related to an unique ID. The full series catalogue can be consulted [here](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries) 

## Pypi Installation ##

```python
pip install sie_banxico
```

## SIEBanxico Class Instance ##

Querying Monetary Aggregates M1 (SF311408) and M2 (SF311418) Data

```python
 >>> from sie_banxico import SIEBanxico
 >>> api = SIEBanxico(token = token, id_series = ['SF311408' ,'SF311418'], language = 'en')
```

## Class documentation and attributes ##

```python
>>> api.__doc__
'Returns the full class documentation'
>>> api.token
'1b7da065cf574289a2cb511faeXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # This is an example token
>>> api.series
'SF311408,SF311418'
```

## Methods for modify the arguments of the object ##
### set_token: Change the current query token ###

```python
>>> api.set_token(token = new_token)
```

### set_id_series: Allows to change the series to query ###

```python
>>> api.append_id_series(id_series = ['SF311412'])
>>> api.series
'SF311408,SF311418,SF311412'
```

### append_id_series: Allows to update the series to query ###

```python
>>> api.set_id_series(id_series='SF311408-SF311418')
>>> api.series
'SF311408-SF311418'
```

## GET Request Methods ##

```python
>>> api = SIEBanxico(token = token, id_series = ['SF311408' ,'SF311418']
```

### get_metadata: Allows to consult metadata of the series ###
        Allows to consult metadata of the series.
        Returns:
            dict: json response format

```python
>>> api.get_metadata()
{'bmx': {'series': [{'idSerie': 'SF311418', 'titulo': 'Monetary Aggregates M2 = M1 + monetary instruments held by residents', 'fechaInicio': '12/01/2000', 'fechaFin': '11/01/2021', 'periodicidad': 'Monthly', 'cifra': 'Stocks', 'unidad': 'Thousands of Pesos', 'versionada': False}, {'idSerie': 'SF311408', 'titulo': 'Monetary Aggregates M1', 'fechaInicio': '12/01/2000', 'fechaFin': '11/01/2021', 'periodicidad': 'Monthly', 'cifra': 'Stocks', 'unidad': 'Thousands of Pesos', 'versionada': False}]}}
```

### get_lastdata: Returns the most recent published data ###
Returns the most recent published data for the requested series.
        Args:
            pct_change (str, optional): None (default) for levels, "PorcObsAnt" for change rate compared to the previous observation, "PorcAnual" for anual change rate, "PorcAcumAnual" for annual acummulated change rate.
        Returns:
            dict: json response format

```python
>>> api.get_lastdata()
{'bmx': {'series': [{'idSerie': 'SF311418', 'titulo': 'Monetary Aggregates M2 = M1 + monetary instruments held by residents', 'datos': [{'fecha': '01/11/2021', 'dato': '11,150,071,721.09'}]}, {'idSerie': 'SF311408', 'titulo': 'Monetary Aggregates M1', 'datos': [{'fecha': '01/11/2021', 'dato': '6,105,266,291.65'}]}]}}
```

### get_timeseries: Allows to consult time series data ###
        Allows to consult the whole time series data, corresponding to the period defined between the initial date and the final date in the metadata.
        Args:
            pct_change (str, optional): None (default) for levels, "PorcObsAnt" for change rate compared to the previous observation, "PorcAnual" for anual change rate, "PorcAcumAnual" for annual acummulated change rate.
        Returns:
            dict: json response format

```python
>>> api.get_timeseries(pct_change='PorcAnual')
{'bmx': {'series': [{'idSerie': 'SF311418',
    'titulo': 'Monetary Aggregates M2 = M1 + monetary instruments held by residents',
    'datos': [{'fecha': '01/12/2001', 'dato': '12.89'},
     {'fecha': '01/01/2002', 'dato': '13.99'},
     ...
     {'fecha': '01/11/2021', 'dato': '13.38'}],
     'incrementos': 'PorcAnual'}]}}
```

### get_timeseries_range: Returns the data for the period defined ###
        Returns the data of the requested series, for the defined period.
        Args:
            init_date (str): The date on which the period of obtained data starts. The date must be sent in the format yyyy-mm-dd. If the given date is out of the metadata time range, the oldest value is returned.
            end_date (str): The date on which the period of obtained data concludes. The date must be sent in the format yyyy-mm-dd. If the given date is out of the metadata time range, the most recent value is returned.
            pct_change (str, optional): None (default) for levels, "PorcObsAnt" for change rate compared to the previous observation, "PorcAnual" for anual change rate, "PorcAcumAnual" for annual acummulated change rate.     
        Returns:
            dict: json response format

```python
>>> api.get_timeseries_range(init_date='2000-12-31', end_date='2004-04-01')
{'bmx': {'series': [{'idSerie': 'SF311408',
    'titulo': 'Monetary Aggregates M1',
    'datos': [{'fecha': '01/01/2001', 'dato': '524,836,129.99'},
     {'fecha': '01/02/2001', 'dato': '517,186,605.97'},
     ...
     {'fecha': '01/04/2004', 'dato': '2,306,755,672.89'}]}]}}
```
## Pandas integration for data manipulation (and further analysis) ##
All the request methods returns a response in json format that can be used with other Python libraries.

The response for the api.get_timeseries_range(init_date='2000-12-31', end_date='2004-04-01') is a nested dictionary, so we need to follow a path to extract the specific values for the series and then transform the data into a pandas object; like a Serie or a DataFrame. For example:

```python
data = api.get_timeseries_range(init_date='2000-12-31', end_date='2004-04-01')

# Extract the Monetary Aggregate M1 data
data['bmx']['series'][0]['datos']
[{'fecha': '01/01/2001', 'dato': '524,836,129.99'},
 ...
 {'fecha': '01/04/2004', 'dato': '799,774,807.43'}]

# Transform the data into a pandas DataDrame
import pandas as pd
df = pd.DataFrame(timeseries_range['bmx']['series'][0]['datos'])
df.head()
        fecha            dato
0  01/01/2001  524,836,129.99
1  01/02/2001  517,186,605.97
2  01/03/2001  509,701,873.04
3  01/04/2001  511,952,430.01
4  01/05/2001  514,845,459.96
```

Another useful pandas function to transform json formats into a dataframe is 'json_normalize':

```python
df = pd.json_normalize(timeseries_range['bmx']['series'], record_path = 'datos', meta = ['idSerie', 'titulo'])
df['titulo'] = df['titulo'].apply(lambda x: x.replace('Monetary Aggregates M2 = M1 + monetary instruments held by residents', 'Monetary Aggregates M2'))
df.head()
        fecha            dato   idSerie                  titulo
0  01/01/2001  524,836,129.99  SF311408  Monetary Aggregates M1
1  01/02/2001  517,186,605.97  SF311408  Monetary Aggregates M1
2  01/03/2001  509,701,873.04  SF311408  Monetary Aggregates M1
3  01/04/2001  511,952,430.01  SF311408  Monetary Aggregates M1
4  01/05/2001  514,845,459.96  SF311408  Monetary Aggregates M1
df.tail()
         fecha              dato   idSerie                  titulo
75  01/12/2003  2,331,594,974.69  SF311418  Monetary Aggregates M2
76  01/01/2004  2,339,289,328.74  SF311418  Monetary Aggregates M2
77  01/02/2004  2,285,732,239.36  SF311418  Monetary Aggregates M2
78  01/03/2004  2,312,217,167.10  SF311418  Monetary Aggregates M2
79  01/04/2004  2,306,755,672.89  SF311418  Monetary Aggregates M2
```

## Licence ##
The MIT License (MIT)

## By ##
Dillan Aguirre Sedeño
(dillan.as22@gmail.com)
