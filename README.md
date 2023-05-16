# :school: Singapore Primary School Explorer
Access the web application [here](https://joanna-khek-sg-primary-school-explorer-about-ihz5yn.streamlit.app/)
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

View the web app here     
```http://localhost:8501/```


# Project Demo
There are four main sections to the web application.
* **1. School Type** - Compare between Government School, Government-Aided School and Government-Aided/ Autonomous School
* **2. School Nature** - Compare between Co-Ed, Girls and Boys School
* **3. CCA** - Explore CCA offered by schools
* **4. Subscription Rate** - Analyse the subscription rate of each phases

## 1. School Type

Compare between **Government School**, **Government-Aided School** and **Government-Aided/ Autonomous School**, to see their distribution in terms of GEP and Affiliations programmes

![School_Type](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/571d7d95-e920-46c7-9920-d683caf9f2e5)


## 2. School Nature

Compare between **Co-Ed**, **Boys School** and **Girls School**, to see their distribution in terms of GEP and Affiliations programmes

![School_Nature](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/b02061e0-a074-4e0b-b6a8-8097ed471307)


## 3. CCA

Find schools offering a particular CCA

![CCA_1](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/fb04275b-22a9-42bf-8abc-07689ecbe54e)

Explore most unique and common CCAs

![CCA_2](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/4fe537fe-46ab-43fa-ab92-8f73356302f2)

Explore schools with highest CCA points by School Type and School Nature

![CCA_3](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/6ad9f5b9-708a-4e3b-8747-829e4ec77d04)
![CCA_4](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/eb7e0d56-6ce7-49db-9bd1-14745f66be12)


## 4. Subscription Rate

Analyse your chances of successfully enrolling at each phase

![Subscription](https://github.com/Joanna-Khek/SG-Primary-School-Explorer/assets/53141849/f7e98208-f8dc-413f-942e-b2fda88e9588)


