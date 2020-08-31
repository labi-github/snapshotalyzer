# snapshotalyzer

Demo project to manage EC2 snapshots

## About

Demo using boto3

## Configuration
Snappy uses the configuration created by the AWS click

'awsconnect --role abcd'

##Running
'pipenv run python snappy/snappy.py <ACTION> <Subactionb> <--project=ProjectName>'

*Action* is instances, volumes and snapshots
*Subaction* - depends of the chosen command 
*project* is Optional
