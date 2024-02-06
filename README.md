# **CITIZEN** **REPORT**
****

### *This is an application to create reports regarding any failure that can happen in the city. User can submit form of report to let clerk evaluate it. The Clerk will then review the report and decide whether the application will be considered. To every report, clerks can make a post about progress of an issue.* ###

****

## **GETTING** **STARTED**

1. Download
   * You need to clone repository to your local destination
       ~~~python
            $ cd path/to/your/workspace
            https://github.com/SDA-wrzesien-2023-gr2/citizen-report.git

   * if you have established ssh connection to github you can use this link to clone repo:
       ~~~python
              git@github.com:SDA-wrzesien-2023-gr2/citizen-report.git
   
2. Make virtual environment (optional) 
    ~~~python
             $ python -m venv venv  
3. Install requirements
    ~~~python
             $ pip install -r requirements.txt
4. After this you can create your superuser

    `python manage.py createsuperuser`

5. Finally, you can run application

    `python manage.py runserver 0.0.0.0:8000`

## **USAGE**

