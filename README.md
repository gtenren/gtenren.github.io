## Welcome to Gary's Page

Hi, there. I am Gary, currently a master of data science student in Macquarie University.

This is my github repository of my previous projects.

### Some background about me
Before doing my master degree, I am an eCommerce specialist/data analyst in Hong Kong and China for 6 years. My role focused on deriving insight from data and help the company to make revenue through the web, transaction and financial data. I used Google Analytics, Google Ads, Google Data Studio, Advance Excel techniques and Tableau. Apart from data analysis, I also worked on other digital marketing such as PPC, SEO and web development such as HTML, CSS and javascript.

I started my master degree in Feb 2018 and expect to finish in 2020. The master degree has a combined of statistic and computing units.

Statistic courses provided a fundamental of statistical learning generalised linear model, multivariate analysis, data mining and some modern computational method of statistics. I have also did external course during the 2019 AMSI summer school on mathematical method of machine learning and optimisation theory. I used R in all of my statistic courses.

Computer courses provide the knowledge to implement machine learning as well as concept in web and data interchange. Courses I took included Data Science, Web Technology, big data technology, Enterprise Application Integration and Project Management. I was a high distinction student in Data Science class. I have also involved in a research internship with a local voice recognition company in 2019 Summer.

The following are some project I previously done.

### mq_data_science_coursework
In the data science course, we completed 3 short projects. This folder contains all the related jupyter notebooks and the code.

- **Portfolio 1** : Analysis on GPS data of a biker cycling on the same route for 8 different times
- **Portfolio 2** : Re-produce a paper on predicting the energy usage of a house based on IoT measurements of temperature and humidity and weather observations (Luis M. Candanedo, Véronique Feldheim, Dominique Deramaix. Energy and Buildings, Volume 140, 1 April 2017, Pages 81-97, ISSN 0378-7788, [http://dx.doi.org/10.1016/j.enbuild.2017.01.083])
- **Portfolio 3** : Classifying if the client will subscribe a term deposit in a telemarketing campaign (S. Moro, P. Cortez and P. Rita. A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems, Elsevier, 62:22-31, June 2014. [http://media.salford-systems.com/video/tutorial/2015/targeted_marketing.pdf])

### speed_dating_experiment_classifier

This project is an attempt to classify a pair of speed dating participants if they will consider their partner as a "match". 

The major challenge of this project is data preprocessing. The original dataset is a combine of three surveys, the participant's profile and their partner's profile. This created huge amount of missing values and duplicates observations. To takle this problem, I have remapped the data based on how different the participant and thier partner is.

### voice_recognition_internship

This project is a part of a vocational internship I did in 2019 Summer sponsored by a local technology business. My role was experimenting how the voice recognition engine performed when different noises are mixed to the audio of the speaker's speech.

The project can be briefly breakdown into 4 stages. 

1. Downloading a collection of audios of speakers' reading a story from an online database platform, Alveo. 
2. Generating different kinds of noise with python and mix them with the speaker audio with my other set of code. This include resampling the audio, controlling how loud the noise should be and covolving effect to the audio. THe code.
3. I work with the REST API to enrol and verify the audio I created as a voice print. Score from the system was then collected and written to csv files.
4. I reported the result with a notebook that compared the results from different treatments on the audio.
5. Due to the need of stronger computational power the code is run on a AWS EC2.

### Legal Citation Classification

This project aim to extend an prior research paper on legal citation classification with different perspectives and deep learning method. 

In data preprocessin, I extracted features from the text and convert them into word vectors. As the data are inbalanced, resampling technique is also applied to counter the issue arised.

In conventional machine learning technique, I built models based on different features and algorithms. Algoritms such as Decision tree, KNN, SVM is used. I have also applied ensemble technique, voting, to combine weaker models into a stronger one. 

For deep learning model, I used a multichannel convolutional neural network which takes different number of words as a token in the learning.  

### EY Data Science Challenge

The challenge is about predicting how many device will enter the target city area given their previous trajectory. 

In this project, I applied multiple instance machine learning technique such as bagging, single instance learning etc. I have also applied different ensemble machine learning technique to combine weaker models to a stronger one.