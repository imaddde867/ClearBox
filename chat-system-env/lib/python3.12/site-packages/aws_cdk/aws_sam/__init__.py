'''
# AWS Serverless Application Model Construct Library

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
import aws_cdk.aws_sam as serverless
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Serverless construct libraries](https://constructs.dev/search?q=serverless)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Serverless resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Serverless.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Serverless](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Serverless.html).

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
class CfnApi(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-sam.CfnApi",
):
    '''A CloudFormation ``AWS::Serverless::Api``.

    :cloudformationResource: AWS::Serverless::Api
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_sam as sam
        
        # authorizers: Any
        # definition_body: Any
        # gateway_responses: Any
        # method_settings: Any
        # models: Any
        
        cfn_api = sam.CfnApi(self, "MyCfnApi",
            stage_name="stageName",
        
            # the properties below are optional
            access_log_setting=sam.CfnApi.AccessLogSettingProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            auth=sam.CfnApi.AuthProperty(
                add_default_authorizer_to_cors_preflight=False,
                authorizers=authorizers,
                default_authorizer="defaultAuthorizer"
            ),
            binary_media_types=["binaryMediaTypes"],
            cache_cluster_enabled=False,
            cache_cluster_size="cacheClusterSize",
            canary_setting=sam.CfnApi.CanarySettingProperty(
                deployment_id="deploymentId",
                percent_traffic=123,
                stage_variable_overrides={
                    "stage_variable_overrides_key": "stageVariableOverrides"
                },
                use_stage_cache=False
            ),
            cors="cors",
            definition_body=definition_body,
            definition_uri="definitionUri",
            description="description",
            disable_execute_api_endpoint=False,
            domain=sam.CfnApi.DomainConfigurationProperty(
                certificate_arn="certificateArn",
                domain_name="domainName",
        
                # the properties below are optional
                base_path=["basePath"],
                endpoint_configuration="endpointConfiguration",
                mutual_tls_authentication=sam.CfnApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                ),
                ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                route53=sam.CfnApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                ),
                security_policy="securityPolicy"
            ),
            endpoint_configuration="endpointConfiguration",
            gateway_responses=gateway_responses,
            method_settings=[method_settings],
            minimum_compression_size=123,
            models=models,
            name="name",
            open_api_version="openApiVersion",
            tags={
                "tags_key": "tags"
            },
            tracing_enabled=False,
            variables={
                "variables_key": "variables"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        stage_name: builtins.str,
        access_log_setting: typing.Optional[typing.Union[typing.Union["CfnApi.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.AuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        canary_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.CanarySettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.CorsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.DomainConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_configuration: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.EndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_responses: typing.Any = None,
        method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        models: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        open_api_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Api``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param stage_name: ``AWS::Serverless::Api.StageName``.
        :param access_log_setting: ``AWS::Serverless::Api.AccessLogSetting``.
        :param auth: ``AWS::Serverless::Api.Auth``.
        :param binary_media_types: ``AWS::Serverless::Api.BinaryMediaTypes``.
        :param cache_cluster_enabled: ``AWS::Serverless::Api.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::Serverless::Api.CacheClusterSize``.
        :param canary_setting: ``AWS::Serverless::Api.CanarySetting``.
        :param cors: ``AWS::Serverless::Api.Cors``.
        :param definition_body: ``AWS::Serverless::Api.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::Api.DefinitionUri``.
        :param description: ``AWS::Serverless::Api.Description``.
        :param disable_execute_api_endpoint: ``AWS::Serverless::Api.DisableExecuteApiEndpoint``.
        :param domain: ``AWS::Serverless::Api.Domain``.
        :param endpoint_configuration: ``AWS::Serverless::Api.EndpointConfiguration``.
        :param gateway_responses: ``AWS::Serverless::Api.GatewayResponses``.
        :param method_settings: ``AWS::Serverless::Api.MethodSettings``.
        :param minimum_compression_size: ``AWS::Serverless::Api.MinimumCompressionSize``.
        :param models: ``AWS::Serverless::Api.Models``.
        :param name: ``AWS::Serverless::Api.Name``.
        :param open_api_version: ``AWS::Serverless::Api.OpenApiVersion``.
        :param tags: ``AWS::Serverless::Api.Tags``.
        :param tracing_enabled: ``AWS::Serverless::Api.TracingEnabled``.
        :param variables: ``AWS::Serverless::Api.Variables``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8d174c9489d2435766305e09ee71df1defe3151360d2fc5e08295c8c1fff61)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiProps(
            stage_name=stage_name,
            access_log_setting=access_log_setting,
            auth=auth,
            binary_media_types=binary_media_types,
            cache_cluster_enabled=cache_cluster_enabled,
            cache_cluster_size=cache_cluster_size,
            canary_setting=canary_setting,
            cors=cors,
            definition_body=definition_body,
            definition_uri=definition_uri,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            domain=domain,
            endpoint_configuration=endpoint_configuration,
            gateway_responses=gateway_responses,
            method_settings=method_settings,
            minimum_compression_size=minimum_compression_size,
            models=models,
            name=name,
            open_api_version=open_api_version,
            tags=tags,
            tracing_enabled=tracing_enabled,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab635332aa820e8ef3c456c75717d6242466dd771c490de9c30cc50c90f9a2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9945ab899f7793ed8d7d05dd0af0ef1f61a0d089312f5ee4dd2dfa410fd2addd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::Serverless::Api.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::Api.DefinitionBody``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Any, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f571d6eff7af193f695ce08ba9055086a945a6825b0db81a9372a633d907f334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionBody", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayResponses")
    def gateway_responses(self) -> typing.Any:
        '''``AWS::Serverless::Api.GatewayResponses``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-gatewayresponses
        '''
        return typing.cast(typing.Any, jsii.get(self, "gatewayResponses"))

    @gateway_responses.setter
    def gateway_responses(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db74d14924afe83925def7f858ae642887373eaf81cb7ac70388527a43926717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayResponses", value)

    @builtins.property
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Any:
        '''``AWS::Serverless::Api.Models``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-models
        '''
        return typing.cast(typing.Any, jsii.get(self, "models"))

    @models.setter
    def models(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f765aa3749509905e01674610c53d8114c1d260081d1892809adbba50efc458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "models", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''``AWS::Serverless::Api.StageName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dcb1048bcb4a3802e22124e86ab1e6108d8181040028560b65dd883bf2821bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSetting")
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.AccessLogSetting``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "accessLogSetting"))

    @access_log_setting.setter
    def access_log_setting(
        self,
        value: typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d412f1e59917cf5da273b8783bb0758018b24da1d204337ed8028c977c8d9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLogSetting", value)

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.AuthProperty"]]:
        '''``AWS::Serverless::Api.Auth``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.AuthProperty"]], jsii.get(self, "auth"))

    @auth.setter
    def auth(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.AuthProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71ffe1090292b1a5983c610167357051a3f38cc18793af5f031ae1b9f3201ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auth", value)

    @builtins.property
    @jsii.member(jsii_name="binaryMediaTypes")
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Api.BinaryMediaTypes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "binaryMediaTypes"))

    @binary_media_types.setter
    def binary_media_types(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec45c90609b25b80db89c60a261dbd49352df8fdf99a24bbb1397cdc3f9c0166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryMediaTypes", value)

    @builtins.property
    @jsii.member(jsii_name="cacheClusterEnabled")
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.CacheClusterEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "cacheClusterEnabled"))

    @cache_cluster_enabled.setter
    def cache_cluster_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9426603404540095b8720f3644af27f71d1fcb8ff77abb5bb79f5fc99defbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheClusterEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cacheClusterSize")
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.CacheClusterSize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheClusterSize"))

    @cache_cluster_size.setter
    def cache_cluster_size(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7ce5f436b5f27dcc9dbcd95eba6bd79cc6f2f4b304ac59a3fef1aad31699de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheClusterSize", value)

    @builtins.property
    @jsii.member(jsii_name="canarySetting")
    def canary_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.CanarySettingProperty"]]:
        '''``AWS::Serverless::Api.CanarySetting``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-canarysetting
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.CanarySettingProperty"]], jsii.get(self, "canarySetting"))

    @canary_setting.setter
    def canary_setting(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.CanarySettingProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5ede5f9f5e7e45fa78b155176748d34375dc19446d84bccb7a5946db2822f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canarySetting", value)

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.CorsConfigurationProperty"]]:
        '''``AWS::Serverless::Api.Cors``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.CorsConfigurationProperty"]], jsii.get(self, "cors"))

    @cors.setter
    def cors(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.CorsConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abae15ee346e903b999c29af3a57dd4e0aef52b9d07a664d115417627ad7ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cors", value)

    @builtins.property
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.S3LocationProperty"]]:
        '''``AWS::Serverless::Api.DefinitionUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.S3LocationProperty"]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.S3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbc70ed3ace1928b2e43a7e6416a4c0fbe8fc7391b8cc98d746925abe1174f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Description``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71379e73816dc66f7afb23c995fa90fd44019ee4dabac582ae2cbb085e01f007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableExecuteApiEndpoint")
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.DisableExecuteApiEndpoint``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-disableexecuteapiendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "disableExecuteApiEndpoint"))

    @disable_execute_api_endpoint.setter
    def disable_execute_api_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b900b5f361f659680b647d38c0b7b05dbf2d0bea83e379dbd1c7b7efd2bf68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableExecuteApiEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.DomainConfigurationProperty"]]:
        '''``AWS::Serverless::Api.Domain``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-domain
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.DomainConfigurationProperty"]], jsii.get(self, "domain"))

    @domain.setter
    def domain(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.DomainConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f1359b547283059e938153da023a7e2e59f7c468a834dd576834a75c0b0874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="endpointConfiguration")
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.EndpointConfigurationProperty"]]:
        '''``AWS::Serverless::Api.EndpointConfiguration``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.EndpointConfigurationProperty"]], jsii.get(self, "endpointConfiguration"))

    @endpoint_configuration.setter
    def endpoint_configuration(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApi.EndpointConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995e0bb41529c0c8153e2b7f724c9df7b50ceee1d2f221ffe2f792233db83a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="methodSettings")
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.MethodSettings``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "methodSettings"))

    @method_settings.setter
    def method_settings(
        self,
        value: typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5865ec72142bebc767816ad218a1343dc6fe51aa3347c3c55e8beac8e752dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methodSettings", value)

    @builtins.property
    @jsii.member(jsii_name="minimumCompressionSize")
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Api.MinimumCompressionSize``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-minimumcompressionsize
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumCompressionSize"))

    @minimum_compression_size.setter
    def minimum_compression_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b974d2a253b91b4204155ead74e1b9ed515a879f89a74d6cde27ea57116577d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumCompressionSize", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Name``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13eb8fc594b3cd9d0073a6582028b2a41569fec5f5b4aff7fc5a6ee4ac0740d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="openApiVersion")
    def open_api_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.OpenApiVersion``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "openApiVersion"))

    @open_api_version.setter
    def open_api_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df99ef68a133f4dccea37284f6139bfccc4ada67b44c11b577c1c00c83b91ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openApiVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tracingEnabled")
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.TracingEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "tracingEnabled"))

    @tracing_enabled.setter
    def tracing_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05eccaac8d3b8787b8b121d1666cca07c46f86c5893ddb699a861d08ac0a644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "variables"))

    @variables.setter
    def variables(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d41210af4cec9e516f29901a1b964a0251fa824d6a25c607c5432c8f338d121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variables", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: ``CfnApi.AccessLogSettingProperty.DestinationArn``.
            :param format: ``CfnApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                access_log_setting_property = sam.CfnApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3bc864bdb2db7f9256ca4a628b1f3798257fea5b777af5bc86b18474ba8319ee)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AccessLogSettingProperty.DestinationArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.AuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_default_authorizer_to_cors_preflight": "addDefaultAuthorizerToCorsPreflight",
            "authorizers": "authorizers",
            "default_authorizer": "defaultAuthorizer",
        },
    )
    class AuthProperty:
        def __init__(
            self,
            *,
            add_default_authorizer_to_cors_preflight: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            authorizers: typing.Any = None,
            default_authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param add_default_authorizer_to_cors_preflight: ``CfnApi.AuthProperty.AddDefaultAuthorizerToCorsPreflight``.
            :param authorizers: ``CfnApi.AuthProperty.Authorizers``.
            :param default_authorizer: ``CfnApi.AuthProperty.DefaultAuthorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # authorizers: Any
                
                auth_property = sam.CfnApi.AuthProperty(
                    add_default_authorizer_to_cors_preflight=False,
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69a0b1b78bf0aa4cdcb1a5c1aa64f9cc921a2515f1162fd631334b41d11c523c)
                check_type(argname="argument add_default_authorizer_to_cors_preflight", value=add_default_authorizer_to_cors_preflight, expected_type=type_hints["add_default_authorizer_to_cors_preflight"])
                check_type(argname="argument authorizers", value=authorizers, expected_type=type_hints["authorizers"])
                check_type(argname="argument default_authorizer", value=default_authorizer, expected_type=type_hints["default_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_default_authorizer_to_cors_preflight is not None:
                self._values["add_default_authorizer_to_cors_preflight"] = add_default_authorizer_to_cors_preflight
            if authorizers is not None:
                self._values["authorizers"] = authorizers
            if default_authorizer is not None:
                self._values["default_authorizer"] = default_authorizer

        @builtins.property
        def add_default_authorizer_to_cors_preflight(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnApi.AuthProperty.AddDefaultAuthorizerToCorsPreflight``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("add_default_authorizer_to_cors_preflight")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def authorizers(self) -> typing.Any:
            '''``CfnApi.AuthProperty.Authorizers``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("authorizers")
            return typing.cast(typing.Any, result)

        @builtins.property
        def default_authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AuthProperty.DefaultAuthorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("default_authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.CanarySettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_id": "deploymentId",
            "percent_traffic": "percentTraffic",
            "stage_variable_overrides": "stageVariableOverrides",
            "use_stage_cache": "useStageCache",
        },
    )
    class CanarySettingProperty:
        def __init__(
            self,
            *,
            deployment_id: typing.Optional[builtins.str] = None,
            percent_traffic: typing.Optional[jsii.Number] = None,
            stage_variable_overrides: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param deployment_id: ``CfnApi.CanarySettingProperty.DeploymentId``.
            :param percent_traffic: ``CfnApi.CanarySettingProperty.PercentTraffic``.
            :param stage_variable_overrides: ``CfnApi.CanarySettingProperty.StageVariableOverrides``.
            :param use_stage_cache: ``CfnApi.CanarySettingProperty.UseStageCache``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                canary_setting_property = sam.CfnApi.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf12642b1799cdd28b654808811d661261342e364af2cf28fd645059177ba24b)
                check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
                check_type(argname="argument percent_traffic", value=percent_traffic, expected_type=type_hints["percent_traffic"])
                check_type(argname="argument stage_variable_overrides", value=stage_variable_overrides, expected_type=type_hints["stage_variable_overrides"])
                check_type(argname="argument use_stage_cache", value=use_stage_cache, expected_type=type_hints["use_stage_cache"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_id is not None:
                self._values["deployment_id"] = deployment_id
            if percent_traffic is not None:
                self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None:
                self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None:
                self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def deployment_id(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CanarySettingProperty.DeploymentId``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-deploymentid
            '''
            result = self._values.get("deployment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            '''``CfnApi.CanarySettingProperty.PercentTraffic``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-percenttraffic
            '''
            result = self._values.get("percent_traffic")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stage_variable_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnApi.CanarySettingProperty.StageVariableOverrides``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-stagevariableoverrides
            '''
            result = self._values.get("stage_variable_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def use_stage_cache(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnApi.CanarySettingProperty.UseStageCache``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-usestagecache
            '''
            result = self._values.get("use_stage_cache")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanarySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.CorsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_origin": "allowOrigin",
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationProperty:
        def __init__(
            self,
            *,
            allow_origin: builtins.str,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            allow_headers: typing.Optional[builtins.str] = None,
            allow_methods: typing.Optional[builtins.str] = None,
            max_age: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allow_origin: ``CfnApi.CorsConfigurationProperty.AllowOrigin``.
            :param allow_credentials: ``CfnApi.CorsConfigurationProperty.AllowCredentials``.
            :param allow_headers: ``CfnApi.CorsConfigurationProperty.AllowHeaders``.
            :param allow_methods: ``CfnApi.CorsConfigurationProperty.AllowMethods``.
            :param max_age: ``CfnApi.CorsConfigurationProperty.MaxAge``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                cors_configuration_property = sam.CfnApi.CorsConfigurationProperty(
                    allow_origin="allowOrigin",
                
                    # the properties below are optional
                    allow_credentials=False,
                    allow_headers="allowHeaders",
                    allow_methods="allowMethods",
                    max_age="maxAge"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7420c9d5e03ea8fcff8e2b27bb895760b44fe3c0dd1b0acdd96048fec37f033)
                check_type(argname="argument allow_origin", value=allow_origin, expected_type=type_hints["allow_origin"])
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "allow_origin": allow_origin,
            }
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_origin(self) -> builtins.str:
            '''``CfnApi.CorsConfigurationProperty.AllowOrigin``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_origin")
            assert result is not None, "Required property 'allow_origin' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnApi.CorsConfigurationProperty.AllowCredentials``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.AllowHeaders``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.AllowMethods``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_age(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.MaxAge``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.DomainConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "domain_name": "domainName",
            "base_path": "basePath",
            "endpoint_configuration": "endpointConfiguration",
            "mutual_tls_authentication": "mutualTlsAuthentication",
            "ownership_verification_certificate_arn": "ownershipVerificationCertificateArn",
            "route53": "route53",
            "security_policy": "securityPolicy",
        },
    )
    class DomainConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            domain_name: builtins.str,
            base_path: typing.Optional[typing.Sequence[builtins.str]] = None,
            endpoint_configuration: typing.Optional[builtins.str] = None,
            mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.MutualTlsAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
            route53: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApi.Route53ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate_arn: ``CfnApi.DomainConfigurationProperty.CertificateArn``.
            :param domain_name: ``CfnApi.DomainConfigurationProperty.DomainName``.
            :param base_path: ``CfnApi.DomainConfigurationProperty.BasePath``.
            :param endpoint_configuration: ``CfnApi.DomainConfigurationProperty.EndpointConfiguration``.
            :param mutual_tls_authentication: ``CfnApi.DomainConfigurationProperty.MutualTlsAuthentication``.
            :param ownership_verification_certificate_arn: ``CfnApi.DomainConfigurationProperty.OwnershipVerificationCertificateArn``.
            :param route53: ``CfnApi.DomainConfigurationProperty.Route53``.
            :param security_policy: ``CfnApi.DomainConfigurationProperty.SecurityPolicy``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                domain_configuration_property = sam.CfnApi.DomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                
                    # the properties below are optional
                    base_path=["basePath"],
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version="truststoreVersion"
                    ),
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    route53=sam.CfnApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f17023b837fd107d56d16f5e6cfb20fb7adb87a282df145943489dacc13318da)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
                check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
                check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
                check_type(argname="argument ownership_verification_certificate_arn", value=ownership_verification_certificate_arn, expected_type=type_hints["ownership_verification_certificate_arn"])
                check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
                check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "domain_name": domain_name,
            }
            if base_path is not None:
                self._values["base_path"] = base_path
            if endpoint_configuration is not None:
                self._values["endpoint_configuration"] = endpoint_configuration
            if mutual_tls_authentication is not None:
                self._values["mutual_tls_authentication"] = mutual_tls_authentication
            if ownership_verification_certificate_arn is not None:
                self._values["ownership_verification_certificate_arn"] = ownership_verification_certificate_arn
            if route53 is not None:
                self._values["route53"] = route53
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''``CfnApi.DomainConfigurationProperty.CertificateArn``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''``CfnApi.DomainConfigurationProperty.DomainName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-domainname
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def base_path(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnApi.DomainConfigurationProperty.BasePath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-basepath
            '''
            result = self._values.get("base_path")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def endpoint_configuration(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.DomainConfigurationProperty.EndpointConfiguration``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-endpointconfiguration
            '''
            result = self._values.get("endpoint_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mutual_tls_authentication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.MutualTlsAuthenticationProperty"]]:
            '''``CfnApi.DomainConfigurationProperty.MutualTlsAuthentication``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-mutualtlsauthentication
            '''
            result = self._values.get("mutual_tls_authentication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.MutualTlsAuthenticationProperty"]], result)

        @builtins.property
        def ownership_verification_certificate_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''``CfnApi.DomainConfigurationProperty.OwnershipVerificationCertificateArn``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-ownershipverificationcertificatearn
            '''
            result = self._values.get("ownership_verification_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def route53(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.Route53ConfigurationProperty"]]:
            '''``CfnApi.DomainConfigurationProperty.Route53``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-route53
            '''
            result = self._values.get("route53")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApi.Route53ConfigurationProperty"]], result)

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.DomainConfigurationProperty.SecurityPolicy``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-domainconfiguration.html#sam-api-domainconfiguration-securitypolicy
            '''
            result = self._values.get("security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "vpc_endpoint_ids": "vpcEndpointIds"},
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param type: ``CfnApi.EndpointConfigurationProperty.Type``.
            :param vpc_endpoint_ids: ``CfnApi.EndpointConfigurationProperty.VpcEndpointIds``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-endpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                endpoint_configuration_property = sam.CfnApi.EndpointConfigurationProperty(
                    type="type",
                    vpc_endpoint_ids=["vpcEndpointIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__072ec80bcc67043294dad0992eac75e08953a9decf4c1e33e36616c0f95db79b)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument vpc_endpoint_ids", value=vpc_endpoint_ids, expected_type=type_hints["vpc_endpoint_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if vpc_endpoint_ids is not None:
                self._values["vpc_endpoint_ids"] = vpc_endpoint_ids

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.EndpointConfigurationProperty.Type``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-endpointconfiguration.html#sam-api-endpointconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_endpoint_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnApi.EndpointConfigurationProperty.VpcEndpointIds``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-endpointconfiguration.html#sam-api-endpointconfiguration-vpcendpointids
            '''
            result = self._values.get("vpc_endpoint_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param truststore_uri: ``CfnApi.MutualTlsAuthenticationProperty.TruststoreUri``.
            :param truststore_version: ``CfnApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                mutual_tls_authentication_property = sam.CfnApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d81afc46b424aae13ba8743df72c104a37810d98e45cce7a47b17147dd26a35d)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.MutualTlsAuthenticationProperty.TruststoreUri``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html#cfn-apigateway-domainname-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html#cfn-apigateway-domainname-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.Route53ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "distributed_domain_name": "distributedDomainName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
            "hosted_zone_name": "hostedZoneName",
            "ip_v6": "ipV6",
        },
    )
    class Route53ConfigurationProperty:
        def __init__(
            self,
            *,
            distributed_domain_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            hosted_zone_name: typing.Optional[builtins.str] = None,
            ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param distributed_domain_name: ``CfnApi.Route53ConfigurationProperty.DistributedDomainName``.
            :param evaluate_target_health: ``CfnApi.Route53ConfigurationProperty.EvaluateTargetHealth``.
            :param hosted_zone_id: ``CfnApi.Route53ConfigurationProperty.HostedZoneId``.
            :param hosted_zone_name: ``CfnApi.Route53ConfigurationProperty.HostedZoneName``.
            :param ip_v6: ``CfnApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                route53_configuration_property = sam.CfnApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75305cc3297379268c8dd98bf8bb8ad2fbe572059ac726e8f3b5494c1819da4a)
                check_type(argname="argument distributed_domain_name", value=distributed_domain_name, expected_type=type_hints["distributed_domain_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
                check_type(argname="argument ip_v6", value=ip_v6, expected_type=type_hints["ip_v6"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if distributed_domain_name is not None:
                self._values["distributed_domain_name"] = distributed_domain_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None:
                self._values["hosted_zone_name"] = hosted_zone_name
            if ip_v6 is not None:
                self._values["ip_v6"] = ip_v6

        @builtins.property
        def distributed_domain_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.Route53ConfigurationProperty.DistributedDomainName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-distributiondomainname
            '''
            result = self._values.get("distributed_domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnApi.Route53ConfigurationProperty.EvaluateTargetHealth``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.Route53ConfigurationProperty.HostedZoneId``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.Route53ConfigurationProperty.HostedZoneName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-hostedzonename
            '''
            result = self._values.get("hosted_zone_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_v6(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-api-route53configuration.html#sam-api-route53configuration-ipv6
            '''
            result = self._values.get("ip_v6")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApi.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: jsii.Number,
        ) -> None:
            '''
            :param bucket: ``CfnApi.S3LocationProperty.Bucket``.
            :param key: ``CfnApi.S3LocationProperty.Key``.
            :param version: ``CfnApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_location_property = sam.CfnApi.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85016dbf64ff1ea193e874533036e451057aa02dcb69dc66eb89086b2fe21ea7)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
                "version": version,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnApi.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnApi.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> jsii.Number:
            '''``CfnApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-sam.CfnApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "stage_name": "stageName",
        "access_log_setting": "accessLogSetting",
        "auth": "auth",
        "binary_media_types": "binaryMediaTypes",
        "cache_cluster_enabled": "cacheClusterEnabled",
        "cache_cluster_size": "cacheClusterSize",
        "canary_setting": "canarySetting",
        "cors": "cors",
        "definition_body": "definitionBody",
        "definition_uri": "definitionUri",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "domain": "domain",
        "endpoint_configuration": "endpointConfiguration",
        "gateway_responses": "gatewayResponses",
        "method_settings": "methodSettings",
        "minimum_compression_size": "minimumCompressionSize",
        "models": "models",
        "name": "name",
        "open_api_version": "openApiVersion",
        "tags": "tags",
        "tracing_enabled": "tracingEnabled",
        "variables": "variables",
    },
)
class CfnApiProps:
    def __init__(
        self,
        *,
        stage_name: builtins.str,
        access_log_setting: typing.Optional[typing.Union[typing.Union[CfnApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.AuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        canary_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.DomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_configuration: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_responses: typing.Any = None,
        method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        models: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        open_api_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApi``.

        :param stage_name: ``AWS::Serverless::Api.StageName``.
        :param access_log_setting: ``AWS::Serverless::Api.AccessLogSetting``.
        :param auth: ``AWS::Serverless::Api.Auth``.
        :param binary_media_types: ``AWS::Serverless::Api.BinaryMediaTypes``.
        :param cache_cluster_enabled: ``AWS::Serverless::Api.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::Serverless::Api.CacheClusterSize``.
        :param canary_setting: ``AWS::Serverless::Api.CanarySetting``.
        :param cors: ``AWS::Serverless::Api.Cors``.
        :param definition_body: ``AWS::Serverless::Api.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::Api.DefinitionUri``.
        :param description: ``AWS::Serverless::Api.Description``.
        :param disable_execute_api_endpoint: ``AWS::Serverless::Api.DisableExecuteApiEndpoint``.
        :param domain: ``AWS::Serverless::Api.Domain``.
        :param endpoint_configuration: ``AWS::Serverless::Api.EndpointConfiguration``.
        :param gateway_responses: ``AWS::Serverless::Api.GatewayResponses``.
        :param method_settings: ``AWS::Serverless::Api.MethodSettings``.
        :param minimum_compression_size: ``AWS::Serverless::Api.MinimumCompressionSize``.
        :param models: ``AWS::Serverless::Api.Models``.
        :param name: ``AWS::Serverless::Api.Name``.
        :param open_api_version: ``AWS::Serverless::Api.OpenApiVersion``.
        :param tags: ``AWS::Serverless::Api.Tags``.
        :param tracing_enabled: ``AWS::Serverless::Api.TracingEnabled``.
        :param variables: ``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_sam as sam
            
            # authorizers: Any
            # definition_body: Any
            # gateway_responses: Any
            # method_settings: Any
            # models: Any
            
            cfn_api_props = sam.CfnApiProps(
                stage_name="stageName",
            
                # the properties below are optional
                access_log_setting=sam.CfnApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                auth=sam.CfnApi.AuthProperty(
                    add_default_authorizer_to_cors_preflight=False,
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                ),
                binary_media_types=["binaryMediaTypes"],
                cache_cluster_enabled=False,
                cache_cluster_size="cacheClusterSize",
                canary_setting=sam.CfnApi.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                ),
                cors="cors",
                definition_body=definition_body,
                definition_uri="definitionUri",
                description="description",
                disable_execute_api_endpoint=False,
                domain=sam.CfnApi.DomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
            
                    # the properties below are optional
                    base_path=["basePath"],
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version="truststoreVersion"
                    ),
                    ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                    route53=sam.CfnApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                ),
                endpoint_configuration="endpointConfiguration",
                gateway_responses=gateway_responses,
                method_settings=[method_settings],
                minimum_compression_size=123,
                models=models,
                name="name",
                open_api_version="openApiVersion",
                tags={
                    "tags_key": "tags"
                },
                tracing_enabled=False,
                variables={
                    "variables_key": "variables"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39db9f20be1c63fd66760448d9c4cd306f8d6a772a64376f2ebd70019bff4be3)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument cache_cluster_enabled", value=cache_cluster_enabled, expected_type=type_hints["cache_cluster_enabled"])
            check_type(argname="argument cache_cluster_size", value=cache_cluster_size, expected_type=type_hints["cache_cluster_size"])
            check_type(argname="argument canary_setting", value=canary_setting, expected_type=type_hints["canary_setting"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument gateway_responses", value=gateway_responses, expected_type=type_hints["gateway_responses"])
            check_type(argname="argument method_settings", value=method_settings, expected_type=type_hints["method_settings"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
            check_type(argname="argument models", value=models, expected_type=type_hints["models"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument open_api_version", value=open_api_version, expected_type=type_hints["open_api_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing_enabled", value=tracing_enabled, expected_type=type_hints["tracing_enabled"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage_name": stage_name,
        }
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if auth is not None:
            self._values["auth"] = auth
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if cache_cluster_enabled is not None:
            self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None:
            self._values["cache_cluster_size"] = cache_cluster_size
        if canary_setting is not None:
            self._values["canary_setting"] = canary_setting
        if cors is not None:
            self._values["cors"] = cors
        if definition_body is not None:
            self._values["definition_body"] = definition_body
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if domain is not None:
            self._values["domain"] = domain
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if gateway_responses is not None:
            self._values["gateway_responses"] = gateway_responses
        if method_settings is not None:
            self._values["method_settings"] = method_settings
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size
        if models is not None:
            self._values["models"] = models
        if name is not None:
            self._values["name"] = name
        if open_api_version is not None:
            self._values["open_api_version"] = open_api_version
        if tags is not None:
            self._values["tags"] = tags
        if tracing_enabled is not None:
            self._values["tracing_enabled"] = tracing_enabled
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''``AWS::Serverless::Api.StageName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.AccessLogSetting``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.AuthProperty]]:
        '''``AWS::Serverless::Api.Auth``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.AuthProperty]], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Api.BinaryMediaTypes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.CacheClusterEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cache_cluster_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.CacheClusterSize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cache_cluster_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def canary_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.CanarySettingProperty]]:
        '''``AWS::Serverless::Api.CanarySetting``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-canarysetting
        '''
        result = self._values.get("canary_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.CanarySettingProperty]], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.CorsConfigurationProperty]]:
        '''``AWS::Serverless::Api.Cors``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.CorsConfigurationProperty]], result)

    @builtins.property
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::Api.DefinitionBody``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("definition_body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.S3LocationProperty]]:
        '''``AWS::Serverless::Api.DefinitionUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.S3LocationProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Description``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.DisableExecuteApiEndpoint``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-disableexecuteapiendpoint
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.DomainConfigurationProperty]]:
        '''``AWS::Serverless::Api.Domain``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.DomainConfigurationProperty]], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.EndpointConfigurationProperty]]:
        '''``AWS::Serverless::Api.EndpointConfiguration``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.EndpointConfigurationProperty]], result)

    @builtins.property
    def gateway_responses(self) -> typing.Any:
        '''``AWS::Serverless::Api.GatewayResponses``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-gatewayresponses
        '''
        result = self._values.get("gateway_responses")
        return typing.cast(typing.Any, result)

    @builtins.property
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.MethodSettings``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("method_settings")
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Api.MinimumCompressionSize``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-minimumcompressionsize
        '''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Any:
        '''``AWS::Serverless::Api.Models``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-api.html#sam-api-models
        '''
        result = self._values.get("models")
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Name``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_api_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.OpenApiVersion``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("open_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Api.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::Api.TracingEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("tracing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-sam.CfnApplication",
):
    '''A CloudFormation ``AWS::Serverless::Application``.

    :cloudformationResource: AWS::Serverless::Application
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_sam as sam
        
        cfn_application = sam.CfnApplication(self, "MyCfnApplication",
            location="location",
        
            # the properties below are optional
            notification_arns=["notificationArns"],
            parameters={
                "parameters_key": "parameters"
            },
            tags={
                "tags_key": "tags"
            },
            timeout_in_minutes=123
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        location: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.ApplicationLocationProperty", typing.Dict[builtins.str, typing.Any]]],
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param location: ``AWS::Serverless::Application.Location``.
        :param notification_arns: ``AWS::Serverless::Application.NotificationArns``.
        :param parameters: ``AWS::Serverless::Application.Parameters``.
        :param tags: ``AWS::Serverless::Application.Tags``.
        :param timeout_in_minutes: ``AWS::Serverless::Application.TimeoutInMinutes``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a343a3e83f97d9d93c193422a6395bb49b89c851d5d13820cc4ee0800c7ca3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            location=location,
            notification_arns=notification_arns,
            parameters=parameters,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f520d3639843237397ada9766a893543dd0d3e005ce1121f8d23c4457186d0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed275051854e188557b1cb332d8f8c9f605d9d1bbc94d3b9bf472343e18001f1)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::Serverless::Application.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApplication.ApplicationLocationProperty"]:
        '''``AWS::Serverless::Application.Location``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApplication.ApplicationLocationProperty"], jsii.get(self, "location"))

    @location.setter
    def location(
        self,
        value: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnApplication.ApplicationLocationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2021f9bfcbae40db46b5ff3fe9b5ffa597a32142707941c05bd5e8b7dca936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Application.NotificationArns``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationArns"))

    @notification_arns.setter
    def notification_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b6d091b94332e4b410a7b83a02b04df28080de0f2030a64b36cf0c8491302d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationArns", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Application.Parameters``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f44826d3a5ceb952ba5cd138018646d6bc75d031bd65d9d35eaf336ff72e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinutes"))

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c34a139ee36720735b4fc3c16ef445bbc5726cdef6c17a7764720b273808f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInMinutes", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnApplication.ApplicationLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_id": "applicationId",
            "semantic_version": "semanticVersion",
        },
    )
    class ApplicationLocationProperty:
        def __init__(
            self,
            *,
            application_id: builtins.str,
            semantic_version: builtins.str,
        ) -> None:
            '''
            :param application_id: ``CfnApplication.ApplicationLocationProperty.ApplicationId``.
            :param semantic_version: ``CfnApplication.ApplicationLocationProperty.SemanticVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                application_location_property = sam.CfnApplication.ApplicationLocationProperty(
                    application_id="applicationId",
                    semantic_version="semanticVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b641da8159ee8d1fbd4b614775c4c892c709f7b892ea81e0f0eef0693bca4da)
                check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
                check_type(argname="argument semantic_version", value=semantic_version, expected_type=type_hints["semantic_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "application_id": application_id,
                "semantic_version": semantic_version,
            }

        @builtins.property
        def application_id(self) -> builtins.str:
            '''``CfnApplication.ApplicationLocationProperty.ApplicationId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            '''
            result = self._values.get("application_id")
            assert result is not None, "Required property 'application_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def semantic_version(self) -> builtins.str:
            '''``CfnApplication.ApplicationLocationProperty.SemanticVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            '''
            result = self._values.get("semantic_version")
            assert result is not None, "Required property 'semantic_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-sam.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        location: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.ApplicationLocationProperty, typing.Dict[builtins.str, typing.Any]]],
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param location: ``AWS::Serverless::Application.Location``.
        :param notification_arns: ``AWS::Serverless::Application.NotificationArns``.
        :param parameters: ``AWS::Serverless::Application.Parameters``.
        :param tags: ``AWS::Serverless::Application.Tags``.
        :param timeout_in_minutes: ``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_sam as sam
            
            cfn_application_props = sam.CfnApplicationProps(
                location="location",
            
                # the properties below are optional
                notification_arns=["notificationArns"],
                parameters={
                    "parameters_key": "parameters"
                },
                tags={
                    "tags_key": "tags"
                },
                timeout_in_minutes=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb277e43ded51f14816e267ec09f1dd736bcb4fe2b928556bca0f020670774c)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def location(
        self,
    ) -> typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApplication.ApplicationLocationProperty]:
        '''``AWS::Serverless::Application.Location``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApplication.ApplicationLocationProperty], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Application.NotificationArns``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Application.Parameters``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Application.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFunction(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-sam.CfnFunction",
):
    '''A CloudFormation ``AWS::Serverless::Function``.

    :cloudformationResource: AWS::Serverless::Function
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_sam as sam
        
        # assume_role_policy_document: Any
        
        cfn_function = sam.CfnFunction(self, "MyCfnFunction",
            architectures=["architectures"],
            assume_role_policy_document=assume_role_policy_document,
            auto_publish_alias="autoPublishAlias",
            auto_publish_code_sha256="autoPublishCodeSha256",
            code_signing_config_arn="codeSigningConfigArn",
            code_uri="codeUri",
            dead_letter_queue=sam.CfnFunction.DeadLetterQueueProperty(
                target_arn="targetArn",
                type="type"
            ),
            deployment_preference=sam.CfnFunction.DeploymentPreferenceProperty(
                enabled=False,
                type="type",
        
                # the properties below are optional
                alarms=["alarms"],
                hooks=sam.CfnFunction.HooksProperty(
                    post_traffic="postTraffic",
                    pre_traffic="preTraffic"
                )
            ),
            description="description",
            environment=sam.CfnFunction.FunctionEnvironmentProperty(
                variables={
                    "variables_key": "variables"
                }
            ),
            event_invoke_config=sam.CfnFunction.EventInvokeConfigProperty(
                destination_config=sam.CfnFunction.EventInvokeDestinationConfigProperty(
                    on_failure=sam.CfnFunction.DestinationProperty(
                        destination="destination",
        
                        # the properties below are optional
                        type="type"
                    ),
                    on_success=sam.CfnFunction.DestinationProperty(
                        destination="destination",
        
                        # the properties below are optional
                        type="type"
                    )
                ),
                maximum_event_age_in_seconds=123,
                maximum_retry_attempts=123
            ),
            events={
                "events_key": sam.CfnFunction.EventSourceProperty(
                    properties=sam.CfnFunction.S3EventProperty(
                        variables={
                            "variables_key": "variables"
                        }
                    ),
                    type="type"
                )
            },
            file_system_configs=[sam.CfnFunction.FileSystemConfigProperty(
                arn="arn",
                local_mount_path="localMountPath"
            )],
            function_name="functionName",
            handler="handler",
            image_config=sam.CfnFunction.ImageConfigProperty(
                command=["command"],
                entry_point=["entryPoint"],
                working_directory="workingDirectory"
            ),
            image_uri="imageUri",
            inline_code="inlineCode",
            kms_key_arn="kmsKeyArn",
            layers=["layers"],
            memory_size=123,
            package_type="packageType",
            permissions_boundary="permissionsBoundary",
            policies="policies",
            provisioned_concurrency_config=sam.CfnFunction.ProvisionedConcurrencyConfigProperty(
                provisioned_concurrent_executions="provisionedConcurrentExecutions"
            ),
            reserved_concurrent_executions=123,
            role="role",
            runtime="runtime",
            tags={
                "tags_key": "tags"
            },
            timeout=123,
            tracing="tracing",
            version_description="versionDescription",
            vpc_config=sam.CfnFunction.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_policy_document: typing.Any = None,
        auto_publish_alias: typing.Optional[builtins.str] = None,
        auto_publish_code_sha256: typing.Optional[builtins.str] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        code_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.DeadLetterQueueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_preference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.DeploymentPreferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.FunctionEnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        event_invoke_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EventInvokeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EventSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.FileSystemConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.ImageConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        inline_code: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.SAMPolicyTemplateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing: typing.Optional[builtins.str] = None,
        version_description: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Function``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param architectures: ``AWS::Serverless::Function.Architectures``.
        :param assume_role_policy_document: ``AWS::Serverless::Function.AssumeRolePolicyDocument``.
        :param auto_publish_alias: ``AWS::Serverless::Function.AutoPublishAlias``.
        :param auto_publish_code_sha256: ``AWS::Serverless::Function.AutoPublishCodeSha256``.
        :param code_signing_config_arn: ``AWS::Serverless::Function.CodeSigningConfigArn``.
        :param code_uri: ``AWS::Serverless::Function.CodeUri``.
        :param dead_letter_queue: ``AWS::Serverless::Function.DeadLetterQueue``.
        :param deployment_preference: ``AWS::Serverless::Function.DeploymentPreference``.
        :param description: ``AWS::Serverless::Function.Description``.
        :param environment: ``AWS::Serverless::Function.Environment``.
        :param event_invoke_config: ``AWS::Serverless::Function.EventInvokeConfig``.
        :param events: ``AWS::Serverless::Function.Events``.
        :param file_system_configs: ``AWS::Serverless::Function.FileSystemConfigs``.
        :param function_name: ``AWS::Serverless::Function.FunctionName``.
        :param handler: ``AWS::Serverless::Function.Handler``.
        :param image_config: ``AWS::Serverless::Function.ImageConfig``.
        :param image_uri: ``AWS::Serverless::Function.ImageUri``.
        :param inline_code: ``AWS::Serverless::Function.InlineCode``.
        :param kms_key_arn: ``AWS::Serverless::Function.KmsKeyArn``.
        :param layers: ``AWS::Serverless::Function.Layers``.
        :param memory_size: ``AWS::Serverless::Function.MemorySize``.
        :param package_type: ``AWS::Serverless::Function.PackageType``.
        :param permissions_boundary: ``AWS::Serverless::Function.PermissionsBoundary``.
        :param policies: ``AWS::Serverless::Function.Policies``.
        :param provisioned_concurrency_config: ``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.
        :param reserved_concurrent_executions: ``AWS::Serverless::Function.ReservedConcurrentExecutions``.
        :param role: ``AWS::Serverless::Function.Role``.
        :param runtime: ``AWS::Serverless::Function.Runtime``.
        :param tags: ``AWS::Serverless::Function.Tags``.
        :param timeout: ``AWS::Serverless::Function.Timeout``.
        :param tracing: ``AWS::Serverless::Function.Tracing``.
        :param version_description: ``AWS::Serverless::Function.VersionDescription``.
        :param vpc_config: ``AWS::Serverless::Function.VpcConfig``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505a349cfb16b4f61d5eb6fc256d8fb156607f06908381cdde8969bb46450ba3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFunctionProps(
            architectures=architectures,
            assume_role_policy_document=assume_role_policy_document,
            auto_publish_alias=auto_publish_alias,
            auto_publish_code_sha256=auto_publish_code_sha256,
            code_signing_config_arn=code_signing_config_arn,
            code_uri=code_uri,
            dead_letter_queue=dead_letter_queue,
            deployment_preference=deployment_preference,
            description=description,
            environment=environment,
            event_invoke_config=event_invoke_config,
            events=events,
            file_system_configs=file_system_configs,
            function_name=function_name,
            handler=handler,
            image_config=image_config,
            image_uri=image_uri,
            inline_code=inline_code,
            kms_key_arn=kms_key_arn,
            layers=layers,
            memory_size=memory_size,
            package_type=package_type,
            permissions_boundary=permissions_boundary,
            policies=policies,
            provisioned_concurrency_config=provisioned_concurrency_config,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            runtime=runtime,
            tags=tags,
            timeout=timeout,
            tracing=tracing,
            version_description=version_description,
            vpc_config=vpc_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a227194132dfe866713746563a00a663c842203935c64a01a26b33a81edf5b69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29cffd0372540845a716d399bb94950623018ba38dd7c46151578398f85a3747)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::Serverless::Function.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicyDocument")
    def assume_role_policy_document(self) -> typing.Any:
        '''``AWS::Serverless::Function.AssumeRolePolicyDocument``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-assumerolepolicydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "assumeRolePolicyDocument"))

    @assume_role_policy_document.setter
    def assume_role_policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76580041999f072f492b36f9f65a08fc1b42d11508b005f3225eaf5ef8f238b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assumeRolePolicyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="architectures")
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Architectures``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-architectures
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "architectures"))

    @architectures.setter
    def architectures(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33bf4a91f9732d689ee90ea47005ae964231a599e4d3e49c8013f79735b0ef10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architectures", value)

    @builtins.property
    @jsii.member(jsii_name="autoPublishAlias")
    def auto_publish_alias(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishAlias``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoPublishAlias"))

    @auto_publish_alias.setter
    def auto_publish_alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e390b835809cd50e78aa4b1bda3a9996c9c184b36c6d04286baa0c23851256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPublishAlias", value)

    @builtins.property
    @jsii.member(jsii_name="autoPublishCodeSha256")
    def auto_publish_code_sha256(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishCodeSha256``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-autopublishcodesha256
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoPublishCodeSha256"))

    @auto_publish_code_sha256.setter
    def auto_publish_code_sha256(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b451223c0f7d15179172ad63de0a5d06d9866e36504647e521bf77a2694a69a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPublishCodeSha256", value)

    @builtins.property
    @jsii.member(jsii_name="codeSigningConfigArn")
    def code_signing_config_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.CodeSigningConfigArn``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-codesigningconfigarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeSigningConfigArn"))

    @code_signing_config_arn.setter
    def code_signing_config_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6df8ec87cd12678f51746f0b53c0f25e5981327219ab9ba1fbea3df88ae5ba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeSigningConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="codeUri")
    def code_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3LocationProperty"]]:
        '''``AWS::Serverless::Function.CodeUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3LocationProperty"]], jsii.get(self, "codeUri"))

    @code_uri.setter
    def code_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4bd2ba4df045757c62a7a481b38179de040c42e9e1a40d9d640d42c4866833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeUri", value)

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DeadLetterQueueProperty"]]:
        '''``AWS::Serverless::Function.DeadLetterQueue``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DeadLetterQueueProperty"]], jsii.get(self, "deadLetterQueue"))

    @dead_letter_queue.setter
    def dead_letter_queue(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DeadLetterQueueProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c58e3d550bd7ad1d9f6a0e5bdb8a3831eaca0e46b144e61c108274e5380fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetterQueue", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentPreference")
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DeploymentPreferenceProperty"]]:
        '''``AWS::Serverless::Function.DeploymentPreference``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DeploymentPreferenceProperty"]], jsii.get(self, "deploymentPreference"))

    @deployment_preference.setter
    def deployment_preference(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DeploymentPreferenceProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1788f527a96924817e15c7d6a4847759fcd0864c76ad9f93c96753bbf2ebe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentPreference", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad8bf22ffe6be903d3107eb15f39f5f2962ba64f19f25d5b0b31fbf1efe2776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FunctionEnvironmentProperty"]]:
        '''``AWS::Serverless::Function.Environment``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FunctionEnvironmentProperty"]], jsii.get(self, "environment"))

    @environment.setter
    def environment(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FunctionEnvironmentProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234f08981bde3f79478a4388ecdc87a46d05e0a06a7af842d2a88f3dbd1e1022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="eventInvokeConfig")
    def event_invoke_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventInvokeConfigProperty"]]:
        '''``AWS::Serverless::Function.EventInvokeConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventInvokeConfigProperty"]], jsii.get(self, "eventInvokeConfig"))

    @event_invoke_config.setter
    def event_invoke_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventInvokeConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad1444528ee74e5cbb13a5b9e2fa5aeb3518dab168ecc948b77139a55cc1c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventInvokeConfig", value)

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventSourceProperty"]]]]:
        '''``AWS::Serverless::Function.Events``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventSourceProperty"]]]], jsii.get(self, "events"))

    @events.setter
    def events(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventSourceProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c9cd896e5e0ecd9a144131cc87358cccc14d4b052179c3a859f6f6276e5794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="fileSystemConfigs")
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FileSystemConfigProperty"]]]]:
        '''``AWS::Serverless::Function.FileSystemConfigs``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FileSystemConfigProperty"]]]], jsii.get(self, "fileSystemConfigs"))

    @file_system_configs.setter
    def file_system_configs(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FileSystemConfigProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21dbfdc88b8a5bea5035814d4664b1760ee5412249aee7664aaa0b2d9f0918b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemConfigs", value)

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.FunctionName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028f4b2030c1c133e39e86f2783cf06fdc925952146135e8443c51451dd106d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Handler``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e7e62384916af4852d8e1dd7f913f33c092cac8fcb0ca4dfbef09ec383c0b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value)

    @builtins.property
    @jsii.member(jsii_name="imageConfig")
    def image_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ImageConfigProperty"]]:
        '''``AWS::Serverless::Function.ImageConfig``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ImageConfigProperty"]], jsii.get(self, "imageConfig"))

    @image_config.setter
    def image_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ImageConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2230d1734a7b9da889259f70dad490f0ca538951ea1f7056ce1c26e0fcae7c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageConfig", value)

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.ImageUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageuri
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424c0d1a53594d96bfd88d7573631584f56da5bad3ffaf1b571809511b7de5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value)

    @builtins.property
    @jsii.member(jsii_name="inlineCode")
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.InlineCode``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineCode"))

    @inline_code.setter
    def inline_code(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b2b96b28e91d6f213ab3b9a43973c4ca6815a6f76cc98bd78f65771ed3f9c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inlineCode", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.KmsKeyArn``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b456f08d239c4a271736e7d954be37f7b38c186486f4b32a3ce40277b2ab6d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="layers")
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Layers``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "layers"))

    @layers.setter
    def layers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67eb0c86ad1b7c5202a15285e7dde55f0979951e96873e3e6cc29a17bf39663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layers", value)

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.MemorySize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySize"))

    @memory_size.setter
    def memory_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05bfc2a7244ed92a6f592193bb6072aae9644d417ff8c5f521bf53db0bda9b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySize", value)

    @builtins.property
    @jsii.member(jsii_name="packageType")
    def package_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PackageType``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-packagetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packageType"))

    @package_type.setter
    def package_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973b2a580bfb638fecb045c1fd744507df1c7d9a85839a588766113d96616865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageType", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PermissionsBoundary``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundary"))

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50bcfcfd17eacdb1bf85855e2cf03c4f2e2a3cace148c201d8fa7242782b548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty"]]]]:
        '''``AWS::Serverless::Function.Policies``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty"]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e7694797db1cfa76973fb57894a799db73498f1a9dd6f800b34bcd2fdbcef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ProvisionedConcurrencyConfigProperty"]]:
        '''``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ProvisionedConcurrencyConfigProperty"]], jsii.get(self, "provisionedConcurrencyConfig"))

    @provisioned_concurrency_config.setter
    def provisioned_concurrency_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ProvisionedConcurrencyConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f5759e0c4fea49027eb19472ba127da2c5032562f40c702122c2753b119d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedConcurrencyConfig", value)

    @builtins.property
    @jsii.member(jsii_name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.ReservedConcurrentExecutions``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "reservedConcurrentExecutions"))

    @reserved_concurrent_executions.setter
    def reserved_concurrent_executions(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87392f1094016feca6eec09ae2aec6e1ac75e33d20ebf897c55d2817c2efe10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedConcurrentExecutions", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Role``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "role"))

    @role.setter
    def role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab904502f3c8fa1dca06625bb988d7c79f6b229d52186659fd9fffef26c6c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Runtime``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5bc2e3af5c3d51fe4d46357f74f3c3916105e17f01a00c24dc6f57aed89cf63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.Timeout``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387c52e3fbac88c4135b39eb406d9524730796f480b0bab3630baed1b2b2c9ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="tracing")
    def tracing(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Tracing``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tracing"))

    @tracing.setter
    def tracing(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008f4327b6919d0d11762096a2818d6dbf34b01371e2b97d754848be9dfa2aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracing", value)

    @builtins.property
    @jsii.member(jsii_name="versionDescription")
    def version_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.VersionDescription``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDescription"))

    @version_description.setter
    def version_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a353be62be3f5f2e5c4362ee791fecab56369588b6948164cb781d4c6b0636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDescription", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.VpcConfigProperty"]]:
        '''``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.VpcConfigProperty"]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.VpcConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1771ccb6d43e47ac4623b10131885d7b6fde17c2a8e6b0d1b6dd0e5022b118b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.AlexaSkillEventProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class AlexaSkillEventProperty:
        def __init__(
            self,
            *,
            variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''
            :param variables: ``CfnFunction.AlexaSkillEventProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#alexaskill
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                alexa_skill_event_property = sam.CfnFunction.AlexaSkillEventProperty(
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9aa8e4d52af5790a383a1dfd1478c609a053549a865d144b6b5f03f23918df8f)
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnFunction.AlexaSkillEventProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#alexaskill
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlexaSkillEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "method": "method",
            "path": "path",
            "auth": "auth",
            "request_model": "requestModel",
            "request_parameters": "requestParameters",
            "rest_api_id": "restApiId",
        },
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            method: builtins.str,
            path: builtins.str,
            auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.AuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            request_model: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.RequestModelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            request_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.RequestParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param method: ``CfnFunction.ApiEventProperty.Method``.
            :param path: ``CfnFunction.ApiEventProperty.Path``.
            :param auth: ``CfnFunction.ApiEventProperty.Auth``.
            :param request_model: ``CfnFunction.ApiEventProperty.RequestModel``.
            :param request_parameters: ``CfnFunction.ApiEventProperty.RequestParameters``.
            :param rest_api_id: ``CfnFunction.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # custom_statements: Any
                
                api_event_property = sam.CfnFunction.ApiEventProperty(
                    method="method",
                    path="path",
                
                    # the properties below are optional
                    auth=sam.CfnFunction.AuthProperty(
                        api_key_required=False,
                        authorization_scopes=["authorizationScopes"],
                        authorizer="authorizer",
                        resource_policy=sam.CfnFunction.AuthResourcePolicyProperty(
                            aws_account_blacklist=["awsAccountBlacklist"],
                            aws_account_whitelist=["awsAccountWhitelist"],
                            custom_statements=[custom_statements],
                            intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                            intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                            intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                            intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                            ip_range_blacklist=["ipRangeBlacklist"],
                            ip_range_whitelist=["ipRangeWhitelist"],
                            source_vpc_blacklist=["sourceVpcBlacklist"],
                            source_vpc_whitelist=["sourceVpcWhitelist"]
                        )
                    ),
                    request_model=sam.CfnFunction.RequestModelProperty(
                        model="model",
                
                        # the properties below are optional
                        required=False,
                        validate_body=False,
                        validate_parameters=False
                    ),
                    request_parameters=["requestParameters"],
                    rest_api_id="restApiId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f01b62e6b0363b01eee2250f5756042c7d680f54357d2a4d2505edeff168b249)
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
                check_type(argname="argument request_model", value=request_model, expected_type=type_hints["request_model"])
                check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "method": method,
                "path": path,
            }
            if auth is not None:
                self._values["auth"] = auth
            if request_model is not None:
                self._values["request_model"] = request_model
            if request_parameters is not None:
                self._values["request_parameters"] = request_parameters
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def method(self) -> builtins.str:
            '''``CfnFunction.ApiEventProperty.Method``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("method")
            assert result is not None, "Required property 'method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnFunction.ApiEventProperty.Path``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.AuthProperty"]]:
            '''``CfnFunction.ApiEventProperty.Auth``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("auth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.AuthProperty"]], result)

        @builtins.property
        def request_model(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.RequestModelProperty"]]:
            '''``CfnFunction.ApiEventProperty.RequestModel``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("request_model")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.RequestModelProperty"]], result)

        @builtins.property
        def request_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.RequestParameterProperty"]]]]:
            '''``CfnFunction.ApiEventProperty.RequestParameters``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("request_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnFunction.RequestParameterProperty"]]]], result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.AuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_key_required": "apiKeyRequired",
            "authorization_scopes": "authorizationScopes",
            "authorizer": "authorizer",
            "resource_policy": "resourcePolicy",
        },
    )
    class AuthProperty:
        def __init__(
            self,
            *,
            api_key_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            authorizer: typing.Optional[builtins.str] = None,
            resource_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.AuthResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param api_key_required: ``CfnFunction.AuthProperty.ApiKeyRequired``.
            :param authorization_scopes: ``CfnFunction.AuthProperty.AuthorizationScopes``.
            :param authorizer: ``CfnFunction.AuthProperty.Authorizer``.
            :param resource_policy: ``CfnFunction.AuthProperty.ResourcePolicy``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # custom_statements: Any
                
                auth_property = sam.CfnFunction.AuthProperty(
                    api_key_required=False,
                    authorization_scopes=["authorizationScopes"],
                    authorizer="authorizer",
                    resource_policy=sam.CfnFunction.AuthResourcePolicyProperty(
                        aws_account_blacklist=["awsAccountBlacklist"],
                        aws_account_whitelist=["awsAccountWhitelist"],
                        custom_statements=[custom_statements],
                        intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                        intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                        intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                        intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                        ip_range_blacklist=["ipRangeBlacklist"],
                        ip_range_whitelist=["ipRangeWhitelist"],
                        source_vpc_blacklist=["sourceVpcBlacklist"],
                        source_vpc_whitelist=["sourceVpcWhitelist"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87133f3259f76a6ebba1a6812adeb658d79861f803a3d59b362b9f4165f41841)
                check_type(argname="argument api_key_required", value=api_key_required, expected_type=type_hints["api_key_required"])
                check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
                check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
                check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key_required is not None:
                self._values["api_key_required"] = api_key_required
            if authorization_scopes is not None:
                self._values["authorization_scopes"] = authorization_scopes
            if authorizer is not None:
                self._values["authorizer"] = authorizer
            if resource_policy is not None:
                self._values["resource_policy"] = resource_policy

        @builtins.property
        def api_key_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.AuthProperty.ApiKeyRequired``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("api_key_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthProperty.AuthorizationScopes``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("authorization_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.AuthProperty.Authorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.AuthResourcePolicyProperty"]]:
            '''``CfnFunction.AuthProperty.ResourcePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("resource_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.AuthResourcePolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.AuthResourcePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_blacklist": "awsAccountBlacklist",
            "aws_account_whitelist": "awsAccountWhitelist",
            "custom_statements": "customStatements",
            "intrinsic_vpc_blacklist": "intrinsicVpcBlacklist",
            "intrinsic_vpce_blacklist": "intrinsicVpceBlacklist",
            "intrinsic_vpce_whitelist": "intrinsicVpceWhitelist",
            "intrinsic_vpc_whitelist": "intrinsicVpcWhitelist",
            "ip_range_blacklist": "ipRangeBlacklist",
            "ip_range_whitelist": "ipRangeWhitelist",
            "source_vpc_blacklist": "sourceVpcBlacklist",
            "source_vpc_whitelist": "sourceVpcWhitelist",
        },
    )
    class AuthResourcePolicyProperty:
        def __init__(
            self,
            *,
            aws_account_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            aws_account_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            custom_statements: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
            intrinsic_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpce_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpce_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            intrinsic_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            ip_range_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            ip_range_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param aws_account_blacklist: ``CfnFunction.AuthResourcePolicyProperty.AwsAccountBlacklist``.
            :param aws_account_whitelist: ``CfnFunction.AuthResourcePolicyProperty.AwsAccountWhitelist``.
            :param custom_statements: ``CfnFunction.AuthResourcePolicyProperty.CustomStatements``.
            :param intrinsic_vpc_blacklist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcBlacklist``.
            :param intrinsic_vpce_blacklist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceBlacklist``.
            :param intrinsic_vpce_whitelist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceWhitelist``.
            :param intrinsic_vpc_whitelist: ``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcWhitelist``.
            :param ip_range_blacklist: ``CfnFunction.AuthResourcePolicyProperty.IpRangeBlacklist``.
            :param ip_range_whitelist: ``CfnFunction.AuthResourcePolicyProperty.IpRangeWhitelist``.
            :param source_vpc_blacklist: ``CfnFunction.AuthResourcePolicyProperty.SourceVpcBlacklist``.
            :param source_vpc_whitelist: ``CfnFunction.AuthResourcePolicyProperty.SourceVpcWhitelist``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # custom_statements: Any
                
                auth_resource_policy_property = sam.CfnFunction.AuthResourcePolicyProperty(
                    aws_account_blacklist=["awsAccountBlacklist"],
                    aws_account_whitelist=["awsAccountWhitelist"],
                    custom_statements=[custom_statements],
                    intrinsic_vpc_blacklist=["intrinsicVpcBlacklist"],
                    intrinsic_vpce_blacklist=["intrinsicVpceBlacklist"],
                    intrinsic_vpce_whitelist=["intrinsicVpceWhitelist"],
                    intrinsic_vpc_whitelist=["intrinsicVpcWhitelist"],
                    ip_range_blacklist=["ipRangeBlacklist"],
                    ip_range_whitelist=["ipRangeWhitelist"],
                    source_vpc_blacklist=["sourceVpcBlacklist"],
                    source_vpc_whitelist=["sourceVpcWhitelist"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76e1719e91bb3aa43d03f49e79361f664be04f825b046eb0ce2a1f8de1980016)
                check_type(argname="argument aws_account_blacklist", value=aws_account_blacklist, expected_type=type_hints["aws_account_blacklist"])
                check_type(argname="argument aws_account_whitelist", value=aws_account_whitelist, expected_type=type_hints["aws_account_whitelist"])
                check_type(argname="argument custom_statements", value=custom_statements, expected_type=type_hints["custom_statements"])
                check_type(argname="argument intrinsic_vpc_blacklist", value=intrinsic_vpc_blacklist, expected_type=type_hints["intrinsic_vpc_blacklist"])
                check_type(argname="argument intrinsic_vpce_blacklist", value=intrinsic_vpce_blacklist, expected_type=type_hints["intrinsic_vpce_blacklist"])
                check_type(argname="argument intrinsic_vpce_whitelist", value=intrinsic_vpce_whitelist, expected_type=type_hints["intrinsic_vpce_whitelist"])
                check_type(argname="argument intrinsic_vpc_whitelist", value=intrinsic_vpc_whitelist, expected_type=type_hints["intrinsic_vpc_whitelist"])
                check_type(argname="argument ip_range_blacklist", value=ip_range_blacklist, expected_type=type_hints["ip_range_blacklist"])
                check_type(argname="argument ip_range_whitelist", value=ip_range_whitelist, expected_type=type_hints["ip_range_whitelist"])
                check_type(argname="argument source_vpc_blacklist", value=source_vpc_blacklist, expected_type=type_hints["source_vpc_blacklist"])
                check_type(argname="argument source_vpc_whitelist", value=source_vpc_whitelist, expected_type=type_hints["source_vpc_whitelist"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_blacklist is not None:
                self._values["aws_account_blacklist"] = aws_account_blacklist
            if aws_account_whitelist is not None:
                self._values["aws_account_whitelist"] = aws_account_whitelist
            if custom_statements is not None:
                self._values["custom_statements"] = custom_statements
            if intrinsic_vpc_blacklist is not None:
                self._values["intrinsic_vpc_blacklist"] = intrinsic_vpc_blacklist
            if intrinsic_vpce_blacklist is not None:
                self._values["intrinsic_vpce_blacklist"] = intrinsic_vpce_blacklist
            if intrinsic_vpce_whitelist is not None:
                self._values["intrinsic_vpce_whitelist"] = intrinsic_vpce_whitelist
            if intrinsic_vpc_whitelist is not None:
                self._values["intrinsic_vpc_whitelist"] = intrinsic_vpc_whitelist
            if ip_range_blacklist is not None:
                self._values["ip_range_blacklist"] = ip_range_blacklist
            if ip_range_whitelist is not None:
                self._values["ip_range_whitelist"] = ip_range_whitelist
            if source_vpc_blacklist is not None:
                self._values["source_vpc_blacklist"] = source_vpc_blacklist
            if source_vpc_whitelist is not None:
                self._values["source_vpc_whitelist"] = source_vpc_whitelist

        @builtins.property
        def aws_account_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.AwsAccountBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("aws_account_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def aws_account_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.AwsAccountWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("aws_account_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def custom_statements(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.AuthResourcePolicyProperty.CustomStatements``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("custom_statements")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def intrinsic_vpc_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpc_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpce_blacklist(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpce_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpce_whitelist(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpceWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpce_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def intrinsic_vpc_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IntrinsicVpcWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("intrinsic_vpc_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ip_range_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IpRangeBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("ip_range_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ip_range_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.IpRangeWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("ip_range_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_vpc_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.SourceVpcBlacklist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("source_vpc_blacklist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_vpc_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.AuthResourcePolicyProperty.SourceVpcWhitelist``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object
            '''
            result = self._values.get("source_vpc_whitelist")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthResourcePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.BucketSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class BucketSAMPTProperty:
        def __init__(self, *, bucket_name: builtins.str) -> None:
            '''
            :param bucket_name: ``CfnFunction.BucketSAMPTProperty.BucketName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                bucket_sAMPTProperty = sam.CfnFunction.BucketSAMPTProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16d20236c51dd02755482e3bbe3908c77866f14168ba2bb60a4cf0e2f2c72e79)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnFunction.BucketSAMPTProperty.BucketName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnFunction.CloudWatchEventEventProperty.Pattern``.
            :param input: ``CfnFunction.CloudWatchEventEventProperty.Input``.
            :param input_path: ``CfnFunction.CloudWatchEventEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # pattern: Any
                
                cloud_watch_event_event_property = sam.CfnFunction.CloudWatchEventEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d42cedc57e2c46641af5717c6782f0feddf9fb2fed57ccf5fb5580af877f1c6)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnFunction.CloudWatchEventEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.CloudWatchEventEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.CloudWatchEventEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.CloudWatchLogsEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filter_pattern": "filterPattern",
            "log_group_name": "logGroupName",
        },
    )
    class CloudWatchLogsEventProperty:
        def __init__(
            self,
            *,
            filter_pattern: builtins.str,
            log_group_name: builtins.str,
        ) -> None:
            '''
            :param filter_pattern: ``CfnFunction.CloudWatchLogsEventProperty.FilterPattern``.
            :param log_group_name: ``CfnFunction.CloudWatchLogsEventProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                cloud_watch_logs_event_property = sam.CfnFunction.CloudWatchLogsEventProperty(
                    filter_pattern="filterPattern",
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4cf09679c7819ce9be2a0ae1187a7eb745c6aab77d6394784f61bfb95cd6398)
                check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "filter_pattern": filter_pattern,
                "log_group_name": log_group_name,
            }

        @builtins.property
        def filter_pattern(self) -> builtins.str:
            '''``CfnFunction.CloudWatchLogsEventProperty.FilterPattern``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchlogs
            '''
            result = self._values.get("filter_pattern")
            assert result is not None, "Required property 'filter_pattern' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_group_name(self) -> builtins.str:
            '''``CfnFunction.CloudWatchLogsEventProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchlogs
            '''
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.CognitoEventProperty",
        jsii_struct_bases=[],
        name_mapping={"trigger": "trigger", "user_pool": "userPool"},
    )
    class CognitoEventProperty:
        def __init__(
            self,
            *,
            trigger: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Sequence[builtins.str]],
            user_pool: builtins.str,
        ) -> None:
            '''
            :param trigger: ``CfnFunction.CognitoEventProperty.Trigger``.
            :param user_pool: ``CfnFunction.CognitoEventProperty.UserPool``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cognito
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                cognito_event_property = sam.CfnFunction.CognitoEventProperty(
                    trigger="trigger",
                    user_pool="userPool"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f79f63b72bd28e6063161819e64e88bd2f6a3e9696d4546783a82335b27f4f39)
                check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
                check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "trigger": trigger,
                "user_pool": user_pool,
            }

        @builtins.property
        def trigger(
            self,
        ) -> typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.List[builtins.str]]:
            '''``CfnFunction.CognitoEventProperty.Trigger``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cognito
            '''
            result = self._values.get("trigger")
            assert result is not None, "Required property 'trigger' is missing"
            return typing.cast(typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.List[builtins.str]], result)

        @builtins.property
        def user_pool(self) -> builtins.str:
            '''``CfnFunction.CognitoEventProperty.UserPool``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cognito
            '''
            result = self._values.get("user_pool")
            assert result is not None, "Required property 'user_pool' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.CollectionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"collection_id": "collectionId"},
    )
    class CollectionSAMPTProperty:
        def __init__(self, *, collection_id: builtins.str) -> None:
            '''
            :param collection_id: ``CfnFunction.CollectionSAMPTProperty.CollectionId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                collection_sAMPTProperty = sam.CfnFunction.CollectionSAMPTProperty(
                    collection_id="collectionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e77fb73265883f664901d8ff52e757fe7f1627d89e18da5e788dc42ed9cbeae)
                check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "collection_id": collection_id,
            }

        @builtins.property
        def collection_id(self) -> builtins.str:
            '''``CfnFunction.CollectionSAMPTProperty.CollectionId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("collection_id")
            assert result is not None, "Required property 'collection_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CollectionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.DeadLetterQueueProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "type": "type"},
    )
    class DeadLetterQueueProperty:
        def __init__(self, *, target_arn: builtins.str, type: builtins.str) -> None:
            '''
            :param target_arn: ``CfnFunction.DeadLetterQueueProperty.TargetArn``.
            :param type: ``CfnFunction.DeadLetterQueueProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deadletterqueue-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                dead_letter_queue_property = sam.CfnFunction.DeadLetterQueueProperty(
                    target_arn="targetArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f17a032068fb82887a30716574e611525adb0ed919b817e3bde35924698f6c68)
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_arn": target_arn,
                "type": type,
            }

        @builtins.property
        def target_arn(self) -> builtins.str:
            '''``CfnFunction.DeadLetterQueueProperty.TargetArn``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("target_arn")
            assert result is not None, "Required property 'target_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.DeadLetterQueueProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterQueueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.DeploymentPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "type": "type",
            "alarms": "alarms",
            "hooks": "hooks",
        },
    )
    class DeploymentPreferenceProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            type: builtins.str,
            alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
            hooks: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.HooksProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnFunction.DeploymentPreferenceProperty.Enabled``.
            :param type: ``CfnFunction.DeploymentPreferenceProperty.Type``.
            :param alarms: ``CfnFunction.DeploymentPreferenceProperty.Alarms``.
            :param hooks: ``CfnFunction.DeploymentPreferenceProperty.Hooks``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/safe_lambda_deployments.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                deployment_preference_property = sam.CfnFunction.DeploymentPreferenceProperty(
                    enabled=False,
                    type="type",
                
                    # the properties below are optional
                    alarms=["alarms"],
                    hooks=sam.CfnFunction.HooksProperty(
                        post_traffic="postTraffic",
                        pre_traffic="preTraffic"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8c1c64236480d5626ce4666449aae0363c1193da40f54e09f4ba011037f8e12)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
                check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
                "type": type,
            }
            if alarms is not None:
                self._values["alarms"] = alarms
            if hooks is not None:
                self._values["hooks"] = hooks

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnFunction.DeploymentPreferenceProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.DeploymentPreferenceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def alarms(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.DeploymentPreferenceProperty.Alarms``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def hooks(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.HooksProperty"]]:
            '''``CfnFunction.DeploymentPreferenceProperty.Hooks``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("hooks")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.HooksProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.DestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure"},
    )
    class DestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.DestinationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''
            :param on_failure: ``CfnFunction.DestinationConfigProperty.OnFailure``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                destination_config_property = sam.CfnFunction.DestinationConfigProperty(
                    on_failure=sam.CfnFunction.DestinationProperty(
                        destination="destination",
                
                        # the properties below are optional
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5f2e1796df1686ac4a7187c75d6f8d6111fa115ef9d1eefd86870eaf619f865)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "on_failure": on_failure,
            }

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationProperty"]:
            '''``CfnFunction.DestinationConfigProperty.OnFailure``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("on_failure")
            assert result is not None, "Required property 'on_failure' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "type": "type"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            destination: builtins.str,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination: ``CfnFunction.DestinationProperty.Destination``.
            :param type: ``CfnFunction.DestinationProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                destination_property = sam.CfnFunction.DestinationProperty(
                    destination="destination",
                
                    # the properties below are optional
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e946903e7d7c6e569d226afd255fb7f52e5059f60382388fe68476cd1430bff)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
            }
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def destination(self) -> builtins.str:
            '''``CfnFunction.DestinationProperty.Destination``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.DestinationProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.DomainSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName"},
    )
    class DomainSAMPTProperty:
        def __init__(self, *, domain_name: builtins.str) -> None:
            '''
            :param domain_name: ``CfnFunction.DomainSAMPTProperty.DomainName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                domain_sAMPTProperty = sam.CfnFunction.DomainSAMPTProperty(
                    domain_name="domainName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c181e302b706f28a883e2d074833bca3b3ae88b4eef852ce6c441d8ba3b9d0f1)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "domain_name": domain_name,
            }

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''``CfnFunction.DomainSAMPTProperty.DomainName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.DynamoDBEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "starting_position": "startingPosition",
            "stream": "stream",
            "batch_size": "batchSize",
            "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
            "destination_config": "destinationConfig",
            "enabled": "enabled",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
            "parallelization_factor": "parallelizationFactor",
        },
    )
    class DynamoDBEventProperty:
        def __init__(
            self,
            *,
            starting_position: builtins.str,
            stream: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            destination_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.DestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
            parallelization_factor: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param starting_position: ``CfnFunction.DynamoDBEventProperty.StartingPosition``.
            :param stream: ``CfnFunction.DynamoDBEventProperty.Stream``.
            :param batch_size: ``CfnFunction.DynamoDBEventProperty.BatchSize``.
            :param bisect_batch_on_function_error: ``CfnFunction.DynamoDBEventProperty.BisectBatchOnFunctionError``.
            :param destination_config: ``CfnFunction.DynamoDBEventProperty.DestinationConfig``.
            :param enabled: ``CfnFunction.DynamoDBEventProperty.Enabled``.
            :param maximum_batching_window_in_seconds: ``CfnFunction.DynamoDBEventProperty.MaximumBatchingWindowInSeconds``.
            :param maximum_record_age_in_seconds: ``CfnFunction.DynamoDBEventProperty.MaximumRecordAgeInSeconds``.
            :param maximum_retry_attempts: ``CfnFunction.DynamoDBEventProperty.MaximumRetryAttempts``.
            :param parallelization_factor: ``CfnFunction.DynamoDBEventProperty.ParallelizationFactor``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                dynamo_dBEvent_property = sam.CfnFunction.DynamoDBEventProperty(
                    starting_position="startingPosition",
                    stream="stream",
                
                    # the properties below are optional
                    batch_size=123,
                    bisect_batch_on_function_error=False,
                    destination_config=sam.CfnFunction.DestinationConfigProperty(
                        on_failure=sam.CfnFunction.DestinationProperty(
                            destination="destination",
                
                            # the properties below are optional
                            type="type"
                        )
                    ),
                    enabled=False,
                    maximum_batching_window_in_seconds=123,
                    maximum_record_age_in_seconds=123,
                    maximum_retry_attempts=123,
                    parallelization_factor=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9081bfed1e11a0c683c6afbde969641abc3c5f9a161f6ed0ab2b6dcaa220ea2)
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument bisect_batch_on_function_error", value=bisect_batch_on_function_error, expected_type=type_hints["bisect_batch_on_function_error"])
                check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
                check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "starting_position": starting_position,
                "stream": stream,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if bisect_batch_on_function_error is not None:
                self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
            if destination_config is not None:
                self._values["destination_config"] = destination_config
            if enabled is not None:
                self._values["enabled"] = enabled
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if maximum_record_age_in_seconds is not None:
                self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts
            if parallelization_factor is not None:
                self._values["parallelization_factor"] = parallelization_factor

        @builtins.property
        def starting_position(self) -> builtins.str:
            '''``CfnFunction.DynamoDBEventProperty.StartingPosition``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("starting_position")
            assert result is not None, "Required property 'starting_position' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stream(self) -> builtins.str:
            '''``CfnFunction.DynamoDBEventProperty.Stream``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("stream")
            assert result is not None, "Required property 'stream' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def bisect_batch_on_function_error(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.DynamoDBEventProperty.BisectBatchOnFunctionError``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("bisect_batch_on_function_error")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def destination_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationConfigProperty"]]:
            '''``CfnFunction.DynamoDBEventProperty.DestinationConfig``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("destination_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationConfigProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.DynamoDBEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumBatchingWindowInSeconds``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumRecordAgeInSeconds``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_record_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumRetryAttempts``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallelization_factor(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.ParallelizationFactor``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("parallelization_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.EmptySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class EmptySAMPTProperty:
        def __init__(self) -> None:
            '''
            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                empty_sAMPTProperty = sam.CfnFunction.EmptySAMPTProperty()
            '''
            self._values: typing.Dict[builtins.str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmptySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnFunction.EventBridgeRuleEventProperty.Pattern``.
            :param event_bus_name: ``CfnFunction.EventBridgeRuleEventProperty.EventBusName``.
            :param input: ``CfnFunction.EventBridgeRuleEventProperty.Input``.
            :param input_path: ``CfnFunction.EventBridgeRuleEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # pattern: Any
                
                event_bridge_rule_event_property = sam.CfnFunction.EventBridgeRuleEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc41a93b3370fb7ad69babd0d7e9b14ac4ef47e0e9c5835e92f8501c58414d58)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnFunction.EventBridgeRuleEventProperty.Pattern``.

            :link: https://docs.aws.amazon.com/eventbridge/latest/userguide/filtering-examples-structure.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.EventBusName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.EventInvokeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_config": "destinationConfig",
            "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
        },
    )
    class EventInvokeConfigProperty:
        def __init__(
            self,
            *,
            destination_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EventInvokeDestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param destination_config: ``CfnFunction.EventInvokeConfigProperty.DestinationConfig``.
            :param maximum_event_age_in_seconds: ``CfnFunction.EventInvokeConfigProperty.MaximumEventAgeInSeconds``.
            :param maximum_retry_attempts: ``CfnFunction.EventInvokeConfigProperty.MaximumRetryAttempts``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                event_invoke_config_property = sam.CfnFunction.EventInvokeConfigProperty(
                    destination_config=sam.CfnFunction.EventInvokeDestinationConfigProperty(
                        on_failure=sam.CfnFunction.DestinationProperty(
                            destination="destination",
                
                            # the properties below are optional
                            type="type"
                        ),
                        on_success=sam.CfnFunction.DestinationProperty(
                            destination="destination",
                
                            # the properties below are optional
                            type="type"
                        )
                    ),
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ee88e03069ae018abe4b6409ac64aa2e9e2ce6908c6e29cba676c2ab6277948)
                check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
                check_type(argname="argument maximum_event_age_in_seconds", value=maximum_event_age_in_seconds, expected_type=type_hints["maximum_event_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_config is not None:
                self._values["destination_config"] = destination_config
            if maximum_event_age_in_seconds is not None:
                self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts

        @builtins.property
        def destination_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventInvokeDestinationConfigProperty"]]:
            '''``CfnFunction.EventInvokeConfigProperty.DestinationConfig``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            '''
            result = self._values.get("destination_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EventInvokeDestinationConfigProperty"]], result)

        @builtins.property
        def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.EventInvokeConfigProperty.MaximumEventAgeInSeconds``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            '''
            result = self._values.get("maximum_event_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.EventInvokeConfigProperty.MaximumRetryAttempts``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-config-object
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventInvokeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.EventInvokeDestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure", "on_success": "onSuccess"},
    )
    class EventInvokeDestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.DestinationProperty", typing.Dict[builtins.str, typing.Any]]],
            on_success: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.DestinationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''
            :param on_failure: ``CfnFunction.EventInvokeDestinationConfigProperty.OnFailure``.
            :param on_success: ``CfnFunction.EventInvokeDestinationConfigProperty.OnSuccess``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-destination-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                event_invoke_destination_config_property = sam.CfnFunction.EventInvokeDestinationConfigProperty(
                    on_failure=sam.CfnFunction.DestinationProperty(
                        destination="destination",
                
                        # the properties below are optional
                        type="type"
                    ),
                    on_success=sam.CfnFunction.DestinationProperty(
                        destination="destination",
                
                        # the properties below are optional
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__656dc15f76064dc2add7ec2c119e09bb254bce2eb9f0a1e3e90cc6f08ed7671f)
                check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
                check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "on_failure": on_failure,
                "on_success": on_success,
            }

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationProperty"]:
            '''``CfnFunction.EventInvokeDestinationConfigProperty.OnFailure``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-destination-config-object
            '''
            result = self._values.get("on_failure")
            assert result is not None, "Required property 'on_failure' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationProperty"], result)

        @builtins.property
        def on_success(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationProperty"]:
            '''``CfnFunction.EventInvokeDestinationConfigProperty.OnSuccess``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#event-invoke-destination-config-object
            '''
            result = self._values.get("on_success")
            assert result is not None, "Required property 'on_success' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DestinationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventInvokeDestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.AlexaSkillEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.ApiEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.CloudWatchEventEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.CloudWatchLogsEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.CognitoEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.DynamoDBEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.EventBridgeRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.S3EventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.SNSEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.SQSEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.KinesisEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.ScheduleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.IoTRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnFunction.HttpApiEventProperty", typing.Dict[builtins.str, typing.Any]]],
            type: builtins.str,
        ) -> None:
            '''
            :param properties: ``CfnFunction.EventSourceProperty.Properties``.
            :param type: ``CfnFunction.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                event_source_property = sam.CfnFunction.EventSourceProperty(
                    properties=sam.CfnFunction.S3EventProperty(
                        variables={
                            "variables_key": "variables"
                        }
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a66da71eac01e4773924ab3c0f785c5b17453496ebaf6d208f4a8d4f9a3c280e)
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "properties": properties,
                "type": type,
            }

        @builtins.property
        def properties(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.CloudWatchLogsEventProperty", "CfnFunction.CognitoEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.EventBridgeRuleEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.ScheduleEventProperty", "CfnFunction.IoTRuleEventProperty", "CfnFunction.HttpApiEventProperty"]:
            '''``CfnFunction.EventSourceProperty.Properties``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-types
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.CloudWatchLogsEventProperty", "CfnFunction.CognitoEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.EventBridgeRuleEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.ScheduleEventProperty", "CfnFunction.IoTRuleEventProperty", "CfnFunction.HttpApiEventProperty"], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.FileSystemConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "local_mount_path": "localMountPath"},
    )
    class FileSystemConfigProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            local_mount_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: ``CfnFunction.FileSystemConfigProperty.Arn``.
            :param local_mount_path: ``CfnFunction.FileSystemConfigProperty.LocalMountPath``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                file_system_config_property = sam.CfnFunction.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99423913694fe0591e852087ba824fe5be326d91ed2eeda9cf8f019dddd293fe)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument local_mount_path", value=local_mount_path, expected_type=type_hints["local_mount_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if local_mount_path is not None:
                self._values["local_mount_path"] = local_mount_path

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.FileSystemConfigProperty.Arn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_mount_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.FileSystemConfigProperty.LocalMountPath``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            '''
            result = self._values.get("local_mount_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileSystemConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.FunctionEnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class FunctionEnvironmentProperty:
        def __init__(
            self,
            *,
            variables: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
        ) -> None:
            '''
            :param variables: ``CfnFunction.FunctionEnvironmentProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#environment-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                function_environment_property = sam.CfnFunction.FunctionEnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b5cc15c640ef872fffc367a817baec7975c7f825931d90d8b079428b269d81a)
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "variables": variables,
            }

        @builtins.property
        def variables(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]:
            '''``CfnFunction.FunctionEnvironmentProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#environment-object
            '''
            result = self._values.get("variables")
            assert result is not None, "Required property 'variables' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionEnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(self, *, function_name: builtins.str) -> None:
            '''
            :param function_name: ``CfnFunction.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                function_sAMPTProperty = sam.CfnFunction.FunctionSAMPTProperty(
                    function_name="functionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__237d006ecc71dd3aed0c0aa0b90ba04699d8eca82ed309b0723110b72a1e66f2)
                check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_name": function_name,
            }

        @builtins.property
        def function_name(self) -> builtins.str:
            '''``CfnFunction.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("function_name")
            assert result is not None, "Required property 'function_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.HooksProperty",
        jsii_struct_bases=[],
        name_mapping={"post_traffic": "postTraffic", "pre_traffic": "preTraffic"},
    )
    class HooksProperty:
        def __init__(
            self,
            *,
            post_traffic: typing.Optional[builtins.str] = None,
            pre_traffic: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param post_traffic: ``CfnFunction.HooksProperty.PostTraffic``.
            :param pre_traffic: ``CfnFunction.HooksProperty.PreTraffic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/safe_lambda_deployments.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                hooks_property = sam.CfnFunction.HooksProperty(
                    post_traffic="postTraffic",
                    pre_traffic="preTraffic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a800f65b32bad5f150236479780db4a521daa6a5bbf8f1edf2fcaffefee51798)
                check_type(argname="argument post_traffic", value=post_traffic, expected_type=type_hints["post_traffic"])
                check_type(argname="argument pre_traffic", value=pre_traffic, expected_type=type_hints["pre_traffic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if post_traffic is not None:
                self._values["post_traffic"] = post_traffic
            if pre_traffic is not None:
                self._values["pre_traffic"] = pre_traffic

        @builtins.property
        def post_traffic(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HooksProperty.PostTraffic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("post_traffic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_traffic(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HooksProperty.PreTraffic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("pre_traffic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HooksProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.HttpApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_id": "apiId",
            "auth": "auth",
            "method": "method",
            "path": "path",
            "payload_format_version": "payloadFormatVersion",
            "route_settings": "routeSettings",
            "timeout_in_millis": "timeoutInMillis",
        },
    )
    class HttpApiEventProperty:
        def __init__(
            self,
            *,
            api_id: typing.Optional[builtins.str] = None,
            auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.HttpApiFunctionAuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            payload_format_version: typing.Optional[builtins.str] = None,
            route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_in_millis: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param api_id: ``CfnFunction.HttpApiEventProperty.ApiId``.
            :param auth: ``CfnFunction.HttpApiEventProperty.Auth``.
            :param method: ``CfnFunction.HttpApiEventProperty.Method``.
            :param path: ``CfnFunction.HttpApiEventProperty.Path``.
            :param payload_format_version: ``CfnFunction.HttpApiEventProperty.PayloadFormatVersion``.
            :param route_settings: ``CfnFunction.HttpApiEventProperty.RouteSettings``.
            :param timeout_in_millis: ``CfnFunction.HttpApiEventProperty.TimeoutInMillis``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#httpapi
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                http_api_event_property = sam.CfnFunction.HttpApiEventProperty(
                    api_id="apiId",
                    auth=sam.CfnFunction.HttpApiFunctionAuthProperty(
                        authorization_scopes=["authorizationScopes"],
                        authorizer="authorizer"
                    ),
                    method="method",
                    path="path",
                    payload_format_version="payloadFormatVersion",
                    route_settings=sam.CfnFunction.RouteSettingsProperty(
                        data_trace_enabled=False,
                        detailed_metrics_enabled=False,
                        logging_level="loggingLevel",
                        throttling_burst_limit=123,
                        throttling_rate_limit=123
                    ),
                    timeout_in_millis=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae00b5b46916d36fb90170aae050432f0cc88f9f1b03ea36464506482d01074d)
                check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
                check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
                check_type(argname="argument route_settings", value=route_settings, expected_type=type_hints["route_settings"])
                check_type(argname="argument timeout_in_millis", value=timeout_in_millis, expected_type=type_hints["timeout_in_millis"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_id is not None:
                self._values["api_id"] = api_id
            if auth is not None:
                self._values["auth"] = auth
            if method is not None:
                self._values["method"] = method
            if path is not None:
                self._values["path"] = path
            if payload_format_version is not None:
                self._values["payload_format_version"] = payload_format_version
            if route_settings is not None:
                self._values["route_settings"] = route_settings
            if timeout_in_millis is not None:
                self._values["timeout_in_millis"] = timeout_in_millis

        @builtins.property
        def api_id(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HttpApiEventProperty.ApiId``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#httpapi
            '''
            result = self._values.get("api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.HttpApiFunctionAuthProperty"]]:
            '''``CfnFunction.HttpApiEventProperty.Auth``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-httpapi.html
            '''
            result = self._values.get("auth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.HttpApiFunctionAuthProperty"]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HttpApiEventProperty.Method``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#httpapi
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HttpApiEventProperty.Path``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#httpapi
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload_format_version(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HttpApiEventProperty.PayloadFormatVersion``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#httpapi
            '''
            result = self._values.get("payload_format_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def route_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.RouteSettingsProperty"]]:
            '''``CfnFunction.HttpApiEventProperty.RouteSettings``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
            '''
            result = self._values.get("route_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.RouteSettingsProperty"]], result)

        @builtins.property
        def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.HttpApiEventProperty.TimeoutInMillis``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#httpapi
            '''
            result = self._values.get("timeout_in_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.HttpApiFunctionAuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_scopes": "authorizationScopes",
            "authorizer": "authorizer",
        },
    )
    class HttpApiFunctionAuthProperty:
        def __init__(
            self,
            *,
            authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param authorization_scopes: ``CfnFunction.HttpApiFunctionAuthProperty.AuthorizationScopes``.
            :param authorizer: ``CfnFunction.HttpApiFunctionAuthProperty.Authorizer``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-httpapifunctionauth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                http_api_function_auth_property = sam.CfnFunction.HttpApiFunctionAuthProperty(
                    authorization_scopes=["authorizationScopes"],
                    authorizer="authorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f434d8ac59decdc2ff911f0b314edc41a52b0172a7252db0e1d60674eeb01928)
                check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
                check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_scopes is not None:
                self._values["authorization_scopes"] = authorization_scopes
            if authorizer is not None:
                self._values["authorizer"] = authorizer

        @builtins.property
        def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.HttpApiFunctionAuthProperty.AuthorizationScopes``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-httpapifunctionauth.html
            '''
            result = self._values.get("authorization_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.HttpApiFunctionAuthProperty.Authorizer``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-httpapifunctionauth.html
            '''
            result = self._values.get("authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiFunctionAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.IAMPolicyDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement", "version": "version"},
    )
    class IAMPolicyDocumentProperty:
        def __init__(
            self,
            *,
            statement: typing.Any,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param statement: ``CfnFunction.IAMPolicyDocumentProperty.Statement``.
            :param version: ``CfnFunction.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # statement: Any
                
                i_aMPolicy_document_property = {
                    "statement": statement,
                
                    # the properties below are optional
                    "version": "version"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b2ede0291baceced7b910eb7cfe6aa3f775b1ea4407c99372b815743b6c9ae7)
                check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "statement": statement,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def statement(self) -> typing.Any:
            '''``CfnFunction.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IAMPolicyDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.IdentitySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"identity_name": "identityName"},
    )
    class IdentitySAMPTProperty:
        def __init__(self, *, identity_name: builtins.str) -> None:
            '''
            :param identity_name: ``CfnFunction.IdentitySAMPTProperty.IdentityName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                identity_sAMPTProperty = sam.CfnFunction.IdentitySAMPTProperty(
                    identity_name="identityName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31ca80a94d0340c9d16f85b86c087af1442b73e9071fa973443a43db225364cf)
                check_type(argname="argument identity_name", value=identity_name, expected_type=type_hints["identity_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "identity_name": identity_name,
            }

        @builtins.property
        def identity_name(self) -> builtins.str:
            '''``CfnFunction.IdentitySAMPTProperty.IdentityName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("identity_name")
            assert result is not None, "Required property 'identity_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentitySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.ImageConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "entry_point": "entryPoint",
            "working_directory": "workingDirectory",
        },
    )
    class ImageConfigProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
            working_directory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param command: ``CfnFunction.ImageConfigProperty.Command``.
            :param entry_point: ``CfnFunction.ImageConfigProperty.EntryPoint``.
            :param working_directory: ``CfnFunction.ImageConfigProperty.WorkingDirectory``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                image_config_property = sam.CfnFunction.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db80b42e70484822ff356a721da6a6769577d734b01ea0f688bbc6444f327789)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
                check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if entry_point is not None:
                self._values["entry_point"] = entry_point
            if working_directory is not None:
                self._values["working_directory"] = working_directory

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.ImageConfigProperty.Command``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def entry_point(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.ImageConfigProperty.EntryPoint``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-entrypoint
            '''
            result = self._values.get("entry_point")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def working_directory(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ImageConfigProperty.WorkingDirectory``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-imageconfig.html#cfn-lambda-function-imageconfig-workingdirectory
            '''
            result = self._values.get("working_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.IoTRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"sql": "sql", "aws_iot_sql_version": "awsIotSqlVersion"},
    )
    class IoTRuleEventProperty:
        def __init__(
            self,
            *,
            sql: builtins.str,
            aws_iot_sql_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param sql: ``CfnFunction.IoTRuleEventProperty.Sql``.
            :param aws_iot_sql_version: ``CfnFunction.IoTRuleEventProperty.AwsIotSqlVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                io_tRule_event_property = sam.CfnFunction.IoTRuleEventProperty(
                    sql="sql",
                
                    # the properties below are optional
                    aws_iot_sql_version="awsIotSqlVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3121f1fef52a8e9581f56f9a5e6144c2d269b4ddb64aea46fddda0394b101618)
                check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
                check_type(argname="argument aws_iot_sql_version", value=aws_iot_sql_version, expected_type=type_hints["aws_iot_sql_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "sql": sql,
            }
            if aws_iot_sql_version is not None:
                self._values["aws_iot_sql_version"] = aws_iot_sql_version

        @builtins.property
        def sql(self) -> builtins.str:
            '''``CfnFunction.IoTRuleEventProperty.Sql``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            '''
            result = self._values.get("sql")
            assert result is not None, "Required property 'sql' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def aws_iot_sql_version(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.IoTRuleEventProperty.AwsIotSqlVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            '''
            result = self._values.get("aws_iot_sql_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.KeySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"key_id": "keyId"},
    )
    class KeySAMPTProperty:
        def __init__(self, *, key_id: builtins.str) -> None:
            '''
            :param key_id: ``CfnFunction.KeySAMPTProperty.KeyId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                key_sAMPTProperty = sam.CfnFunction.KeySAMPTProperty(
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92727d11b5a9b91b124b1e95cb5c4a131033aaeaf43955a9c05797fdd8811db6)
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key_id": key_id,
            }

        @builtins.property
        def key_id(self) -> builtins.str:
            '''``CfnFunction.KeySAMPTProperty.KeyId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("key_id")
            assert result is not None, "Required property 'key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.KinesisEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "starting_position": "startingPosition",
            "stream": "stream",
            "batch_size": "batchSize",
            "enabled": "enabled",
            "function_response_types": "functionResponseTypes",
        },
    )
    class KinesisEventProperty:
        def __init__(
            self,
            *,
            starting_position: builtins.str,
            stream: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param starting_position: ``CfnFunction.KinesisEventProperty.StartingPosition``.
            :param stream: ``CfnFunction.KinesisEventProperty.Stream``.
            :param batch_size: ``CfnFunction.KinesisEventProperty.BatchSize``.
            :param enabled: ``CfnFunction.KinesisEventProperty.Enabled``.
            :param function_response_types: ``CfnFunction.KinesisEventProperty.FunctionResponseTypes``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                kinesis_event_property = sam.CfnFunction.KinesisEventProperty(
                    starting_position="startingPosition",
                    stream="stream",
                
                    # the properties below are optional
                    batch_size=123,
                    enabled=False,
                    function_response_types=["functionResponseTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e56b37e02a04eb7425d69277f4897db5605d3e1b72750bd4cd2ce034dcc8d20)
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument function_response_types", value=function_response_types, expected_type=type_hints["function_response_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "starting_position": starting_position,
                "stream": stream,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled
            if function_response_types is not None:
                self._values["function_response_types"] = function_response_types

        @builtins.property
        def starting_position(self) -> builtins.str:
            '''``CfnFunction.KinesisEventProperty.StartingPosition``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("starting_position")
            assert result is not None, "Required property 'starting_position' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stream(self) -> builtins.str:
            '''``CfnFunction.KinesisEventProperty.Stream``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("stream")
            assert result is not None, "Required property 'stream' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.KinesisEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.KinesisEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def function_response_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.KinesisEventProperty.FunctionResponseTypes``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("function_response_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.LogGroupSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogGroupSAMPTProperty:
        def __init__(self, *, log_group_name: builtins.str) -> None:
            '''
            :param log_group_name: ``CfnFunction.LogGroupSAMPTProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                log_group_sAMPTProperty = sam.CfnFunction.LogGroupSAMPTProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6230cf227eb2e7962b69414c9ca43b1491b7c10d0cf42a44fd9584906edf3920)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group_name": log_group_name,
            }

        @builtins.property
        def log_group_name(self) -> builtins.str:
            '''``CfnFunction.LogGroupSAMPTProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogGroupSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.ParameterNameSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"parameter_name": "parameterName"},
    )
    class ParameterNameSAMPTProperty:
        def __init__(self, *, parameter_name: builtins.str) -> None:
            '''
            :param parameter_name: ``CfnFunction.ParameterNameSAMPTProperty.ParameterName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                parameter_name_sAMPTProperty = sam.CfnFunction.ParameterNameSAMPTProperty(
                    parameter_name="parameterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__121e9784c55c86ce0a439394161d08d7ecb81d38d14ddec8332878ff51c4d381)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "parameter_name": parameter_name,
            }

        @builtins.property
        def parameter_name(self) -> builtins.str:
            '''``CfnFunction.ParameterNameSAMPTProperty.ParameterName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("parameter_name")
            assert result is not None, "Required property 'parameter_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterNameSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.ProvisionedConcurrencyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provisioned_concurrent_executions": "provisionedConcurrentExecutions",
        },
    )
    class ProvisionedConcurrencyConfigProperty:
        def __init__(self, *, provisioned_concurrent_executions: builtins.str) -> None:
            '''
            :param provisioned_concurrent_executions: ``CfnFunction.ProvisionedConcurrencyConfigProperty.ProvisionedConcurrentExecutions``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#provisioned-concurrency-config-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                provisioned_concurrency_config_property = sam.CfnFunction.ProvisionedConcurrencyConfigProperty(
                    provisioned_concurrent_executions="provisionedConcurrentExecutions"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4021ddef1bd86daec9a11ea0350d0cdd68bb96b30cff99381cd3552db9c6c0f2)
                check_type(argname="argument provisioned_concurrent_executions", value=provisioned_concurrent_executions, expected_type=type_hints["provisioned_concurrent_executions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "provisioned_concurrent_executions": provisioned_concurrent_executions,
            }

        @builtins.property
        def provisioned_concurrent_executions(self) -> builtins.str:
            '''``CfnFunction.ProvisionedConcurrencyConfigProperty.ProvisionedConcurrentExecutions``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#provisioned-concurrency-config-object
            '''
            result = self._values.get("provisioned_concurrent_executions")
            assert result is not None, "Required property 'provisioned_concurrent_executions' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedConcurrencyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.QueueSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"queue_name": "queueName"},
    )
    class QueueSAMPTProperty:
        def __init__(self, *, queue_name: builtins.str) -> None:
            '''
            :param queue_name: ``CfnFunction.QueueSAMPTProperty.QueueName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                queue_sAMPTProperty = sam.CfnFunction.QueueSAMPTProperty(
                    queue_name="queueName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__264f5be22c104c853c4e499d25140cee70e114ef90ed9488d5d87b50a9b26bf2)
                check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "queue_name": queue_name,
            }

        @builtins.property
        def queue_name(self) -> builtins.str:
            '''``CfnFunction.QueueSAMPTProperty.QueueName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("queue_name")
            assert result is not None, "Required property 'queue_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.RequestModelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "model": "model",
            "required": "required",
            "validate_body": "validateBody",
            "validate_parameters": "validateParameters",
        },
    )
    class RequestModelProperty:
        def __init__(
            self,
            *,
            model: builtins.str,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            validate_body: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            validate_parameters: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param model: ``CfnFunction.RequestModelProperty.Model``.
            :param required: ``CfnFunction.RequestModelProperty.Required``.
            :param validate_body: ``CfnFunction.RequestModelProperty.ValidateBody``.
            :param validate_parameters: ``CfnFunction.RequestModelProperty.ValidateParameters``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                request_model_property = sam.CfnFunction.RequestModelProperty(
                    model="model",
                
                    # the properties below are optional
                    required=False,
                    validate_body=False,
                    validate_parameters=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80a9c0446a5075dcbd473aeffcddbd0db2fb4ad8b351a7547aac464a05187897)
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument validate_body", value=validate_body, expected_type=type_hints["validate_body"])
                check_type(argname="argument validate_parameters", value=validate_parameters, expected_type=type_hints["validate_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "model": model,
            }
            if required is not None:
                self._values["required"] = required
            if validate_body is not None:
                self._values["validate_body"] = validate_body
            if validate_parameters is not None:
                self._values["validate_parameters"] = validate_parameters

        @builtins.property
        def model(self) -> builtins.str:
            '''``CfnFunction.RequestModelProperty.Model``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-model
            '''
            result = self._values.get("model")
            assert result is not None, "Required property 'model' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.RequestModelProperty.Required``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def validate_body(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.RequestModelProperty.ValidateBody``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-validatebody
            '''
            result = self._values.get("validate_body")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def validate_parameters(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.RequestModelProperty.ValidateParameters``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestmodel.html#sam-function-requestmodel-validateparameters
            '''
            result = self._values.get("validate_parameters")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.RequestParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"caching": "caching", "required": "required"},
    )
    class RequestParameterProperty:
        def __init__(
            self,
            *,
            caching: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param caching: ``CfnFunction.RequestParameterProperty.Caching``.
            :param required: ``CfnFunction.RequestParameterProperty.Required``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                request_parameter_property = sam.CfnFunction.RequestParameterProperty(
                    caching=False,
                    required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ec70a4e5ab8bf920ef11391480ca9ea3d77cb961c3f636fbd680a7525c793f0)
                check_type(argname="argument caching", value=caching, expected_type=type_hints["caching"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if caching is not None:
                self._values["caching"] = caching
            if required is not None:
                self._values["required"] = required

        @builtins.property
        def caching(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.RequestParameterProperty.Caching``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestparameter.html#sam-function-requestparameter-caching
            '''
            result = self._values.get("caching")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.RequestParameterProperty.Required``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-requestparameter.html#sam-function-requestparameter-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param data_trace_enabled: ``CfnFunction.RouteSettingsProperty.DataTraceEnabled``.
            :param detailed_metrics_enabled: ``CfnFunction.RouteSettingsProperty.DetailedMetricsEnabled``.
            :param logging_level: ``CfnFunction.RouteSettingsProperty.LoggingLevel``.
            :param throttling_burst_limit: ``CfnFunction.RouteSettingsProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnFunction.RouteSettingsProperty.ThrottlingRateLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                route_settings_property = sam.CfnFunction.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e362b6b06b1b919ab06228a32a9e359d7a70f3641e7049c13c19977d349312ae)
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument detailed_metrics_enabled", value=detailed_metrics_enabled, expected_type=type_hints["detailed_metrics_enabled"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.RouteSettingsProperty.DataTraceEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.RouteSettingsProperty.DetailedMetricsEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-detailedmetricsenabled
            '''
            result = self._values.get("detailed_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.RouteSettingsProperty.LoggingLevel``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.RouteSettingsProperty.ThrottlingBurstLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.RouteSettingsProperty.ThrottlingRateLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.S3EventProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "events": "events", "filter": "filter"},
    )
    class S3EventProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            events: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Sequence[builtins.str]],
            filter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.S3NotificationFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param bucket: ``CfnFunction.S3EventProperty.Bucket``.
            :param events: ``CfnFunction.S3EventProperty.Events``.
            :param filter: ``CfnFunction.S3EventProperty.Filter``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_event_property = sam.CfnFunction.S3EventProperty(
                    bucket="bucket",
                    events="events",
                
                    # the properties below are optional
                    filter=sam.CfnFunction.S3NotificationFilterProperty(
                        s3_key=sam.CfnFunction.S3KeyFilterProperty(
                            rules=[sam.CfnFunction.S3KeyFilterRuleProperty(
                                name="name",
                                value="value"
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38af21ae160c5270503c04a09253853e61ce282db4c3201fbfec9a8ff42f53cf)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "events": events,
            }
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnFunction.S3EventProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def events(
            self,
        ) -> typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.List[builtins.str]]:
            '''``CfnFunction.S3EventProperty.Events``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("events")
            assert result is not None, "Required property 'events' is missing"
            return typing.cast(typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.List[builtins.str]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3NotificationFilterProperty"]]:
            '''``CfnFunction.S3EventProperty.Filter``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3NotificationFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3EventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.S3KeyFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class S3KeyFilterProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.S3KeyFilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''
            :param rules: ``CfnFunction.S3KeyFilterProperty.Rules``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_key_filter_property = sam.CfnFunction.S3KeyFilterProperty(
                    rules=[sam.CfnFunction.S3KeyFilterRuleProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c556636d8a23436ac5d42b03375c4a0229b10fb815b3b690b5cd2da67f41de29)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3KeyFilterRuleProperty"]]]:
            '''``CfnFunction.S3KeyFilterProperty.Rules``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3KeyFilterRuleProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.S3KeyFilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class S3KeyFilterRuleProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''
            :param name: ``CfnFunction.S3KeyFilterRuleProperty.Name``.
            :param value: ``CfnFunction.S3KeyFilterRuleProperty.Value``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_key_filter_rule_property = sam.CfnFunction.S3KeyFilterRuleProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39104646d713050855438706718102007cfa15d75275e6bb80004e3a39eed048)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnFunction.S3KeyFilterRuleProperty.Name``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnFunction.S3KeyFilterRuleProperty.Value``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnFunction.S3LocationProperty.Bucket``.
            :param key: ``CfnFunction.S3LocationProperty.Key``.
            :param version: ``CfnFunction.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_location_property = sam.CfnFunction.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85fe6ffb57da8f0d099872a978c689b3859bb27acabe3051c77b75133bdd9c97)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnFunction.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnFunction.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.S3NotificationFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_key": "s3Key"},
    )
    class S3NotificationFilterProperty:
        def __init__(
            self,
            *,
            s3_key: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.S3KeyFilterProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''
            :param s3_key: ``CfnFunction.S3NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_notification_filter_property = sam.CfnFunction.S3NotificationFilterProperty(
                    s3_key=sam.CfnFunction.S3KeyFilterProperty(
                        rules=[sam.CfnFunction.S3KeyFilterRuleProperty(
                            name="name",
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fcc566ffda7e98525a21855c11091952a935480b37ab1d408aded87689514113)
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_key(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3KeyFilterProperty"]:
            '''``CfnFunction.S3NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.S3KeyFilterProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3NotificationFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ami_describe_policy": "amiDescribePolicy",
            "aws_secrets_manager_get_secret_value_policy": "awsSecretsManagerGetSecretValuePolicy",
            "cloud_formation_describe_stacks_policy": "cloudFormationDescribeStacksPolicy",
            "cloud_watch_put_metric_policy": "cloudWatchPutMetricPolicy",
            "dynamo_db_crud_policy": "dynamoDbCrudPolicy",
            "dynamo_db_read_policy": "dynamoDbReadPolicy",
            "dynamo_db_stream_read_policy": "dynamoDbStreamReadPolicy",
            "dynamo_db_write_policy": "dynamoDbWritePolicy",
            "ec2_describe_policy": "ec2DescribePolicy",
            "elasticsearch_http_post_policy": "elasticsearchHttpPostPolicy",
            "filter_log_events_policy": "filterLogEventsPolicy",
            "kinesis_crud_policy": "kinesisCrudPolicy",
            "kinesis_stream_read_policy": "kinesisStreamReadPolicy",
            "kms_decrypt_policy": "kmsDecryptPolicy",
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "rekognition_detect_only_policy": "rekognitionDetectOnlyPolicy",
            "rekognition_labels_policy": "rekognitionLabelsPolicy",
            "rekognition_no_data_access_policy": "rekognitionNoDataAccessPolicy",
            "rekognition_read_policy": "rekognitionReadPolicy",
            "rekognition_write_only_access_policy": "rekognitionWriteOnlyAccessPolicy",
            "s3_crud_policy": "s3CrudPolicy",
            "s3_read_policy": "s3ReadPolicy",
            "s3_write_policy": "s3WritePolicy",
            "ses_bulk_templated_crud_policy": "sesBulkTemplatedCrudPolicy",
            "ses_crud_policy": "sesCrudPolicy",
            "ses_email_template_crud_policy": "sesEmailTemplateCrudPolicy",
            "ses_send_bounce_policy": "sesSendBouncePolicy",
            "sns_crud_policy": "snsCrudPolicy",
            "sns_publish_message_policy": "snsPublishMessagePolicy",
            "sqs_poller_policy": "sqsPollerPolicy",
            "sqs_send_message_policy": "sqsSendMessagePolicy",
            "ssm_parameter_read_policy": "ssmParameterReadPolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
            "vpc_access_policy": "vpcAccessPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            ami_describe_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            aws_secrets_manager_get_secret_value_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.SecretArnSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_formation_describe_stacks_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_put_metric_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.TableStreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_write_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.TableSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ec2_describe_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            elasticsearch_http_post_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.DomainSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_log_events_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.LogGroupSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.StreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.StreamSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kms_decrypt_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.KeySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.FunctionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_detect_only_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_labels_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_no_data_access_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rekognition_write_only_access_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.CollectionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_write_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.BucketSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_bulk_templated_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_email_template_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ses_send_bounce_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.IdentitySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.TopicSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns_publish_message_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.TopicSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_poller_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.QueueSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_send_message_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.QueueSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ssm_parameter_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.ParameterNameSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.StateMachineSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_access_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunction.EmptySAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param ami_describe_policy: ``CfnFunction.SAMPolicyTemplateProperty.AMIDescribePolicy``.
            :param aws_secrets_manager_get_secret_value_policy: ``CfnFunction.SAMPolicyTemplateProperty.AWSSecretsManagerGetSecretValuePolicy``.
            :param cloud_formation_describe_stacks_policy: ``CfnFunction.SAMPolicyTemplateProperty.CloudFormationDescribeStacksPolicy``.
            :param cloud_watch_put_metric_policy: ``CfnFunction.SAMPolicyTemplateProperty.CloudWatchPutMetricPolicy``.
            :param dynamo_db_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBCrudPolicy``.
            :param dynamo_db_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBReadPolicy``.
            :param dynamo_db_stream_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBStreamReadPolicy``.
            :param dynamo_db_write_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBWritePolicy``.
            :param ec2_describe_policy: ``CfnFunction.SAMPolicyTemplateProperty.EC2DescribePolicy``.
            :param elasticsearch_http_post_policy: ``CfnFunction.SAMPolicyTemplateProperty.ElasticsearchHttpPostPolicy``.
            :param filter_log_events_policy: ``CfnFunction.SAMPolicyTemplateProperty.FilterLogEventsPolicy``.
            :param kinesis_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.KinesisCrudPolicy``.
            :param kinesis_stream_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.KinesisStreamReadPolicy``.
            :param kms_decrypt_policy: ``CfnFunction.SAMPolicyTemplateProperty.KMSDecryptPolicy``.
            :param lambda_invoke_policy: ``CfnFunction.SAMPolicyTemplateProperty.LambdaInvokePolicy``.
            :param rekognition_detect_only_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionDetectOnlyPolicy``.
            :param rekognition_labels_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionLabelsPolicy``.
            :param rekognition_no_data_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionNoDataAccessPolicy``.
            :param rekognition_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionReadPolicy``.
            :param rekognition_write_only_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionWriteOnlyAccessPolicy``.
            :param s3_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3CrudPolicy``.
            :param s3_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3ReadPolicy``.
            :param s3_write_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3WritePolicy``.
            :param ses_bulk_templated_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESBulkTemplatedCrudPolicy``.
            :param ses_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESCrudPolicy``.
            :param ses_email_template_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESEmailTemplateCrudPolicy``.
            :param ses_send_bounce_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESSendBouncePolicy``.
            :param sns_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SNSCrudPolicy``.
            :param sns_publish_message_policy: ``CfnFunction.SAMPolicyTemplateProperty.SNSPublishMessagePolicy``.
            :param sqs_poller_policy: ``CfnFunction.SAMPolicyTemplateProperty.SQSPollerPolicy``.
            :param sqs_send_message_policy: ``CfnFunction.SAMPolicyTemplateProperty.SQSSendMessagePolicy``.
            :param ssm_parameter_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.SSMParameterReadPolicy``.
            :param step_functions_execution_policy: ``CfnFunction.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.
            :param vpc_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.VPCAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s_aMPolicy_template_property = sam.CfnFunction.SAMPolicyTemplateProperty(
                    ami_describe_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    aws_secrets_manager_get_secret_value_policy=sam.CfnFunction.SecretArnSAMPTProperty(
                        secret_arn="secretArn"
                    ),
                    cloud_formation_describe_stacks_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    cloud_watch_put_metric_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    dynamo_db_crud_policy=sam.CfnFunction.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    dynamo_db_read_policy=sam.CfnFunction.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    dynamo_db_stream_read_policy=sam.CfnFunction.TableStreamSAMPTProperty(
                        stream_name="streamName",
                        table_name="tableName"
                    ),
                    dynamo_db_write_policy=sam.CfnFunction.TableSAMPTProperty(
                        table_name="tableName"
                    ),
                    ec2_describe_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    elasticsearch_http_post_policy=sam.CfnFunction.DomainSAMPTProperty(
                        domain_name="domainName"
                    ),
                    filter_log_events_policy=sam.CfnFunction.LogGroupSAMPTProperty(
                        log_group_name="logGroupName"
                    ),
                    kinesis_crud_policy=sam.CfnFunction.StreamSAMPTProperty(
                        stream_name="streamName"
                    ),
                    kinesis_stream_read_policy=sam.CfnFunction.StreamSAMPTProperty(
                        stream_name="streamName"
                    ),
                    kms_decrypt_policy=sam.CfnFunction.KeySAMPTProperty(
                        key_id="keyId"
                    ),
                    lambda_invoke_policy=sam.CfnFunction.FunctionSAMPTProperty(
                        function_name="functionName"
                    ),
                    rekognition_detect_only_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    rekognition_labels_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    rekognition_no_data_access_policy=sam.CfnFunction.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    rekognition_read_policy=sam.CfnFunction.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    rekognition_write_only_access_policy=sam.CfnFunction.CollectionSAMPTProperty(
                        collection_id="collectionId"
                    ),
                    s3_crud_policy=sam.CfnFunction.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    s3_read_policy=sam.CfnFunction.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    s3_write_policy=sam.CfnFunction.BucketSAMPTProperty(
                        bucket_name="bucketName"
                    ),
                    ses_bulk_templated_crud_policy=sam.CfnFunction.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    ses_crud_policy=sam.CfnFunction.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    ses_email_template_crud_policy=sam.CfnFunction.EmptySAMPTProperty(),
                    ses_send_bounce_policy=sam.CfnFunction.IdentitySAMPTProperty(
                        identity_name="identityName"
                    ),
                    sns_crud_policy=sam.CfnFunction.TopicSAMPTProperty(
                        topic_name="topicName"
                    ),
                    sns_publish_message_policy=sam.CfnFunction.TopicSAMPTProperty(
                        topic_name="topicName"
                    ),
                    sqs_poller_policy=sam.CfnFunction.QueueSAMPTProperty(
                        queue_name="queueName"
                    ),
                    sqs_send_message_policy=sam.CfnFunction.QueueSAMPTProperty(
                        queue_name="queueName"
                    ),
                    ssm_parameter_read_policy=sam.CfnFunction.ParameterNameSAMPTProperty(
                        parameter_name="parameterName"
                    ),
                    step_functions_execution_policy=sam.CfnFunction.StateMachineSAMPTProperty(
                        state_machine_name="stateMachineName"
                    ),
                    vpc_access_policy=sam.CfnFunction.EmptySAMPTProperty()
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae6d8b904c88efeffe795738cbd054646b712e8461a6a97e94b7bb44825adbc5)
                check_type(argname="argument ami_describe_policy", value=ami_describe_policy, expected_type=type_hints["ami_describe_policy"])
                check_type(argname="argument aws_secrets_manager_get_secret_value_policy", value=aws_secrets_manager_get_secret_value_policy, expected_type=type_hints["aws_secrets_manager_get_secret_value_policy"])
                check_type(argname="argument cloud_formation_describe_stacks_policy", value=cloud_formation_describe_stacks_policy, expected_type=type_hints["cloud_formation_describe_stacks_policy"])
                check_type(argname="argument cloud_watch_put_metric_policy", value=cloud_watch_put_metric_policy, expected_type=type_hints["cloud_watch_put_metric_policy"])
                check_type(argname="argument dynamo_db_crud_policy", value=dynamo_db_crud_policy, expected_type=type_hints["dynamo_db_crud_policy"])
                check_type(argname="argument dynamo_db_read_policy", value=dynamo_db_read_policy, expected_type=type_hints["dynamo_db_read_policy"])
                check_type(argname="argument dynamo_db_stream_read_policy", value=dynamo_db_stream_read_policy, expected_type=type_hints["dynamo_db_stream_read_policy"])
                check_type(argname="argument dynamo_db_write_policy", value=dynamo_db_write_policy, expected_type=type_hints["dynamo_db_write_policy"])
                check_type(argname="argument ec2_describe_policy", value=ec2_describe_policy, expected_type=type_hints["ec2_describe_policy"])
                check_type(argname="argument elasticsearch_http_post_policy", value=elasticsearch_http_post_policy, expected_type=type_hints["elasticsearch_http_post_policy"])
                check_type(argname="argument filter_log_events_policy", value=filter_log_events_policy, expected_type=type_hints["filter_log_events_policy"])
                check_type(argname="argument kinesis_crud_policy", value=kinesis_crud_policy, expected_type=type_hints["kinesis_crud_policy"])
                check_type(argname="argument kinesis_stream_read_policy", value=kinesis_stream_read_policy, expected_type=type_hints["kinesis_stream_read_policy"])
                check_type(argname="argument kms_decrypt_policy", value=kms_decrypt_policy, expected_type=type_hints["kms_decrypt_policy"])
                check_type(argname="argument lambda_invoke_policy", value=lambda_invoke_policy, expected_type=type_hints["lambda_invoke_policy"])
                check_type(argname="argument rekognition_detect_only_policy", value=rekognition_detect_only_policy, expected_type=type_hints["rekognition_detect_only_policy"])
                check_type(argname="argument rekognition_labels_policy", value=rekognition_labels_policy, expected_type=type_hints["rekognition_labels_policy"])
                check_type(argname="argument rekognition_no_data_access_policy", value=rekognition_no_data_access_policy, expected_type=type_hints["rekognition_no_data_access_policy"])
                check_type(argname="argument rekognition_read_policy", value=rekognition_read_policy, expected_type=type_hints["rekognition_read_policy"])
                check_type(argname="argument rekognition_write_only_access_policy", value=rekognition_write_only_access_policy, expected_type=type_hints["rekognition_write_only_access_policy"])
                check_type(argname="argument s3_crud_policy", value=s3_crud_policy, expected_type=type_hints["s3_crud_policy"])
                check_type(argname="argument s3_read_policy", value=s3_read_policy, expected_type=type_hints["s3_read_policy"])
                check_type(argname="argument s3_write_policy", value=s3_write_policy, expected_type=type_hints["s3_write_policy"])
                check_type(argname="argument ses_bulk_templated_crud_policy", value=ses_bulk_templated_crud_policy, expected_type=type_hints["ses_bulk_templated_crud_policy"])
                check_type(argname="argument ses_crud_policy", value=ses_crud_policy, expected_type=type_hints["ses_crud_policy"])
                check_type(argname="argument ses_email_template_crud_policy", value=ses_email_template_crud_policy, expected_type=type_hints["ses_email_template_crud_policy"])
                check_type(argname="argument ses_send_bounce_policy", value=ses_send_bounce_policy, expected_type=type_hints["ses_send_bounce_policy"])
                check_type(argname="argument sns_crud_policy", value=sns_crud_policy, expected_type=type_hints["sns_crud_policy"])
                check_type(argname="argument sns_publish_message_policy", value=sns_publish_message_policy, expected_type=type_hints["sns_publish_message_policy"])
                check_type(argname="argument sqs_poller_policy", value=sqs_poller_policy, expected_type=type_hints["sqs_poller_policy"])
                check_type(argname="argument sqs_send_message_policy", value=sqs_send_message_policy, expected_type=type_hints["sqs_send_message_policy"])
                check_type(argname="argument ssm_parameter_read_policy", value=ssm_parameter_read_policy, expected_type=type_hints["ssm_parameter_read_policy"])
                check_type(argname="argument step_functions_execution_policy", value=step_functions_execution_policy, expected_type=type_hints["step_functions_execution_policy"])
                check_type(argname="argument vpc_access_policy", value=vpc_access_policy, expected_type=type_hints["vpc_access_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ami_describe_policy is not None:
                self._values["ami_describe_policy"] = ami_describe_policy
            if aws_secrets_manager_get_secret_value_policy is not None:
                self._values["aws_secrets_manager_get_secret_value_policy"] = aws_secrets_manager_get_secret_value_policy
            if cloud_formation_describe_stacks_policy is not None:
                self._values["cloud_formation_describe_stacks_policy"] = cloud_formation_describe_stacks_policy
            if cloud_watch_put_metric_policy is not None:
                self._values["cloud_watch_put_metric_policy"] = cloud_watch_put_metric_policy
            if dynamo_db_crud_policy is not None:
                self._values["dynamo_db_crud_policy"] = dynamo_db_crud_policy
            if dynamo_db_read_policy is not None:
                self._values["dynamo_db_read_policy"] = dynamo_db_read_policy
            if dynamo_db_stream_read_policy is not None:
                self._values["dynamo_db_stream_read_policy"] = dynamo_db_stream_read_policy
            if dynamo_db_write_policy is not None:
                self._values["dynamo_db_write_policy"] = dynamo_db_write_policy
            if ec2_describe_policy is not None:
                self._values["ec2_describe_policy"] = ec2_describe_policy
            if elasticsearch_http_post_policy is not None:
                self._values["elasticsearch_http_post_policy"] = elasticsearch_http_post_policy
            if filter_log_events_policy is not None:
                self._values["filter_log_events_policy"] = filter_log_events_policy
            if kinesis_crud_policy is not None:
                self._values["kinesis_crud_policy"] = kinesis_crud_policy
            if kinesis_stream_read_policy is not None:
                self._values["kinesis_stream_read_policy"] = kinesis_stream_read_policy
            if kms_decrypt_policy is not None:
                self._values["kms_decrypt_policy"] = kms_decrypt_policy
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if rekognition_detect_only_policy is not None:
                self._values["rekognition_detect_only_policy"] = rekognition_detect_only_policy
            if rekognition_labels_policy is not None:
                self._values["rekognition_labels_policy"] = rekognition_labels_policy
            if rekognition_no_data_access_policy is not None:
                self._values["rekognition_no_data_access_policy"] = rekognition_no_data_access_policy
            if rekognition_read_policy is not None:
                self._values["rekognition_read_policy"] = rekognition_read_policy
            if rekognition_write_only_access_policy is not None:
                self._values["rekognition_write_only_access_policy"] = rekognition_write_only_access_policy
            if s3_crud_policy is not None:
                self._values["s3_crud_policy"] = s3_crud_policy
            if s3_read_policy is not None:
                self._values["s3_read_policy"] = s3_read_policy
            if s3_write_policy is not None:
                self._values["s3_write_policy"] = s3_write_policy
            if ses_bulk_templated_crud_policy is not None:
                self._values["ses_bulk_templated_crud_policy"] = ses_bulk_templated_crud_policy
            if ses_crud_policy is not None:
                self._values["ses_crud_policy"] = ses_crud_policy
            if ses_email_template_crud_policy is not None:
                self._values["ses_email_template_crud_policy"] = ses_email_template_crud_policy
            if ses_send_bounce_policy is not None:
                self._values["ses_send_bounce_policy"] = ses_send_bounce_policy
            if sns_crud_policy is not None:
                self._values["sns_crud_policy"] = sns_crud_policy
            if sns_publish_message_policy is not None:
                self._values["sns_publish_message_policy"] = sns_publish_message_policy
            if sqs_poller_policy is not None:
                self._values["sqs_poller_policy"] = sqs_poller_policy
            if sqs_send_message_policy is not None:
                self._values["sqs_send_message_policy"] = sqs_send_message_policy
            if ssm_parameter_read_policy is not None:
                self._values["ssm_parameter_read_policy"] = ssm_parameter_read_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy
            if vpc_access_policy is not None:
                self._values["vpc_access_policy"] = vpc_access_policy

        @builtins.property
        def ami_describe_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.AMIDescribePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ami_describe_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        @builtins.property
        def aws_secrets_manager_get_secret_value_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.SecretArnSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.AWSSecretsManagerGetSecretValuePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("aws_secrets_manager_get_secret_value_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.SecretArnSAMPTProperty"]], result)

        @builtins.property
        def cloud_formation_describe_stacks_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.CloudFormationDescribeStacksPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("cloud_formation_describe_stacks_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        @builtins.property
        def cloud_watch_put_metric_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.CloudWatchPutMetricPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("cloud_watch_put_metric_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableSAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableSAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableStreamSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBStreamReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableStreamSAMPTProperty"]], result)

        @builtins.property
        def dynamo_db_write_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBWritePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_write_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TableSAMPTProperty"]], result)

        @builtins.property
        def ec2_describe_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.EC2DescribePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ec2_describe_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        @builtins.property
        def elasticsearch_http_post_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DomainSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.ElasticsearchHttpPostPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("elasticsearch_http_post_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.DomainSAMPTProperty"]], result)

        @builtins.property
        def filter_log_events_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.LogGroupSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.FilterLogEventsPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("filter_log_events_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.LogGroupSAMPTProperty"]], result)

        @builtins.property
        def kinesis_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.StreamSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KinesisCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kinesis_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.StreamSAMPTProperty"]], result)

        @builtins.property
        def kinesis_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.StreamSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KinesisStreamReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kinesis_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.StreamSAMPTProperty"]], result)

        @builtins.property
        def kms_decrypt_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.KeySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KMSDecryptPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kms_decrypt_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.KeySAMPTProperty"]], result)

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FunctionSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.LambdaInvokePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.FunctionSAMPTProperty"]], result)

        @builtins.property
        def rekognition_detect_only_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionDetectOnlyPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_detect_only_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        @builtins.property
        def rekognition_labels_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionLabelsPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_labels_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        @builtins.property
        def rekognition_no_data_access_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.CollectionSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionNoDataAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_no_data_access_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.CollectionSAMPTProperty"]], result)

        @builtins.property
        def rekognition_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.CollectionSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.CollectionSAMPTProperty"]], result)

        @builtins.property
        def rekognition_write_only_access_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.CollectionSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionWriteOnlyAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_write_only_access_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.CollectionSAMPTProperty"]], result)

        @builtins.property
        def s3_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.BucketSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3CrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.BucketSAMPTProperty"]], result)

        @builtins.property
        def s3_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.BucketSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3ReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.BucketSAMPTProperty"]], result)

        @builtins.property
        def s3_write_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.BucketSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3WritePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_write_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.BucketSAMPTProperty"]], result)

        @builtins.property
        def ses_bulk_templated_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IdentitySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESBulkTemplatedCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_bulk_templated_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IdentitySAMPTProperty"]], result)

        @builtins.property
        def ses_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IdentitySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IdentitySAMPTProperty"]], result)

        @builtins.property
        def ses_email_template_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESEmailTemplateCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_email_template_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        @builtins.property
        def ses_send_bounce_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IdentitySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESSendBouncePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_send_bounce_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.IdentitySAMPTProperty"]], result)

        @builtins.property
        def sns_crud_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TopicSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SNSCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sns_crud_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TopicSAMPTProperty"]], result)

        @builtins.property
        def sns_publish_message_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TopicSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SNSPublishMessagePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sns_publish_message_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.TopicSAMPTProperty"]], result)

        @builtins.property
        def sqs_poller_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.QueueSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SQSPollerPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sqs_poller_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.QueueSAMPTProperty"]], result)

        @builtins.property
        def sqs_send_message_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.QueueSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SQSSendMessagePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sqs_send_message_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.QueueSAMPTProperty"]], result)

        @builtins.property
        def ssm_parameter_read_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ParameterNameSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SSMParameterReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ssm_parameter_read_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.ParameterNameSAMPTProperty"]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.StateMachineSAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.StateMachineSAMPTProperty"]], result)

        @builtins.property
        def vpc_access_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.VPCAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("vpc_access_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunction.EmptySAMPTProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.SNSEventProperty",
        jsii_struct_bases=[],
        name_mapping={"topic": "topic"},
    )
    class SNSEventProperty:
        def __init__(self, *, topic: builtins.str) -> None:
            '''
            :param topic: ``CfnFunction.SNSEventProperty.Topic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sns
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s_nSEvent_property = sam.CfnFunction.SNSEventProperty(
                    topic="topic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ecbdf0c8ac73225eaf8894e23d446aa68c05f0210c72f9c14a39d8584a6eb80a)
                check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "topic": topic,
            }

        @builtins.property
        def topic(self) -> builtins.str:
            '''``CfnFunction.SNSEventProperty.Topic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sns
            '''
            result = self._values.get("topic")
            assert result is not None, "Required property 'topic' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SNSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.SQSEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "queue": "queue",
            "batch_size": "batchSize",
            "enabled": "enabled",
        },
    )
    class SQSEventProperty:
        def __init__(
            self,
            *,
            queue: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param queue: ``CfnFunction.SQSEventProperty.Queue``.
            :param batch_size: ``CfnFunction.SQSEventProperty.BatchSize``.
            :param enabled: ``CfnFunction.SQSEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s_qSEvent_property = sam.CfnFunction.SQSEventProperty(
                    queue="queue",
                
                    # the properties below are optional
                    batch_size=123,
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__481286c083b1a7b191cfff074603042a66c1d07eaa31144c79c1f5ce7ce7cdb6)
                check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "queue": queue,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def queue(self) -> builtins.str:
            '''``CfnFunction.SQSEventProperty.Queue``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("queue")
            assert result is not None, "Required property 'queue' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.SQSEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.SQSEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SQSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schedule": "schedule",
            "description": "description",
            "enabled": "enabled",
            "input": "input",
            "name": "name",
        },
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            schedule: builtins.str,
            description: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            input: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param schedule: ``CfnFunction.ScheduleEventProperty.Schedule``.
            :param description: ``CfnFunction.ScheduleEventProperty.Description``.
            :param enabled: ``CfnFunction.ScheduleEventProperty.Enabled``.
            :param input: ``CfnFunction.ScheduleEventProperty.Input``.
            :param name: ``CfnFunction.ScheduleEventProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                schedule_event_property = sam.CfnFunction.ScheduleEventProperty(
                    schedule="schedule",
                
                    # the properties below are optional
                    description="description",
                    enabled=False,
                    input="input",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eeac7993745801101c32af47af337bbbacd1e37ef5210801b5eb300d31b8a16b)
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule": schedule,
            }
            if description is not None:
                self._values["description"] = description
            if enabled is not None:
                self._values["enabled"] = enabled
            if input is not None:
                self._values["input"] = input
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def schedule(self) -> builtins.str:
            '''``CfnFunction.ScheduleEventProperty.Schedule``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("schedule")
            assert result is not None, "Required property 'schedule' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ScheduleEventProperty.Description``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnFunction.ScheduleEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ScheduleEventProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.SecretArnSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn"},
    )
    class SecretArnSAMPTProperty:
        def __init__(self, *, secret_arn: builtins.str) -> None:
            '''
            :param secret_arn: ``CfnFunction.SecretArnSAMPTProperty.SecretArn``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                secret_arn_sAMPTProperty = sam.CfnFunction.SecretArnSAMPTProperty(
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48ba5ad4a2f03c19283a5e54579dc7fc3116227adbda75fc3690f781506cae80)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_arn": secret_arn,
            }

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''``CfnFunction.SecretArnSAMPTProperty.SecretArn``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretArnSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(self, *, state_machine_name: builtins.str) -> None:
            '''
            :param state_machine_name: ``CfnFunction.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                state_machine_sAMPTProperty = sam.CfnFunction.StateMachineSAMPTProperty(
                    state_machine_name="stateMachineName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a75d62622288ec794a77b7dff6389f13c4a9d4d0d860667dfaa020fc70a37fbe)
                check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "state_machine_name": state_machine_name,
            }

        @builtins.property
        def state_machine_name(self) -> builtins.str:
            '''``CfnFunction.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("state_machine_name")
            assert result is not None, "Required property 'state_machine_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.StreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName"},
    )
    class StreamSAMPTProperty:
        def __init__(self, *, stream_name: builtins.str) -> None:
            '''
            :param stream_name: ``CfnFunction.StreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                stream_sAMPTProperty = sam.CfnFunction.StreamSAMPTProperty(
                    stream_name="streamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abe17bcb601a7203b167645fdd3022838a2ff2ef2fe20599d90662043aa05808)
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_name": stream_name,
            }

        @builtins.property
        def stream_name(self) -> builtins.str:
            '''``CfnFunction.StreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("stream_name")
            assert result is not None, "Required property 'stream_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.TableSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName"},
    )
    class TableSAMPTProperty:
        def __init__(self, *, table_name: builtins.str) -> None:
            '''
            :param table_name: ``CfnFunction.TableSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                table_sAMPTProperty = sam.CfnFunction.TableSAMPTProperty(
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b18a73d61a969f9f1834e1456de11a9f17a048354363dbe249f8edc201955681)
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "table_name": table_name,
            }

        @builtins.property
        def table_name(self) -> builtins.str:
            '''``CfnFunction.TableSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.TableStreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName", "table_name": "tableName"},
    )
    class TableStreamSAMPTProperty:
        def __init__(
            self,
            *,
            stream_name: builtins.str,
            table_name: builtins.str,
        ) -> None:
            '''
            :param stream_name: ``CfnFunction.TableStreamSAMPTProperty.StreamName``.
            :param table_name: ``CfnFunction.TableStreamSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                table_stream_sAMPTProperty = sam.CfnFunction.TableStreamSAMPTProperty(
                    stream_name="streamName",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d564fc7b8e24d8b70f90c9906af0f501ecca6689dbc26dbfd9e845b51021cd2b)
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_name": stream_name,
                "table_name": table_name,
            }

        @builtins.property
        def stream_name(self) -> builtins.str:
            '''``CfnFunction.TableStreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("stream_name")
            assert result is not None, "Required property 'stream_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''``CfnFunction.TableStreamSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableStreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.TopicSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_name": "topicName"},
    )
    class TopicSAMPTProperty:
        def __init__(self, *, topic_name: builtins.str) -> None:
            '''
            :param topic_name: ``CfnFunction.TopicSAMPTProperty.TopicName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                topic_sAMPTProperty = sam.CfnFunction.TopicSAMPTProperty(
                    topic_name="topicName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c58e0bd81ab7e11ec5326bf2fbaddc324b9a1e15cf33b45e8970bf2e228c1e6)
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "topic_name": topic_name,
            }

        @builtins.property
        def topic_name(self) -> builtins.str:
            '''``CfnFunction.TopicSAMPTProperty.TopicName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("topic_name")
            assert result is not None, "Required property 'topic_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnFunction.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Sequence[builtins.str],
            subnet_ids: typing.Sequence[builtins.str],
        ) -> None:
            '''
            :param security_group_ids: ``CfnFunction.VpcConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnFunction.VpcConfigProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                vpc_config_property = sam.CfnFunction.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc8ccdfe6cd335dc2ce3c125af88a28851b7db715ffd0e960112bbfb1bf52724)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            '''``CfnFunction.VpcConfigProperty.SecurityGroupIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            '''
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            '''``CfnFunction.VpcConfigProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            '''
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-sam.CfnFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "architectures": "architectures",
        "assume_role_policy_document": "assumeRolePolicyDocument",
        "auto_publish_alias": "autoPublishAlias",
        "auto_publish_code_sha256": "autoPublishCodeSha256",
        "code_signing_config_arn": "codeSigningConfigArn",
        "code_uri": "codeUri",
        "dead_letter_queue": "deadLetterQueue",
        "deployment_preference": "deploymentPreference",
        "description": "description",
        "environment": "environment",
        "event_invoke_config": "eventInvokeConfig",
        "events": "events",
        "file_system_configs": "fileSystemConfigs",
        "function_name": "functionName",
        "handler": "handler",
        "image_config": "imageConfig",
        "image_uri": "imageUri",
        "inline_code": "inlineCode",
        "kms_key_arn": "kmsKeyArn",
        "layers": "layers",
        "memory_size": "memorySize",
        "package_type": "packageType",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "provisioned_concurrency_config": "provisionedConcurrencyConfig",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime": "runtime",
        "tags": "tags",
        "timeout": "timeout",
        "tracing": "tracing",
        "version_description": "versionDescription",
        "vpc_config": "vpcConfig",
    },
)
class CfnFunctionProps:
    def __init__(
        self,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        assume_role_policy_document: typing.Any = None,
        auto_publish_alias: typing.Optional[builtins.str] = None,
        auto_publish_code_sha256: typing.Optional[builtins.str] = None,
        code_signing_config_arn: typing.Optional[builtins.str] = None,
        code_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DeadLetterQueueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_preference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.FunctionEnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        event_invoke_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EventInvokeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        image_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        inline_code: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        package_type: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing: typing.Optional[builtins.str] = None,
        version_description: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFunction``.

        :param architectures: ``AWS::Serverless::Function.Architectures``.
        :param assume_role_policy_document: ``AWS::Serverless::Function.AssumeRolePolicyDocument``.
        :param auto_publish_alias: ``AWS::Serverless::Function.AutoPublishAlias``.
        :param auto_publish_code_sha256: ``AWS::Serverless::Function.AutoPublishCodeSha256``.
        :param code_signing_config_arn: ``AWS::Serverless::Function.CodeSigningConfigArn``.
        :param code_uri: ``AWS::Serverless::Function.CodeUri``.
        :param dead_letter_queue: ``AWS::Serverless::Function.DeadLetterQueue``.
        :param deployment_preference: ``AWS::Serverless::Function.DeploymentPreference``.
        :param description: ``AWS::Serverless::Function.Description``.
        :param environment: ``AWS::Serverless::Function.Environment``.
        :param event_invoke_config: ``AWS::Serverless::Function.EventInvokeConfig``.
        :param events: ``AWS::Serverless::Function.Events``.
        :param file_system_configs: ``AWS::Serverless::Function.FileSystemConfigs``.
        :param function_name: ``AWS::Serverless::Function.FunctionName``.
        :param handler: ``AWS::Serverless::Function.Handler``.
        :param image_config: ``AWS::Serverless::Function.ImageConfig``.
        :param image_uri: ``AWS::Serverless::Function.ImageUri``.
        :param inline_code: ``AWS::Serverless::Function.InlineCode``.
        :param kms_key_arn: ``AWS::Serverless::Function.KmsKeyArn``.
        :param layers: ``AWS::Serverless::Function.Layers``.
        :param memory_size: ``AWS::Serverless::Function.MemorySize``.
        :param package_type: ``AWS::Serverless::Function.PackageType``.
        :param permissions_boundary: ``AWS::Serverless::Function.PermissionsBoundary``.
        :param policies: ``AWS::Serverless::Function.Policies``.
        :param provisioned_concurrency_config: ``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.
        :param reserved_concurrent_executions: ``AWS::Serverless::Function.ReservedConcurrentExecutions``.
        :param role: ``AWS::Serverless::Function.Role``.
        :param runtime: ``AWS::Serverless::Function.Runtime``.
        :param tags: ``AWS::Serverless::Function.Tags``.
        :param timeout: ``AWS::Serverless::Function.Timeout``.
        :param tracing: ``AWS::Serverless::Function.Tracing``.
        :param version_description: ``AWS::Serverless::Function.VersionDescription``.
        :param vpc_config: ``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_sam as sam
            
            # assume_role_policy_document: Any
            
            cfn_function_props = sam.CfnFunctionProps(
                architectures=["architectures"],
                assume_role_policy_document=assume_role_policy_document,
                auto_publish_alias="autoPublishAlias",
                auto_publish_code_sha256="autoPublishCodeSha256",
                code_signing_config_arn="codeSigningConfigArn",
                code_uri="codeUri",
                dead_letter_queue=sam.CfnFunction.DeadLetterQueueProperty(
                    target_arn="targetArn",
                    type="type"
                ),
                deployment_preference=sam.CfnFunction.DeploymentPreferenceProperty(
                    enabled=False,
                    type="type",
            
                    # the properties below are optional
                    alarms=["alarms"],
                    hooks=sam.CfnFunction.HooksProperty(
                        post_traffic="postTraffic",
                        pre_traffic="preTraffic"
                    )
                ),
                description="description",
                environment=sam.CfnFunction.FunctionEnvironmentProperty(
                    variables={
                        "variables_key": "variables"
                    }
                ),
                event_invoke_config=sam.CfnFunction.EventInvokeConfigProperty(
                    destination_config=sam.CfnFunction.EventInvokeDestinationConfigProperty(
                        on_failure=sam.CfnFunction.DestinationProperty(
                            destination="destination",
            
                            # the properties below are optional
                            type="type"
                        ),
                        on_success=sam.CfnFunction.DestinationProperty(
                            destination="destination",
            
                            # the properties below are optional
                            type="type"
                        )
                    ),
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                events={
                    "events_key": sam.CfnFunction.EventSourceProperty(
                        properties=sam.CfnFunction.S3EventProperty(
                            variables={
                                "variables_key": "variables"
                            }
                        ),
                        type="type"
                    )
                },
                file_system_configs=[sam.CfnFunction.FileSystemConfigProperty(
                    arn="arn",
                    local_mount_path="localMountPath"
                )],
                function_name="functionName",
                handler="handler",
                image_config=sam.CfnFunction.ImageConfigProperty(
                    command=["command"],
                    entry_point=["entryPoint"],
                    working_directory="workingDirectory"
                ),
                image_uri="imageUri",
                inline_code="inlineCode",
                kms_key_arn="kmsKeyArn",
                layers=["layers"],
                memory_size=123,
                package_type="packageType",
                permissions_boundary="permissionsBoundary",
                policies="policies",
                provisioned_concurrency_config=sam.CfnFunction.ProvisionedConcurrencyConfigProperty(
                    provisioned_concurrent_executions="provisionedConcurrentExecutions"
                ),
                reserved_concurrent_executions=123,
                role="role",
                runtime="runtime",
                tags={
                    "tags_key": "tags"
                },
                timeout=123,
                tracing="tracing",
                version_description="versionDescription",
                vpc_config=sam.CfnFunction.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4242ea0641d96c3940b0e5587df1597eb9bde023b751a910d038684585db21)
            check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
            check_type(argname="argument assume_role_policy_document", value=assume_role_policy_document, expected_type=type_hints["assume_role_policy_document"])
            check_type(argname="argument auto_publish_alias", value=auto_publish_alias, expected_type=type_hints["auto_publish_alias"])
            check_type(argname="argument auto_publish_code_sha256", value=auto_publish_code_sha256, expected_type=type_hints["auto_publish_code_sha256"])
            check_type(argname="argument code_signing_config_arn", value=code_signing_config_arn, expected_type=type_hints["code_signing_config_arn"])
            check_type(argname="argument code_uri", value=code_uri, expected_type=type_hints["code_uri"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument deployment_preference", value=deployment_preference, expected_type=type_hints["deployment_preference"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument event_invoke_config", value=event_invoke_config, expected_type=type_hints["event_invoke_config"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument file_system_configs", value=file_system_configs, expected_type=type_hints["file_system_configs"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument inline_code", value=inline_code, expected_type=type_hints["inline_code"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument package_type", value=package_type, expected_type=type_hints["package_type"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument provisioned_concurrency_config", value=provisioned_concurrency_config, expected_type=type_hints["provisioned_concurrency_config"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architectures is not None:
            self._values["architectures"] = architectures
        if assume_role_policy_document is not None:
            self._values["assume_role_policy_document"] = assume_role_policy_document
        if auto_publish_alias is not None:
            self._values["auto_publish_alias"] = auto_publish_alias
        if auto_publish_code_sha256 is not None:
            self._values["auto_publish_code_sha256"] = auto_publish_code_sha256
        if code_signing_config_arn is not None:
            self._values["code_signing_config_arn"] = code_signing_config_arn
        if code_uri is not None:
            self._values["code_uri"] = code_uri
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if deployment_preference is not None:
            self._values["deployment_preference"] = deployment_preference
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if event_invoke_config is not None:
            self._values["event_invoke_config"] = event_invoke_config
        if events is not None:
            self._values["events"] = events
        if file_system_configs is not None:
            self._values["file_system_configs"] = file_system_configs
        if function_name is not None:
            self._values["function_name"] = function_name
        if handler is not None:
            self._values["handler"] = handler
        if image_config is not None:
            self._values["image_config"] = image_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if layers is not None:
            self._values["layers"] = layers
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if package_type is not None:
            self._values["package_type"] = package_type
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if provisioned_concurrency_config is not None:
            self._values["provisioned_concurrency_config"] = provisioned_concurrency_config
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime is not None:
            self._values["runtime"] = runtime
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if version_description is not None:
            self._values["version_description"] = version_description
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Architectures``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-architectures
        '''
        result = self._values.get("architectures")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assume_role_policy_document(self) -> typing.Any:
        '''``AWS::Serverless::Function.AssumeRolePolicyDocument``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-assumerolepolicydocument
        '''
        result = self._values.get("assume_role_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def auto_publish_alias(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishAlias``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("auto_publish_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_publish_code_sha256(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishCodeSha256``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-autopublishcodesha256
        '''
        result = self._values.get("auto_publish_code_sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_signing_config_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.CodeSigningConfigArn``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-codesigningconfigarn
        '''
        result = self._values.get("code_signing_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.S3LocationProperty]]:
        '''``AWS::Serverless::Function.CodeUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("code_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.S3LocationProperty]], result)

    @builtins.property
    def dead_letter_queue(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.DeadLetterQueueProperty]]:
        '''``AWS::Serverless::Function.DeadLetterQueue``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.DeadLetterQueueProperty]], result)

    @builtins.property
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.DeploymentPreferenceProperty]]:
        '''``AWS::Serverless::Function.DeploymentPreference``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
        '''
        result = self._values.get("deployment_preference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.DeploymentPreferenceProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.FunctionEnvironmentProperty]]:
        '''``AWS::Serverless::Function.Environment``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.FunctionEnvironmentProperty]], result)

    @builtins.property
    def event_invoke_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.EventInvokeConfigProperty]]:
        '''``AWS::Serverless::Function.EventInvokeConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("event_invoke_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.EventInvokeConfigProperty]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.EventSourceProperty]]]]:
        '''``AWS::Serverless::Function.Events``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.EventSourceProperty]]]], result)

    @builtins.property
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.FileSystemConfigProperty]]]]:
        '''``AWS::Serverless::Function.FileSystemConfigs``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
        '''
        result = self._values.get("file_system_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.FileSystemConfigProperty]]]], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.FunctionName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Handler``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.ImageConfigProperty]]:
        '''``AWS::Serverless::Function.ImageConfig``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageconfig
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.ImageConfigProperty]], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.ImageUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-imageuri
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.InlineCode``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("inline_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.KmsKeyArn``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Layers``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.MemorySize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PackageType``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-packagetype
        '''
        result = self._values.get("package_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PermissionsBoundary``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.IAMPolicyDocumentProperty, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty]]]]:
        '''``AWS::Serverless::Function.Policies``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.IAMPolicyDocumentProperty, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty]]]], result)

    @builtins.property
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.ProvisionedConcurrencyConfigProperty]]:
        '''``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("provisioned_concurrency_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.ProvisionedConcurrencyConfigProperty]], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.ReservedConcurrentExecutions``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Role``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Runtime``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Function.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.Timeout``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tracing(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Tracing``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.VersionDescription``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.VpcConfigProperty]]:
        '''``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.VpcConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnHttpApi(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-sam.CfnHttpApi",
):
    '''A CloudFormation ``AWS::Serverless::HttpApi``.

    :cloudformationResource: AWS::Serverless::HttpApi
    :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_sam as sam
        
        # authorizers: Any
        # definition_body: Any
        
        cfn_http_api = sam.CfnHttpApi(self, "MyCfnHttpApi",
            access_log_setting=sam.CfnHttpApi.AccessLogSettingProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            auth=sam.CfnHttpApi.HttpApiAuthProperty(
                authorizers=authorizers,
                default_authorizer="defaultAuthorizer"
            ),
            cors_configuration=False,
            default_route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                data_trace_enabled=False,
                detailed_metrics_enabled=False,
                logging_level="loggingLevel",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            ),
            definition_body=definition_body,
            definition_uri="definitionUri",
            description="description",
            disable_execute_api_endpoint=False,
            domain=sam.CfnHttpApi.HttpApiDomainConfigurationProperty(
                certificate_arn="certificateArn",
                domain_name="domainName",
        
                # the properties below are optional
                base_path="basePath",
                endpoint_configuration="endpointConfiguration",
                mutual_tls_authentication=sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version=False
                ),
                route53=sam.CfnHttpApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                ),
                security_policy="securityPolicy"
            ),
            fail_on_warnings=False,
            route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                data_trace_enabled=False,
                detailed_metrics_enabled=False,
                logging_level="loggingLevel",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            ),
            stage_name="stageName",
            stage_variables={
                "stage_variables_key": "stageVariables"
            },
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        access_log_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.HttpApiAuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cors_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.CorsConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.HttpApiDomainConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.RouteSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        stage_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::HttpApi``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_log_setting: ``AWS::Serverless::HttpApi.AccessLogSetting``.
        :param auth: ``AWS::Serverless::HttpApi.Auth``.
        :param cors_configuration: ``AWS::Serverless::HttpApi.CorsConfiguration``.
        :param default_route_settings: ``AWS::Serverless::HttpApi.DefaultRouteSettings``.
        :param definition_body: ``AWS::Serverless::HttpApi.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::HttpApi.DefinitionUri``.
        :param description: ``AWS::Serverless::HttpApi.Description``.
        :param disable_execute_api_endpoint: ``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.
        :param domain: ``AWS::Serverless::HttpApi.Domain``.
        :param fail_on_warnings: ``AWS::Serverless::HttpApi.FailOnWarnings``.
        :param route_settings: ``AWS::Serverless::HttpApi.RouteSettings``.
        :param stage_name: ``AWS::Serverless::HttpApi.StageName``.
        :param stage_variables: ``AWS::Serverless::HttpApi.StageVariables``.
        :param tags: ``AWS::Serverless::HttpApi.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d312f3a7639fbebc5f5860f4c97253365be3518f22a0290a7ab5285a822732)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHttpApiProps(
            access_log_setting=access_log_setting,
            auth=auth,
            cors_configuration=cors_configuration,
            default_route_settings=default_route_settings,
            definition_body=definition_body,
            definition_uri=definition_uri,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            domain=domain,
            fail_on_warnings=fail_on_warnings,
            route_settings=route_settings,
            stage_name=stage_name,
            stage_variables=stage_variables,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e511aa7827771d244ec55a488d07347c36da7f78f16a493302cc5445f0169a9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d1a3ec0fcbb4bfe5d679eace4284a04840a141a63568b1835339822126cac40)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::Serverless::HttpApi.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::HttpApi.DefinitionBody``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Any, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58b5dbedbae4317d4f6e3fd90ed1069321a148cc5d7cf102bb3e19810655c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionBody", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSetting")
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.AccessLogSettingProperty"]]:
        '''``AWS::Serverless::HttpApi.AccessLogSetting``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.AccessLogSettingProperty"]], jsii.get(self, "accessLogSetting"))

    @access_log_setting.setter
    def access_log_setting(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.AccessLogSettingProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92a684b6a70e3453a886715fbb370d88f5574750c12d4c5ed80a24a41eb7b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLogSetting", value)

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.HttpApiAuthProperty"]]:
        '''``AWS::Serverless::HttpApi.Auth``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.HttpApiAuthProperty"]], jsii.get(self, "auth"))

    @auth.setter
    def auth(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.HttpApiAuthProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b250b828fef54caa83ab16698d20da2e1d52414d11503a7c1e70c4e62cd25092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auth", value)

    @builtins.property
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.CorsConfigurationObjectProperty"]]:
        '''``AWS::Serverless::HttpApi.CorsConfiguration``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.CorsConfigurationObjectProperty"]], jsii.get(self, "corsConfiguration"))

    @cors_configuration.setter
    def cors_configuration(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.CorsConfigurationObjectProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5ef6db64fe957e3794bc5d7bc139fa2b2debfa6a4370df82743493c7914c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "corsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRouteSettings")
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.RouteSettingsProperty"]]:
        '''``AWS::Serverless::HttpApi.DefaultRouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.RouteSettingsProperty"]], jsii.get(self, "defaultRouteSettings"))

    @default_route_settings.setter
    def default_route_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.RouteSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb82caa4ab99e088cec6a8e6bb62a59ff43baa7f1c9fe639a270848d7b628a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRouteSettings", value)

    @builtins.property
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.S3LocationProperty"]]:
        '''``AWS::Serverless::HttpApi.DefinitionUri``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.S3LocationProperty"]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.S3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d077cbc57cada4107273d9a5c4b45ddb493db5fa017d8cbd7ea2c7e96a12eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.Description``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a0dbb6852c46789e7c7d5d6018a949f72b078e2c207de9516c81e1033c85247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableExecuteApiEndpoint")
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-httpapi.html#sam-httpapi-disableexecuteapiendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "disableExecuteApiEndpoint"))

    @disable_execute_api_endpoint.setter
    def disable_execute_api_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ac97bf40a4818fbff25fe8116c2aa3dc6a94cf2b04fd106c34ccd7bbfa45bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableExecuteApiEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.HttpApiDomainConfigurationProperty"]]:
        '''``AWS::Serverless::HttpApi.Domain``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.HttpApiDomainConfigurationProperty"]], jsii.get(self, "domain"))

    @domain.setter
    def domain(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.HttpApiDomainConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267f5ecfc6d7c5a6730f26213842ce678608eb6a22521ebe00dd7017b5ceccce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="failOnWarnings")
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::HttpApi.FailOnWarnings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "failOnWarnings"))

    @fail_on_warnings.setter
    def fail_on_warnings(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd8ccb3b930e4bb16381e30bf4e7dd0bdc096b01cc360ccea5c142c8e74e1f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnWarnings", value)

    @builtins.property
    @jsii.member(jsii_name="routeSettings")
    def route_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.RouteSettingsProperty"]]:
        '''``AWS::Serverless::HttpApi.RouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.RouteSettingsProperty"]], jsii.get(self, "routeSettings"))

    @route_settings.setter
    def route_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.RouteSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d3e5d2416a5350b7df87f082c94778f5289232f53093a49d17ed472435503f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeSettings", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.StageName``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611ddfcd42968321486611b5023f95e8b6792cb4e3a8930f123f6b63c2618d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="stageVariables")
    def stage_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::HttpApi.StageVariables``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "stageVariables"))

    @stage_variables.setter
    def stage_variables(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f52073a38cecd1841716e087d6274bf661323ad136bf81f1f798d6a597d76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageVariables", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: ``CfnHttpApi.AccessLogSettingProperty.DestinationArn``.
            :param format: ``CfnHttpApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                access_log_setting_property = sam.CfnHttpApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a7b7d0c234bb6171c7fc6318b46e099d78e6da29e4a28d2d25cbf0b2d24ea82)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.AccessLogSettingProperty.DestinationArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.CorsConfigurationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "allow_origins": "allowOrigins",
            "expose_headers": "exposeHeaders",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationObjectProperty:
        def __init__(
            self,
            *,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
            expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param allow_credentials: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowCredentials``.
            :param allow_headers: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowHeaders``.
            :param allow_methods: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowMethods``.
            :param allow_origins: ``CfnHttpApi.CorsConfigurationObjectProperty.AllowOrigins``.
            :param expose_headers: ``CfnHttpApi.CorsConfigurationObjectProperty.ExposeHeaders``.
            :param max_age: ``CfnHttpApi.CorsConfigurationObjectProperty.MaxAge``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                cors_configuration_object_property = sam.CfnHttpApi.CorsConfigurationObjectProperty(
                    allow_credentials=False,
                    allow_headers=["allowHeaders"],
                    allow_methods=["allowMethods"],
                    allow_origins=["allowOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f438c63a743c26f95015f82101296a2aade0d962b4628e904ae57a928cc3a25)
                check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
                check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
                check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
                check_type(argname="argument allow_origins", value=allow_origins, expected_type=type_hints["allow_origins"])
                check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if allow_origins is not None:
                self._values["allow_origins"] = allow_origins
            if expose_headers is not None:
                self._values["expose_headers"] = expose_headers
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowCredentials``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowHeaders``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowMethods``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.AllowOrigins``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("allow_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.ExposeHeaders``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("expose_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            '''``CfnHttpApi.CorsConfigurationObjectProperty.MaxAge``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration-object
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.HttpApiAuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorizers": "authorizers",
            "default_authorizer": "defaultAuthorizer",
        },
    )
    class HttpApiAuthProperty:
        def __init__(
            self,
            *,
            authorizers: typing.Any = None,
            default_authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param authorizers: ``CfnHttpApi.HttpApiAuthProperty.Authorizers``.
            :param default_authorizer: ``CfnHttpApi.HttpApiAuthProperty.DefaultAuthorizer``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapiauth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # authorizers: Any
                
                http_api_auth_property = sam.CfnHttpApi.HttpApiAuthProperty(
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7753a9357adde30f51603c1a319f3d9f016e679623218999652e044a6fbb3b1f)
                check_type(argname="argument authorizers", value=authorizers, expected_type=type_hints["authorizers"])
                check_type(argname="argument default_authorizer", value=default_authorizer, expected_type=type_hints["default_authorizer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorizers is not None:
                self._values["authorizers"] = authorizers
            if default_authorizer is not None:
                self._values["default_authorizer"] = default_authorizer

        @builtins.property
        def authorizers(self) -> typing.Any:
            '''``CfnHttpApi.HttpApiAuthProperty.Authorizers``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapiauth.html#sam-httpapi-httpapiauth-defaultauthorizer
            '''
            result = self._values.get("authorizers")
            return typing.cast(typing.Any, result)

        @builtins.property
        def default_authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiAuthProperty.DefaultAuthorizer``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapiauth.html#sam-httpapi-httpapiauth-authorizers
            '''
            result = self._values.get("default_authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.HttpApiDomainConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "domain_name": "domainName",
            "base_path": "basePath",
            "endpoint_configuration": "endpointConfiguration",
            "mutual_tls_authentication": "mutualTlsAuthentication",
            "route53": "route53",
            "security_policy": "securityPolicy",
        },
    )
    class HttpApiDomainConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            domain_name: builtins.str,
            base_path: typing.Optional[builtins.str] = None,
            endpoint_configuration: typing.Optional[builtins.str] = None,
            mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.MutualTlsAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            route53: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHttpApi.Route53ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate_arn: ``CfnHttpApi.HttpApiDomainConfigurationProperty.CertificateArn``.
            :param domain_name: ``CfnHttpApi.HttpApiDomainConfigurationProperty.DomainName``.
            :param base_path: ``CfnHttpApi.HttpApiDomainConfigurationProperty.BasePath``.
            :param endpoint_configuration: ``CfnHttpApi.HttpApiDomainConfigurationProperty.EndpointConfiguration``.
            :param mutual_tls_authentication: ``CfnHttpApi.HttpApiDomainConfigurationProperty.MutualTlsAuthentication``.
            :param route53: ``CfnHttpApi.HttpApiDomainConfigurationProperty.Route53``.
            :param security_policy: ``CfnHttpApi.HttpApiDomainConfigurationProperty.SecurityPolicy``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                http_api_domain_configuration_property = sam.CfnHttpApi.HttpApiDomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
                
                    # the properties below are optional
                    base_path="basePath",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version=False
                    ),
                    route53=sam.CfnHttpApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39a0e5b5e2055329f374ebca4a1585f5794b833bde19fc56719f54398083e5ac)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
                check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
                check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
                check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
                check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "domain_name": domain_name,
            }
            if base_path is not None:
                self._values["base_path"] = base_path
            if endpoint_configuration is not None:
                self._values["endpoint_configuration"] = endpoint_configuration
            if mutual_tls_authentication is not None:
                self._values["mutual_tls_authentication"] = mutual_tls_authentication
            if route53 is not None:
                self._values["route53"] = route53
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.CertificateArn``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.DomainName``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def base_path(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.BasePath``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("base_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_configuration(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.EndpointConfiguration``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("endpoint_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mutual_tls_authentication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.MutualTlsAuthenticationProperty"]]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.MutualTlsAuthentication``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-httpapidomainconfiguration.html#sam-httpapi-httpapidomainconfiguration-mutualtlsauthentication
            '''
            result = self._values.get("mutual_tls_authentication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.MutualTlsAuthenticationProperty"]], result)

        @builtins.property
        def route53(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.Route53ConfigurationProperty"]]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.Route53``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("route53")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHttpApi.Route53ConfigurationProperty"]], result)

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.HttpApiDomainConfigurationProperty.SecurityPolicy``.

            :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#domain-configuration-object
            '''
            result = self._values.get("security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpApiDomainConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param truststore_uri: ``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreUri``.
            :param truststore_version: ``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                mutual_tls_authentication_property = sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02a95259d6bec0b4acc410fd7d69b7feeb64e6c8d84b0bb153e8cc3e49211bc2)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreUri``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnHttpApi.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.Route53ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "distributed_domain_name": "distributedDomainName",
            "evaluate_target_health": "evaluateTargetHealth",
            "hosted_zone_id": "hostedZoneId",
            "hosted_zone_name": "hostedZoneName",
            "ip_v6": "ipV6",
        },
    )
    class Route53ConfigurationProperty:
        def __init__(
            self,
            *,
            distributed_domain_name: typing.Optional[builtins.str] = None,
            evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            hosted_zone_name: typing.Optional[builtins.str] = None,
            ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param distributed_domain_name: ``CfnHttpApi.Route53ConfigurationProperty.DistributedDomainName``.
            :param evaluate_target_health: ``CfnHttpApi.Route53ConfigurationProperty.EvaluateTargetHealth``.
            :param hosted_zone_id: ``CfnHttpApi.Route53ConfigurationProperty.HostedZoneId``.
            :param hosted_zone_name: ``CfnHttpApi.Route53ConfigurationProperty.HostedZoneName``.
            :param ip_v6: ``CfnHttpApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                route53_configuration_property = sam.CfnHttpApi.Route53ConfigurationProperty(
                    distributed_domain_name="distributedDomainName",
                    evaluate_target_health=False,
                    hosted_zone_id="hostedZoneId",
                    hosted_zone_name="hostedZoneName",
                    ip_v6=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__887b4b55977498cfae5ab5c5f1e78a5a5324e460fdea4c69085d467964b0d0d1)
                check_type(argname="argument distributed_domain_name", value=distributed_domain_name, expected_type=type_hints["distributed_domain_name"])
                check_type(argname="argument evaluate_target_health", value=evaluate_target_health, expected_type=type_hints["evaluate_target_health"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument hosted_zone_name", value=hosted_zone_name, expected_type=type_hints["hosted_zone_name"])
                check_type(argname="argument ip_v6", value=ip_v6, expected_type=type_hints["ip_v6"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if distributed_domain_name is not None:
                self._values["distributed_domain_name"] = distributed_domain_name
            if evaluate_target_health is not None:
                self._values["evaluate_target_health"] = evaluate_target_health
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if hosted_zone_name is not None:
                self._values["hosted_zone_name"] = hosted_zone_name
            if ip_v6 is not None:
                self._values["ip_v6"] = ip_v6

        @builtins.property
        def distributed_domain_name(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.Route53ConfigurationProperty.DistributedDomainName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-distributiondomainname
            '''
            result = self._values.get("distributed_domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluate_target_health(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnHttpApi.Route53ConfigurationProperty.EvaluateTargetHealth``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-evaluatetargethealth
            '''
            result = self._values.get("evaluate_target_health")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.Route53ConfigurationProperty.HostedZoneId``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_name(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.Route53ConfigurationProperty.HostedZoneName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-hostedzonename
            '''
            result = self._values.get("hosted_zone_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_v6(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnHttpApi.Route53ConfigurationProperty.IpV6``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-httpapi-route53configuration.html#sam-httpapi-route53configuration-ipv6
            '''
            result = self._values.get("ip_v6")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param data_trace_enabled: ``CfnHttpApi.RouteSettingsProperty.DataTraceEnabled``.
            :param detailed_metrics_enabled: ``CfnHttpApi.RouteSettingsProperty.DetailedMetricsEnabled``.
            :param logging_level: ``CfnHttpApi.RouteSettingsProperty.LoggingLevel``.
            :param throttling_burst_limit: ``CfnHttpApi.RouteSettingsProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnHttpApi.RouteSettingsProperty.ThrottlingRateLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                route_settings_property = sam.CfnHttpApi.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef81c6f0b76e8ed12507a896f16b07f9161f429a13f9748ef9bce32520d13aca)
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument detailed_metrics_enabled", value=detailed_metrics_enabled, expected_type=type_hints["detailed_metrics_enabled"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnHttpApi.RouteSettingsProperty.DataTraceEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnHttpApi.RouteSettingsProperty.DetailedMetricsEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-detailedmetricsenabled
            '''
            result = self._values.get("detailed_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''``CfnHttpApi.RouteSettingsProperty.LoggingLevel``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''``CfnHttpApi.RouteSettingsProperty.ThrottlingBurstLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''``CfnHttpApi.RouteSettingsProperty.ThrottlingRateLimit``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnHttpApi.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: jsii.Number,
        ) -> None:
            '''
            :param bucket: ``CfnHttpApi.S3LocationProperty.Bucket``.
            :param key: ``CfnHttpApi.S3LocationProperty.Key``.
            :param version: ``CfnHttpApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_location_property = sam.CfnHttpApi.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0766c8685041f432dcac220c2c37a6004c5db7ab591b8e010dbd8e1f8eeb2393)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
                "version": version,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnHttpApi.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnHttpApi.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> jsii.Number:
            '''``CfnHttpApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-sam.CfnHttpApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log_setting": "accessLogSetting",
        "auth": "auth",
        "cors_configuration": "corsConfiguration",
        "default_route_settings": "defaultRouteSettings",
        "definition_body": "definitionBody",
        "definition_uri": "definitionUri",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "domain": "domain",
        "fail_on_warnings": "failOnWarnings",
        "route_settings": "routeSettings",
        "stage_name": "stageName",
        "stage_variables": "stageVariables",
        "tags": "tags",
    },
)
class CfnHttpApiProps:
    def __init__(
        self,
        *,
        access_log_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.HttpApiAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        cors_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.CorsConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        stage_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnHttpApi``.

        :param access_log_setting: ``AWS::Serverless::HttpApi.AccessLogSetting``.
        :param auth: ``AWS::Serverless::HttpApi.Auth``.
        :param cors_configuration: ``AWS::Serverless::HttpApi.CorsConfiguration``.
        :param default_route_settings: ``AWS::Serverless::HttpApi.DefaultRouteSettings``.
        :param definition_body: ``AWS::Serverless::HttpApi.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::HttpApi.DefinitionUri``.
        :param description: ``AWS::Serverless::HttpApi.Description``.
        :param disable_execute_api_endpoint: ``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.
        :param domain: ``AWS::Serverless::HttpApi.Domain``.
        :param fail_on_warnings: ``AWS::Serverless::HttpApi.FailOnWarnings``.
        :param route_settings: ``AWS::Serverless::HttpApi.RouteSettings``.
        :param stage_name: ``AWS::Serverless::HttpApi.StageName``.
        :param stage_variables: ``AWS::Serverless::HttpApi.StageVariables``.
        :param tags: ``AWS::Serverless::HttpApi.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_sam as sam
            
            # authorizers: Any
            # definition_body: Any
            
            cfn_http_api_props = sam.CfnHttpApiProps(
                access_log_setting=sam.CfnHttpApi.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                auth=sam.CfnHttpApi.HttpApiAuthProperty(
                    authorizers=authorizers,
                    default_authorizer="defaultAuthorizer"
                ),
                cors_configuration=False,
                default_route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                definition_body=definition_body,
                definition_uri="definitionUri",
                description="description",
                disable_execute_api_endpoint=False,
                domain=sam.CfnHttpApi.HttpApiDomainConfigurationProperty(
                    certificate_arn="certificateArn",
                    domain_name="domainName",
            
                    # the properties below are optional
                    base_path="basePath",
                    endpoint_configuration="endpointConfiguration",
                    mutual_tls_authentication=sam.CfnHttpApi.MutualTlsAuthenticationProperty(
                        truststore_uri="truststoreUri",
                        truststore_version=False
                    ),
                    route53=sam.CfnHttpApi.Route53ConfigurationProperty(
                        distributed_domain_name="distributedDomainName",
                        evaluate_target_health=False,
                        hosted_zone_id="hostedZoneId",
                        hosted_zone_name="hostedZoneName",
                        ip_v6=False
                    ),
                    security_policy="securityPolicy"
                ),
                fail_on_warnings=False,
                route_settings=sam.CfnHttpApi.RouteSettingsProperty(
                    data_trace_enabled=False,
                    detailed_metrics_enabled=False,
                    logging_level="loggingLevel",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                ),
                stage_name="stageName",
                stage_variables={
                    "stage_variables_key": "stageVariables"
                },
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347395152d6489cf3fb3b9b060b4aefa49fe509db83763b390118adfb1e8a17e)
            check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument cors_configuration", value=cors_configuration, expected_type=type_hints["cors_configuration"])
            check_type(argname="argument default_route_settings", value=default_route_settings, expected_type=type_hints["default_route_settings"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument fail_on_warnings", value=fail_on_warnings, expected_type=type_hints["fail_on_warnings"])
            check_type(argname="argument route_settings", value=route_settings, expected_type=type_hints["route_settings"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument stage_variables", value=stage_variables, expected_type=type_hints["stage_variables"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if auth is not None:
            self._values["auth"] = auth
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if default_route_settings is not None:
            self._values["default_route_settings"] = default_route_settings
        if definition_body is not None:
            self._values["definition_body"] = definition_body
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if domain is not None:
            self._values["domain"] = domain
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if route_settings is not None:
            self._values["route_settings"] = route_settings
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if stage_variables is not None:
            self._values["stage_variables"] = stage_variables
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.AccessLogSettingProperty]]:
        '''``AWS::Serverless::HttpApi.AccessLogSetting``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.AccessLogSettingProperty]], result)

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.HttpApiAuthProperty]]:
        '''``AWS::Serverless::HttpApi.Auth``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.HttpApiAuthProperty]], result)

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.CorsConfigurationObjectProperty]]:
        '''``AWS::Serverless::HttpApi.CorsConfiguration``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("cors_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.CorsConfigurationObjectProperty]], result)

    @builtins.property
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.RouteSettingsProperty]]:
        '''``AWS::Serverless::HttpApi.DefaultRouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("default_route_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.RouteSettingsProperty]], result)

    @builtins.property
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::HttpApi.DefinitionBody``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("definition_body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.S3LocationProperty]]:
        '''``AWS::Serverless::HttpApi.DefinitionUri``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.S3LocationProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.Description``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::HttpApi.DisableExecuteApiEndpoint``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-httpapi.html#sam-httpapi-disableexecuteapiendpoint
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.HttpApiDomainConfigurationProperty]]:
        '''``AWS::Serverless::HttpApi.Domain``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.HttpApiDomainConfigurationProperty]], result)

    @builtins.property
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::Serverless::HttpApi.FailOnWarnings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("fail_on_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def route_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.RouteSettingsProperty]]:
        '''``AWS::Serverless::HttpApi.RouteSettings``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("route_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.RouteSettingsProperty]], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::HttpApi.StageName``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::HttpApi.StageVariables``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("stage_variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::HttpApi.Tags``.

        :link: https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesshttpapi
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHttpApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLayerVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-sam.CfnLayerVersion",
):
    '''A CloudFormation ``AWS::Serverless::LayerVersion``.

    :cloudformationResource: AWS::Serverless::LayerVersion
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_sam as sam
        
        cfn_layer_version = sam.CfnLayerVersion(self, "MyCfnLayerVersion",
            compatible_runtimes=["compatibleRuntimes"],
            content_uri="contentUri",
            description="description",
            layer_name="layerName",
            license_info="licenseInfo",
            retention_policy="retentionPolicy"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLayerVersion.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::LayerVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compatible_runtimes: ``AWS::Serverless::LayerVersion.CompatibleRuntimes``.
        :param content_uri: ``AWS::Serverless::LayerVersion.ContentUri``.
        :param description: ``AWS::Serverless::LayerVersion.Description``.
        :param layer_name: ``AWS::Serverless::LayerVersion.LayerName``.
        :param license_info: ``AWS::Serverless::LayerVersion.LicenseInfo``.
        :param retention_policy: ``AWS::Serverless::LayerVersion.RetentionPolicy``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b1c8112a6572710e7fa8ab81fbdb9e9cba758115ac10f400b38e8fd3eb7a39)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLayerVersionProps(
            compatible_runtimes=compatible_runtimes,
            content_uri=content_uri,
            description=description,
            layer_name=layer_name,
            license_info=license_info,
            retention_policy=retention_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4485db6a87896370ea15b9541b25822582380e17ea0ed4708bc1688bdc132e7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b0ffebdd4bd69941412694188d8c6d1f55fd0e39b16268eb15787a4dc1ac5f6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::LayerVersion.CompatibleRuntimes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "compatibleRuntimes"))

    @compatible_runtimes.setter
    def compatible_runtimes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b7c69ad755bee7fbe91ca31b7a440f62a634e576e6e8c50aadb7120a684093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibleRuntimes", value)

    @builtins.property
    @jsii.member(jsii_name="contentUri")
    def content_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnLayerVersion.S3LocationProperty"]]:
        '''``AWS::Serverless::LayerVersion.ContentUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnLayerVersion.S3LocationProperty"]], jsii.get(self, "contentUri"))

    @content_uri.setter
    def content_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnLayerVersion.S3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71fb83e8d69d6a6feb3014256556ebec53bae4b2c81fc7eb33c5738051a7a1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b95408556510f242df47bfe71417f6c9d8399cc09c210874101869b0a2335e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="layerName")
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LayerName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "layerName"))

    @layer_name.setter
    def layer_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c39b066e0d4db3c1581f0207f9cb200a3cc3a7b98f42bcc049280940bbc397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layerName", value)

    @builtins.property
    @jsii.member(jsii_name="licenseInfo")
    def license_info(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LicenseInfo``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseInfo"))

    @license_info.setter
    def license_info(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048cef76d654da4f9928a71e24cf13369eb53286911ef70d048bd21e04a36389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseInfo", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPolicy"))

    @retention_policy.setter
    def retention_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d294f39f9a39a31634689fbead54bbcbfa67b759d86b4f7fa2a382a73b660eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicy", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnLayerVersion.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnLayerVersion.S3LocationProperty.Bucket``.
            :param key: ``CfnLayerVersion.S3LocationProperty.Key``.
            :param version: ``CfnLayerVersion.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_location_property = sam.CfnLayerVersion.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b86726824941fefff6e36ce810aa00ac33dfeba4a5afd07903bbd6287ee794ab)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnLayerVersion.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnLayerVersion.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnLayerVersion.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-sam.CfnLayerVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "compatible_runtimes": "compatibleRuntimes",
        "content_uri": "contentUri",
        "description": "description",
        "layer_name": "layerName",
        "license_info": "licenseInfo",
        "retention_policy": "retentionPolicy",
    },
)
class CfnLayerVersionProps:
    def __init__(
        self,
        *,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLayerVersion.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLayerVersion``.

        :param compatible_runtimes: ``AWS::Serverless::LayerVersion.CompatibleRuntimes``.
        :param content_uri: ``AWS::Serverless::LayerVersion.ContentUri``.
        :param description: ``AWS::Serverless::LayerVersion.Description``.
        :param layer_name: ``AWS::Serverless::LayerVersion.LayerName``.
        :param license_info: ``AWS::Serverless::LayerVersion.LicenseInfo``.
        :param retention_policy: ``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_sam as sam
            
            cfn_layer_version_props = sam.CfnLayerVersionProps(
                compatible_runtimes=["compatibleRuntimes"],
                content_uri="contentUri",
                description="description",
                layer_name="layerName",
                license_info="licenseInfo",
                retention_policy="retentionPolicy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7cd99a98ccba0cee58b50d50e1d510fd6f19fc72e9edd0c224b527cfed8f05)
            check_type(argname="argument compatible_runtimes", value=compatible_runtimes, expected_type=type_hints["compatible_runtimes"])
            check_type(argname="argument content_uri", value=content_uri, expected_type=type_hints["content_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument layer_name", value=layer_name, expected_type=type_hints["layer_name"])
            check_type(argname="argument license_info", value=license_info, expected_type=type_hints["license_info"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatible_runtimes is not None:
            self._values["compatible_runtimes"] = compatible_runtimes
        if content_uri is not None:
            self._values["content_uri"] = content_uri
        if description is not None:
            self._values["description"] = description
        if layer_name is not None:
            self._values["layer_name"] = layer_name
        if license_info is not None:
            self._values["license_info"] = license_info
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::LayerVersion.CompatibleRuntimes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("compatible_runtimes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnLayerVersion.S3LocationProperty]]:
        '''``AWS::Serverless::LayerVersion.ContentUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("content_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnLayerVersion.S3LocationProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LayerName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("layer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_info(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LicenseInfo``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("license_info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSimpleTable(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-sam.CfnSimpleTable",
):
    '''A CloudFormation ``AWS::Serverless::SimpleTable``.

    :cloudformationResource: AWS::Serverless::SimpleTable
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_sam as sam
        
        cfn_simple_table = sam.CfnSimpleTable(self, "MyCfnSimpleTable",
            primary_key=sam.CfnSimpleTable.PrimaryKeyProperty(
                type="type",
        
                # the properties below are optional
                name="name"
            ),
            provisioned_throughput=sam.CfnSimpleTable.ProvisionedThroughputProperty(
                write_capacity_units=123,
        
                # the properties below are optional
                read_capacity_units=123
            ),
            sse_specification=sam.CfnSimpleTable.SSESpecificationProperty(
                sse_enabled=False
            ),
            table_name="tableName",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        primary_key: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSimpleTable.PrimaryKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sse_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSimpleTable.SSESpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::SimpleTable``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param primary_key: ``AWS::Serverless::SimpleTable.PrimaryKey``.
        :param provisioned_throughput: ``AWS::Serverless::SimpleTable.ProvisionedThroughput``.
        :param sse_specification: ``AWS::Serverless::SimpleTable.SSESpecification``.
        :param table_name: ``AWS::Serverless::SimpleTable.TableName``.
        :param tags: ``AWS::Serverless::SimpleTable.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5420b6660378767cecf830cbcc165b8f03e153c4a35297a271679130d46d3d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSimpleTableProps(
            primary_key=primary_key,
            provisioned_throughput=provisioned_throughput,
            sse_specification=sse_specification,
            table_name=table_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ce5804f3f29634e1ac3e0aa11ad607c5164e4a53cd19ff1fc2ec362b439f45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff8ee15c4cbe548707fa6bdb12d3f6e0e3f0ec64f0e9c7422cee00da678a0937)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.PrimaryKeyProperty"]]:
        '''``AWS::Serverless::SimpleTable.PrimaryKey``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.PrimaryKeyProperty"]], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.PrimaryKeyProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7856302704d955f8de7c78fd947bf23605ba5bfdd820fa511b6210a41b9626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.ProvisionedThroughputProperty"]]:
        '''``AWS::Serverless::SimpleTable.ProvisionedThroughput``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.ProvisionedThroughputProperty"]], jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.ProvisionedThroughputProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a87e09c1783a14c074097e3343b00ab643903c1932ef4749ff452b4804d821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedThroughput", value)

    @builtins.property
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.SSESpecificationProperty"]]:
        '''``AWS::Serverless::SimpleTable.SSESpecification``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.SSESpecificationProperty"]], jsii.get(self, "sseSpecification"))

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimpleTable.SSESpecificationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68784902f952b811bbf65e06fe8f334ecbad10626ff58b91bed197904ef5700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::SimpleTable.TableName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c482795a676d707c5a59f0705e339b9bcd98067caaad503d7ff13cd4198a02b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnSimpleTable.PrimaryKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "name": "name"},
    )
    class PrimaryKeyProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param type: ``CfnSimpleTable.PrimaryKeyProperty.Type``.
            :param name: ``CfnSimpleTable.PrimaryKeyProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                primary_key_property = sam.CfnSimpleTable.PrimaryKeyProperty(
                    type="type",
                
                    # the properties below are optional
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e47a14e8dbfc019cb472f1996b340636dc72b86fffad039e28975a92982e1d27)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnSimpleTable.PrimaryKeyProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnSimpleTable.PrimaryKeyProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrimaryKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnSimpleTable.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "write_capacity_units": "writeCapacityUnits",
            "read_capacity_units": "readCapacityUnits",
        },
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self,
            *,
            write_capacity_units: jsii.Number,
            read_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param write_capacity_units: ``CfnSimpleTable.ProvisionedThroughputProperty.WriteCapacityUnits``.
            :param read_capacity_units: ``CfnSimpleTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                provisioned_throughput_property = sam.CfnSimpleTable.ProvisionedThroughputProperty(
                    write_capacity_units=123,
                
                    # the properties below are optional
                    read_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13862af4e76efe5150d1f076c865199117e13f26196c8b7621071cf3d01cfc0e)
                check_type(argname="argument write_capacity_units", value=write_capacity_units, expected_type=type_hints["write_capacity_units"])
                check_type(argname="argument read_capacity_units", value=read_capacity_units, expected_type=type_hints["read_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "write_capacity_units": write_capacity_units,
            }
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units

        @builtins.property
        def write_capacity_units(self) -> jsii.Number:
            '''``CfnSimpleTable.ProvisionedThroughputProperty.WriteCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            '''
            result = self._values.get("write_capacity_units")
            assert result is not None, "Required property 'write_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''``CfnSimpleTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnSimpleTable.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param sse_enabled: ``CfnSimpleTable.SSESpecificationProperty.SSEEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s_sESpecification_property = sam.CfnSimpleTable.SSESpecificationProperty(
                    sse_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30a0472b485700ea495dad9f5db4e9104890274e4c48f562f243df83ecabed82)
                check_type(argname="argument sse_enabled", value=sse_enabled, expected_type=type_hints["sse_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnSimpleTable.SSESpecificationProperty.SSEEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-sam.CfnSimpleTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "primary_key": "primaryKey",
        "provisioned_throughput": "provisionedThroughput",
        "sse_specification": "sseSpecification",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnSimpleTableProps:
    def __init__(
        self,
        *,
        primary_key: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.PrimaryKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        sse_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSimpleTable``.

        :param primary_key: ``AWS::Serverless::SimpleTable.PrimaryKey``.
        :param provisioned_throughput: ``AWS::Serverless::SimpleTable.ProvisionedThroughput``.
        :param sse_specification: ``AWS::Serverless::SimpleTable.SSESpecification``.
        :param table_name: ``AWS::Serverless::SimpleTable.TableName``.
        :param tags: ``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_sam as sam
            
            cfn_simple_table_props = sam.CfnSimpleTableProps(
                primary_key=sam.CfnSimpleTable.PrimaryKeyProperty(
                    type="type",
            
                    # the properties below are optional
                    name="name"
                ),
                provisioned_throughput=sam.CfnSimpleTable.ProvisionedThroughputProperty(
                    write_capacity_units=123,
            
                    # the properties below are optional
                    read_capacity_units=123
                ),
                sse_specification=sam.CfnSimpleTable.SSESpecificationProperty(
                    sse_enabled=False
                ),
                table_name="tableName",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af3e54ff6e41752079f553cf40563379f449bd2cff2f9d4724986666fcfd93f)
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument sse_specification", value=sse_specification, expected_type=type_hints["sse_specification"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if primary_key is not None:
            self._values["primary_key"] = primary_key
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.PrimaryKeyProperty]]:
        '''``AWS::Serverless::SimpleTable.PrimaryKey``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.PrimaryKeyProperty]], result)

    @builtins.property
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.ProvisionedThroughputProperty]]:
        '''``AWS::Serverless::SimpleTable.ProvisionedThroughput``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.ProvisionedThroughputProperty]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.SSESpecificationProperty]]:
        '''``AWS::Serverless::SimpleTable.SSESpecification``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.SSESpecificationProperty]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::SimpleTable.TableName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimpleTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStateMachine(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-sam.CfnStateMachine",
):
    '''A CloudFormation ``AWS::Serverless::StateMachine``.

    :cloudformationResource: AWS::Serverless::StateMachine
    :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_sam as sam
        
        # definition: Any
        
        cfn_state_machine = sam.CfnStateMachine(self, "MyCfnStateMachine",
            definition=definition,
            definition_substitutions={
                "definition_substitutions_key": "definitionSubstitutions"
            },
            definition_uri="definitionUri",
            events={
                "events_key": sam.CfnStateMachine.EventSourceProperty(
                    properties=sam.CfnStateMachine.CloudWatchEventEventProperty(
                        method="method",
                        path="path",
        
                        # the properties below are optional
                        rest_api_id="restApiId"
                    ),
                    type="type"
                )
            },
            logging=sam.CfnStateMachine.LoggingConfigurationProperty(
                destinations=[sam.CfnStateMachine.LogDestinationProperty(
                    cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )],
                include_execution_data=False,
                level="level"
            ),
            name="name",
            permissions_boundaries="permissionsBoundaries",
            policies="policies",
            role="role",
            tags={
                "tags_key": "tags"
            },
            tracing=sam.CfnStateMachine.TracingConfigurationProperty(
                enabled=False
            ),
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        definition: typing.Any = None,
        definition_substitutions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.EventSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        logging: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundaries: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.IAMPolicyDocumentProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.SAMPolicyTemplateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.TracingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::StateMachine``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition: ``AWS::Serverless::StateMachine.Definition``.
        :param definition_substitutions: ``AWS::Serverless::StateMachine.DefinitionSubstitutions``.
        :param definition_uri: ``AWS::Serverless::StateMachine.DefinitionUri``.
        :param events: ``AWS::Serverless::StateMachine.Events``.
        :param logging: ``AWS::Serverless::StateMachine.Logging``.
        :param name: ``AWS::Serverless::StateMachine.Name``.
        :param permissions_boundaries: ``AWS::Serverless::StateMachine.PermissionsBoundaries``.
        :param policies: ``AWS::Serverless::StateMachine.Policies``.
        :param role: ``AWS::Serverless::StateMachine.Role``.
        :param tags: ``AWS::Serverless::StateMachine.Tags``.
        :param tracing: ``AWS::Serverless::StateMachine.Tracing``.
        :param type: ``AWS::Serverless::StateMachine.Type``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31dc497519d4835581ef7f7e3ae9e36eff1ce80c8e374e4b5ec2cd62717b95a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStateMachineProps(
            definition=definition,
            definition_substitutions=definition_substitutions,
            definition_uri=definition_uri,
            events=events,
            logging=logging,
            name=name,
            permissions_boundaries=permissions_boundaries,
            policies=policies,
            role=role,
            tags=tags,
            tracing=tracing,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a9d7b5dd5cd04e2c66cfa8daad577da97ae42f5721f797e274e701a0024a52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96876133bb2b704004dd7e9d6d3d490aa552de82ae58ca9a5f539ade481b9453)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::Serverless::StateMachine.Tags``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Any:
        '''``AWS::Serverless::StateMachine.Definition``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Any, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b1c7da7545c517aa189e48eb19bfad7578f676a33d25507b8dbfe3741ee107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="definitionSubstitutions")
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::StateMachine.DefinitionSubstitutions``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "definitionSubstitutions"))

    @definition_substitutions.setter
    def definition_substitutions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bba57b7baea13a57a574d726d92e0e1ff1901e4338d2b8386b1781cef10aece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionSubstitutions", value)

    @builtins.property
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.S3LocationProperty"]]:
        '''``AWS::Serverless::StateMachine.DefinitionUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.S3LocationProperty"]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.S3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0220aeecd3ee69d35b28f00e7afddd9f3cd8c6b7d318f9fc478fe9938737b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionUri", value)

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.EventSourceProperty"]]]]:
        '''``AWS::Serverless::StateMachine.Events``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.EventSourceProperty"]]]], jsii.get(self, "events"))

    @events.setter
    def events(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.EventSourceProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590e24976922d45048bc6f40be998bc920cac5d1bac925f882f99c78f35bf910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.LoggingConfigurationProperty"]]:
        '''``AWS::Serverless::StateMachine.Logging``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.LoggingConfigurationProperty"]], jsii.get(self, "logging"))

    @logging.setter
    def logging(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.LoggingConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e848e8896412cd27f05b5306977537420f72334c0ab63573a5fa782ac76cc4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Name``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d001fdcdfa95970cacd71a43f60873010de2b986441c8df002f5304adb368f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundaries")
    def permissions_boundaries(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.PermissionsBoundaries``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-permissionsboundary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundaries"))

    @permissions_boundaries.setter
    def permissions_boundaries(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c6fbd76aa63726835d9867cc70f94f068ab3a52bcac47e72f3b35e764e38bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundaries", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty"]]]]:
        '''``AWS::Serverless::StateMachine.Policies``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty"]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.IAMPolicyDocumentProperty", typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2e8f0cc5c458de19b7d821171e2a3cdc21d1d96768753d42897fcf38540c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Role``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "role"))

    @role.setter
    def role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388d1a49dcf3d114fb5eafa4f85b475f4b3d635b3a2336cde8e92a0a0721e974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="tracing")
    def tracing(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.TracingConfigurationProperty"]]:
        '''``AWS::Serverless::StateMachine.Tracing``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-tracing
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.TracingConfigurationProperty"]], jsii.get(self, "tracing"))

    @tracing.setter
    def tracing(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.TracingConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d00260df73eabe54a3b4a8834305e5f1af6cc18c436e4386f40bd47e854123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tracing", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ca32324c79b3950bf7fbfda54d03c7b006e8484a7ca70aa7819efbc6c74770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={"method": "method", "path": "path", "rest_api_id": "restApiId"},
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            method: builtins.str,
            path: builtins.str,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param method: ``CfnStateMachine.ApiEventProperty.Method``.
            :param path: ``CfnStateMachine.ApiEventProperty.Path``.
            :param rest_api_id: ``CfnStateMachine.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                api_event_property = sam.CfnStateMachine.ApiEventProperty(
                    method="method",
                    path="path",
                
                    # the properties below are optional
                    rest_api_id="restApiId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51beee57b20b949c97be332bfc1ef9a035f8039e661b4f9692eeddd24f1688f2)
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "method": method,
                "path": path,
            }
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def method(self) -> builtins.str:
            '''``CfnStateMachine.ApiEventProperty.Method``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("method")
            assert result is not None, "Required property 'method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnStateMachine.ApiEventProperty.Path``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnStateMachine.CloudWatchEventEventProperty.Pattern``.
            :param event_bus_name: ``CfnStateMachine.CloudWatchEventEventProperty.EventBusName``.
            :param input: ``CfnStateMachine.CloudWatchEventEventProperty.Input``.
            :param input_path: ``CfnStateMachine.CloudWatchEventEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # pattern: Any
                
                cloud_watch_event_event_property = sam.CfnStateMachine.CloudWatchEventEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86075f01e40bf34536f9cc1a493b784b4d3c27cdf4de64dcf0001608bc03e2f3)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnStateMachine.CloudWatchEventEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.EventBusName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.Input``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.CloudWatchLogsLogGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsLogGroupProperty:
        def __init__(self, *, log_group_arn: builtins.str) -> None:
            '''
            :param log_group_arn: ``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                cloud_watch_logs_log_group_property = sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e0e8acd2f3ab3237de9ae7fbf10c5f1cdf407096f9222d7ae3c0ee8662e1625)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group_arn": log_group_arn,
            }

        @builtins.property
        def log_group_arn(self) -> builtins.str:
            '''``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html
            '''
            result = self._values.get("log_group_arn")
            assert result is not None, "Required property 'log_group_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnStateMachine.EventBridgeRuleEventProperty.Pattern``.
            :param event_bus_name: ``CfnStateMachine.EventBridgeRuleEventProperty.EventBusName``.
            :param input: ``CfnStateMachine.EventBridgeRuleEventProperty.Input``.
            :param input_path: ``CfnStateMachine.EventBridgeRuleEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # pattern: Any
                
                event_bridge_rule_event_property = sam.CfnStateMachine.EventBridgeRuleEventProperty(
                    pattern=pattern,
                
                    # the properties below are optional
                    event_bus_name="eventBusName",
                    input="input",
                    input_path="inputPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6012635d667431d968a70ddfb95541c7bc140a65773810e6471b82323f2b2b45)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument input_path", value=input_path, expected_type=type_hints["input_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.EventBusName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.Input``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.ApiEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.CloudWatchEventEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.EventBridgeRuleEventProperty", typing.Dict[builtins.str, typing.Any]], typing.Union["CfnStateMachine.ScheduleEventProperty", typing.Dict[builtins.str, typing.Any]]],
            type: builtins.str,
        ) -> None:
            '''
            :param properties: ``CfnStateMachine.EventSourceProperty.Properties``.
            :param type: ``CfnStateMachine.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                event_source_property = sam.CfnStateMachine.EventSourceProperty(
                    properties=sam.CfnStateMachine.CloudWatchEventEventProperty(
                        method="method",
                        path="path",
                
                        # the properties below are optional
                        rest_api_id="restApiId"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b789197bde3ea50c0b16529e997be7ec157aef1a1f4fa09f220e1e5f9ad1ea81)
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "properties": properties,
                "type": type,
            }

        @builtins.property
        def properties(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.ApiEventProperty", "CfnStateMachine.CloudWatchEventEventProperty", "CfnStateMachine.EventBridgeRuleEventProperty", "CfnStateMachine.ScheduleEventProperty"]:
            '''``CfnStateMachine.EventSourceProperty.Properties``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-types
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.ApiEventProperty", "CfnStateMachine.CloudWatchEventEventProperty", "CfnStateMachine.EventBridgeRuleEventProperty", "CfnStateMachine.ScheduleEventProperty"], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnStateMachine.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(self, *, function_name: builtins.str) -> None:
            '''
            :param function_name: ``CfnStateMachine.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                function_sAMPTProperty = sam.CfnStateMachine.FunctionSAMPTProperty(
                    function_name="functionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59ca8d9de7a426b6e0f249d5a713c26ff438a90b5d2248a81138df1190bf512d)
                check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_name": function_name,
            }

        @builtins.property
        def function_name(self) -> builtins.str:
            '''``CfnStateMachine.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("function_name")
            assert result is not None, "Required property 'function_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.IAMPolicyDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement", "version": "version"},
    )
    class IAMPolicyDocumentProperty:
        def __init__(self, *, statement: typing.Any, version: builtins.str) -> None:
            '''
            :param statement: ``CfnStateMachine.IAMPolicyDocumentProperty.Statement``.
            :param version: ``CfnStateMachine.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                # statement: Any
                
                i_aMPolicy_document_property = {
                    "statement": statement,
                    "version": "version"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1760aae6a35a7797cc24200f3561677ea5390a40a356d5db6e62badb89c2d7a)
                check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "statement": statement,
                "version": version,
            }

        @builtins.property
        def statement(self) -> typing.Any:
            '''``CfnStateMachine.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''``CfnStateMachine.IAMPolicyDocumentProperty.Version``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IAMPolicyDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.LogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs_log_group": "cloudWatchLogsLogGroup"},
    )
    class LogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''
            :param cloud_watch_logs_log_group: ``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                log_destination_property = sam.CfnStateMachine.LogDestinationProperty(
                    cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                        log_group_arn="logGroupArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2c58f08d741835705c81b4bc6b493193163d9eb6c988036eded5171df096950)
                check_type(argname="argument cloud_watch_logs_log_group", value=cloud_watch_logs_log_group, expected_type=type_hints["cloud_watch_logs_log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cloud_watch_logs_log_group": cloud_watch_logs_log_group,
            }

        @builtins.property
        def cloud_watch_logs_log_group(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.CloudWatchLogsLogGroupProperty"]:
            '''``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            '''
            result = self._values.get("cloud_watch_logs_log_group")
            assert result is not None, "Required property 'cloud_watch_logs_log_group' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.CloudWatchLogsLogGroupProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destinations": "destinations",
            "include_execution_data": "includeExecutionData",
            "level": "level",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destinations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.LogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]],
            include_execution_data: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            level: builtins.str,
        ) -> None:
            '''
            :param destinations: ``CfnStateMachine.LoggingConfigurationProperty.Destinations``.
            :param include_execution_data: ``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.
            :param level: ``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                logging_configuration_property = sam.CfnStateMachine.LoggingConfigurationProperty(
                    destinations=[sam.CfnStateMachine.LogDestinationProperty(
                        cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d609751bc600c452b023a065bb12f6b8bc6fef29e85812b86c4b714c41dc47f)
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destinations": destinations,
                "include_execution_data": include_execution_data,
                "level": level,
            }

        @builtins.property
        def destinations(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.LogDestinationProperty"]]]:
            '''``CfnStateMachine.LoggingConfigurationProperty.Destinations``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("destinations")
            assert result is not None, "Required property 'destinations' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.LogDestinationProperty"]]], result)

        @builtins.property
        def include_execution_data(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("include_execution_data")
            assert result is not None, "Required property 'include_execution_data' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def level(self) -> builtins.str:
            '''``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("level")
            assert result is not None, "Required property 'level' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnStateMachine.S3LocationProperty.Bucket``.
            :param key: ``CfnStateMachine.S3LocationProperty.Key``.
            :param version: ``CfnStateMachine.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s3_location_property = sam.CfnStateMachine.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c6f95c62d01de4708c9d8f947c4ccf2ff0ba7f9ca504135c393d6f5a1adb1cf)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnStateMachine.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.FunctionSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStateMachine.StateMachineSAMPTProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param lambda_invoke_policy: ``CfnStateMachine.SAMPolicyTemplateProperty.LambdaInvokePolicy``.
            :param step_functions_execution_policy: ``CfnStateMachine.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                s_aMPolicy_template_property = sam.CfnStateMachine.SAMPolicyTemplateProperty(
                    lambda_invoke_policy=sam.CfnStateMachine.FunctionSAMPTProperty(
                        function_name="functionName"
                    ),
                    step_functions_execution_policy=sam.CfnStateMachine.StateMachineSAMPTProperty(
                        state_machine_name="stateMachineName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5713cdd830ee24587bbd6de7608856164d057fc159e08fb5bfed1261117539a8)
                check_type(argname="argument lambda_invoke_policy", value=lambda_invoke_policy, expected_type=type_hints["lambda_invoke_policy"])
                check_type(argname="argument step_functions_execution_policy", value=step_functions_execution_policy, expected_type=type_hints["step_functions_execution_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.FunctionSAMPTProperty"]]:
            '''``CfnStateMachine.SAMPolicyTemplateProperty.LambdaInvokePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.FunctionSAMPTProperty"]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.StateMachineSAMPTProperty"]]:
            '''``CfnStateMachine.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStateMachine.StateMachineSAMPTProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule": "schedule", "input": "input"},
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            schedule: builtins.str,
            input: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param schedule: ``CfnStateMachine.ScheduleEventProperty.Schedule``.
            :param input: ``CfnStateMachine.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                schedule_event_property = sam.CfnStateMachine.ScheduleEventProperty(
                    schedule="schedule",
                
                    # the properties below are optional
                    input="input"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d4e011a6d05880c3423cbd2adac46a670019ccbf5f6e90611df5a02a25f7c50)
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule": schedule,
            }
            if input is not None:
                self._values["input"] = input

        @builtins.property
        def schedule(self) -> builtins.str:
            '''``CfnStateMachine.ScheduleEventProperty.Schedule``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("schedule")
            assert result is not None, "Required property 'schedule' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(self, *, state_machine_name: builtins.str) -> None:
            '''
            :param state_machine_name: ``CfnStateMachine.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                state_machine_sAMPTProperty = sam.CfnStateMachine.StateMachineSAMPTProperty(
                    state_machine_name="stateMachineName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2609c24d001f114ebe6e01598e6e2782637764184a93f0a08ccc16e64b0e19ee)
                check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "state_machine_name": state_machine_name,
            }

        @builtins.property
        def state_machine_name(self) -> builtins.str:
            '''``CfnStateMachine.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("state_machine_name")
            assert result is not None, "Required property 'state_machine_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-sam.CfnStateMachine.TracingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class TracingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnStateMachine.TracingConfigurationProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_sam as sam
                
                tracing_configuration_property = sam.CfnStateMachine.TracingConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8511074ad7c55a8cc47e2b9b194bac962a1a4fef07bdfe3b3837ee16c59d0792)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnStateMachine.TracingConfigurationProperty.Enabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tracingconfiguration.html
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TracingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-sam.CfnStateMachineProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "definition_substitutions": "definitionSubstitutions",
        "definition_uri": "definitionUri",
        "events": "events",
        "logging": "logging",
        "name": "name",
        "permissions_boundaries": "permissionsBoundaries",
        "policies": "policies",
        "role": "role",
        "tags": "tags",
        "tracing": "tracing",
        "type": "type",
    },
)
class CfnStateMachineProps:
    def __init__(
        self,
        *,
        definition: typing.Any = None,
        definition_substitutions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        logging: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundaries: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnStateMachine``.

        :param definition: ``AWS::Serverless::StateMachine.Definition``.
        :param definition_substitutions: ``AWS::Serverless::StateMachine.DefinitionSubstitutions``.
        :param definition_uri: ``AWS::Serverless::StateMachine.DefinitionUri``.
        :param events: ``AWS::Serverless::StateMachine.Events``.
        :param logging: ``AWS::Serverless::StateMachine.Logging``.
        :param name: ``AWS::Serverless::StateMachine.Name``.
        :param permissions_boundaries: ``AWS::Serverless::StateMachine.PermissionsBoundaries``.
        :param policies: ``AWS::Serverless::StateMachine.Policies``.
        :param role: ``AWS::Serverless::StateMachine.Role``.
        :param tags: ``AWS::Serverless::StateMachine.Tags``.
        :param tracing: ``AWS::Serverless::StateMachine.Tracing``.
        :param type: ``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_sam as sam
            
            # definition: Any
            
            cfn_state_machine_props = sam.CfnStateMachineProps(
                definition=definition,
                definition_substitutions={
                    "definition_substitutions_key": "definitionSubstitutions"
                },
                definition_uri="definitionUri",
                events={
                    "events_key": sam.CfnStateMachine.EventSourceProperty(
                        properties=sam.CfnStateMachine.CloudWatchEventEventProperty(
                            method="method",
                            path="path",
            
                            # the properties below are optional
                            rest_api_id="restApiId"
                        ),
                        type="type"
                    )
                },
                logging=sam.CfnStateMachine.LoggingConfigurationProperty(
                    destinations=[sam.CfnStateMachine.LogDestinationProperty(
                        cloud_watch_logs_log_group=sam.CfnStateMachine.CloudWatchLogsLogGroupProperty(
                            log_group_arn="logGroupArn"
                        )
                    )],
                    include_execution_data=False,
                    level="level"
                ),
                name="name",
                permissions_boundaries="permissionsBoundaries",
                policies="policies",
                role="role",
                tags={
                    "tags_key": "tags"
                },
                tracing=sam.CfnStateMachine.TracingConfigurationProperty(
                    enabled=False
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2297c2cabaecca5de49cd67e0292da6868b168fc9e15ea7e113ca7feaa77b8de)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_substitutions", value=definition_substitutions, expected_type=type_hints["definition_substitutions"])
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions_boundaries", value=permissions_boundaries, expected_type=type_hints["permissions_boundaries"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if definition is not None:
            self._values["definition"] = definition
        if definition_substitutions is not None:
            self._values["definition_substitutions"] = definition_substitutions
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if events is not None:
            self._values["events"] = events
        if logging is not None:
            self._values["logging"] = logging
        if name is not None:
            self._values["name"] = name
        if permissions_boundaries is not None:
            self._values["permissions_boundaries"] = permissions_boundaries
        if policies is not None:
            self._values["policies"] = policies
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags
        if tracing is not None:
            self._values["tracing"] = tracing
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def definition(self) -> typing.Any:
        '''``AWS::Serverless::StateMachine.Definition``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::StateMachine.DefinitionSubstitutions``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition_substitutions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.S3LocationProperty]]:
        '''``AWS::Serverless::StateMachine.DefinitionUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.S3LocationProperty]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.EventSourceProperty]]]]:
        '''``AWS::Serverless::StateMachine.Events``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.EventSourceProperty]]]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.LoggingConfigurationProperty]]:
        '''``AWS::Serverless::StateMachine.Logging``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.LoggingConfigurationProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Name``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundaries(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.PermissionsBoundaries``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-permissionsboundary
        '''
        result = self._values.get("permissions_boundaries")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.IAMPolicyDocumentProperty, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty]]]]:
        '''``AWS::Serverless::StateMachine.Policies``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.IAMPolicyDocumentProperty, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty]]]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Role``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::StateMachine.Tags``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.TracingConfigurationProperty]]:
        '''``AWS::Serverless::StateMachine.Tracing``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html#sam-statemachine-tracing
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.TracingConfigurationProperty]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApi",
    "CfnApiProps",
    "CfnApplication",
    "CfnApplicationProps",
    "CfnFunction",
    "CfnFunctionProps",
    "CfnHttpApi",
    "CfnHttpApiProps",
    "CfnLayerVersion",
    "CfnLayerVersionProps",
    "CfnSimpleTable",
    "CfnSimpleTableProps",
    "CfnStateMachine",
    "CfnStateMachineProps",
]

publication.publish()

def _typecheckingstub__bf8d174c9489d2435766305e09ee71df1defe3151360d2fc5e08295c8c1fff61(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    stage_name: builtins.str,
    access_log_setting: typing.Optional[typing.Union[typing.Union[CfnApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.AuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    cache_cluster_size: typing.Optional[builtins.str] = None,
    canary_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.DomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_configuration: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_responses: typing.Any = None,
    method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    models: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    open_api_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab635332aa820e8ef3c456c75717d6242466dd771c490de9c30cc50c90f9a2d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9945ab899f7793ed8d7d05dd0af0ef1f61a0d089312f5ee4dd2dfa410fd2addd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f571d6eff7af193f695ce08ba9055086a945a6825b0db81a9372a633d907f334(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db74d14924afe83925def7f858ae642887373eaf81cb7ac70388527a43926717(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f765aa3749509905e01674610c53d8114c1d260081d1892809adbba50efc458(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcb1048bcb4a3802e22124e86ab1e6108d8181040028560b65dd883bf2821bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d412f1e59917cf5da273b8783bb0758018b24da1d204337ed8028c977c8d9f8(
    value: typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71ffe1090292b1a5983c610167357051a3f38cc18793af5f031ae1b9f3201ec(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.AuthProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec45c90609b25b80db89c60a261dbd49352df8fdf99a24bbb1397cdc3f9c0166(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9426603404540095b8720f3644af27f71d1fcb8ff77abb5bb79f5fc99defbef(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7ce5f436b5f27dcc9dbcd95eba6bd79cc6f2f4b304ac59a3fef1aad31699de(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5ede5f9f5e7e45fa78b155176748d34375dc19446d84bccb7a5946db2822f7(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.CanarySettingProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abae15ee346e903b999c29af3a57dd4e0aef52b9d07a664d115417627ad7ab9(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.CorsConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbc70ed3ace1928b2e43a7e6416a4c0fbe8fc7391b8cc98d746925abe1174f0(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.S3LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71379e73816dc66f7afb23c995fa90fd44019ee4dabac582ae2cbb085e01f007(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b900b5f361f659680b647d38c0b7b05dbf2d0bea83e379dbd1c7b7efd2bf68(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f1359b547283059e938153da023a7e2e59f7c468a834dd576834a75c0b0874(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApi.DomainConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995e0bb41529c0c8153e2b7f724c9df7b50ceee1d2f221ffe2f792233db83a85(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApi.EndpointConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5865ec72142bebc767816ad218a1343dc6fe51aa3347c3c55e8beac8e752dfa(
    value: typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b974d2a253b91b4204155ead74e1b9ed515a879f89a74d6cde27ea57116577d1(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13eb8fc594b3cd9d0073a6582028b2a41569fec5f5b4aff7fc5a6ee4ac0740d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df99ef68a133f4dccea37284f6139bfccc4ada67b44c11b577c1c00c83b91ba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05eccaac8d3b8787b8b121d1666cca07c46f86c5893ddb699a861d08ac0a644(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d41210af4cec9e516f29901a1b964a0251fa824d6a25c607c5432c8f338d121(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc864bdb2db7f9256ca4a628b1f3798257fea5b777af5bc86b18474ba8319ee(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a0b1b78bf0aa4cdcb1a5c1aa64f9cc921a2515f1162fd631334b41d11c523c(
    *,
    add_default_authorizer_to_cors_preflight: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    authorizers: typing.Any = None,
    default_authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf12642b1799cdd28b654808811d661261342e364af2cf28fd645059177ba24b(
    *,
    deployment_id: typing.Optional[builtins.str] = None,
    percent_traffic: typing.Optional[jsii.Number] = None,
    stage_variable_overrides: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7420c9d5e03ea8fcff8e2b27bb895760b44fe3c0dd1b0acdd96048fec37f033(
    *,
    allow_origin: builtins.str,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    allow_headers: typing.Optional[builtins.str] = None,
    allow_methods: typing.Optional[builtins.str] = None,
    max_age: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17023b837fd107d56d16f5e6cfb20fb7adb87a282df145943489dacc13318da(
    *,
    certificate_arn: builtins.str,
    domain_name: builtins.str,
    base_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint_configuration: typing.Optional[builtins.str] = None,
    mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.MutualTlsAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
    route53: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.Route53ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072ec80bcc67043294dad0992eac75e08953a9decf4c1e33e36616c0f95db79b(
    *,
    type: typing.Optional[builtins.str] = None,
    vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81afc46b424aae13ba8743df72c104a37810d98e45cce7a47b17147dd26a35d(
    *,
    truststore_uri: typing.Optional[builtins.str] = None,
    truststore_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75305cc3297379268c8dd98bf8bb8ad2fbe572059ac726e8f3b5494c1819da4a(
    *,
    distributed_domain_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85016dbf64ff1ea193e874533036e451057aa02dcb69dc66eb89086b2fe21ea7(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39db9f20be1c63fd66760448d9c4cd306f8d6a772a64376f2ebd70019bff4be3(
    *,
    stage_name: builtins.str,
    access_log_setting: typing.Optional[typing.Union[typing.Union[CfnApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.AuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    cache_cluster_size: typing.Optional[builtins.str] = None,
    canary_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cors: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.DomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_configuration: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApi.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_responses: typing.Any = None,
    method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    models: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    open_api_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a343a3e83f97d9d93c193422a6395bb49b89c851d5d13820cc4ee0800c7ca3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    location: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.ApplicationLocationProperty, typing.Dict[builtins.str, typing.Any]]],
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f520d3639843237397ada9766a893543dd0d3e005ce1121f8d23c4457186d0b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed275051854e188557b1cb332d8f8c9f605d9d1bbc94d3b9bf472343e18001f1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2021f9bfcbae40db46b5ff3fe9b5ffa597a32142707941c05bd5e8b7dca936(
    value: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnApplication.ApplicationLocationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b6d091b94332e4b410a7b83a02b04df28080de0f2030a64b36cf0c8491302d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f44826d3a5ceb952ba5cd138018646d6bc75d031bd65d9d35eaf336ff72e91(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c34a139ee36720735b4fc3c16ef445bbc5726cdef6c17a7764720b273808f9(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b641da8159ee8d1fbd4b614775c4c892c709f7b892ea81e0f0eef0693bca4da(
    *,
    application_id: builtins.str,
    semantic_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb277e43ded51f14816e267ec09f1dd736bcb4fe2b928556bca0f020670774c(
    *,
    location: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.ApplicationLocationProperty, typing.Dict[builtins.str, typing.Any]]],
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505a349cfb16b4f61d5eb6fc256d8fb156607f06908381cdde8969bb46450ba3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    assume_role_policy_document: typing.Any = None,
    auto_publish_alias: typing.Optional[builtins.str] = None,
    auto_publish_code_sha256: typing.Optional[builtins.str] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    code_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DeadLetterQueueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_preference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.FunctionEnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_invoke_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EventInvokeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    file_system_configs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    inline_code: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    tracing: typing.Optional[builtins.str] = None,
    version_description: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a227194132dfe866713746563a00a663c842203935c64a01a26b33a81edf5b69(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cffd0372540845a716d399bb94950623018ba38dd7c46151578398f85a3747(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76580041999f072f492b36f9f65a08fc1b42d11508b005f3225eaf5ef8f238b(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bf4a91f9732d689ee90ea47005ae964231a599e4d3e49c8013f79735b0ef10(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e390b835809cd50e78aa4b1bda3a9996c9c184b36c6d04286baa0c23851256(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b451223c0f7d15179172ad63de0a5d06d9866e36504647e521bf77a2694a69a2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6df8ec87cd12678f51746f0b53c0f25e5981327219ab9ba1fbea3df88ae5ba2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4bd2ba4df045757c62a7a481b38179de040c42e9e1a40d9d640d42c4866833(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.S3LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c58e3d550bd7ad1d9f6a0e5bdb8a3831eaca0e46b144e61c108274e5380fc3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.DeadLetterQueueProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1788f527a96924817e15c7d6a4847759fcd0864c76ad9f93c96753bbf2ebe4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.DeploymentPreferenceProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad8bf22ffe6be903d3107eb15f39f5f2962ba64f19f25d5b0b31fbf1efe2776(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234f08981bde3f79478a4388ecdc87a46d05e0a06a7af842d2a88f3dbd1e1022(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.FunctionEnvironmentProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad1444528ee74e5cbb13a5b9e2fa5aeb3518dab168ecc948b77139a55cc1c28(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.EventInvokeConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c9cd896e5e0ecd9a144131cc87358cccc14d4b052179c3a859f6f6276e5794(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.EventSourceProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dbfdc88b8a5bea5035814d4664b1760ee5412249aee7664aaa0b2d9f0918b9(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.FileSystemConfigProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028f4b2030c1c133e39e86f2783cf06fdc925952146135e8443c51451dd106d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e7e62384916af4852d8e1dd7f913f33c092cac8fcb0ca4dfbef09ec383c0b0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2230d1734a7b9da889259f70dad490f0ca538951ea1f7056ce1c26e0fcae7c65(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.ImageConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424c0d1a53594d96bfd88d7573631584f56da5bad3ffaf1b571809511b7de5b7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b2b96b28e91d6f213ab3b9a43973c4ca6815a6f76cc98bd78f65771ed3f9c4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b456f08d239c4a271736e7d954be37f7b38c186486f4b32a3ce40277b2ab6d32(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67eb0c86ad1b7c5202a15285e7dde55f0979951e96873e3e6cc29a17bf39663(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bfc2a7244ed92a6f592193bb6072aae9644d417ff8c5f521bf53db0bda9b27(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973b2a580bfb638fecb045c1fd744507df1c7d9a85839a588766113d96616865(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50bcfcfd17eacdb1bf85855e2cf03c4f2e2a3cace148c201d8fa7242782b548(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e7694797db1cfa76973fb57894a799db73498f1a9dd6f800b34bcd2fdbcef3(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.IAMPolicyDocumentProperty, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f5759e0c4fea49027eb19472ba127da2c5032562f40c702122c2753b119d77(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.ProvisionedConcurrencyConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87392f1094016feca6eec09ae2aec6e1ac75e33d20ebf897c55d2817c2efe10d(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab904502f3c8fa1dca06625bb988d7c79f6b229d52186659fd9fffef26c6c19(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bc2e3af5c3d51fe4d46357f74f3c3916105e17f01a00c24dc6f57aed89cf63(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387c52e3fbac88c4135b39eb406d9524730796f480b0bab3630baed1b2b2c9ce(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008f4327b6919d0d11762096a2818d6dbf34b01371e2b97d754848be9dfa2aee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a353be62be3f5f2e5c4362ee791fecab56369588b6948164cb781d4c6b0636(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1771ccb6d43e47ac4623b10131885d7b6fde17c2a8e6b0d1b6dd0e5022b118b4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunction.VpcConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa8e4d52af5790a383a1dfd1478c609a053549a865d144b6b5f03f23918df8f(
    *,
    variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01b62e6b0363b01eee2250f5756042c7d680f54357d2a4d2505edeff168b249(
    *,
    method: builtins.str,
    path: builtins.str,
    auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.AuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    request_model: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.RequestModelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    request_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.RequestParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87133f3259f76a6ebba1a6812adeb658d79861f803a3d59b362b9f4165f41841(
    *,
    api_key_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorizer: typing.Optional[builtins.str] = None,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.AuthResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e1719e91bb3aa43d03f49e79361f664be04f825b046eb0ce2a1f8de1980016(
    *,
    aws_account_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_account_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_statements: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
    intrinsic_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpce_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpce_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    intrinsic_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_range_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_range_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_vpc_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_vpc_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d20236c51dd02755482e3bbe3908c77866f14168ba2bb60a4cf0e2f2c72e79(
    *,
    bucket_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d42cedc57e2c46641af5717c6782f0feddf9fb2fed57ccf5fb5580af877f1c6(
    *,
    pattern: typing.Any,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cf09679c7819ce9be2a0ae1187a7eb745c6aab77d6394784f61bfb95cd6398(
    *,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79f63b72bd28e6063161819e64e88bd2f6a3e9696d4546783a82335b27f4f39(
    *,
    trigger: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Sequence[builtins.str]],
    user_pool: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e77fb73265883f664901d8ff52e757fe7f1627d89e18da5e788dc42ed9cbeae(
    *,
    collection_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17a032068fb82887a30716574e611525adb0ed919b817e3bde35924698f6c68(
    *,
    target_arn: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c1c64236480d5626ce4666449aae0363c1193da40f54e09f4ba011037f8e12(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    type: builtins.str,
    alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
    hooks: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.HooksProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f2e1796df1686ac4a7187c75d6f8d6111fa115ef9d1eefd86870eaf619f865(
    *,
    on_failure: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e946903e7d7c6e569d226afd255fb7f52e5059f60382388fe68476cd1430bff(
    *,
    destination: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c181e302b706f28a883e2d074833bca3b3ae88b4eef852ce6c441d8ba3b9d0f1(
    *,
    domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9081bfed1e11a0c683c6afbde969641abc3c5f9a161f6ed0ab2b6dcaa220ea2(
    *,
    starting_position: builtins.str,
    stream: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    destination_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc41a93b3370fb7ad69babd0d7e9b14ac4ef47e0e9c5835e92f8501c58414d58(
    *,
    pattern: typing.Any,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee88e03069ae018abe4b6409ac64aa2e9e2ce6908c6e29cba676c2ab6277948(
    *,
    destination_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EventInvokeDestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656dc15f76064dc2add7ec2c119e09bb254bce2eb9f0a1e3e90cc6f08ed7671f(
    *,
    on_failure: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DestinationProperty, typing.Dict[builtins.str, typing.Any]]],
    on_success: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66da71eac01e4773924ab3c0f785c5b17453496ebaf6d208f4a8d4f9a3c280e(
    *,
    properties: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.AlexaSkillEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.ApiEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.CloudWatchEventEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.CloudWatchLogsEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.CognitoEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.DynamoDBEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.EventBridgeRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.S3EventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SNSEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SQSEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.KinesisEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.ScheduleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.IoTRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.HttpApiEventProperty, typing.Dict[builtins.str, typing.Any]]],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99423913694fe0591e852087ba824fe5be326d91ed2eeda9cf8f019dddd293fe(
    *,
    arn: typing.Optional[builtins.str] = None,
    local_mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5cc15c640ef872fffc367a817baec7975c7f825931d90d8b079428b269d81a(
    *,
    variables: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237d006ecc71dd3aed0c0aa0b90ba04699d8eca82ed309b0723110b72a1e66f2(
    *,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a800f65b32bad5f150236479780db4a521daa6a5bbf8f1edf2fcaffefee51798(
    *,
    post_traffic: typing.Optional[builtins.str] = None,
    pre_traffic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae00b5b46916d36fb90170aae050432f0cc88f9f1b03ea36464506482d01074d(
    *,
    api_id: typing.Optional[builtins.str] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.HttpApiFunctionAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    payload_format_version: typing.Optional[builtins.str] = None,
    route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_in_millis: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f434d8ac59decdc2ff911f0b314edc41a52b0172a7252db0e1d60674eeb01928(
    *,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2ede0291baceced7b910eb7cfe6aa3f775b1ea4407c99372b815743b6c9ae7(
    *,
    statement: typing.Any,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ca80a94d0340c9d16f85b86c087af1442b73e9071fa973443a43db225364cf(
    *,
    identity_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db80b42e70484822ff356a721da6a6769577d734b01ea0f688bbc6444f327789(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    entry_point: typing.Optional[typing.Sequence[builtins.str]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3121f1fef52a8e9581f56f9a5e6144c2d269b4ddb64aea46fddda0394b101618(
    *,
    sql: builtins.str,
    aws_iot_sql_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92727d11b5a9b91b124b1e95cb5c4a131033aaeaf43955a9c05797fdd8811db6(
    *,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e56b37e02a04eb7425d69277f4897db5605d3e1b72750bd4cd2ce034dcc8d20(
    *,
    starting_position: builtins.str,
    stream: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    function_response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6230cf227eb2e7962b69414c9ca43b1491b7c10d0cf42a44fd9584906edf3920(
    *,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121e9784c55c86ce0a439394161d08d7ecb81d38d14ddec8332878ff51c4d381(
    *,
    parameter_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4021ddef1bd86daec9a11ea0350d0cdd68bb96b30cff99381cd3552db9c6c0f2(
    *,
    provisioned_concurrent_executions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264f5be22c104c853c4e499d25140cee70e114ef90ed9488d5d87b50a9b26bf2(
    *,
    queue_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a9c0446a5075dcbd473aeffcddbd0db2fb4ad8b351a7547aac464a05187897(
    *,
    model: builtins.str,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    validate_body: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    validate_parameters: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec70a4e5ab8bf920ef11391480ca9ea3d77cb961c3f636fbd680a7525c793f0(
    *,
    caching: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e362b6b06b1b919ab06228a32a9e359d7a70f3641e7049c13c19977d349312ae(
    *,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38af21ae160c5270503c04a09253853e61ce282db4c3201fbfec9a8ff42f53cf(
    *,
    bucket: builtins.str,
    events: typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Sequence[builtins.str]],
    filter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.S3NotificationFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c556636d8a23436ac5d42b03375c4a0229b10fb815b3b690b5cd2da67f41de29(
    *,
    rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.S3KeyFilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39104646d713050855438706718102007cfa15d75275e6bb80004e3a39eed048(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fe6ffb57da8f0d099872a978c689b3859bb27acabe3051c77b75133bdd9c97(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc566ffda7e98525a21855c11091952a935480b37ab1d408aded87689514113(
    *,
    s3_key: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.S3KeyFilterProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6d8b904c88efeffe795738cbd054646b712e8461a6a97e94b7bb44825adbc5(
    *,
    ami_describe_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    aws_secrets_manager_get_secret_value_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.SecretArnSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_formation_describe_stacks_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_put_metric_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.TableStreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_write_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.TableSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ec2_describe_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    elasticsearch_http_post_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DomainSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_log_events_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.LogGroupSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.StreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_stream_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.StreamSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_decrypt_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.KeySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.FunctionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_detect_only_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_labels_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_no_data_access_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rekognition_write_only_access_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.CollectionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_write_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.BucketSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_bulk_templated_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_email_template_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ses_send_bounce_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IdentitySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns_crud_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.TopicSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns_publish_message_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.TopicSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_poller_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.QueueSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_send_message_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.QueueSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ssm_parameter_read_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.ParameterNameSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.StateMachineSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_access_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EmptySAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbdf0c8ac73225eaf8894e23d446aa68c05f0210c72f9c14a39d8584a6eb80a(
    *,
    topic: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481286c083b1a7b191cfff074603042a66c1d07eaa31144c79c1f5ce7ce7cdb6(
    *,
    queue: builtins.str,
    batch_size: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeac7993745801101c32af47af337bbbacd1e37ef5210801b5eb300d31b8a16b(
    *,
    schedule: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    input: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ba5ad4a2f03c19283a5e54579dc7fc3116227adbda75fc3690f781506cae80(
    *,
    secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75d62622288ec794a77b7dff6389f13c4a9d4d0d860667dfaa020fc70a37fbe(
    *,
    state_machine_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe17bcb601a7203b167645fdd3022838a2ff2ef2fe20599d90662043aa05808(
    *,
    stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18a73d61a969f9f1834e1456de11a9f17a048354363dbe249f8edc201955681(
    *,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d564fc7b8e24d8b70f90c9906af0f501ecca6689dbc26dbfd9e845b51021cd2b(
    *,
    stream_name: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c58e0bd81ab7e11ec5326bf2fbaddc324b9a1e15cf33b45e8970bf2e228c1e6(
    *,
    topic_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8ccdfe6cd335dc2ce3c125af88a28851b7db715ffd0e960112bbfb1bf52724(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4242ea0641d96c3940b0e5587df1597eb9bde023b751a910d038684585db21(
    *,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    assume_role_policy_document: typing.Any = None,
    auto_publish_alias: typing.Optional[builtins.str] = None,
    auto_publish_code_sha256: typing.Optional[builtins.str] = None,
    code_signing_config_arn: typing.Optional[builtins.str] = None,
    code_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DeadLetterQueueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_preference: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.DeploymentPreferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.FunctionEnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_invoke_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EventInvokeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    file_system_configs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.FileSystemConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    function_name: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    image_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.ImageConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    inline_code: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    package_type: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnFunction.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    provisioned_concurrency_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    tracing: typing.Optional[builtins.str] = None,
    version_description: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunction.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d312f3a7639fbebc5f5860f4c97253365be3518f22a0290a7ab5285a822732(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    access_log_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.HttpApiAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cors_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.CorsConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    stage_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e511aa7827771d244ec55a488d07347c36da7f78f16a493302cc5445f0169a9b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1a3ec0fcbb4bfe5d679eace4284a04840a141a63568b1835339822126cac40(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58b5dbedbae4317d4f6e3fd90ed1069321a148cc5d7cf102bb3e19810655c4a(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92a684b6a70e3453a886715fbb370d88f5574750c12d4c5ed80a24a41eb7b6a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.AccessLogSettingProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b250b828fef54caa83ab16698d20da2e1d52414d11503a7c1e70c4e62cd25092(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.HttpApiAuthProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5ef6db64fe957e3794bc5d7bc139fa2b2debfa6a4370df82743493c7914c0c(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.CorsConfigurationObjectProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb82caa4ab99e088cec6a8e6bb62a59ff43baa7f1c9fe639a270848d7b628a4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.RouteSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d077cbc57cada4107273d9a5c4b45ddb493db5fa017d8cbd7ea2c7e96a12eed(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.S3LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0dbb6852c46789e7c7d5d6018a949f72b078e2c207de9516c81e1033c85247(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ac97bf40a4818fbff25fe8116c2aa3dc6a94cf2b04fd106c34ccd7bbfa45bf(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267f5ecfc6d7c5a6730f26213842ce678608eb6a22521ebe00dd7017b5ceccce(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.HttpApiDomainConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd8ccb3b930e4bb16381e30bf4e7dd0bdc096b01cc360ccea5c142c8e74e1f3(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d3e5d2416a5350b7df87f082c94778f5289232f53093a49d17ed472435503f(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnHttpApi.RouteSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611ddfcd42968321486611b5023f95e8b6792cb4e3a8930f123f6b63c2618d10(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f52073a38cecd1841716e087d6274bf661323ad136bf81f1f798d6a597d76d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7b7d0c234bb6171c7fc6318b46e099d78e6da29e4a28d2d25cbf0b2d24ea82(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f438c63a743c26f95015f82101296a2aade0d962b4628e904ae57a928cc3a25(
    *,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7753a9357adde30f51603c1a319f3d9f016e679623218999652e044a6fbb3b1f(
    *,
    authorizers: typing.Any = None,
    default_authorizer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a0e5b5e2055329f374ebca4a1585f5794b833bde19fc56719f54398083e5ac(
    *,
    certificate_arn: builtins.str,
    domain_name: builtins.str,
    base_path: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[builtins.str] = None,
    mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.MutualTlsAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    route53: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.Route53ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a95259d6bec0b4acc410fd7d69b7feeb64e6c8d84b0bb153e8cc3e49211bc2(
    *,
    truststore_uri: typing.Optional[builtins.str] = None,
    truststore_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887b4b55977498cfae5ab5c5f1e78a5a5324e460fdea4c69085d467964b0d0d1(
    *,
    distributed_domain_name: typing.Optional[builtins.str] = None,
    evaluate_target_health: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    hosted_zone_name: typing.Optional[builtins.str] = None,
    ip_v6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef81c6f0b76e8ed12507a896f16b07f9161f429a13f9748ef9bce32520d13aca(
    *,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0766c8685041f432dcac220c2c37a6004c5db7ab591b8e010dbd8e1f8eeb2393(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347395152d6489cf3fb3b9b060b4aefa49fe509db83763b390118adfb1e8a17e(
    *,
    access_log_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.HttpApiAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cors_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.CorsConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    definition_body: typing.Any = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    domain: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.HttpApiDomainConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    route_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHttpApi.RouteSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    stage_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b1c8112a6572710e7fa8ab81fbdb9e9cba758115ac10f400b38e8fd3eb7a39(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLayerVersion.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    layer_name: typing.Optional[builtins.str] = None,
    license_info: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4485db6a87896370ea15b9541b25822582380e17ea0ed4708bc1688bdc132e7c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0ffebdd4bd69941412694188d8c6d1f55fd0e39b16268eb15787a4dc1ac5f6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b7c69ad755bee7fbe91ca31b7a440f62a634e576e6e8c50aadb7120a684093(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fb83e8d69d6a6feb3014256556ebec53bae4b2c81fc7eb33c5738051a7a1fa(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnLayerVersion.S3LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b95408556510f242df47bfe71417f6c9d8399cc09c210874101869b0a2335e4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c39b066e0d4db3c1581f0207f9cb200a3cc3a7b98f42bcc049280940bbc397(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048cef76d654da4f9928a71e24cf13369eb53286911ef70d048bd21e04a36389(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d294f39f9a39a31634689fbead54bbcbfa67b759d86b4f7fa2a382a73b660eea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86726824941fefff6e36ce810aa00ac33dfeba4a5afd07903bbd6287ee794ab(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7cd99a98ccba0cee58b50d50e1d510fd6f19fc72e9edd0c224b527cfed8f05(
    *,
    compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLayerVersion.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    layer_name: typing.Optional[builtins.str] = None,
    license_info: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5420b6660378767cecf830cbcc165b8f03e153c4a35297a271679130d46d3d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    primary_key: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.PrimaryKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ce5804f3f29634e1ac3e0aa11ad607c5164e4a53cd19ff1fc2ec362b439f45(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8ee15c4cbe548707fa6bdb12d3f6e0e3f0ec64f0e9c7422cee00da678a0937(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7856302704d955f8de7c78fd947bf23605ba5bfdd820fa511b6210a41b9626(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.PrimaryKeyProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a87e09c1783a14c074097e3343b00ab643903c1932ef4749ff452b4804d821(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.ProvisionedThroughputProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68784902f952b811bbf65e06fe8f334ecbad10626ff58b91bed197904ef5700(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimpleTable.SSESpecificationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c482795a676d707c5a59f0705e339b9bcd98067caaad503d7ff13cd4198a02b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47a14e8dbfc019cb472f1996b340636dc72b86fffad039e28975a92982e1d27(
    *,
    type: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13862af4e76efe5150d1f076c865199117e13f26196c8b7621071cf3d01cfc0e(
    *,
    write_capacity_units: jsii.Number,
    read_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a0472b485700ea495dad9f5db4e9104890274e4c48f562f243df83ecabed82(
    *,
    sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af3e54ff6e41752079f553cf40563379f449bd2cff2f9d4724986666fcfd93f(
    *,
    primary_key: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.PrimaryKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimpleTable.SSESpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31dc497519d4835581ef7f7e3ae9e36eff1ce80c8e374e4b5ec2cd62717b95a5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    definition: typing.Any = None,
    definition_substitutions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logging: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions_boundaries: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a9d7b5dd5cd04e2c66cfa8daad577da97ae42f5721f797e274e701a0024a52(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96876133bb2b704004dd7e9d6d3d490aa552de82ae58ca9a5f539ade481b9453(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b1c7da7545c517aa189e48eb19bfad7578f676a33d25507b8dbfe3741ee107(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bba57b7baea13a57a574d726d92e0e1ff1901e4338d2b8386b1781cef10aece(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0220aeecd3ee69d35b28f00e7afddd9f3cd8c6b7d318f9fc478fe9938737b8(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.S3LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590e24976922d45048bc6f40be998bc920cac5d1bac925f882f99c78f35bf910(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.EventSourceProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e848e8896412cd27f05b5306977537420f72334c0ab63573a5fa782ac76cc4b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.LoggingConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d001fdcdfa95970cacd71a43f60873010de2b986441c8df002f5304adb368f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c6fbd76aa63726835d9867cc70f94f068ab3a52bcac47e72f3b35e764e38bd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2e8f0cc5c458de19b7d821171e2a3cdc21d1d96768753d42897fcf38540c5f(
    value: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.IAMPolicyDocumentProperty, typing.List[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388d1a49dcf3d114fb5eafa4f85b475f4b3d635b3a2336cde8e92a0a0721e974(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d00260df73eabe54a3b4a8834305e5f1af6cc18c436e4386f40bd47e854123(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStateMachine.TracingConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ca32324c79b3950bf7fbfda54d03c7b006e8484a7ca70aa7819efbc6c74770(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51beee57b20b949c97be332bfc1ef9a035f8039e661b4f9692eeddd24f1688f2(
    *,
    method: builtins.str,
    path: builtins.str,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86075f01e40bf34536f9cc1a493b784b4d3c27cdf4de64dcf0001608bc03e2f3(
    *,
    pattern: typing.Any,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0e8acd2f3ab3237de9ae7fbf10c5f1cdf407096f9222d7ae3c0ee8662e1625(
    *,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6012635d667431d968a70ddfb95541c7bc140a65773810e6471b82323f2b2b45(
    *,
    pattern: typing.Any,
    event_bus_name: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    input_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b789197bde3ea50c0b16529e997be7ec157aef1a1f4fa09f220e1e5f9ad1ea81(
    *,
    properties: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.ApiEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.CloudWatchEventEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.EventBridgeRuleEventProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.ScheduleEventProperty, typing.Dict[builtins.str, typing.Any]]],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ca8d9de7a426b6e0f249d5a713c26ff438a90b5d2248a81138df1190bf512d(
    *,
    function_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1760aae6a35a7797cc24200f3561677ea5390a40a356d5db6e62badb89c2d7a(
    *,
    statement: typing.Any,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c58f08d741835705c81b4bc6b493193163d9eb6c988036eded5171df096950(
    *,
    cloud_watch_logs_log_group: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.CloudWatchLogsLogGroupProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d609751bc600c452b023a065bb12f6b8bc6fef29e85812b86c4b714c41dc47f(
    *,
    destinations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.LogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    include_execution_data: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    level: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6f95c62d01de4708c9d8f947c4ccf2ff0ba7f9ca504135c393d6f5a1adb1cf(
    *,
    bucket: builtins.str,
    key: builtins.str,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5713cdd830ee24587bbd6de7608856164d057fc159e08fb5bfed1261117539a8(
    *,
    lambda_invoke_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.FunctionSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    step_functions_execution_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.StateMachineSAMPTProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4e011a6d05880c3423cbd2adac46a670019ccbf5f6e90611df5a02a25f7c50(
    *,
    schedule: builtins.str,
    input: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2609c24d001f114ebe6e01598e6e2782637764184a93f0a08ccc16e64b0e19ee(
    *,
    state_machine_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8511074ad7c55a8cc47e2b9b194bac962a1a4fef07bdfe3b3837ee16c59d0792(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2297c2cabaecca5de49cd67e0292da6868b168fc9e15ea7e113ca7feaa77b8de(
    *,
    definition: typing.Any = None,
    definition_substitutions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    definition_uri: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    events: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.EventSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logging: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions_boundaries: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, _aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.IAMPolicyDocumentProperty, typing.Dict[builtins.str, typing.Any]], typing.Union[CfnStateMachine.SAMPolicyTemplateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStateMachine.TracingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
