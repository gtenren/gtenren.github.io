# auraya_project
summer vocation project on Classify Audio Channels using Machine Learning

## Classify Audio Channels using Machine Learning

Voice biometrics use audio recordings to identify and verify the identity of individuals.  This  made more difficult by the variety of recording devices and transmission channels that are in use.  To improve system performance, we need examples of different kinds of noisy speech recordings.

In this project you will artificially create new channel specific audio from an existing database of clean audio. This might be done by mixing in noisy audio, by applying reverb and echo, or by filtering different frequencies. There are open source tools to assist with this, including open source noise databases.

Next, you will design and implement a computer program to classify audio as coming from one of the generated (or clean) audio databases. You may use the ArmorVox speech biometric product or an algorithm of your own choosing (or a combination).

Things to consider:

- Noisy audio should be created with a wide variety of noise samples so the classifier does not just pick regularities in the - noise.
- How much or how little of the audio is needed to make a good classification?
- How many different channels should be created? Should they match the characteristics of known channels such as mobile phones, hands-free, headsets, in-car, etc?
