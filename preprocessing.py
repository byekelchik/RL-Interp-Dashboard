import get_synthetic_heatmap_data as syn

def main_data_pipeline():
    
    # USING CSV FOR NOW, GCP WILL TAKE MORE TIME(POSSIBLY MUCH MORE IDK)
    # Training:
    #     - call RL Alg with the ofllowing parameters:
    #         epochs, episodes, start, end, num of layers
    #     - make unique name for saved model to be passed to testing
    # Testing:
    #     - import the previously saved model
    #     - need to remove date count in act()
    #     - same start/end as training
    #     - output data with choices to get_synthetic_heatmap_data()
    # get_synthetic_heatmap_data:
    #     - get correct data from the alg
    #     - send output to the alg, but correct the parameters to only include the ones necessary for synthetic data
    # Testing: 
    #     - output correctly labeled data to the dash app directory
    pass
