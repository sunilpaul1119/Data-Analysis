import boto3


def delete_quicksight_dataset(aws_account_id, dataset_id, region='eu-west-1'):
    """
    Deletes a QuickSight dataset.

    Parameters:
    - aws_account_id (str): The AWS account ID where the dataset resides.
    - dataset_id (str): The ID of the QuickSight dataset to delete.
    - region (str): The AWS region where QuickSight is hosted. Default is 'us-east-1'.

    Returns:
    - str: A message indicating whether the deletion was successful or an error occurred.
    """
    # Create a QuickSight client
    client = boto3.client('quicksight', region_name=region)

    try:
        # Attempt to delete the dataset
        response = client.delete_data_set(
            AwsAccountId=aws_account_id,
            DataSetId=dataset_id
        )
        return f"Dataset {dataset_id} deleted successfully."

    except client.exceptions.ResourceNotFoundException:
        return f"Dataset {dataset_id} not found."

    except Exception as e:
        return f"Error deleting dataset: {e}"


# Example usage:
aws_account_id = '463470983418'  # Replace with your AWS account ID
dataset_id = 'bc77bcb9-7ade-48f3-9b35-68f1aaf3da81'  # Replace with the ID of the dataset you want to delete

# Call the function
result = delete_quicksight_dataset(aws_account_id, dataset_id)
print(result)