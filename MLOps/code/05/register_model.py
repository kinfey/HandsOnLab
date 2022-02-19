from azureml.core import Run, Workspace, Experiment, Model, Dataset
from azureml.core.resource_configuration import ResourceConfiguration
import sklearn
import sys
import os


print("...getting run context, experiment, and workspace")
run = Run.get_context()
if (run.id.startswith('OfflineRun')):
    os.environ['AZUREML_DATAREFERENCE_irisdata'] = '.\sample_data.csv'
    os.environ['AZUREML_DATAREFERENCE_model_output'] = '.\model_output'
    ws = Workspace.from_config()
    model_name = 'iris_classifier_model'
    training_step_name = 'iris_supervised_model.py'

    expirement_name = "your_experiment_name"
    parentrunid = "previous_pipeline_runid_for_your_experiment"
    exp = Experiment(ws,expirement_name)
    parentrun = Run(exp,parentrunid)
    # sys.exit("Currently this model registration script can only run in "+ 
    #     "context of a parent pipeline.")
else:
    ws = run.experiment.workspace
    print("...getting arguments (model_name, training_step_name)")
    model_name = sys.argv[2]
    training_step_name = sys.argv[4] 
    parentrun = run.parent


print("model_name:",model_name)
print("training_step_name:",training_step_name)

# The required metrics should be present in the parent run, the below condition has been included
# to show an alternative approach by getting those metrics from the prior training step directly.
training_run_id = None
tagsdict = parentrun.get_tags()
if (tagsdict.get("best_model")) != None:
    model_type = tagsdict['best_model']
    model_accuracy = float(tagsdict['accuracy'])
    training_run_id = parentrun.id
else:
    for step in parentrun.get_children():
        print("Outputs of step " + step.name)
        if step.name == training_step_name:
                tagsdict = step.get_tags()
                model_type = tagsdict['best_model']
                model_accuracy = float(tagsdict['accuracy'])
                training_run_id = step.id    

if (training_run_id == None):
    sys.exit("Failed to retrieve model information from run.")

# A sample dataset can be included with the registered model for reference. 
# To get the dataset, the data reference has to be a cloud storage path, therefore a local run won't work.
mntpath = os.environ['AZUREML_DATAREFERENCE_irisdata']

# dataset = None
# if not(run.id.startswith('OfflineRun')):
#     # get last section of the mnt location starting after '/workspaceblobstore' which is the blob storage location
#     # print
#     blobstoragepath = mntpath.rsplit('/workspaceblobstore',maxsplit=1)[1]
#     dataset = Dataset.Tabular.from_delimited_files(path=[(ws.get_default_datastore(), blobstoragepath)])

# getting the model output path (the path to the model.pkl file) from the previous step's output. 
model_output = os.environ['AZUREML_DATAREFERENCE_model_output']
print("model path",model_output)
print("files in model path",os.listdir(path=model_output))

# will register the model to the parent which encapsulates all the steps 
# if model already exists, error will be thrown, ignore.
try:
    # to register a model to a run, the file has to be uploaded to that run first.
    parentrun.upload_file('model.pkl',model_output+'/model.pkl')
except:
    None

# model_path is the local path of the parentrun model file (see upload_file action above)
model_path = "model.pkl"
print("...working directory")
print(os.listdir(path='.'))

# if the model has been previously registered, retrieve the accuracy. This will be used to determine if the new model
# should be registered or if the old one should be kept as the latest version.
try:
    model = Model(ws, model_name)
    acc_to_beat = float(model.properties["accuracy"])
except:
    acc_to_beat = 0

# comment out the below line to only register the model if the new accuracy score is better
acc_to_beat = 0

print("accuracy to beat",acc_to_beat)
if model_accuracy > acc_to_beat:
    print("model is better, registering")

    # Registering the model to the parent run (the pipeline). The entire pipeline encapsulates the training process.
    model = parentrun.register_model(
                       model_name=model_name,                # Name of the registered model in your workspace.
                       model_path=model_path,  # Local file to upload and register as a model.
                       model_framework=Model.Framework.SCIKITLEARN,  # Framework used to create the model.
                       model_framework_version=sklearn.__version__,  # Version of scikit-learn used to create the model.
                    #    sample_input_dataset=dataset,
                       resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=0.5),
                       description='basic iris classification',
                       tags={'quality': 'good', 'type': 'classification'})
    model.add_properties({"accuracy":model_accuracy,"model_type":model_type})
    model.add_tags({"accuracy":model_accuracy,"model_type":model_type})

    print(model)
    # Azure ML UI doesn't list the datasets so the print statement below does indeed show the dataset was included.
    print(model.sample_input_dataset)
else:
    print("model didn't perform better, not registering")