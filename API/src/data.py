import logging

import pandas
from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlDataFetcher:
    """
    Class to fetch data from a SPARQL endpoint and return it as a pandas DataFrame.
    """

    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint

    def get_data(self, query: str) -> pandas.DataFrame:
        """
        Fetches data from the SPARQL endpoint using the provided query.

        Args:
            query (str): The SPARQL query to execute.

        Returns:
            pandas.DataFrame: The results of the SPARQL query as a DataFrame.
        """
        return _get_data(query, self.endpoint)


def _get_data(query: str, endpoint: str = None) -> pandas.DataFrame:
    """
    Fetches data from a SPARQL endpoint and returns it as a pandas DataFrame.

    Args:
        query (str): The SPARQL query to execute.
        endpoint (str): None

    Returns:
        pandas.DataFrame: The results of the SPARQL query as a DataFrame.
    """
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    logging.info(results)
    return pandas.json_normalize(results['results']['bindings'])
