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