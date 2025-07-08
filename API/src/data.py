import logging

import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlDataFetcher:
    """
    Class to fetch data from a SPARQL endpoint and return it as a pandas DataFrame.
    """

    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint

    def get_data(self, query: str, **param) -> pd.DataFrame:
        """
        Fetches data from the SPARQL endpoint using the provided query.

        Args:
            query (str): The SPARQL query to execute.

        Returns:
            pandas.DataFrame: The results of the SPARQL query as a DataFrame.
        """
        return _get_data(query, self.endpoint, **param)


def _get_data(query: str, endpoint: str = None,
              **param: None) -> pd.DataFrame:
    """
    Fetches data from a SPARQL endpoint and returns it as a pandas DataFrame.

    Args:
        query (str): The SPARQL query to execute.
        endpoint (str): None

    Returns:
        pandas.DataFrame: The results of the SPARQL query as a DataFrame.
    """

    if param:
        logging.info(f"params is {param}")
        query = query.format(**param)
        logging.info(f"Query after formatting: {query}")
    else:
        logging.info("No params provided, using query as is")
    base_query = query
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(base_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    result_processed = pd.json_normalize(results['results']['bindings'])

    full_df = result_processed
    # Clean .value columns
    value_cols = [col for col in full_df.columns if col.endswith('.value')]
    clean_df = full_df[value_cols]

    # Rename them to remove the `.value` suffix
    clean_df.columns = [col.replace('.value', '') for col in clean_df.columns]
    return clean_df
