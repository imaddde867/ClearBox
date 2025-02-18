'''
# Amazon MQ Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_amazonmq as amazonmq
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AmazonMQ construct libraries](https://constructs.dev/search?q=amazonmq)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AmazonMQ resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AmazonMQ.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AmazonMQ](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AmazonMQ.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnBroker(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amazonmq.CfnBroker",
):
    '''A CloudFormation ``AWS::AmazonMQ::Broker``.

    A *broker* is a message broker environment running on Amazon MQ . It is the basic building block of Amazon MQ .

    The ``AWS::AmazonMQ::Broker`` resource lets you create Amazon MQ for ActiveMQ and Amazon MQ for RabbitMQ brokers, add configuration changes or modify users for a speified ActiveMQ broker, return information about the specified broker, and delete the broker. For more information, see `How Amazon MQ works <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/amazon-mq-how-it-works.html>`_ in the *Amazon MQ Developer Guide* .

    - ``ec2:CreateNetworkInterface``

    This permission is required to allow Amazon MQ to create an elastic network interface (ENI) on behalf of your account.

    - ``ec2:CreateNetworkInterfacePermission``

    This permission is required to attach the ENI to the broker instance.

    - ``ec2:DeleteNetworkInterface``
    - ``ec2:DeleteNetworkInterfacePermission``
    - ``ec2:DetachNetworkInterface``
    - ``ec2:DescribeInternetGateways``
    - ``ec2:DescribeNetworkInterfaces``
    - ``ec2:DescribeNetworkInterfacePermissions``
    - ``ec2:DescribeRouteTables``
    - ``ec2:DescribeSecurityGroups``
    - ``ec2:DescribeSubnets``
    - ``ec2:DescribeVpcs``

    :cloudformationResource: AWS::AmazonMQ::Broker
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amazonmq as amazonmq
        
        cfn_broker = amazonmq.CfnBroker(self, "MyCfnBroker",
            auto_minor_version_upgrade=False,
            broker_name="brokerName",
            deployment_mode="deploymentMode",
            engine_type="engineType",
            engine_version="engineVersion",
            host_instance_type="hostInstanceType",
            publicly_accessible=False,
            users=[amazonmq.CfnBroker.UserProperty(
                password="password",
                username="username",
        
                # the properties below are optional
                console_access=False,
                groups=["groups"]
            )],
        
            # the properties below are optional
            authentication_strategy="authenticationStrategy",
            configuration=amazonmq.CfnBroker.ConfigurationIdProperty(
                id="id",
                revision=123
            ),
            encryption_options=amazonmq.CfnBroker.EncryptionOptionsProperty(
                use_aws_owned_key=False,
        
                # the properties below are optional
                kms_key_id="kmsKeyId"
            ),
            ldap_server_metadata=amazonmq.CfnBroker.LdapServerMetadataProperty(
                hosts=["hosts"],
                role_base="roleBase",
                role_search_matching="roleSearchMatching",
                service_account_password="serviceAccountPassword",
                service_account_username="serviceAccountUsername",
                user_base="userBase",
                user_search_matching="userSearchMatching",
        
                # the properties below are optional
                role_name="roleName",
                role_search_subtree=False,
                user_role_name="userRoleName",
                user_search_subtree=False
            ),
            logs=amazonmq.CfnBroker.LogListProperty(
                audit=False,
                general=False
            ),
            maintenance_window_start_time=amazonmq.CfnBroker.MaintenanceWindowProperty(
                day_of_week="dayOfWeek",
                time_of_day="timeOfDay",
                time_zone="timeZone"
            ),
            security_groups=["securityGroups"],
            storage_type="storageType",
            subnet_ids=["subnetIds"],
            tags=[amazonmq.CfnBroker.TagsEntryProperty(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        auto_minor_version_upgrade: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        broker_name: builtins.str,
        deployment_mode: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        host_instance_type: builtins.str,
        publicly_accessible: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        users: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBroker.UserProperty", typing.Dict[builtins.str, typing.Any]]]]],
        authentication_strategy: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBroker.ConfigurationIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBroker.EncryptionOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ldap_server_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBroker.LdapServerMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBroker.LogListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maintenance_window_start_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBroker.MaintenanceWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnBroker.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AmazonMQ::Broker``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_minor_version_upgrade: Enables automatic upgrades to new minor versions for brokers, as new broker engine versions are released and supported by Amazon MQ. Automatic upgrades occur during the scheduled maintenance window of the broker or after a manual broker reboot.
        :param broker_name: The name of the broker. This value must be unique in your AWS account , 1-50 characters long, must contain only letters, numbers, dashes, and underscores, and must not contain white spaces, brackets, wildcard characters, or special characters. .. epigraph:: Do not add personally identifiable information (PII) or other confidential or sensitive information in broker names. Broker names are accessible to other AWS services, including C CloudWatch Logs . Broker names are not intended to be used for private or sensitive data.
        :param deployment_mode: The deployment mode of the broker. Available values:. - ``SINGLE_INSTANCE`` - ``ACTIVE_STANDBY_MULTI_AZ`` - ``CLUSTER_MULTI_AZ``
        :param engine_type: The type of broker engine. Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .
        :param engine_version: The version of the broker engine. For a list of supported engine versions, see `Engine <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_ in the *Amazon MQ Developer Guide* .
        :param host_instance_type: The broker's instance type.
        :param publicly_accessible: Enables connections from applications outside of the VPC that hosts the broker's subnets.
        :param users: The list of broker users (persons or applications) who can access queues and topics. For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent RabbitMQ users are created by via the RabbitMQ web console or by using the RabbitMQ management API.
        :param authentication_strategy: Optional. The authentication strategy used to secure the broker. The default is ``SIMPLE`` .
        :param configuration: A list of information about the configuration. Does not apply to RabbitMQ brokers.
        :param encryption_options: Encryption options for the broker. Does not apply to RabbitMQ brokers.
        :param ldap_server_metadata: Optional. The metadata of the LDAP server used to authenticate and authorize connections to the broker. Does not apply to RabbitMQ brokers.
        :param logs: Enables Amazon CloudWatch logging for brokers.
        :param maintenance_window_start_time: The scheduled time period relative to UTC during which Amazon MQ begins to apply pending updates or patches to the broker.
        :param security_groups: The list of rules (1 minimum, 125 maximum) that authorize connections to brokers.
        :param storage_type: The broker's storage type.
        :param subnet_ids: The list of groups that define which subnets and IP ranges the broker can use from different Availability Zones. If you specify more than one subnet, the subnets must be in different Availability Zones. Amazon MQ will not be able to create VPC endpoints for your broker with multiple subnets in the same Availability Zone. A SINGLE_INSTANCE deployment requires one subnet (for example, the default subnet). An ACTIVE_STANDBY_MULTI_AZ deployment (ACTIVEMQ) requires two subnets. A CLUSTER_MULTI_AZ deployment (RABBITMQ) has no subnet requirements when deployed with public accessibility, deployment without public accessibility requires at least one subnet. .. epigraph:: If you specify subnets in a shared VPC for a RabbitMQ broker, the associated VPC to which the specified subnets belong must be owned by your AWS account . Amazon MQ will not be able to create VPC enpoints in VPCs that are not owned by your AWS account .
        :param tags: An array of key-value pairs. For more information, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the *Billing and Cost Management User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27019b0b679211473fc3b3ec320c3dd0026020438314751341ae1c5a1f880409)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBrokerProps(
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            broker_name=broker_name,
            deployment_mode=deployment_mode,
            engine_type=engine_type,
            engine_version=engine_version,
            host_instance_type=host_instance_type,
            publicly_accessible=publicly_accessible,
            users=users,
            authentication_strategy=authentication_strategy,
            configuration=configuration,
            encryption_options=encryption_options,
            ldap_server_metadata=ldap_server_metadata,
            logs=logs,
            maintenance_window_start_time=maintenance_window_start_time,
            security_groups=security_groups,
            storage_type=storage_type,
            subnet_ids=subnet_ids,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7b61b1bb0fd6820a9d42b1f797b5b264556c53486d0c9c7393577aa36e1983)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae92737f22dda6dddcd1108965f8032ad422462654ccd564ba7ef9d8e826cb08)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAmqpEndpoints")
    def attr_amqp_endpoints(self) -> typing.List[builtins.str]:
        '''The AMQP endpoints of each broker instance as a list of strings.

        ``amqp+ssl://b-4aada85d-a80c-4be0-9d30-e344a01b921e-1.mq.eu-central-amazonaws.com:5671``

        :cloudformationAttribute: AmqpEndpoints
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrAmqpEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon MQ broker.

        ``arn:aws:mq:us-east-2:123456789012:broker:MyBroker:b-1234a5b6-78cd-901e-2fgh-3i45j6k178l9``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationId")
    def attr_configuration_id(self) -> builtins.str:
        '''The unique ID that Amazon MQ generates for the configuration.

        ``c-1234a5b6-78cd-901e-2fgh-3i45j6k178l9``

        :cloudformationAttribute: ConfigurationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationId"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationRevision")
    def attr_configuration_revision(self) -> jsii.Number:
        '''The revision number of the configuration.

        ``1``

        :cloudformationAttribute: ConfigurationRevision
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrConfigurationRevision"))

    @builtins.property
    @jsii.member(jsii_name="attrIpAddresses")
    def attr_ip_addresses(self) -> typing.List[builtins.str]:
        '''The IP addresses of each broker instance as a list of strings. Does not apply to RabbitMQ brokers.

        ``['198.51.100.2', '203.0.113.9']``

        :cloudformationAttribute: IpAddresses
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="attrMqttEndpoints")
    def attr_mqtt_endpoints(self) -> typing.List[builtins.str]:
        '''The MQTT endpoints of each broker instance as a list of strings.

        ``mqtt+ssl://b-4aada85d-a80c-4be0-9d30-e344a01b921e-1.mq.eu-central-amazonaws.com:8883``

        :cloudformationAttribute: MqttEndpoints
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrMqttEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="attrOpenWireEndpoints")
    def attr_open_wire_endpoints(self) -> typing.List[builtins.str]:
        '''The OpenWire endpoints of each broker instance as a list of strings.

        ``ssl://b-4aada85d-a80c-4be0-9d30-e344a01b921e-1.mq.eu-central-amazonaws.com:61617``

        :cloudformationAttribute: OpenWireEndpoints
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrOpenWireEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="attrStompEndpoints")
    def attr_stomp_endpoints(self) -> typing.List[builtins.str]:
        '''The STOMP endpoints of each broker instance as a list of strings.

        ``stomp+ssl://b-4aada85d-a80c-4be0-9d30-e344a01b921e-1.mq.eu-central-amazonaws.com:61614``

        :cloudformationAttribute: StompEndpoints
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrStompEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="attrWssEndpoints")
    def attr_wss_endpoints(self) -> typing.List[builtins.str]:
        '''The WSS endpoints of each broker instance as a list of strings.

        ``wss://b-4aada85d-a80c-4be0-9d30-e344a01b921e-1.mq.eu-central-amazonaws.com:61619``

        :cloudformationAttribute: WssEndpoints
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrWssEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs.

        For more information, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the *Billing and Cost Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Enables automatic upgrades to new minor versions for brokers, as new broker engine versions are released and supported by Amazon MQ.

        Automatic upgrades occur during the scheduled maintenance window of the broker or after a manual broker reboot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-autominorversionupgrade
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "autoMinorVersionUpgrade"))

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73cb4392e397a8bf6024cecdbaeba56fcb3808f2de8cdd0fd09da159e5893273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="brokerName")
    def broker_name(self) -> builtins.str:
        '''The name of the broker.

        This value must be unique in your AWS account , 1-50 characters long, must contain only letters, numbers, dashes, and underscores, and must not contain white spaces, brackets, wildcard characters, or special characters.
        .. epigraph::

           Do not add personally identifiable information (PII) or other confidential or sensitive information in broker names. Broker names are accessible to other AWS services, including C CloudWatch Logs . Broker names are not intended to be used for private or sensitive data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-brokername
        '''
        return typing.cast(builtins.str, jsii.get(self, "brokerName"))

    @broker_name.setter
    def broker_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0daa4666e6bf3bde78b2b09f9623b4537b65c6e1535d32eeac33f6dbd83c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brokerName", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentMode")
    def deployment_mode(self) -> builtins.str:
        '''The deployment mode of the broker. Available values:.

        - ``SINGLE_INSTANCE``
        - ``ACTIVE_STANDBY_MULTI_AZ``
        - ``CLUSTER_MULTI_AZ``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-deploymentmode
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentMode"))

    @deployment_mode.setter
    def deployment_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff81b11ff0f11c306803914ef42deca65122e4781c59eaa6542f54d38a82a7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentMode", value)

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        '''The type of broker engine.

        Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-enginetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "engineType"))

    @engine_type.setter
    def engine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3434128f0868a1bd4c025b936b4adf4f295e8d3fefc3abc95671069848e0f10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineType", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        '''The version of the broker engine.

        For a list of supported engine versions, see `Engine <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_ in the *Amazon MQ Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-engineversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed3f7f986e26e31d15715ef94dda88292b22b1207b58d1c8b6a94c00da84e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="hostInstanceType")
    def host_instance_type(self) -> builtins.str:
        '''The broker's instance type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-hostinstancetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "hostInstanceType"))

    @host_instance_type.setter
    def host_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0753f154ec9741cad46cd1d079728296e32fee5a4a68de4f1f91e82703c74daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostInstanceType", value)

    @builtins.property
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Enables connections from applications outside of the VPC that hosts the broker's subnets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-publiclyaccessible
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "publiclyAccessible"))

    @publicly_accessible.setter
    def publicly_accessible(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460739a9e103382ef6cca205e1e6351438ca1b1790b6c577779e20ee9011597a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publiclyAccessible", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.UserProperty"]]]:
        '''The list of broker users (persons or applications) who can access queues and topics.

        For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent RabbitMQ users are created by via the RabbitMQ web console or by using the RabbitMQ management API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-users
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.UserProperty"]]], jsii.get(self, "users"))

    @users.setter
    def users(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.UserProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c69e5eee99b81f87f5ec7fc579d26ad9c6f437bc2c8c899efd98eb3d188aee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationStrategy")
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authentication strategy used to secure the broker. The default is ``SIMPLE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-authenticationstrategy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationStrategy"))

    @authentication_strategy.setter
    def authentication_strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d15489b5d4dccefc72409fe616528a32b012ba48a36c03c91efcf12a12e00a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.ConfigurationIdProperty"]]:
        '''A list of information about the configuration.

        Does not apply to RabbitMQ brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-configuration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.ConfigurationIdProperty"]], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.ConfigurationIdProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4c89e8c8c08cc5fee504b889ab16f8a7310a8bb63c6c0406f375697d73c3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionOptions")
    def encryption_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.EncryptionOptionsProperty"]]:
        '''Encryption options for the broker.

        Does not apply to RabbitMQ brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-encryptionoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.EncryptionOptionsProperty"]], jsii.get(self, "encryptionOptions"))

    @encryption_options.setter
    def encryption_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.EncryptionOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e859f5c54cc89b4b305ddb74c5d84ac0f8d10df42424aa389ee07de09059fb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionOptions", value)

    @builtins.property
    @jsii.member(jsii_name="ldapServerMetadata")
    def ldap_server_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.LdapServerMetadataProperty"]]:
        '''Optional.

        The metadata of the LDAP server used to authenticate and authorize connections to the broker. Does not apply to RabbitMQ brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-ldapservermetadata
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.LdapServerMetadataProperty"]], jsii.get(self, "ldapServerMetadata"))

    @ldap_server_metadata.setter
    def ldap_server_metadata(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.LdapServerMetadataProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c980bd0a1b1d01423ebcdd6b42dcee5e463473481f74ac833385ac3b3a9fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapServerMetadata", value)

    @builtins.property
    @jsii.member(jsii_name="logs")
    def logs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.LogListProperty"]]:
        '''Enables Amazon CloudWatch logging for brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-logs
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.LogListProperty"]], jsii.get(self, "logs"))

    @logs.setter
    def logs(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.LogListProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c729b20922ae729368cd92107c608e71c43cc80c6f867b96deeb6b7de24ec7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logs", value)

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowStartTime")
    def maintenance_window_start_time(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.MaintenanceWindowProperty"]]:
        '''The scheduled time period relative to UTC during which Amazon MQ begins to apply pending updates or patches to the broker.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-maintenancewindowstarttime
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.MaintenanceWindowProperty"]], jsii.get(self, "maintenanceWindowStartTime"))

    @maintenance_window_start_time.setter
    def maintenance_window_start_time(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBroker.MaintenanceWindowProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5476c524ab327dc98bf5ce6989e4b5742ae9a3f3ea869b21c5b321c1c1102ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindowStartTime", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of rules (1 minimum, 125 maximum) that authorize connections to brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-securitygroups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58008eccb5ae19f5e6494f57bdb4800e53474924a5cf49b672a744844bd9604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''The broker's storage type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-storagetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69ca80da5598bce3148b83bc2c14eb8a4b3d7c8e5d3734cb2c6363991cceb48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of groups that define which subnets and IP ranges the broker can use from different Availability Zones.

        If you specify more than one subnet, the subnets must be in different Availability Zones. Amazon MQ will not be able to create VPC endpoints for your broker with multiple subnets in the same Availability Zone. A SINGLE_INSTANCE deployment requires one subnet (for example, the default subnet). An ACTIVE_STANDBY_MULTI_AZ deployment (ACTIVEMQ) requires two subnets. A CLUSTER_MULTI_AZ deployment (RABBITMQ) has no subnet requirements when deployed with public accessibility, deployment without public accessibility requires at least one subnet.
        .. epigraph::

           If you specify subnets in a shared VPC for a RabbitMQ broker, the associated VPC to which the specified subnets belong must be owned by your AWS account . Amazon MQ will not be able to create VPC enpoints in VPCs that are not owned by your AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-subnetids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd922d79c4748acbbbfded20d2d8b2b8cf807fff3b0d1a79300286cefdc07e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.ConfigurationIdProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "revision": "revision"},
    )
    class ConfigurationIdProperty:
        def __init__(self, *, id: builtins.str, revision: jsii.Number) -> None:
            '''A list of information about the configuration.

            .. epigraph::

               Does not apply to RabbitMQ brokers.

            :param id: The unique ID that Amazon MQ generates for the configuration.
            :param revision: The revision number of the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                configuration_id_property = amazonmq.CfnBroker.ConfigurationIdProperty(
                    id="id",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be5a6b2e970164831cfa0ee5b5311ec0b27daf4377ef558f348b14fc0cdcc565)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "revision": revision,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''The unique ID that Amazon MQ generates for the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def revision(self) -> jsii.Number:
            '''The revision number of the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.EncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"use_aws_owned_key": "useAwsOwnedKey", "kms_key_id": "kmsKeyId"},
    )
    class EncryptionOptionsProperty:
        def __init__(
            self,
            *,
            use_aws_owned_key: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Encryption options for the broker.

            .. epigraph::

               Does not apply to RabbitMQ brokers.

            :param use_aws_owned_key: Enables the use of an AWS owned CMK using AWS KMS (KMS). Set to ``true`` by default, if no value is provided, for example, for RabbitMQ brokers.
            :param kms_key_id: The customer master key (CMK) to use for the A AWS KMS (KMS). This key is used to encrypt your data at rest. If not provided, Amazon MQ will use a default CMK to encrypt your data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                encryption_options_property = amazonmq.CfnBroker.EncryptionOptionsProperty(
                    use_aws_owned_key=False,
                
                    # the properties below are optional
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af04634f064b7cd6792c8d2bc1f49aec63c3a1a08a03d2fbd85bd105e28adcbd)
                check_type(argname="argument use_aws_owned_key", value=use_aws_owned_key, expected_type=type_hints["use_aws_owned_key"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "use_aws_owned_key": use_aws_owned_key,
            }
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def use_aws_owned_key(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Enables the use of an AWS owned CMK using AWS KMS (KMS).

            Set to ``true`` by default, if no value is provided, for example, for RabbitMQ brokers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html#cfn-amazonmq-broker-encryptionoptions-useawsownedkey
            '''
            result = self._values.get("use_aws_owned_key")
            assert result is not None, "Required property 'use_aws_owned_key' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The customer master key (CMK) to use for the A AWS KMS (KMS).

            This key is used to encrypt your data at rest. If not provided, Amazon MQ will use a default CMK to encrypt your data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html#cfn-amazonmq-broker-encryptionoptions-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.LdapServerMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hosts": "hosts",
            "role_base": "roleBase",
            "role_search_matching": "roleSearchMatching",
            "service_account_password": "serviceAccountPassword",
            "service_account_username": "serviceAccountUsername",
            "user_base": "userBase",
            "user_search_matching": "userSearchMatching",
            "role_name": "roleName",
            "role_search_subtree": "roleSearchSubtree",
            "user_role_name": "userRoleName",
            "user_search_subtree": "userSearchSubtree",
        },
    )
    class LdapServerMetadataProperty:
        def __init__(
            self,
            *,
            hosts: typing.Sequence[builtins.str],
            role_base: builtins.str,
            role_search_matching: builtins.str,
            service_account_password: builtins.str,
            service_account_username: builtins.str,
            user_base: builtins.str,
            user_search_matching: builtins.str,
            role_name: typing.Optional[builtins.str] = None,
            role_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            user_role_name: typing.Optional[builtins.str] = None,
            user_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Optional. The metadata of the LDAP server used to authenticate and authorize connections to the broker.

            .. epigraph::

               Does not apply to RabbitMQ brokers.

            :param hosts: Specifies the location of the LDAP server such as AWS Directory Service for Microsoft Active Directory . Optional failover server.
            :param role_base: The distinguished name of the node in the directory information tree (DIT) to search for roles or groups. For example, ``ou=group`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .
            :param role_search_matching: The LDAP search filter used to find roles within the roleBase. The distinguished name of the user matched by userSearchMatching is substituted into the ``{0}`` placeholder in the search filter. The client's username is substituted into the ``{1}`` placeholder. For example, if you set this option to ``(member=uid={1})`` for the user janedoe, the search filter becomes ``(member=uid=janedoe)`` after string substitution. It matches all role entries that have a member attribute equal to ``uid=janedoe`` under the subtree selected by the ``RoleBases`` .
            :param service_account_password: Service account password. A service account is an account in your LDAP server that has access to initiate a connection. For example, ``cn=admin`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .
            :param service_account_username: Service account username. A service account is an account in your LDAP server that has access to initiate a connection. For example, ``cn=admin`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .
            :param user_base: Select a particular subtree of the directory information tree (DIT) to search for user entries. The subtree is specified by a DN, which specifies the base node of the subtree. For example, by setting this option to ``ou=Users`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` , the search for user entries is restricted to the subtree beneath ``ou=Users`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .
            :param user_search_matching: The LDAP search filter used to find users within the ``userBase`` . The client's username is substituted into the ``{0}`` placeholder in the search filter. For example, if this option is set to ``(uid={0})`` and the received username is ``janedoe`` , the search filter becomes ``(uid=janedoe)`` after string substitution. It will result in matching an entry like ``uid=janedoe`` , ``ou=Users`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .
            :param role_name: The group name attribute in a role entry whose value is the name of that role. For example, you can specify ``cn`` for a group entry's common name. If authentication succeeds, then the user is assigned the the value of the ``cn`` attribute for each role entry that they are a member of.
            :param role_search_subtree: The directory search scope for the role. If set to true, scope is to search the entire subtree.
            :param user_role_name: The name of the LDAP attribute in the user's directory entry for the user's group membership. In some cases, user roles may be identified by the value of an attribute in the user's directory entry. The ``UserRoleName`` option allows you to provide the name of this attribute.
            :param user_search_subtree: The directory search scope for the user. If set to true, scope is to search the entire subtree.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                ldap_server_metadata_property = amazonmq.CfnBroker.LdapServerMetadataProperty(
                    hosts=["hosts"],
                    role_base="roleBase",
                    role_search_matching="roleSearchMatching",
                    service_account_password="serviceAccountPassword",
                    service_account_username="serviceAccountUsername",
                    user_base="userBase",
                    user_search_matching="userSearchMatching",
                
                    # the properties below are optional
                    role_name="roleName",
                    role_search_subtree=False,
                    user_role_name="userRoleName",
                    user_search_subtree=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7954c8223dcd086e9841c9e5603e56801f792e63cc8218af6b0833a9bfa973ac)
                check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
                check_type(argname="argument role_base", value=role_base, expected_type=type_hints["role_base"])
                check_type(argname="argument role_search_matching", value=role_search_matching, expected_type=type_hints["role_search_matching"])
                check_type(argname="argument service_account_password", value=service_account_password, expected_type=type_hints["service_account_password"])
                check_type(argname="argument service_account_username", value=service_account_username, expected_type=type_hints["service_account_username"])
                check_type(argname="argument user_base", value=user_base, expected_type=type_hints["user_base"])
                check_type(argname="argument user_search_matching", value=user_search_matching, expected_type=type_hints["user_search_matching"])
                check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
                check_type(argname="argument role_search_subtree", value=role_search_subtree, expected_type=type_hints["role_search_subtree"])
                check_type(argname="argument user_role_name", value=user_role_name, expected_type=type_hints["user_role_name"])
                check_type(argname="argument user_search_subtree", value=user_search_subtree, expected_type=type_hints["user_search_subtree"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hosts": hosts,
                "role_base": role_base,
                "role_search_matching": role_search_matching,
                "service_account_password": service_account_password,
                "service_account_username": service_account_username,
                "user_base": user_base,
                "user_search_matching": user_search_matching,
            }
            if role_name is not None:
                self._values["role_name"] = role_name
            if role_search_subtree is not None:
                self._values["role_search_subtree"] = role_search_subtree
            if user_role_name is not None:
                self._values["user_role_name"] = user_role_name
            if user_search_subtree is not None:
                self._values["user_search_subtree"] = user_search_subtree

        @builtins.property
        def hosts(self) -> typing.List[builtins.str]:
            '''Specifies the location of the LDAP server such as AWS Directory Service for Microsoft Active Directory .

            Optional failover server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-hosts
            '''
            result = self._values.get("hosts")
            assert result is not None, "Required property 'hosts' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def role_base(self) -> builtins.str:
            '''The distinguished name of the node in the directory information tree (DIT) to search for roles or groups.

            For example, ``ou=group`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolebase
            '''
            result = self._values.get("role_base")
            assert result is not None, "Required property 'role_base' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_search_matching(self) -> builtins.str:
            '''The LDAP search filter used to find roles within the roleBase.

            The distinguished name of the user matched by userSearchMatching is substituted into the ``{0}`` placeholder in the search filter. The client's username is substituted into the ``{1}`` placeholder. For example, if you set this option to ``(member=uid={1})`` for the user janedoe, the search filter becomes ``(member=uid=janedoe)`` after string substitution. It matches all role entries that have a member attribute equal to ``uid=janedoe`` under the subtree selected by the ``RoleBases`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolesearchmatching
            '''
            result = self._values.get("role_search_matching")
            assert result is not None, "Required property 'role_search_matching' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def service_account_password(self) -> builtins.str:
            '''Service account password.

            A service account is an account in your LDAP server that has access to initiate a connection. For example, ``cn=admin`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-serviceaccountpassword
            '''
            result = self._values.get("service_account_password")
            assert result is not None, "Required property 'service_account_password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def service_account_username(self) -> builtins.str:
            '''Service account username.

            A service account is an account in your LDAP server that has access to initiate a connection. For example, ``cn=admin`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-serviceaccountusername
            '''
            result = self._values.get("service_account_username")
            assert result is not None, "Required property 'service_account_username' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_base(self) -> builtins.str:
            '''Select a particular subtree of the directory information tree (DIT) to search for user entries.

            The subtree is specified by a DN, which specifies the base node of the subtree. For example, by setting this option to ``ou=Users`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` , the search for user entries is restricted to the subtree beneath ``ou=Users`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-userbase
            '''
            result = self._values.get("user_base")
            assert result is not None, "Required property 'user_base' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_search_matching(self) -> builtins.str:
            '''The LDAP search filter used to find users within the ``userBase`` .

            The client's username is substituted into the ``{0}`` placeholder in the search filter. For example, if this option is set to ``(uid={0})`` and the received username is ``janedoe`` , the search filter becomes ``(uid=janedoe)`` after string substitution. It will result in matching an entry like ``uid=janedoe`` , ``ou=Users`` , ``ou=corp`` , ``dc=corp`` , ``dc=example`` , ``dc=com`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-usersearchmatching
            '''
            result = self._values.get("user_search_matching")
            assert result is not None, "Required property 'user_search_matching' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_name(self) -> typing.Optional[builtins.str]:
            '''The group name attribute in a role entry whose value is the name of that role.

            For example, you can specify ``cn`` for a group entry's common name. If authentication succeeds, then the user is assigned the the value of the ``cn`` attribute for each role entry that they are a member of.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolename
            '''
            result = self._values.get("role_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_search_subtree(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''The directory search scope for the role.

            If set to true, scope is to search the entire subtree.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolesearchsubtree
            '''
            result = self._values.get("role_search_subtree")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def user_role_name(self) -> typing.Optional[builtins.str]:
            '''The name of the LDAP attribute in the user's directory entry for the user's group membership.

            In some cases, user roles may be identified by the value of an attribute in the user's directory entry. The ``UserRoleName`` option allows you to provide the name of this attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-userrolename
            '''
            result = self._values.get("user_role_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_search_subtree(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''The directory search scope for the user.

            If set to true, scope is to search the entire subtree.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-usersearchsubtree
            '''
            result = self._values.get("user_search_subtree")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LdapServerMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.LogListProperty",
        jsii_struct_bases=[],
        name_mapping={"audit": "audit", "general": "general"},
    )
    class LogListProperty:
        def __init__(
            self,
            *,
            audit: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            general: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''The list of information about logs to be enabled for the specified broker.

            :param audit: Enables audit logging. Every user management action made using JMX or the ActiveMQ Web Console is logged. Does not apply to RabbitMQ brokers.
            :param general: Enables general logging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                log_list_property = amazonmq.CfnBroker.LogListProperty(
                    audit=False,
                    general=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__033183c07de2b290edc4b22eb38314ed619a3b899441e4aa75ba245db31bd48c)
                check_type(argname="argument audit", value=audit, expected_type=type_hints["audit"])
                check_type(argname="argument general", value=general, expected_type=type_hints["general"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audit is not None:
                self._values["audit"] = audit
            if general is not None:
                self._values["general"] = general

        @builtins.property
        def audit(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables audit logging.

            Every user management action made using JMX or the ActiveMQ Web Console is logged. Does not apply to RabbitMQ brokers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-audit
            '''
            result = self._values.get("audit")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def general(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables general logging.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-general
            '''
            result = self._values.get("general")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.MaintenanceWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "day_of_week": "dayOfWeek",
            "time_of_day": "timeOfDay",
            "time_zone": "timeZone",
        },
    )
    class MaintenanceWindowProperty:
        def __init__(
            self,
            *,
            day_of_week: builtins.str,
            time_of_day: builtins.str,
            time_zone: builtins.str,
        ) -> None:
            '''The parameters that determine the ``WeeklyStartTime`` to apply pending updates or patches to the broker.

            :param day_of_week: The day of the week.
            :param time_of_day: The time, in 24-hour format.
            :param time_zone: The time zone, UTC by default, in either the Country/City format, or the UTC offset format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                maintenance_window_property = amazonmq.CfnBroker.MaintenanceWindowProperty(
                    day_of_week="dayOfWeek",
                    time_of_day="timeOfDay",
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__357cad3ac224307535225ced2484ed6cd99705f8b6531b8436649c3fa60ba91d)
                check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
                check_type(argname="argument time_of_day", value=time_of_day, expected_type=type_hints["time_of_day"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "day_of_week": day_of_week,
                "time_of_day": time_of_day,
                "time_zone": time_zone,
            }

        @builtins.property
        def day_of_week(self) -> builtins.str:
            '''The day of the week.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-dayofweek
            '''
            result = self._values.get("day_of_week")
            assert result is not None, "Required property 'day_of_week' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time_of_day(self) -> builtins.str:
            '''The time, in 24-hour format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timeofday
            '''
            result = self._values.get("time_of_day")
            assert result is not None, "Required property 'time_of_day' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time_zone(self) -> builtins.str:
            '''The time zone, UTC by default, in either the Country/City format, or the UTC offset format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timezone
            '''
            result = self._values.get("time_zone")
            assert result is not None, "Required property 'time_zone' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A key-value pair to associate with the broker.

            :param key: The key in a key-value pair.
            :param value: The value in a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                tags_entry_property = amazonmq.CfnBroker.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6611f03f8e8ece288be78f62053da50aced9d59b6c8db4ffb28ae429ce43842d)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The key in a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value in a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.UserProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "username": "username",
            "console_access": "consoleAccess",
            "groups": "groups",
        },
    )
    class UserProperty:
        def __init__(
            self,
            *,
            password: builtins.str,
            username: builtins.str,
            console_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The list of broker users (persons or applications) who can access queues and topics.

            For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent broker users are created via the RabbitMQ web console or by using the RabbitMQ management API.

            :param password: The password of the user. This value must be at least 12 characters long, must contain at least 4 unique characters, and must not contain commas, colons, or equal signs (,:=).
            :param username: The username of the broker user. For Amazon MQ for ActiveMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). For Amazon MQ for RabbitMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores (- . _). This value must not contain a tilde (~) character. Amazon MQ prohibts using guest as a valid usename. This value must be 2-100 characters long. .. epigraph:: Do not add personally identifiable information (PII) or other confidential or sensitive information in broker usernames. Broker usernames are accessible to other AWS services, including CloudWatch Logs . Broker usernames are not intended to be used for private or sensitive data.
            :param console_access: Enables access to the ActiveMQ web console for the ActiveMQ user. Does not apply to RabbitMQ brokers.
            :param groups: The list of groups (20 maximum) to which the ActiveMQ user belongs. This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 2-100 characters long. Does not apply to RabbitMQ brokers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                user_property = amazonmq.CfnBroker.UserProperty(
                    password="password",
                    username="username",
                
                    # the properties below are optional
                    console_access=False,
                    groups=["groups"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83ae718ba897f3cb3366a78422d449da7fc993682bc3ae56dd05209a69d46803)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
                check_type(argname="argument console_access", value=console_access, expected_type=type_hints["console_access"])
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }
            if console_access is not None:
                self._values["console_access"] = console_access
            if groups is not None:
                self._values["groups"] = groups

        @builtins.property
        def password(self) -> builtins.str:
            '''The password of the user.

            This value must be at least 12 characters long, must contain at least 4 unique characters, and must not contain commas, colons, or equal signs (,:=).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The username of the broker user.

            For Amazon MQ for ActiveMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). For Amazon MQ for RabbitMQ brokers, this value can contain only alphanumeric characters, dashes, periods, underscores (- . _). This value must not contain a tilde (~) character. Amazon MQ prohibts using guest as a valid usename. This value must be 2-100 characters long.
            .. epigraph::

               Do not add personally identifiable information (PII) or other confidential or sensitive information in broker usernames. Broker usernames are accessible to other AWS services, including CloudWatch Logs . Broker usernames are not intended to be used for private or sensitive data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def console_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables access to the ActiveMQ web console for the ActiveMQ user.

            Does not apply to RabbitMQ brokers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-consoleaccess
            '''
            result = self._values.get("console_access")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of groups (20 maximum) to which the ActiveMQ user belongs.

            This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 2-100 characters long. Does not apply to RabbitMQ brokers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amazonmq.CfnBrokerProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "broker_name": "brokerName",
        "deployment_mode": "deploymentMode",
        "engine_type": "engineType",
        "engine_version": "engineVersion",
        "host_instance_type": "hostInstanceType",
        "publicly_accessible": "publiclyAccessible",
        "users": "users",
        "authentication_strategy": "authenticationStrategy",
        "configuration": "configuration",
        "encryption_options": "encryptionOptions",
        "ldap_server_metadata": "ldapServerMetadata",
        "logs": "logs",
        "maintenance_window_start_time": "maintenanceWindowStartTime",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnBrokerProps:
    def __init__(
        self,
        *,
        auto_minor_version_upgrade: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        broker_name: builtins.str,
        deployment_mode: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        host_instance_type: builtins.str,
        publicly_accessible: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        users: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.UserProperty, typing.Dict[builtins.str, typing.Any]]]]],
        authentication_strategy: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.EncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        ldap_server_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.LdapServerMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.LogListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        maintenance_window_start_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.MaintenanceWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnBroker.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnBroker``.

        :param auto_minor_version_upgrade: Enables automatic upgrades to new minor versions for brokers, as new broker engine versions are released and supported by Amazon MQ. Automatic upgrades occur during the scheduled maintenance window of the broker or after a manual broker reboot.
        :param broker_name: The name of the broker. This value must be unique in your AWS account , 1-50 characters long, must contain only letters, numbers, dashes, and underscores, and must not contain white spaces, brackets, wildcard characters, or special characters. .. epigraph:: Do not add personally identifiable information (PII) or other confidential or sensitive information in broker names. Broker names are accessible to other AWS services, including C CloudWatch Logs . Broker names are not intended to be used for private or sensitive data.
        :param deployment_mode: The deployment mode of the broker. Available values:. - ``SINGLE_INSTANCE`` - ``ACTIVE_STANDBY_MULTI_AZ`` - ``CLUSTER_MULTI_AZ``
        :param engine_type: The type of broker engine. Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .
        :param engine_version: The version of the broker engine. For a list of supported engine versions, see `Engine <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_ in the *Amazon MQ Developer Guide* .
        :param host_instance_type: The broker's instance type.
        :param publicly_accessible: Enables connections from applications outside of the VPC that hosts the broker's subnets.
        :param users: The list of broker users (persons or applications) who can access queues and topics. For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent RabbitMQ users are created by via the RabbitMQ web console or by using the RabbitMQ management API.
        :param authentication_strategy: Optional. The authentication strategy used to secure the broker. The default is ``SIMPLE`` .
        :param configuration: A list of information about the configuration. Does not apply to RabbitMQ brokers.
        :param encryption_options: Encryption options for the broker. Does not apply to RabbitMQ brokers.
        :param ldap_server_metadata: Optional. The metadata of the LDAP server used to authenticate and authorize connections to the broker. Does not apply to RabbitMQ brokers.
        :param logs: Enables Amazon CloudWatch logging for brokers.
        :param maintenance_window_start_time: The scheduled time period relative to UTC during which Amazon MQ begins to apply pending updates or patches to the broker.
        :param security_groups: The list of rules (1 minimum, 125 maximum) that authorize connections to brokers.
        :param storage_type: The broker's storage type.
        :param subnet_ids: The list of groups that define which subnets and IP ranges the broker can use from different Availability Zones. If you specify more than one subnet, the subnets must be in different Availability Zones. Amazon MQ will not be able to create VPC endpoints for your broker with multiple subnets in the same Availability Zone. A SINGLE_INSTANCE deployment requires one subnet (for example, the default subnet). An ACTIVE_STANDBY_MULTI_AZ deployment (ACTIVEMQ) requires two subnets. A CLUSTER_MULTI_AZ deployment (RABBITMQ) has no subnet requirements when deployed with public accessibility, deployment without public accessibility requires at least one subnet. .. epigraph:: If you specify subnets in a shared VPC for a RabbitMQ broker, the associated VPC to which the specified subnets belong must be owned by your AWS account . Amazon MQ will not be able to create VPC enpoints in VPCs that are not owned by your AWS account .
        :param tags: An array of key-value pairs. For more information, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the *Billing and Cost Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amazonmq as amazonmq
            
            cfn_broker_props = amazonmq.CfnBrokerProps(
                auto_minor_version_upgrade=False,
                broker_name="brokerName",
                deployment_mode="deploymentMode",
                engine_type="engineType",
                engine_version="engineVersion",
                host_instance_type="hostInstanceType",
                publicly_accessible=False,
                users=[amazonmq.CfnBroker.UserProperty(
                    password="password",
                    username="username",
            
                    # the properties below are optional
                    console_access=False,
                    groups=["groups"]
                )],
            
                # the properties below are optional
                authentication_strategy="authenticationStrategy",
                configuration=amazonmq.CfnBroker.ConfigurationIdProperty(
                    id="id",
                    revision=123
                ),
                encryption_options=amazonmq.CfnBroker.EncryptionOptionsProperty(
                    use_aws_owned_key=False,
            
                    # the properties below are optional
                    kms_key_id="kmsKeyId"
                ),
                ldap_server_metadata=amazonmq.CfnBroker.LdapServerMetadataProperty(
                    hosts=["hosts"],
                    role_base="roleBase",
                    role_search_matching="roleSearchMatching",
                    service_account_password="serviceAccountPassword",
                    service_account_username="serviceAccountUsername",
                    user_base="userBase",
                    user_search_matching="userSearchMatching",
            
                    # the properties below are optional
                    role_name="roleName",
                    role_search_subtree=False,
                    user_role_name="userRoleName",
                    user_search_subtree=False
                ),
                logs=amazonmq.CfnBroker.LogListProperty(
                    audit=False,
                    general=False
                ),
                maintenance_window_start_time=amazonmq.CfnBroker.MaintenanceWindowProperty(
                    day_of_week="dayOfWeek",
                    time_of_day="timeOfDay",
                    time_zone="timeZone"
                ),
                security_groups=["securityGroups"],
                storage_type="storageType",
                subnet_ids=["subnetIds"],
                tags=[amazonmq.CfnBroker.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c75b5bfc38002f59a69ec66343a3c328a180a46cdfdc82b6518609aef93d458)
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument broker_name", value=broker_name, expected_type=type_hints["broker_name"])
            check_type(argname="argument deployment_mode", value=deployment_mode, expected_type=type_hints["deployment_mode"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument host_instance_type", value=host_instance_type, expected_type=type_hints["host_instance_type"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument authentication_strategy", value=authentication_strategy, expected_type=type_hints["authentication_strategy"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument encryption_options", value=encryption_options, expected_type=type_hints["encryption_options"])
            check_type(argname="argument ldap_server_metadata", value=ldap_server_metadata, expected_type=type_hints["ldap_server_metadata"])
            check_type(argname="argument logs", value=logs, expected_type=type_hints["logs"])
            check_type(argname="argument maintenance_window_start_time", value=maintenance_window_start_time, expected_type=type_hints["maintenance_window_start_time"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_minor_version_upgrade": auto_minor_version_upgrade,
            "broker_name": broker_name,
            "deployment_mode": deployment_mode,
            "engine_type": engine_type,
            "engine_version": engine_version,
            "host_instance_type": host_instance_type,
            "publicly_accessible": publicly_accessible,
            "users": users,
        }
        if authentication_strategy is not None:
            self._values["authentication_strategy"] = authentication_strategy
        if configuration is not None:
            self._values["configuration"] = configuration
        if encryption_options is not None:
            self._values["encryption_options"] = encryption_options
        if ldap_server_metadata is not None:
            self._values["ldap_server_metadata"] = ldap_server_metadata
        if logs is not None:
            self._values["logs"] = logs
        if maintenance_window_start_time is not None:
            self._values["maintenance_window_start_time"] = maintenance_window_start_time
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Enables automatic upgrades to new minor versions for brokers, as new broker engine versions are released and supported by Amazon MQ.

        Automatic upgrades occur during the scheduled maintenance window of the broker or after a manual broker reboot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        assert result is not None, "Required property 'auto_minor_version_upgrade' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def broker_name(self) -> builtins.str:
        '''The name of the broker.

        This value must be unique in your AWS account , 1-50 characters long, must contain only letters, numbers, dashes, and underscores, and must not contain white spaces, brackets, wildcard characters, or special characters.
        .. epigraph::

           Do not add personally identifiable information (PII) or other confidential or sensitive information in broker names. Broker names are accessible to other AWS services, including C CloudWatch Logs . Broker names are not intended to be used for private or sensitive data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-brokername
        '''
        result = self._values.get("broker_name")
        assert result is not None, "Required property 'broker_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_mode(self) -> builtins.str:
        '''The deployment mode of the broker. Available values:.

        - ``SINGLE_INSTANCE``
        - ``ACTIVE_STANDBY_MULTI_AZ``
        - ``CLUSTER_MULTI_AZ``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-deploymentmode
        '''
        result = self._values.get("deployment_mode")
        assert result is not None, "Required property 'deployment_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_type(self) -> builtins.str:
        '''The type of broker engine.

        Currently, Amazon MQ supports ``ACTIVEMQ`` and ``RABBITMQ`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-enginetype
        '''
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_version(self) -> builtins.str:
        '''The version of the broker engine.

        For a list of supported engine versions, see `Engine <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_ in the *Amazon MQ Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-engineversion
        '''
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_instance_type(self) -> builtins.str:
        '''The broker's instance type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-hostinstancetype
        '''
        result = self._values.get("host_instance_type")
        assert result is not None, "Required property 'host_instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Enables connections from applications outside of the VPC that hosts the broker's subnets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        assert result is not None, "Required property 'publicly_accessible' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.UserProperty]]]:
        '''The list of broker users (persons or applications) who can access queues and topics.

        For Amazon MQ for RabbitMQ brokers, one and only one administrative user is accepted and created when a broker is first provisioned. All subsequent RabbitMQ users are created by via the RabbitMQ web console or by using the RabbitMQ management API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-users
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.UserProperty]]], result)

    @builtins.property
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authentication strategy used to secure the broker. The default is ``SIMPLE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-authenticationstrategy
        '''
        result = self._values.get("authentication_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.ConfigurationIdProperty]]:
        '''A list of information about the configuration.

        Does not apply to RabbitMQ brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.ConfigurationIdProperty]], result)

    @builtins.property
    def encryption_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.EncryptionOptionsProperty]]:
        '''Encryption options for the broker.

        Does not apply to RabbitMQ brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-encryptionoptions
        '''
        result = self._values.get("encryption_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.EncryptionOptionsProperty]], result)

    @builtins.property
    def ldap_server_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.LdapServerMetadataProperty]]:
        '''Optional.

        The metadata of the LDAP server used to authenticate and authorize connections to the broker. Does not apply to RabbitMQ brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-ldapservermetadata
        '''
        result = self._values.get("ldap_server_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.LdapServerMetadataProperty]], result)

    @builtins.property
    def logs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.LogListProperty]]:
        '''Enables Amazon CloudWatch logging for brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-logs
        '''
        result = self._values.get("logs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.LogListProperty]], result)

    @builtins.property
    def maintenance_window_start_time(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.MaintenanceWindowProperty]]:
        '''The scheduled time period relative to UTC during which Amazon MQ begins to apply pending updates or patches to the broker.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-maintenancewindowstarttime
        '''
        result = self._values.get("maintenance_window_start_time")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.MaintenanceWindowProperty]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of rules (1 minimum, 125 maximum) that authorize connections to brokers.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''The broker's storage type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of groups that define which subnets and IP ranges the broker can use from different Availability Zones.

        If you specify more than one subnet, the subnets must be in different Availability Zones. Amazon MQ will not be able to create VPC endpoints for your broker with multiple subnets in the same Availability Zone. A SINGLE_INSTANCE deployment requires one subnet (for example, the default subnet). An ACTIVE_STANDBY_MULTI_AZ deployment (ACTIVEMQ) requires two subnets. A CLUSTER_MULTI_AZ deployment (RABBITMQ) has no subnet requirements when deployed with public accessibility, deployment without public accessibility requires at least one subnet.
        .. epigraph::

           If you specify subnets in a shared VPC for a RabbitMQ broker, the associated VPC to which the specified subnets belong must be owned by your AWS account . Amazon MQ will not be able to create VPC enpoints in VPCs that are not owned by your AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnBroker.TagsEntryProperty]]:
        '''An array of key-value pairs.

        For more information, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the *Billing and Cost Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnBroker.TagsEntryProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBrokerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amazonmq.CfnConfiguration",
):
    '''A CloudFormation ``AWS::AmazonMQ::Configuration``.

    Creates a new configuration for the specified configuration name. Amazon MQ uses the default configuration (the engine type and version).
    .. epigraph::

       Does not apply to RabbitMQ brokers.

    :cloudformationResource: AWS::AmazonMQ::Configuration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amazonmq as amazonmq
        
        cfn_configuration = amazonmq.CfnConfiguration(self, "MyCfnConfiguration",
            data="data",
            engine_type="engineType",
            engine_version="engineVersion",
            name="name",
        
            # the properties below are optional
            authentication_strategy="authenticationStrategy",
            description="description",
            tags=[amazonmq.CfnConfiguration.TagsEntryProperty(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        data: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        authentication_strategy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnConfiguration.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AmazonMQ::Configuration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data: The base64-encoded XML configuration.
        :param engine_type: The type of broker engine. Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.
        :param engine_version: The version of the broker engine. For a list of supported engine versions, see ` <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_
        :param name: The name of the configuration. This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 1-150 characters long.
        :param authentication_strategy: Optional. The authentication strategy associated with the configuration. The default is ``SIMPLE`` .
        :param description: The description of the configuration.
        :param tags: Create tags when creating the configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1110e23ae530bf3bfc062d82d69450994660528863e08ac04e8693b00914758)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigurationProps(
            data=data,
            engine_type=engine_type,
            engine_version=engine_version,
            name=name,
            authentication_strategy=authentication_strategy,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13dc0dec6e515fe0d82110d13f52d7bb4876fecf60710870834565ba12ec81a)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4650a4304acb0b889b34047300b8150c987a80a878762f6d5c8fc13cd3372fe)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon MQ configuration.

        ``arn:aws:mq:us-east-2:123456789012:configuration:MyConfigurationDevelopment:c-1234a5b6-78cd-901e-2fgh-3i45j6k178l9``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the Amazon MQ configuration.

        ``c-1234a5b6-78cd-901e-2fgh-3i45j6k178l9``

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrRevision")
    def attr_revision(self) -> jsii.Number:
        '''The revision number of the configuration.

        ``1``

        :cloudformationAttribute: Revision
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrRevision"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Create tags when creating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        '''The base64-encoded XML configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-data
        '''
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661c724322628e3f70e18e939f27b81e9724a2800b211851b0990342ae83d281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        '''The type of broker engine.

        Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-enginetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "engineType"))

    @engine_type.setter
    def engine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b51e0930e305bd9fb65fd0216e5b40120bf8b1bdd9721384d28f8a03a874ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineType", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        '''The version of the broker engine.

        For a list of supported engine versions, see ` <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-engineversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668af4a2b1544aeeda5ceec1bb27d99d9de7d5eb3ea1c381d95754d1b506b975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the configuration.

        This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 1-150 characters long.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da131008a1317d675f5e4525c285d12b4da807c47c328e49246f5d116f69317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationStrategy")
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authentication strategy associated with the configuration. The default is ``SIMPLE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-authenticationstrategy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationStrategy"))

    @authentication_strategy.setter
    def authentication_strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0b4db9339a28a10c5fd7172ed578ca64713fd6f1293f94d9dde6faf1a7164b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814906162a8c4457c08f8177f6e510ed10ae55532b8063baf20e0e8b26f6bef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnConfiguration.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A key-value pair to associate with the configuration.

            :param key: The key in a key-value pair.
            :param value: The value in a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                tags_entry_property = amazonmq.CfnConfiguration.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c25bd225a4cbea2b164d1cf220023d3b9e2c6c343d4a0bb6427166b37385b6d)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The key in a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value in a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConfigurationAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociation",
):
    '''A CloudFormation ``AWS::AmazonMQ::ConfigurationAssociation``.

    Use the AWS CloudFormation ``AWS::AmazonMQ::ConfigurationAssociation`` resource to associate a configuration with a broker, or return information about the specified ConfigurationAssociation. Only use one per broker, and don't use a configuration on the broker resource if you have associated a configuration with that broker.
    .. epigraph::

       Does not apply to RabbitMQ brokers.

    :cloudformationResource: AWS::AmazonMQ::ConfigurationAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amazonmq as amazonmq
        
        cfn_configuration_association = amazonmq.CfnConfigurationAssociation(self, "MyCfnConfigurationAssociation",
            broker="broker",
            configuration=amazonmq.CfnConfigurationAssociation.ConfigurationIdProperty(
                id="id",
                revision=123
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        broker: builtins.str,
        configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationAssociation.ConfigurationIdProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Create a new ``AWS::AmazonMQ::ConfigurationAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param broker: The broker to associate with a configuration.
        :param configuration: The configuration to associate with a broker.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c312160df1719f2b30ccdede3f640dd96511b25796698e6334985d56b628bf7c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigurationAssociationProps(
            broker=broker, configuration=configuration
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54522f2f1c322dd110c5d6dd95e617edbf070d78a3ec3d252f58b3ffb07fe08b)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02cee162766420865f704c4624061c4b3a7072fee335ebb4097eefdcfc4269b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="broker")
    def broker(self) -> builtins.str:
        '''The broker to associate with a configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-broker
        '''
        return typing.cast(builtins.str, jsii.get(self, "broker"))

    @broker.setter
    def broker(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593921f7a4fea8bebe0127624ddad10ad5f5dfe6544740ad4f870ab16ae9556a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "broker", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationAssociation.ConfigurationIdProperty"]:
        '''The configuration to associate with a broker.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-configuration
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationAssociation.ConfigurationIdProperty"], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationAssociation.ConfigurationIdProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84457b4abaeca25e0fd5bc2da0ea9f667839c738cd64d8a95077be153ce5a6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociation.ConfigurationIdProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "revision": "revision"},
    )
    class ConfigurationIdProperty:
        def __init__(self, *, id: builtins.str, revision: jsii.Number) -> None:
            '''The ``ConfigurationId`` property type specifies a configuration Id and the revision of a configuration.

            :param id: The unique ID that Amazon MQ generates for the configuration.
            :param revision: The revision number of the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amazonmq as amazonmq
                
                configuration_id_property = amazonmq.CfnConfigurationAssociation.ConfigurationIdProperty(
                    id="id",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f2b5caedfdec26d41b55c580e4d02c9e8d6f0ca49d8c0bc4dd60d978a32263f)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "revision": revision,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''The unique ID that Amazon MQ generates for the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def revision(self) -> jsii.Number:
            '''The revision number of the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"broker": "broker", "configuration": "configuration"},
)
class CfnConfigurationAssociationProps:
    def __init__(
        self,
        *,
        broker: builtins.str,
        configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationAssociation.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Properties for defining a ``CfnConfigurationAssociation``.

        :param broker: The broker to associate with a configuration.
        :param configuration: The configuration to associate with a broker.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amazonmq as amazonmq
            
            cfn_configuration_association_props = amazonmq.CfnConfigurationAssociationProps(
                broker="broker",
                configuration=amazonmq.CfnConfigurationAssociation.ConfigurationIdProperty(
                    id="id",
                    revision=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428634789c69f6957756c36c9085dff6a44b4cbe67abece2b8dc30a2f9d7a5b2)
            check_type(argname="argument broker", value=broker, expected_type=type_hints["broker"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "broker": broker,
            "configuration": configuration,
        }

    @builtins.property
    def broker(self) -> builtins.str:
        '''The broker to associate with a configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-broker
        '''
        result = self._values.get("broker")
        assert result is not None, "Required property 'broker' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationAssociation.ConfigurationIdProperty]:
        '''The configuration to associate with a broker.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-configuration
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationAssociation.ConfigurationIdProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "engine_type": "engineType",
        "engine_version": "engineVersion",
        "name": "name",
        "authentication_strategy": "authenticationStrategy",
        "description": "description",
        "tags": "tags",
    },
)
class CfnConfigurationProps:
    def __init__(
        self,
        *,
        data: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        authentication_strategy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnConfiguration.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConfiguration``.

        :param data: The base64-encoded XML configuration.
        :param engine_type: The type of broker engine. Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.
        :param engine_version: The version of the broker engine. For a list of supported engine versions, see ` <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_
        :param name: The name of the configuration. This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 1-150 characters long.
        :param authentication_strategy: Optional. The authentication strategy associated with the configuration. The default is ``SIMPLE`` .
        :param description: The description of the configuration.
        :param tags: Create tags when creating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amazonmq as amazonmq
            
            cfn_configuration_props = amazonmq.CfnConfigurationProps(
                data="data",
                engine_type="engineType",
                engine_version="engineVersion",
                name="name",
            
                # the properties below are optional
                authentication_strategy="authenticationStrategy",
                description="description",
                tags=[amazonmq.CfnConfiguration.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5baee08be750734e826c81a7cb9cf2b9ddc74300e358e073e99a4143e49cee3c)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authentication_strategy", value=authentication_strategy, expected_type=type_hints["authentication_strategy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "engine_type": engine_type,
            "engine_version": engine_version,
            "name": name,
        }
        if authentication_strategy is not None:
            self._values["authentication_strategy"] = authentication_strategy
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data(self) -> builtins.str:
        '''The base64-encoded XML configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-data
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_type(self) -> builtins.str:
        '''The type of broker engine.

        Note: Currently, Amazon MQ only supports ACTIVEMQ for creating and editing broker configurations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-enginetype
        '''
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_version(self) -> builtins.str:
        '''The version of the broker engine.

        For a list of supported engine versions, see ` <https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-engineversion
        '''
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the configuration.

        This value can contain only alphanumeric characters, dashes, periods, underscores, and tildes (- . _ ~). This value must be 1-150 characters long.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authentication strategy associated with the configuration. The default is ``SIMPLE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-authenticationstrategy
        '''
        result = self._values.get("authentication_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnConfiguration.TagsEntryProperty]]:
        '''Create tags when creating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnConfiguration.TagsEntryProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnBroker",
    "CfnBrokerProps",
    "CfnConfiguration",
    "CfnConfigurationAssociation",
    "CfnConfigurationAssociationProps",
    "CfnConfigurationProps",
]

publication.publish()

def _typecheckingstub__27019b0b679211473fc3b3ec320c3dd0026020438314751341ae1c5a1f880409(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    auto_minor_version_upgrade: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    broker_name: builtins.str,
    deployment_mode: builtins.str,
    engine_type: builtins.str,
    engine_version: builtins.str,
    host_instance_type: builtins.str,
    publicly_accessible: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    users: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.UserProperty, typing.Dict[builtins.str, typing.Any]]]]],
    authentication_strategy: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.EncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ldap_server_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.LdapServerMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.LogListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_window_start_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.MaintenanceWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnBroker.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7b61b1bb0fd6820a9d42b1f797b5b264556c53486d0c9c7393577aa36e1983(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae92737f22dda6dddcd1108965f8032ad422462654ccd564ba7ef9d8e826cb08(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73cb4392e397a8bf6024cecdbaeba56fcb3808f2de8cdd0fd09da159e5893273(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0daa4666e6bf3bde78b2b09f9623b4537b65c6e1535d32eeac33f6dbd83c5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff81b11ff0f11c306803914ef42deca65122e4781c59eaa6542f54d38a82a7d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3434128f0868a1bd4c025b936b4adf4f295e8d3fefc3abc95671069848e0f10f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed3f7f986e26e31d15715ef94dda88292b22b1207b58d1c8b6a94c00da84e91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0753f154ec9741cad46cd1d079728296e32fee5a4a68de4f1f91e82703c74daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460739a9e103382ef6cca205e1e6351438ca1b1790b6c577779e20ee9011597a(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c69e5eee99b81f87f5ec7fc579d26ad9c6f437bc2c8c899efd98eb3d188aee2(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.UserProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d15489b5d4dccefc72409fe616528a32b012ba48a36c03c91efcf12a12e00a6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4c89e8c8c08cc5fee504b889ab16f8a7310a8bb63c6c0406f375697d73c3b7(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.ConfigurationIdProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e859f5c54cc89b4b305ddb74c5d84ac0f8d10df42424aa389ee07de09059fb5e(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.EncryptionOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c980bd0a1b1d01423ebcdd6b42dcee5e463473481f74ac833385ac3b3a9fe1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.LdapServerMetadataProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c729b20922ae729368cd92107c608e71c43cc80c6f867b96deeb6b7de24ec7b7(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.LogListProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5476c524ab327dc98bf5ce6989e4b5742ae9a3f3ea869b21c5b321c1c1102ea1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBroker.MaintenanceWindowProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58008eccb5ae19f5e6494f57bdb4800e53474924a5cf49b672a744844bd9604(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69ca80da5598bce3148b83bc2c14eb8a4b3d7c8e5d3734cb2c6363991cceb48(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd922d79c4748acbbbfded20d2d8b2b8cf807fff3b0d1a79300286cefdc07e0(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5a6b2e970164831cfa0ee5b5311ec0b27daf4377ef558f348b14fc0cdcc565(
    *,
    id: builtins.str,
    revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af04634f064b7cd6792c8d2bc1f49aec63c3a1a08a03d2fbd85bd105e28adcbd(
    *,
    use_aws_owned_key: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7954c8223dcd086e9841c9e5603e56801f792e63cc8218af6b0833a9bfa973ac(
    *,
    hosts: typing.Sequence[builtins.str],
    role_base: builtins.str,
    role_search_matching: builtins.str,
    service_account_password: builtins.str,
    service_account_username: builtins.str,
    user_base: builtins.str,
    user_search_matching: builtins.str,
    role_name: typing.Optional[builtins.str] = None,
    role_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    user_role_name: typing.Optional[builtins.str] = None,
    user_search_subtree: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033183c07de2b290edc4b22eb38314ed619a3b899441e4aa75ba245db31bd48c(
    *,
    audit: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    general: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357cad3ac224307535225ced2484ed6cd99705f8b6531b8436649c3fa60ba91d(
    *,
    day_of_week: builtins.str,
    time_of_day: builtins.str,
    time_zone: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6611f03f8e8ece288be78f62053da50aced9d59b6c8db4ffb28ae429ce43842d(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ae718ba897f3cb3366a78422d449da7fc993682bc3ae56dd05209a69d46803(
    *,
    password: builtins.str,
    username: builtins.str,
    console_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c75b5bfc38002f59a69ec66343a3c328a180a46cdfdc82b6518609aef93d458(
    *,
    auto_minor_version_upgrade: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    broker_name: builtins.str,
    deployment_mode: builtins.str,
    engine_type: builtins.str,
    engine_version: builtins.str,
    host_instance_type: builtins.str,
    publicly_accessible: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    users: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.UserProperty, typing.Dict[builtins.str, typing.Any]]]]],
    authentication_strategy: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.EncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ldap_server_metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.LdapServerMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.LogListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_window_start_time: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBroker.MaintenanceWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnBroker.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1110e23ae530bf3bfc062d82d69450994660528863e08ac04e8693b00914758(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    data: builtins.str,
    engine_type: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    authentication_strategy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnConfiguration.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13dc0dec6e515fe0d82110d13f52d7bb4876fecf60710870834565ba12ec81a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4650a4304acb0b889b34047300b8150c987a80a878762f6d5c8fc13cd3372fe(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661c724322628e3f70e18e939f27b81e9724a2800b211851b0990342ae83d281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b51e0930e305bd9fb65fd0216e5b40120bf8b1bdd9721384d28f8a03a874ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668af4a2b1544aeeda5ceec1bb27d99d9de7d5eb3ea1c381d95754d1b506b975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da131008a1317d675f5e4525c285d12b4da807c47c328e49246f5d116f69317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0b4db9339a28a10c5fd7172ed578ca64713fd6f1293f94d9dde6faf1a7164b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814906162a8c4457c08f8177f6e510ed10ae55532b8063baf20e0e8b26f6bef6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c25bd225a4cbea2b164d1cf220023d3b9e2c6c343d4a0bb6427166b37385b6d(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c312160df1719f2b30ccdede3f640dd96511b25796698e6334985d56b628bf7c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    broker: builtins.str,
    configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationAssociation.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54522f2f1c322dd110c5d6dd95e617edbf070d78a3ec3d252f58b3ffb07fe08b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02cee162766420865f704c4624061c4b3a7072fee335ebb4097eefdcfc4269b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593921f7a4fea8bebe0127624ddad10ad5f5dfe6544740ad4f870ab16ae9556a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84457b4abaeca25e0fd5bc2da0ea9f667839c738cd64d8a95077be153ce5a6b8(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationAssociation.ConfigurationIdProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2b5caedfdec26d41b55c580e4d02c9e8d6f0ca49d8c0bc4dd60d978a32263f(
    *,
    id: builtins.str,
    revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428634789c69f6957756c36c9085dff6a44b4cbe67abece2b8dc30a2f9d7a5b2(
    *,
    broker: builtins.str,
    configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationAssociation.ConfigurationIdProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5baee08be750734e826c81a7cb9cf2b9ddc74300e358e073e99a4143e49cee3c(
    *,
    data: builtins.str,
    engine_type: builtins.str,
    engine_version: builtins.str,
    name: builtins.str,
    authentication_strategy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnConfiguration.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
