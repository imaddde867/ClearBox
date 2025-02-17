'''
# Amazon CloudWatch Logs Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This library supplies constructs for working with CloudWatch Logs.

## Log Groups/Streams

The basic unit of CloudWatch is a *Log Group*. Every log group typically has the
same kind of data logged to it, in the same format. If there are multiple
applications or services logging into the Log Group, each of them creates a new
*Log Stream*.

Every log operation creates a "log event", which can consist of a simple string
or a single-line JSON object. JSON objects have the advantage that they afford
more filtering abilities (see below).

The only configurable attribute for log streams is the retention period, which
configures after how much time the events in the log stream expire and are
deleted.

The default retention period if not supplied is 2 years, but it can be set to
one of the values in the `RetentionDays` enum to configure a different
retention period (including infinite retention).

```python
# Configure log group for short retention
log_group = LogGroup(stack, "LogGroup",
    retention=RetentionDays.ONE_WEEK
)# Configure log group for infinite retention
log_group = LogGroup(stack, "LogGroup",
    retention=Infinity
)
```

## LogRetention

The `LogRetention` construct is a way to control the retention period of log groups that are created outside of the CDK. The construct is usually
used on log groups that are auto created by AWS services, such as [AWS
lambda](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html).

This is implemented using a [CloudFormation custom
resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html)
which pre-creates the log group if it doesn't exist, and sets the specified log retention period (never expire, by default).

By default, the log group will be created in the same region as the stack. The `logGroupRegion` property can be used to configure
log groups in other regions. This is typically useful when controlling retention for log groups auto-created by global services that
publish their log group to a specific region, such as AWS Chatbot creating a log group in `us-east-1`.

## Resource Policy

CloudWatch Resource Policies allow other AWS services or IAM Principals to put log events into the log groups.
A resource policy is automatically created when `addToResourcePolicy` is called on the LogGroup for the first time:

```python
log_group = logs.LogGroup(self, "LogGroup")
log_group.add_to_resource_policy(iam.PolicyStatement(
    actions=["logs:CreateLogStream", "logs:PutLogEvents"],
    principals=[iam.ServicePrincipal("es.amazonaws.com")],
    resources=[log_group.log_group_arn]
))
```

Or more conveniently, write permissions to the log group can be granted as follows which gives same result as in the above example.

```python
log_group = logs.LogGroup(self, "LogGroup")
log_group.grant_write(iam.ServicePrincipal("es.amazonaws.com"))
```

Be aware that any ARNs or tokenized values passed to the resource policy will be converted into AWS Account IDs.
This is because CloudWatch Logs Resource Policies do not accept ARNs as principals, but they do accept
Account ID strings. Non-ARN principals, like Service principals or Any princpals, are accepted by CloudWatch.

## Encrypting Log Groups

By default, log group data is always encrypted in CloudWatch Logs. You have the
option to encrypt log group data using a AWS KMS customer master key (CMK) should
you not wish to use the default AWS encryption. Keep in mind that if you decide to
encrypt a log group, any service or IAM identity that needs to read the encrypted
log streams in the future will require the same CMK to decrypt the data.

Here's a simple example of creating an encrypted Log Group using a KMS CMK.

```python
import aws_cdk.aws_kms as kms


logs.LogGroup(self, "LogGroup",
    encryption_key=kms.Key(self, "Key")
)
```

See the AWS documentation for more detailed information about [encrypting CloudWatch
Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html).

## Subscriptions and Destinations

Log events matching a particular filter can be sent to either a Lambda function
or a Kinesis stream.

If the Kinesis stream lives in a different account, a `CrossAccountDestination`
object needs to be added in the destination account which will act as a proxy
for the remote Kinesis stream. This object is automatically created for you
if you use the CDK Kinesis library.

Create a `SubscriptionFilter`, initialize it with an appropriate `Pattern` (see
below) and supply the intended destination:

```python
import aws_cdk.aws_logs_destinations as destinations
# fn: lambda.Function
# log_group: logs.LogGroup


logs.SubscriptionFilter(self, "Subscription",
    log_group=log_group,
    destination=destinations.LambdaDestination(fn),
    filter_pattern=logs.FilterPattern.all_terms("ERROR", "MainThread")
)
```

## Metric Filters

CloudWatch Logs can extract and emit metrics based on a textual log stream.
Depending on your needs, this may be a more convenient way of generating metrics
for you application than making calls to CloudWatch Metrics yourself.

A `MetricFilter` either emits a fixed number every time it sees a log event
matching a particular pattern (see below), or extracts a number from the log
event and uses that as the metric value.

Example:

```python
MetricFilter(self, "MetricFilter",
    log_group=log_group,
    metric_namespace="MyApp",
    metric_name="Latency",
    filter_pattern=FilterPattern.exists("$.latency"),
    metric_value="$.latency"
)
```

Remember that if you want to use a value from the log event as the metric value,
you must mention it in your pattern somewhere.

A very simple MetricFilter can be created by using the `logGroup.extractMetric()`
helper function:

```python
# log_group: logs.LogGroup

log_group.extract_metric("$.jsonField", "Namespace", "MetricName")
```

Will extract the value of `jsonField` wherever it occurs in JSON-structed
log records in the LogGroup, and emit them to CloudWatch Metrics under
the name `Namespace/MetricName`.

### Exposing Metric on a Metric Filter

You can expose a metric on a metric filter by calling the `MetricFilter.metric()` API.
This has a default of `statistic = 'avg'` if the statistic is not set in the `props`.

```python
# log_group: logs.LogGroup

mf = logs.MetricFilter(self, "MetricFilter",
    log_group=log_group,
    metric_namespace="MyApp",
    metric_name="Latency",
    filter_pattern=logs.FilterPattern.exists("$.latency"),
    metric_value="$.latency"
)

# expose a metric from the metric filter
metric = mf.metric()

# you can use the metric to create a new alarm
cloudwatch.Alarm(self, "alarm from metric filter",
    metric=metric,
    threshold=100,
    evaluation_periods=2
)
```

## Patterns

Patterns describe which log events match a subscription or metric filter. There
are three types of patterns:

* Text patterns
* JSON patterns
* Space-delimited table patterns

All patterns are constructed by using static functions on the `FilterPattern`
class.

In addition to the patterns above, the following special patterns exist:

* `FilterPattern.allEvents()`: matches all log events.
* `FilterPattern.literal(string)`: if you already know what pattern expression to
  use, this function takes a string and will use that as the log pattern. For
  more information, see the [Filter and Pattern
  Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html).

### Text Patterns

Text patterns match if the literal strings appear in the text form of the log
line.

* `FilterPattern.allTerms(term, term, ...)`: matches if all of the given terms
  (substrings) appear in the log event.
* `FilterPattern.anyTerm(term, term, ...)`: matches if all of the given terms
  (substrings) appear in the log event.
* `FilterPattern.anyTermGroup([term, term, ...], [term, term, ...], ...)`: matches if
  all of the terms in any of the groups (specified as arrays) matches. This is
  an OR match.

Examples:

```python
# Search for lines that contain both "ERROR" and "MainThread"
pattern1 = logs.FilterPattern.all_terms("ERROR", "MainThread")

# Search for lines that either contain both "ERROR" and "MainThread", or
# both "WARN" and "Deadlock".
pattern2 = logs.FilterPattern.any_term_group(["ERROR", "MainThread"], ["WARN", "Deadlock"])
```

## JSON Patterns

JSON patterns apply if the log event is the JSON representation of an object
(without any other characters, so it cannot include a prefix such as timestamp
or log level). JSON patterns can make comparisons on the values inside the
fields.

* **Strings**: the comparison operators allowed for strings are `=` and `!=`.
  String values can start or end with a `*` wildcard.
* **Numbers**: the comparison operators allowed for numbers are `=`, `!=`,
  `<`, `<=`, `>`, `>=`.

Fields in the JSON structure are identified by identifier the complete object as `$`
and then descending into it, such as `$.field` or `$.list[0].field`.

* `FilterPattern.stringValue(field, comparison, string)`: matches if the given
  field compares as indicated with the given string value.
* `FilterPattern.numberValue(field, comparison, number)`: matches if the given
  field compares as indicated with the given numerical value.
* `FilterPattern.isNull(field)`: matches if the given field exists and has the
  value `null`.
* `FilterPattern.notExists(field)`: matches if the given field is not in the JSON
  structure.
* `FilterPattern.exists(field)`: matches if the given field is in the JSON
  structure.
* `FilterPattern.booleanValue(field, boolean)`: matches if the given field
  is exactly the given boolean value.
* `FilterPattern.all(jsonPattern, jsonPattern, ...)`: matches if all of the
  given JSON patterns match. This makes an AND combination of the given
  patterns.
* `FilterPattern.any(jsonPattern, jsonPattern, ...)`: matches if any of the
  given JSON patterns match. This makes an OR combination of the given
  patterns.

Example:

```python
# Search for all events where the component field is equal to
# "HttpServer" and either error is true or the latency is higher
# than 1000.
pattern = logs.FilterPattern.all(
    logs.FilterPattern.string_value("$.component", "=", "HttpServer"),
    logs.FilterPattern.any(
        logs.FilterPattern.boolean_value("$.error", True),
        logs.FilterPattern.number_value("$.latency", ">", 1000)))
```

## Space-delimited table patterns

If the log events are rows of a space-delimited table, this pattern can be used
to identify the columns in that structure and add conditions on any of them. The
canonical example where you would apply this type of pattern is Apache server
logs.

Text that is surrounded by `"..."` quotes or `[...]` square brackets will
be treated as one column.

* `FilterPattern.spaceDelimited(column, column, ...)`: construct a
  `SpaceDelimitedTextPattern` object with the indicated columns. The columns
  map one-by-one the columns found in the log event. The string `"..."` may
  be used to specify an arbitrary number of unnamed columns anywhere in the
  name list (but may only be specified once).

After constructing a `SpaceDelimitedTextPattern`, you can use the following
two members to add restrictions:

* `pattern.whereString(field, comparison, string)`: add a string condition.
  The rules are the same as for JSON patterns.
* `pattern.whereNumber(field, comparison, number)`: add a numerical condition.
  The rules are the same as for JSON patterns.

Multiple restrictions can be added on the same column; they must all apply.

Example:

```python
# Search for all events where the component is "HttpServer" and the
# result code is not equal to 200.
pattern = logs.FilterPattern.space_delimited("time", "component", "...", "result_code", "latency").where_string("component", "=", "HttpServer").where_number("result_code", "!=", 200)
```

## Logs Insights Query Definition

Creates a query definition for CloudWatch Logs Insights.

Example:

```python
logs.QueryDefinition(self, "QueryDefinition",
    query_definition_name="MyQuery",
    query_string=logs.QueryString(
        fields=["@timestamp", "@message"],
        sort="@timestamp desc",
        limit=20
    )
)
```

## Notes

Be aware that Log Group ARNs will always have the string `:*` appended to
them, to match the behavior of [the CloudFormation `AWS::Logs::LogGroup`
resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#aws-resource-logs-loggroup-return-values).
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

import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_9b88bb94
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_kms as _aws_cdk_aws_kms_e491a92b
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDestination(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CfnDestination",
):
    '''A CloudFormation ``AWS::Logs::Destination``.

    The AWS::Logs::Destination resource specifies a CloudWatch Logs destination. A destination encapsulates a physical resource (such as an Amazon Kinesis data stream) and enables you to subscribe that resource to a stream of log events.

    :cloudformationResource: AWS::Logs::Destination
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        
        cfn_destination = logs.CfnDestination(self, "MyCfnDestination",
            destination_name="destinationName",
            role_arn="roleArn",
            target_arn="targetArn",
        
            # the properties below are optional
            destination_policy="destinationPolicy"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        destination_name: builtins.str,
        role_arn: builtins.str,
        target_arn: builtins.str,
        destination_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::Destination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_name: The name of the destination.
        :param role_arn: The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.
        :param target_arn: The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).
        :param destination_policy: An IAM policy document that governs which AWS accounts can create subscription filters against this destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a9ac01bae9592ae8de7203ceca96f34339eaba96a238d69b5c2265bad3cdca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDestinationProps(
            destination_name=destination_name,
            role_arn=role_arn,
            target_arn=target_arn,
            destination_policy=destination_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f710cca39e823468f4bc1cb0679c5d9c9c7a96dcb65b3dff2f69a1030925100)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b87521f6860b8ca9f00d730cabe8e6e9ee43afbad9d8c0bb16b629a00ff7d00a)
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
        '''The ARN of the CloudWatch Logs destination, such as ``arn:aws:logs:us-west-1:123456789012:destination:MyDestination`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> builtins.str:
        '''The name of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationName"))

    @destination_name.setter
    def destination_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61122b82f7f2f9083601326f9b560797424bf0b0520d4a9890eed55fd162dc96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8a01ca68857ebb1bcc73a2c5bdbc87c65e0dc21b9b3147c77eac4fd16ddcd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c515db59a4964ed61af3035341eabae95c893b90584c81c609fb814bc53d51a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value)

    @builtins.property
    @jsii.member(jsii_name="destinationPolicy")
    def destination_policy(self) -> typing.Optional[builtins.str]:
        '''An IAM policy document that governs which AWS accounts can create subscription filters against this destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPolicy"))

    @destination_policy.setter
    def destination_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303977960cdec77aefab8a68771e09a3ec555e46f4141c5101d8c07f5d5cbe2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPolicy", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CfnDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_name": "destinationName",
        "role_arn": "roleArn",
        "target_arn": "targetArn",
        "destination_policy": "destinationPolicy",
    },
)
class CfnDestinationProps:
    def __init__(
        self,
        *,
        destination_name: builtins.str,
        role_arn: builtins.str,
        target_arn: builtins.str,
        destination_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDestination``.

        :param destination_name: The name of the destination.
        :param role_arn: The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.
        :param target_arn: The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).
        :param destination_policy: An IAM policy document that governs which AWS accounts can create subscription filters against this destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            cfn_destination_props = logs.CfnDestinationProps(
                destination_name="destinationName",
                role_arn="roleArn",
                target_arn="targetArn",
            
                # the properties below are optional
                destination_policy="destinationPolicy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6db4f53601d44fc0add1e6aec21a40509733b70a131fac77c05838c2be3a4e7)
            check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument destination_policy", value=destination_policy, expected_type=type_hints["destination_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_name": destination_name,
            "role_arn": role_arn,
            "target_arn": target_arn,
        }
        if destination_policy is not None:
            self._values["destination_policy"] = destination_policy

    @builtins.property
    def destination_name(self) -> builtins.str:
        '''The name of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        '''
        result = self._values.get("destination_name")
        assert result is not None, "Required property 'destination_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_policy(self) -> typing.Optional[builtins.str]:
        '''An IAM policy document that governs which AWS accounts can create subscription filters against this destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        '''
        result = self._values.get("destination_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLogGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CfnLogGroup",
):
    '''A CloudFormation ``AWS::Logs::LogGroup``.

    The ``AWS::Logs::LogGroup`` resource specifies a log group. A log group defines common properties for log streams, such as their retention and access control rules. Each log stream must belong to one log group.

    You can create up to 1,000,000 log groups per Region per account. You must use the following guidelines when naming a log group:

    - Log group names must be unique within a Region for an AWS account.
    - Log group names can be between 1 and 512 characters long.
    - Log group names consist of the following characters: a-z, A-Z, 0-9, '_' (underscore), '-' (hyphen), '/' (forward slash), and '.' (period).

    :cloudformationResource: AWS::Logs::LogGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        
        # data_protection_policy: Any
        
        cfn_log_group = logs.CfnLogGroup(self, "MyCfnLogGroup",
            data_protection_policy=data_protection_policy,
            kms_key_id="kmsKeyId",
            log_group_name="logGroupName",
            retention_in_days=123,
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
        data_protection_policy: typing.Any = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::LogGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_protection_policy: Creates a data protection policy and assigns it to the log group. A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks. For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .
        :param kms_key_id: The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data. To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested. If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error. Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_
        :param log_group_name: The name of the log group. If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.
        :param retention_in_days: The number of days to retain the log events in the specified log group. Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653. To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .
        :param tags: An array of key-value pairs to apply to the log group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee156e4e87958d63d23eb0e81324114b020fb6ae841e65ead5b929ce9e94456)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLogGroupProps(
            data_protection_policy=data_protection_policy,
            kms_key_id=kms_key_id,
            log_group_name=log_group_name,
            retention_in_days=retention_in_days,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bbbbfcb259196087d0b4bd37cfeb7e3473c89c9f83b25b3228236b81861dae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33801a7c7bdd2c40e00cf9273b126c42634ea0d0663aefa0992058b06c6d72fb)
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
        '''The ARN of the log group, such as ``arn:aws:logs:us-west-1:123456789012:log-group:/mystack-testgroup-12ABC1AB12A1:*``.

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
        '''An array of key-value pairs to apply to the log group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionPolicy")
    def data_protection_policy(self) -> typing.Any:
        '''Creates a data protection policy and assigns it to the log group.

        A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks.

        For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-dataprotectionpolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "dataProtectionPolicy"))

    @data_protection_policy.setter
    def data_protection_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f467d550a09cc131afd7d769eae84967fa3ea5091976b7d3153704336c67b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataProtectionPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data.

        To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested.

        If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error.

        Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6002bc9fff029bdb8a6543d1e8d2416cf1b4f3457ae28759dab09fe1c6898a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log group.

        If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4747c815f30ccde544215b45b1cb1118df79a23115e530d7b468e22fea2b949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="retentionInDays")
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain the log events in the specified log group.

        Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653.

        To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-retentionindays
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionInDays"))

    @retention_in_days.setter
    def retention_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282e930518fea7055ed974105ed2dc7f97c9996d0d3448cf3e60ef9cd37e91cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInDays", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CfnLogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_protection_policy": "dataProtectionPolicy",
        "kms_key_id": "kmsKeyId",
        "log_group_name": "logGroupName",
        "retention_in_days": "retentionInDays",
        "tags": "tags",
    },
)
class CfnLogGroupProps:
    def __init__(
        self,
        *,
        data_protection_policy: typing.Any = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLogGroup``.

        :param data_protection_policy: Creates a data protection policy and assigns it to the log group. A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks. For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .
        :param kms_key_id: The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data. To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested. If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error. Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_
        :param log_group_name: The name of the log group. If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.
        :param retention_in_days: The number of days to retain the log events in the specified log group. Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653. To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .
        :param tags: An array of key-value pairs to apply to the log group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            # data_protection_policy: Any
            
            cfn_log_group_props = logs.CfnLogGroupProps(
                data_protection_policy=data_protection_policy,
                kms_key_id="kmsKeyId",
                log_group_name="logGroupName",
                retention_in_days=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f876f18d174156e05ea500405dd37b38662fad2172d38fe2cedb205140d1d8)
            check_type(argname="argument data_protection_policy", value=data_protection_policy, expected_type=type_hints["data_protection_policy"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_protection_policy is not None:
            self._values["data_protection_policy"] = data_protection_policy
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if retention_in_days is not None:
            self._values["retention_in_days"] = retention_in_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_protection_policy(self) -> typing.Any:
        '''Creates a data protection policy and assigns it to the log group.

        A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks.

        For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-dataprotectionpolicy
        '''
        result = self._values.get("data_protection_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key to use when encrypting log data.

        To associate an AWS KMS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested.

        If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error.

        Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS KMS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log group.

        If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain the log events in the specified log group.

        Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653.

        To set a log group so that its log events do not expire, use `DeleteRetentionPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteRetentionPolicy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-retentionindays
        '''
        result = self._values.get("retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to the log group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLogStream(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CfnLogStream",
):
    '''A CloudFormation ``AWS::Logs::LogStream``.

    The ``AWS::Logs::LogStream`` resource specifies an Amazon CloudWatch Logs log stream in a specific log group. A log stream represents the sequence of events coming from an application instance or resource that you are monitoring.

    There is no limit on the number of log streams that you can create for a log group.

    You must use the following guidelines when naming a log stream:

    - Log stream names must be unique within the log group.
    - Log stream names can be between 1 and 512 characters long.
    - The ':' (colon) and '*' (asterisk) characters are not allowed.

    :cloudformationResource: AWS::Logs::LogStream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        
        cfn_log_stream = logs.CfnLogStream(self, "MyCfnLogStream",
            log_group_name="logGroupName",
        
            # the properties below are optional
            log_stream_name="logStreamName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::LogStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param log_group_name: The name of the log group where the log stream is created.
        :param log_stream_name: The name of the log stream. The name must be unique within the log group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0b59ec0df43596ec71b8c73d255febe60b771129a868e7cb92d8d3eb61a372)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLogStreamProps(
            log_group_name=log_group_name, log_stream_name=log_stream_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c68101b277a5b590427f085944025792aa9f4cea807bda8eaa7db50e2a031b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdca3c6b6b25d78535021aa88c44824e59b51d306e8f515581ddb6351b0b26ca)
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
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The name of the log group where the log stream is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9c06bd021523c43325d0c68cf83c99e60d9adfcc1c091ac09edb2cec513b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream.

        The name must be unique within the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c42aedcc85092d202042d0e690983cfb00a574f3af9bf8553f6854cdd106fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CfnLogStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class CfnLogStreamProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLogStream``.

        :param log_group_name: The name of the log group where the log stream is created.
        :param log_stream_name: The name of the log stream. The name must be unique within the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            cfn_log_stream_props = logs.CfnLogStreamProps(
                log_group_name="logGroupName",
            
                # the properties below are optional
                log_stream_name="logStreamName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d1b614107f05b70caafde9559c36f8a34033fcad8c1a2b661d25f7db47c9b8)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
        }
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The name of the log group where the log stream is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream.

        The name must be unique within the log group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnMetricFilter(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CfnMetricFilter",
):
    '''A CloudFormation ``AWS::Logs::MetricFilter``.

    The ``AWS::Logs::MetricFilter`` resource specifies a metric filter that describes how CloudWatch Logs extracts information from logs and transforms it into Amazon CloudWatch metrics. If you have multiple metric filters that are associated with a log group, all the filters are applied to the log streams in that group.

    The maximum number of metric filters that can be associated with a log group is 100.

    :cloudformationResource: AWS::Logs::MetricFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        
        cfn_metric_filter = logs.CfnMetricFilter(self, "MyCfnMetricFilter",
            filter_pattern="filterPattern",
            log_group_name="logGroupName",
            metric_transformations=[logs.CfnMetricFilter.MetricTransformationProperty(
                metric_name="metricName",
                metric_namespace="metricNamespace",
                metric_value="metricValue",
        
                # the properties below are optional
                default_value=123,
                dimensions=[logs.CfnMetricFilter.DimensionProperty(
                    key="key",
                    value="value"
                )],
                unit="unit"
            )],
        
            # the properties below are optional
            filter_name="filterName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        metric_transformations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnMetricFilter.MetricTransformationProperty", typing.Dict[builtins.str, typing.Any]]]]],
        filter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::MetricFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param filter_pattern: A filter pattern for extracting metric data out of ingested log events. For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The name of an existing log group that you want to associate with this metric filter.
        :param metric_transformations: The metric transformations.
        :param filter_name: The name of the metric filter.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21a6e52789f5b4c858131cad8b61c0043016f16923a35d9f224682931bd22c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMetricFilterProps(
            filter_pattern=filter_pattern,
            log_group_name=log_group_name,
            metric_transformations=metric_transformations,
            filter_name=filter_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc98f66fc4412f7d8f891a121d5512a9cf4c965bc42132e83b68d9d3c0b426b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1422eb434acf7c7fcce873af70ac496388e48d82ffb832e09a02600e08cd45)
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
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> builtins.str:
        '''A filter pattern for extracting metric data out of ingested log events.

        For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filterpattern
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterPattern"))

    @filter_pattern.setter
    def filter_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a585c30195f3666ada99fbdf6f84ad426036e1a3db59c256916ec65dd33f95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The name of an existing log group that you want to associate with this metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb235d54c935f08677ae003d9cca22e4d661a759879adae077a65961f72bc7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="metricTransformations")
    def metric_transformations(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMetricFilter.MetricTransformationProperty"]]]:
        '''The metric transformations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-metrictransformations
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMetricFilter.MetricTransformationProperty"]]], jsii.get(self, "metricTransformations"))

    @metric_transformations.setter
    def metric_transformations(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMetricFilter.MetricTransformationProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9b7d18641ff80112260954bd03087eb03ad0d3495fd1465c80d4198d53e9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTransformations", value)

    @builtins.property
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filtername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterName"))

    @filter_name.setter
    def filter_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2308df07571f8c2c8a328b9121673422da964d5b3daf17d425b5583ab7a96bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-logs.CfnMetricFilter.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''Specifies the CloudWatch metric dimensions to publish with this metric.

            Because dimensions are part of the unique identifier for a metric, whenever a unique dimension name/value pair is extracted from your logs, you are creating a new variation of that metric.

            For more information about publishing dimensions with metrics created by metric filters, see `Publishing dimensions with metrics from values in JSON or space-delimited log events <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html#logs-metric-filters-dimensions>`_ .
            .. epigraph::

               Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric.

               To help prevent accidental high charges, Amazon disables a metric filter if it generates 1000 different name/value pairs for the dimensions that you have specified within a certain amount of time.

               You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .

            :param key: The name for the CloudWatch metric dimension that the metric filter creates. Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon (:).
            :param value: The log event field that will contain the value for this dimension. This dimension will only be published for a metric if the value is found in the log event. For example, ``$.eventType`` for JSON log events, or ``$server`` for space-delimited log events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_logs as logs
                
                dimension_property = logs.CfnMetricFilter.DimensionProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a52cbe9cf216e393e5bfdd84a6bfc8de3a133ee543dcdebba72d6e00d4a6fa8f)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The name for the CloudWatch metric dimension that the metric filter creates.

            Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon (:).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html#cfn-logs-metricfilter-dimension-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The log event field that will contain the value for this dimension.

            This dimension will only be published for a metric if the value is found in the log event. For example, ``$.eventType`` for JSON log events, or ``$server`` for space-delimited log events.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html#cfn-logs-metricfilter-dimension-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-logs.CfnMetricFilter.MetricTransformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_name": "metricName",
            "metric_namespace": "metricNamespace",
            "metric_value": "metricValue",
            "default_value": "defaultValue",
            "dimensions": "dimensions",
            "unit": "unit",
        },
    )
    class MetricTransformationProperty:
        def __init__(
            self,
            *,
            metric_name: builtins.str,
            metric_namespace: builtins.str,
            metric_value: builtins.str,
            default_value: typing.Optional[jsii.Number] = None,
            dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnMetricFilter.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricTransformation`` is a property of the ``AWS::Logs::MetricFilter`` resource that describes how to transform log streams into a CloudWatch metric.

            :param metric_name: The name of the CloudWatch metric.
            :param metric_namespace: A custom namespace to contain your metric in CloudWatch. Use namespaces to group together metrics that are similar. For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .
            :param metric_value: The value that is published to the CloudWatch metric. For example, if you're counting the occurrences of a particular term like ``Error`` , specify 1 for the metric value. If you're counting the number of bytes transferred, reference the value that is in the log event by using $. followed by the name of the field that you specified in the filter pattern, such as ``$.size`` .
            :param default_value: (Optional) The value to emit when a filter pattern does not match a log event. This value can be null.
            :param dimensions: The fields to use as dimensions for the metric. One metric filter can include as many as three dimensions. .. epigraph:: Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric. CloudWatch Logs disables a metric filter if it generates 1000 different name/value pairs for your specified dimensions within a certain amount of time. This helps to prevent accidental high charges. You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .
            :param unit: The unit to assign to the metric. If you omit this, the unit is set as ``None`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_logs as logs
                
                metric_transformation_property = logs.CfnMetricFilter.MetricTransformationProperty(
                    metric_name="metricName",
                    metric_namespace="metricNamespace",
                    metric_value="metricValue",
                
                    # the properties below are optional
                    default_value=123,
                    dimensions=[logs.CfnMetricFilter.DimensionProperty(
                        key="key",
                        value="value"
                    )],
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__021ba37262cc618ad0767fad84d5335ca673e2be61f1aecbe4eaf72ab7ed25f8)
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
                check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "metric_name": metric_name,
                "metric_namespace": metric_namespace,
                "metric_value": metric_value,
            }
            if default_value is not None:
                self._values["default_value"] = default_value
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''The name of the CloudWatch metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_namespace(self) -> builtins.str:
            '''A custom namespace to contain your metric in CloudWatch.

            Use namespaces to group together metrics that are similar. For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricnamespace
            '''
            result = self._values.get("metric_namespace")
            assert result is not None, "Required property 'metric_namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_value(self) -> builtins.str:
            '''The value that is published to the CloudWatch metric.

            For example, if you're counting the occurrences of a particular term like ``Error`` , specify 1 for the metric value. If you're counting the number of bytes transferred, reference the value that is in the log event by using $. followed by the name of the field that you specified in the filter pattern, such as ``$.size`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricvalue
            '''
            result = self._values.get("metric_value")
            assert result is not None, "Required property 'metric_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def default_value(self) -> typing.Optional[jsii.Number]:
            '''(Optional) The value to emit when a filter pattern does not match a log event.

            This value can be null.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMetricFilter.DimensionProperty"]]]]:
            '''The fields to use as dimensions for the metric. One metric filter can include as many as three dimensions.

            .. epigraph::

               Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric.

               CloudWatch Logs disables a metric filter if it generates 1000 different name/value pairs for your specified dimensions within a certain amount of time. This helps to prevent accidental high charges.

               You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMetricFilter.DimensionProperty"]]]], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to assign to the metric.

            If you omit this, the unit is set as ``None`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricTransformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CfnMetricFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "metric_transformations": "metricTransformations",
        "filter_name": "filterName",
    },
)
class CfnMetricFilterProps:
    def __init__(
        self,
        *,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        metric_transformations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnMetricFilter.MetricTransformationProperty, typing.Dict[builtins.str, typing.Any]]]]],
        filter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMetricFilter``.

        :param filter_pattern: A filter pattern for extracting metric data out of ingested log events. For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The name of an existing log group that you want to associate with this metric filter.
        :param metric_transformations: The metric transformations.
        :param filter_name: The name of the metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            cfn_metric_filter_props = logs.CfnMetricFilterProps(
                filter_pattern="filterPattern",
                log_group_name="logGroupName",
                metric_transformations=[logs.CfnMetricFilter.MetricTransformationProperty(
                    metric_name="metricName",
                    metric_namespace="metricNamespace",
                    metric_value="metricValue",
            
                    # the properties below are optional
                    default_value=123,
                    dimensions=[logs.CfnMetricFilter.DimensionProperty(
                        key="key",
                        value="value"
                    )],
                    unit="unit"
                )],
            
                # the properties below are optional
                filter_name="filterName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cba185bae3d066dcf278c9667765ab05714c9e433cea02dadc4e5fecbd6625c)
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument metric_transformations", value=metric_transformations, expected_type=type_hints["metric_transformations"])
            check_type(argname="argument filter_name", value=filter_name, expected_type=type_hints["filter_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "log_group_name": log_group_name,
            "metric_transformations": metric_transformations,
        }
        if filter_name is not None:
            self._values["filter_name"] = filter_name

    @builtins.property
    def filter_pattern(self) -> builtins.str:
        '''A filter pattern for extracting metric data out of ingested log events.

        For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The name of an existing log group that you want to associate with this metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_transformations(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnMetricFilter.MetricTransformationProperty]]]:
        '''The metric transformations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-metrictransformations
        '''
        result = self._values.get("metric_transformations")
        assert result is not None, "Required property 'metric_transformations' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnMetricFilter.MetricTransformationProperty]]], result)

    @builtins.property
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filtername
        '''
        result = self._values.get("filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnQueryDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CfnQueryDefinition",
):
    '''A CloudFormation ``AWS::Logs::QueryDefinition``.

    Creates a query definition for CloudWatch Logs Insights. For more information, see `Analyzing Log Data with CloudWatch Logs Insights <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html>`_ .

    :cloudformationResource: AWS::Logs::QueryDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        
        cfn_query_definition = logs.CfnQueryDefinition(self, "MyCfnQueryDefinition",
            name="name",
            query_string="queryString",
        
            # the properties below are optional
            log_group_names=["logGroupNames"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        query_string: builtins.str,
        log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::QueryDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the query definition.
        :param query_string: The query string to use for this query definition. For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .
        :param log_group_names: Use this parameter if you want the query to query only certain log groups.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c504df6b0e06ae31b2c2651181dc1915c131430666f5e6a245aa1e4bc1151dfd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnQueryDefinitionProps(
            name=name, query_string=query_string, log_group_names=log_group_names
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a4b72b95fa1c84707d2d97d220113a5cf4e842fc49f58406492a300f858f17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c039b469a1430de832c8216d3d5b354bd22a55ded3a97804b4c6afd61ede40f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrQueryDefinitionId")
    def attr_query_definition_id(self) -> builtins.str:
        '''The ID of the query definition.

        :cloudformationAttribute: QueryDefinitionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrQueryDefinitionId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the query definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fc5385e32244b4624a5281d81312318a3bdaddeb43f4e11bfcd920aa071a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        '''The query string to use for this query definition.

        For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-querystring
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3401dee44e9a163aaedff81f2f8d91b18b79d895f5159ca5ab9e9e09b6cfc00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupNames")
    def log_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Use this parameter if you want the query to query only certain log groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-loggroupnames
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logGroupNames"))

    @log_group_names.setter
    def log_group_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff23e93375e01a0902f8c8a760a99862ae96fd945bda66450970473ae54fb05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupNames", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CfnQueryDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "query_string": "queryString",
        "log_group_names": "logGroupNames",
    },
)
class CfnQueryDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        query_string: builtins.str,
        log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnQueryDefinition``.

        :param name: A name for the query definition.
        :param query_string: The query string to use for this query definition. For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .
        :param log_group_names: Use this parameter if you want the query to query only certain log groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            cfn_query_definition_props = logs.CfnQueryDefinitionProps(
                name="name",
                query_string="queryString",
            
                # the properties below are optional
                log_group_names=["logGroupNames"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e65de67e25034430f10f63be798a617625c8904620173a4b61102c5c1aa95c6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument log_group_names", value=log_group_names, expected_type=type_hints["log_group_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "query_string": query_string,
        }
        if log_group_names is not None:
            self._values["log_group_names"] = log_group_names

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the query definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''The query string to use for this query definition.

        For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-querystring
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Use this parameter if you want the query to query only certain log groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-loggroupnames
        '''
        result = self._values.get("log_group_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueryDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourcePolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::Logs::ResourcePolicy``.

    Creates or updates a resource policy that allows other AWS services to put log events to this account. An account can have up to 10 resource policies per AWS Region.

    :cloudformationResource: AWS::Logs::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        
        cfn_resource_policy = logs.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            policy_document="policyDocument",
            policy_name="policyName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy_document: builtins.str,
        policy_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Logs::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: The details of the policy. It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.
        :param policy_name: The name of the resource policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3e2cababb17dd0241f31fdecd32f64af1a7275a2864c3162fbe0dd8196a46e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourcePolicyProps(
            policy_document=policy_document, policy_name=policy_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08563cc60984232404b9b0817a2e9f1fa8e4fe4aade8c0e030acedb84563ed29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__981d8a120b09fbeca2b44a5f8d4e65ae3cc35235b57640ad754624cf43948606)
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
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> builtins.str:
        '''The details of the policy.

        It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policydocument
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f381d87a4e705503a754a7b1619644291d0f69a16c95886dc3e6756653f52f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the resource policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69206a0f6c656c7e375579940f365db8322102b5f5b3574e01e76191c6eebb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "policy_name": "policyName"},
)
class CfnResourcePolicyProps:
    def __init__(
        self,
        *,
        policy_document: builtins.str,
        policy_name: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnResourcePolicy``.

        :param policy_document: The details of the policy. It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.
        :param policy_name: The name of the resource policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            cfn_resource_policy_props = logs.CfnResourcePolicyProps(
                policy_document="policyDocument",
                policy_name="policyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627e6ef869672b1b7bb67bd5a74bdba32c341c134f9cad705b28f81b8f0e1a38)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
            "policy_name": policy_name,
        }

    @builtins.property
    def policy_document(self) -> builtins.str:
        '''The details of the policy.

        It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the resource policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSubscriptionFilter(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CfnSubscriptionFilter",
):
    '''A CloudFormation ``AWS::Logs::SubscriptionFilter``.

    The ``AWS::Logs::SubscriptionFilter`` resource specifies a subscription filter and associates it with the specified log group. Subscription filters allow you to subscribe to a real-time stream of log events and have them delivered to a specific destination. Currently, the supported destinations are:

    - An Amazon Kinesis data stream belonging to the same account as the subscription filter, for same-account delivery.
    - A logical destination that belongs to a different account, for cross-account delivery.
    - An Amazon Kinesis Firehose delivery stream that belongs to the same account as the subscription filter, for same-account delivery.
    - An AWS Lambda function that belongs to the same account as the subscription filter, for same-account delivery.

    There can be as many as two subscription filters associated with a log group.

    :cloudformationResource: AWS::Logs::SubscriptionFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        
        cfn_subscription_filter = logs.CfnSubscriptionFilter(self, "MyCfnSubscriptionFilter",
            destination_arn="destinationArn",
            filter_pattern="filterPattern",
            log_group_name="logGroupName",
        
            # the properties below are optional
            distribution="distribution",
            filter_name="filterName",
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        destination_arn: builtins.str,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        distribution: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::SubscriptionFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: The Amazon Resource Name (ARN) of the destination.
        :param filter_pattern: The filtering expressions that restrict what gets delivered to the destination AWS resource. For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The log group to associate with the subscription filter. All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.
        :param distribution: The method used to distribute log data to the destination, which can be either random or grouped by log stream.
        :param filter_name: The name of the subscription filter.
        :param role_arn: The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream. You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c309b6e47084dd6203318a3fa9b57377c3b49b057c711617683f6f4b712c13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubscriptionFilterProps(
            destination_arn=destination_arn,
            filter_pattern=filter_pattern,
            log_group_name=log_group_name,
            distribution=distribution,
            filter_name=filter_name,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac5ce7ab85414a9ab4d07a6730c90303a0f6f9d21900acfa34cbad1068c3e34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb14361fed02c4db43a0932407afa9b0115a6a35087a2cf2b8f2ca11127a800)
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
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-destinationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e798c2dcd3c6b5c8f4ed5e7f12612acaf7bd564ad175f0e8dc29ff7f64a76552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> builtins.str:
        '''The filtering expressions that restrict what gets delivered to the destination AWS resource.

        For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filterpattern
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterPattern"))

    @filter_pattern.setter
    def filter_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7837bfc99de40bda02092ef11f3ab18f09fa3b4a2af655884615123b2238901b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The log group to associate with the subscription filter.

        All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a848ba126c9392809ea99ca5e19a9daad4d405a9bd5ad71113a6eba8a8d729d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> typing.Optional[builtins.str]:
        '''The method used to distribute log data to the destination, which can be either random or grouped by log stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-distribution
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30c53e2238044eeabdb58fe12521d512be68ba9124a96f3bfc5367e0406ee06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value)

    @builtins.property
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filtername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterName"))

    @filter_name.setter
    def filter_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c19e816d1f986e29273f06ae0b73ed2a7554099fac6ca8c5b0a72de8709544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream.

        You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288732d67b6d776d3fbb3ea79ed6035ffe508f4e6e884b4c7f85e72b0ceaf072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CfnSubscriptionFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_arn": "destinationArn",
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "distribution": "distribution",
        "filter_name": "filterName",
        "role_arn": "roleArn",
    },
)
class CfnSubscriptionFilterProps:
    def __init__(
        self,
        *,
        destination_arn: builtins.str,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        distribution: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSubscriptionFilter``.

        :param destination_arn: The Amazon Resource Name (ARN) of the destination.
        :param filter_pattern: The filtering expressions that restrict what gets delivered to the destination AWS resource. For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The log group to associate with the subscription filter. All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.
        :param distribution: The method used to distribute log data to the destination, which can be either random or grouped by log stream.
        :param filter_name: The name of the subscription filter.
        :param role_arn: The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream. You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            cfn_subscription_filter_props = logs.CfnSubscriptionFilterProps(
                destination_arn="destinationArn",
                filter_pattern="filterPattern",
                log_group_name="logGroupName",
            
                # the properties below are optional
                distribution="distribution",
                filter_name="filterName",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ffd84b26d5803b73c5cf3c6076240ee2f143dee48f27b0d5bd9812df5a4e097)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument filter_name", value=filter_name, expected_type=type_hints["filter_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_arn": destination_arn,
            "filter_pattern": filter_pattern,
            "log_group_name": log_group_name,
        }
        if distribution is not None:
            self._values["distribution"] = distribution
        if filter_name is not None:
            self._values["filter_name"] = filter_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-destinationarn
        '''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_pattern(self) -> builtins.str:
        '''The filtering expressions that restrict what gets delivered to the destination AWS resource.

        For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The log group to associate with the subscription filter.

        All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def distribution(self) -> typing.Optional[builtins.str]:
        '''The method used to distribute log data to the destination, which can be either random or grouped by log stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-distribution
        '''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription filter.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filtername
        '''
        result = self._values.get("filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream.

        You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.ColumnRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "comparison": "comparison",
        "number_value": "numberValue",
        "string_value": "stringValue",
    },
)
class ColumnRestriction:
    def __init__(
        self,
        *,
        comparison: builtins.str,
        number_value: typing.Optional[jsii.Number] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparison: Comparison operator to use.
        :param number_value: Number value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.
        :param string_value: String value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            column_restriction = logs.ColumnRestriction(
                comparison="comparison",
            
                # the properties below are optional
                number_value=123,
                string_value="stringValue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25991b0f3cd90c0ead8b679929ca6482be293e771ca4be27d23be9b0b1518a31)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument number_value", value=number_value, expected_type=type_hints["number_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
        }
        if number_value is not None:
            self._values["number_value"] = number_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def comparison(self) -> builtins.str:
        '''Comparison operator to use.'''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def number_value(self) -> typing.Optional[jsii.Number]:
        '''Number value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.
        '''
        result = self._values.get("number_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColumnRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.CrossAccountDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "role": "role",
        "target_arn": "targetArn",
        "destination_name": "destinationName",
    },
)
class CrossAccountDestinationProps:
    def __init__(
        self,
        *,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
        target_arn: builtins.str,
        destination_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a CrossAccountDestination.

        :param role: The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: The log destination target's ARN.
        :param destination_name: The name of the log destination. Default: Automatically generated

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_logs as logs
            
            # role: iam.Role
            
            cross_account_destination_props = logs.CrossAccountDestinationProps(
                role=role,
                target_arn="targetArn",
            
                # the properties below are optional
                destination_name="destinationName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8385eb16ba3569f03e0da403285b09a1cd68fb4851cb34cfde7d1db0908e5f12)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
            "target_arn": target_arn,
        }
        if destination_name is not None:
            self._values["destination_name"] = destination_name

    @builtins.property
    def role(self) -> _aws_cdk_aws_iam_940a1ce0.IRole:
        '''The role to assume that grants permissions to write to 'target'.

        The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IRole, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''The log destination target's ARN.'''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log destination.

        :default: Automatically generated
        '''
        result = self._values.get("destination_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossAccountDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilterPattern(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.FilterPattern",
):
    '''A collection of static methods to generate appropriate ILogPatterns.

    :exampleMetadata: infused

    Example::

        # Search for lines that contain both "ERROR" and "MainThread"
        pattern1 = logs.FilterPattern.all_terms("ERROR", "MainThread")
        
        # Search for lines that either contain both "ERROR" and "MainThread", or
        # both "WARN" and "Deadlock".
        pattern2 = logs.FilterPattern.any_term_group(["ERROR", "MainThread"], ["WARN", "Deadlock"])
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls, *patterns: "JsonPattern") -> "JsonPattern":
        '''A JSON log pattern that matches if all given JSON log patterns match.

        :param patterns: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12c867dce60bf09173093bf750d392ba4689c977ab027b6bb00cbd4ac4de8af)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "all", [*patterns]))

    @jsii.member(jsii_name="allEvents")
    @builtins.classmethod
    def all_events(cls) -> "IFilterPattern":
        '''A log pattern that matches all events.'''
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "allEvents", []))

    @jsii.member(jsii_name="allTerms")
    @builtins.classmethod
    def all_terms(cls, *terms: builtins.str) -> "IFilterPattern":
        '''A log pattern that matches if all the strings given appear in the event.

        :param terms: The words to search for. All terms must match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dddfad7e68dbd267d67c2e6243cb3474e87d4e15f4bde1bcb14a572c64e4b9d4)
            check_type(argname="argument terms", value=terms, expected_type=typing.Tuple[type_hints["terms"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "allTerms", [*terms]))

    @jsii.member(jsii_name="any")
    @builtins.classmethod
    def any(cls, *patterns: "JsonPattern") -> "JsonPattern":
        '''A JSON log pattern that matches if any of the given JSON log patterns match.

        :param patterns: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8daf7ed22088c64251f58d811acc49d51c39ef2fb6512905b61f8212603a6dce)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "any", [*patterns]))

    @jsii.member(jsii_name="anyTerm")
    @builtins.classmethod
    def any_term(cls, *terms: builtins.str) -> "IFilterPattern":
        '''A log pattern that matches if any of the strings given appear in the event.

        :param terms: The words to search for. Any terms must match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c086083fcdc9729199ce19516c28925c398d32d2bf4385f066140b5bd0ae93)
            check_type(argname="argument terms", value=terms, expected_type=typing.Tuple[type_hints["terms"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "anyTerm", [*terms]))

    @jsii.member(jsii_name="anyTermGroup")
    @builtins.classmethod
    def any_term_group(
        cls,
        *term_groups: typing.List[builtins.str],
    ) -> "IFilterPattern":
        '''A log pattern that matches if any of the given term groups matches the event.

        A term group matches an event if all the terms in it appear in the event string.

        :param term_groups: A list of term groups to search for. Any one of the clauses must match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f490dc1cc4cb4c652bd94b41be028f11b34b43888af74efa67a48dcc0a7e3192)
            check_type(argname="argument term_groups", value=term_groups, expected_type=typing.Tuple[type_hints["term_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "anyTermGroup", [*term_groups]))

    @jsii.member(jsii_name="booleanValue")
    @builtins.classmethod
    def boolean_value(
        cls,
        json_field: builtins.str,
        value: builtins.bool,
    ) -> "JsonPattern":
        '''A JSON log pattern that matches if the field exists and equals the boolean value.

        :param json_field: Field inside JSON. Example: "$.myField"
        :param value: The value to match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5feb09f01306ac3af00a9343e2e42afcf2821bcb2c5496e2ad37f5bf6c744e3e)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "booleanValue", [json_field, value]))

    @jsii.member(jsii_name="exists")
    @builtins.classmethod
    def exists(cls, json_field: builtins.str) -> "JsonPattern":
        '''A JSON log patter that matches if the field exists.

        This is a readable convenience wrapper over 'field = *'

        :param json_field: Field inside JSON. Example: "$.myField"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce84d76799399782f65215b9e275e5911bac66ec446b2b1911f993c31066de80)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "exists", [json_field]))

    @jsii.member(jsii_name="isNull")
    @builtins.classmethod
    def is_null(cls, json_field: builtins.str) -> "JsonPattern":
        '''A JSON log pattern that matches if the field exists and has the special value 'null'.

        :param json_field: Field inside JSON. Example: "$.myField"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e623cfcbdc8db428e5c910dbabfa70dec2e5ca569e002af922c4e0687ba4d54a)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "isNull", [json_field]))

    @jsii.member(jsii_name="literal")
    @builtins.classmethod
    def literal(cls, log_pattern_string: builtins.str) -> "IFilterPattern":
        '''Use the given string as log pattern.

        See https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html
        for information on writing log patterns.

        :param log_pattern_string: The pattern string to use.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9d3fcaa8b1b00f55df678f5944d9e544caf68b8d4ab2324976f80113dd0861)
            check_type(argname="argument log_pattern_string", value=log_pattern_string, expected_type=type_hints["log_pattern_string"])
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "literal", [log_pattern_string]))

    @jsii.member(jsii_name="notExists")
    @builtins.classmethod
    def not_exists(cls, json_field: builtins.str) -> "JsonPattern":
        '''A JSON log pattern that matches if the field does not exist.

        :param json_field: Field inside JSON. Example: "$.myField"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a427ab962f9380edd6b2daba1e9e16fd501b0ca1f3320845f15de7bf5116d41a)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "notExists", [json_field]))

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(
        cls,
        json_field: builtins.str,
        comparison: builtins.str,
        value: jsii.Number,
    ) -> "JsonPattern":
        '''A JSON log pattern that compares numerical values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the value in the indicated way.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. One of =, !=, <, <=, >, >=.
        :param value: The numerical value to compare to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee269639b68b9cc22a951fc6acab5ec8b50d0e46b388d6e7663c07aaf7e6ab3)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "numberValue", [json_field, comparison, value]))

    @jsii.member(jsii_name="spaceDelimited")
    @builtins.classmethod
    def space_delimited(cls, *columns: builtins.str) -> "SpaceDelimitedTextPattern":
        '''A space delimited log pattern matcher.

        The log event is divided into space-delimited columns (optionally
        enclosed by "" or [] to capture spaces into column values), and names
        are given to each column.

        '...' may be specified once to match any number of columns.

        Afterwards, conditions may be added to individual columns.

        :param columns: The columns in the space-delimited log stream.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce5c99a456f30a5a654f29bc555596cf9e6465e0cf8a647387c99cf3b3c91d2)
            check_type(argname="argument columns", value=columns, expected_type=typing.Tuple[type_hints["columns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("SpaceDelimitedTextPattern", jsii.sinvoke(cls, "spaceDelimited", [*columns]))

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(
        cls,
        json_field: builtins.str,
        comparison: builtins.str,
        value: builtins.str,
    ) -> "JsonPattern":
        '''A JSON log pattern that compares string values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the string value.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. Either = or !=.
        :param value: The string value to compare to. May use '*' as wildcard at start or end of string.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1638c94c8ae801da61e7fe1b4c36f10c4da6f8f2aefc6ee054a88e581d32a660)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "stringValue", [json_field, comparison, value]))


@jsii.interface(jsii_type="@aws-cdk/aws-logs.IFilterPattern")
class IFilterPattern(typing_extensions.Protocol):
    '''Interface for objects that can render themselves to log patterns.'''

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        ...


class _IFilterPatternProxy:
    '''Interface for objects that can render themselves to log patterns.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-logs.IFilterPattern"

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilterPattern).__jsii_proxy_class__ = lambda : _IFilterPatternProxy


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogGroup")
class ILogGroup(
    _aws_cdk_aws_iam_940a1ce0.IResourceWithPolicy,
    typing_extensions.Protocol,
):
    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''The ARN of this log group, with ':*' appended.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The name of this log group.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        '''
        ...

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        '''
        ...

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: "ILogSubscriptionDestination",
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        '''
        ...

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Give permissions to write to create and write to streams in this log group.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="logGroupPhysicalName")
    def log_group_physical_name(self) -> builtins.str:
        '''Public method to get the physical name of this log group.'''
        ...


class _ILogGroupProxy(
    jsii.proxy_for(_aws_cdk_aws_iam_940a1ce0.IResourceWithPolicy), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-logs.ILogGroup"

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''The ARN of this log group, with ':*' appended.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The name of this log group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8435b9fe0f1f1ac0fcfe37217a44e20adead9bfb2f53aebc9d126da72053a62)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MetricFilterOptions(
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        return typing.cast("MetricFilter", jsii.invoke(self, "addMetricFilter", [id, props]))

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac8be277097df09a82ca02fcf5d64644e033bb0017d8ce9a4bece0cb1be3d17)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StreamOptions(log_stream_name=log_stream_name)

        return typing.cast("LogStream", jsii.invoke(self, "addStream", [id, props]))

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: "ILogSubscriptionDestination",
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366b6c1cea54699757edbbcfe8d537f612d9c84640b0afdc93115057048094d7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubscriptionFilterOptions(
            destination=destination, filter_pattern=filter_pattern
        )

        return typing.cast("SubscriptionFilter", jsii.invoke(self, "addSubscriptionFilter", [id, props]))

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90bb8ac1398b13f4c289ac239724b9648ed9433f046f4aad17b0d054d08e07e)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a720a3a946089a37be837ee306534f82ed11332e331740778c33506dfbd2f28)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Give permissions to write to create and write to streams in this log group.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95562428cbfc033e17460b3cd1f06e64be81f1ea118c19d4dc7252e54e6f588f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="logGroupPhysicalName")
    def log_group_physical_name(self) -> builtins.str:
        '''Public method to get the physical name of this log group.'''
        return typing.cast(builtins.str, jsii.invoke(self, "logGroupPhysicalName", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogGroup).__jsii_proxy_class__ = lambda : _ILogGroupProxy


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogStream")
class ILogStream(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''The name of this log stream.

        :attribute: true
        '''
        ...


class _ILogStreamProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-logs.ILogStream"

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''The name of this log stream.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogStream).__jsii_proxy_class__ = lambda : _ILogStreamProxy


@jsii.interface(jsii_type="@aws-cdk/aws-logs.ILogSubscriptionDestination")
class ILogSubscriptionDestination(typing_extensions.Protocol):
    '''Interface for classes that can be the destination of a log Subscription.'''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        source_log_group: ILogGroup,
    ) -> "LogSubscriptionDestinationConfig":
        '''Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -
        '''
        ...


