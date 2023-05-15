import pandas as pd
import numpy as np
import re

def preprocessing(df_school, df_gep, df_ip):
        """This function extracts and formats the school nature, school type,
        programmes and cca information"""

        df_school_processed = (df_school
                        .assign(Clean_School_Nature=lambda df_: df_.School_Nature.str.split("\nSchool nature:\n").str[1],
                                Clean_School_Type=lambda df_: df_.School_Type.str.extract('School type:\n(.*)\nSchool fees'),
                                Clean_Programmes=lambda df_: (df_.Programmes
                                                        .str.replace(r'^Programmes\n', '', regex=True)
                                                        .str.replace(r'Applied Learning Programme \(ALP\)\n', '', regex=True)
                                                        .str.replace(r'Learning for Life Programme \(LLP\)\n', '', regex=True)),
                                Clean_CCA=lambda df_: df_.CCA.str.replace(r" \(.*?\)", "", regex=True),
                                Clean_Affiliation=lambda df_: np.where(pd.notnull(df_.Affiliation), 'Yes', 'No')
                                )
                        .drop(['School_Type', 'School_Nature', 'Affiliation', 'Programmes', 'CCA'], axis=1)
                        .rename(columns={'Clean_School_Nature': 'School_Nature',
                                        'Clean_School_Type': 'School_Type',
                                        'Clean_Programmes': 'Programmes',
                                        'Clean_CCA': 'CCA',
                                        'Clean_Affiliation': 'Affiliation'})
                        .loc[:,['Name', 'School_Nature', 'School_Type', 'Affiliation', 'Programmes', 'CCA']]
                        .sort_values(by=['Name'], ascending=True)
                        )
        
        # Replacing name
        df_school_processed.at[145, 'Name'] = "St. Margaret's Primary School"

        # Remove non-existent school
        df_school_processed = df_school_processed.query("Name != 'Pioneer Primary School'")

        # Add GEP and IP information
        gep_list = list(df_gep.Name)
        ip_list = list(df_ip.Name)
        df_school_gep_ip = (df_school_processed
                              .assign(GEP=lambda df_: np.where(df_.Name.isin(gep_list), 'Yes', 'No'),
                                      IP=lambda df_: np.where(df_.Name.isin(ip_list), 'Yes', 'No'))
        )
        return df_school_gep_ip

def create_cca_list(df_school_processed):
        """This function takes the list of CCAs and one hot encode it"""

        # One hot encode all the CCAs
        df_school_cca = pd.concat([df_school_processed.loc[:, 'Name'], 
                                   df_school_processed.CCA.str.get_dummies(sep='\n')], axis=1)
        
        # Replace all 0 with nans
        cols = df_school_cca.columns.to_list()
        cols.remove('Name')
        df_school_cca[cols] = df_school_cca[cols].replace({0: np.nan})

        # Melt CCA score and save to dataframe
        df_melt_school_cca = pd.melt(df_school_cca, 
                             id_vars=['Name'], 
                             var_name='CCA',
                             value_name='Indicator',
                             value_vars=cols)

        df_melt_school_cca.to_csv("../../data/processed/full-school-cca-points.csv", index=False)
        return df_school_cca


def assign_cca_score(df_school_cca):
        """ Assign each CCA a value according to how rare it is (count).
          and sum up the total value"""

        df_cca_processed = df_school_cca.copy()

        # Obtain the max count
        max_count = df_cca_processed.drop('Name', axis=1).sum(axis=0).max() + 1

        # Assign each CCA to a value, which is based on Count
        sum_cca = (df_cca_processed
           .iloc[:, 1:]
           .sum(axis=0)
           .reset_index()
           .rename(columns={'index': 'CCA',
                            0: 'Count'})
           .assign(Points=lambda df_: max_count  - df_.Count)
        )
        
        # Save cca points dataframe
        sum_cca.to_csv("../../data/processed/cca-points.csv", index=False)

        # Create a dictionary containing {'CCA': 'Points'}
        dict_cca_points = dict(zip(sum_cca.CCA, sum_cca.Points))
        
        # Multiply the points i.e (1 * points)
        for col in list(df_cca_processed.columns)[1:]:
                points = dict_cca_points[col]
                indicators = np.array(df_cca_processed[col])
                df_cca_processed[col] =  np.multiply(indicators, points)
        
        # Remove first column 'Name', which is not numeric, so that we can perform aggregations
        cols_to_sum = df_cca_processed.columns.to_list()
        cols_to_sum.remove('Name')

        # Perform aggregations
        df_cca_scores = (df_cca_processed
                        .assign(CCA_Sum_Score = df_cca_processed[cols_to_sum].sum(axis=1),
                                CCA_Avg_Score = df_cca_processed[cols_to_sum].mean(axis=1),
                                CCA_Median_Score = df_cca_processed[cols_to_sum].median(axis=1),
                                Number_of_CCA = df_cca_processed[cols_to_sum].count(axis=1),
                                CCA_Skewed=lambda df_: np.where(df_.CCA_Avg_Score > df_.CCA_Median_Score, "Right Skewed", 
                                                                np.where(df_.CCA_Avg_Score == df_.CCA_Median_Score, 'Symmetric', 'Left Skewed')
                                ))
                        .loc[:,['Name', 'Number_of_CCA', 'CCA_Sum_Score']])

        return df_cca_scores

