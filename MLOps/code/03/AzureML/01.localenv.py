#%%
from azureml.core import Workspace

ws = Workspace.create(name='azuremlhack', # provide a name for your workspace
                      subscription_id='901e11c6-42ed-4fcc-875a-6bd77390af5b', # provide your subscription ID
                      resource_group='kinfeymldemogroup', # provide a resource group name
                      create_resource_group=True,
                      location='eastasia') # For example: 'westeurope' or 'eastus2' or 'westus2' or 'southeastasia'.

# write out the workspace details to a configuration file: .azureml/config.json
ws.write_config(path='.azureml')
# %%
