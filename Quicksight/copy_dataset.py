import boto3
import uuid


def copy_quicksight_dataset(aws_account_id, old_dataset_id, new_dataset_name, region='eu-west-1'):
    """
    Copies an existing QuickSight dataset into a new dataset with a unique dataset ID.

    Parameters:
    - aws_account_id (str): The AWS account ID where the dataset exists.
    - old_dataset_id (str): The ID of the existing dataset to copy.
    - new_dataset_name (str): The name of the new dataset.
    - region (str): The AWS region where QuickSight is hosted. Default is 'us-east-1'.

    Returns:
    - str: A message indicating whether the copy was successful or an error occurred.
    """
    # Generate a unique dataset ID for the new dataset
    new_dataset_id = f"{uuid.uuid4()}"

    # Create a QuickSight client
    client = boto3.client('quicksight', region_name=region)

    try:
        # Get the details of the existing dataset
        response = client.describe_data_set(
            AwsAccountId=aws_account_id,
            DataSetId=old_dataset_id
        )

        # Extract information from the existing dataset (for copying)
        old_dataset = response['DataSet']
        physical_table_map = old_dataset['PhysicalTableMap']
        # Check if permissions exist, and if not, default to an empty list
        permissions = old_dataset.get('Permissions', [])
        if not permissions:
            permissions = [
                {
                    'Principal': f'arn:aws:quicksight:{region}:{aws_account_id}:user/default/{aws_account_id}',  # Replace with a valid principal ARN
                    'Actions': ["quicksight:DescribeDataSet","quicksight:DescribeDataSetPermissions","quicksight:PassDataSet","quicksight:DescribeIngestion","quicksight:ListIngestions","quicksight:UpdateDataSet","quicksight:DeleteDataSet","quicksight:CreateIngestion","quicksight:CancelIngestion","quicksight:UpdateDataSetPermissions"]
                }
            ]
        import_mode = old_dataset['ImportMode']

        # Create the new dataset based on the old dataset's details
        response = client.create_data_set(
            AwsAccountId=aws_account_id,
            DataSetId=new_dataset_id,
            Name=new_dataset_name,
            PhysicalTableMap=physical_table_map,  # Copy table configurations
            Permissions=permissions,  # Copy the permissions
            ImportMode=import_mode  # Copy the import mode (SPICE or DIRECT_QUERY)
        )

        return f"Dataset copied successfully. New dataset ID: {new_dataset_id}"

    except client.exceptions.ResourceNotFoundException:
        return f"The dataset with ID {old_dataset_id} was not found."
    except Exception as e:
        return f"Error copying dataset: {e}"


# Example usage:
aws_account_id = 'xxxx'  # Replace with your AWS account ID
old_dataset_id = 'xxxx'  # Replace with the ID of the dataset you want to copy
new_dataset_name = 'Dev_People_Overview'  # Name for the new dataset

# Call the function
result = copy_quicksight_dataset(aws_account_id, old_dataset_id, new_dataset_name)
print(result)

