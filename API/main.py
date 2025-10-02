import requests
import logging
from src.sparql_interface import SparqlDataFetcher
from src.sparql_query import patient_id_query, dvh_curve_query, query_filter_by_id, \
    query_clinical_patient_g, query_clinical_cat, query_clinical_patient_detail,query_clinical_data_sp_g
import traceback
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

app = FastAPI()
logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


@app.get("/", tags=["Root"], summary="Root Endpoint")
async def root():
    """
    Root endpoint to check if the API is running.

    Returns:
        dict: A simple message indicating that the API is running.
    """
    return {"message": "API is running"}


@app.get("/patients_dvh", tags=["Patient Data"], summary="Retrieve Patient IDs")
async def get_patients_processed(endpoint: str):
    """
    Endpoint to retrieve all patients ID for which dvh calculation has been done.

    Returns:
        dict: A dictionary containing the list of patient IDs.
    """
    try:
        sdf = SparqlDataFetcher(endpoint=endpoint)
        result = await run_in_threadpool(sdf.get_data, patient_id_query)
        logging.info(f"Retrieved {len(result)} patients.")
        return JSONResponse(content=result.to_dict(orient="records"))
    except Exception as e:
        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")

        logging.error(f"Error retrieving patient data: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")


@app.get("/patients_dvh/{p_id}", tags=["Patient Data"], summary="Retrieve Patient IDs DVH")
async def get_patients_by_id(endpoint: str, p_id: str):
    """
    Endpoint to retrieve all patients ID for which dvh calculation has been done.

    Returns:
        dict: A dictionary containing the list of patient IDs.
    """
    try:
        sdf = SparqlDataFetcher(endpoint=endpoint)
        result = await run_in_threadpool(sdf.get_data, query_filter_by_id, **{"p_id": p_id})
        logging.info(f"Retrieved {len(result)} patients.")
        return JSONResponse(content=result.to_dict(orient="records"))
    except Exception as e:
        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")

        logging.error(f"Error retrieving patient data: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")


@app.get("/dvh_curve", tags=["DVH curve"], summary="Retrieve DVH curve per patient and structure")
async def get_patients_processed(endpoint: str, p_id: str, str: str):
    """
    Endpoint to retrieve all patients ID for which dvh calculation has been done.

    Returns:
        dict: A dictionary containing the list of patient IDs.
    """
    try:
        sdf = SparqlDataFetcher(endpoint=endpoint)
        # result = await sdf.get_data(query=dvh_curve_query)
        result = await run_in_threadpool(sdf.get_data, dvh_curve_query, **{"p_id": p_id, "str": str})
        logging.info(f"Retrieved {len(result)} patients.")
        return {"patients": result}
    except Exception as e:
        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")

        logging.error(f"Error retrieving dvh data: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")


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


@app.get("/clinical_patient", tags=["Clinical Data"], summary="Retrieve Clinical Data")
async def get_patient_clinical_data(endpoint: str):
    """
    Endpoint to retrieve clinical data for a specific patient.

    Args:
        endpoint (str): The GraphDB repository URL.
        p_id (str): The patient ID.

    Returns:
        dict: A dictionary containing the clinical data for the specified patient.
    """
    try:
        sdf = SparqlDataFetcher(endpoint=endpoint)
        # result = await sdf.get_data(query=dvh_curve_query)
        result = await run_in_threadpool(sdf.get_data, query_clinical_patient_g)
        logging.info(f"Retrieved {len(result)} patients.")
        return JSONResponse(content=result.to_dict(orient="records"))
    except Exception as e:
        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")

        logging.error(f"Error retrieving dvh data: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")


@app.get("/clinical_patient/{p_id}", tags=["Clinical Data"], summary="Retrieve Clinical Data by patient ID")
async def get_generic_by_patient_id(endpoint: str, p_id: str):
    """
    Endpoint to retrieve clinical data for a specific patient.

    Args:
        endpoint (str): The GraphDB repository URL.
        p_id (str): The patient ID.

    Returns:
        dict: A dictionary containing the clinical data for the specified patient.
    """
    try:
        sdf = SparqlDataFetcher(endpoint=endpoint)
        result = await run_in_threadpool(sdf.get_data, query_clinical_data_sp_g, **{"p_id": p_id})
        logging.info(f"Retrieved {len(result)} patients.")
        return JSONResponse(content=result.to_dict(orient="records"))
    except Exception as e:
        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")

        logging.error(f"Error retrieving dvh data: {e}")
        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")


#@app.get("/clinical_patient/{p_id}", tags=["Clinical Data"], summary="Retrieve Clinical Data by patient ID")
#async def get_clinical_data_by_patient_id(endpoint: str, p_id: str):
#    """
#    Endpoint to retrieve clinical data for a specific patient.
#
#    Args:
#        endpoint (str): The GraphDB repository URL.
#        p_id (str): The patient ID.
#
#    Returns:
#        dict: A dictionary containing the clinical data for the specified patient.
#    """
#    try:
#        sdf = SparqlDataFetcher(endpoint=endpoint)
#        result = await run_in_threadpool(sdf.get_data, query_clinical_cat, **{"p_id": p_id})
#        logging.info(f"Retrieved {len(result)} patients.")
#        return JSONResponse(content=result.to_dict(orient="records"))
#    except Exception as e:
#        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")
#
#        logging.error(f"Error retrieving dvh data: {e}")
#        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")
#
#
#@app.get("/clinical_detail/{p_id}/{cat}", tags=["Clinical Detail"], summary="Clinical Detail sub cat")
#async def get_clinical_detail(endpoint: str, p_id: str, cat: str):
#    """
#    Detail of the clinical data for a specific patient and category.
#
#    Returns:
#        dict: A dictionary containing the clinical data for the specified patient and sub category.
#    """
#    try:
#        sdf = SparqlDataFetcher(endpoint=endpoint)
#        result = await run_in_threadpool(sdf.get_data, query_clinical_patient_detail, **{"p_id": p_id, "cat": cat})
#        return JSONResponse(content=result.to_dict(orient="records"))
#    except Exception as e:
#        logging.warning(f"Exception occurred while retrieving patient data: {traceback.format_exc()}")
#
#        logging.error(f"Error retrieving dvh data: {e}")
#        raise HTTPException(status_code=400, detail="Failed to retrieve patient data.")



