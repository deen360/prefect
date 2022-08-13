

docs on from prefect deployment
https://docs.prefect.io/tutorials/deployments/

#you will be needing 4 terminals in the same folder 

have the two servers running in different terminals 

#using conda environment and the dependencies in environment.yml

mlflow
# mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root artifacts_local
 
available on http://127.0.0.1:5000


For this project, we use a local Prefect Orion server. Open a separate terminal and start the Prefect Orion server with the prefect orion start CLI command: 

 orion
# prefect orion start
http://127.0.0.1:4200


in this folder, i have 2 python files, paris.py and paris_flow_local.py
the paris.py file has a "main()" at the bottom, and when you run it as a python script, it logs the artifact and you can see it in themlflow ui,

check that both servers are running 

your can run the paris.py file with "python paris.py"


Then the same file paris_flow_local.py is deployed using prefect, with the "main()" at the buttom removed, and this is the same exact file as the paris.py, this paris_flow_local.py  is then run with the prefect, and prefect does not log the artifacts as the when running the file 
as a python script in the case of the python.py

steps used to deploy the prefectflow are explained below

check that both servers are running 

steps to deploy the prefect flow are as follows


prefect deployment build is the Prefect CLI command that enables you to prepare the settings for a deployment
## prefect deployment build ./paris_flow.py:main -n paris-housing-deployment -t Parisjob
     
# parameters: {'name':'Paris'}
Open the paris_flow.py-deployment.yaml file and add the parameter 

#  prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
Note the message to set PREFECT_API_URL so that you're coordinating flows with this API instance.
Open another terminal and run this command to set the API URL:

# these file should be present in the folder 
The flow code in paris_flow.py.py (mandatory)
The manifest paris_flow.py-manifest.json (this is not mandatory)
The deployment settings paris_flow.py-deployment.yaml (mandatory)

# prefect deployment apply main-deployment.yaml
Now use the prefect deployment apply command to create the deployment on the Prefect Orion server, specifying the name of the main-deployment.yaml file.

# prefect deployment ls
To demonstrate that your deployment exists, list all of the current deployments:

#  prefect deployment inspect main/paris-housing-deployment
to display details for a specific deployment.
# ------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Work queues and agent<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
.
# prefect agent start -t Parisjob
run the prefect agent start command, passing a -t test option that creates a work queue for test tags. Remember, we configured this same tag on the deployment at an earlier step.


Now that you've created the deployment, agent, and associated work queue, you can interact with it in multiple ways. For example, you can use the Prefect CLI to run a local flow run for the deployment

# prefect deployment run main/paris-housing-deployment


the flow will activate and you will see it in the ui but the artifacts will not be logged

the files in the db show in the registry 
