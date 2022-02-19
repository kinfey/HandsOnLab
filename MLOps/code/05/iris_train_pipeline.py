# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
experiment_name = 'iris-training-auto'
upload_sample_data = False
register_data = False


# %%
#import required packages to build the pipeline artifact
from azureml.core import Experiment, Dataset
from azureml.core.compute import AmlCompute, ComputeTarget, DatabricksCompute
from azureml.core.datastore import Datastore
from azureml.core.runconfig import CondaDependencies, RunConfiguration
from azureml.data.data_reference import DataReference
from azureml.pipeline.core import Pipeline, PipelineData, PortDataReference
from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule
from azureml.pipeline.steps import PythonScriptStep, DatabricksStep
from azureml.core.model import Model



# %%
import os
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

svc_pr_password = os.environ.get("AZUREML_SECRET")
svc_pr = ServicePrincipalAuthentication(
    tenant_id=os.environ['AZUREML_TENANTID'],
    service_principal_id=os.environ['AZUREML_CLIENTID'],
    service_principal_password=svc_pr_password)

ws = Workspace(
    subscription_id=os.environ['AZUREML_SUBSCRIPTION'],
    resource_group=os.environ['AZUREML_RESOURCE_GROUP'],
    workspace_name=os.environ['AZUREML_WORKSPACE'],
    auth=svc_pr
    )

print("Found workspace {} at location {}".format(ws.name, ws.location))

# %%
from azureml.core.compute_target import ComputeTargetException

aml_compute_target = "cpu-cluster"
try:
    aml_compute = AmlCompute(ws, aml_compute_target)
    print("found existing compute target.")
except ComputeTargetException:
    print("creating new compute target")
    
    provisioning_config = AmlCompute.provisioning_configuration(vm_size = "STANDARD_D2_V2",
                                                                min_nodes = 0, 
                                                                max_nodes = 4)    
    aml_compute = ComputeTarget.create(ws, aml_compute_target, provisioning_config)
    aml_compute.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)
    
print("Aml Compute attached")


# %%
# Getting the default blob store (Datastore) for the Azure ML workspace
ds = ws.get_default_datastore()
print("Default Blobstore's name: {}".format(ds.name))
print("Default Blobstore's container name: {}".format(ds.container_name))

# %% [markdown]
# Upload and register the iris data to Azure ML to be used in pipelines

# %%
# upload iris data
if upload_sample_data:
    ds.upload_files(['sample_data.csv'], target_path='/data', overwrite=True, show_progress=True)


# %%
if register_data:
    # create target dataset 
    registereddata = Dataset.Tabular.from_delimited_files(ds.path('/data/sample_data.csv'))
    # NO TIMESTAMP COLUMN EXISTS
    # target = target.with_timestamp_columns('datetime')
    # register the target dataset
    registereddata = registereddata.register(ws, 'iris-data')


# %%
dataset = Dataset.get_by_name(ws,name='iris-data',version='latest')


# %%
dataset_ref = DataReference(
    datastore=ds,
    data_reference_name='irisdata',
    path_on_datastore="data/sample_data.csv")
print("DataReference object created")


model_output = PipelineData("model_output",datastore=ds)
print("PipelineData object created for models")

# %% [markdown]
# #### Create Pipeline Steps to be executed each time the pipeline runs

# %%
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE

# create a new runconfig object
run_config = RunConfiguration()

# enable Docker 
run_config.environment.docker.enabled = True
# set Docker base image to the default CPU-based image
run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE
# use conda_dependencies.yml to create a conda environment in the Docker image for execution
run_config.environment.python.user_managed_dependencies = False

# specify CondaDependencies obj
run_config.environment.python.conda_dependencies = CondaDependencies.create(
    pip_packages=['azureml-sdk','sklearn', 'scipy', 'numpy', 'pandas'],
    conda_packages=['matplotlib'])


# %%
# run the transformation script to produce the intermediate data that will go to the inferencing step
trainingScript = PythonScriptStep(
    script_name="iris_supervised_model.py", 
    inputs=[dataset_ref],
    outputs=[model_output],
    compute_target=aml_compute, 
    source_directory=".",
    runconfig=run_config
)
print("trainingStep created")


# %%
# run the transformation script to produce the intermediate data that will go to the inferencing step
registerModelStep = PythonScriptStep(
    script_name="register_model.py", 
    arguments=["--model_name", "iris_classifier_model","--training_step_name","iris_supervised_model.py"],
    inputs=[dataset_ref,model_output],
    #outputs=[model_output],
    compute_target=aml_compute, 
    source_directory=".",
    runconfig=run_config
)
print("registerModelStep created")

# %% [markdown]
# ### Using the output
# In the previous PythonScriptStep, a PipelineOutputFileDataset was created as an output and assigned to "models". Doc is here: https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.pipeline_output_dataset.pipelineoutputfiledataset?view=azure-ml-py

# %%
iris_train_pipeline = Pipeline(workspace=ws, steps=[trainingScript,registerModelStep])
print ("Pipeline is built")


# %%
exp = Experiment(ws,experiment_name)
exp.set_tags({'automl':'no','working':'no'})

pipeline_run1 = exp.submit(iris_train_pipeline)
print("Pipeline is submitted for execution")

pipeline_run1.wait_for_completion()

# %%
# TODO: retrieve results to determine if new pipeline should be published (old pipeline should also be disabled)
publish = False
if publish:
    published_pipeline = iris_train_pipeline.publish(name="iris_training_demo", description="Iris Classification Demo", continue_on_step_failure=True)
    published_pipeline


# %%
# Pipeline must be published first to be put on a schedule
schedule = False
if schedule:
    recurrence = ScheduleRecurrence(frequency="Day", interval=1, hours=[22], minutes=[30]) # Runs every day at 10:30pm

    schedule = Schedule.create(workspace=ws, name="iris_training_demo_schedule",
                            pipeline_id=published_pipeline.id, 
                            experiment_name='iris_training_demo_daily_schedule_run',
                            recurrence=recurrence,
                            wait_for_provisioning=True,
                            description="iris training demo daily Schedule Run")