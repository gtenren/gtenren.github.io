import pyalveo
import os
import json
from scipy.signal import convolve
import librosa
import numpy as np
import random
import soundfile as sf

#initialize the API
# client = pyalveo.Client(configfile="alveo.config", use_cache=False)


def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""

    filelist = os.listdir(directory)
    return [x for x in filelist if not (x.startswith('.'))]


def download_item_list(item_list_url, speaker_data = False, channel='all', outputdir = 'data'):
    '''
    download all the files from an item list in alveo
    :param item_list_url:
    :param speaker:
    :param documents:
    :param outputdir:
    :return:
    '''

    client = pyalveo.Client(configfile="alveo.config", use_cache=False)
    item_lists = client.get_item_list(item_list_url)

    #focus on a particular item
    for url in item_lists:
        item_url = url
        item = client.get_item(item_url)
        meta = item.metadata()

        #set up output directory
        if speaker_data == True:
            #split into sub directory it is a speaker
            speakerurl = meta['alveo:metadata']['olac:speaker']
            speaker_meta = client.get_speaker(speakerurl)
            speakerid = speaker_meta['dcterms:identifier']
            subdir = os.path.join(outputdir, speakerid)

        else:
            subdir = outputdir

        #create sub-folder based on speaker names
        if not os.path.exists(subdir):
            os.makedirs(subdir)

        for doc in item.get_documents():
            filename = doc.get_filename()

            if filename.endswith('.wav') or filename.endswith('.TextGrid'):
                if channel != 'all':
                    if channel in filename:
                        print(filename)
                        doc.download_content(dir_path=subdir)
                else:
                    print(filename)
                    doc.download_content(dir_path=subdir)

    print('download complete')



def resample_audio(audio_url, outputdir, sr=8000):
    '''
    downsampling an audio and write it back to the output directory
    '''

    audio_name = os.path.basename(audio_url)
    audio,rate = librosa.load(audio_url)

    output_name = audio_name[:-4]+'8k.wav'
    output_audio(audio, outputdir, output_name, rate, sr)
    return(audio_name)


def resample_audios(audio_dir, outputdir, sr=8000):
    '''
    down sampling all the audio in a given speaker's directory
    and save the new file in the output directory
    :param audio_directory:
    :return:
    '''

    speakers = mylistdir(audio_dir)

    for speaker in speakers:
        audios = mylistdir(os.path.join(audio_dir,speaker))

        for audio in audios:
            audio_url = os.path.join(audio_dir, speaker+"/"+audio)
            output_url = os.path.join(outputdir, speaker)
            print(audio_url)
            resample_audio(audio_url,output_url, sr)


def convolve_audio(audio_url, impulse_url, output_directory, sr):
    '''
    take in a impulse signal and convolve it with an audio
    and save the file in the designated output directory

    :param target_sr: output sample rate
    :param audio_url: path of audio
    :param impulse_url: path of impulse signal
    :return: array, An N-dimensional array containing a subset of the discrete linear convolution of in1 with in2.
    '''

    # load wav file with librosa
    audio, audio_rate = librosa.load(audio_url)
    impulse, impulse_rate = librosa.load(impulse_url)
    output = convolve(audio, impulse)

    #write output wav file
    audio_name = os.path.basename(audio_url)[:-4]
    impulse_name = os.path.basename(impulse_url)[:-4]
    output_name = audio_name + '-' + impulse_name + '.wav'
    output_audio(output, output_directory, output_name, audio_rate, sr)


def convolve_audios(audio_directory, impulse_name, outputdir, sr):
    '''
    convolve all the file within the audio directory with the signal in the impulse directory
    files will be export to the output directory with the given sampling rate
    :param audio_directory: directory for the audio input
    :param impulse_directory: directory for the impulse signal
    :param outputdir: directory for the output
    :param sr: sampling rate
    :return: all the convolved audio from audio_directory
    '''

    #list out the file names in the input directory
    speakers = mylistdir(os.path.join(audio_directory))

    #list out the files for every speakers
    for speaker in speakers:
        speaker_dir = os.path.join(audio_directory, speaker)
        audios = mylistdir(os.path.join(speaker_dir))

        for audio in audios:
            audio_url = os.path.join(speaker_dir, audio)

            # create and write the files to the output directory
            impulse_url = os.path.join('data/impulse', impulse_name)
            output_directory = os.path.join(outputdir, speaker)
            convolve_audio(audio_url, impulse_url, output_directory, sr)

    print('convolution complete')