def combine_main_and_cca(df_school_gep_ip, df_cca_scores):

        # Merge the total CCA score to the main data
        df_school_data = (df_school_gep_ip
                           .merge(df_cca_scores, left_on=['Name'], right_on=['Name'], how='left')
                           .drop(['Programmes', 'CCA'], axis=1)
        )
        return df_school_data

def clean_vacancy_data(df_vacancy):

        # Map the school name to match school-details
        df_ref = pd.read_csv("../../data/reference/School_Map_Name.csv")
        ref_dict = dict(zip(df_ref.School_Name, df_ref.Name))
        df_vacancy_clean = (df_vacancy
                    .assign(Name=lambda df_: df_.School_Name.map(ref_dict),
                            Phase1_sub_taken=lambda df_: df_.Phase1_taken/df_.Phase1_vac*100,
                            Phase1_sub_apply=lambda df_: df_.Phase1_applied/df_.Phase1_vac*100,
                            Phase2A_sub_taken=lambda df_: df_.Phase2A_taken/df_.Phase2A_vac*100,
                            Phase2A_sub_apply=lambda df_: df_.Phase2A_applied/df_.Phase2A_vac*100,
                            Phase2B_sub_taken=lambda df_: df_.Phase2B_taken/df_.Phase2B_vac*100,
                            Phase2B_sub_apply=lambda df_: df_.Phase2B_applied/df_.Phase2B_vac*100,
                            Phase2C_sub_taken=lambda df_: df_.Phase2C_taken/df_.Phase2C_vac*100,
                            Phase2C_sub_apply=lambda df_: df_.Phase2C_applied/df_.Phase2C_vac*100,
                            After_Phase1_2A_vac=lambda df_: df_.Phase2A_vac - df_.Phase2A_taken,
                            After_Phase2B_vac=lambda df_: df_.Phase2B_vac - df_.Phase2B_taken,
                            After_Phase2C_vac=lambda df_: df_.Phase2C_vac - df_.Phase2C_taken,
                            Phase2A_oversub=lambda df_:  np.where(df_.Phase2A_applied > df_.Phase2A_vac, 'Yes', 'No'),
                            Phase2B_oversub=lambda df_: np.where(df_.Phase2B_applied > df_.Phase2B_vac, 'Yes', 'No'),
                            Phase2C_oversub=lambda df_: np.where(df_.Phase2C_applied > df_.Phase2C_vac, 'Yes', 'No'),
                            Phase2A_oversub_count=lambda df_: np.where(df_.Phase2A_oversub == 'Yes', df_.Phase2A_applied - df_.Phase2A_vac, 'No'),
                            Phase2B_oversub_count=lambda df_: np.where(df_.Phase2B_oversub == 'Yes', df_.Phase2B_applied - df_.Phase2B_vac, 'No'),
                            Phase2C_oversub_count=lambda df_: np.where(df_.Phase2C_oversub == 'Yes', df_.Phase2C_applied - df_.Phase2C_vac, 'No'))
                    .drop("School_Name", axis=1))

        return df_vacancy_clean



if __name__ == "__main__":

        # Read files
        df_school_vacancy = pd.read_csv("../../data/raw/vacancy-data.csv")
        df_school = pd.read_csv("../../data/raw/school-details.csv")
        df_gep = pd.read_csv("../../data/raw/school-gep.csv")
        df_ip = pd.read_csv("../../data/raw/school-ip.csv")

        # Preprocess
        df_school_gep_ip = preprocessing(df_school, df_gep, df_ip)
        df_cca = create_cca_list(df_school_gep_ip)
        df_cca_scores = assign_cca_score(df_cca)
        df_school_full = combine_main_and_cca(df_school_gep_ip, df_cca_scores)
        df_vacancy_clean = clean_vacancy_data(df_school_vacancy)

        # Save to file
        df_school_full.to_csv("../../data/processed/clean-school-details.csv", index=False)
        df_cca.to_csv("../../data/processed/clean-cca-data.csv", index=False)
        df_vacancy_clean.to_csv("../../data/processed/clean-vacancy-data.csv", index=False)