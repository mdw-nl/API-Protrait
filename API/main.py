import requests
import logging
from src.data import SparqlDataFetcher
from src.query import patient_id_query, dvh_curve_query
import traceback
from fastapi import FastAPI, Body, Query, HTTPException
app = FastAPI()

logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


@app.get("/patients", tags=["Patient Data"], summary="Retrieve Patient IDs")
async def get_patients_processed(endpoint: str):
    """
    Endpoint to retrieve all patients ID for which dvh calculation has been done.

    Returns:
        dict: A dictionary containing the list of patient IDs.
    """
    try:
        sdf = SparqlDataFetcher(endpoint=endpoint)
        result = sdf.get_data(query=patient_id_query)
        logging.info(f"Retrieved {len(result)} patients.")
        return {"patients": result}
    except Exception as e:
        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")

        logging.error(f"Error retrieving patient data: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")


@app.get("/dvh_curve", tags=["DVH curve"], summary="Retrieve DVH curve per patient and structure")
async def get_patients_processed(endpoint: str):
    """
    Endpoint to retrieve all patients ID for which dvh calculation has been done.

    Returns:
        dict: A dictionary containing the list of patient IDs.
    """
    try:
        sdf = SparqlDataFetcher(endpoint=endpoint)
        result = await sdf.get_data(query=dvh_curve_query)
        logging.info(f"Retrieved {len(result)} patients.")
        return {"patients": result}
    except Exception as e:
        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")

        logging.error(f"Error retrieving dvh data: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")


# post request to upload json to graphdb
@app.post("/upload_json", tags=["GraphDB Operations"], summary="Upload JSON-LD to GraphDB")
async def upload_json_to_graphdb(jsonld_data: dict = Body(...), endpoint: str = Query(...)):
    """
    Endpoint to upload JSON-LD data to a GraphDB repository.

    Args:
        jsonld_data (dict): The JSON-LD data to upload.
        graphdb_url (str): The GraphDB repository URL for uploading the data.

    Returns:
        dict: A confirmation message indicating success or failure.
        :param jsonld_data:
        :param endpoint:
    """
    headers = {"Content-Type": "application/ld+json"}
    try:

        response = requests.post(endpoint, headers=headers, json=jsonld_data)
        logging.info("JSON-LD data successfully uploaded to GraphDB.")
        if response.status_code in [200, 201, 204]:
            logging.info("Upload successful.")
            return {"message": "Data successfully uploaded to GraphDB."}
        else:
            raise Exception(f"Failed to upload data to GraphDB.{response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Error uploading JSON-LD data: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload data to GraphDB.")