def initial_folders(directory):
    '''initialise the folder in the directory and create if the directory does not exist'''

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory + ' is created')

    else:
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        print(directory +' is initialised')


def white_noise(audio_url, output_directory, snr, sr):
    '''
    generate white noise based on certain signal to noise ratio
    output to the output directory
    '''

    audio, audio_rate = librosa.load(audio_url)
    rmse_a = np.mean(librosa.feature.rmse(audio))

    # generate white noise signal with amplitude based on snr and the root mean square energy of the audio
    noise = np.random.normal(0, rmse_a / snr, audio.shape)
    output = audio + noise

    # write the output file
    audio_name = os.path.basename(audio_url)[:-4]
    output_name = audio_name + '-white_noise' + '.wav'
    output_audio(output, output_directory, output_name, audio_rate, sr)


def add_white_noises(audio_directory, snr, output_directory, sr):
    '''
    :param audio_directory: directory for the input audio files
    :param snr: signal to noise ratio
    :param output_directory: output directory
    :return: all the audio files with white noise
    '''

    speakers = mylistdir(os.path.join(audio_directory))

    for speaker in speakers:
        speaker_dir = os.path.join(audio_directory, speaker)
        audio = mylistdir(speaker_dir)

        #add white noise for every audio for the speaker
        for a in audio:
            audio_url = os.path.join(speaker_dir, a)
            output_url = os.path.join(output_directory, speaker)
            white_noise(audio_url, output_url, snr, sr)

    print('white noise insert complete')


def bg_noise(audio_url, noise_url, output_directory, snr, target_sr):
    '''
    Add background noise to audio based on the given signal and noise ratio
    :param audio_url: audio directory url
    :param noise_url: noise directory url
    :param snr: signal noise ratio
    :return: audio time series
    '''

    audio, audio_rate = librosa.load(audio_url)
    rmse_a = np.mean(librosa.feature.rmse(audio))
    noise, noise_rate = librosa.load(noise_url)
    rmse_n = np.mean(librosa.feature.rmse(noise))

    #calculate the new rmse for background noise
    weight = (1/rmse_n)*(rmse_a/snr)
    noise = noise * weight

    #add the noise to audio
    if noise.shape[0]>=audio.shape[0]:
        noise = noise[0:audio.shape[0]]

    else:
        #randomise the start of the noise if the noise is shorter than the audio
        r = random.randint(1,round(audio.shape[0]/2,0))
        noise_n = np.hstack((np.zeros([r,]),noise))

        if noise_n.shape[0] > audio.shape[0]:
            noise = noise_n[audio.shape[0]]
        else:
            noise= np.hstack((noise_n, np.zeros([audio.shape[0]-noise_n.shape[0],])))

    output = audio + noise

    # write output into output directory
    audio_name = os.path.basename(audio_url)[:-4]
    noise_name = os.path.basename(noise_url)[:-4]
    output_name = audio_name + '-'+noise_name + '.wav'
    output_audio(output, output_directory, output_name, audio_rate, target_sr)



def add_bg_noises(audio_directory, noise_name, snr, outputdir,sr):
    '''
    insert background noise into the audio with a specific signal noise ratio
    :param audio_url: audio directory url
    :param noise_url: noise directory url
    :param snr: signal noise ratio
    :param sr: output sampling rate
    :return: audio overlay noise wav file output
    '''

    speakers = mylistdir(os.path.join(audio_directory))
    noise_url = os.path.join('data/noise',noise_name)

    for speaker in speakers:
        speaker_dir = os.path.join(audio_directory, speaker)
        audios = mylistdir(os.path.join(speaker_dir))
        for audio in audios:
            audio_url = os.path.join(speaker_dir, audio)
            output_directory = os.path.join(outputdir, speaker)
            bg_noise(audio_url, noise_url, output_directory, snr, sr)


    print('background noise is added')



