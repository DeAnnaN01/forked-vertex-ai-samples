# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Automated Vertex AI resource cleanup for python-docs-samples-test
'''

from google.cloud import aiplatform
from google.cloud import bigquery
import time
import datetime

PROJECT_ID = "python-docs-samples-tests"

REGION = "us-central1"
aiplatform.init(project=PROJECT_ID, location=REGION)

now = datetime.datetime.now()

def date_delete(day):
    if now.day > 2:
        if day < now.day - 2:
            return True
    else:
        if day < 31 - now.day:
            return True
    return True

# delete datasets
for dstype in [aiplatform.ImageDataset, aiplatform.TextDataset, aiplatform.VideoDataset, aiplatform.TimeSeriesDataset]:
    datasets = dstype.list()
    for dataset in datasets:
        if not dataset.display_name.startswith("perm"):
            if date_delete(dataset.create_time.day):
                dataset.delete()
                
# delete feature store
fss = aiplatform.Featurestore.list()
for fs in fss:
    if not fs.display_name.startswith("perm"):
        if date_delete(fs.create_time.day):
            fs.delete(force=True)
            
# delete pipelines
jobs = aiplatform.PipelineJob.list()
print(len(jobs))

for job in jobs:
    if not job.display_name.startswith("perm"):
        if date_delete(job.create_time.day):
            try:
                job.delete()
            except Exception as e:
                 print(e)
            time.sleep(1)
                
# delete AutoML training jobs
jobs = aiplatform.PipelineJob.list()
print(len(jobs))

for job in jobs:
    if not job.display_name.startswith("perm"):
        if date_delete(job.create_time.day):
            try:
                job.delete()
            except Exception as e:
                 print(e)
            time.sleep(1)
            
# delete custom training jobs
for trtype in [ aiplatform.CustomContainerTrainingJob, 
                aiplatform.CustomJob,
                aiplatform.CustomPythonPackageTrainingJob,
                aiplatform.CustomTrainingJob
              ]:
    jobs = trtype.list()
    for job in jobs:
        if not job.display_name.startswith("perm"):   
            if date_delete(job.create_time.day):
                try:
                    job.delete()
                except Exception as e:
                    print(e)
                time.sleep(1)
                
# Delete hyperparameter tuning job
for job in aiplatform.HyperparameterTuningJob.list():
    if not job.display_name.startswith("perm"):       
        if date_delete(job.create_time.day):
            try:
                job.delete()
            except Exception as e:
                print(e)
            time.sleep(1)
            
# Delete experiments
for experiment in aiplatform.Experiment.list():
    if not experiment.name.startswith("perm"):
        #if date_delete(experiment.create_time.day):
        try:
            experiment.delete()
        except Exception as e:
            print(e)
        time.sleep(1)
        
# Delete batch prediction jobs
for job in aiplatform.BatchPredictionJob.list():
    if not job.display_name.startswith("perm"):
        if date_delete(job.create_time.day):
            try:
                job.delete()
            except Exception as e:
                print(e)
            time.sleep(1)
            
# Delete endpoints
for endpoint in aiplatform.Endpoint.list():
     if not endpoint.display_name.startswith("perm"):
        if date_delete(endpoint.create_time.day):
            try:
                endpoint.undeploy_all()
                endpoint.delete()
            except Exception as e:
                print(e)
            time.sleep(1)
            
for endpoint in aiplatform.PrivateEndpoint.list():
     if not endpoint.display_name.startswith("perm"):      
        if date_delete(endpoint.create_time.day):
            try:
                endpoint.undeploy_all()
                endpoint.delete()
            except Exception as e:
                print(e)
            time.sleep(1)
            
# Delete Models
for model in aiplatform.Model.list():
     if not model.display_name.startswith("perm"):    
        if date_delete(model.create_time.day):
            try:
                model.delete()
            except Exception as e:
                print(e)
            time.sleep(1)