class _ILogSubscriptionDestinationProxy:
    '''Interface for classes that can be the destination of a log Subscription.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-logs.ILogSubscriptionDestination"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        source_log_group: ILogGroup,
    ) -> "LogSubscriptionDestinationConfig":
        '''Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf01a387df4b02adeb6bb4dceae63a13cf4ec522dd08101d158e4330938ed1c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument source_log_group", value=source_log_group, expected_type=type_hints["source_log_group"])
        return typing.cast("LogSubscriptionDestinationConfig", jsii.invoke(self, "bind", [scope, source_log_group]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogSubscriptionDestination).__jsii_proxy_class__ = lambda : _ILogSubscriptionDestinationProxy


@jsii.implements(IFilterPattern)
class JsonPattern(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-logs.JsonPattern",
):
    '''Base class for patterns that only match JSON log events.

    :exampleMetadata: infused

    Example::

        # Search for all events where the component field is equal to
        # "HttpServer" and either error is true or the latency is higher
        # than 1000.
        pattern = logs.FilterPattern.all(
            logs.FilterPattern.string_value("$.component", "=", "HttpServer"),
            logs.FilterPattern.any(
                logs.FilterPattern.boolean_value("$.error", True),
                logs.FilterPattern.number_value("$.latency", ">", 1000)))
    '''

    def __init__(self, json_pattern_string: builtins.str) -> None:
        '''
        :param json_pattern_string: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b2b80876993186fa4e0b5716444dd1f7fff8354a805f35f012bb9ee8bdc506)
            check_type(argname="argument json_pattern_string", value=json_pattern_string, expected_type=type_hints["json_pattern_string"])
        jsii.create(self.__class__, self, [json_pattern_string])

    @builtins.property
    @jsii.member(jsii_name="jsonPatternString")
    def json_pattern_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonPatternString"))

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))


class _JsonPatternProxy(JsonPattern):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, JsonPattern).__jsii_proxy_class__ = lambda : _JsonPatternProxy


@jsii.implements(ILogGroup)
class LogGroup(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.LogGroup",
):
    '''Define a CloudWatch Log Group.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_logs as logs
        
        
        log_group = logs.LogGroup(self, "Log Group")
        log_bucket = s3.Bucket(self, "S3 Bucket")
        
        tasks.EmrContainersStartJobRun(self, "EMR Containers Start Job Run",
            virtual_cluster=tasks.VirtualClusterInput.from_virtual_cluster_id("de92jdei2910fwedz"),
            release_label=tasks.ReleaseLabel.EMR_6_2_0,
            job_driver=tasks.JobDriver(
                spark_submit_job_driver=tasks.SparkSubmitJobDriver(
                    entry_point=sfn.TaskInput.from_text("local:///usr/lib/spark/examples/src/main/python/pi.py"),
                    spark_submit_parameters="--conf spark.executor.instances=2 --conf spark.executor.memory=2G --conf spark.executor.cores=2 --conf spark.driver.cores=1"
                )
            ),
            monitoring=tasks.Monitoring(
                log_group=log_group,
                log_bucket=log_bucket
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        retention: typing.Optional["RetentionDays"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption_key: The KMS Key to encrypt the log group with. Default: - log group is encrypted with the default master key
        :param log_group_name: Name of the log group. Default: Automatically generated
        :param removal_policy: Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97af22380b83ee70ccc756af305ffc4d4ee5dbfee3f6d8e147e17f43438bf02c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LogGroupProps(
            encryption_key=encryption_key,
            log_group_name=log_group_name,
            removal_policy=removal_policy,
            retention=retention,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogGroupArn")
    @builtins.classmethod
    def from_log_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        log_group_arn: builtins.str,
    ) -> ILogGroup:
        '''Import an existing LogGroup given its ARN.

        :param scope: -
        :param id: -
        :param log_group_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c054557df5fd12946464a179c6ed437034385a3f022b8b08552499ae7437c34a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
        return typing.cast(ILogGroup, jsii.sinvoke(cls, "fromLogGroupArn", [scope, id, log_group_arn]))

    @jsii.member(jsii_name="fromLogGroupName")
    @builtins.classmethod
    def from_log_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        log_group_name: builtins.str,
    ) -> ILogGroup:
        '''Import an existing LogGroup given its name.

        :param scope: -
        :param id: -
        :param log_group_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ceea9f4f40ea5cacdc8fb256a76b0dd16b09d83a0bfe92c6adf89cbd2195a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
        return typing.cast(ILogGroup, jsii.sinvoke(cls, "fromLogGroupName", [scope, id, log_group_name]))

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bcc8f9a761fb7023b15b7c4f4401fac3fe5beb70b5fdd2d247698537f8bc93)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MetricFilterOptions(
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        return typing.cast("MetricFilter", jsii.invoke(self, "addMetricFilter", [id, props]))

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bf16eaac8c46d366ebfa3fa642aa1ef4c5b8a13264b933f195d6ca975a0b89)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StreamOptions(log_stream_name=log_stream_name)

        return typing.cast("LogStream", jsii.invoke(self, "addStream", [id, props]))

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502819747cf4c96af2b5cc72205e7b13c78e2722d4f6c407ebbbc1d11d778ac0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubscriptionFilterOptions(
            destination=destination, filter_pattern=filter_pattern
        )

        return typing.cast("SubscriptionFilter", jsii.invoke(self, "addSubscriptionFilter", [id, props]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    ) -> _aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult:
        '''Adds a statement to the resource policy associated with this log group.

        A resource policy will be automatically created upon the first call to ``addToResourcePolicy``.

        Any ARN Principals inside of the statement will be converted into AWS Account ID strings
        because CloudWatch Logs Resource Policies do not accept ARN principals.

        :param statement: The policy statement to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4461ad8c4a0aa1a0cd854772affcab1b8d69663f518c3ad99c4d36e9c8d540da)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fcb78cebb01aa944b636845f0bbe65e20c1b5defb8f3ad2ee893ed1a7264346)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a584073841f54ee9844bd0752df8fa849b7c8fc548fb987b0304be0f53a08182)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Give permissions to create and write to streams in this log group.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2df0bbdada3a5fa7c7156b53be858b8a55bdd4312d8a8585fca1d9876be69b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @jsii.member(jsii_name="logGroupPhysicalName")
    def log_group_physical_name(self) -> builtins.str:
        '''Public method to get the physical name of this log group.

        :return: Physical name of log group
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "logGroupPhysicalName", []))

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''The ARN of this log group.'''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''The name of this log group.'''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.LogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "log_group_name": "logGroupName",
        "removal_policy": "removalPolicy",
        "retention": "retention",
    },
)
class LogGroupProps:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        retention: typing.Optional["RetentionDays"] = None,
    ) -> None:
        '''Properties for a LogGroup.

        :param encryption_key: The KMS Key to encrypt the log group with. Default: - log group is encrypted with the default master key
        :param log_group_name: Name of the log group. Default: Automatically generated
        :param removal_policy: Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS

        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            kms_key = kms.Key(self, "KmsKey")
            
            # Pass the KMS key in the `encryptionKey` field to associate the key to the log group
            log_group = logs.LogGroup(self, "LogGroup",
                encryption_key=kms_key
            )
            
            # Pass the KMS key in the `encryptionKey` field to associate the key to the S3 bucket
            exec_bucket = s3.Bucket(self, "EcsExecBucket",
                encryption_key=kms_key
            )
            
            cluster = ecs.Cluster(self, "Cluster",
                vpc=vpc,
                execute_command_configuration=ecs.ExecuteCommandConfiguration(
                    kms_key=kms_key,
                    log_configuration=ecs.ExecuteCommandLogConfiguration(
                        cloud_watch_log_group=log_group,
                        cloud_watch_encryption_enabled=True,
                        s3_bucket=exec_bucket,
                        s3_encryption_enabled=True,
                        s3_key_prefix="exec-command-output"
                    ),
                    logging=ecs.ExecuteCommandLogging.OVERRIDE
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f17a19a7adf93289664d5773de5ba2d638eb61a2eab0a94641eb009280dcf2)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''The KMS Key to encrypt the log group with.

        :default: - log group is encrypted with the default master key
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Name of the log group.

        :default: Automatically generated
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy]:
        '''Determine the removal policy of this log group.

        Normally you want to retain the log group so you can diagnose issues
        from logs even after a deployment that no longer includes the log group.
        In that case, use the normal date-based retention policy to age out your
        logs.

        :default: RemovalPolicy.Retain
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy], result)

    @builtins.property
    def retention(self) -> typing.Optional["RetentionDays"]:
        '''How long, in days, the log contents will be retained.

        To retain all logs, set this value to RetentionDays.INFINITE.

        :default: RetentionDays.TWO_YEARS
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional["RetentionDays"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogRetention(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.LogRetention",
):
    '''Creates a custom resource to control the retention policy of a CloudWatch Logs log group.

    The log group is created if it doesn't already exist. The policy
    is removed when ``retentionDays`` is ``undefined`` or equal to ``Infinity``.
    Log group can be created in the region that is different from stack region by
    specifying ``logGroupRegion``

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_logs as logs
        import aws_cdk.core as cdk
        
        # role: iam.Role
        
        log_retention = logs.LogRetention(self, "MyLogRetention",
            log_group_name="logGroupName",
            retention=logs.RetentionDays.ONE_DAY,
        
            # the properties below are optional
            log_group_region="logGroupRegion",
            log_retention_retry_options=logs.LogRetentionRetryOptions(
                base=cdk.Duration.minutes(30),
                max_retries=123
            ),
            role=role
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        retention: "RetentionDays",
        log_group_region: typing.Optional[builtins.str] = None,
        log_retention_retry_options: typing.Optional[typing.Union["LogRetentionRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group_name: The log group name.
        :param retention: The number of days log events are kept in CloudWatch Logs.
        :param log_group_region: The region where the log group should be created. Default: - same region as the stack
        :param log_retention_retry_options: Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12c43cc31930bc56a14fd1accdbba11fc5c1c0aee2e9590b73976d950aab79e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LogRetentionProps(
            log_group_name=log_group_name,
            retention=retention,
            log_group_region=log_group_region,
            log_retention_retry_options=log_retention_retry_options,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''The ARN of the LogGroup.'''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.LogRetentionProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "retention": "retention",
        "log_group_region": "logGroupRegion",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "role": "role",
    },
)
class LogRetentionProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        retention: "RetentionDays",
        log_group_region: typing.Optional[builtins.str] = None,
        log_retention_retry_options: typing.Optional[typing.Union["LogRetentionRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Construction properties for a LogRetention.

        :param log_group_name: The log group name.
        :param retention: The number of days log events are kept in CloudWatch Logs.
        :param log_group_region: The region where the log group should be created. Default: - same region as the stack
        :param log_retention_retry_options: Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_logs as logs
            import aws_cdk.core as cdk
            
            # role: iam.Role
            
            log_retention_props = logs.LogRetentionProps(
                log_group_name="logGroupName",
                retention=logs.RetentionDays.ONE_DAY,
            
                # the properties below are optional
                log_group_region="logGroupRegion",
                log_retention_retry_options=logs.LogRetentionRetryOptions(
                    base=cdk.Duration.minutes(30),
                    max_retries=123
                ),
                role=role
            )
        '''
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = LogRetentionRetryOptions(**log_retention_retry_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895f130bee902a5a83a0aa11a3247dc80a37168b7adc395abb574e78ad015520)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument log_group_region", value=log_group_region, expected_type=type_hints["log_group_region"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
            "retention": retention,
        }
        if log_group_region is not None:
            self._values["log_group_region"] = log_group_region
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''The log group name.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention(self) -> "RetentionDays":
        '''The number of days log events are kept in CloudWatch Logs.'''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast("RetentionDays", result)

    @builtins.property
    def log_group_region(self) -> typing.Optional[builtins.str]:
        '''The region where the log group should be created.

        :default: - same region as the stack
        '''
        result = self._values.get("log_group_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional["LogRetentionRetryOptions"]:
        '''Retry options for all AWS API calls.

        :default: - AWS SDK default retry options
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional["LogRetentionRetryOptions"], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The IAM role for the Lambda function associated with the custom resource.

        :default: - A new role is created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogRetentionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.LogRetentionRetryOptions",
    jsii_struct_bases=[],
    name_mapping={"base": "base", "max_retries": "maxRetries"},
)
class LogRetentionRetryOptions:
    def __init__(
        self,
        *,
        base: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Retry options for all AWS API calls.

        :param base: The base duration to use in the exponential backoff for operation retries. Default: Duration.millis(100) (AWS SDK default)
        :param max_retries: The maximum amount of retries. Default: 3 (AWS SDK default)

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            import aws_cdk.core as cdk
            
            log_retention_retry_options = logs.LogRetentionRetryOptions(
                base=cdk.Duration.minutes(30),
                max_retries=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7146aa77b5ffc90a996736a3e19c5283a2bb7659a61be3303f97d1dd0d144fa)
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base is not None:
            self._values["base"] = base
        if max_retries is not None:
            self._values["max_retries"] = max_retries

    @builtins.property
    def base(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The base duration to use in the exponential backoff for operation retries.

        :default: Duration.millis(100) (AWS SDK default)
        '''
        result = self._values.get("base")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of retries.

        :default: 3 (AWS SDK default)
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogRetentionRetryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILogStream)
class LogStream(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.LogStream",
):
    '''Define a Log Stream in a Log Group.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_logs as logs
        import aws_cdk.core as cdk
        
        # log_group: logs.LogGroup
        
        log_stream = logs.LogStream(self, "MyLogStream",
            log_group=log_group,
        
            # the properties below are optional
            log_stream_name="logStreamName",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        log_stream_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: The log group to create a log stream for.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cac097b81bc4ebe7289e7282eb5cde1a15112953834aa2898a0fd264c08ca91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LogStreamProps(
            log_group=log_group,
            log_stream_name=log_stream_name,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogStreamName")
    @builtins.classmethod
    def from_log_stream_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        log_stream_name: builtins.str,
    ) -> ILogStream:
        '''Import an existing LogGroup.

        :param scope: -
        :param id: -
        :param log_stream_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1a6a46966768baa13021e795ceb7d866809bf525dc16a6ac78772e9fdf30cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        return typing.cast(ILogStream, jsii.sinvoke(cls, "fromLogStreamName", [scope, id, log_stream_name]))

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''The name of this log stream.'''
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.LogStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group": "logGroup",
        "log_stream_name": "logStreamName",
        "removal_policy": "removalPolicy",
    },
)
class LogStreamProps:
    def __init__(
        self,
        *,
        log_group: ILogGroup,
        log_stream_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    ) -> None:
        '''Properties for a LogStream.

        :param log_group: The log group to create a log stream for.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            import aws_cdk.core as cdk
            
            # log_group: logs.LogGroup
            
            log_stream_props = logs.LogStreamProps(
                log_group=log_group,
            
                # the properties below are optional
                log_stream_name="logStreamName",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eda758fb7d6923508bfc7c8238cc1f17d48bb5456bd3a554e7238f9c2ab0183)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group": log_group,
        }
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''The log group to create a log stream for.'''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream to create.

        The name must be unique within the log group.

        :default: Automatically generated
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy]:
        '''Determine what happens when the log stream resource is removed from the app.

        Normally you want to retain the log stream so you can diagnose issues from
        logs even after a deployment that no longer includes the log stream.

        The date-based retention policy of your log group will age out the logs
        after a certain time.

        :default: RemovalPolicy.Retain
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.LogSubscriptionDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "role": "role"},
)
class LogSubscriptionDestinationConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Properties returned by a Subscription destination.

        :param arn: The ARN of the subscription's destination.
        :param role: The role to assume to write log events to the destination. Default: No role assumed

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_logs as logs
            
            # role: iam.Role
            
            log_subscription_destination_config = logs.LogSubscriptionDestinationConfig(
                arn="arn",
            
                # the properties below are optional
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd4700cd41a081d074e36cebb5356119bfaac9f28e05f5c288327496fc7ce5c)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def arn(self) -> builtins.str:
        '''The ARN of the subscription's destination.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The role to assume to write log events to the destination.

        :default: No role assumed
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogSubscriptionDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetricFilter(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.MetricFilter",
):
    '''A filter that extracts information from CloudWatch Logs and emits to CloudWatch Metrics.

    :exampleMetadata: lit=test/integ.metricfilter.lit.ts infused

    Example::

        MetricFilter(self, "MetricFilter",
            log_group=log_group,
            metric_namespace="MyApp",
            metric_name="Latency",
            filter_pattern=FilterPattern.exists("$.latency"),
            metric_value="$.latency"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: The log group to create the filter on.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ffcbe12c1372344b1de53c9940be36b599c7e712b70c69cb672af0bb66d4ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MetricFilterProps(
            log_group=log_group,
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for this Metric Filter.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: avg over 5 minutes
        '''
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metric", [props]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.MetricFilterOptions",
    jsii_struct_bases=[],
    name_mapping={
        "filter_pattern": "filterPattern",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "default_value": "defaultValue",
        "metric_value": "metricValue",
    },
)
class MetricFilterOptions:
    def __init__(
        self,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a MetricFilter created from a LogGroup.

        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            # filter_pattern: logs.IFilterPattern
            
            metric_filter_options = logs.MetricFilterOptions(
                filter_pattern=filter_pattern,
                metric_name="metricName",
                metric_namespace="metricNamespace",
            
                # the properties below are optional
                default_value=123,
                metric_value="metricValue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374b48d054c7b998f12d5e806c683276c4e4be86cb8ff5573954938cf6092623)
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if metric_value is not None:
            self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''Pattern to search for log events.'''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The name of the metric to emit.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''The namespace of the metric to emit.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        '''The value to emit if the pattern does not match a particular event.

        :default: No metric emitted.
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_value(self) -> typing.Optional[builtins.str]:
        '''The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        :default: "1"
        '''
        result = self._values.get("metric_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.MetricFilterProps",
    jsii_struct_bases=[MetricFilterOptions],
    name_mapping={
        "filter_pattern": "filterPattern",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "default_value": "defaultValue",
        "metric_value": "metricValue",
        "log_group": "logGroup",
    },
)
class MetricFilterProps(MetricFilterOptions):
    def __init__(
        self,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
        log_group: ILogGroup,
    ) -> None:
        '''Properties for a MetricFilter.

        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        :param log_group: The log group to create the filter on.

        :exampleMetadata: lit=test/integ.metricfilter.lit.ts infused

        Example::

            MetricFilter(self, "MetricFilter",
                log_group=log_group,
                metric_namespace="MyApp",
                metric_name="Latency",
                filter_pattern=FilterPattern.exists("$.latency"),
                metric_value="$.latency"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100e83a70454e3dd4df2fc2c5e3636e60f11f80632c4e8f0e6a387f73fb2d462)
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "log_group": log_group,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if metric_value is not None:
            self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''Pattern to search for log events.'''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The name of the metric to emit.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''The namespace of the metric to emit.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        '''The value to emit if the pattern does not match a particular event.

        :default: No metric emitted.
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_value(self) -> typing.Optional[builtins.str]:
        '''The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        :default: "1"
        '''
        result = self._values.get("metric_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''The log group to create the filter on.'''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueryDefinition(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.QueryDefinition",
):
    '''Define a query definition for CloudWatch Logs Insights.

    :exampleMetadata: infused

    Example::

        logs.QueryDefinition(self, "QueryDefinition",
            query_definition_name="MyQuery",
            query_string=logs.QueryString(
                fields=["@timestamp", "@message"],
                sort="@timestamp desc",
                limit=20
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        query_definition_name: builtins.str,
        query_string: "QueryString",
        log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param query_definition_name: Name of the query definition.
        :param query_string: The query string to use for this query definition.
        :param log_groups: Specify certain log groups for the query definition. Default: - no specified log groups
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead5a62400fc0bd858eb01659d108b2bffb5c46f956999caee1a4baf846de3fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueryDefinitionProps(
            query_definition_name=query_definition_name,
            query_string=query_string,
            log_groups=log_groups,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="queryDefinitionId")
    def query_definition_id(self) -> builtins.str:
        '''The ID of the query definition.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryDefinitionId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.QueryDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "query_definition_name": "queryDefinitionName",
        "query_string": "queryString",
        "log_groups": "logGroups",
    },
)
class QueryDefinitionProps:
    def __init__(
        self,
        *,
        query_definition_name: builtins.str,
        query_string: "QueryString",
        log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
    ) -> None:
        '''Properties for a QueryDefinition.

        :param query_definition_name: Name of the query definition.
        :param query_string: The query string to use for this query definition.
        :param log_groups: Specify certain log groups for the query definition. Default: - no specified log groups

        :exampleMetadata: infused

        Example::

            logs.QueryDefinition(self, "QueryDefinition",
                query_definition_name="MyQuery",
                query_string=logs.QueryString(
                    fields=["@timestamp", "@message"],
                    sort="@timestamp desc",
                    limit=20
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0310ec427ca69013660b21077c10a544dd720378ae9ea02af209ef3aa780037a)
            check_type(argname="argument query_definition_name", value=query_definition_name, expected_type=type_hints["query_definition_name"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument log_groups", value=log_groups, expected_type=type_hints["log_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query_definition_name": query_definition_name,
            "query_string": query_string,
        }
        if log_groups is not None:
            self._values["log_groups"] = log_groups

    @builtins.property
    def query_definition_name(self) -> builtins.str:
        '''Name of the query definition.'''
        result = self._values.get("query_definition_name")
        assert result is not None, "Required property 'query_definition_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_string(self) -> "QueryString":
        '''The query string to use for this query definition.'''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast("QueryString", result)

    @builtins.property
    def log_groups(self) -> typing.Optional[typing.List[ILogGroup]]:
        '''Specify certain log groups for the query definition.

        :default: - no specified log groups
        '''
        result = self._values.get("log_groups")
        return typing.cast(typing.Optional[typing.List[ILogGroup]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueryString(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-logs.QueryString"):
    '''Define a QueryString.

    :exampleMetadata: infused

    Example::

        logs.QueryDefinition(self, "QueryDefinition",
            query_definition_name="MyQuery",
            query_string=logs.QueryString(
                fields=["@timestamp", "@message"],
                sort="@timestamp desc",
                limit=20
            )
        )
    '''

    def __init__(
        self,
        *,
        display: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        filter: typing.Optional[builtins.str] = None,
        limit: typing.Optional[jsii.Number] = None,
        parse: typing.Optional[builtins.str] = None,
        sort: typing.Optional[builtins.str] = None,
        stats: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display: Specifies which fields to display in the query results. Default: - no display in QueryString
        :param fields: Retrieves the specified fields from log events for display. Default: - no fields in QueryString
        :param filter: Filters the results of a query that's based on one or more conditions. Default: - no filter in QueryString
        :param limit: Specifies the number of log events returned by the query. Default: - no limit in QueryString
        :param parse: Extracts data from a log field and creates one or more ephemeral fields that you can process further in the query. Default: - no parse in QueryString
        :param sort: Sorts the retrieved log events. Default: - no sort in QueryString
        :param stats: Uses log field values to calculate aggregate statistics. Default: - no stats in QueryString
        '''
        props = QueryStringProps(
            display=display,
            fields=fields,
            filter=filter,
            limit=limit,
            parse=parse,
            sort=sort,
            stats=stats,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''String representation of this QueryString.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.QueryStringProps",
    jsii_struct_bases=[],
    name_mapping={
        "display": "display",
        "fields": "fields",
        "filter": "filter",
        "limit": "limit",
        "parse": "parse",
        "sort": "sort",
        "stats": "stats",
    },
)
class QueryStringProps:
    def __init__(
        self,
        *,
        display: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        filter: typing.Optional[builtins.str] = None,
        limit: typing.Optional[jsii.Number] = None,
        parse: typing.Optional[builtins.str] = None,
        sort: typing.Optional[builtins.str] = None,
        stats: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a QueryString.

        :param display: Specifies which fields to display in the query results. Default: - no display in QueryString
        :param fields: Retrieves the specified fields from log events for display. Default: - no fields in QueryString
        :param filter: Filters the results of a query that's based on one or more conditions. Default: - no filter in QueryString
        :param limit: Specifies the number of log events returned by the query. Default: - no limit in QueryString
        :param parse: Extracts data from a log field and creates one or more ephemeral fields that you can process further in the query. Default: - no parse in QueryString
        :param sort: Sorts the retrieved log events. Default: - no sort in QueryString
        :param stats: Uses log field values to calculate aggregate statistics. Default: - no stats in QueryString

        :exampleMetadata: infused

        Example::

            logs.QueryDefinition(self, "QueryDefinition",
                query_definition_name="MyQuery",
                query_string=logs.QueryString(
                    fields=["@timestamp", "@message"],
                    sort="@timestamp desc",
                    limit=20
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ef890250a4eee691a58ce3e6a01f3d2b7af3afcc0f1a29af167952a1046d49)
            check_type(argname="argument display", value=display, expected_type=type_hints["display"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument parse", value=parse, expected_type=type_hints["parse"])
            check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            check_type(argname="argument stats", value=stats, expected_type=type_hints["stats"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display is not None:
            self._values["display"] = display
        if fields is not None:
            self._values["fields"] = fields
        if filter is not None:
            self._values["filter"] = filter
        if limit is not None:
            self._values["limit"] = limit
        if parse is not None:
            self._values["parse"] = parse
        if sort is not None:
            self._values["sort"] = sort
        if stats is not None:
            self._values["stats"] = stats

    @builtins.property
    def display(self) -> typing.Optional[builtins.str]:
        '''Specifies which fields to display in the query results.

        :default: - no display in QueryString
        '''
        result = self._values.get("display")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Retrieves the specified fields from log events for display.

        :default: - no fields in QueryString
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''Filters the results of a query that's based on one or more conditions.

        :default: - no filter in QueryString
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of log events returned by the query.

        :default: - no limit in QueryString
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parse(self) -> typing.Optional[builtins.str]:
        '''Extracts data from a log field and creates one or more ephemeral fields that you can process further in the query.

        :default: - no parse in QueryString
        '''
        result = self._values.get("parse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort(self) -> typing.Optional[builtins.str]:
        '''Sorts the retrieved log events.

        :default: - no sort in QueryString
        '''
        result = self._values.get("sort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stats(self) -> typing.Optional[builtins.str]:
        '''Uses log field values to calculate aggregate statistics.

        :default: - no stats in QueryString
        '''
        result = self._values.get("stats")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryStringProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResourcePolicy(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.ResourcePolicy",
):
    '''Resource Policy for CloudWatch Log Groups.

    Policies define the operations that are allowed on this resource.

    You almost never need to define this construct directly.

    All AWS resources that support resource policies have a method called
    ``addToResourcePolicy()``, which will automatically create a new resource
    policy if one doesn't exist yet, otherwise it will add to the existing
    policy.

    Prefer to use ``addToResourcePolicy()`` instead.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_logs as logs
        
        # policy_statement: iam.PolicyStatement
        
        resource_policy = logs.ResourcePolicy(self, "MyResourcePolicy",
            policy_statements=[policy_statement],
            resource_policy_name="resourcePolicyName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
        resource_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param policy_statements: Initial statements to add to the resource policy. Default: - No statements
        :param resource_policy_name: Name of the log group resource policy. Default: - Uses a unique id based on the construct path
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ea75fa2dc73dbbda850da1f874f118d229860e7cfdd44f85179266dd54e479)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ResourcePolicyProps(
            policy_statements=policy_statements,
            resource_policy_name=resource_policy_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> _aws_cdk_aws_iam_940a1ce0.PolicyDocument:
        '''The IAM policy document for this resource policy.'''
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.PolicyDocument, jsii.get(self, "document"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.ResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_statements": "policyStatements",
        "resource_policy_name": "resourcePolicyName",
    },
)
class ResourcePolicyProps:
    def __init__(
        self,
        *,
        policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
        resource_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties to define Cloudwatch log group resource policy.

        :param policy_statements: Initial statements to add to the resource policy. Default: - No statements
        :param resource_policy_name: Name of the log group resource policy. Default: - Uses a unique id based on the construct path

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_logs as logs
            
            # policy_statement: iam.PolicyStatement
            
            resource_policy_props = logs.ResourcePolicyProps(
                policy_statements=[policy_statement],
                resource_policy_name="resourcePolicyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896557f17758d0c8f3b0e6bfab34975d6516647e512b7e34d766d8820f7ff946)
            check_type(argname="argument policy_statements", value=policy_statements, expected_type=type_hints["policy_statements"])
            check_type(argname="argument resource_policy_name", value=resource_policy_name, expected_type=type_hints["resource_policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_statements is not None:
            self._values["policy_statements"] = policy_statements
        if resource_policy_name is not None:
            self._values["resource_policy_name"] = resource_policy_name

    @builtins.property
    def policy_statements(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]]:
        '''Initial statements to add to the resource policy.

        :default: - No statements
        '''
        result = self._values.get("policy_statements")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]], result)

    @builtins.property
    def resource_policy_name(self) -> typing.Optional[builtins.str]:
        '''Name of the log group resource policy.

        :default: - Uses a unique id based on the construct path
        '''
        result = self._values.get("resource_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-logs.RetentionDays")
class RetentionDays(enum.Enum):
    '''How long, in days, the log contents will be retained.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_logs as logs
        # my_logs_publishing_role: iam.Role
        # vpc: ec2.Vpc
        
        
        # Exporting logs from a cluster
        cluster = rds.DatabaseCluster(self, "Database",
            engine=rds.DatabaseClusterEngine.aurora(
                version=rds.AuroraEngineVersion.VER_1_17_9
            ),
            instance_props=rds.InstanceProps(
                vpc=vpc
            ),
            cloudwatch_logs_exports=["error", "general", "slowquery", "audit"],  # Export all available MySQL-based logs
            cloudwatch_logs_retention=logs.RetentionDays.THREE_MONTHS,  # Optional - default is to never expire logs
            cloudwatch_logs_retention_role=my_logs_publishing_role
        )
        
        # Exporting logs from an instance
        instance = rds.DatabaseInstance(self, "Instance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_3
            ),
            vpc=vpc,
            cloudwatch_logs_exports=["postgresql"]
        )
    '''

    ONE_DAY = "ONE_DAY"
    '''1 day.'''
    THREE_DAYS = "THREE_DAYS"
    '''3 days.'''
    FIVE_DAYS = "FIVE_DAYS"
    '''5 days.'''
    ONE_WEEK = "ONE_WEEK"
    '''1 week.'''
    TWO_WEEKS = "TWO_WEEKS"
    '''2 weeks.'''
    ONE_MONTH = "ONE_MONTH"
    '''1 month.'''
    TWO_MONTHS = "TWO_MONTHS"
    '''2 months.'''
    THREE_MONTHS = "THREE_MONTHS"
    '''3 months.'''
    FOUR_MONTHS = "FOUR_MONTHS"
    '''4 months.'''
    FIVE_MONTHS = "FIVE_MONTHS"
    '''5 months.'''
    SIX_MONTHS = "SIX_MONTHS"
    '''6 months.'''
    ONE_YEAR = "ONE_YEAR"
    '''1 year.'''
    THIRTEEN_MONTHS = "THIRTEEN_MONTHS"
    '''13 months.'''
    EIGHTEEN_MONTHS = "EIGHTEEN_MONTHS"
    '''18 months.'''
    TWO_YEARS = "TWO_YEARS"
    '''2 years.'''
    FIVE_YEARS = "FIVE_YEARS"
    '''5 years.'''
    SIX_YEARS = "SIX_YEARS"
    '''6 years.'''
    SEVEN_YEARS = "SEVEN_YEARS"
    '''7 years.'''
    EIGHT_YEARS = "EIGHT_YEARS"
    '''8 years.'''
    NINE_YEARS = "NINE_YEARS"
    '''9 years.'''
    TEN_YEARS = "TEN_YEARS"
    '''10 years.'''
    INFINITE = "INFINITE"
    '''Retain logs forever.'''


@jsii.implements(IFilterPattern)
class SpaceDelimitedTextPattern(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.SpaceDelimitedTextPattern",
):
    '''Space delimited text pattern.

    :exampleMetadata: infused

    Example::

        # Search for all events where the component is "HttpServer" and the
        # result code is not equal to 200.
        pattern = logs.FilterPattern.space_delimited("time", "component", "...", "result_code", "latency").where_string("component", "=", "HttpServer").where_number("result_code", "!=", 200)
    '''

    def __init__(
        self,
        columns: typing.Sequence[builtins.str],
        restrictions: typing.Mapping[builtins.str, typing.Sequence[typing.Union[ColumnRestriction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param columns: -
        :param restrictions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea2689a42af06bfeb160543c22e6b8155ccecd6887cf44dc96bf3dae059a92b)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
        jsii.create(self.__class__, self, [columns, restrictions])

    @jsii.member(jsii_name="construct")
    @builtins.classmethod
    def construct(
        cls,
        columns: typing.Sequence[builtins.str],
    ) -> "SpaceDelimitedTextPattern":
        '''Construct a new instance of a space delimited text pattern.

        Since this class must be public, we can't rely on the user only creating it through
        the ``LogPattern.spaceDelimited()`` factory function. We must therefore validate the
        argument in the constructor. Since we're returning a copy on every mutation, and we
        don't want to re-validate the same things on every construction, we provide a limited
        set of mutator functions and only validate the new data every time.

        :param columns: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0dda74911439372e09fe611d28623b38dd5efb17f7fb049e95b41494798346)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        return typing.cast("SpaceDelimitedTextPattern", jsii.sinvoke(cls, "construct", [columns]))

    @jsii.member(jsii_name="whereNumber")
    def where_number(
        self,
        column_name: builtins.str,
        comparison: builtins.str,
        value: jsii.Number,
    ) -> "SpaceDelimitedTextPattern":
        '''Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee12fb948401852d08ad3f47e7ee45bd7a9838b1c693528897fe09a3bad0f5f)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("SpaceDelimitedTextPattern", jsii.invoke(self, "whereNumber", [column_name, comparison, value]))

    @jsii.member(jsii_name="whereString")
    def where_string(
        self,
        column_name: builtins.str,
        comparison: builtins.str,
        value: builtins.str,
    ) -> "SpaceDelimitedTextPattern":
        '''Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f639c01762b8ad938cb20004b605fa5202918f09aeade600a8bb9e1d56179b)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("SpaceDelimitedTextPattern", jsii.invoke(self, "whereString", [column_name, comparison, value]))

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.StreamOptions",
    jsii_struct_bases=[],
    name_mapping={"log_stream_name": "logStreamName"},
)
class StreamOptions:
    def __init__(
        self,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a new LogStream created from a LogGroup.

        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            stream_options = logs.StreamOptions(
                log_stream_name="logStreamName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce2251b01736601b2ac0794f0b3c5e8a287d00fa2c09360a00c34a63220dded)
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream to create.

        The name must be unique within the log group.

        :default: Automatically generated
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubscriptionFilter(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.SubscriptionFilter",
):
    '''A new Subscription on a CloudWatch log group.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_logs_destinations as destinations
        # fn: lambda.Function
        # log_group: logs.LogGroup
        
        
        logs.SubscriptionFilter(self, "Subscription",
            log_group=log_group,
            destination=destinations.LambdaDestination(fn),
            filter_pattern=logs.FilterPattern.all_terms("ERROR", "MainThread")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: The log group to create the subscription on.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f960bf6c055b42696a5f22463e1ea2081644fba906942e629582ca60b0ecfd4f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubscriptionFilterProps(
            log_group=log_group, destination=destination, filter_pattern=filter_pattern
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.SubscriptionFilterOptions",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "filter_pattern": "filterPattern"},
)
class SubscriptionFilterOptions:
    def __init__(
        self,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> None:
        '''Properties for a new SubscriptionFilter created from a LogGroup.

        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs as logs
            
            # filter_pattern: logs.IFilterPattern
            # log_subscription_destination: logs.ILogSubscriptionDestination
            
            subscription_filter_options = logs.SubscriptionFilterOptions(
                destination=log_subscription_destination,
                filter_pattern=filter_pattern
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448184ea673cd0baa41e13a3c7d041ae497e0b8eb3d1e5bc34c4774276c6af24)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "filter_pattern": filter_pattern,
        }

    @builtins.property
    def destination(self) -> ILogSubscriptionDestination:
        '''The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(ILogSubscriptionDestination, result)

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''Log events matching this pattern will be sent to the destination.'''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs.SubscriptionFilterProps",
    jsii_struct_bases=[SubscriptionFilterOptions],
    name_mapping={
        "destination": "destination",
        "filter_pattern": "filterPattern",
        "log_group": "logGroup",
    },
)
class SubscriptionFilterProps(SubscriptionFilterOptions):
    def __init__(
        self,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
        log_group: ILogGroup,
    ) -> None:
        '''Properties for a SubscriptionFilter.

        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        :param log_group: The log group to create the subscription on.

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_logs_destinations as destinations
            # fn: lambda.Function
            # log_group: logs.LogGroup
            
            
            logs.SubscriptionFilter(self, "Subscription",
                log_group=log_group,
                destination=destinations.LambdaDestination(fn),
                filter_pattern=logs.FilterPattern.all_terms("ERROR", "MainThread")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b76c867fb15c148d24d9ef614508a36ff48b549f4b48c4e1a448ece761baf2)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "filter_pattern": filter_pattern,
            "log_group": log_group,
        }

    @builtins.property
    def destination(self) -> ILogSubscriptionDestination:
        '''The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(ILogSubscriptionDestination, result)

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''Log events matching this pattern will be sent to the destination.'''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''The log group to create the subscription on.'''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILogSubscriptionDestination)
class CrossAccountDestination(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs.CrossAccountDestination",
):
    '''A new CloudWatch Logs Destination for use in cross-account scenarios.

    CrossAccountDestinations are used to subscribe a Kinesis stream in a
    different account to a CloudWatch Subscription.

    Consumers will hardly ever need to use this class. Instead, directly
    subscribe a Kinesis stream using the integration class in the
    ``@aws-cdk/aws-logs-destinations`` package; if necessary, a
    ``CrossAccountDestination`` will be created automatically.

    :resource: AWS::Logs::Destination
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_logs as logs
        
        # role: iam.Role
        
        cross_account_destination = logs.CrossAccountDestination(self, "MyCrossAccountDestination",
            role=role,
            target_arn="targetArn",
        
            # the properties below are optional
            destination_name="destinationName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
        target_arn: builtins.str,
        destination_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param role: The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: The log destination target's ARN.
        :param destination_name: The name of the log destination. Default: Automatically generated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ea0d1cf7bd3e9c0919cc0a4c93ed09c3f6608b522aa762a88eac03d03ecb07)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CrossAccountDestinationProps(
            role=role, target_arn=target_arn, destination_name=destination_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    ) -> None:
        '''
        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7e1e4c6ec64eb8aa5d35814d3f0e934f6f336b20f0ad2614bc443ea9c6b09e)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        _source_log_group: ILogGroup,
    ) -> LogSubscriptionDestinationConfig:
        '''Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param _scope: -
        :param _source_log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e837c642a32f333468145caf9a4f933a63a9db522c85c235bc05564d30c85d81)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _source_log_group", value=_source_log_group, expected_type=type_hints["_source_log_group"])
        return typing.cast(LogSubscriptionDestinationConfig, jsii.invoke(self, "bind", [_scope, _source_log_group]))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''The ARN of this CrossAccountDestination object.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @builtins.property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> builtins.str:
        '''The name of this CrossAccountDestination object.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationName"))

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> _aws_cdk_aws_iam_940a1ce0.PolicyDocument:
        '''Policy object of this CrossAccountDestination object.'''
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.PolicyDocument, jsii.get(self, "policyDocument"))


__all__ = [
    "CfnDestination",
    "CfnDestinationProps",
    "CfnLogGroup",
    "CfnLogGroupProps",
    "CfnLogStream",
    "CfnLogStreamProps",
    "CfnMetricFilter",
    "CfnMetricFilterProps",
    "CfnQueryDefinition",
    "CfnQueryDefinitionProps",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnSubscriptionFilter",
    "CfnSubscriptionFilterProps",
    "ColumnRestriction",
    "CrossAccountDestination",
    "CrossAccountDestinationProps",
    "FilterPattern",
    "IFilterPattern",
    "ILogGroup",
    "ILogStream",
    "ILogSubscriptionDestination",
    "JsonPattern",
    "LogGroup",
    "LogGroupProps",
    "LogRetention",
    "LogRetentionProps",
    "LogRetentionRetryOptions",
    "LogStream",
    "LogStreamProps",
    "LogSubscriptionDestinationConfig",
    "MetricFilter",
    "MetricFilterOptions",
    "MetricFilterProps",
    "QueryDefinition",
    "QueryDefinitionProps",
    "QueryString",
    "QueryStringProps",
    "ResourcePolicy",
    "ResourcePolicyProps",
    "RetentionDays",
    "SpaceDelimitedTextPattern",
    "StreamOptions",
    "SubscriptionFilter",
    "SubscriptionFilterOptions",
    "SubscriptionFilterProps",
]

publication.publish()

def _typecheckingstub__11a9ac01bae9592ae8de7203ceca96f34339eaba96a238d69b5c2265bad3cdca(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    destination_name: builtins.str,
    role_arn: builtins.str,
    target_arn: builtins.str,
    destination_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f710cca39e823468f4bc1cb0679c5d9c9c7a96dcb65b3dff2f69a1030925100(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87521f6860b8ca9f00d730cabe8e6e9ee43afbad9d8c0bb16b629a00ff7d00a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61122b82f7f2f9083601326f9b560797424bf0b0520d4a9890eed55fd162dc96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8a01ca68857ebb1bcc73a2c5bdbc87c65e0dc21b9b3147c77eac4fd16ddcd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c515db59a4964ed61af3035341eabae95c893b90584c81c609fb814bc53d51a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303977960cdec77aefab8a68771e09a3ec555e46f4141c5101d8c07f5d5cbe2a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6db4f53601d44fc0add1e6aec21a40509733b70a131fac77c05838c2be3a4e7(
    *,
    destination_name: builtins.str,
    role_arn: builtins.str,
    target_arn: builtins.str,
    destination_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee156e4e87958d63d23eb0e81324114b020fb6ae841e65ead5b929ce9e94456(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    data_protection_policy: typing.Any = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bbbbfcb259196087d0b4bd37cfeb7e3473c89c9f83b25b3228236b81861dae(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33801a7c7bdd2c40e00cf9273b126c42634ea0d0663aefa0992058b06c6d72fb(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f467d550a09cc131afd7d769eae84967fa3ea5091976b7d3153704336c67b5(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6002bc9fff029bdb8a6543d1e8d2416cf1b4f3457ae28759dab09fe1c6898a1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4747c815f30ccde544215b45b1cb1118df79a23115e530d7b468e22fea2b949(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282e930518fea7055ed974105ed2dc7f97c9996d0d3448cf3e60ef9cd37e91cd(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f876f18d174156e05ea500405dd37b38662fad2172d38fe2cedb205140d1d8(
    *,
    data_protection_policy: typing.Any = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0b59ec0df43596ec71b8c73d255febe60b771129a868e7cb92d8d3eb61a372(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    log_group_name: builtins.str,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c68101b277a5b590427f085944025792aa9f4cea807bda8eaa7db50e2a031b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdca3c6b6b25d78535021aa88c44824e59b51d306e8f515581ddb6351b0b26ca(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9c06bd021523c43325d0c68cf83c99e60d9adfcc1c091ac09edb2cec513b0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c42aedcc85092d202042d0e690983cfb00a574f3af9bf8553f6854cdd106fd2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d1b614107f05b70caafde9559c36f8a34033fcad8c1a2b661d25f7db47c9b8(
    *,
    log_group_name: builtins.str,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21a6e52789f5b4c858131cad8b61c0043016f16923a35d9f224682931bd22c0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    metric_transformations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnMetricFilter.MetricTransformationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    filter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc98f66fc4412f7d8f891a121d5512a9cf4c965bc42132e83b68d9d3c0b426b4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1422eb434acf7c7fcce873af70ac496388e48d82ffb832e09a02600e08cd45(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a585c30195f3666ada99fbdf6f84ad426036e1a3db59c256916ec65dd33f95b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb235d54c935f08677ae003d9cca22e4d661a759879adae077a65961f72bc7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9b7d18641ff80112260954bd03087eb03ad0d3495fd1465c80d4198d53e9fd(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnMetricFilter.MetricTransformationProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2308df07571f8c2c8a328b9121673422da964d5b3daf17d425b5583ab7a96bf7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52cbe9cf216e393e5bfdd84a6bfc8de3a133ee543dcdebba72d6e00d4a6fa8f(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021ba37262cc618ad0767fad84d5335ca673e2be61f1aecbe4eaf72ab7ed25f8(
    *,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_value: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnMetricFilter.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cba185bae3d066dcf278c9667765ab05714c9e433cea02dadc4e5fecbd6625c(
    *,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    metric_transformations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnMetricFilter.MetricTransformationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    filter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c504df6b0e06ae31b2c2651181dc1915c131430666f5e6a245aa1e4bc1151dfd(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    query_string: builtins.str,
    log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a4b72b95fa1c84707d2d97d220113a5cf4e842fc49f58406492a300f858f17(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c039b469a1430de832c8216d3d5b354bd22a55ded3a97804b4c6afd61ede40f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fc5385e32244b4624a5281d81312318a3bdaddeb43f4e11bfcd920aa071a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3401dee44e9a163aaedff81f2f8d91b18b79d895f5159ca5ab9e9e09b6cfc00c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff23e93375e01a0902f8c8a760a99862ae96fd945bda66450970473ae54fb05(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e65de67e25034430f10f63be798a617625c8904620173a4b61102c5c1aa95c6(
    *,
    name: builtins.str,
    query_string: builtins.str,
    log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3e2cababb17dd0241f31fdecd32f64af1a7275a2864c3162fbe0dd8196a46e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy_document: builtins.str,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08563cc60984232404b9b0817a2e9f1fa8e4fe4aade8c0e030acedb84563ed29(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981d8a120b09fbeca2b44a5f8d4e65ae3cc35235b57640ad754624cf43948606(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f381d87a4e705503a754a7b1619644291d0f69a16c95886dc3e6756653f52f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69206a0f6c656c7e375579940f365db8322102b5f5b3574e01e76191c6eebb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627e6ef869672b1b7bb67bd5a74bdba32c341c134f9cad705b28f81b8f0e1a38(
    *,
    policy_document: builtins.str,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c309b6e47084dd6203318a3fa9b57377c3b49b057c711617683f6f4b712c13(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    destination_arn: builtins.str,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    distribution: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac5ce7ab85414a9ab4d07a6730c90303a0f6f9d21900acfa34cbad1068c3e34(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb14361fed02c4db43a0932407afa9b0115a6a35087a2cf2b8f2ca11127a800(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e798c2dcd3c6b5c8f4ed5e7f12612acaf7bd564ad175f0e8dc29ff7f64a76552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7837bfc99de40bda02092ef11f3ab18f09fa3b4a2af655884615123b2238901b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a848ba126c9392809ea99ca5e19a9daad4d405a9bd5ad71113a6eba8a8d729d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30c53e2238044eeabdb58fe12521d512be68ba9124a96f3bfc5367e0406ee06(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c19e816d1f986e29273f06ae0b73ed2a7554099fac6ca8c5b0a72de8709544(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288732d67b6d776d3fbb3ea79ed6035ffe508f4e6e884b4c7f85e72b0ceaf072(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ffd84b26d5803b73c5cf3c6076240ee2f143dee48f27b0d5bd9812df5a4e097(
    *,
    destination_arn: builtins.str,
    filter_pattern: builtins.str,
    log_group_name: builtins.str,
    distribution: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25991b0f3cd90c0ead8b679929ca6482be293e771ca4be27d23be9b0b1518a31(
    *,
    comparison: builtins.str,
    number_value: typing.Optional[jsii.Number] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8385eb16ba3569f03e0da403285b09a1cd68fb4851cb34cfde7d1db0908e5f12(
    *,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
    target_arn: builtins.str,
    destination_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12c867dce60bf09173093bf750d392ba4689c977ab027b6bb00cbd4ac4de8af(
    *patterns: JsonPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dddfad7e68dbd267d67c2e6243cb3474e87d4e15f4bde1bcb14a572c64e4b9d4(
    *terms: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8daf7ed22088c64251f58d811acc49d51c39ef2fb6512905b61f8212603a6dce(
    *patterns: JsonPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c086083fcdc9729199ce19516c28925c398d32d2bf4385f066140b5bd0ae93(
    *terms: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f490dc1cc4cb4c652bd94b41be028f11b34b43888af74efa67a48dcc0a7e3192(
    *term_groups: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5feb09f01306ac3af00a9343e2e42afcf2821bcb2c5496e2ad37f5bf6c744e3e(
    json_field: builtins.str,
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce84d76799399782f65215b9e275e5911bac66ec446b2b1911f993c31066de80(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e623cfcbdc8db428e5c910dbabfa70dec2e5ca569e002af922c4e0687ba4d54a(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9d3fcaa8b1b00f55df678f5944d9e544caf68b8d4ab2324976f80113dd0861(
    log_pattern_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a427ab962f9380edd6b2daba1e9e16fd501b0ca1f3320845f15de7bf5116d41a(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee269639b68b9cc22a951fc6acab5ec8b50d0e46b388d6e7663c07aaf7e6ab3(
    json_field: builtins.str,
    comparison: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce5c99a456f30a5a654f29bc555596cf9e6465e0cf8a647387c99cf3b3c91d2(
    *columns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1638c94c8ae801da61e7fe1b4c36f10c4da6f8f2aefc6ee054a88e581d32a660(
    json_field: builtins.str,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8435b9fe0f1f1ac0fcfe37217a44e20adead9bfb2f53aebc9d126da72053a62(
    id: builtins.str,
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac8be277097df09a82ca02fcf5d64644e033bb0017d8ce9a4bece0cb1be3d17(
    id: builtins.str,
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366b6c1cea54699757edbbcfe8d537f612d9c84640b0afdc93115057048094d7(
    id: builtins.str,
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90bb8ac1398b13f4c289ac239724b9648ed9433f046f4aad17b0d054d08e07e(
    json_field: builtins.str,
    metric_namespace: builtins.str,
    metric_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a720a3a946089a37be837ee306534f82ed11332e331740778c33506dfbd2f28(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95562428cbfc033e17460b3cd1f06e64be81f1ea118c19d4dc7252e54e6f588f(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf01a387df4b02adeb6bb4dceae63a13cf4ec522dd08101d158e4330938ed1c5(
    scope: _aws_cdk_core_f4b25747.Construct,
    source_log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b2b80876993186fa4e0b5716444dd1f7fff8354a805f35f012bb9ee8bdc506(
    json_pattern_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97af22380b83ee70ccc756af305ffc4d4ee5dbfee3f6d8e147e17f43438bf02c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    retention: typing.Optional[RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c054557df5fd12946464a179c6ed437034385a3f022b8b08552499ae7437c34a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ceea9f4f40ea5cacdc8fb256a76b0dd16b09d83a0bfe92c6adf89cbd2195a9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bcc8f9a761fb7023b15b7c4f4401fac3fe5beb70b5fdd2d247698537f8bc93(
    id: builtins.str,
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bf16eaac8c46d366ebfa3fa642aa1ef4c5b8a13264b933f195d6ca975a0b89(
    id: builtins.str,
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502819747cf4c96af2b5cc72205e7b13c78e2722d4f6c407ebbbc1d11d778ac0(
    id: builtins.str,
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4461ad8c4a0aa1a0cd854772affcab1b8d69663f518c3ad99c4d36e9c8d540da(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fcb78cebb01aa944b636845f0bbe65e20c1b5defb8f3ad2ee893ed1a7264346(
    json_field: builtins.str,
    metric_namespace: builtins.str,
    metric_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a584073841f54ee9844bd0752df8fa849b7c8fc548fb987b0304be0f53a08182(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2df0bbdada3a5fa7c7156b53be858b8a55bdd4312d8a8585fca1d9876be69b(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f17a19a7adf93289664d5773de5ba2d638eb61a2eab0a94641eb009280dcf2(
    *,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    retention: typing.Optional[RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12c43cc31930bc56a14fd1accdbba11fc5c1c0aee2e9590b73976d950aab79e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group_name: builtins.str,
    retention: RetentionDays,
    log_group_region: typing.Optional[builtins.str] = None,
    log_retention_retry_options: typing.Optional[typing.Union[LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895f130bee902a5a83a0aa11a3247dc80a37168b7adc395abb574e78ad015520(
    *,
    log_group_name: builtins.str,
    retention: RetentionDays,
    log_group_region: typing.Optional[builtins.str] = None,
    log_retention_retry_options: typing.Optional[typing.Union[LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7146aa77b5ffc90a996736a3e19c5283a2bb7659a61be3303f97d1dd0d144fa(
    *,
    base: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    max_retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cac097b81bc4ebe7289e7282eb5cde1a15112953834aa2898a0fd264c08ca91(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group: ILogGroup,
    log_stream_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1a6a46966768baa13021e795ceb7d866809bf525dc16a6ac78772e9fdf30cf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    log_stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eda758fb7d6923508bfc7c8238cc1f17d48bb5456bd3a554e7238f9c2ab0183(
    *,
    log_group: ILogGroup,
    log_stream_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd4700cd41a081d074e36cebb5356119bfaac9f28e05f5c288327496fc7ce5c(
    *,
    arn: builtins.str,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ffcbe12c1372344b1de53c9940be36b599c7e712b70c69cb672af0bb66d4ef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group: ILogGroup,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374b48d054c7b998f12d5e806c683276c4e4be86cb8ff5573954938cf6092623(
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100e83a70454e3dd4df2fc2c5e3636e60f11f80632c4e8f0e6a387f73fb2d462(
    *,
    filter_pattern: IFilterPattern,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    default_value: typing.Optional[jsii.Number] = None,
    metric_value: typing.Optional[builtins.str] = None,
    log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead5a62400fc0bd858eb01659d108b2bffb5c46f956999caee1a4baf846de3fd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    query_definition_name: builtins.str,
    query_string: QueryString,
    log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0310ec427ca69013660b21077c10a544dd720378ae9ea02af209ef3aa780037a(
    *,
    query_definition_name: builtins.str,
    query_string: QueryString,
    log_groups: typing.Optional[typing.Sequence[ILogGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ef890250a4eee691a58ce3e6a01f3d2b7af3afcc0f1a29af167952a1046d49(
    *,
    display: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    filter: typing.Optional[builtins.str] = None,
    limit: typing.Optional[jsii.Number] = None,
    parse: typing.Optional[builtins.str] = None,
    sort: typing.Optional[builtins.str] = None,
    stats: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ea75fa2dc73dbbda850da1f874f118d229860e7cfdd44f85179266dd54e479(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
    resource_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896557f17758d0c8f3b0e6bfab34975d6516647e512b7e34d766d8820f7ff946(
    *,
    policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.PolicyStatement]] = None,
    resource_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea2689a42af06bfeb160543c22e6b8155ccecd6887cf44dc96bf3dae059a92b(
    columns: typing.Sequence[builtins.str],
    restrictions: typing.Mapping[builtins.str, typing.Sequence[typing.Union[ColumnRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0dda74911439372e09fe611d28623b38dd5efb17f7fb049e95b41494798346(
    columns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee12fb948401852d08ad3f47e7ee45bd7a9838b1c693528897fe09a3bad0f5f(
    column_name: builtins.str,
    comparison: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f639c01762b8ad938cb20004b605fa5202918f09aeade600a8bb9e1d56179b(
    column_name: builtins.str,
    comparison: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce2251b01736601b2ac0794f0b3c5e8a287d00fa2c09360a00c34a63220dded(
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f960bf6c055b42696a5f22463e1ea2081644fba906942e629582ca60b0ecfd4f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group: ILogGroup,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448184ea673cd0baa41e13a3c7d041ae497e0b8eb3d1e5bc34c4774276c6af24(
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b76c867fb15c148d24d9ef614508a36ff48b549f4b48c4e1a448ece761baf2(
    *,
    destination: ILogSubscriptionDestination,
    filter_pattern: IFilterPattern,
    log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ea0d1cf7bd3e9c0919cc0a4c93ed09c3f6608b522aa762a88eac03d03ecb07(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
    target_arn: builtins.str,
    destination_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7e1e4c6ec64eb8aa5d35814d3f0e934f6f336b20f0ad2614bc443ea9c6b09e(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e837c642a32f333468145caf9a4f933a63a9db522c85c235bc05564d30c85d81(
    _scope: _aws_cdk_core_f4b25747.Construct,
    _source_log_group: ILogGroup,
) -> None:
    """Type checking stubs"""
    pass