def output_audio(audio,output_directory,output_name, original_sr, output_sr):
    '''
    output the audio files in the folder of the output directory
    and print what file is created
    :param audio:
    :param outputdir:
    :param output_name:
    :return:
    '''

    audio = librosa.resample(audio,original_sr,output_sr)
    path = os.path.join(output_directory, output_name)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    sf.write(path, audio, output_sr, subtype='PCM_16')
    print(output_name+' is created.')



def config(config_file):
    '''read the configure file and prepare data for the experiment'''

    # read configuration file
    with open(config_file,encoding='utf-8') as config_file:
        config = json.load(config_file)

    return config



def audio_manipulation(audio_directory, use, config):
    '''manipulate audio to create data for enrolment or vertification'''

    sr = config['sampling_rate']
    channel = config['channel']

    # set up the input and output directory url
    audio_dir = os.path.join(config['audio_directory'] + '/' + channel, use)
    outputdir = os.path.join(config['output_directory'] + '/' + channel, use)


    # check which treatment should be used
    if use == 'enrol':
        treatment = config['enrol_treatment']
        try:
            snr = int(config["enrol_signal_to_noise_ratio"])
        except ValueError:
            pass
        outputdir = os.path.join(outputdir,treatment+config['enrol_signal_to_noise_ratio'])

    elif use== 'verify':
        treatment = config['verify_treatment']
        try:
            snr = int(config["verify_signal_to_noise_ratio"])
        except ValueError:
            pass
        outputdir = os.path.join(outputdir, treatment + config['verify_signal_to_noise_ratio'])

    else:
        print('Key Error: use must be enrol/verify')


    # Call different function for different treatment
    if treatment == 'control':
        resample_audios(audio_directory, outputdir, 8000)

    elif treatment == 'convolve':
        impulse_name = config['impulse']
        convolve_audios(audio_dir, impulse_name, outputdir, sr)

    elif treatment == 'white_noise':
        add_white_noises(audio_dir, snr, outputdir, sr)

    elif treatment == 'bg_noise':
        noise_name =  config['noise']
        add_bg_noises(audio_dir, noise_name, snr, outputdir, sr)

    else:
        print('unknown treatment, please use control/convolve/white_noise/bg_noise')


def data_prep(config):


    audio_directory = config['audio_directory']
    impulse_directory = config['impulse_directory']
    output_directory = config['output_directory']
    channel = config['channel']

    enrol_dir = os.path.join(output_directory, channel+'/'+'enrol')
    enrol_audio_dir = os.path.join(audio_directory, channel+'/'+'enrol')
    verify_dir = os.path.join(output_directory, channel+'/'+'verify')
    verify_audio_dir = os.path.join(audio_directory, channel+'/'+'verify')

   #download the audio files
    if config['redownload_audio'] == 'True':
        initial_folders(audio_directory)
        initial_folders(impulse_directory)
        download_item_list(config['enrol_item_list'], speaker_data=True, channel=config['channel'],
                           outputdir=enrol_audio_dir)
        download_item_list(config['verify_item_list'], speaker_data=True, channel=config['channel'],
                           outputdir=verify_audio_dir)

    if config['enrol_treatment'] == 'convolve' or config['verify_treatment'] =="convolve":
        download_item_list(config['impulse_item_list'], speaker_data=False, channel='all',
                           outputdir=impulse_directory)

    print('start manipulating data')


    if config['recreate_enrol'] == "True":
       #read the config to determine whether recreate the enrolment audio is needed
        initial_folders(enrol_dir)
        audio_manipulation(enrol_audio_dir,'enrol',config)
        print("data for enrolment is ready")

    if config['recreate_verify'] == "True":
        # read the config to determine whether recreate the verification audio is needed
        initial_folders(verify_dir)
        audio_manipulation(verify_audio_dir,'verify',config)
        print("data for verification is ready")

if __name__ == '__main__':
    with open('experiment/test.json','r') as setting:
        config = json.load(setting)
    data_prep(config)

