import urllib3, os
import json
import base64
import csv
from austalk import data_prep, mylistdir

urllib3.disable_warnings()
http = urllib3.PoolManager()


def read_audio(audio_list):
    '''
    create uttrances array based on a list of audio
    :param audio_list:
    :return:
    '''

    encodedbytes_list = list()

    for audio in audio_list:

        with open(audio, 'rb') as a:
            bytes = a.read()
            encodedBytes = base64.encodebytes(bytes).decode("utf-8")
            encodedbytes_list.append({"content": encodedBytes})

    utterances = json.dumps({"utterances": encodedbytes_list})

    return (utterances)


def enrolment(audio_directory, api, id, print_name, authorization):
    '''
    enrol the speakers in the audio directory
    :param audio_directory:
    :return: if the speaker successfully enrolled to the system
    '''

    audios = mylistdir(audio_directory)

    audio_list = []
    for audio in audios:
        audio_url = os.path.join(audio_directory, audio)
        audio_list.append(audio_url)

    # creating a post request for the speaker
    enrolment_url = api + 'voiceprint/'+ id +'/' + print_name +'/' + '?group='+ authorization
    enrolment = http.request("post", enrolment_url, body=read_audio(audio_list))
    result = {'speaker':id,'status':json.loads(enrolment.data.decode('utf-8'))['status']}

    return (result)



def enrol_speakers(enrol_dir, api, print_name, authorization):
    '''enrol all the speakers under a input directory'''


    speakers = mylistdir(enrol_dir)
    print(len(speakers), "speakers")

    results = []

    for speaker in speakers:
        results.append(enrolment(os.path.join(enrol_dir, speaker), api, speaker, print_name, authorization))

    return results



def verify(audio_url, api, id, print_name, authorization):
    '''
    verify a given audio of an id
    :param audio_url:
    :param api:
    :param id:
    :param print_name:
    :param authorization:
    :return:
    '''

    verify_url = api + 'voiceprint/' + id + '/' + print_name + '/' + '?group=' + authorization

    with open(audio_url, 'rb') as a:
        bytes = a.read()
        encodedBytes =base64.encodebytes(bytes).decode("utf-8")
        utterances = json.dumps({"utterance": {"content": encodedBytes}})

    verify = http.request("put", verify_url, body=utterances)

    return verify.data


def verify_speakers(input_directory, api, print_name, authorization):
    '''verify the speakers with each audio in the directory'''


    input = mylistdir(input_directory)

    for impulse in input:
        speakers_list_url = os.path.join(input_directory, impulse)
        speakers = mylistdir(speakers_list_url)

        result = {}
        for speaker in speakers:
            id = speaker
            speaker_url = os.path.join(speakers_list_url, speaker)
            print(id)

            audios = mylistdir(speaker_url)
            for audio in audios:
                audio_url = os.path.join(speaker_url, audio)
                result[id] = {"audio" : audio,
                    "result":verify(audio_url, api, id, print_name, authorization)}

    return result


def audio_quality(audio):
    '''
    check the quality of a particular audio
    :param audio:
    :return:
    '''

    with open(audio, 'rb') as a:
        bytes = a.read()
        encodedBytes = base64.encodebytes(bytes).decode("utf-8")

    utterances = json.dumps({"utterance": {"content": encodedBytes}})
    quality = http.request("post", quality_url, body=utterances)

    return quality.data


def cross_match(audio_url, api, print_name, authorization, ids):
    '''verify the speakers with each audio in the directory'''


    cross_match_url = api + 'voiceprint/' + print_name + '?group=' + authorization

    with open(audio_url, 'rb') as a:
        bytes = a.read()
        encodedBytes = base64.encodebytes(bytes).decode("utf-8")
        utterances = json.dumps({"utterance": {"content": encodedBytes},"ids":ids})

    cross_match = http.request("put", cross_match_url, body=utterances)

    return cross_match.data


def delete(api, id, print_name, authorization):
    '''
    delete a voice print from auraya
    :param api:
    :param id:
    :param print_name:
    :param authorization:
    :return:
    '''

    delete_url = api + 'voiceprint/' + id + '/' + print_name + '?group=' + authorization
    delete_voiceprint = http.request("DELETE", delete_url)

    return delete_voiceprint.data


