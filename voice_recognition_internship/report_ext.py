import pandas as pd
import json, os
from austalk import mylistdir


def read_result(exp_setting):
    '''
    read experiment result from exp_setting
    return a data frame
    '''
    
    #read the experiment setting
    with open(exp_setting,"r") as exp_setting:
        setting = json.loads(exp_setting.read())
    
    #read the result
    result_csv = os.path.join("result/",setting['title']+'.csv')
    data = pd.read_csv(result_csv)

    #remove rows with out scores because some enrolment failed
    data = data[data['score'].notnull()]


    content_list = []
    for i in range(0,data.shape[0]):
        for n in range(len(setting['verify'])):
            content = setting['verify'][n]

            if content in data.audio.iloc[i]:
                content_list.append(content)
                break
    data = data.assign(content=content_list)
    

    

    return(data)


def frr_far_cal(data, benchmark):
    '''
    calculate the false rejection rate based on the threshold from benchmark 
    and the threshold optimized based on each dataframe
    para::data : data frame, the experiment dataframe
    para::train_data : string, which content the threshold is optimised on
    para::benchmark : the benchmark use to calculate the benchmark false rejection rate
    
    return:
    threshold: the optimised threshold based on the training data set
    opt_frr: the false rejection rate calculated based on the threshold
    b_frr = the false rejection rate calculated based on the benchmark score
    '''
    
    try:
        # split the data based on true speaker and imposter
        true_speaker = data.loc[data['true_speaker']==1]
        imposter = data.loc[data['true_speaker']==0]

        # split the data for training and testing
        true_speaker_train = true_speaker.loc[(true_speaker['content']=="_3_004") | (true_speaker['content']=="_3_005")]
        true_speaker_test = true_speaker.loc[(true_speaker['content']!="_3_004") & (true_speaker['content']!="_3_005")]
        imposter_train = imposter.loc[(imposter['content']=="_3_004") | (imposter['content']=="_3_005")]
        imposter_test = imposter.loc[(imposter['content']!="_3_004") & (imposter['content']!="_3_005")]
        
        
        #caclulate the threshold
        threshold_fr = imposter_train.score.quantile(.99,'higher')
        false_reject = true_speaker_test[true_speaker_test['score']<threshold_fr].shape[0]
        false_reject_R = false_reject/true_speaker_test.shape[0]

        threshold_fa = true_speaker_train.score.quantile(.01,'lower')
        false_accept = imposter_test[imposter_test['score']>threshold_fa].shape[0]
        false_accept_R = false_accept/imposter_test.shape[0]
        
        false_reject_b = true_speaker_test[true_speaker_test['score']<benchmark[0]].shape[0]
        false_reject_R_b = false_reject_b/true_speaker_test.shape[0]
        
        false_accept_b = imposter_test[imposter_test['score']>benchmark[1]].shape[0]
        false_accept_R_b = false_reject_b/imposter_test.shape[0]
        
    except ZeroDivisionError:
        threshold_fr = None
        false_reject_R = None
        false_reject_R_b = None
        threshold_fa = None
        false_accept_R = None
        alse_accept_R_b = None
    
    return {"threshold_ffr":threshold_fr, "frr_opt":false_reject_R,"frr_b":false_reject_R_b, "fr_b":false_reject_b, "fr_opt":false_reject,
           "threshold_far":threshold_fa, "far_opt":false_accept_R,"far_b":false_accept_R_b,"fa_b":false_accept_b, "fa_opt":false_accept}





def extract_result(exp_files, experiment_setting, benchmark):
    '''take the input of the experiment result and setting for a list of false rejection rate'''
    
    
    #remove rows with out scores because some enrolment failed
    result =[]
    for exp_filename in experiment_setting:
        if any(map(lambda x: x in exp_filename, exp_files)):
            exp_setting = os.path.join('completed_experiment',exp_filename)
            exp_result = read_result(exp_setting)

            with open(exp_setting,"r") as exp_setting:
                exp_config = json.loads(exp_setting.read())

            cal = frr_far_cal(exp_result,benchmark)

            output = {"enrol_treatment":exp_config["enrol_treatment"],
             "enrol_treatment":exp_config["enrol_treatment"]+str(exp_config['enrol_signal_to_noise_ratio']),
             "verify_treatment":exp_config["verify_treatment"]+str(exp_config['verify_signal_to_noise_ratio']),
            "channel":exp_config["channel"],
              "experiment":exp_config['title']}
            output.update(cal)
            result.append(output)

    df = pd.DataFrame(result)
    
    return df




def result_df(exp_file_exp, benchmark):
    '''
    take a list of regular expression of the needed file name
    return a dataframe from the selected files
    '''
    
    experiment_settings = mylistdir('completed_experiment/')
    result =[]
    for exp_filename in experiment_settings:
        if any(map(lambda x: x in exp_filename, exp_file_exp)):
            experiment_setting = os.path.join('completed_experiment',exp_filename)
            
            
            with open(experiment_setting,"r") as exp_setting:
                experiment_result = os.path.join('result',json.loads(exp_setting.read())['title']+'.csv')
                experiment_result = extract_result(experiment_result, experiment_setting, benchmark)
                for i in experiment_result:
                    result.append(i)
    df = pd.DataFrame(result)
    return(df)


def get_enrol_result(experiment_setting, exp_files):
    '''take a list of enrolment setting
    return a dataframe with each speaker enrolment status for each experiment '''

    experiment_setting = mylistdir('completed_experiment')
    exp_files = ['experiment11_0','experiment12_','experiment13_0','experiment14_']
    result =pd.DataFrame()
    for exp_filename in experiment_setting:
        if any(map(lambda x: x in exp_filename, exp_files)):
            exp_setting = os.path.join('completed_experiment',exp_filename)
            with open(exp_setting,"r") as exp_setting:
                exp_config = json.loads(exp_setting.read())
            enrol_path = os.path.join('result/enrol','enrol_'+exp_config['title']+'.csv')
            enrol = pd.read_csv(enrol_path)
            enrol = enrol.assign(channel = exp_config['channel'])
            enrol = enrol.assign(treatment = exp_config['enrol_treatment']+exp_config['enrol_signal_to_noise_ratio'])
            result = result.append(enrol)
    
    return(result)








if __name__ == '__main__':
    exp_setting = 'completed_experiment/experiment1_0.json'
    data = read_result(exp_setting)
    print(data.head())

    result = []

    with open(exp_setting, "r") as exp_setting:
        exp_config = json.loads(exp_setting.read())
    print(exp_config)

    frr = false_reject_rate(data, '3_004', 1)

    print(frr)