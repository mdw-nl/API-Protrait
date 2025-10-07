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

query_clinical_patient_g = """
PREFIX path: <http://www.ontotext.com/path#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX nsi: <http://www.cancerdata.org/roo/>
PREFIX ncicb: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
SELECT ?id
    WHERE {
      # if instances might be typed via subclasses, keep the path:
      ?pat rdf:type/rdfs:subClassOf* ncicb:C16960 .
      
      ?pat nsi:P100061 ?id_h.
      ?id_h nsi:P100042 ?id
      
}
"""

query_clinical_data_sp_g = """
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX nsi:   <http://www.cancerdata.org/roo/>
PREFIX ncicb: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>

SELECT DISTINCT ?cat ?name ?value
WHERE {{
  # anchor the patient by its P100061/P100042 id
  ?pat rdf:type/rdfs:subClassOf* ncicb:C16960 ;
       nsi:P100061 ?id_h .
  ?id_h nsi:P100042 ?pid.
  FILTER(?pid ='{p_id}').

  # traverse ANY predicates except P100061, to any depth
  ?pat !(nsi:P100061)+ ?node .
  # leaf values
  ?node (nsi:P100042|nsi:local_value) ?value .
  # friendly field label
  BIND(REPLACE(STR(?node), ".*/", "") AS ?field)
  BIND( REPLACE(STR(?node), "/[^/]*$", "") AS ?withoutLast )
  BIND(REPLACE(str(?withoutLast),".*/","")as ?name)
  BIND("Generic" AS ?cat)
    }}





}}

"""

query_clinical_patient_hn = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix protrait: <https://protrait.com/>
select distinct ?id
where {
    ?s rdf:type <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16960> .
    ?s protrait:ID ?id

} 
"""
#query_clinical_cat = """
#PREFIX pro:  <https://protrait.com/>
#PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#
#SELECT DISTINCT ?id ?name_c
#WHERE {{
#
#  ?patient pro:ID ?id .
#  filter(?id ='{p_id}')
#  ?patient pro:has ?cat.
#  ?cat pro:has_name ?name_c.
#
#}}
#"""
query_clinical_cat = """
PREFIX pro:  <https://protrait.com/>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?cat ?name ?value
WHERE {{
  # Every patient
  ?patient pro:ID ?id .
  filter(?id ='{p_id}')

  # Patient → cancerTreatment → radiotherapy (exact root, no guessing)
  ?patient pro:has ?cat1.
  ?cat1 pro:has_name ?name_c.

  ?cat1 pro:has ?cat2.
  ?cat2 pro:has_name ?cat.
  

  # Any descendant node that has a value
  ?cat2 (pro:has)+ ?node .
  ?node pro:has_value ?value .
  ?prenode pro:has ?node.
   BIND( REPLACE(STR(?node), ".*/", "") AS ?name )
  
  
}}
"""

query_clinical_patient_detail = """
PREFIX pro:  <https://protrait.com/>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?cat ?name ?value
WHERE {{
  # Every patient
  ?patient pro:ID ?id .
  filter(?id ='{p_id}')

  # Patient → cancerTreatment → radiotherapy (exact root, no guessing)
  ?patient pro:has ?cat1.
  ?cat1 pro:has_name ?name_c.
  filter(?name_c ='{cat}')
  ?cat1 pro:has ?cat2.
  ?cat2 pro:has_name ?cat.
  

  # Any descendant node that has a value
  ?cat2 (pro:has)+ ?node .
  ?node pro:has_value ?value .
  ?prenode pro:has ?node.
   BIND( REPLACE(STR(?node), ".*/", "") AS ?name )
  
  
}}
"""
