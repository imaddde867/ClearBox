'''
# AWS Key Management Service Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

Define a KMS key:

```python
kms.Key(self, "MyKey",
    enable_key_rotation=True
)
```

Define a KMS key with waiting period:

Specifies the number of days in the waiting period before AWS KMS deletes a CMK that has been removed from a CloudFormation stack.

```python
key = kms.Key(self, "MyKey",
    pending_window=Duration.days(10)
)
```

Add a couple of aliases:

```python
key = kms.Key(self, "MyKey")
key.add_alias("alias/foo")
key.add_alias("alias/bar")
```

Define a key with specific key spec and key usage:

Valid `keySpec` values depends on `keyUsage` value.

```python
key = kms.Key(self, "MyKey",
    key_spec=kms.KeySpec.ECC_SECG_P256K1,  # Default to SYMMETRIC_DEFAULT
    key_usage=kms.KeyUsage.SIGN_VERIFY
)
```

## Sharing keys between stacks

To use a KMS key in a different stack in the same CDK application,
pass the construct to the other stack:

```python
#
# Stack that defines the key
#
class KeyStack(cdk.Stack):

    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        self.key = kms.Key(self, "MyKey", removal_policy=cdk.RemovalPolicy.DESTROY)

#
# Stack that uses the key
#
class UseStack(cdk.Stack):
    def __init__(self, scope, id, *, key, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, key=key, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        # Use the IKey object here.
        kms.Alias(self, "Alias",
            alias_name="alias/foo",
            target_key=key
        )

key_stack = KeyStack(app, "KeyStack")
UseStack(app, "UseStack", key=key_stack.key)
```

## Importing existing keys

### Import key by ARN

To use a KMS key that is not defined in this CDK app, but is created through other means, use
`Key.fromKeyArn(parent, name, ref)`:

```python
my_key_imported = kms.Key.from_key_arn(self, "MyImportedKey", "arn:aws:...")

# you can do stuff with this imported key.
my_key_imported.add_alias("alias/foo")
```

Note that a call to `.addToResourcePolicy(statement)` on `myKeyImported` will not have
an affect on the key's policy because it is not owned by your stack. The call
will be a no-op.

### Import key by alias

If a Key has an associated Alias, the Alias can be imported by name and used in place
of the Key as a reference. A common scenario for this is in referencing AWS managed keys.

```python
import aws_cdk.aws_cloudtrail as cloudtrail


my_key_alias = kms.Alias.from_alias_name(self, "myKey", "alias/aws/s3")
trail = cloudtrail.Trail(self, "myCloudTrail",
    send_to_cloud_watch_logs=True,
    kms_key=my_key_alias
)
```

Note that calls to `addToResourcePolicy` and `grant*` methods on `myKeyAlias` will be
no-ops, and `addAlias` and `aliasTargetKey` will fail, as the imported alias does not
have a reference to the underlying KMS Key.

### Lookup key by alias

If you can't use a KMS key imported by alias (e.g. because you need access to the key id), you can lookup the key with `Key.fromLookup()`.

In general, the preferred method would be to use `Alias.fromAliasName()` which returns an `IAlias` object which extends `IKey`. However, some services need to have access to the underlying key id. In this case, `Key.fromLookup()` allows to lookup the key id.

The result of the `Key.fromLookup()` operation will be written to a file
called `cdk.context.json`. You must commit this file to source control so
that the lookup values are available in non-privileged environments such
as CI build steps, and to ensure your template builds are repeatable.

Here's how `Key.fromLookup()` can be used:

```python
my_key_lookup = kms.Key.from_lookup(self, "MyKeyLookup",
    alias_name="alias/KeyAlias"
)

role = iam.Role(self, "MyRole",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
)
my_key_lookup.grant_encrypt_decrypt(role)
```

Note that a call to `.addToResourcePolicy(statement)` on `myKeyLookup` will not have
an affect on the key's policy because it is not owned by your stack. The call
will be a no-op.

## Key Policies

Controlling access and usage of KMS Keys requires the use of key policies (resource-based policies attached to the key);
this is in contrast to most other AWS resources where access can be entirely controlled with IAM policies,
and optionally complemented with resource policies. For more in-depth understanding of KMS key access and policies, see

* https://docs.aws.amazon.com/kms/latest/developerguide/control-access-overview.html
* https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html

KMS keys can be created to trust IAM policies. This is the default behavior for both the KMS APIs and in
the console. This behavior is enabled by the '@aws-cdk/aws-kms:defaultKeyPolicies' feature flag,
which is set for all new projects; for existing projects, this same behavior can be enabled by
passing the `trustAccountIdentities` property as `true` when creating the key:

```python
kms.Key(self, "MyKey", trust_account_identities=True)
```

With either the `@aws-cdk/aws-kms:defaultKeyPolicies` feature flag set,
or the `trustAccountIdentities` prop set, the Key will be given the following default key policy:

```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::111122223333:root"},
  "Action": "kms:*",
  "Resource": "*"
}
```

This policy grants full access to the key to the root account user.
This enables the root account user -- via IAM policies -- to grant access to other IAM principals.
With the above default policy, future permissions can be added to either the key policy or IAM principal policy.

```python
key = kms.Key(self, "MyKey")
user = iam.User(self, "MyUser")
key.grant_encrypt(user)
```

Adopting the default KMS key policy (and so trusting account identities)
solves many issues around cyclic dependencies between stacks.
Without this default key policy, future permissions must be added to both the key policy and IAM principal policy,
which can cause cyclic dependencies if the permissions cross stack boundaries.
(For example, an encrypted bucket in one stack, and Lambda function that accesses it in another.)

### Appending to or replacing the default key policy

The default key policy can be amended or replaced entirely, depending on your use case and requirements.
A common addition to the key policy would be to add other key admins that are allowed to administer the key
(e.g., change permissions, revoke, delete). Additional key admins can be specified at key creation or after
via the `grantAdmin` method.

```python
my_trusted_admin_role = iam.Role.from_role_arn(self, "TrustedRole", "arn:aws:iam:....")
key = kms.Key(self, "MyKey",
    admins=[my_trusted_admin_role]
)

second_key = kms.Key(self, "MyKey2")
second_key.grant_admin(my_trusted_admin_role)
```

Alternatively, a custom key policy can be specified, which will replace the default key policy.

> **Note**: In applications without the '@aws-cdk/aws-kms:defaultKeyPolicies' feature flag set
> and with `trustedAccountIdentities` set to false (the default), specifying a policy at key creation *appends* the
> provided policy to the default key policy, rather than *replacing* the default policy.

```python
my_trusted_admin_role = iam.Role.from_role_arn(self, "TrustedRole", "arn:aws:iam:....")
# Creates a limited admin policy and assigns to the account root.
my_custom_policy = iam.PolicyDocument(
    statements=[iam.PolicyStatement(
        actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"
        ],
        principals=[iam.AccountRootPrincipal()],
        resources=["*"]
    )]
)
key = kms.Key(self, "MyKey",
    policy=my_custom_policy
)
```

> **Warning:** Replacing the default key policy with one that only grants access to a specific user or role
> runs the risk of the key becoming unmanageable if that user or role is deleted.
> It is highly recommended that the key policy grants access to the account root, rather than specific principals.
> See https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html for more information.
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


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kms.AliasAttributes",
    jsii_struct_bases=[],
    name_mapping={"alias_name": "aliasName", "alias_target_key": "aliasTargetKey"},
)
class AliasAttributes:
    def __init__(self, *, alias_name: builtins.str, alias_target_key: "IKey") -> None:
        '''Properties of a reference to an existing KMS Alias.

        :param alias_name: Specifies the alias name. This value must begin with alias/ followed by a name (i.e. alias/ExampleAlias)
        :param alias_target_key: The customer master key (CMK) to which the Alias refers.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kms as kms
            
            # key: kms.Key
            
            alias_attributes = kms.AliasAttributes(
                alias_name="aliasName",
                alias_target_key=key
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c13509115e8e038e4a6043370ce6a5eb2b93eba5b1b5538796ee22807fb583)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument alias_target_key", value=alias_target_key, expected_type=type_hints["alias_target_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias_name": alias_name,
            "alias_target_key": alias_target_key,
        }

    @builtins.property
    def alias_name(self) -> builtins.str:
        '''Specifies the alias name.

        This value must begin with alias/ followed by a name (i.e. alias/ExampleAlias)
        '''
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias_target_key(self) -> "IKey":
        '''The customer master key (CMK) to which the Alias refers.'''
        result = self._values.get("alias_target_key")
        assert result is not None, "Required property 'alias_target_key' is missing"
        return typing.cast("IKey", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AliasAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kms.AliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias_name": "aliasName",
        "target_key": "targetKey",
        "removal_policy": "removalPolicy",
    },
)
class AliasProps:
    def __init__(
        self,
        *,
        alias_name: builtins.str,
        target_key: "IKey",
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    ) -> None:
        '''Construction properties for a KMS Key Alias object.

        :param alias_name: The name of the alias. The name must start with alias followed by a forward slash, such as alias/. You can't specify aliases that begin with alias/AWS. These aliases are reserved.
        :param target_key: The ID of the key for which you are creating the alias. Specify the key's globally unique identifier or Amazon Resource Name (ARN). You can't specify another alias.
        :param removal_policy: Policy to apply when the alias is removed from this stack. Default: - The alias will be deleted

        :exampleMetadata: lit=test/integ.key-sharing.lit.ts infused

        Example::

            #
            # Stack that defines the key
            #
            class KeyStack(cdk.Stack):
            
                def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                    super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
                    self.key = kms.Key(self, "MyKey", removal_policy=cdk.RemovalPolicy.DESTROY)
            
            #
            # Stack that uses the key
            #
            class UseStack(cdk.Stack):
                def __init__(self, scope, id, *, key, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                    super().__init__(scope, id, key=key, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
            
                    # Use the IKey object here.
                    kms.Alias(self, "Alias",
                        alias_name="alias/foo",
                        target_key=key
                    )
            
            key_stack = KeyStack(app, "KeyStack")
            UseStack(app, "UseStack", key=key_stack.key)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7824789d4cf44e9bafbc9a7476170cc5f519640586a0b00cd8b9ffbbaf5e9f6e)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument target_key", value=target_key, expected_type=type_hints["target_key"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias_name": alias_name,
            "target_key": target_key,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def alias_name(self) -> builtins.str:
        '''The name of the alias.

        The name must start with alias followed by a
        forward slash, such as alias/. You can't specify aliases that begin with
        alias/AWS. These aliases are reserved.
        '''
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_key(self) -> "IKey":
        '''The ID of the key for which you are creating the alias.

        Specify the key's
        globally unique identifier or Amazon Resource Name (ARN). You can't
        specify another alias.
        '''
        result = self._values.get("target_key")
        assert result is not None, "Required property 'target_key' is missing"
        return typing.cast("IKey", result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy]:
        '''Policy to apply when the alias is removed from this stack.

        :default: - The alias will be deleted
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAlias(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kms.CfnAlias",
):
    '''A CloudFormation ``AWS::KMS::Alias``.

    The ``AWS::KMS::Alias`` resource specifies a display name for a `KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys>`_ . You can use an alias to identify a KMS key in the AWS KMS console, in the `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ operation, and in `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ , such as `Decrypt <https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html>`_ and `GenerateDataKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html>`_ .
    .. epigraph::

       Adding, deleting, or updating an alias can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

    Using an alias to refer to a KMS key can help you simplify key management. For example, an alias in your code can be associated with different KMS keys in different AWS Regions . For more information, see `Using aliases <https://docs.aws.amazon.com/kms/latest/developerguide/kms-alias.html>`_ in the *AWS Key Management Service Developer Guide* .

    When specifying an alias, observe the following rules.

    - Each alias is associated with one KMS key, but multiple aliases can be associated with the same KMS key.
    - The alias and its associated KMS key must be in the same AWS account and Region.
    - The alias name must be unique in the AWS account and Region. However, you can create aliases with the same name in different AWS Regions . For example, you can have an ``alias/projectKey`` in multiple Regions, each of which is associated with a KMS key in its Region.
    - Each alias name must begin with ``alias/`` followed by a name, such as ``alias/exampleKey`` . The alias name can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). Alias names cannot begin with ``alias/aws/`` . That alias name prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .

    *Regions*

    AWS KMS CloudFormation resources are available in all AWS Regions in which AWS KMS and AWS CloudFormation are supported.

    :cloudformationResource: AWS::KMS::Alias
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_kms as kms
        
        cfn_alias = kms.CfnAlias(self, "MyCfnAlias",
            alias_name="aliasName",
            target_key_id="targetKeyId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        alias_name: builtins.str,
        target_key_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::KMS::Alias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alias_name: Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias`` . .. epigraph:: If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC). The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/`` . The ``alias/aws/`` prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ . *Pattern* : ``^alias/[a-zA-Z0-9/_-]+$`` *Minimum* : ``1`` *Maximum* : ``256``
        :param target_key_id: Associates the alias with the specified `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ . The KMS key must be in the same AWS account and Region. A valid key ID is required. If you supply a null or empty string value, this operation returns an error. For help finding the key ID and ARN, see `Finding the key ID and ARN <https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn>`_ in the *AWS Key Management Service Developer Guide* . Specify the key ID or the key ARN of the KMS key. For example: - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` To get the key ID and key ARN for a KMS key, use `ListKeys <https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html>`_ or `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b506a20a6c6dcd3b6af210b0c2535764c1f6210a5ed41f6db31cc9ddec99e289)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAliasProps(alias_name=alias_name, target_key_id=target_key_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a592c037d8cf5eb56c8fbf2b691ca4ba6008a15e5c0628873ca76a825d54fcd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05b872b0a20a288c78b83081f7d8733f0ee43adbb75f68a6c498b7add2462307)
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
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        '''Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias`` .

        .. epigraph::

           If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC).

        The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/`` . The ``alias/aws/`` prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .

        *Pattern* : ``^alias/[a-zA-Z0-9/_-]+$``

        *Minimum* : ``1``

        *Maximum* : ``256``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-aliasname
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasName"))

    @alias_name.setter
    def alias_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33ee5bcef3759ff22cff5f4be978d2a088882867fa9cf74d62337691c36c2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aliasName", value)

    @builtins.property
    @jsii.member(jsii_name="targetKeyId")
    def target_key_id(self) -> builtins.str:
        '''Associates the alias with the specified `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ . The KMS key must be in the same AWS account and Region.

        A valid key ID is required. If you supply a null or empty string value, this operation returns an error.

        For help finding the key ID and ARN, see `Finding the key ID and ARN <https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn>`_ in the *AWS Key Management Service Developer Guide* .

        Specify the key ID or the key ARN of the KMS key.

        For example:

        - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
        - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``

        To get the key ID and key ARN for a KMS key, use `ListKeys <https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html>`_ or `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-targetkeyid
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetKeyId"))

    @target_key_id.setter
    def target_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030b0e4dce674403221f238f73863580de9fd10d8a85e65a616a2a6ba9299dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetKeyId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kms.CfnAliasProps",
    jsii_struct_bases=[],
    name_mapping={"alias_name": "aliasName", "target_key_id": "targetKeyId"},
)
class CfnAliasProps:
    def __init__(
        self,
        *,
        alias_name: builtins.str,
        target_key_id: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnAlias``.

        :param alias_name: Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias`` . .. epigraph:: If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC). The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/`` . The ``alias/aws/`` prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ . *Pattern* : ``^alias/[a-zA-Z0-9/_-]+$`` *Minimum* : ``1`` *Maximum* : ``256``
        :param target_key_id: Associates the alias with the specified `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ . The KMS key must be in the same AWS account and Region. A valid key ID is required. If you supply a null or empty string value, this operation returns an error. For help finding the key ID and ARN, see `Finding the key ID and ARN <https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn>`_ in the *AWS Key Management Service Developer Guide* . Specify the key ID or the key ARN of the KMS key. For example: - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` To get the key ID and key ARN for a KMS key, use `ListKeys <https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html>`_ or `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kms as kms
            
            cfn_alias_props = kms.CfnAliasProps(
                alias_name="aliasName",
                target_key_id="targetKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce24a029d04af8248ff498fbc64461d0b4d893863192fde8ae2ad6ac5b65caf)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument target_key_id", value=target_key_id, expected_type=type_hints["target_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias_name": alias_name,
            "target_key_id": target_key_id,
        }

    @builtins.property
    def alias_name(self) -> builtins.str:
        '''Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias`` .

        .. epigraph::

           If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC).

        The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/`` . The ``alias/aws/`` prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .

        *Pattern* : ``^alias/[a-zA-Z0-9/_-]+$``

        *Minimum* : ``1``

        *Maximum* : ``256``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-aliasname
        '''
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_key_id(self) -> builtins.str:
        '''Associates the alias with the specified `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ . The KMS key must be in the same AWS account and Region.

        A valid key ID is required. If you supply a null or empty string value, this operation returns an error.

        For help finding the key ID and ARN, see `Finding the key ID and ARN <https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn>`_ in the *AWS Key Management Service Developer Guide* .

        Specify the key ID or the key ARN of the KMS key.

        For example:

        - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
        - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``

        To get the key ID and key ARN for a KMS key, use `ListKeys <https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html>`_ or `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-targetkeyid
        '''
        result = self._values.get("target_key_id")
        assert result is not None, "Required property 'target_key_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnKey(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kms.CfnKey",
):
    '''A CloudFormation ``AWS::KMS::Key``.

    The ``AWS::KMS::Key`` resource specifies an `KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys>`_ in AWS Key Management Service . You can use this resource to create symmetric encryption KMS keys, asymmetric KMS keys for encryption or signing, and symmetric HMAC KMS keys. You can use ``AWS::KMS::Key`` to create `multi-Region primary keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html#mrk-primary-key>`_ of all supported types. To replicate a multi-Region key, use the ``AWS::KMS::ReplicaKey`` resource.
    .. epigraph::

       If you change the value of the ``KeySpec`` , ``KeyUsage`` , or ``MultiRegion`` properties of an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing any of its immutable property values. > AWS KMS replaced the term *customer master key (CMK)* with *AWS KMS key* and *KMS key* . The concept has not changed. To prevent breaking changes, AWS KMS is keeping some variations of this term.

    You can use symmetric encryption KMS keys to encrypt and decrypt small amounts of data, but they are more commonly used to generate data keys and data key pairs. You can also use a symmetric encryption KMS key to encrypt data stored in AWS services that are `integrated with AWS KMS <https://docs.aws.amazon.com//kms/features/#AWS_Service_Integration>`_ . For more information, see `Symmetric encryption KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#symmetric-cmks>`_ in the *AWS Key Management Service Developer Guide* .

    You can use asymmetric KMS keys to encrypt and decrypt data or sign messages and verify signatures. To create an asymmetric key, you must specify an asymmetric ``KeySpec`` value and a ``KeyUsage`` value. For details, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

    You can use HMAC KMS keys (which are also symmetric keys) to generate and verify hash-based message authentication codes. To create an HMAC key, you must specify an HMAC ``KeySpec`` value and a ``KeyUsage`` value of ``GENERATE_VERIFY_MAC`` . For details, see `HMAC keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/hmac.html>`_ in the *AWS Key Management Service Developer Guide* .

    You can also create symmetric encryption, asymmetric, and HMAC multi-Region primary keys. To create a multi-Region primary key, set the ``MultiRegion`` property to ``true`` . For information about multi-Region keys, see `Multi-Region keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

    You cannot use the ``AWS::KMS::Key`` resource to specify a KMS key with `imported key material <https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html>`_ or a KMS key in a `custom key store <https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html>`_ .

    *Regions*

    AWS KMS CloudFormation resources are available in all Regions in which AWS KMS and AWS CloudFormation are supported. You can use the ``AWS::KMS::Key`` resource to create and manage all KMS key types that are supported in a Region.

    :cloudformationResource: AWS::KMS::Key
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
    :exampleMetadata: infused

    Example::

        # cfn_template: cfn_inc.CfnInclude
        
        cfn_key = cfn_template.get_resource("Key")
        key = kms.Key.from_cfn_key(cfn_key)
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        key_policy: typing.Any,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        key_spec: typing.Optional[builtins.str] = None,
        key_usage: typing.Optional[builtins.str] = None,
        multi_region: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::KMS::Key``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_policy: The key policy that authorizes use of the KMS key. The key policy must conform to the following rules. - The key policy must allow the caller to make a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** . - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* . If you are unsure of which policy to use, consider the *default key policy* . This is the key policy that AWS KMS applies to KMS keys that are created by using the CreateKey API with no specified key policy. It gives the AWS account that owns the key permission to perform all operations on the key. It also allows you write IAM policies to authorize access to the key. For details, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default>`_ in the *AWS Key Management Service Developer Guide* . A key policy document can include only the following characters: - Printable ASCII characters - Printable characters in the Basic Latin and Latin-1 Supplement character set - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters *Minimum* : ``1`` *Maximum* : ``32768``
        :param description: A description of the KMS key. Use a description that helps you to distinguish this KMS key from others in the account, such as its intended use.
        :param enabled: Specifies whether the KMS key is enabled. Disabled KMS keys cannot be used in cryptographic operations. When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` . The actual key state of the KMS key might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param enable_key_rotation: Enables automatic rotation of the key material for the specified KMS key. By default, automatic key rotation is not enabled. AWS KMS supports automatic rotation only for symmetric encryption KMS keys ( ``KeySpec`` = ``SYMMETRIC_DEFAULT`` ). For asymmetric KMS keys and HMAC KMS keys, omit the ``EnableKeyRotation`` property or set it to ``false`` . To enable automatic key rotation of the key material for a multi-Region KMS key, set ``EnableKeyRotation`` to ``true`` on the primary key (created by using ``AWS::KMS::Key`` ). AWS KMS copies the rotation status to all replica keys. For details, see `Rotating multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-manage.html#multi-region-rotate>`_ in the *AWS Key Management Service Developer Guide* . When you enable automatic rotation, AWS KMS automatically creates new key material for the KMS key one year after the enable date and every year thereafter. AWS KMS retains all key material until you delete the KMS key. For detailed information about automatic key rotation, see `Rotating KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param key_spec: Specifies the type of KMS key to create. The default value, ``SYMMETRIC_DEFAULT`` , creates a KMS key with a 256-bit symmetric key for encryption and decryption. In China Regions, ``SYMMETRIC_DEFAULT`` creates a 128-bit symmetric key that uses SM4 encryption. You can't change the ``KeySpec`` value after the KMS key is created. For help choosing a key spec for your KMS key, see `Choosing a KMS key type <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html>`_ in the *AWS Key Management Service Developer Guide* . The ``KeySpec`` property determines the type of key material in the KMS key and the algorithms that the KMS key supports. To further restrict the algorithms that can be used with the KMS key, use a condition key in its key policy or IAM policy. For more information, see `AWS KMS condition keys <https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms>`_ in the *AWS Key Management Service Developer Guide* . .. epigraph:: If you change the value of the ``KeySpec`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. > `AWS services that are integrated with AWS KMS <https://docs.aws.amazon.com/kms/features/#AWS_Service_Integration>`_ use symmetric encryption KMS keys to protect your data. These services do not support encryption with asymmetric KMS keys. For help determining whether a KMS key is asymmetric, see `Identifying asymmetric KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/find-symm-asymm.html>`_ in the *AWS Key Management Service Developer Guide* . AWS KMS supports the following key specs for KMS keys: - Symmetric encryption key (default) - ``SYMMETRIC_DEFAULT`` (AES-256-GCM) - HMAC keys (symmetric) - ``HMAC_224`` - ``HMAC_256`` - ``HMAC_384`` - ``HMAC_512`` - Asymmetric RSA key pairs - ``RSA_2048`` - ``RSA_3072`` - ``RSA_4096`` - Asymmetric NIST-recommended elliptic curve key pairs - ``ECC_NIST_P256`` (secp256r1) - ``ECC_NIST_P384`` (secp384r1) - ``ECC_NIST_P521`` (secp521r1) - Other asymmetric elliptic curve key pairs - ``ECC_SECG_P256K1`` (secp256k1), commonly used for cryptocurrencies. - SM2 key pairs (China Regions only) - ``SM2``
        :param key_usage: Determines the `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ for which you can use the KMS key. The default value is ``ENCRYPT_DECRYPT`` . This property is required for asymmetric KMS keys and HMAC KMS keys. You can't change the ``KeyUsage`` value after the KMS key is created. .. epigraph:: If you change the value of the ``KeyUsage`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. Select only one valid value. - For symmetric encryption KMS keys, omit the property or specify ``ENCRYPT_DECRYPT`` . - For asymmetric KMS keys with RSA key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` . - For asymmetric KMS keys with ECC key material, specify ``SIGN_VERIFY`` . - For asymmetric KMS keys with SM2 (China Regions only) key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` . - For HMAC KMS keys, specify ``GENERATE_VERIFY_MAC`` .
        :param multi_region: Creates a multi-Region primary key that you can replicate in other AWS Regions . You can't change the ``MultiRegion`` value after the KMS key is created. For a list of AWS Regions in which multi-Region keys are supported, see `Multi-Region keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** . .. epigraph:: If you change the value of the ``MultiRegion`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. For a multi-Region key, set to this property to ``true`` . For a single-Region key, omit this property or set it to ``false`` . The default value is ``false`` . *Multi-Region keys* are an AWS KMS feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . You can create a symmetric encryption, HMAC, or asymmetric multi-Region KMS key, and you can create a multi-Region key with imported key material. However, you cannot create a multi-Region key in a custom key store. To create a replica of this primary key in a different AWS Region , create an `AWS::KMS::ReplicaKey <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html>`_ resource in a CloudFormation stack in the replica Region. Specify the key ARN of this primary key.
        :param pending_window_in_days: Specifies the number of days in the waiting period before AWS KMS deletes a KMS key that has been removed from a CloudFormation stack. Enter a value between 7 and 30 days. The default value is 30 days. When you remove a KMS key from a CloudFormation stack, AWS KMS schedules the KMS key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of KMS key is ``Pending Deletion`` or ``Pending Replica Deletion`` , which prevents the KMS key from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the KMS key. AWS KMS will not delete a `multi-Region primary key <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ that has replica keys. If you remove a multi-Region primary key from a CloudFormation stack, its key state changes to ``PendingReplicaDeletion`` so it cannot be replicated or used in cryptographic operations. This state can persist indefinitely. When the last of its replica keys is deleted, the key state of the primary key changes to ``PendingDeletion`` and the waiting period specified by ``PendingWindowInDays`` begins. When this waiting period expires, AWS KMS deletes the primary key. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* . You cannot use a CloudFormation template to cancel deletion of the KMS key after you remove it from the stack, regardless of the waiting period. If you specify a KMS key in your template, even one with the same name, CloudFormation creates a new KMS key. To cancel deletion of a KMS key, use the AWS KMS console or the `CancelKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_CancelKeyDeletion.html>`_ operation. For information about the ``Pending Deletion`` and ``Pending Replica Deletion`` key states, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* . *Minimum* : 7 *Maximum* : 30
        :param tags: Assigns one or more tags to the replica key. .. epigraph:: Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in AWS KMS , see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in CloudFormation, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7248794f26bf3b6b81f243e562390e80b7bf8b4657642b6c34d4a7b5d42f14cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnKeyProps(
            key_policy=key_policy,
            description=description,
            enabled=enabled,
            enable_key_rotation=enable_key_rotation,
            key_spec=key_spec,
            key_usage=key_usage,
            multi_region=multi_region,
            pending_window_in_days=pending_window_in_days,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df25b32bf80c52cef333a35d995fcf119908173afbaaa7838921132a08df046b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__decb5c9c70ebbad64089e7c02072be8f7bd6a219afd4f24657c741136919d93c)
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
        '''The Amazon Resource Name (ARN) of the KMS key, such as ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` .

        For information about the key ARN of a KMS key, see `Key ARN <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-ARN>`_ in the *AWS Key Management Service Developer Guide* .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrKeyId")
    def attr_key_id(self) -> builtins.str:
        '''The key ID of the KMS key, such as ``1234abcd-12ab-34cd-56ef-1234567890ab`` .

        For information about the key ID of a KMS key, see `Key ID <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id-key-id>`_ in the *AWS Key Management Service Developer Guide* .

        :cloudformationAttribute: KeyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKeyId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Assigns one or more tags to the replica key.

        .. epigraph::

           Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

        For information about tags in AWS KMS , see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in CloudFormation, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="keyPolicy")
    def key_policy(self) -> typing.Any:
        '''The key policy that authorizes use of the KMS key. The key policy must conform to the following rules.

        - The key policy must allow the caller to make a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** .
        - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* .

        If you are unsure of which policy to use, consider the *default key policy* . This is the key policy that AWS KMS applies to KMS keys that are created by using the CreateKey API with no specified key policy. It gives the AWS account that owns the key permission to perform all operations on the key. It also allows you write IAM policies to authorize access to the key. For details, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default>`_ in the *AWS Key Management Service Developer Guide* .

        A key policy document can include only the following characters:

        - Printable ASCII characters
        - Printable characters in the Basic Latin and Latin-1 Supplement character set
        - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters

        *Minimum* : ``1``

        *Maximum* : ``32768``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keypolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "keyPolicy"))

    @key_policy.setter
    def key_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aab3e6a664f52f5a9c3f11fbe682b21c6adbbb42a0e440386c5131eda41617f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the KMS key.

        Use a description that helps you to distinguish this KMS key from others in the account, such as its intended use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ae4d149404f325c7c27063006a5aa5688da81cdf2ce84169936eef1628a7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the KMS key is enabled. Disabled KMS keys cannot be used in cryptographic operations.

        When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` .

        The actual key state of the KMS key might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations.

        For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d3957bf573a963dba6c5abbb62621f6444da0980daa1486044a23b2dc296c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="enableKeyRotation")
    def enable_key_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables automatic rotation of the key material for the specified KMS key.

        By default, automatic key rotation is not enabled.

        AWS KMS supports automatic rotation only for symmetric encryption KMS keys ( ``KeySpec`` = ``SYMMETRIC_DEFAULT`` ). For asymmetric KMS keys and HMAC KMS keys, omit the ``EnableKeyRotation`` property or set it to ``false`` .

        To enable automatic key rotation of the key material for a multi-Region KMS key, set ``EnableKeyRotation`` to ``true`` on the primary key (created by using ``AWS::KMS::Key`` ). AWS KMS copies the rotation status to all replica keys. For details, see `Rotating multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-manage.html#multi-region-rotate>`_ in the *AWS Key Management Service Developer Guide* .

        When you enable automatic rotation, AWS KMS automatically creates new key material for the KMS key one year after the enable date and every year thereafter. AWS KMS retains all key material until you delete the KMS key. For detailed information about automatic key rotation, see `Rotating KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enablekeyrotation
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enableKeyRotation"))

    @enable_key_rotation.setter
    def enable_key_rotation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1211b35e1c49b2d1b30c778c5cfb39a7e336f92ef75769b665aefcb9823e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableKeyRotation", value)

    @builtins.property
    @jsii.member(jsii_name="keySpec")
    def key_spec(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of KMS key to create.

        The default value, ``SYMMETRIC_DEFAULT`` , creates a KMS key with a 256-bit symmetric key for encryption and decryption. In China Regions, ``SYMMETRIC_DEFAULT`` creates a 128-bit symmetric key that uses SM4 encryption. You can't change the ``KeySpec`` value after the KMS key is created. For help choosing a key spec for your KMS key, see `Choosing a KMS key type <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html>`_ in the *AWS Key Management Service Developer Guide* .

        The ``KeySpec`` property determines the type of key material in the KMS key and the algorithms that the KMS key supports. To further restrict the algorithms that can be used with the KMS key, use a condition key in its key policy or IAM policy. For more information, see `AWS KMS condition keys <https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms>`_ in the *AWS Key Management Service Developer Guide* .
        .. epigraph::

           If you change the value of the ``KeySpec`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. > `AWS services that are integrated with AWS KMS <https://docs.aws.amazon.com/kms/features/#AWS_Service_Integration>`_ use symmetric encryption KMS keys to protect your data. These services do not support encryption with asymmetric KMS keys. For help determining whether a KMS key is asymmetric, see `Identifying asymmetric KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/find-symm-asymm.html>`_ in the *AWS Key Management Service Developer Guide* .

        AWS KMS supports the following key specs for KMS keys:

        - Symmetric encryption key (default)
        - ``SYMMETRIC_DEFAULT`` (AES-256-GCM)
        - HMAC keys (symmetric)
        - ``HMAC_224``
        - ``HMAC_256``
        - ``HMAC_384``
        - ``HMAC_512``
        - Asymmetric RSA key pairs
        - ``RSA_2048``
        - ``RSA_3072``
        - ``RSA_4096``
        - Asymmetric NIST-recommended elliptic curve key pairs
        - ``ECC_NIST_P256`` (secp256r1)
        - ``ECC_NIST_P384`` (secp384r1)
        - ``ECC_NIST_P521`` (secp521r1)
        - Other asymmetric elliptic curve key pairs
        - ``ECC_SECG_P256K1`` (secp256k1), commonly used for cryptocurrencies.
        - SM2 key pairs (China Regions only)
        - ``SM2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyspec
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keySpec"))

    @key_spec.setter
    def key_spec(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a571c78fe90c983ca56d63153d8a623f8c3d53e987b4619ba04c569ff50d8ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keySpec", value)

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(self) -> typing.Optional[builtins.str]:
        '''Determines the `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ for which you can use the KMS key. The default value is ``ENCRYPT_DECRYPT`` . This property is required for asymmetric KMS keys and HMAC KMS keys. You can't change the ``KeyUsage`` value after the KMS key is created.

        .. epigraph::

           If you change the value of the ``KeyUsage`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value.

        Select only one valid value.

        - For symmetric encryption KMS keys, omit the property or specify ``ENCRYPT_DECRYPT`` .
        - For asymmetric KMS keys with RSA key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` .
        - For asymmetric KMS keys with ECC key material, specify ``SIGN_VERIFY`` .
        - For asymmetric KMS keys with SM2 (China Regions only) key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` .
        - For HMAC KMS keys, specify ``GENERATE_VERIFY_MAC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyusage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyUsage"))

    @key_usage.setter
    def key_usage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a728f5df84657fe9dc3f214a7418b430bd406e3fa794e860ae76b9a11999d1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyUsage", value)

    @builtins.property
    @jsii.member(jsii_name="multiRegion")
    def multi_region(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Creates a multi-Region primary key that you can replicate in other AWS Regions .

        You can't change the ``MultiRegion`` value after the KMS key is created.

        For a list of AWS Regions in which multi-Region keys are supported, see `Multi-Region keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** .
        .. epigraph::

           If you change the value of the ``MultiRegion`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value.

        For a multi-Region key, set to this property to ``true`` . For a single-Region key, omit this property or set it to ``false`` . The default value is ``false`` .

        *Multi-Region keys* are an AWS KMS feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        You can create a symmetric encryption, HMAC, or asymmetric multi-Region KMS key, and you can create a multi-Region key with imported key material. However, you cannot create a multi-Region key in a custom key store.

        To create a replica of this primary key in a different AWS Region , create an `AWS::KMS::ReplicaKey <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html>`_ resource in a CloudFormation stack in the replica Region. Specify the key ARN of this primary key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-multiregion
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "multiRegion"))

    @multi_region.setter
    def multi_region(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4c3fe229901d0296615ebba2ffb43424aa2f5e25550028fe4dd6accabbcf40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiRegion", value)

    @builtins.property
    @jsii.member(jsii_name="pendingWindowInDays")
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days in the waiting period before AWS KMS deletes a KMS key that has been removed from a CloudFormation stack.

        Enter a value between 7 and 30 days. The default value is 30 days.

        When you remove a KMS key from a CloudFormation stack, AWS KMS schedules the KMS key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of KMS key is ``Pending Deletion`` or ``Pending Replica Deletion`` , which prevents the KMS key from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the KMS key.

        AWS KMS will not delete a `multi-Region primary key <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ that has replica keys. If you remove a multi-Region primary key from a CloudFormation stack, its key state changes to ``PendingReplicaDeletion`` so it cannot be replicated or used in cryptographic operations. This state can persist indefinitely. When the last of its replica keys is deleted, the key state of the primary key changes to ``PendingDeletion`` and the waiting period specified by ``PendingWindowInDays`` begins. When this waiting period expires, AWS KMS deletes the primary key. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* .

        You cannot use a CloudFormation template to cancel deletion of the KMS key after you remove it from the stack, regardless of the waiting period. If you specify a KMS key in your template, even one with the same name, CloudFormation creates a new KMS key. To cancel deletion of a KMS key, use the AWS KMS console or the `CancelKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_CancelKeyDeletion.html>`_ operation.

        For information about the ``Pending Deletion`` and ``Pending Replica Deletion`` key states, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        *Minimum* : 7

        *Maximum* : 30

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-pendingwindowindays
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pendingWindowInDays"))

    @pending_window_in_days.setter
    def pending_window_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7032cf4f218f41bb90deea579df2d188d5a625355193dfb17b2f5a1411b9c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pendingWindowInDays", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kms.CfnKeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_policy": "keyPolicy",
        "description": "description",
        "enabled": "enabled",
        "enable_key_rotation": "enableKeyRotation",
        "key_spec": "keySpec",
        "key_usage": "keyUsage",
        "multi_region": "multiRegion",
        "pending_window_in_days": "pendingWindowInDays",
        "tags": "tags",
    },
)
class CfnKeyProps:
    def __init__(
        self,
        *,
        key_policy: typing.Any,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        key_spec: typing.Optional[builtins.str] = None,
        key_usage: typing.Optional[builtins.str] = None,
        multi_region: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnKey``.

        :param key_policy: The key policy that authorizes use of the KMS key. The key policy must conform to the following rules. - The key policy must allow the caller to make a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** . - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* . If you are unsure of which policy to use, consider the *default key policy* . This is the key policy that AWS KMS applies to KMS keys that are created by using the CreateKey API with no specified key policy. It gives the AWS account that owns the key permission to perform all operations on the key. It also allows you write IAM policies to authorize access to the key. For details, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default>`_ in the *AWS Key Management Service Developer Guide* . A key policy document can include only the following characters: - Printable ASCII characters - Printable characters in the Basic Latin and Latin-1 Supplement character set - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters *Minimum* : ``1`` *Maximum* : ``32768``
        :param description: A description of the KMS key. Use a description that helps you to distinguish this KMS key from others in the account, such as its intended use.
        :param enabled: Specifies whether the KMS key is enabled. Disabled KMS keys cannot be used in cryptographic operations. When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` . The actual key state of the KMS key might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param enable_key_rotation: Enables automatic rotation of the key material for the specified KMS key. By default, automatic key rotation is not enabled. AWS KMS supports automatic rotation only for symmetric encryption KMS keys ( ``KeySpec`` = ``SYMMETRIC_DEFAULT`` ). For asymmetric KMS keys and HMAC KMS keys, omit the ``EnableKeyRotation`` property or set it to ``false`` . To enable automatic key rotation of the key material for a multi-Region KMS key, set ``EnableKeyRotation`` to ``true`` on the primary key (created by using ``AWS::KMS::Key`` ). AWS KMS copies the rotation status to all replica keys. For details, see `Rotating multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-manage.html#multi-region-rotate>`_ in the *AWS Key Management Service Developer Guide* . When you enable automatic rotation, AWS KMS automatically creates new key material for the KMS key one year after the enable date and every year thereafter. AWS KMS retains all key material until you delete the KMS key. For detailed information about automatic key rotation, see `Rotating KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param key_spec: Specifies the type of KMS key to create. The default value, ``SYMMETRIC_DEFAULT`` , creates a KMS key with a 256-bit symmetric key for encryption and decryption. In China Regions, ``SYMMETRIC_DEFAULT`` creates a 128-bit symmetric key that uses SM4 encryption. You can't change the ``KeySpec`` value after the KMS key is created. For help choosing a key spec for your KMS key, see `Choosing a KMS key type <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html>`_ in the *AWS Key Management Service Developer Guide* . The ``KeySpec`` property determines the type of key material in the KMS key and the algorithms that the KMS key supports. To further restrict the algorithms that can be used with the KMS key, use a condition key in its key policy or IAM policy. For more information, see `AWS KMS condition keys <https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms>`_ in the *AWS Key Management Service Developer Guide* . .. epigraph:: If you change the value of the ``KeySpec`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. > `AWS services that are integrated with AWS KMS <https://docs.aws.amazon.com/kms/features/#AWS_Service_Integration>`_ use symmetric encryption KMS keys to protect your data. These services do not support encryption with asymmetric KMS keys. For help determining whether a KMS key is asymmetric, see `Identifying asymmetric KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/find-symm-asymm.html>`_ in the *AWS Key Management Service Developer Guide* . AWS KMS supports the following key specs for KMS keys: - Symmetric encryption key (default) - ``SYMMETRIC_DEFAULT`` (AES-256-GCM) - HMAC keys (symmetric) - ``HMAC_224`` - ``HMAC_256`` - ``HMAC_384`` - ``HMAC_512`` - Asymmetric RSA key pairs - ``RSA_2048`` - ``RSA_3072`` - ``RSA_4096`` - Asymmetric NIST-recommended elliptic curve key pairs - ``ECC_NIST_P256`` (secp256r1) - ``ECC_NIST_P384`` (secp384r1) - ``ECC_NIST_P521`` (secp521r1) - Other asymmetric elliptic curve key pairs - ``ECC_SECG_P256K1`` (secp256k1), commonly used for cryptocurrencies. - SM2 key pairs (China Regions only) - ``SM2``
        :param key_usage: Determines the `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ for which you can use the KMS key. The default value is ``ENCRYPT_DECRYPT`` . This property is required for asymmetric KMS keys and HMAC KMS keys. You can't change the ``KeyUsage`` value after the KMS key is created. .. epigraph:: If you change the value of the ``KeyUsage`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. Select only one valid value. - For symmetric encryption KMS keys, omit the property or specify ``ENCRYPT_DECRYPT`` . - For asymmetric KMS keys with RSA key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` . - For asymmetric KMS keys with ECC key material, specify ``SIGN_VERIFY`` . - For asymmetric KMS keys with SM2 (China Regions only) key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` . - For HMAC KMS keys, specify ``GENERATE_VERIFY_MAC`` .
        :param multi_region: Creates a multi-Region primary key that you can replicate in other AWS Regions . You can't change the ``MultiRegion`` value after the KMS key is created. For a list of AWS Regions in which multi-Region keys are supported, see `Multi-Region keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** . .. epigraph:: If you change the value of the ``MultiRegion`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. For a multi-Region key, set to this property to ``true`` . For a single-Region key, omit this property or set it to ``false`` . The default value is ``false`` . *Multi-Region keys* are an AWS KMS feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . You can create a symmetric encryption, HMAC, or asymmetric multi-Region KMS key, and you can create a multi-Region key with imported key material. However, you cannot create a multi-Region key in a custom key store. To create a replica of this primary key in a different AWS Region , create an `AWS::KMS::ReplicaKey <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html>`_ resource in a CloudFormation stack in the replica Region. Specify the key ARN of this primary key.
        :param pending_window_in_days: Specifies the number of days in the waiting period before AWS KMS deletes a KMS key that has been removed from a CloudFormation stack. Enter a value between 7 and 30 days. The default value is 30 days. When you remove a KMS key from a CloudFormation stack, AWS KMS schedules the KMS key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of KMS key is ``Pending Deletion`` or ``Pending Replica Deletion`` , which prevents the KMS key from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the KMS key. AWS KMS will not delete a `multi-Region primary key <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ that has replica keys. If you remove a multi-Region primary key from a CloudFormation stack, its key state changes to ``PendingReplicaDeletion`` so it cannot be replicated or used in cryptographic operations. This state can persist indefinitely. When the last of its replica keys is deleted, the key state of the primary key changes to ``PendingDeletion`` and the waiting period specified by ``PendingWindowInDays`` begins. When this waiting period expires, AWS KMS deletes the primary key. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* . You cannot use a CloudFormation template to cancel deletion of the KMS key after you remove it from the stack, regardless of the waiting period. If you specify a KMS key in your template, even one with the same name, CloudFormation creates a new KMS key. To cancel deletion of a KMS key, use the AWS KMS console or the `CancelKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_CancelKeyDeletion.html>`_ operation. For information about the ``Pending Deletion`` and ``Pending Replica Deletion`` key states, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* . *Minimum* : 7 *Maximum* : 30
        :param tags: Assigns one or more tags to the replica key. .. epigraph:: Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in AWS KMS , see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in CloudFormation, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kms as kms
            
            # key_policy: Any
            
            cfn_key_props = kms.CfnKeyProps(
                key_policy=key_policy,
            
                # the properties below are optional
                description="description",
                enabled=False,
                enable_key_rotation=False,
                key_spec="keySpec",
                key_usage="keyUsage",
                multi_region=False,
                pending_window_in_days=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16d036cc4e7e4855c8824e44f7c62a103452211e66c359b4c19e16f5ed47abf)
            check_type(argname="argument key_policy", value=key_policy, expected_type=type_hints["key_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_key_rotation", value=enable_key_rotation, expected_type=type_hints["enable_key_rotation"])
            check_type(argname="argument key_spec", value=key_spec, expected_type=type_hints["key_spec"])
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument multi_region", value=multi_region, expected_type=type_hints["multi_region"])
            check_type(argname="argument pending_window_in_days", value=pending_window_in_days, expected_type=type_hints["pending_window_in_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_policy": key_policy,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if key_spec is not None:
            self._values["key_spec"] = key_spec
        if key_usage is not None:
            self._values["key_usage"] = key_usage
        if multi_region is not None:
            self._values["multi_region"] = multi_region
        if pending_window_in_days is not None:
            self._values["pending_window_in_days"] = pending_window_in_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def key_policy(self) -> typing.Any:
        '''The key policy that authorizes use of the KMS key. The key policy must conform to the following rules.

        - The key policy must allow the caller to make a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** .
        - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* .

        If you are unsure of which policy to use, consider the *default key policy* . This is the key policy that AWS KMS applies to KMS keys that are created by using the CreateKey API with no specified key policy. It gives the AWS account that owns the key permission to perform all operations on the key. It also allows you write IAM policies to authorize access to the key. For details, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default>`_ in the *AWS Key Management Service Developer Guide* .

        A key policy document can include only the following characters:

        - Printable ASCII characters
        - Printable characters in the Basic Latin and Latin-1 Supplement character set
        - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters

        *Minimum* : ``1``

        *Maximum* : ``32768``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keypolicy
        '''
        result = self._values.get("key_policy")
        assert result is not None, "Required property 'key_policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the KMS key.

        Use a description that helps you to distinguish this KMS key from others in the account, such as its intended use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the KMS key is enabled. Disabled KMS keys cannot be used in cryptographic operations.

        When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` .

        The actual key state of the KMS key might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations.

        For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def enable_key_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables automatic rotation of the key material for the specified KMS key.

        By default, automatic key rotation is not enabled.

        AWS KMS supports automatic rotation only for symmetric encryption KMS keys ( ``KeySpec`` = ``SYMMETRIC_DEFAULT`` ). For asymmetric KMS keys and HMAC KMS keys, omit the ``EnableKeyRotation`` property or set it to ``false`` .

        To enable automatic key rotation of the key material for a multi-Region KMS key, set ``EnableKeyRotation`` to ``true`` on the primary key (created by using ``AWS::KMS::Key`` ). AWS KMS copies the rotation status to all replica keys. For details, see `Rotating multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-manage.html#multi-region-rotate>`_ in the *AWS Key Management Service Developer Guide* .

        When you enable automatic rotation, AWS KMS automatically creates new key material for the KMS key one year after the enable date and every year thereafter. AWS KMS retains all key material until you delete the KMS key. For detailed information about automatic key rotation, see `Rotating KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enablekeyrotation
        '''
        result = self._values.get("enable_key_rotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def key_spec(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of KMS key to create.

        The default value, ``SYMMETRIC_DEFAULT`` , creates a KMS key with a 256-bit symmetric key for encryption and decryption. In China Regions, ``SYMMETRIC_DEFAULT`` creates a 128-bit symmetric key that uses SM4 encryption. You can't change the ``KeySpec`` value after the KMS key is created. For help choosing a key spec for your KMS key, see `Choosing a KMS key type <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html>`_ in the *AWS Key Management Service Developer Guide* .

        The ``KeySpec`` property determines the type of key material in the KMS key and the algorithms that the KMS key supports. To further restrict the algorithms that can be used with the KMS key, use a condition key in its key policy or IAM policy. For more information, see `AWS KMS condition keys <https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms>`_ in the *AWS Key Management Service Developer Guide* .
        .. epigraph::

           If you change the value of the ``KeySpec`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. > `AWS services that are integrated with AWS KMS <https://docs.aws.amazon.com/kms/features/#AWS_Service_Integration>`_ use symmetric encryption KMS keys to protect your data. These services do not support encryption with asymmetric KMS keys. For help determining whether a KMS key is asymmetric, see `Identifying asymmetric KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/find-symm-asymm.html>`_ in the *AWS Key Management Service Developer Guide* .

        AWS KMS supports the following key specs for KMS keys:

        - Symmetric encryption key (default)
        - ``SYMMETRIC_DEFAULT`` (AES-256-GCM)
        - HMAC keys (symmetric)
        - ``HMAC_224``
        - ``HMAC_256``
        - ``HMAC_384``
        - ``HMAC_512``
        - Asymmetric RSA key pairs
        - ``RSA_2048``
        - ``RSA_3072``
        - ``RSA_4096``
        - Asymmetric NIST-recommended elliptic curve key pairs
        - ``ECC_NIST_P256`` (secp256r1)
        - ``ECC_NIST_P384`` (secp384r1)
        - ``ECC_NIST_P521`` (secp521r1)
        - Other asymmetric elliptic curve key pairs
        - ``ECC_SECG_P256K1`` (secp256k1), commonly used for cryptocurrencies.
        - SM2 key pairs (China Regions only)
        - ``SM2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyspec
        '''
        result = self._values.get("key_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_usage(self) -> typing.Optional[builtins.str]:
        '''Determines the `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ for which you can use the KMS key. The default value is ``ENCRYPT_DECRYPT`` . This property is required for asymmetric KMS keys and HMAC KMS keys. You can't change the ``KeyUsage`` value after the KMS key is created.

        .. epigraph::

           If you change the value of the ``KeyUsage`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value.

        Select only one valid value.

        - For symmetric encryption KMS keys, omit the property or specify ``ENCRYPT_DECRYPT`` .
        - For asymmetric KMS keys with RSA key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` .
        - For asymmetric KMS keys with ECC key material, specify ``SIGN_VERIFY`` .
        - For asymmetric KMS keys with SM2 (China Regions only) key material, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` .
        - For HMAC KMS keys, specify ``GENERATE_VERIFY_MAC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyusage
        '''
        result = self._values.get("key_usage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Creates a multi-Region primary key that you can replicate in other AWS Regions .

        You can't change the ``MultiRegion`` value after the KMS key is created.

        For a list of AWS Regions in which multi-Region keys are supported, see `Multi-Region keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** .
        .. epigraph::

           If you change the value of the ``MultiRegion`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value.

        For a multi-Region key, set to this property to ``true`` . For a single-Region key, omit this property or set it to ``false`` . The default value is ``false`` .

        *Multi-Region keys* are an AWS KMS feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        You can create a symmetric encryption, HMAC, or asymmetric multi-Region KMS key, and you can create a multi-Region key with imported key material. However, you cannot create a multi-Region key in a custom key store.

        To create a replica of this primary key in a different AWS Region , create an `AWS::KMS::ReplicaKey <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html>`_ resource in a CloudFormation stack in the replica Region. Specify the key ARN of this primary key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-multiregion
        '''
        result = self._values.get("multi_region")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days in the waiting period before AWS KMS deletes a KMS key that has been removed from a CloudFormation stack.

        Enter a value between 7 and 30 days. The default value is 30 days.

        When you remove a KMS key from a CloudFormation stack, AWS KMS schedules the KMS key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of KMS key is ``Pending Deletion`` or ``Pending Replica Deletion`` , which prevents the KMS key from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the KMS key.

        AWS KMS will not delete a `multi-Region primary key <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ that has replica keys. If you remove a multi-Region primary key from a CloudFormation stack, its key state changes to ``PendingReplicaDeletion`` so it cannot be replicated or used in cryptographic operations. This state can persist indefinitely. When the last of its replica keys is deleted, the key state of the primary key changes to ``PendingDeletion`` and the waiting period specified by ``PendingWindowInDays`` begins. When this waiting period expires, AWS KMS deletes the primary key. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* .

        You cannot use a CloudFormation template to cancel deletion of the KMS key after you remove it from the stack, regardless of the waiting period. If you specify a KMS key in your template, even one with the same name, CloudFormation creates a new KMS key. To cancel deletion of a KMS key, use the AWS KMS console or the `CancelKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_CancelKeyDeletion.html>`_ operation.

        For information about the ``Pending Deletion`` and ``Pending Replica Deletion`` key states, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        *Minimum* : 7

        *Maximum* : 30

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-pendingwindowindays
        '''
        result = self._values.get("pending_window_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Assigns one or more tags to the replica key.

        .. epigraph::

           Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

        For information about tags in AWS KMS , see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in CloudFormation, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnReplicaKey(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kms.CfnReplicaKey",
):
    '''A CloudFormation ``AWS::KMS::ReplicaKey``.

    The ``AWS::KMS::ReplicaKey`` resource specifies a multi-Region replica key that is based on a multi-Region primary key.

    *Multi-Region keys* are an AWS KMS feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

    A multi-Region *primary key* is a fully functional symmetric encryption KMS key, HMAC KMS key, or asymmetric KMS key that is also the model for replica keys in other AWS Regions . To create a multi-Region primary key, add an `AWS::KMS::Key <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html>`_ resource to your CloudFormation stack. Set its ``MultiRegion`` property to true.

    A multi-Region *replica key* is a fully functional KMS key that has the same key ID and key material as a multi-Region primary key, but is located in a different AWS Region of the same AWS partition. There can be multiple replicas of a primary key, but each must be in a different AWS Region .

    When you create a replica key in AWS CloudFormation , the replica key is created in the AWS Region represented by the endpoint you use for the request. If you try to replicate a multi-Region key into a Region in which the key type is not supported, the request will fail.

    A primary key and its replicas have the same key ID and key material. They also have the same key spec, key usage, key material origin, and automatic key rotation status. These properties are known as *shared properties* . If they change, AWS KMS synchronizes the change to all related multi-Region keys. All other properties of a replica key can differ, including its key policy, tags, aliases, and key state. AWS KMS does not synchronize these properties.

    *Regions*

    AWS KMS CloudFormation resources are available in all AWS Regions in which AWS KMS and AWS CloudFormation are supported. You can use the ``AWS::KMS::ReplicaKey`` resource to create replica keys in all Regions that support multi-Region KMS keys. For details, see `Multi-Region keys in AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** .

    :cloudformationResource: AWS::KMS::ReplicaKey
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_kms as kms
        
        # key_policy: Any
        
        cfn_replica_key = kms.CfnReplicaKey(self, "MyCfnReplicaKey",
            key_policy=key_policy,
            primary_key_arn="primaryKeyArn",
        
            # the properties below are optional
            description="description",
            enabled=False,
            pending_window_in_days=123,
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
        key_policy: typing.Any,
        primary_key_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::KMS::ReplicaKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_policy: The key policy that authorizes use of the replica key. The key policy is not a shared property of multi-Region keys. You can specify the same key policy or a different key policy for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property. The key policy must conform to the following rules. - The key policy must give the caller `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ permission on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** . - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* . A key policy document can include only the following characters: - Printable ASCII characters from the space character ( ``\\ u0020`` ) through the end of the ASCII character range. - Printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ). - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters *Minimum* : ``1`` *Maximum* : ``32768``
        :param primary_key_arn: Specifies the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS partition. You can create only one replica of a given primary key in each AWS Region . .. epigraph:: If you change the ``PrimaryKeyArn`` value of a replica key, the existing replica key is scheduled for deletion and a new replica key is created based on the specified primary key. While it is scheduled for deletion, the existing replica key becomes unusable. You can cancel the scheduled deletion of the key outside of CloudFormation. However, if you inadvertently delete a replica key, you can decrypt ciphertext encrypted by that replica key by using any related multi-Region key. If necessary, you can recreate the replica in the same Region after the previous one is completely deleted. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* Specify the key ARN of an existing multi-Region primary key. For example, ``arn:aws:kms:us-east-2:111122223333:key/mrk-1234abcd12ab34cd56ef1234567890ab`` .
        :param description: A description of the KMS key. The default value is an empty string (no description). The description is not a shared property of multi-Region keys. You can specify the same description or a different description for each key in a set of related multi-Region keys. AWS Key Management Service does not synchronize this property.
        :param enabled: Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` . The actual key state of the replica might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. Also, while the replica key is being created, its key state is ``Creating`` . When the process is complete, the key state of the replica key changes to ``Enabled`` . For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param pending_window_in_days: Specifies the number of days in the waiting period before AWS KMS deletes a replica key that has been removed from a CloudFormation stack. Enter a value between 7 and 30 days. The default value is 30 days. When you remove a replica key from a CloudFormation stack, AWS KMS schedules the replica key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of replica key is ``Pending Deletion`` , which prevents it from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the replica key. If the KMS key is a multi-Region primary key with replica keys, the waiting period begins when the last of its replica keys is deleted. Otherwise, the waiting period begins immediately. You cannot use a CloudFormation template to cancel deletion of the replica after you remove it from the stack, regardless of the waiting period. However, if you specify a replica key in your template that is based on the same primary key as the original replica key, CloudFormation creates a new replica key with the same key ID, key material, and other shared properties of the original replica key. This new replica key can decrypt ciphertext that was encrypted under the original replica key, or any related multi-Region key. For detailed information about deleting multi-Region keys, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* . For information about the ``PendingDeletion`` key state, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* . *Minimum* : 7 *Maximum* : 30
        :param tags: Assigns one or more tags to the replica key. .. epigraph:: Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* . Tags are not a shared property of multi-Region keys. You can specify the same tags or different tags for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property. Each tag consists of a tag key and a tag value. Both the tag key and the tag value are required, but the tag value can be an empty (null) string. You cannot have more than one tag on a KMS key with the same tag key. If you specify an existing tag key with a different tag value, AWS KMS replaces the current tag value with the specified one. When you assign tags to an AWS resource, AWS generates a cost allocation report with usage and costs aggregated by tags. Tags can also be used to control access to a KMS key. For details, see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d559427e1d7884de953e4026fc80eb13cfc39d05aad8e903fd1f946a17a5da2c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReplicaKeyProps(
            key_policy=key_policy,
            primary_key_arn=primary_key_arn,
            description=description,
            enabled=enabled,
            pending_window_in_days=pending_window_in_days,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1dd7d5ae6612915dcecdc900a84c16ae34cd746cb3526b91a755ea450a34a28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b165feb645cb87d0d563cdb5bb805ada5fc4eec0ecdac8dbf71b7f2591f17d)
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
        '''The Amazon Resource Name (ARN) of the replica key, such as ``arn:aws:kms:us-west-2:111122223333:key/mrk-1234abcd12ab34cd56ef1234567890ab`` .

        The key ARNs of related multi-Region keys differ only in the Region value. For information about the key ARNs of multi-Region keys, see `How multi-Region keys work <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html#mrk-how-it-works>`_ in the *AWS Key Management Service Developer Guide* .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrKeyId")
    def attr_key_id(self) -> builtins.str:
        '''The key ID of the replica key, such as ``mrk-1234abcd12ab34cd56ef1234567890ab`` .

        Related multi-Region keys have the same key ID. For information about the key IDs of multi-Region keys, see `How multi-Region keys work <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html#mrk-how-it-works>`_ in the *AWS Key Management Service Developer Guide* .

        :cloudformationAttribute: KeyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKeyId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Assigns one or more tags to the replica key.

        .. epigraph::

           Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

        Tags are not a shared property of multi-Region keys. You can specify the same tags or different tags for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property.

        Each tag consists of a tag key and a tag value. Both the tag key and the tag value are required, but the tag value can be an empty (null) string. You cannot have more than one tag on a KMS key with the same tag key. If you specify an existing tag key with a different tag value, AWS KMS replaces the current tag value with the specified one.

        When you assign tags to an AWS resource, AWS generates a cost allocation report with usage and costs aggregated by tags. Tags can also be used to control access to a KMS key. For details, see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="keyPolicy")
    def key_policy(self) -> typing.Any:
        '''The key policy that authorizes use of the replica key.

        The key policy is not a shared property of multi-Region keys. You can specify the same key policy or a different key policy for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property.

        The key policy must conform to the following rules.

        - The key policy must give the caller `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ permission on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** .
        - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* .

        A key policy document can include only the following characters:

        - Printable ASCII characters from the space character ( ``\\ u0020`` ) through the end of the ASCII character range.
        - Printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ).
        - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters

        *Minimum* : ``1``

        *Maximum* : ``32768``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-keypolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "keyPolicy"))

    @key_policy.setter
    def key_policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a9ff41f934a1a642ef2128eadf89099f2a76ac59fb21d89ec3bbd2106d7660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKeyArn")
    def primary_key_arn(self) -> builtins.str:
        '''Specifies the multi-Region primary key to replicate.

        The primary key must be in a different AWS Region of the same AWS partition. You can create only one replica of a given primary key in each AWS Region .
        .. epigraph::

           If you change the ``PrimaryKeyArn`` value of a replica key, the existing replica key is scheduled for deletion and a new replica key is created based on the specified primary key. While it is scheduled for deletion, the existing replica key becomes unusable. You can cancel the scheduled deletion of the key outside of CloudFormation.

           However, if you inadvertently delete a replica key, you can decrypt ciphertext encrypted by that replica key by using any related multi-Region key. If necessary, you can recreate the replica in the same Region after the previous one is completely deleted. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide*

        Specify the key ARN of an existing multi-Region primary key. For example, ``arn:aws:kms:us-east-2:111122223333:key/mrk-1234abcd12ab34cd56ef1234567890ab`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-primarykeyarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "primaryKeyArn"))

    @primary_key_arn.setter
    def primary_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551ff52f760067b3c65e675f5671f4f2771e11e9e8a5749287e6012a5073a3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the KMS key.

        The default value is an empty string (no description).

        The description is not a shared property of multi-Region keys. You can specify the same description or a different description for each key in a set of related multi-Region keys. AWS Key Management Service does not synchronize this property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1286c5b360d6530edb9610619a9669208251831b0deb87e68bb3e965c1fe59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations.

        When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` .

        The actual key state of the replica might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. Also, while the replica key is being created, its key state is ``Creating`` . When the process is complete, the key state of the replica key changes to ``Enabled`` .

        For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc85df26c8a13553d5d476d44148176f759db9348941b186aed2444fc263e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="pendingWindowInDays")
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days in the waiting period before AWS KMS deletes a replica key that has been removed from a CloudFormation stack.

        Enter a value between 7 and 30 days. The default value is 30 days.

        When you remove a replica key from a CloudFormation stack, AWS KMS schedules the replica key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of replica key is ``Pending Deletion`` , which prevents it from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the replica key.

        If the KMS key is a multi-Region primary key with replica keys, the waiting period begins when the last of its replica keys is deleted. Otherwise, the waiting period begins immediately.

        You cannot use a CloudFormation template to cancel deletion of the replica after you remove it from the stack, regardless of the waiting period. However, if you specify a replica key in your template that is based on the same primary key as the original replica key, CloudFormation creates a new replica key with the same key ID, key material, and other shared properties of the original replica key. This new replica key can decrypt ciphertext that was encrypted under the original replica key, or any related multi-Region key.

        For detailed information about deleting multi-Region keys, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* .

        For information about the ``PendingDeletion`` key state, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        *Minimum* : 7

        *Maximum* : 30

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-pendingwindowindays
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pendingWindowInDays"))

    @pending_window_in_days.setter
    def pending_window_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400afa3743909d37c9bd69bb29538ec5fa71aa0142ead25f6b83c035288881d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pendingWindowInDays", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kms.CfnReplicaKeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_policy": "keyPolicy",
        "primary_key_arn": "primaryKeyArn",
        "description": "description",
        "enabled": "enabled",
        "pending_window_in_days": "pendingWindowInDays",
        "tags": "tags",
    },
)
class CfnReplicaKeyProps:
    def __init__(
        self,
        *,
        key_policy: typing.Any,
        primary_key_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnReplicaKey``.

        :param key_policy: The key policy that authorizes use of the replica key. The key policy is not a shared property of multi-Region keys. You can specify the same key policy or a different key policy for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property. The key policy must conform to the following rules. - The key policy must give the caller `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ permission on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** . - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* . A key policy document can include only the following characters: - Printable ASCII characters from the space character ( ``\\ u0020`` ) through the end of the ASCII character range. - Printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ). - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters *Minimum* : ``1`` *Maximum* : ``32768``
        :param primary_key_arn: Specifies the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS partition. You can create only one replica of a given primary key in each AWS Region . .. epigraph:: If you change the ``PrimaryKeyArn`` value of a replica key, the existing replica key is scheduled for deletion and a new replica key is created based on the specified primary key. While it is scheduled for deletion, the existing replica key becomes unusable. You can cancel the scheduled deletion of the key outside of CloudFormation. However, if you inadvertently delete a replica key, you can decrypt ciphertext encrypted by that replica key by using any related multi-Region key. If necessary, you can recreate the replica in the same Region after the previous one is completely deleted. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* Specify the key ARN of an existing multi-Region primary key. For example, ``arn:aws:kms:us-east-2:111122223333:key/mrk-1234abcd12ab34cd56ef1234567890ab`` .
        :param description: A description of the KMS key. The default value is an empty string (no description). The description is not a shared property of multi-Region keys. You can specify the same description or a different description for each key in a set of related multi-Region keys. AWS Key Management Service does not synchronize this property.
        :param enabled: Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` . The actual key state of the replica might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. Also, while the replica key is being created, its key state is ``Creating`` . When the process is complete, the key state of the replica key changes to ``Enabled`` . For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param pending_window_in_days: Specifies the number of days in the waiting period before AWS KMS deletes a replica key that has been removed from a CloudFormation stack. Enter a value between 7 and 30 days. The default value is 30 days. When you remove a replica key from a CloudFormation stack, AWS KMS schedules the replica key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of replica key is ``Pending Deletion`` , which prevents it from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the replica key. If the KMS key is a multi-Region primary key with replica keys, the waiting period begins when the last of its replica keys is deleted. Otherwise, the waiting period begins immediately. You cannot use a CloudFormation template to cancel deletion of the replica after you remove it from the stack, regardless of the waiting period. However, if you specify a replica key in your template that is based on the same primary key as the original replica key, CloudFormation creates a new replica key with the same key ID, key material, and other shared properties of the original replica key. This new replica key can decrypt ciphertext that was encrypted under the original replica key, or any related multi-Region key. For detailed information about deleting multi-Region keys, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* . For information about the ``PendingDeletion`` key state, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* . *Minimum* : 7 *Maximum* : 30
        :param tags: Assigns one or more tags to the replica key. .. epigraph:: Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* . Tags are not a shared property of multi-Region keys. You can specify the same tags or different tags for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property. Each tag consists of a tag key and a tag value. Both the tag key and the tag value are required, but the tag value can be an empty (null) string. You cannot have more than one tag on a KMS key with the same tag key. If you specify an existing tag key with a different tag value, AWS KMS replaces the current tag value with the specified one. When you assign tags to an AWS resource, AWS generates a cost allocation report with usage and costs aggregated by tags. Tags can also be used to control access to a KMS key. For details, see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kms as kms
            
            # key_policy: Any
            
            cfn_replica_key_props = kms.CfnReplicaKeyProps(
                key_policy=key_policy,
                primary_key_arn="primaryKeyArn",
            
                # the properties below are optional
                description="description",
                enabled=False,
                pending_window_in_days=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e01d8fcf994b41906fd812d9cbf6d3591c0133e4be1f531e3ff7e58ea7c8d7b)
            check_type(argname="argument key_policy", value=key_policy, expected_type=type_hints["key_policy"])
            check_type(argname="argument primary_key_arn", value=primary_key_arn, expected_type=type_hints["primary_key_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument pending_window_in_days", value=pending_window_in_days, expected_type=type_hints["pending_window_in_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_policy": key_policy,
            "primary_key_arn": primary_key_arn,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if pending_window_in_days is not None:
            self._values["pending_window_in_days"] = pending_window_in_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def key_policy(self) -> typing.Any:
        '''The key policy that authorizes use of the replica key.

        The key policy is not a shared property of multi-Region keys. You can specify the same key policy or a different key policy for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property.

        The key policy must conform to the following rules.

        - The key policy must give the caller `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ permission on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** .
        - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS KMS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS KMS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* .

        A key policy document can include only the following characters:

        - Printable ASCII characters from the space character ( ``\\ u0020`` ) through the end of the ASCII character range.
        - Printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ).
        - The tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` ) special characters

        *Minimum* : ``1``

        *Maximum* : ``32768``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-keypolicy
        '''
        result = self._values.get("key_policy")
        assert result is not None, "Required property 'key_policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def primary_key_arn(self) -> builtins.str:
        '''Specifies the multi-Region primary key to replicate.

        The primary key must be in a different AWS Region of the same AWS partition. You can create only one replica of a given primary key in each AWS Region .
        .. epigraph::

           If you change the ``PrimaryKeyArn`` value of a replica key, the existing replica key is scheduled for deletion and a new replica key is created based on the specified primary key. While it is scheduled for deletion, the existing replica key becomes unusable. You can cancel the scheduled deletion of the key outside of CloudFormation.

           However, if you inadvertently delete a replica key, you can decrypt ciphertext encrypted by that replica key by using any related multi-Region key. If necessary, you can recreate the replica in the same Region after the previous one is completely deleted. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide*

        Specify the key ARN of an existing multi-Region primary key. For example, ``arn:aws:kms:us-east-2:111122223333:key/mrk-1234abcd12ab34cd56ef1234567890ab`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-primarykeyarn
        '''
        result = self._values.get("primary_key_arn")
        assert result is not None, "Required property 'primary_key_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the KMS key.

        The default value is an empty string (no description).

        The description is not a shared property of multi-Region keys. You can specify the same description or a different description for each key in a set of related multi-Region keys. AWS Key Management Service does not synchronize this property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations.

        When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` .

        The actual key state of the replica might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. Also, while the replica key is being created, its key state is ``Creating`` . When the process is complete, the key state of the replica key changes to ``Enabled`` .

        For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days in the waiting period before AWS KMS deletes a replica key that has been removed from a CloudFormation stack.

        Enter a value between 7 and 30 days. The default value is 30 days.

        When you remove a replica key from a CloudFormation stack, AWS KMS schedules the replica key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of replica key is ``Pending Deletion`` , which prevents it from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the replica key.

        If the KMS key is a multi-Region primary key with replica keys, the waiting period begins when the last of its replica keys is deleted. Otherwise, the waiting period begins immediately.

        You cannot use a CloudFormation template to cancel deletion of the replica after you remove it from the stack, regardless of the waiting period. However, if you specify a replica key in your template that is based on the same primary key as the original replica key, CloudFormation creates a new replica key with the same key ID, key material, and other shared properties of the original replica key. This new replica key can decrypt ciphertext that was encrypted under the original replica key, or any related multi-Region key.

        For detailed information about deleting multi-Region keys, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* .

        For information about the ``PendingDeletion`` key state, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        *Minimum* : 7

        *Maximum* : 30

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-pendingwindowindays
        '''
        result = self._values.get("pending_window_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Assigns one or more tags to the replica key.

        .. epigraph::

           Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS KMS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

        Tags are not a shared property of multi-Region keys. You can specify the same tags or different tags for each key in a set of related multi-Region keys. AWS KMS does not synchronize this property.

        Each tag consists of a tag key and a tag value. Both the tag key and the tag value are required, but the tag value can be an empty (null) string. You cannot have more than one tag on a KMS key with the same tag key. If you specify an existing tag key with a different tag value, AWS KMS replaces the current tag value with the specified one.

        When you assign tags to an AWS resource, AWS generates a cost allocation report with usage and costs aggregated by tags. Tags can also be used to control access to a KMS key. For details, see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicaKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-kms.IKey")
class IKey(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''A KMS Key, either managed by this CDK app, or imported.'''

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        '''The ARN of the key.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        '''The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: builtins.str) -> "Alias":
        '''Defines a new alias for the key.

        :param alias: -
        '''
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult:
        '''Adds a statement to the KMS key resource policy.

        :param statement: The policy statement to add.
        :param allow_no_op: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant the indicated permissions on this key to the given principal.

        :param grantee: -
        :param actions: -
        '''
        ...

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption permissions using this key to the given principal.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption and decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        ...


class _IKeyProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''A KMS Key, either managed by this CDK app, or imported.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-kms.IKey"

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        '''The ARN of the key.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "keyArn"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        '''The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: builtins.str) -> "Alias":
        '''Defines a new alias for the key.

        :param alias: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e79c0a12f3c8bc4b849033fa10a00b4686d559dc2ad534ef985e12b5fbbbc1)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
        return typing.cast("Alias", jsii.invoke(self, "addAlias", [alias]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult:
        '''Adds a statement to the KMS key resource policy.

        :param statement: The policy statement to add.
        :param allow_no_op: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c693b13952d914f59c7b4e984ea15ad05c5c7655d5338deaccd3f602f52bcdb)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument allow_no_op", value=allow_no_op, expected_type=type_hints["allow_no_op"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant the indicated permissions on this key to the given principal.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083f95a4238b4fd800a3ea380800401675361fa9efe42d90f0d313440651145a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6490ca8f5344fbafec2a54b6ec396d67cb8a09bf3cab5ea3cf398da4219c17f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantDecrypt", [grantee]))

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f6a33f953c25f9cfceae42edc91567532c67f4accd2b7c80c513aeda8f23f3)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantEncrypt", [grantee]))

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption and decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4fd9c1824297d0dc29a5298fa810a8d0da08d0bf38ce57891d95e18a667b01)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantEncryptDecrypt", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IKey).__jsii_proxy_class__ = lambda : _IKeyProxy


@jsii.implements(IKey)
class Key(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kms.Key",
):
    '''Defines a KMS key.

    :resource: AWS::KMS::Key
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kms as kms
        
        
        encryption_key = kms.Key(self, "Key",
            enable_key_rotation=True
        )
        table = dynamodb.Table(self, "MyTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,
            encryption_key=encryption_key
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        admins: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IPrincipal]] = None,
        alias: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        key_spec: typing.Optional["KeySpec"] = None,
        key_usage: typing.Optional["KeyUsage"] = None,
        pending_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        policy: typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        trust_account_identities: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param admins: A list of principals to add as key administrators to the key policy. Key administrators have permissions to manage the key (e.g., change permissions, revoke), but do not have permissions to use the key in cryptographic operations (e.g., encrypt, decrypt). These principals will be added to the default key policy (if none specified), or to the specified policy (if provided). Default: []
        :param alias: Initial alias to add to the key. More aliases can be added later by calling ``addAlias``. Default: - No alias is added for the key.
        :param description: A description of the key. Use a description that helps your users decide whether the key is appropriate for a particular task. Default: - No description.
        :param enabled: Indicates whether the key is available for use. Default: - Key is enabled.
        :param enable_key_rotation: Indicates whether AWS KMS rotates the key. Default: false
        :param key_spec: The cryptographic configuration of the key. The valid value depends on usage of the key. IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion and a new key is created with the specified value. Default: KeySpec.SYMMETRIC_DEFAULT
        :param key_usage: The cryptographic operations for which the key can be used. IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion and a new key is created with the specified value. Default: KeyUsage.ENCRYPT_DECRYPT
        :param pending_window: Specifies the number of days in the waiting period before AWS KMS deletes a CMK that has been removed from a CloudFormation stack. When you remove a customer master key (CMK) from a CloudFormation stack, AWS KMS schedules the CMK for deletion and starts the mandatory waiting period. The PendingWindowInDays property determines the length of waiting period. During the waiting period, the key state of CMK is Pending Deletion, which prevents the CMK from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the CMK. Enter a value between 7 and 30 days. Default: - 30 days
        :param policy: Custom policy document to attach to the KMS key. NOTE - If the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set (the default for new projects), this policy will *override* the default key policy and become the only key policy for the key. If the feature flag is not set, this policy will be appended to the default key policy. Default: - A policy document with permissions for the account root to administer the key will be created.
        :param removal_policy: Whether the encryption key should be retained when it is removed from the Stack. This is useful when one wants to retain access to data that was encrypted with a key that is being retired. Default: RemovalPolicy.Retain
        :param trust_account_identities: (deprecated) Whether the key usage can be granted by IAM policies. Setting this to true adds a default statement which delegates key access control completely to the identity's IAM policy (similar to how it works for other AWS resources). This matches the default behavior when creating KMS keys via the API or console. If the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set (the default for new projects), this flag will always be treated as 'true' and does not need to be explicitly set. Default: - false, unless the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c594592899cc30c1c88281346af0a6f62f5b3fd7ecfb54611dfea951d49269b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = KeyProps(
            admins=admins,
            alias=alias,
            description=description,
            enabled=enabled,
            enable_key_rotation=enable_key_rotation,
            key_spec=key_spec,
            key_usage=key_usage,
            pending_window=pending_window,
            policy=policy,
            removal_policy=removal_policy,
            trust_account_identities=trust_account_identities,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCfnKey")
    @builtins.classmethod
    def from_cfn_key(cls, cfn_key: CfnKey) -> IKey:
        '''Create a mutable {@link IKey} based on a low-level {@link CfnKey}.

        This is most useful when combined with the cloudformation-include module.
        This method is different than {@link fromKeyArn()} because the {@link IKey}
        returned from this method is mutable;
        meaning, calling any mutating methods on it,
        like {@link IKey.addToResourcePolicy()},
        will actually be reflected in the resulting template,
        as opposed to the object returned from {@link fromKeyArn()},
        on which calling those methods would have no effect.

        :param cfn_key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8203ae5cd13dd08fbbe6efbd4a005523ac1aba62a73c3aed7afb07cff08f9354)
            check_type(argname="argument cfn_key", value=cfn_key, expected_type=type_hints["cfn_key"])
        return typing.cast(IKey, jsii.sinvoke(cls, "fromCfnKey", [cfn_key]))

    @jsii.member(jsii_name="fromKeyArn")
    @builtins.classmethod
    def from_key_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        key_arn: builtins.str,
    ) -> IKey:
        '''Import an externally defined KMS Key using its ARN.

        :param scope: the construct that will "own" the imported key.
        :param id: the id of the imported key in the construct tree.
        :param key_arn: the ARN of an existing KMS key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bad9c0af7854304235dc8fcf752e304ae3ff4f57029817e364afe6477025d2e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
        return typing.cast(IKey, jsii.sinvoke(cls, "fromKeyArn", [scope, id, key_arn]))

    @jsii.member(jsii_name="fromLookup")
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias_name: builtins.str,
    ) -> IKey:
        '''Import an existing Key by querying the AWS environment this stack is deployed to.

        This function only needs to be used to use Keys not defined in your CDK
        application. If you are looking to share a Key between stacks, you can
        pass the ``Key`` object between stacks and use it as normal. In addition,
        it's not necessary to use this method if an interface accepts an ``IKey``.
        In this case, ``Alias.fromAliasName()`` can be used which returns an alias
        that extends ``IKey``.

        Calling this method will lead to a lookup when the CDK CLI is executed.
        You can therefore not use any values that will only be available at
        CloudFormation execution time (i.e., Tokens).

        The Key information will be cached in ``cdk.context.json`` and the same Key
        will be used on future runs. To refresh the lookup, you will have to
        evict the value from the cache using the ``cdk context`` command. See
        https://docs.aws.amazon.com/cdk/latest/guide/context.html for more information.

        :param scope: -
        :param id: -
        :param alias_name: The alias name of the Key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9047f404e4d7db0203c914cde1b7eb5511b7e96879c78b79bbf90acf11bb472)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = KeyLookupOptions(alias_name=alias_name)

        return typing.cast(IKey, jsii.sinvoke(cls, "fromLookup", [scope, id, options]))

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias_name: builtins.str) -> "Alias":
        '''Defines a new alias for the key.

        :param alias_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42fc6275ae752b03595fc9cb82497bbba1b1e16d806cd57a5553e3e367a3045)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
        return typing.cast("Alias", jsii.invoke(self, "addAlias", [alias_name]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult:
        '''Adds a statement to the KMS key resource policy.

        :param statement: The policy statement to add.
        :param allow_no_op: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7ad6910fcfe2809d1bd30420180f14e02e86f06d469b8049d172ac34be4b66)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument allow_no_op", value=allow_no_op, expected_type=type_hints["allow_no_op"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant the indicated permissions on this key to the given principal.

        This modifies both the principal's policy as well as the resource policy,
        since the default CloudFormation setup for KMS keys is that the policy
        must not be empty and so default grants won't work.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ad1d45e372c043b927509a9350f0480be52db0d006f1673515af92837334df)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantAdmin")
    def grant_admin(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant admins permissions using this key to the given principal.

        Key administrators have permissions to manage the key (e.g., change permissions, revoke), but do not have permissions
        to use the key in cryptographic operations (e.g., encrypt, decrypt).

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99b292abb55ef0c0c654b346c6d7b474f62397849f75c9e30a7ccebb30d03aa)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantAdmin", [grantee]))

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d1e2ce2bddfc1589ef69e0c7bc22b99be247366a62a58f9a693bcecfb6af69)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantDecrypt", [grantee]))

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40842dc0148dc825fd9f202584cc24f67ff77e0da95ed1aee38982db8513ae3d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantEncrypt", [grantee]))

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption and decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68af90ea452ab003f02f5ace08cd7fd3a4f72867a2a46c567d0a0b0e4aff47e8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantEncryptDecrypt", [grantee]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        '''The ARN of the key.'''
        return typing.cast(builtins.str, jsii.get(self, "keyArn"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        '''The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).'''
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @builtins.property
    @jsii.member(jsii_name="trustAccountIdentities")
    def _trust_account_identities(self) -> builtins.bool:
        '''Optional property to control trusting account identities.

        If specified, grants will default identity policies instead of to both
        resource and identity policies. This matches the default behavior when creating
        KMS keys via the API or console.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "trustAccountIdentities"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def _policy(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument]:
        '''Optional policy document that represents the resource policy of this key.

        If specified, addToResourcePolicy can be used to edit this policy.
        Otherwise this method will no-op.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument], jsii.get(self, "policy"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kms.KeyLookupOptions",
    jsii_struct_bases=[],
    name_mapping={"alias_name": "aliasName"},
)
class KeyLookupOptions:
    def __init__(self, *, alias_name: builtins.str) -> None:
        '''Properties for looking up an existing Key.

        :param alias_name: The alias name of the Key.

        :exampleMetadata: infused

        Example::

            my_key_lookup = kms.Key.from_lookup(self, "MyKeyLookup",
                alias_name="alias/KeyAlias"
            )
            
            role = iam.Role(self, "MyRole",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
            )
            my_key_lookup.grant_encrypt_decrypt(role)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52d4cc596f85628ed6f77ed90b11b1657f8174f32376e5217f6a571a5caaf22)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias_name": alias_name,
        }

    @builtins.property
    def alias_name(self) -> builtins.str:
        '''The alias name of the Key.'''
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kms.KeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "admins": "admins",
        "alias": "alias",
        "description": "description",
        "enabled": "enabled",
        "enable_key_rotation": "enableKeyRotation",
        "key_spec": "keySpec",
        "key_usage": "keyUsage",
        "pending_window": "pendingWindow",
        "policy": "policy",
        "removal_policy": "removalPolicy",
        "trust_account_identities": "trustAccountIdentities",
    },
)
class KeyProps:
    def __init__(
        self,
        *,
        admins: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IPrincipal]] = None,
        alias: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        key_spec: typing.Optional["KeySpec"] = None,
        key_usage: typing.Optional["KeyUsage"] = None,
        pending_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        policy: typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument] = None,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
        trust_account_identities: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Construction properties for a KMS Key object.

        :param admins: A list of principals to add as key administrators to the key policy. Key administrators have permissions to manage the key (e.g., change permissions, revoke), but do not have permissions to use the key in cryptographic operations (e.g., encrypt, decrypt). These principals will be added to the default key policy (if none specified), or to the specified policy (if provided). Default: []
        :param alias: Initial alias to add to the key. More aliases can be added later by calling ``addAlias``. Default: - No alias is added for the key.
        :param description: A description of the key. Use a description that helps your users decide whether the key is appropriate for a particular task. Default: - No description.
        :param enabled: Indicates whether the key is available for use. Default: - Key is enabled.
        :param enable_key_rotation: Indicates whether AWS KMS rotates the key. Default: false
        :param key_spec: The cryptographic configuration of the key. The valid value depends on usage of the key. IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion and a new key is created with the specified value. Default: KeySpec.SYMMETRIC_DEFAULT
        :param key_usage: The cryptographic operations for which the key can be used. IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion and a new key is created with the specified value. Default: KeyUsage.ENCRYPT_DECRYPT
        :param pending_window: Specifies the number of days in the waiting period before AWS KMS deletes a CMK that has been removed from a CloudFormation stack. When you remove a customer master key (CMK) from a CloudFormation stack, AWS KMS schedules the CMK for deletion and starts the mandatory waiting period. The PendingWindowInDays property determines the length of waiting period. During the waiting period, the key state of CMK is Pending Deletion, which prevents the CMK from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the CMK. Enter a value between 7 and 30 days. Default: - 30 days
        :param policy: Custom policy document to attach to the KMS key. NOTE - If the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set (the default for new projects), this policy will *override* the default key policy and become the only key policy for the key. If the feature flag is not set, this policy will be appended to the default key policy. Default: - A policy document with permissions for the account root to administer the key will be created.
        :param removal_policy: Whether the encryption key should be retained when it is removed from the Stack. This is useful when one wants to retain access to data that was encrypted with a key that is being retired. Default: RemovalPolicy.Retain
        :param trust_account_identities: (deprecated) Whether the key usage can be granted by IAM policies. Setting this to true adds a default statement which delegates key access control completely to the identity's IAM policy (similar to how it works for other AWS resources). This matches the default behavior when creating KMS keys via the API or console. If the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set (the default for new projects), this flag will always be treated as 'true' and does not need to be explicitly set. Default: - false, unless the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set.

        :exampleMetadata: infused

        Example::

            my_trusted_admin_role = iam.Role.from_role_arn(self, "TrustedRole", "arn:aws:iam:....")
            # Creates a limited admin policy and assigns to the account root.
            my_custom_policy = iam.PolicyDocument(
                statements=[iam.PolicyStatement(
                    actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"
                    ],
                    principals=[iam.AccountRootPrincipal()],
                    resources=["*"]
                )]
            )
            key = kms.Key(self, "MyKey",
                policy=my_custom_policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c163d819b5cd58ad2a4f60159367a72483c4f45b6f8ee06f2f412d6f2e52f9d)
            check_type(argname="argument admins", value=admins, expected_type=type_hints["admins"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_key_rotation", value=enable_key_rotation, expected_type=type_hints["enable_key_rotation"])
            check_type(argname="argument key_spec", value=key_spec, expected_type=type_hints["key_spec"])
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument pending_window", value=pending_window, expected_type=type_hints["pending_window"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument trust_account_identities", value=trust_account_identities, expected_type=type_hints["trust_account_identities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admins is not None:
            self._values["admins"] = admins
        if alias is not None:
            self._values["alias"] = alias
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if key_spec is not None:
            self._values["key_spec"] = key_spec
        if key_usage is not None:
            self._values["key_usage"] = key_usage
        if pending_window is not None:
            self._values["pending_window"] = pending_window
        if policy is not None:
            self._values["policy"] = policy
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if trust_account_identities is not None:
            self._values["trust_account_identities"] = trust_account_identities

    @builtins.property
    def admins(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.IPrincipal]]:
        '''A list of principals to add as key administrators to the key policy.

        Key administrators have permissions to manage the key (e.g., change permissions, revoke), but do not have permissions
        to use the key in cryptographic operations (e.g., encrypt, decrypt).

        These principals will be added to the default key policy (if none specified), or to the specified policy (if provided).

        :default: []
        '''
        result = self._values.get("admins")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.IPrincipal]], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Initial alias to add to the key.

        More aliases can be added later by calling ``addAlias``.

        :default: - No alias is added for the key.
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the key.

        Use a description that helps your users decide
        whether the key is appropriate for a particular task.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the key is available for use.

        :default: - Key is enabled.
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_key_rotation(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether AWS KMS rotates the key.

        :default: false
        '''
        result = self._values.get("enable_key_rotation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_spec(self) -> typing.Optional["KeySpec"]:
        '''The cryptographic configuration of the key. The valid value depends on usage of the key.

        IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion
        and a new key is created with the specified value.

        :default: KeySpec.SYMMETRIC_DEFAULT
        '''
        result = self._values.get("key_spec")
        return typing.cast(typing.Optional["KeySpec"], result)

    @builtins.property
    def key_usage(self) -> typing.Optional["KeyUsage"]:
        '''The cryptographic operations for which the key can be used.

        IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion
        and a new key is created with the specified value.

        :default: KeyUsage.ENCRYPT_DECRYPT
        '''
        result = self._values.get("key_usage")
        return typing.cast(typing.Optional["KeyUsage"], result)

    @builtins.property
    def pending_window(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''Specifies the number of days in the waiting period before AWS KMS deletes a CMK that has been removed from a CloudFormation stack.

        When you remove a customer master key (CMK) from a CloudFormation stack, AWS KMS schedules the CMK for deletion
        and starts the mandatory waiting period. The PendingWindowInDays property determines the length of waiting period.
        During the waiting period, the key state of CMK is Pending Deletion, which prevents the CMK from being used in
        cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the CMK.

        Enter a value between 7 and 30 days.

        :default: - 30 days

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-pendingwindowindays
        '''
        result = self._values.get("pending_window")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def policy(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument]:
        '''Custom policy document to attach to the KMS key.

        NOTE - If the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set (the default for new projects),
        this policy will *override* the default key policy and become the only key policy for the key. If the
        feature flag is not set, this policy will be appended to the default key policy.

        :default:

        - A policy document with permissions for the account root to
        administer the key will be created.
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy]:
        '''Whether the encryption key should be retained when it is removed from the Stack.

        This is useful when one wants to
        retain access to data that was encrypted with a key that is being retired.

        :default: RemovalPolicy.Retain
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy], result)

    @builtins.property
    def trust_account_identities(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether the key usage can be granted by IAM policies.

        Setting this to true adds a default statement which delegates key
        access control completely to the identity's IAM policy (similar
        to how it works for other AWS resources). This matches the default behavior
        when creating KMS keys via the API or console.

        If the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set (the default for new projects),
        this flag will always be treated as 'true' and does not need to be explicitly set.

        :default: - false, unless the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set.

        :deprecated: redundant with the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag

        :see: https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam
        :stability: deprecated
        '''
        result = self._values.get("trust_account_identities")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-kms.KeySpec")
class KeySpec(enum.Enum):
    '''The key spec, represents the cryptographic configuration of keys.

    :exampleMetadata: infused

    Example::

        key = kms.Key(self, "MyKey",
            key_spec=kms.KeySpec.ECC_SECG_P256K1,  # Default to SYMMETRIC_DEFAULT
            key_usage=kms.KeyUsage.SIGN_VERIFY
        )
    '''

    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    '''The default key spec.

    Valid usage: ENCRYPT_DECRYPT
    '''
    RSA_2048 = "RSA_2048"
    '''RSA with 2048 bits of key.

    Valid usage: ENCRYPT_DECRYPT and SIGN_VERIFY
    '''
    RSA_3072 = "RSA_3072"
    '''RSA with 3072 bits of key.

    Valid usage: ENCRYPT_DECRYPT and SIGN_VERIFY
    '''
    RSA_4096 = "RSA_4096"
    '''RSA with 4096 bits of key.

    Valid usage: ENCRYPT_DECRYPT and SIGN_VERIFY
    '''
    ECC_NIST_P256 = "ECC_NIST_P256"
    '''NIST FIPS 186-4, Section 6.4, ECDSA signature using the curve specified by the key and SHA-256 for the message digest.

    Valid usage: SIGN_VERIFY
    '''
    ECC_NIST_P384 = "ECC_NIST_P384"
    '''NIST FIPS 186-4, Section 6.4, ECDSA signature using the curve specified by the key and SHA-384 for the message digest.

    Valid usage: SIGN_VERIFY
    '''
    ECC_NIST_P521 = "ECC_NIST_P521"
    '''NIST FIPS 186-4, Section 6.4, ECDSA signature using the curve specified by the key and SHA-512 for the message digest.

    Valid usage: SIGN_VERIFY
    '''
    ECC_SECG_P256K1 = "ECC_SECG_P256K1"
    '''Standards for Efficient Cryptography 2, Section 2.4.1, ECDSA signature on the Koblitz curve.

    Valid usage: SIGN_VERIFY
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-kms.KeyUsage")
class KeyUsage(enum.Enum):
    '''The key usage, represents the cryptographic operations of keys.

    :exampleMetadata: infused

    Example::

        key = kms.Key(self, "MyKey",
            key_spec=kms.KeySpec.ECC_SECG_P256K1,  # Default to SYMMETRIC_DEFAULT
            key_usage=kms.KeyUsage.SIGN_VERIFY
        )
    '''

    ENCRYPT_DECRYPT = "ENCRYPT_DECRYPT"
    '''Encryption and decryption.'''
    SIGN_VERIFY = "SIGN_VERIFY"
    '''Signing and verification.'''


class ViaServicePrincipal(
    _aws_cdk_aws_iam_940a1ce0.PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kms.ViaServicePrincipal",
):
    '''A principal to allow access to a key if it's being used through another AWS service.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_kms as kms
        
        # principal: iam.IPrincipal
        
        via_service_principal = kms.ViaServicePrincipal("serviceName", principal)
    '''

    def __init__(
        self,
        service_name: builtins.str,
        base_principal: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IPrincipal] = None,
    ) -> None:
        '''
        :param service_name: -
        :param base_principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9a0608c88a27ae09bed8fa12c45703958eb84796d767ac00066a1fa9180249)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument base_principal", value=base_principal, expected_type=type_hints["base_principal"])
        jsii.create(self.__class__, self, [service_name, base_principal])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> _aws_cdk_aws_iam_940a1ce0.PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.interface(jsii_type="@aws-cdk/aws-kms.IAlias")
class IAlias(IKey, typing_extensions.Protocol):
    '''A KMS Key alias.

    An alias can be used in all places that expect a key.
    '''

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        '''The name of the alias.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="aliasTargetKey")
    def alias_target_key(self) -> IKey:
        '''The Key to which the Alias refers.

        :attribute: true
        '''
        ...


class _IAliasProxy(
    jsii.proxy_for(IKey), # type: ignore[misc]
):
    '''A KMS Key alias.

    An alias can be used in all places that expect a key.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-kms.IAlias"

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        '''The name of the alias.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasName"))

    @builtins.property
    @jsii.member(jsii_name="aliasTargetKey")
    def alias_target_key(self) -> IKey:
        '''The Key to which the Alias refers.

        :attribute: true
        '''
        return typing.cast(IKey, jsii.get(self, "aliasTargetKey"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAlias).__jsii_proxy_class__ = lambda : _IAliasProxy


@jsii.implements(IAlias)
class Alias(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kms.Alias",
):
    '''Defines a display name for a customer master key (CMK) in AWS Key Management Service (AWS KMS).

    Using an alias to refer to a key can help you simplify key
    management. For example, when rotating keys, you can just update the alias
    mapping instead of tracking and changing key IDs. For more information, see
    Working with Aliases in the AWS Key Management Service Developer Guide.

    You can also add an alias for a key by calling ``key.addAlias(alias)``.

    :resource: AWS::KMS::Alias
    :exampleMetadata: infused

    Example::

        # Passing an encrypted replication bucket created in a different stack.
        app = App()
        replication_stack = Stack(app, "ReplicationStack",
            env=Environment(
                region="us-west-1"
            )
        )
        key = kms.Key(replication_stack, "ReplicationKey")
        alias = kms.Alias(replication_stack, "ReplicationAlias",
            # aliasName is required
            alias_name=PhysicalName.GENERATE_IF_NEEDED,
            target_key=key
        )
        replication_bucket = s3.Bucket(replication_stack, "ReplicationBucket",
            bucket_name=PhysicalName.GENERATE_IF_NEEDED,
            encryption_key=alias
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias_name: builtins.str,
        target_key: IKey,
        removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alias_name: The name of the alias. The name must start with alias followed by a forward slash, such as alias/. You can't specify aliases that begin with alias/AWS. These aliases are reserved.
        :param target_key: The ID of the key for which you are creating the alias. Specify the key's globally unique identifier or Amazon Resource Name (ARN). You can't specify another alias.
        :param removal_policy: Policy to apply when the alias is removed from this stack. Default: - The alias will be deleted
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd67e1e19cb5d168beb8d885babc0a1cd20860491dde39b1f0d8c4545fb7343c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AliasProps(
            alias_name=alias_name, target_key=target_key, removal_policy=removal_policy
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAliasAttributes")
    @builtins.classmethod
    def from_alias_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias_name: builtins.str,
        alias_target_key: IKey,
    ) -> IAlias:
        '''Import an existing KMS Alias defined outside the CDK app.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param alias_name: Specifies the alias name. This value must begin with alias/ followed by a name (i.e. alias/ExampleAlias)
        :param alias_target_key: The customer master key (CMK) to which the Alias refers.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c3a3d39d50e599fc4dad9a80f936b19f5d529f783f1d41cde61f8e5172e876)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AliasAttributes(
            alias_name=alias_name, alias_target_key=alias_target_key
        )

        return typing.cast(IAlias, jsii.sinvoke(cls, "fromAliasAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromAliasName")
    @builtins.classmethod
    def from_alias_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        alias_name: builtins.str,
    ) -> IAlias:
        '''Import an existing KMS Alias defined outside the CDK app, by the alias name.

        This method should be used
        instead of 'fromAliasAttributes' when the underlying KMS Key ARN is not available.
        This Alias will not have a direct reference to the KMS Key, so addAlias and grant* methods are not supported.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param alias_name: The full name of the KMS Alias (e.g., 'alias/aws/s3', 'alias/myKeyAlias').
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39bc6ed3ffeabf44763c7993639690ae9a877935f4cac8f3be75c5e2c3924172)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
        return typing.cast(IAlias, jsii.sinvoke(cls, "fromAliasName", [scope, id, alias_name]))

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: builtins.str) -> "Alias":
        '''Defines a new alias for the key.

        :param alias: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfda00a5b1acee1b748a3781d50a091ace3050506cb0c6fc0dacc14491be845)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
        return typing.cast("Alias", jsii.invoke(self, "addAlias", [alias]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult:
        '''Adds a statement to the KMS key resource policy.

        :param statement: -
        :param allow_no_op: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264270d7892b3969bf3351ade9fab3adf71485acc3a57b4b1901961b12495dd4)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument allow_no_op", value=allow_no_op, expected_type=type_hints["allow_no_op"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op]))

    @jsii.member(jsii_name="generatePhysicalName")
    def _generate_physical_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "generatePhysicalName", []))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant the indicated permissions on this key to the given principal.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ae397ef91c0dc92995f296da31c56959b85a88cc43bb8a4ad511c9a6c40568)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48265d0e31dbe79e10c22f8742d710a3a63954f901fe71ef2f531681970389a7)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantDecrypt", [grantee]))

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65870cba3ea8cae9d5534c9385b0b508d0a132540aa511f25d514ff650c23033)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantEncrypt", [grantee]))

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant encryption and decryption permissions using this key to the given principal.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73df55accdf22c822949dbe3b21d485974642df4900c2a647d0a585c391538d6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantEncryptDecrypt", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        '''The name of the alias.'''
        return typing.cast(builtins.str, jsii.get(self, "aliasName"))

    @builtins.property
    @jsii.member(jsii_name="aliasTargetKey")
    def alias_target_key(self) -> IKey:
        '''The Key to which the Alias refers.'''
        return typing.cast(IKey, jsii.get(self, "aliasTargetKey"))

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        '''The ARN of the key.'''
        return typing.cast(builtins.str, jsii.get(self, "keyArn"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        '''The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).'''
        return typing.cast(builtins.str, jsii.get(self, "keyId"))


__all__ = [
    "Alias",
    "AliasAttributes",
    "AliasProps",
    "CfnAlias",
    "CfnAliasProps",
    "CfnKey",
    "CfnKeyProps",
    "CfnReplicaKey",
    "CfnReplicaKeyProps",
    "IAlias",
    "IKey",
    "Key",
    "KeyLookupOptions",
    "KeyProps",
    "KeySpec",
    "KeyUsage",
    "ViaServicePrincipal",
]

publication.publish()

def _typecheckingstub__c0c13509115e8e038e4a6043370ce6a5eb2b93eba5b1b5538796ee22807fb583(
    *,
    alias_name: builtins.str,
    alias_target_key: IKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7824789d4cf44e9bafbc9a7476170cc5f519640586a0b00cd8b9ffbbaf5e9f6e(
    *,
    alias_name: builtins.str,
    target_key: IKey,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b506a20a6c6dcd3b6af210b0c2535764c1f6210a5ed41f6db31cc9ddec99e289(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    alias_name: builtins.str,
    target_key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a592c037d8cf5eb56c8fbf2b691ca4ba6008a15e5c0628873ca76a825d54fcd0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b872b0a20a288c78b83081f7d8733f0ee43adbb75f68a6c498b7add2462307(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33ee5bcef3759ff22cff5f4be978d2a088882867fa9cf74d62337691c36c2e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030b0e4dce674403221f238f73863580de9fd10d8a85e65a616a2a6ba9299dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce24a029d04af8248ff498fbc64461d0b4d893863192fde8ae2ad6ac5b65caf(
    *,
    alias_name: builtins.str,
    target_key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7248794f26bf3b6b81f243e562390e80b7bf8b4657642b6c34d4a7b5d42f14cb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    key_policy: typing.Any,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_spec: typing.Optional[builtins.str] = None,
    key_usage: typing.Optional[builtins.str] = None,
    multi_region: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    pending_window_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df25b32bf80c52cef333a35d995fcf119908173afbaaa7838921132a08df046b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decb5c9c70ebbad64089e7c02072be8f7bd6a219afd4f24657c741136919d93c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aab3e6a664f52f5a9c3f11fbe682b21c6adbbb42a0e440386c5131eda41617f(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ae4d149404f325c7c27063006a5aa5688da81cdf2ce84169936eef1628a7d2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d3957bf573a963dba6c5abbb62621f6444da0980daa1486044a23b2dc296c6(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1211b35e1c49b2d1b30c778c5cfb39a7e336f92ef75769b665aefcb9823e97(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a571c78fe90c983ca56d63153d8a623f8c3d53e987b4619ba04c569ff50d8ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a728f5df84657fe9dc3f214a7418b430bd406e3fa794e860ae76b9a11999d1c9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4c3fe229901d0296615ebba2ffb43424aa2f5e25550028fe4dd6accabbcf40(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7032cf4f218f41bb90deea579df2d188d5a625355193dfb17b2f5a1411b9c5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16d036cc4e7e4855c8824e44f7c62a103452211e66c359b4c19e16f5ed47abf(
    *,
    key_policy: typing.Any,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_spec: typing.Optional[builtins.str] = None,
    key_usage: typing.Optional[builtins.str] = None,
    multi_region: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    pending_window_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d559427e1d7884de953e4026fc80eb13cfc39d05aad8e903fd1f946a17a5da2c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    key_policy: typing.Any,
    primary_key_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    pending_window_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dd7d5ae6612915dcecdc900a84c16ae34cd746cb3526b91a755ea450a34a28(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b165feb645cb87d0d563cdb5bb805ada5fc4eec0ecdac8dbf71b7f2591f17d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a9ff41f934a1a642ef2128eadf89099f2a76ac59fb21d89ec3bbd2106d7660(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551ff52f760067b3c65e675f5671f4f2771e11e9e8a5749287e6012a5073a3ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1286c5b360d6530edb9610619a9669208251831b0deb87e68bb3e965c1fe59(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc85df26c8a13553d5d476d44148176f759db9348941b186aed2444fc263e63(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400afa3743909d37c9bd69bb29538ec5fa71aa0142ead25f6b83c035288881d5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e01d8fcf994b41906fd812d9cbf6d3591c0133e4be1f531e3ff7e58ea7c8d7b(
    *,
    key_policy: typing.Any,
    primary_key_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    pending_window_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e79c0a12f3c8bc4b849033fa10a00b4686d559dc2ad534ef985e12b5fbbbc1(
    alias: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c693b13952d914f59c7b4e984ea15ad05c5c7655d5338deaccd3f602f52bcdb(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    allow_no_op: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083f95a4238b4fd800a3ea380800401675361fa9efe42d90f0d313440651145a(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6490ca8f5344fbafec2a54b6ec396d67cb8a09bf3cab5ea3cf398da4219c17f(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f6a33f953c25f9cfceae42edc91567532c67f4accd2b7c80c513aeda8f23f3(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4fd9c1824297d0dc29a5298fa810a8d0da08d0bf38ce57891d95e18a667b01(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c594592899cc30c1c88281346af0a6f62f5b3fd7ecfb54611dfea951d49269b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    admins: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IPrincipal]] = None,
    alias: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    key_spec: typing.Optional[KeySpec] = None,
    key_usage: typing.Optional[KeyUsage] = None,
    pending_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    policy: typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    trust_account_identities: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8203ae5cd13dd08fbbe6efbd4a005523ac1aba62a73c3aed7afb07cff08f9354(
    cfn_key: CfnKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bad9c0af7854304235dc8fcf752e304ae3ff4f57029817e364afe6477025d2e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9047f404e4d7db0203c914cde1b7eb5511b7e96879c78b79bbf90acf11bb472(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42fc6275ae752b03595fc9cb82497bbba1b1e16d806cd57a5553e3e367a3045(
    alias_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7ad6910fcfe2809d1bd30420180f14e02e86f06d469b8049d172ac34be4b66(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    allow_no_op: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ad1d45e372c043b927509a9350f0480be52db0d006f1673515af92837334df(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99b292abb55ef0c0c654b346c6d7b474f62397849f75c9e30a7ccebb30d03aa(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d1e2ce2bddfc1589ef69e0c7bc22b99be247366a62a58f9a693bcecfb6af69(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40842dc0148dc825fd9f202584cc24f67ff77e0da95ed1aee38982db8513ae3d(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68af90ea452ab003f02f5ace08cd7fd3a4f72867a2a46c567d0a0b0e4aff47e8(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52d4cc596f85628ed6f77ed90b11b1657f8174f32376e5217f6a571a5caaf22(
    *,
    alias_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c163d819b5cd58ad2a4f60159367a72483c4f45b6f8ee06f2f412d6f2e52f9d(
    *,
    admins: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IPrincipal]] = None,
    alias: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    key_spec: typing.Optional[KeySpec] = None,
    key_usage: typing.Optional[KeyUsage] = None,
    pending_window: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    policy: typing.Optional[_aws_cdk_aws_iam_940a1ce0.PolicyDocument] = None,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
    trust_account_identities: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9a0608c88a27ae09bed8fa12c45703958eb84796d767ac00066a1fa9180249(
    service_name: builtins.str,
    base_principal: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IPrincipal] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd67e1e19cb5d168beb8d885babc0a1cd20860491dde39b1f0d8c4545fb7343c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias_name: builtins.str,
    target_key: IKey,
    removal_policy: typing.Optional[_aws_cdk_core_f4b25747.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c3a3d39d50e599fc4dad9a80f936b19f5d529f783f1d41cde61f8e5172e876(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias_name: builtins.str,
    alias_target_key: IKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bc6ed3ffeabf44763c7993639690ae9a877935f4cac8f3be75c5e2c3924172(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    alias_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfda00a5b1acee1b748a3781d50a091ace3050506cb0c6fc0dacc14491be845(
    alias: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264270d7892b3969bf3351ade9fab3adf71485acc3a57b4b1901961b12495dd4(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    allow_no_op: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ae397ef91c0dc92995f296da31c56959b85a88cc43bb8a4ad511c9a6c40568(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48265d0e31dbe79e10c22f8742d710a3a63954f901fe71ef2f531681970389a7(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65870cba3ea8cae9d5534c9385b0b508d0a132540aa511f25d514ff650c23033(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73df55accdf22c822949dbe3b21d485974642df4900c2a647d0a585c391538d6(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass
