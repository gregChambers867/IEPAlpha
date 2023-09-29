__author__ = 'gregChambers'

import boto.dynamodb2
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection

access_id = 'AKIAJVNPJVK5YMV5G27A'
secret_key = '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'

conn = DynamoDBConnection(aws_access_key_id=access_id, aws_secret_access_key=secret_key)

gimbaltable = Table('gimbalsighting')

gimbaltable.put_item()