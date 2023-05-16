# :school: Singapore Primary School Explorer
Access the web application [here](https://joanna-khek-sg-primary-school-explorer-about-ihz5yn.streamlit.app/)    

![2](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/9d95017d-5521-4f1e-beb0-48913c2ba88d)


# Project Description
Choosing a primary school for your child can be a daunting task.
* What phase am I eligble for?
* What are the chances of getting into this particular school?
* What are the schools with this particular CCA?
* Should I enroll my child in a Co-ed or Boys/Girls school?

In an attempt to answer all those questions, I have created a web application to assist parents in selecting a primary school for their children.

# Running docker container
Clone the repository     
```git clone https://github.com/Joanna-Khek/SG-Primary-School-Explorer```   

Build the docker image    
```docker build -t pri-school-app:latest .```   

Run the docker image    
```docker run -p 8501:8501 pri-school-app:latest```

View the web app using this url    
```http://localhost:8501/```


# Project Demo
There are four main sections to the web application.
* **1. School Type** - Compare between Government School, Government-Aided School and Government-Aided/ Autonomous School
* **2. School Nature** - Compare between Co-Ed, Girls and Boys School
* **3. CCA** - Explore CCA offered by schools
* **4. Subscription Rate** - Analyse the subscription rate of each phases

## 1. School Type

Compare between **Government School**, **Government-Aided School** and **Government-Aided/ Autonomous School**, to see their distribution in terms of GEP and Affiliations programmes

![School-Type](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/6d1b31f1-4aae-4c0b-a85d-db3cc0fb12d4)


## 2. School Nature

Compare between **Co-Ed**, **Boys School** and **Girls School**, to see their distribution in terms of GEP and Affiliations programmes

![School-Nature](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/3016a15f-17ed-475a-9802-acea7275cc76)


## 3. CCA

Find schools offering a particular CCA

![CCA-1](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/642f3729-4461-4c85-adf8-b5c501d1eb3e)

Explore most unique and common CCAs

![CCA-2](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/6fdf2c74-60c9-4526-be1b-2d8b851d51d1)


Explore schools with highest CCA points by School Type and School Nature
![CCA-3](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/9dc6eb7d-683d-4a15-85af-beb9781bebe5)
![CCA-4](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/60d62d41-e81e-4cf7-9305-c8a44cb5aa82)


## 4. Subscription Rate

Analyse your chances of successfully enrolling at each phase

![Subscription](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/39e1fee9-1e6f-46cd-8548-7424e0687377)



