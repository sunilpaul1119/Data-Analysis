from textwrap import indent

import boto3
import json

from pandas.core.dtypes.cast import convert_dtypes

# Initialize the QuickSight client
client = boto3.client('quicksight')

# Your AWS account ID
aws_account_id = '463470983418'

# Function to list all shared folders
def list_shared_folders():
    try:
        # response = quicksight_client.list_folders(
        #     AwsAccountId=aws_account_id
        #     # Namespace='default'
        # )
        response = client.list_folders(
            AwsAccountId=aws_account_id,  # Your AWS Account ID
            # FolderType='ALL',  # You can filter by 'SHARED' or 'ALL'
            MaxResults=10  # Optional, for pagination
            # NextToken=None  # Optional, for pagination
        )

        for folder in response['FolderSummaryList']:
            folder_id = folder['FolderId']
            folder_name = folder['Name']
            folder_type = folder['FolderType']
            # parent_folderid = folder.get('ParentFolderId', None)
            print(f"Folder ID: {folder_id}")
            print(f"Folder Name: {folder_name}")
            print(f"Folder Type: {folder_type}")
            print("-----")

    except Exception as e:
        print(f"Error listing shared folders: {e}")

# import boto3

# Initialize a QuickSight client
# client = boto3.client('quicksight', region_name='us-east-1')  # Change to your AWS region

def list_datasets(aws_account_id, max_results=10, next_token=None):
    try:
        # List datasets in QuickSight
        if next_token:
            response = client.list_data_sets(
                AwsAccountId=aws_account_id,
                MaxResults=max_results,
                NextToken=next_token
            )
        else:
            response = client.list_data_sets(
                AwsAccountId=aws_account_id,
                MaxResults=max_results
            )

        # Print dataset details: ID, Name, and Status
        for dataset in response['DataSetSummaries']:
            dataset_id = dataset['DataSetId']
            dataset_name = dataset['Name']
            dataset_rls = dataset['RowLevelPermissionTagConfigurationApplied']
            # dataset_status = dataset['Status']

            # print(f"Dataset ID: {dataset_id}")
            # print(f"Dataset Name: {dataset_name}")
            # # print(f"Dataset Status: {dataset_status}")
            # print("-----")
            print(f"Dataset ID: {dataset_id} | Dataset Name: {dataset_name} | RLS: {dataset_rls}")

        # Check if there are more results (pagination)
        if 'NextToken' in response:
            print(f"More datasets available. Use NextToken: {response['NextToken']}")
            # You can call the function again with the NextToken to paginate
            list_datasets(aws_account_id, max_results, response['NextToken'])

    except Exception as e:
        print(f"Error listing datasets: {e}")


# Call the function to list datasets
list_datasets(aws_account_id, max_results=10)
# list_shared_folders()