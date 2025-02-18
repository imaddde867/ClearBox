from aws_cdk import (
    aws_amazonmq as mq,
    aws_ec2 as ec2,  # For creating our Virtual Private Cloud (VPC) where our database will live
    aws_rds as rds,  # For setting up our PostgreSQL database
    aws_iot as iot,  # For our MQTT messaging system
    aws_cognito as cognito,  # For user authentication
    aws_secretsmanager as secretsmanager,  # For securely storing database credentials
    core
)
from aws_cdk.core import Stack

class ChatSystemStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC for RDS
        vpc = ec2.Vpc(
            self, "ChatSystemVPC",
            max_azs=2,  # We'll use 2 availability zones for high availability
            nat_gateways=1,  # Adding a NAT Gateway for private subnets
        )

        db_security_group = ec2.SecurityGroup(
            self, "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for Chat System database",
            allow_all_outbound=False  # More secure: only allow necessary outbound traffic
        )

        db_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(5432),
            description="Allow PostgreSQL inbound from VPC"
        )

        # Create database credentials and store in Secrets Manager
        db_credentials = secretsmanager.Secret(
            self, "DatabaseCredentials",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "admin", "password": "${password}"}',
                generate_string_key="password",
                exclude_characters=r'/@"\ '
            )
        )

        # Create the database instance with credentials
        database = rds.DatabaseInstance(
            self, "ChatDatabase",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_14
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MEDIUM
            ),
            vpc=vpc,
            security_groups=[db_security_group],
            multi_az=True,  # Enable high availability
            allocated_storage=10,  # Starts with 10 GB of storage
            max_allocated_storage=20,  # Enable storage autoscaling up to 20 GB
            database_name="ChatDatabase",
            credentials=rds.Credentials.from_secret(db_credentials),
            port=5432
        )

        # Output the database endpoint
        core.CfnOutput(self, "DatabaseEndpoint",
            value=database.instance_endpoint.hostname,
            description="Database endpoint"
        )

        broker_credentials = secretsmanager.Secret(
            self, "BrokerCredentials",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "admin", "password": "${password}"}',
                generate_string_key="password",
                exclude_characters=r'/@"\ '
            )
        )

        # Output the secret ARN (for retrieving credentials)
        core.CfnOutput(self, "DatabaseCredentialsArn",
            value=db_credentials.secret_arn,
            description="Database credentials secret ARN"
        )

        # Creating the Amazon MQ Broker using RabbitMQ
        broker = mq.CfnBroker(self, "ClearBox",
            auto_minor_version_upgrade=True,
            broker_name="ClearBox",
            deployment_mode="SINGLE_INSTANCE",
            engine_type="RABBITMQ",
            engine_version="3.13.7",
            host_instance_type="mq.t3.micro",
            publicly_accessible=True,
            users=[{
                "consoleAccess": True,
                "username": "admin",
                "password": broker_credentials.secret_value_from_json("password").unsafe_unwrap()
            }],
            logs={"general": True},
            subnetIds=vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnet_ids,
        )

        # Using core.CfnOutput for proper output handling of broker's endpoints
        core.CfnOutput(self, "BrokerEndpoint",
            value=broker.attr_amqp_endpoints[0],
            description="RabbitMQ broker endpoint"
        )
        # output for the broker credentials ARN
        core.CfnOutput(self, "BrokerCredentialsArn",
            value=broker_credentials.secret_arn,
            description="Broker credentials secret ARN"
        )