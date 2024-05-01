import streamlit as st
import spacy
from pyvis.network import Network
import networkx as nx
import os

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities_relations(doc):
    entities = list(set([ent.text for ent in doc.ents]))  # Use set to remove duplicates
    relations = []
    for token in doc:
        # Check for verbs and their subjects and objects
        if token.pos_ == 'VERB':
            subjects = [child for child in token.children if child.dep_ in ('nsubj', 'nsubjpass')]
            objects = [child for child in token.children if child.dep_ in ('dobj', 'attr', 'prep', 'pobj')]
            for subj in subjects:
                for obj in objects:
                    if obj.dep_ == 'prep':
                        # Include objects of prepositions
                        objects_prep = [child for child in obj.children if child.dep_ == 'pobj']
                        for obj_prep in objects_prep:
                            relations.append((subj.text, token.lemma_ + ' ' + obj.text, obj_prep.text))
                    else:
                        relations.append((subj.text, token.lemma_, obj.text))
    return entities, relations

def create_network(entities, relations):
    G = nx.Graph()
    G.add_nodes_from(entities)
    G.add_edges_from([(rel[0], rel[2], {'label': rel[1]}) for rel in relations])
    return G

def draw_network(G, path='graph.html'):
    net = Network(height="700px", width="700px", bgcolor="#ffffff", font_color="#000000")  # Set background to white and font to black
    net.from_nx(G)
    # Use the write_html method to save the visualization as an HTML file
    net.save_graph(path)
    return path


st.title('Knowledge Graph pewpewpewwwwwww')
text_input = st.text_area("enter text")


if st.button('Generate Graph'):
    doc = nlp(text_input)
    entities, relations = extract_entities_relations(doc)
    G = create_network(entities, relations)
    path = draw_network(G)
    HtmlFile = open(path, 'r', encoding='utf-8')
    source_code = HtmlFile.read()    
    st.components.v1.html(source_code, height=500)
