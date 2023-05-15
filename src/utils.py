import pandas as pd 
from pathlib import Path
from configs import config


def read_data():
    df_school = pd.read_csv(Path(config['processed_dir'], config['school_data']))
    df_vacancy = pd.read_csv(Path(config['processed_dir'], config['vacancy_data']))
    
    # Include schools without CCA information
    # df_school_full = (df_school
    #                   .merge(df_vacancy, on=['Name'], how='left'))
    
    # Remove schools without CCA information
    df_school_cca = (df_school
                    .query("CCA_Sum_Score != 0"))
    
    df_school_full = (df_school
                     .merge(df_vacancy, left_on=['Name'], right_on=['Name'], how='left'))
    
    return df_school_full, df_school_cca

def read_cca_points():
    df_school_cca_points = pd.read_csv(Path(config['processed_dir'], config['school_cca_points']))
    df_cca_points = pd.read_csv(Path(config['processed_dir'], config['cca_points']))
    return df_school_cca_points, df_cca_points

