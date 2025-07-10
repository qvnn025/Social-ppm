# LOCAL RUN GUIDE 
To run the project locally, and access the admin panel, use the credentials provided through the .env file in this branch. To also access the old sqlite database, the following changes in the project root [settings.py](https://github.com/qvnn025/Social-ppm/blob/master/User_project/settings.py) are required:
 * (line 16) change the **ENVIRONMENT** variable to 'development'
 * (line 105) change the **POSTGRES_LOCALLY** variable to 'False'
   
 > [!NOTE]
 > The POSTGRES_LOCALLY change is usually not strictly necessary.
