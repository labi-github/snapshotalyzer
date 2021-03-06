import boto3
import os
import click

os.environ['AWS_DEFAULT_REGION'] = "us-east-2"

session = boto3.Session(profile_name='WS-000G-role_DEVOPS')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', "Values":[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

def filter_volumes(project):
    volumes = []

    if project:
        filters = [{'Name':'tag:Project', "Values":[project]}]
        volumes = ec2.volumes.filter(Filters=filters)
    else:
        volumes = ec2.volumes.all()
    return volumes
    
@click.group()
def cli():
    """Snappy Manages snapshots"""

@cli.group("volumes")
def volumes():
    """Commands for volumes"""

@volumes.command('list')

@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")

def list_volumes(project):
    "List volumes for mathcing Instances"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
            v.id,
            i.id,
            v.state,
            str(v.size) + "GB",
            v.encrypted and "Encyrpted" or "Not Encrypted"
            )))
    return

@cli.group("snapshots")
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')

@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")

def list_snapshots(project):
    "List snapshots for mathcing Instances"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    i.id,
                    v.id,
                    s.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return

@cli.group("instances")
def instances():
    """Commands for instances"""

@instances.command('snapshot')
@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshot(project):
    "Create snapshot for EC2 Instances"

    instances = filter_instances(project)
    
    for i in instances:
        print("Stopping {0} ..".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot for volume {0} for instance {1}".format(v.id,i.id))
            v.create_snapshot(Description="Created by snapshot tool")

        print("Starting {0} ..".format(i.id))

        i.start()
        i.wait_until_running()
    print("Job completed!!!")

    return 

@instances.command('list')
@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    instances = filter_instances(project)
    
    for i in instances:
        tags = { t["Key"]: t["Value"] for t in i.tags or []}
        print(", ".join((
            i.id,
            i.instance_type,
            i.placement["AvailabilityZone"],
            i.state["Name"],
            i.public_dns_name,
            tags.get("Project","<no project>")
            )))
    return

@instances.command("stop")
@click.option("--project", default=None,
    help="Only instances for this project")
def stop_instances(project):
    "Stop EC2 Instances"
    instances = filter_instances(project)
    
    for i in instances:
        print("Stopping {0}".format(i.id))
        i.stop()
    
    return

@instances.command("start")
@click.option("--project", default=None,
    help="Only instances for this project")
def start_instances(project):
    "Start EC2 Instances"
    instances = filter_instances(project)
    
    for i in instances:
        print("Starting {0}".format(i.id))
        i.start()
    
    return

if __name__ == '__main__':
    cli()