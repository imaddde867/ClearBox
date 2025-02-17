from aws_cdk import (
    Stack,
    aws_amazonmq as mq,
    aws_ec2 as ec2, # For creating our Virtual Private Cloud (VPC) where our database will live
    aws_rds as rds, # For setting up our PostgreSQL database
    aws_iot as iot, # For our MQTT messaging system
    aws_cognito as cognito, # For user authentication
    aws_secretsmanager as secretsmanager, # For securely storing database credentials
    core
)

class ChatSystemStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC for RDS
        vpc = ec2.Vpc(
            self, "ChatSystemVPC",
            max_azs=2,  # We'll use 2 availability zones for high availability
            nat_gateways=1  # Adding a NAT Gateway for private subnets
        )

        db_security_group = ec2.SecurityGroup(
            self, "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for Chat System database",
            allow_all_outbound=True # Our database can send traffic anywhere 
        )

        db_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(5432),
            description="Allow PostgreSQL inbound from VPC"
        )

        #setting up the database 
        database = rds.DatabaseInstance(
            self, "ChatDatabase",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_14
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MEDIUM,
            ),
            vpc=vpc,  # Added missing VPC configuration
            security_groups=[db_security_group],  # Added security group configuration
            multi_az=True,  # Enable high availability by creating a standby copy in another AZ for failover
            allocated_storage=10, #starts with 10 Gb of storage
            max_allocated_storage=20,  # Enable storage autoscaling up to 20 Gbs if needed
        )

        # Creating the Amazon MQ Broker using RabbitMQ
        broker = mq.CfnBroker(self, "ClearBox",
            auto_minor_version_upgrade=True,
            broker_name="ClearBox",
            deployment_mode="SINGLE_INSTANCE",
            engine_type="RABBITMQ",
            engine_version="3.13",
            host_instance_type="mq.t3.micro",
            publicly_accessible=True,
            users=[{
                "consoleAccess": True,
                "username": "admin",
                # Password stored in Secrets Manager instead of hardcoding
                "password": secretsmanager.Secret(self, "BrokerPassword").secret_value
            }],
            logs={"general": True},
            subnetIds=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnet_ids,
        )

        # Using core.CfnOutput for proper output handling of broker's endpoints
        core.CfnOutput(self, "BrokerEndpoint",
            value=broker.attr_amqp_endpoints[0],
            description="RabbitMQ broker endpoint"
        )