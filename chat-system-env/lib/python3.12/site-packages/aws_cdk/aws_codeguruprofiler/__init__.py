'''
# AWS::CodeGuruProfiler Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

Amazon CodeGuru Profiler collects runtime performance data from your live applications, and provides recommendations that can help you fine-tune your application performance.

## Installation

Import to your project:

```python
import aws_cdk.aws_codeguruprofiler as codeguruprofiler
```

## Basic usage

Here's how to setup a profiling group and give your compute role permissions to publish to the profiling group to the profiling agent can publish profiling information:

```python
# The execution role of your application that publishes to the ProfilingGroup via CodeGuru Profiler Profiling Agent. (the following is merely an example)
publish_app_role = iam.Role(self, "PublishAppRole",
    assumed_by=iam.AccountRootPrincipal()
)

profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup")
profiling_group.grant_publish(publish_app_role)
```

## Compute Platform configuration

Code Guru Profiler supports multiple compute environments.
They can be configured when creating a Profiling Group by using the `computePlatform` property:

```python
profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup",
    compute_platform=codeguruprofiler.ComputePlatform.AWS_LAMBDA
)
```
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnProfilingGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroup",
):
    '''A CloudFormation ``AWS::CodeGuruProfiler::ProfilingGroup``.

    Creates a profiling group.

    :cloudformationResource: AWS::CodeGuruProfiler::ProfilingGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_codeguruprofiler as codeguruprofiler
        
        # agent_permissions: Any
        
        cfn_profiling_group = codeguruprofiler.CfnProfilingGroup(self, "MyCfnProfilingGroup",
            profiling_group_name="profilingGroupName",
        
            # the properties below are optional
            agent_permissions=agent_permissions,
            anomaly_detection_notification_configuration=[codeguruprofiler.CfnProfilingGroup.ChannelProperty(
                channel_uri="channelUri",
        
                # the properties below are optional
                channel_id="channelId"
            )],
            compute_platform="computePlatform",
            tags=[CfnTag(
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
        profiling_group_name: builtins.str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnProfilingGroup.ChannelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param profiling_group_name: The name of the profiling group.
        :param agent_permissions: The agent permissions attached to this profiling group. This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` . *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key. For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .
        :param anomaly_detection_notification_configuration: Adds anomaly notifications for a profiling group.
        :param compute_platform: The compute platform of the profiling group. Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.
        :param tags: A list of tags to add to the created profiling group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f716c140051ab3ab0d85b12915727069b195d1b8b90a71c09337bd86eed52c55)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProfilingGroupProps(
            profiling_group_name=profiling_group_name,
            agent_permissions=agent_permissions,
            anomaly_detection_notification_configuration=anomaly_detection_notification_configuration,
            compute_platform=compute_platform,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8d9915cd249d32e2cca82629c4798ab6b6578ff7e101f1d0fe197015130b43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9120857a7ca75673ab928dc634fc0ff341c0a256d3f8e97da5d3d1c50c868af)
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
        '''The full Amazon Resource Name (ARN) for that profiling group.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of tags to add to the created profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentPermissions")
    def agent_permissions(self) -> typing.Any:
        '''The agent permissions attached to this profiling group.

        This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` .

        *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key.

        For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        '''
        return typing.cast(typing.Any, jsii.get(self, "agentPermissions"))

    @agent_permissions.setter
    def agent_permissions(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8f16257dd8b97675d05722f4c74a89415dfe9dd90c9c69acfa5fb72268e9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentPermissions", value)

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''The name of the profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupName"))

    @profiling_group_name.setter
    def profiling_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827c37a5bbd608aa0ab6c3cd91c24b907ebc73319417390b0a1c6656740f2bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profilingGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="anomalyDetectionNotificationConfiguration")
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProfilingGroup.ChannelProperty"]]]]:
        '''Adds anomaly notifications for a profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProfilingGroup.ChannelProperty"]]]], jsii.get(self, "anomalyDetectionNotificationConfiguration"))

    @anomaly_detection_notification_configuration.setter
    def anomaly_detection_notification_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnProfilingGroup.ChannelProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8dbd2729ce0a37f9a95dcd047bc3c7c6bbbe1f281e0cefa1ec7a889ad8ac9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anomalyDetectionNotificationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The compute platform of the profiling group.

        Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computePlatform"))

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54bdaa4e19c8380cabfc1afb202043849692b396db8548d3f7e55cd3ce85d369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computePlatform", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroup.AgentPermissionsProperty",
        jsii_struct_bases=[],
        name_mapping={"principals": "principals"},
    )
    class AgentPermissionsProperty:
        def __init__(self, *, principals: typing.Sequence[builtins.str]) -> None:
            '''
            :param principals: ``CfnProfilingGroup.AgentPermissionsProperty.Principals``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-agentpermissions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codeguruprofiler as codeguruprofiler
                
                agent_permissions_property = codeguruprofiler.CfnProfilingGroup.AgentPermissionsProperty(
                    principals=["principals"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30fe6ae1b3b847041e02a0703afa10fbbab3170e1df4694345a7ef3fdd5b28df)
                check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "principals": principals,
            }

        @builtins.property
        def principals(self) -> typing.List[builtins.str]:
            '''``CfnProfilingGroup.AgentPermissionsProperty.Principals``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-agentpermissions.html#cfn-codeguruprofiler-profilinggroup-agentpermissions-principals
            '''
            result = self._values.get("principals")
            assert result is not None, "Required property 'principals' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentPermissionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroup.ChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_uri": "channelUri", "channel_id": "channelId"},
    )
    class ChannelProperty:
        def __init__(
            self,
            *,
            channel_uri: builtins.str,
            channel_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Notification medium for users to get alerted for events that occur in application profile.

            We support SNS topic as a notification channel.

            :param channel_uri: The channel URI.
            :param channel_id: The channel ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codeguruprofiler as codeguruprofiler
                
                channel_property = codeguruprofiler.CfnProfilingGroup.ChannelProperty(
                    channel_uri="channelUri",
                
                    # the properties below are optional
                    channel_id="channelId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a6c20a5deea4cd71b89d6e657354d122cbb4a3334b43d004333284d685373ea)
                check_type(argname="argument channel_uri", value=channel_uri, expected_type=type_hints["channel_uri"])
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "channel_uri": channel_uri,
            }
            if channel_id is not None:
                self._values["channel_id"] = channel_id

        @builtins.property
        def channel_uri(self) -> builtins.str:
            '''The channel URI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channeluri
            '''
            result = self._values.get("channel_uri")
            assert result is not None, "Required property 'channel_uri' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def channel_id(self) -> typing.Optional[builtins.str]:
            '''The channel ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channelid
            '''
            result = self._values.get("channel_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "profiling_group_name": "profilingGroupName",
        "agent_permissions": "agentPermissions",
        "anomaly_detection_notification_configuration": "anomalyDetectionNotificationConfiguration",
        "compute_platform": "computePlatform",
        "tags": "tags",
    },
)
class CfnProfilingGroupProps:
    def __init__(
        self,
        *,
        profiling_group_name: builtins.str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnProfilingGroup.ChannelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProfilingGroup``.

        :param profiling_group_name: The name of the profiling group.
        :param agent_permissions: The agent permissions attached to this profiling group. This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` . *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key. For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .
        :param anomaly_detection_notification_configuration: Adds anomaly notifications for a profiling group.
        :param compute_platform: The compute platform of the profiling group. Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.
        :param tags: A list of tags to add to the created profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codeguruprofiler as codeguruprofiler
            
            # agent_permissions: Any
            
            cfn_profiling_group_props = codeguruprofiler.CfnProfilingGroupProps(
                profiling_group_name="profilingGroupName",
            
                # the properties below are optional
                agent_permissions=agent_permissions,
                anomaly_detection_notification_configuration=[codeguruprofiler.CfnProfilingGroup.ChannelProperty(
                    channel_uri="channelUri",
            
                    # the properties below are optional
                    channel_id="channelId"
                )],
                compute_platform="computePlatform",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ab3f016dc6dd9dc09dbdd386c1dc4b0b32d9e05d5f91674f86042fc33b91f7)
            check_type(argname="argument profiling_group_name", value=profiling_group_name, expected_type=type_hints["profiling_group_name"])
            check_type(argname="argument agent_permissions", value=agent_permissions, expected_type=type_hints["agent_permissions"])
            check_type(argname="argument anomaly_detection_notification_configuration", value=anomaly_detection_notification_configuration, expected_type=type_hints["anomaly_detection_notification_configuration"])
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "profiling_group_name": profiling_group_name,
        }
        if agent_permissions is not None:
            self._values["agent_permissions"] = agent_permissions
        if anomaly_detection_notification_configuration is not None:
            self._values["anomaly_detection_notification_configuration"] = anomaly_detection_notification_configuration
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def profiling_group_name(self) -> builtins.str:
        '''The name of the profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        '''
        result = self._values.get("profiling_group_name")
        assert result is not None, "Required property 'profiling_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_permissions(self) -> typing.Any:
        '''The agent permissions attached to this profiling group.

        This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` .

        *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key.

        For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        '''
        result = self._values.get("agent_permissions")
        return typing.cast(typing.Any, result)

    @builtins.property
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnProfilingGroup.ChannelProperty]]]]:
        '''Adds anomaly notifications for a profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        '''
        result = self._values.get("anomaly_detection_notification_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnProfilingGroup.ChannelProperty]]]], result)

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The compute platform of the profiling group.

        Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags to add to the created profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codeguruprofiler.ComputePlatform")
class ComputePlatform(enum.Enum):
    '''The compute platform of the profiling group.

    :exampleMetadata: infused

    Example::

        profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup",
            compute_platform=codeguruprofiler.ComputePlatform.AWS_LAMBDA
        )
    '''

    AWS_LAMBDA = "AWS_LAMBDA"
    '''Use AWS_LAMBDA if your application runs on AWS Lambda.'''
    DEFAULT = "DEFAULT"
    '''Use Default if your application runs on a compute platform that is not AWS Lambda, such an Amazon EC2 instance, an on-premises server, or a different platform.'''


@jsii.interface(jsii_type="@aws-cdk/aws-codeguruprofiler.IProfilingGroup")
class IProfilingGroup(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''IResource represents a Profiling Group.'''

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''A name for the profiling group.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.
        '''
        ...


class _IProfilingGroupProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''IResource represents a Profiling Group.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codeguruprofiler.IProfilingGroup"

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''A name for the profiling group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupName"))

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88e8453e918064181c1aecee1bd3f67e3be3f106ccfa35c61d2de14a0beeba1)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPublish", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857e490ea8ed611e137f8d741192595357d9fbd8af493fecefa027a9441b3fc6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProfilingGroup).__jsii_proxy_class__ = lambda : _IProfilingGroupProxy


@jsii.implements(IProfilingGroup)
class ProfilingGroup(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codeguruprofiler.ProfilingGroup",
):
    '''A new Profiling Group.

    :exampleMetadata: infused

    Example::

        # The execution role of your application that publishes to the ProfilingGroup via CodeGuru Profiler Profiling Agent. (the following is merely an example)
        publish_app_role = iam.Role(self, "PublishAppRole",
            assumed_by=iam.AccountRootPrincipal()
        )
        
        profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup")
        profiling_group.grant_publish(publish_app_role)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_platform: typing.Optional[ComputePlatform] = None,
        profiling_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_platform: The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: A name for the profiling group. Default: - automatically generated name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f73721c21dbd5761dbe85ea68b74337db5ee95895842cc79becdf3ebf80b5e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ProfilingGroupProps(
            compute_platform=compute_platform,
            profiling_group_name=profiling_group_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromProfilingGroupArn")
    @builtins.classmethod
    def from_profiling_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        profiling_group_arn: builtins.str,
    ) -> IProfilingGroup:
        '''Import an existing Profiling Group provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_arn: Profiling Group ARN.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed5b8ed1bb81d6853ec217fb9bd052bbd652fe0f6f31c9f27ee10afe4e5ab1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument profiling_group_arn", value=profiling_group_arn, expected_type=type_hints["profiling_group_arn"])
        return typing.cast(IProfilingGroup, jsii.sinvoke(cls, "fromProfilingGroupArn", [scope, id, profiling_group_arn]))

    @jsii.member(jsii_name="fromProfilingGroupName")
    @builtins.classmethod
    def from_profiling_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        profiling_group_name: builtins.str,
    ) -> IProfilingGroup:
        '''Import an existing Profiling Group provided a Profiling Group Name.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_name: Profiling Group Name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6570e1a29cd47f21d0efb3006df51f83531a77b485867312993aecbecf4920f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument profiling_group_name", value=profiling_group_name, expected_type=type_hints["profiling_group_name"])
        return typing.cast(IProfilingGroup, jsii.sinvoke(cls, "fromProfilingGroupName", [scope, id, profiling_group_name]))

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715e3c0f5162e7f09ed226e552e8e16f1a41229f938c0db122a3e0b441b7f297)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPublish", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2bc605fb815f0a8c34f4a8f4fd0712c20779ff807cd5bcf82c063d4778bc7fd)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="profilingGroupArn")
    def profiling_group_arn(self) -> builtins.str:
        '''The ARN of the Profiling Group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''The name of the Profiling Group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codeguruprofiler.ProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_platform": "computePlatform",
        "profiling_group_name": "profilingGroupName",
    },
)
class ProfilingGroupProps:
    def __init__(
        self,
        *,
        compute_platform: typing.Optional[ComputePlatform] = None,
        profiling_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for creating a new Profiling Group.

        :param compute_platform: The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: A name for the profiling group. Default: - automatically generated name.

        :exampleMetadata: infused

        Example::

            profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup",
                compute_platform=codeguruprofiler.ComputePlatform.AWS_LAMBDA
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b7f51223bb1d72f5f58c12cadd72e0fcf5c8c84883fb377edf6a43144c7485)
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument profiling_group_name", value=profiling_group_name, expected_type=type_hints["profiling_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if profiling_group_name is not None:
            self._values["profiling_group_name"] = profiling_group_name

    @builtins.property
    def compute_platform(self) -> typing.Optional[ComputePlatform]:
        '''The compute platform of the profiling group.

        :default: ComputePlatform.DEFAULT
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[ComputePlatform], result)

    @builtins.property
    def profiling_group_name(self) -> typing.Optional[builtins.str]:
        '''A name for the profiling group.

        :default: - automatically generated name.
        '''
        result = self._values.get("profiling_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProfilingGroup",
    "CfnProfilingGroupProps",
    "ComputePlatform",
    "IProfilingGroup",
    "ProfilingGroup",
    "ProfilingGroupProps",
]

publication.publish()

def _typecheckingstub__f716c140051ab3ab0d85b12915727069b195d1b8b90a71c09337bd86eed52c55(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    profiling_group_name: builtins.str,
    agent_permissions: typing.Any = None,
    anomaly_detection_notification_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnProfilingGroup.ChannelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compute_platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8d9915cd249d32e2cca82629c4798ab6b6578ff7e101f1d0fe197015130b43(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9120857a7ca75673ab928dc634fc0ff341c0a256d3f8e97da5d3d1c50c868af(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8f16257dd8b97675d05722f4c74a89415dfe9dd90c9c69acfa5fb72268e9e3(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827c37a5bbd608aa0ab6c3cd91c24b907ebc73319417390b0a1c6656740f2bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8dbd2729ce0a37f9a95dcd047bc3c7c6bbbe1f281e0cefa1ec7a889ad8ac9b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnProfilingGroup.ChannelProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bdaa4e19c8380cabfc1afb202043849692b396db8548d3f7e55cd3ce85d369(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fe6ae1b3b847041e02a0703afa10fbbab3170e1df4694345a7ef3fdd5b28df(
    *,
    principals: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6c20a5deea4cd71b89d6e657354d122cbb4a3334b43d004333284d685373ea(
    *,
    channel_uri: builtins.str,
    channel_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ab3f016dc6dd9dc09dbdd386c1dc4b0b32d9e05d5f91674f86042fc33b91f7(
    *,
    profiling_group_name: builtins.str,
    agent_permissions: typing.Any = None,
    anomaly_detection_notification_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnProfilingGroup.ChannelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compute_platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88e8453e918064181c1aecee1bd3f67e3be3f106ccfa35c61d2de14a0beeba1(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857e490ea8ed611e137f8d741192595357d9fbd8af493fecefa027a9441b3fc6(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f73721c21dbd5761dbe85ea68b74337db5ee95895842cc79becdf3ebf80b5e0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_platform: typing.Optional[ComputePlatform] = None,
    profiling_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed5b8ed1bb81d6853ec217fb9bd052bbd652fe0f6f31c9f27ee10afe4e5ab1b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    profiling_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6570e1a29cd47f21d0efb3006df51f83531a77b485867312993aecbecf4920f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    profiling_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715e3c0f5162e7f09ed226e552e8e16f1a41229f938c0db122a3e0b441b7f297(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2bc605fb815f0a8c34f4a8f4fd0712c20779ff807cd5bcf82c063d4778bc7fd(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b7f51223bb1d72f5f58c12cadd72e0fcf5c8c84883fb377edf6a43144c7485(
    *,
    compute_platform: typing.Optional[ComputePlatform] = None,
    profiling_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
