patient_id_query = """
 PREFIX ldcm: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX ldcmdh: <https://johanvansoest.nl/ontologies/LinkedDicom-dvh/>
prefix schema: <https://schema.org/>
select distinct ?x
where {
    ?s ldcmdh:PatientIdentifier ?x.
    ?s ldcmdh:containsStructureDose ?str.
    ?str ldcmdh:structureName ?name.
}"""

dvh_curve_query = """
PREFIX ldcm: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX ldcmdh: <https://johanvansoest.nl/ontologies/LinkedDicom-dvh/>
prefix schema: <https://schema.org/>
select distinct ?p_id ?str ?d_value ?v_value
where {
	?s ldcmdh:PatientIdentifier ?p_id.
    ?s ldcmdh:containsStructureDose ?str.
    ?str ldcmdh:structureName ?name.
    ?str ldcmdh:dvh_curve ?f.
    ?f ldcmdh:dvh_point ?x.
    ?x ldcmdh:dvh_d_point ?d_value.
    ?x ldcmdh:dvh_v_point ?v_value.
    } 
    """
dvh = """
PREFIX ldcm: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX ldcmdh: <https://johanvansoest.nl/ontologies/LinkedDicom-dvh/>
prefix schema: <https://schema.org/>
select distinct ?p_id ?name ?x ?d_value ?v_value
where {{
	?s ldcmdh:PatientIdentifier ?p_id.
	FILTER(?p_id = '{p_id}' && ?name = '{str}' ).
    ?s ldcmdh:containsStructureDose ?str.
    ?str ldcmdh:structureName ?name.
    ?str ldcmdh:dvh_curve ?f.
    ?f ldcmdh:dvh_point ?x.
    ?x ldcmdh:dvh_d_point ?d_value.
    ?x ldcmdh:dvh_v_point ?v_value.
}} """

query_detail_patient = """
PREFIX ldcm: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX ldcmdh: <https://johanvansoest.nl/ontologies/LinkedDicom-dvh/>
prefix schema: <https://schema.org/>
select distinct ?name ?VD2 ?VD95 ?VD98
where {{
	?s ldcmdh:PatientIdentifier ?p_id.
    FILTER(?p_id = '{p_id}').
    ?s ldcmdh:containsStructureDose ?str.
    ?str ldcmdh:structureName ?name.
    ?str ldcmdh:D2 ?VD2.
    ?str ldcmdh:D95 ?VD95.
    ?str ldcmdh:D98 ?VD98.
    
}}
    """

query_filter_by_id = """
PREFIX ldcm: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX ldcmdh: <https://johanvansoest.nl/ontologies/LinkedDicom-dvh/>
prefix schema: <https://schema.org/>
select distinct ?p_id ?name ?min ?max ?mean ?volume
where {{
	?s ldcmdh:PatientIdentifier ?p_id.
    FILTER(?p_id = '{p_id}').
    ?s ldcmdh:containsStructureDose ?str.
    ?str ldcmdh:structureName ?name.
    ?str ldcmdh:mean ?vmean.
    ?str ldcmdh:min ?vmin.
    ?str ldcmdh:max ?vmax.
    ?str ldcmdh:volume ?vvolume.
    
    ?vmin schema:value ?min.
    ?vmax schema:value ?max.
    ?vmean schema:value ?mean.
    ?vvolume schema:value ?volume.
}}
"""

query_clinical_patient = """

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

select distinct ?s 
where {
    ?s rdf:type <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16960> .
} 
"""
