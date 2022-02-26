# Import necessary modules
import pandas as pd
import math
import sys
import numpy as np
from scipy.spatial import distance
import pickle

def find_top_similar_entitties(max, nba, distance_frame, primary_column):
    
    similar_list = []

    for i in range(max):
    
        current_farthest            = distance_frame.iloc[i]["idx"]
        #print('closest player index: '+str(int(current_farthest)))
        close_to_the_top_founder    = nba.loc[int(current_farthest)][primary_column]

        current_distance    = distance_frame.iloc[i]["dist"]
        percentile          = 100 - (100 / 18.9714833602) * current_distance
        
        current_distance = round(current_distance, 2)
    
        if percentile < 0:
            percentile = 0  
            
        percentile = round(percentile, 2)    

        print('similar '+str(i)+' : '+str(close_to_the_top_founder) + ' - distance : '+str(current_distance) + ", Percentile : "+ (str(percentile)))

        current_country = {
            "country"       : str(close_to_the_top_founder),
            "distance"      : current_distance,
            "percentile"    : percentile
        }

        similar_list.append(current_country)

    return similar_list 

def find_similar_learner(columns, primary_column, given_entity_name):
    
    df = pd.read_csv("datasets/cleaned_gender_inequality.csv")

    df.fillna(round(df.mean()), inplace=True)

    selected_player = df[df[primary_column] == given_entity_name].iloc[0]   
    nba_numeric     = df[columns]
    nba_normalized  = (nba_numeric - nba_numeric.mean()) / nba_numeric.std()

    nba_normalized.fillna(round(nba_normalized.mean()), inplace=True)

    top_founder_normalized  = nba_normalized[df[primary_column] == given_entity_name]
    euclidean_distances     = nba_normalized.apply(lambda row: distance.euclidean(row, top_founder_normalized), axis=1)
    distance_frame          = pd.DataFrame(data={"dist": euclidean_distances, "idx": euclidean_distances.index})

    distance_frame.sort_values(by=["dist"], inplace=True)

    second_smallest     = distance_frame.iloc[1]["idx"]
    most_nearer_entity  = df.loc[int(second_smallest)][primary_column]

    print('Direct similarity : '+most_nearer_entity)

    print('\nTop 10 similar learner Sorted')
    similar_10_list = find_top_similar_entitties(11, df, distance_frame, primary_column)

    return similar_10_list

def find_similar_student(top_developer_name):

    columns = [
        'GII Rank',
        'Gender Inequality Index (GII)',
        'Maternal Mortality Ratio',
        'Adolescent Birth Rate',    
        'Percent Representation in Parliament',
        'Population with Secondary Education (Female)',
        'Population with Secondary Education (Male)',
        'Labour Force Participation Rate (Female)',
        'Labour Force Participation Rate (Male)',
    ]

    primary_column = "Country"

    return find_similar_learner( columns, primary_column, top_developer_name)

def startpy():

    find_similar_student('India')
    
    pickle_out = open("knn-model.pkl", "wb")

    pickle.dump(find_similar_student ,pickle_out)

    pickle_out.close()

# if __name__ == '__main__':
#     startpy()