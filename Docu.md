# I. Framing of the dataset
### 1. ER Diagram
<img width="797" height="752" alt="image" src="https://github.com/user-attachments/assets/c257a148-26ea-49ad-964f-29ae9e348f9f" />


### 2. Each Table With Column definition 
**courses.csv**
File contains the list of all available modules and their presentations. The columns are:

- code_module – code name of the module, which serves as the identifier.
- code_presentation – code name of the presentation. It consists of the year and “B” for the presentation starting in February and “J” for the presentation starting in October.
- length – length of the module-presentation in days.
The structure of B and J presentations may differ and therefore it is good practice to analyse the B and J presentations separately. Nevertheless, for some presentations the corresponding previous B/J presentation do not exist and therefore the J presentation must be used to inform the B presentation or vice versa. In the dataset this is the case of CCC, EEE and GGG modules.

**studentInfo.csv**
This file contains demographic information about the students together with their results. File contains the following columns:

- code_module – an identification code for a module on which the student is registered.
- code_presentation – the identification code of the presentation during which the student is registered on the module.
- id_student – a unique identification number for the student.
- gender – the student’s gender.
- region – identifies the geographic region, where the student lived while taking the module-presentation.
- highest_education – highest student education level on entry to the module presentation.
- imd_band – specifies the [Index of Multiple Depravation](https://en.wikipedia.org/wiki/Deprivation_index) band of the place where the student lived during the module-presentation.
- age_band – band of the student’s age.
- num_of_prev_attempts – the number times the student has attempted this module.
- studied_credits – the total number of credits for the modules the student is currently studying.
- disability – indicates whether the student has declared a disability.
- final_result – student’s final result in the module-presentation.
**studentRegistration.csv**
This file contains information about the time when the student registered for the module presentation. For students who unregistered the unregistered date is also recorded. File contains five columns:

- code_module – an identification code for a module.
- code_presentation – the identification code of the presentation.
- id_student – a unique identification number for the student.
- date_registration – the date of student’s registration on the module presentation, this is the number of days measured relative to the start of the module-presentation (e.g. the negative value -30 means that the student registered to module presentation 30 days before it started).
- date_unregistration – the student’s unregistered date from the module presentation, this is the number of days measured relative to the start of the module-presentation. Students, who completed the course have this field empty. Students who unregistered have Withdrawal as the value of the final_result column in the studentInfo.csv file.

**studentVle.csv**
The studentVle.csv file contains information about each student’s interactions with the materials in the VLE.
This file contains the following columns:

- code_module – an identification code for a module.
- code_presentation – the identification code of the module presentation.
- id_student – a unique identification number for the student.
- id_site – an identification number for the VLE material.
- date – the date of student’s interaction with the material measured as the number of days since the start of the module-presentation.
- sum_click – the number of times a student interacts with the material in that day.

**vle.csv**
The csv file contains information about the available materials in the VLE. Typically, these are html pages, pdf files, etc. Students have access to these materials online and their interactions with the materials are recorded.
The vle.csv file contains the following columns:

- id_site – an identification number of the material.
- code_module – an identification code for module.
- code_presentation – the identification code of presentation.
- activity_type – the role associated with the module material.
- week_from – the week from which the material is planned to be used.
- week_to – week until which the material is planned to be used.
### 3. Tables Used (and why)
- StudentInfo: Since it contains all the primary information, including but not limited to final_result,imd_band,age_band,gender,region
- StudentRegistration: As will be shown later, it was used to figure out individual that unregistered early or registered late
- Courses: Used to figure out module lengths, so as to figure out duration since latest activity
- StudentVle: Used to figure out activity trends based on clicks
- ~~Vle: Used to figure out ratio of where the activity of each student is focused~~ *Explained later why the table and its features were removed*  
### 4. Relation between tables


# II. Major observations


# III. Features Engineered
### 1. Mention all features engineered (With definitions)
### 2. Mention Why Features Were engineered a certain way
### 3. Mention which features were scrapped and why

# IV. ML Models 
### 1. Mention Which Were Used(tested)
### 2. Mention accuracy percentages
### 3. Mention Final Choice of ML model

# V. LLM Details
### 1. LLM Used and Details
### 2. Prompt Engineering Details
### 3. Effectiveness at Explaining 

# VI. Streamlit
### 1. Explain Mistakes made 
### 2. Explain basic understanding 
### 3. Explain Choices made