def delete_speakers(audio_directory,api, print_name,authorization):
    '''remove all the speaker voice print from the speakers in the audio directory'''

    speakers = mylistdir(audio_directory)

    for speaker in speakers:
        delete_url = api + 'voiceprint/' + speaker + '/' + print_name + '?group=' + authorization
        delete_voiceprint = http.request("DELETE", delete_url)

        print(speaker)
        print(delete_voiceprint.data)


def main(auraya_config, exp_config):

    #read configure file
    print(exp_config['title'])

    api = auraya_config['api']
    authorization = auraya_config['authorization']
    print_name = auraya_config['print_name']

    enrol_directory = os.path.join(exp_config['output_directory']+'/'+exp_config['channel'],
                                   os.path.join('enrol',
                                                exp_config['enrol_treatment']+str(exp_config['enrol_signal_to_noise_ratio'])))
    verify_directory = os.path.join(exp_config['output_directory']+'/'+exp_config['channel'],
                                    os.path.join('verify',
                                                 exp_config['verify_treatment']+str(exp_config['verify_signal_to_noise_ratio'])))

    re_enrol = exp_config['re_enrol']

    if re_enrol == 'True':
        #remove the enrolled voice print
        print("remove all the speakers' previous voice print")
        delete_speakers(enrol_directory, api, print_name, authorization)

        # enrol speakers
        print('start enrolment')
        enrols = enrol_speakers(enrol_directory, api, print_name, authorization)

        # write enrolment result into file
        if not os.path.exists('result/enrol'):
            os.makedirs('result/enrol')
        result_path = os.path.join("result/enrol", 'enrol_'+ experiment['title'] + ".csv")
        f = csv.writer(open(result_path, "w"))
        f.writerow(["speaker","status"]) #write header

        for row in enrols:
            f.writerow([row["speaker"],row["status"]])

    # cross matching
    print('start cross matching')
    speakers = mylistdir(enrol_directory)
    result = []
    for speaker in speakers:
        # read files in output/enrol
        audios_url = os.path.join(verify_directory, speaker)
        audios = mylistdir(audios_url)
        print(speaker)
        for audio in audios:
            audio_url = os.path.join(audios_url, audio)
            cm_result = json.loads(cross_match(audio_url, api, print_name, authorization, speakers).decode('utf-8'))

            # store the result as json in a list
            for match in cm_result['speakers']:
                if match['id'] == speaker:
                    true_speaker = 1
                else:
                    true_speaker = 0

                result.append({"speaker": speaker, "match": match['id'], "audio": audio, "score": match['score'],
                               "true_speaker": true_speaker,"enrol_treatment":exp_config['enrol_treatment'],
                               "enrol_signal_to_noise_ratio": exp_config['enrol_signal_to_noise_ratio'],
                               "verify_treatment":exp_config['verify_treatment'],
                               'verify_signal_to_noise_ratio':exp_config['verify_signal_to_noise_ratio']})
    return(result)



if __name__ == '__main__':


    with open('auraya.json', 'r', encoding='utf-8') as config_file:
        auraya = json.load(config_file)

    experiments = mylistdir("experiment")
    experiments.sort()

    for exp_json in experiments:
        experiment_url = "experiment/"+exp_json
        print(exp_json)

        with open(experiment_url,'r', encoding='utf-8') as config_file:
            experiment = json.load(config_file)

        data_prep(experiment)

        result = main(auraya,experiment)

        # write file into csv
        result_path = os.path.join("result",experiment['title']+".csv")
        f = csv.writer(open(result_path, "w"))
        f.writerow(["speaker","match","audio", "score","true_speaker",
                    "enrol_treatment","enrol_signal_to_noise_ratio",
                    "verify_treatment","verify_signal_to_noise_ratio"]) #write header

        for row in result:
            f.writerow([row["speaker"],row["match"], row["audio"], row["score"],row["true_speaker"],
                        row["enrol_treatment"],row['enrol_signal_to_noise_ratio'],
                        row['verify_treatment'],row['verify_signal_to_noise_ratio']])
