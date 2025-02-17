'''
# AWS Identity and Access Management Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

Define a role and add permissions to it. This will automatically create and
attach an IAM policy to the role:

```python
role = Role(self, "MyRole",
    assumed_by=ServicePrincipal("sns.amazonaws.com")
)

role.add_to_policy(PolicyStatement(
    resources=["*"],
    actions=["lambda:InvokeFunction"]
))
```

Define a policy and attach it to groups, users and roles. Note that it is possible to attach
the policy either by calling `xxx.attachInlinePolicy(policy)` or `policy.attachToXxx(xxx)`.

```python
user = User(self, "MyUser", password=cdk.SecretValue.unsafe_plain_text("1234"))
group = Group(self, "MyGroup")

policy = Policy(self, "MyPolicy")
policy.attach_to_user(user)
group.attach_inline_policy(policy)
```

Managed policies can be attached using `xxx.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))`:

```python
group = Group(self, "MyGroup")
group.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
```

## Granting permissions to resources

Many of the AWS CDK resources have `grant*` methods that allow you to grant other resources access to that resource. As an example, the following code gives a Lambda function write permissions (Put, Update, Delete) to a DynamoDB table.

```python
# fn: lambda.Function
# table: dynamodb.Table


table.grant_write_data(fn)
```

The more generic `grant` method allows you to give specific permissions to a resource:

```python
# fn: lambda.Function
# table: dynamodb.Table


table.grant(fn, "dynamodb:PutItem")
```

The `grant*` methods accept an `IGrantable` object. This interface is implemented by IAM principlal resources (groups, users and roles) and resources that assume a role such as a Lambda function, EC2 instance or a Codebuild project.

You can find which `grant*` methods exist for a resource in the [AWS CDK API Reference](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html).

## Roles

Many AWS resources require *Roles* to operate. These Roles define the AWS API
calls an instance or other AWS service is allowed to make.

Creating Roles and populating them with the right permissions *Statements* is
a necessary but tedious part of setting up AWS infrastructure. In order to
help you focus on your business logic, CDK will take care of creating
roles and populating them with least-privilege permissions automatically.

All constructs that require Roles will create one for you if don't specify
one at construction time. Permissions will be added to that role
automatically if you associate the construct with other constructs from the
AWS Construct Library (for example, if you tell an *AWS CodePipeline* to trigger
an *AWS Lambda Function*, the Pipeline's Role will automatically get
`lambda:InvokeFunction` permissions on that particular Lambda Function),
or if you explicitly grant permissions using `grant` functions (see the
previous section).

### Opting out of automatic permissions management

You may prefer to manage a Role's permissions yourself instead of having the
CDK automatically manage them for you. This may happen in one of the
following cases:

* You don't like the permissions that CDK automatically generates and
  want to substitute your own set.
* The least-permissions policy that the CDK generates is becoming too
  big for IAM to store, and you need to add some wildcards to keep the
  policy size down.

To prevent constructs from updating your Role's policy, pass the object
returned by `myRole.withoutPolicyUpdates()` instead of `myRole` itself.

For example, to have an AWS CodePipeline *not* automatically add the required
permissions to trigger the expected targets, do the following:

```python
role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
    # custom description if desired
    description="This is a custom role..."
)

codepipeline.Pipeline(self, "Pipeline",
    # Give the Pipeline an immutable view of the Role
    role=role.without_policy_updates()
)

# You now have to manage the Role policies yourself
role.add_to_policy(iam.PolicyStatement(
    actions=[],
    resources=[]
))
```

### Using existing roles

If there are Roles in your account that have already been created which you
would like to use in your CDK application, you can use `Role.fromRoleArn` to
import them, as follows:

```python
role = iam.Role.from_role_arn(self, "Role", "arn:aws:iam::123456789012:role/MyExistingRole",
    # Set 'mutable' to 'false' to use the role as-is and prevent adding new
    # policies to it. The default is 'true', which means the role may be
    # modified as part of the deployment.
    mutable=False
)
```

## Configuring an ExternalId

If you need to create Roles that will be assumed by third parties, it is generally a good idea to [require an `ExternalId`
to assume them](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).  Configuring
an `ExternalId` works like this:

```python
role = iam.Role(self, "MyRole",
    assumed_by=iam.AccountPrincipal("123456789012"),
    external_ids=["SUPPLY-ME"]
)
```

## Principals vs Identities

When we say *Principal*, we mean an entity you grant permissions to. This
entity can be an AWS Service, a Role, or something more abstract such as "all
users in this account" or even "all users in this organization". An
*Identity* is an IAM representing a single IAM entity that can have
a policy attached, one of `Role`, `User`, or `Group`.

## IAM Principals

When defining policy statements as part of an AssumeRole policy or as part of a
resource policy, statements would usually refer to a specific IAM principal
under `Principal`.

IAM principals are modeled as classes that derive from the `iam.PolicyPrincipal`
abstract class. Principal objects include principal type (string) and value
(array of string), optional set of conditions and the action that this principal
requires when it is used in an assume role policy document.

To add a principal to a policy statement you can either use the abstract
`statement.addPrincipal`, one of the concrete `addXxxPrincipal` methods:

* `addAwsPrincipal`, `addArnPrincipal` or `new ArnPrincipal(arn)` for `{ "AWS": arn }`
* `addAwsAccountPrincipal` or `new AccountPrincipal(accountId)` for `{ "AWS": account-arn }`
* `addServicePrincipal` or `new ServicePrincipal(service)` for `{ "Service": service }`
* `addAccountRootPrincipal` or `new AccountRootPrincipal()` for `{ "AWS": { "Ref: "AWS::AccountId" } }`
* `addCanonicalUserPrincipal` or `new CanonicalUserPrincipal(id)` for `{ "CanonicalUser": id }`
* `addFederatedPrincipal` or `new FederatedPrincipal(federated, conditions, assumeAction)` for
  `{ "Federated": arn }` and a set of optional conditions and the assume role action to use.
* `addAnyPrincipal` or `new AnyPrincipal` for `{ "AWS": "*" }`

If multiple principals are added to the policy statement, they will be merged together:

```python
statement = iam.PolicyStatement()
statement.add_service_principal("cloudwatch.amazonaws.com")
statement.add_service_principal("ec2.amazonaws.com")
statement.add_arn_principal("arn:aws:boom:boom")
```

Will result in:

```json
{
  "Principal": {
    "Service": [ "cloudwatch.amazonaws.com", "ec2.amazonaws.com" ],
    "AWS": "arn:aws:boom:boom"
  }
}
```

The `CompositePrincipal` class can also be used to define complex principals, for example:

```python
role = iam.Role(self, "MyRole",
    assumed_by=iam.CompositePrincipal(
        iam.ServicePrincipal("ec2.amazonaws.com"),
        iam.AccountPrincipal("1818188181818187272"))
)
```

The `PrincipalWithConditions` class can be used to add conditions to a
principal, especially those that don't take a `conditions` parameter in their
constructor. The `principal.withConditions()` method can be used to create a
`PrincipalWithConditions` from an existing principal, for example:

```python
principal = iam.AccountPrincipal("123456789000").with_conditions({"StringEquals": {"foo": "baz"}})
```

> NOTE: If you need to define an IAM condition that uses a token (such as a
> deploy-time attribute of another resource) in a JSON map key, use `CfnJson` to
> render this condition. See [this test](./test/integ.condition-with-ref.ts) for
> an example.

The `WebIdentityPrincipal` class can be used as a principal for web identities like
Cognito, Amazon, Google or Facebook, for example:

```python
principal = iam.WebIdentityPrincipal("cognito-identity.amazonaws.com", {
    "StringEquals": {"cognito-identity.amazonaws.com:aud": "us-east-2:12345678-abcd-abcd-abcd-123456"},
    "ForAnyValue:StringLike": {"cognito-identity.amazonaws.com:amr": "unauthenticated"}
})
```

If your identity provider is configured to assume a Role with [session
tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html), you
need to call `.withSessionTags()` to add the required permissions to the Role's
policy document:

```python
iam.Role(self, "Role",
    assumed_by=iam.WebIdentityPrincipal("cognito-identity.amazonaws.com", {
        "StringEquals": {
            "cognito-identity.amazonaws.com:aud": "us-east-2:12345678-abcd-abcd-abcd-123456"
        },
        "ForAnyValue:StringLike": {
            "cognito-identity.amazonaws.com:amr": "unauthenticated"
        }
    }).with_session_tags()
)
```

## Parsing JSON Policy Documents

The `PolicyDocument.fromJson` and `PolicyStatement.fromJson` static methods can be used to parse JSON objects. For example:

```python
policy_document = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "FirstStatement",
        "Effect": "Allow",
        "Action": ["iam:ChangePassword"],
        "Resource": "*"
    }, {
        "Sid": "SecondStatement",
        "Effect": "Allow",
        "Action": "s3:ListAllMyBuckets",
        "Resource": "*"
    }, {
        "Sid": "ThirdStatement",
        "Effect": "Allow",
        "Action": ["s3:List*", "s3:Get*"
        ],
        "Resource": ["arn:aws:s3:::confidential-data", "arn:aws:s3:::confidential-data/*"
        ],
        "Condition": {"Bool": {"aws:_multi_factor_auth_present": "true"}}
    }
    ]
}

custom_policy_document = iam.PolicyDocument.from_json(policy_document)

# You can pass this document as an initial document to a ManagedPolicy
# or inline Policy.
new_managed_policy = iam.ManagedPolicy(self, "MyNewManagedPolicy",
    document=custom_policy_document
)
new_policy = iam.Policy(self, "MyNewPolicy",
    document=custom_policy_document
)
```

## Permissions Boundaries

[Permissions
Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
can be used as a mechanism to prevent privilege esclation by creating new
`Role`s. Permissions Boundaries are a Managed Policy, attached to Roles or
Users, that represent the *maximum* set of permissions they can have. The
effective set of permissions of a Role (or User) will be the intersection of
the Identity Policy and the Permissions Boundary attached to the Role (or
User). Permissions Boundaries are typically created by account
Administrators, and their use on newly created `Role`s will be enforced by
IAM policies.

It is possible to attach Permissions Boundaries to all Roles created in a construct
tree all at once:

```python
# Directly apply the boundary to a Role you create
# role: iam.Role

# Apply the boundary to an Role that was implicitly created for you
# fn: lambda.Function

# Remove a Permissions Boundary that is inherited, for example from the Stack level
# custom_resource: CustomResource
# This imports an existing policy.
boundary = iam.ManagedPolicy.from_managed_policy_arn(self, "Boundary", "arn:aws:iam::123456789012:policy/boundary")

# This creates a new boundary
boundary2 = iam.ManagedPolicy(self, "Boundary2",
    statements=[
        iam.PolicyStatement(
            effect=iam.Effect.DENY,
            actions=["iam:*"],
            resources=["*"]
        )
    ]
)
iam.PermissionsBoundary.of(role).apply(boundary)
iam.PermissionsBoundary.of(fn).apply(boundary)

# Apply the boundary to all Roles in a stack
iam.PermissionsBoundary.of(self).apply(boundary)
iam.PermissionsBoundary.of(custom_resource).clear()
```

## OpenID Connect Providers

OIDC identity providers are entities in IAM that describe an external identity
provider (IdP) service that supports the [OpenID Connect](http://openid.net/connect) (OIDC) standard, such
as Google or Salesforce. You use an IAM OIDC identity provider when you want to
establish trust between an OIDC-compatible IdP and your AWS account. This is
useful when creating a mobile app or web application that requires access to AWS
resources, but you don't want to create custom sign-in code or manage your own
user identities. For more information about this scenario, see [About Web
Identity Federation] and the relevant documentation in the [Amazon Cognito
Identity Pools Developer Guide].

The following examples defines an OpenID Connect provider. Two client IDs
(audiences) are will be able to send authentication requests to
[https://openid/connect](https://openid/connect).

```python
provider = iam.OpenIdConnectProvider(self, "MyProvider",
    url="https://openid/connect",
    client_ids=["myclient1", "myclient2"]
)
```

You can specify an optional list of `thumbprints`. If not specified, the
thumbprint of the root certificate authority (CA) will automatically be obtained
from the host as described
[here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html).

Once you define an OpenID connect provider, you can use it with AWS services
that expect an IAM OIDC provider. For example, when you define an [Amazon
Cognito identity
pool](https://docs.aws.amazon.com/cognito/latest/developerguide/open-id.html)
you can reference the provider's ARN as follows:

```python
import aws_cdk.aws_cognito as cognito

# my_provider: iam.OpenIdConnectProvider

cognito.CfnIdentityPool(self, "IdentityPool",
    open_id_connect_provider_arns=[my_provider.open_id_connect_provider_arn],
    # And the other properties for your identity pool
    allow_unauthenticated_identities=False
)
```

The `OpenIdConnectPrincipal` class can be used as a principal used with a `OpenIdConnectProvider`, for example:

```python
provider = iam.OpenIdConnectProvider(self, "MyProvider",
    url="https://openid/connect",
    client_ids=["myclient1", "myclient2"]
)
principal = iam.OpenIdConnectPrincipal(provider)
```

## SAML provider

An IAM SAML 2.0 identity provider is an entity in IAM that describes an external
identity provider (IdP) service that supports the SAML 2.0 (Security Assertion
Markup Language 2.0) standard. You use an IAM identity provider when you want
to establish trust between a SAML-compatible IdP such as Shibboleth or Active
Directory Federation Services and AWS, so that users in your organization can
access AWS resources. IAM SAML identity providers are used as principals in an
IAM trust policy.

```python
iam.SamlProvider(self, "Provider",
    metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
)
```

The `SamlPrincipal` class can be used as a principal with a `SamlProvider`:

```python
provider = iam.SamlProvider(self, "Provider",
    metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
)
principal = iam.SamlPrincipal(provider, {
    "StringEquals": {
        "SAML:iss": "issuer"
    }
})
```

When creating a role for programmatic and AWS Management Console access, use the `SamlConsolePrincipal`
class:

```python
provider = iam.SamlProvider(self, "Provider",
    metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
)
iam.Role(self, "Role",
    assumed_by=iam.SamlConsolePrincipal(provider)
)
```

## Users

IAM manages users for your AWS account. To create a new user:

```python
user = iam.User(self, "MyUser")
```

To import an existing user by name [with path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names):

```python
user = iam.User.from_user_name(self, "MyImportedUserByName", "johnsmith")
```

To import an existing user by ARN:

```python
user = iam.User.from_user_arn(self, "MyImportedUserByArn", "arn:aws:iam::123456789012:user/johnsmith")
```

To import an existing user by attributes:

```python
user = iam.User.from_user_attributes(self, "MyImportedUserByAttributes",
    user_arn="arn:aws:iam::123456789012:user/johnsmith"
)
```

### Access Keys

The ability for a user to make API calls via the CLI or an SDK is enabled by the user having an
access key pair. To create an access key:

```python
user = iam.User(self, "MyUser")
access_key = iam.AccessKey(self, "MyAccessKey", user=user)
```

You can force CloudFormation to rotate the access key by providing a monotonically increasing `serial`
property. Simply provide a higher serial value than any number used previously:

```python
user = iam.User(self, "MyUser")
access_key = iam.AccessKey(self, "MyAccessKey", user=user, serial=1)
```

An access key may only be associated with a single user and cannot be "moved" between users. Changing
the user associated with an access key replaces the access key (and its ID and secret value).

## Groups

An IAM user group is a collection of IAM users. User groups let you specify permissions for multiple users.

```python
group = iam.Group(self, "MyGroup")
```

To import an existing group by ARN:

```python
group = iam.Group.from_group_arn(self, "MyImportedGroupByArn", "arn:aws:iam::account-id:group/group-name")
```

To import an existing group by name [with path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names):

```python
group = iam.Group.from_group_name(self, "MyImportedGroupByName", "group-name")
```

To add a user to a group (both for a new and imported user/group):

```python
user = iam.User(self, "MyUser") # or User.fromUserName(stack, 'User', 'johnsmith');
group = iam.Group(self, "MyGroup") # or Group.fromGroupArn(stack, 'Group', 'arn:aws:iam::account-id:group/group-name');

user.add_to_group(group)
# or
group.add_user(user)
```

## Features

* Policy name uniqueness is enforced. If two policies by the same name are attached to the same
  principal, the attachment will fail.
* Policy names are not required - the CDK logical ID will be used and ensured to be unique.
* Policies are validated during synthesis to ensure that they have actions, and that policies
  attached to IAM principals specify relevant resources, while policies attached to resources
  specify which IAM principals they apply to.
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
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.AccessKeyProps",
    jsii_struct_bases=[],
    name_mapping={"user": "user", "serial": "serial", "status": "status"},
)
class AccessKeyProps:
    def __init__(
        self,
        *,
        user: "IUser",
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional["AccessKeyStatus"] = None,
    ) -> None:
        '''Properties for defining an IAM access key.

        :param user: The IAM user this key will belong to. Changing this value will result in the access key being deleted and a new access key (with a different ID and secret value) being assigned to the new user.
        :param serial: A CloudFormation-specific value that signifies the access key should be replaced/rotated. This value can only be incremented. Incrementing this value will cause CloudFormation to replace the Access Key resource. Default: - No serial value
        :param status: The status of the access key. An Active access key is allowed to be used to make API calls; An Inactive key cannot. Default: - The access key is active

        :exampleMetadata: infused

        Example::

            # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
            user = iam.User(self, "User")
            access_key = iam.AccessKey(self, "AccessKey", user=user)
            secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
            secretsmanager.Secret(self, "Secret",
                secret_string_beta1=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a1416c22de88a620b216c5e13428adb6716ba5f4284a6bb32b744db11b9a6a)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument serial", value=serial, expected_type=type_hints["serial"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user": user,
        }
        if serial is not None:
            self._values["serial"] = serial
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def user(self) -> "IUser":
        '''The IAM user this key will belong to.

        Changing this value will result in the access key being deleted and a new
        access key (with a different ID and secret value) being assigned to the new
        user.
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast("IUser", result)

    @builtins.property
    def serial(self) -> typing.Optional[jsii.Number]:
        '''A CloudFormation-specific value that signifies the access key should be replaced/rotated.

        This value can only be incremented. Incrementing this
        value will cause CloudFormation to replace the Access Key resource.

        :default: - No serial value
        '''
        result = self._values.get("serial")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional["AccessKeyStatus"]:
        '''The status of the access key.

        An Active access key is allowed to be used
        to make API calls; An Inactive key cannot.

        :default: - The access key is active
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["AccessKeyStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-iam.AccessKeyStatus")
class AccessKeyStatus(enum.Enum):
    '''Valid statuses for an IAM Access Key.'''

    ACTIVE = "ACTIVE"
    '''An active access key.

    An active key can be used to make API calls.
    '''
    INACTIVE = "INACTIVE"
    '''An inactive access key.

    An inactive key cannot be used to make API calls.
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.AddToPrincipalPolicyResult",
    jsii_struct_bases=[],
    name_mapping={
        "statement_added": "statementAdded",
        "policy_dependable": "policyDependable",
    },
)
class AddToPrincipalPolicyResult:
    def __init__(
        self,
        *,
        statement_added: builtins.bool,
        policy_dependable: typing.Optional[_aws_cdk_core_f4b25747.IDependable] = None,
    ) -> None:
        '''Result of calling ``addToPrincipalPolicy``.

        :param statement_added: Whether the statement was added to the identity's policies.
        :param policy_dependable: Dependable which allows depending on the policy change being applied. Default: - Required if ``statementAdded`` is true.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.core as cdk
            
            # dependable: cdk.IDependable
            
            add_to_principal_policy_result = iam.AddToPrincipalPolicyResult(
                statement_added=False,
            
                # the properties below are optional
                policy_dependable=dependable
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ef98f6e162ecc49216a84424a34cbcd99b925e29023b1e6b0a9fce25ea1b3d)
            check_type(argname="argument statement_added", value=statement_added, expected_type=type_hints["statement_added"])
            check_type(argname="argument policy_dependable", value=policy_dependable, expected_type=type_hints["policy_dependable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "statement_added": statement_added,
        }
        if policy_dependable is not None:
            self._values["policy_dependable"] = policy_dependable

    @builtins.property
    def statement_added(self) -> builtins.bool:
        '''Whether the statement was added to the identity's policies.'''
        result = self._values.get("statement_added")
        assert result is not None, "Required property 'statement_added' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def policy_dependable(self) -> typing.Optional[_aws_cdk_core_f4b25747.IDependable]:
        '''Dependable which allows depending on the policy change being applied.

        :default: - Required if ``statementAdded`` is true.
        '''
        result = self._values.get("policy_dependable")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IDependable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddToPrincipalPolicyResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.AddToResourcePolicyResult",
    jsii_struct_bases=[],
    name_mapping={
        "statement_added": "statementAdded",
        "policy_dependable": "policyDependable",
    },
)
class AddToResourcePolicyResult:
    def __init__(
        self,
        *,
        statement_added: builtins.bool,
        policy_dependable: typing.Optional[_aws_cdk_core_f4b25747.IDependable] = None,
    ) -> None:
        '''Result of calling addToResourcePolicy.

        :param statement_added: Whether the statement was added.
        :param policy_dependable: Dependable which allows depending on the policy change being applied. Default: - If ``statementAdded`` is true, the resource object itself. Otherwise, no dependable.

        :exampleMetadata: infused

        Example::

            bucket = s3.Bucket.from_bucket_name(self, "existingBucket", "bucket-name")
            
            # No policy statement will be added to the resource
            result = bucket.add_to_resource_policy(iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[bucket.arn_for_objects("file.txt")],
                principals=[iam.AccountRootPrincipal()]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d9e4e3a3d0914c75521a1473c8de7bb301f6791cdb68e3b3b1bb1f8582d1b1)
            check_type(argname="argument statement_added", value=statement_added, expected_type=type_hints["statement_added"])
            check_type(argname="argument policy_dependable", value=policy_dependable, expected_type=type_hints["policy_dependable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "statement_added": statement_added,
        }
        if policy_dependable is not None:
            self._values["policy_dependable"] = policy_dependable

    @builtins.property
    def statement_added(self) -> builtins.bool:
        '''Whether the statement was added.'''
        result = self._values.get("statement_added")
        assert result is not None, "Required property 'statement_added' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def policy_dependable(self) -> typing.Optional[_aws_cdk_core_f4b25747.IDependable]:
        '''Dependable which allows depending on the policy change being applied.

        :default:

        - If ``statementAdded`` is true, the resource object itself.
        Otherwise, no dependable.
        '''
        result = self._values.get("policy_dependable")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IDependable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddToResourcePolicyResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAccessKey(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnAccessKey",
):
    '''A CloudFormation ``AWS::IAM::AccessKey``.

    Creates a new AWS secret access key and corresponding AWS access key ID for the specified user. The default status for new keys is ``Active`` .

    For information about quotas on the number of keys you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       To ensure the security of your AWS account , the secret access key is accessible only during key and user creation. You must save the key (for example, in a text file) if you want to be able to access it again. If a secret key is lost, you can rotate access keys by increasing the value of the ``serial`` property.

    :cloudformationResource: AWS::IAM::AccessKey
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        cfn_access_key = iam.CfnAccessKey(self, "MyCfnAccessKey",
            user_name="userName",
        
            # the properties below are optional
            serial=123,
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        user_name: builtins.str,
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::AccessKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_name: The name of the IAM user that the new key will belong to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param serial: This value is specific to CloudFormation and can only be *incremented* . Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.
        :param status: The status of the access key. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa6cbae092328b8aff5cda78e1da7ba9a694031046f305bb48ecb2139e1c2bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessKeyProps(user_name=user_name, serial=serial, status=status)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f15da46a99bc07348d19740b25b14184a985d28f13a8be30e11685b4e8f0ea4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5676e3c6392e8cb0473b4e8782eda56ef98533c8228359495f58e40f44791e65)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSecretAccessKey")
    def attr_secret_access_key(self) -> builtins.str:
        '''Returns the secret access key for the specified AWS::IAM::AccessKey resource.

        For example: wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY.

        :cloudformationAttribute: SecretAccessKey
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSecretAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The name of the IAM user that the new key will belong to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860cf915a0ac64b28b68db2c008c248935780719c99ffbf203c320ee0d91ee88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="serial")
    def serial(self) -> typing.Optional[jsii.Number]:
        '''This value is specific to CloudFormation and can only be *incremented* .

        Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-serial
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serial"))

    @serial.setter
    def serial(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150c776515b1c7523874b462c62a35a1005a23087485081d878132b3a20552a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serial", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the access key.

        ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d872830178849f932d025904b16ffe79838915ab95f3ee898835f3ebe980037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnAccessKeyProps",
    jsii_struct_bases=[],
    name_mapping={"user_name": "userName", "serial": "serial", "status": "status"},
)
class CfnAccessKeyProps:
    def __init__(
        self,
        *,
        user_name: builtins.str,
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessKey``.

        :param user_name: The name of the IAM user that the new key will belong to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param serial: This value is specific to CloudFormation and can only be *incremented* . Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.
        :param status: The status of the access key. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            cfn_access_key_props = iam.CfnAccessKeyProps(
                user_name="userName",
            
                # the properties below are optional
                serial=123,
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7ed84b5ec8a936c144ed47067cb468cacb975f83e5049a1aa8df388b2211e2)
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument serial", value=serial, expected_type=type_hints["serial"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_name": user_name,
        }
        if serial is not None:
            self._values["serial"] = serial
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def user_name(self) -> builtins.str:
        '''The name of the IAM user that the new key will belong to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def serial(self) -> typing.Optional[jsii.Number]:
        '''This value is specific to CloudFormation and can only be *incremented* .

        Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-serial
        '''
        result = self._values.get("serial")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the access key.

        ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnGroup",
):
    '''A CloudFormation ``AWS::IAM::Group``.

    Creates a new group.

    For information about the number of groups you can create, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::Group
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # policy_document: Any
        
        cfn_group = iam.CfnGroup(self, "MyCfnGroup",
            group_name="groupName",
            managed_policy_arns=["managedPolicyArns"],
            path="path",
            policies=[iam.CfnGroup.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGroup.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: The name of the group to create. Do not include the path in this value. The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param managed_policy_arns: The Amazon Resource Name (ARN) of the IAM policy you want to attach. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM group. To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ . .. epigraph:: The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4017e26628b4ac40c45ae3de3d527ff4ecadaa9969645b50be89f187b5e763)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(
            group_name=group_name,
            managed_policy_arns=managed_policy_arns,
            path=path,
            policies=policies,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58dea00a5cd1032971b7708e014f8fdf6e2f535643811c41abd30f74b08a1a91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d2406f072d1428f166ea587cc677807c082d5879a108a89e151aedb3100d638)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::Group`` resource.

        For example: ``arn:aws:iam::123456789012:group/mystack-mygroup-1DZETITOWEKVO`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group to create. Do not include the path in this value.

        The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-groupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c4745df9cc7871b99dffd6f2d05519570d4c623a64f348fedb26d44994a91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-managepolicyarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managedPolicyArns"))

    @managed_policy_arns.setter
    def managed_policy_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1320df791d0fbdb2f9945b814789f3e61ffe602d962cd041df89a7403b750aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9a3f88e09c80c00ca9a22d4d7e27becafee90c18df582b9ff771926216b11e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.PolicyProperty"]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM group.

        To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ .
        .. epigraph::

           The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-policies
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.PolicyProperty"]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.PolicyProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db9e4304586acb1e7788cc3d393e30ada4edc231c6c9a229611d105ba979c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iam.CfnGroup.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any,
            policy_name: builtins.str,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The policy document.
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iam as iam
                
                # policy_document: Any
                
                policy_property = iam.CfnGroup.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__841b8e984be5df111232d9c9e13f84b35ee9bdce0330bce1446562c8afa01ef7)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_document": policy_document,
                "policy_name": policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The policy document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            '''
            result = self._values.get("policy_document")
            assert result is not None, "Required property 'policy_document' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "managed_policy_arns": "managedPolicyArns",
        "path": "path",
        "policies": "policies",
    },
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGroup``.

        :param group_name: The name of the group to create. Do not include the path in this value. The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param managed_policy_arns: The Amazon Resource Name (ARN) of the IAM policy you want to attach. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM group. To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ . .. epigraph:: The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # policy_document: Any
            
            cfn_group_props = iam.CfnGroupProps(
                group_name="groupName",
                managed_policy_arns=["managedPolicyArns"],
                path="path",
                policies=[iam.CfnGroup.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c711db90d1b5a925d9125ecd09b35213fb1789bfc4ee6ae24c723c777d58a7)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None:
            self._values["path"] = path
        if policies is not None:
            self._values["policies"] = policies

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group to create. Do not include the path in this value.

        The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-managepolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.PolicyProperty]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM group.

        To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ .
        .. epigraph::

           The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.PolicyProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnInstanceProfile(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnInstanceProfile",
):
    '''A CloudFormation ``AWS::IAM::InstanceProfile``.

    Creates a new instance profile. For information about instance profiles, see `Using instance profiles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html>`_ .

    For information about the number of instance profiles you can create, see `IAM object quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::InstanceProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        cfn_instance_profile = iam.CfnInstanceProfile(self, "MyCfnInstanceProfile",
            roles=["roles"],
        
            # the properties below are optional
            instance_profile_name="instanceProfileName",
            path="path"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        roles: typing.Sequence[builtins.str],
        instance_profile_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::InstanceProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param roles: The name of the role to associate with the instance profile. Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.
        :param instance_profile_name: The name of the instance profile to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param path: The path to the instance profile. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7d68a9ce06737826e7884e1c0308d9a217296bcd4fcd51aff93ed3fb01cd2f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInstanceProfileProps(
            roles=roles, instance_profile_name=instance_profile_name, path=path
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48069dc5a780f331b553b4afd9a95cdeb108094e6b93c8d1d7ac02be20fd2af4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__455e6a839e50f149eaf163b882a8923c6da91013cca943d98949acc75432d4c4)
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
        '''Returns the Amazon Resource Name (ARN) for the instance profile. For example:.

        ``{"Fn::GetAtt" : ["MyProfile", "Arn"] }``

        This returns a value such as ``arn:aws:iam::1234567890:instance-profile/MyProfile-ASDNSDLKJ`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        '''The name of the role to associate with the instance profile.

        Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-roles
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8dad48aa81c8069fe7c92065526deba65cf5e8dde62a523c27d5db69285bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="instanceProfileName")
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance profile to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-instanceprofilename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceProfileName"))

    @instance_profile_name.setter
    def instance_profile_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4416a6aef16c477160d51976111f48dc45cbb067755c0676bbf135a640348fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceProfileName", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the instance profile.

        For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5291fdd81326b970a438f7a808c39f2afb0268e3df6038d258acf415f50ea29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnInstanceProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "roles": "roles",
        "instance_profile_name": "instanceProfileName",
        "path": "path",
    },
)
class CfnInstanceProfileProps:
    def __init__(
        self,
        *,
        roles: typing.Sequence[builtins.str],
        instance_profile_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnInstanceProfile``.

        :param roles: The name of the role to associate with the instance profile. Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.
        :param instance_profile_name: The name of the instance profile to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param path: The path to the instance profile. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            cfn_instance_profile_props = iam.CfnInstanceProfileProps(
                roles=["roles"],
            
                # the properties below are optional
                instance_profile_name="instanceProfileName",
                path="path"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5012b618b5e1682b35a1700191a6564fde84e254bfa938a7749a75ad1db0d082)
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument instance_profile_name", value=instance_profile_name, expected_type=type_hints["instance_profile_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles": roles,
        }
        if instance_profile_name is not None:
            self._values["instance_profile_name"] = instance_profile_name
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def roles(self) -> typing.List[builtins.str]:
        '''The name of the role to associate with the instance profile.

        Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-roles
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance profile to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-instanceprofilename
        '''
        result = self._values.get("instance_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the instance profile.

        For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnManagedPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnManagedPolicy",
):
    '''A CloudFormation ``AWS::IAM::ManagedPolicy``.

    Creates a new managed policy for your AWS account .

    This operation creates a policy version with a version identifier of ``v1`` and sets v1 as the policy's default version. For more information about policy versions, see `Versioning for managed policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`_ in the *IAM User Guide* .

    As a best practice, you can validate your IAM policies. To learn more, see `Validating IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_policy-validator.html>`_ in the *IAM User Guide* .

    For more information about managed policies in general, see `Managed policies and inline policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::ManagedPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # policy_document: Any
        
        cfn_managed_policy = iam.CfnManagedPolicy(self, "MyCfnManagedPolicy",
            policy_document=policy_document,
        
            # the properties below are optional
            description="description",
            groups=["groups"],
            managed_policy_name="managedPolicyName",
            path="path",
            roles=["roles"],
            users=["users"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::ManagedPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: The JSON policy document that you want to use as the content for the new policy. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ . To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* . The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param description: A friendly description of the policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
        :param groups: The name (friendly name, not ARN) of the group to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param managed_policy_name: The friendly name of the policy. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: You cannot use an asterisk (*) in the path name.
        :param roles: The name (friendly name, not ARN) of the role to attach the policy to. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name (friendly name, not ARN) of the IAM user to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7405bd778db44d00c800df1ff74a743b4f71443476bbbf82bbb7d59647a92f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnManagedPolicyProps(
            policy_document=policy_document,
            description=description,
            groups=groups,
            managed_policy_name=managed_policy_name,
            path=path,
            roles=roles,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401a4638da40774f3940f52739980773f86d3a3d2d9d044f4e99745610b6a81f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0de0e4e32e9f9c79989dc34a2ddf138af5b8dc57ab7c813f62cd3254ef51f6)
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
    def policy_document(self) -> typing.Any:
        '''The JSON policy document that you want to use as the content for the new policy.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ .

        To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* .

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62dfa7120d72994241ef14e2366eda9cffadbef2a9b34387428dc1143737735d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A friendly description of the policy.

        Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables."

        The policy description is immutable. After a value is assigned, it cannot be changed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6f95eade608491e1aecd5314e8b30fdc478a0bb58546fd703abddcff4c9d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the group to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-groups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a20464338fa4ab0038165ce78610d3c26ca0e1cf7a42bc4bbe9f5eea156184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyName")
    def managed_policy_name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of the policy.

        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-managedpolicyname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedPolicyName"))

    @managed_policy_name.setter
    def managed_policy_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8934b0078389739c7333b9895c38040426347a67cc9b67183e2b1c25ee22da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           You cannot use an asterisk (*) in the path name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-ec2-dhcpoptions-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5719d42cfe0c8bfb7f56c9921d590677a0616f52f67f2f41e91a09b99b570526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the role to attach the policy to.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-roles
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e4fa36440ede7dabb105c8d71ca16b4592db51c2b48f52ae0f39a0fd9b040d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the IAM user to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-users
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c0f543477844162f6d0d8d8df5bae0ec4edf62f16f5ad382fddf1c891f542f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnManagedPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "description": "description",
        "groups": "groups",
        "managed_policy_name": "managedPolicyName",
        "path": "path",
        "roles": "roles",
        "users": "users",
    },
)
class CfnManagedPolicyProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnManagedPolicy``.

        :param policy_document: The JSON policy document that you want to use as the content for the new policy. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ . To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* . The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param description: A friendly description of the policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
        :param groups: The name (friendly name, not ARN) of the group to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param managed_policy_name: The friendly name of the policy. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: You cannot use an asterisk (*) in the path name.
        :param roles: The name (friendly name, not ARN) of the role to attach the policy to. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name (friendly name, not ARN) of the IAM user to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # policy_document: Any
            
            cfn_managed_policy_props = iam.CfnManagedPolicyProps(
                policy_document=policy_document,
            
                # the properties below are optional
                description="description",
                groups=["groups"],
                managed_policy_name="managedPolicyName",
                path="path",
                roles=["roles"],
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62d487b0e5adc2faf71d6792a8bde6282615f37234599431f92701eed79c5f1)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
        }
        if description is not None:
            self._values["description"] = description
        if groups is not None:
            self._values["groups"] = groups
        if managed_policy_name is not None:
            self._values["managed_policy_name"] = managed_policy_name
        if path is not None:
            self._values["path"] = path
        if roles is not None:
            self._values["roles"] = roles
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The JSON policy document that you want to use as the content for the new policy.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ .

        To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* .

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A friendly description of the policy.

        Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables."

        The policy description is immutable. After a value is assigned, it cannot be changed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the group to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def managed_policy_name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of the policy.

        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-managedpolicyname
        '''
        result = self._values.get("managed_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           You cannot use an asterisk (*) in the path name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-ec2-dhcpoptions-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the role to attach the policy to.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the IAM user to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnManagedPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnOIDCProvider(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnOIDCProvider",
):
    '''A CloudFormation ``AWS::IAM::OIDCProvider``.

    Creates or updates an IAM entity to describe an identity provider (IdP) that supports `OpenID Connect (OIDC) <https://docs.aws.amazon.com/http://openid.net/connect/>`_ .

    The OIDC provider that you create with this operation can be used as a principal in a role's trust policy. Such a policy establishes a trust relationship between AWS and the OIDC provider.

    When you create the IAM OIDC provider, you specify the following:

    - The URL of the OIDC identity provider (IdP) to trust
    - A list of client IDs (also known as audiences) that identify the application or applications that are allowed to authenticate using the OIDC provider
    - A list of tags that are attached to the specified IAM OIDC provider
    - A list of thumbprints of one or more server certificates that the IdP uses

    You get all of this information from the OIDC IdP that you want to use to access AWS .

    When you update the IAM OIDC provider, you specify the following:

    - The URL of the OIDC identity provider (IdP) to trust
    - A list of client IDs (also known as audiences) that replaces the existing list of client IDs associated with the OIDC IdP
    - A list of tags that replaces the existing list of tags attached to the specified IAM OIDC provider
    - A list of thumbprints that replaces the existing list of server certificates thumbprints that the IdP uses

    .. epigraph::

       The trust for the OIDC provider is derived from the IAM provider that this operation creates. Therefore, it is best to limit access to the `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ operation to highly privileged users.

    :cloudformationResource: AWS::IAM::OIDCProvider
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        cfn_oIDCProvider = iam.CfnOIDCProvider(self, "MyCfnOIDCProvider",
            thumbprint_list=["thumbprintList"],
        
            # the properties below are optional
            client_id_list=["clientIdList"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            url="url"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        thumbprint_list: typing.Sequence[builtins.str],
        client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::OIDCProvider``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param thumbprint_list: A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param client_id_list: A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param tags: A list of tags that are attached to the specified IAM OIDC provider. The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        :param url: The URL that the IAM OIDC provider resource object is associated with. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64d829cf2255983b6697aaabba068760e784de1807b9c47a49d1b34a7956ce9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnOIDCProviderProps(
            thumbprint_list=thumbprint_list,
            client_id_list=client_id_list,
            tags=tags,
            url=url,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ed625d5dc4318aff35627ae253d05ea0ce179c7b09f3f644ce3142f454862e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bf722ffce1a2fba9118f611a3c9f9845e4faecb8bdf7e90637b51855bcd8521)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::OIDCProvider`` resource.

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
        '''A list of tags that are attached to the specified IAM OIDC provider.

        The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintList")
    def thumbprint_list(self) -> typing.List[builtins.str]:
        '''A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-thumbprintlist
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "thumbprintList"))

    @thumbprint_list.setter
    def thumbprint_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19fc4bbecf9e2cc2cabe79ef4b4dfd16cae9e2f208f7df4a45dc785c5b877e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprintList", value)

    @builtins.property
    @jsii.member(jsii_name="clientIdList")
    def client_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-clientidlist
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clientIdList"))

    @client_id_list.setter
    def client_id_list(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79c112e6971b0a138d8e6e383e5afc56227471d7f4505c70cc962668c0638cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientIdList", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL that the IAM OIDC provider resource object is associated with.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-url
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "url"))

    @url.setter
    def url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f82aca862212d2897f4d0cf19491f10b5de81ce369cdadf57b19f2389f790a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnOIDCProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "thumbprint_list": "thumbprintList",
        "client_id_list": "clientIdList",
        "tags": "tags",
        "url": "url",
    },
)
class CfnOIDCProviderProps:
    def __init__(
        self,
        *,
        thumbprint_list: typing.Sequence[builtins.str],
        client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnOIDCProvider``.

        :param thumbprint_list: A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param client_id_list: A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param tags: A list of tags that are attached to the specified IAM OIDC provider. The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        :param url: The URL that the IAM OIDC provider resource object is associated with. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            cfn_oIDCProvider_props = iam.CfnOIDCProviderProps(
                thumbprint_list=["thumbprintList"],
            
                # the properties below are optional
                client_id_list=["clientIdList"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                url="url"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9826c7762172f597ccaaa167d81f46fbf181f9114f5ff3f21e111a206ab92e07)
            check_type(argname="argument thumbprint_list", value=thumbprint_list, expected_type=type_hints["thumbprint_list"])
            check_type(argname="argument client_id_list", value=client_id_list, expected_type=type_hints["client_id_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thumbprint_list": thumbprint_list,
        }
        if client_id_list is not None:
            self._values["client_id_list"] = client_id_list
        if tags is not None:
            self._values["tags"] = tags
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def thumbprint_list(self) -> typing.List[builtins.str]:
        '''A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-thumbprintlist
        '''
        result = self._values.get("thumbprint_list")
        assert result is not None, "Required property 'thumbprint_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def client_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-clientidlist
        '''
        result = self._values.get("client_id_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags that are attached to the specified IAM OIDC provider.

        The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL that the IAM OIDC provider resource object is associated with.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-url
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOIDCProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnPolicy",
):
    '''A CloudFormation ``AWS::IAM::Policy``.

    Adds or updates an inline policy document that is embedded in the specified IAM user, group, or role.

    An IAM user can also have a managed policy attached to it. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    The Groups, Roles, and Users properties are optional. However, you must specify at least one of these properties.

    For information about policy documents see `Creating IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html>`_ in the *IAM User Guide* .

    For information about limits on the number of inline policies that you can embed in an identity, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::Policy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # policy_document: Any
        
        cfn_policy = iam.CfnPolicy(self, "MyCfnPolicy",
            policy_document=policy_document,
            policy_name="policyName",
        
            # the properties below are optional
            groups=["groups"],
            roles=["roles"],
            users=["users"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy_document: typing.Any,
        policy_name: builtins.str,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::Policy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param groups: The name of the group to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.
        :param roles: The name of the role to associate the policy with. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name of the user to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53162e251261ed8b83b4a1e526c2fbc7a1b73c60fe284f975ca54e9142ff60f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPolicyProps(
            policy_document=policy_document,
            policy_name=policy_name,
            groups=groups,
            roles=roles,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83ff569c112bcc2c7df18fda83c34af21fa3994a7b0166fa26c24ba34411b66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59c799ad27e30d5147cbcc46b9dd04c3929304116cecb52716ccb568aff25cdc)
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
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2006575d3dc0eb086ac238513796a36357a675ee4e1caeb4084bb822853fdf32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8100e578d852455fc7e3f3dd63215ff3c3c519e1e33c796557866c0f6a743f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the group to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-groups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c1d43829c7d40c491c798edd408c805b090d47c57bffa10c87cd9a55bedac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the role to associate the policy with.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-roles
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183599a3e80b946121ea4b10ef27ce3acae62930ebac5225501294bac8d599a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the user to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-users
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4790e7d3a2a32b62bb7c1204efd6ff86aef80a310da66eb71df7f540e01da93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "policy_name": "policyName",
        "groups": "groups",
        "roles": "roles",
        "users": "users",
    },
)
class CfnPolicyProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any,
        policy_name: builtins.str,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPolicy``.

        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param groups: The name of the group to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.
        :param roles: The name of the role to associate the policy with. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name of the user to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # policy_document: Any
            
            cfn_policy_props = iam.CfnPolicyProps(
                policy_document=policy_document,
                policy_name="policyName",
            
                # the properties below are optional
                groups=["groups"],
                roles=["roles"],
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd52a4d00a1936382a0a104f9d73ff692ac2923da2c65aad072b062899e7758)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
            "policy_name": policy_name,
        }
        if groups is not None:
            self._values["groups"] = groups
        if roles is not None:
            self._values["roles"] = roles
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the group to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the role to associate the policy with.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the user to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRole(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnRole",
):
    '''A CloudFormation ``AWS::IAM::Role``.

    Creates a new role for your AWS account . For more information about roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`_ . For information about quotas for role names and the number of roles you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::Role
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # assume_role_policy_document: Any
        # policy_document: Any
        
        cfn_role = iam.CfnRole(self, "MyCfnRole",
            assume_role_policy_document=assume_role_policy_document,
        
            # the properties below are optional
            description="description",
            managed_policy_arns=["managedPolicyArns"],
            max_session_duration=123,
            path="path",
            permissions_boundary="permissionsBoundary",
            policies=[iam.CfnRole.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )],
            role_name="roleName",
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
        assume_role_policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_session_duration: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRole.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::Role``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assume_role_policy_document: The trust policy that is associated with this role. Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .
        :param description: A description of the role that you provide.
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param max_session_duration: The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours. Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .
        :param path: The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the policy used to set the permissions boundary for the role. For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM role. When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ . A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* . For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* . .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param role_name: A name for the IAM role, up to 64 characters in length. For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* . This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param tags: A list of tags that are attached to the role. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e20f55c1a36eee3998dee673995816ac45fa24cba02d7b0f338417f9a063dd9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRoleProps(
            assume_role_policy_document=assume_role_policy_document,
            description=description,
            managed_policy_arns=managed_policy_arns,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            policies=policies,
            role_name=role_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed1a9ba5968e0bfefa71739e4c7effa4d8526abb3ba63359884c3dd3fe1218d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc1a61dcb42675b18fb5e48c623661827af4e75e57247f3395f6dd8b4cd47cbe)
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
        '''Returns the Amazon Resource Name (ARN) for the role. For example:.

        ``{"Fn::GetAtt" : ["MyRole", "Arn"] }``

        This will return a value such as ``arn:aws:iam::1234567890:role/MyRole-AJJHDSKSDF`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRoleId")
    def attr_role_id(self) -> builtins.str:
        '''Returns the stable and unique string identifying the role. For example, ``AIDAJQABLZS4A3QDU576Q`` .

        For more information about IDs, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

        :cloudformationAttribute: RoleId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRoleId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of tags that are attached to the role.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicyDocument")
    def assume_role_policy_document(self) -> typing.Any:
        '''The trust policy that is associated with this role.

        Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-assumerolepolicydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "assumeRolePolicyDocument"))

    @assume_role_policy_document.setter
    def assume_role_policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b114ac2e39bbff6321e8c6e77f09603448faebed181a5d375725c17143754cbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assumeRolePolicyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role that you provide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a45d0f55b630b2ee54ea84ce4aeee37cd04205f662404e8cc8c21990b6d141d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-managepolicyarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managedPolicyArns"))

    @managed_policy_arns.setter
    def managed_policy_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbb7787a3d274f9b7e986e6048d6e2e8ef572b452753efa16fdbf0827e4d2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="maxSessionDuration")
    def max_session_duration(self) -> typing.Optional[jsii.Number]:
        '''The maximum session duration (in seconds) that you want to set for the specified role.

        If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours.

        Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-maxsessionduration
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSessionDuration"))

    @max_session_duration.setter
    def max_session_duration(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083b7f6a883dc28ffeb90cfa10b1a4b1f0c95d1e20583b27eaa1f6cd665c7c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSessionDuration", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7104656480ab5b150db3309e2d6297a79b04b8c057a3a09a775cfd78ac24490a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the policy used to set the permissions boundary for the role.

        For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-permissionsboundary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundary"))

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1ff4af19ba56e41512ff3c64a881a13912eb1ecf6b36b205cf8265b12f1dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRole.PolicyProperty"]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM role.

        When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ .

        A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

        For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-policies
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRole.PolicyProperty"]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRole.PolicyProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f6852edff1517b44bb2125313d6a63ba69b942ee9c5cc599b02035a7504957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role, up to 64 characters in length.

        For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* .

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-rolename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleName"))

    @role_name.setter
    def role_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4939c84e3d855a135a406c0160a28bdd110bffe4cc472f852af7ee497f568e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iam.CfnRole.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any,
            policy_name: builtins.str,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, refer to `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The entire contents of the policy that defines permissions. For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iam as iam
                
                # policy_document: Any
                
                policy_property = iam.CfnRole.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db348398319580afb09df9a6e8aaac71b9cd38e33fc0d1ef33df424c8c72a44b)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_document": policy_document,
                "policy_name": policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The entire contents of the policy that defines permissions.

            For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            '''
            result = self._values.get("policy_document")
            assert result is not None, "Required property 'policy_document' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "assume_role_policy_document": "assumeRolePolicyDocument",
        "description": "description",
        "managed_policy_arns": "managedPolicyArns",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "role_name": "roleName",
        "tags": "tags",
    },
)
class CfnRoleProps:
    def __init__(
        self,
        *,
        assume_role_policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_session_duration: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRole.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRole``.

        :param assume_role_policy_document: The trust policy that is associated with this role. Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .
        :param description: A description of the role that you provide.
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param max_session_duration: The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours. Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .
        :param path: The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the policy used to set the permissions boundary for the role. For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM role. When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ . A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* . For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* . .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param role_name: A name for the IAM role, up to 64 characters in length. For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* . This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param tags: A list of tags that are attached to the role. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # assume_role_policy_document: Any
            # policy_document: Any
            
            cfn_role_props = iam.CfnRoleProps(
                assume_role_policy_document=assume_role_policy_document,
            
                # the properties below are optional
                description="description",
                managed_policy_arns=["managedPolicyArns"],
                max_session_duration=123,
                path="path",
                permissions_boundary="permissionsBoundary",
                policies=[iam.CfnRole.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )],
                role_name="roleName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e23ac1f54a2cf6c4b3e974cee549ae8cab3cf6b8cc4975c71190746b04aaaa)
            check_type(argname="argument assume_role_policy_document", value=assume_role_policy_document, expected_type=type_hints["assume_role_policy_document"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument max_session_duration", value=max_session_duration, expected_type=type_hints["max_session_duration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assume_role_policy_document": assume_role_policy_document,
        }
        if description is not None:
            self._values["description"] = description
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if role_name is not None:
            self._values["role_name"] = role_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assume_role_policy_document(self) -> typing.Any:
        '''The trust policy that is associated with this role.

        Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-assumerolepolicydocument
        '''
        result = self._values.get("assume_role_policy_document")
        assert result is not None, "Required property 'assume_role_policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role that you provide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-managepolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[jsii.Number]:
        '''The maximum session duration (in seconds) that you want to set for the specified role.

        If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours.

        Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-maxsessionduration
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the policy used to set the permissions boundary for the role.

        For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRole.PolicyProperty]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM role.

        When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ .

        A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

        For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRole.PolicyProperty]]]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role, up to 64 characters in length.

        For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* .

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-rolename
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags that are attached to the role.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSAMLProvider(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnSAMLProvider",
):
    '''A CloudFormation ``AWS::IAM::SAMLProvider``.

    Creates an IAM resource that describes an identity provider (IdP) that supports SAML 2.0.

    The SAML provider resource that you create with this operation can be used as a principal in an IAM role's trust policy. Such a policy can enable federated users who sign in using the SAML IdP to assume the role. You can create an IAM role that supports Web-based single sign-on (SSO) to the AWS Management Console or one that supports API access to AWS .

    When you create the SAML provider resource, you upload a SAML metadata document that you get from your IdP. That document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that the IdP sends. You must generate the metadata document using the identity management software that is used as your organization's IdP.
    .. epigraph::

       This operation requires `Signature Version 4 <https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`_ .

    For more information, see `Enabling SAML 2.0 federated users to access the AWS Management Console <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-saml.html>`_ and `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::SAMLProvider
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        cfn_sAMLProvider = iam.CfnSAMLProvider(self, "MyCfnSAMLProvider",
            saml_metadata_document="samlMetadataDocument",
        
            # the properties below are optional
            name="name",
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
        saml_metadata_document: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::SAMLProvider``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param saml_metadata_document: An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP. For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*
        :param name: The name of the provider to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that you want to attach to the new IAM SAML provider. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294dab5076af8fe4c1eb063300635f68b22c4ce3c734b57a8a86d8705f4fdad8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSAMLProviderProps(
            saml_metadata_document=saml_metadata_document, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa90a949db9ec5ce2faaf15b7f7f4978f4b5d2fc1cc02f9d58b71019c7f00ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d8c4c5a48a8ceb137cba61aea505824c333479278ed776599e74fbb1fe9fbfc)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::SAMLProvider`` resource.

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
        '''A list of tags that you want to attach to the new IAM SAML provider.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="samlMetadataDocument")
    def saml_metadata_document(self) -> builtins.str:
        '''An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.

        For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-samlmetadatadocument
        '''
        return typing.cast(builtins.str, jsii.get(self, "samlMetadataDocument"))

    @saml_metadata_document.setter
    def saml_metadata_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e00073cf2cb0100ab06d01cbb11a1bd87efc2eecf6c4e8145d7022928958bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlMetadataDocument", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the provider to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646f2fc0c953ba2a1fd3a0476573568efc94bd196135b0e90e507c07e4881b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnSAMLProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "saml_metadata_document": "samlMetadataDocument",
        "name": "name",
        "tags": "tags",
    },
)
class CfnSAMLProviderProps:
    def __init__(
        self,
        *,
        saml_metadata_document: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSAMLProvider``.

        :param saml_metadata_document: An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP. For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*
        :param name: The name of the provider to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that you want to attach to the new IAM SAML provider. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            cfn_sAMLProvider_props = iam.CfnSAMLProviderProps(
                saml_metadata_document="samlMetadataDocument",
            
                # the properties below are optional
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050a5fc7218c11c3ef6cf83de71f21e208ff338265ba15f1f7249e25edb01132)
            check_type(argname="argument saml_metadata_document", value=saml_metadata_document, expected_type=type_hints["saml_metadata_document"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "saml_metadata_document": saml_metadata_document,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def saml_metadata_document(self) -> builtins.str:
        '''An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.

        For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-samlmetadatadocument
        '''
        result = self._values.get("saml_metadata_document")
        assert result is not None, "Required property 'saml_metadata_document' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the provider to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags that you want to attach to the new IAM SAML provider.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSAMLProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnServerCertificate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnServerCertificate",
):
    '''A CloudFormation ``AWS::IAM::ServerCertificate``.

    Uploads a server certificate entity for the AWS account . The server certificate entity includes a public key certificate, a private key, and an optional certificate chain, which should all be PEM-encoded.

    We recommend that you use `AWS Certificate Manager <https://docs.aws.amazon.com/acm/>`_ to provision, manage, and deploy your server certificates. With ACM you can request a certificate, deploy it to AWS resources, and let ACM handle certificate renewals for you. Certificates provided by ACM are free. For more information about using ACM, see the `AWS Certificate Manager User Guide <https://docs.aws.amazon.com/acm/latest/userguide/>`_ .

    For more information about working with server certificates, see `Working with server certificates <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`_ in the *IAM User Guide* . This topic includes a list of AWS services that can use the server certificates that you manage with IAM.

    For information about the number of server certificates you can upload, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       Because the body of the public key certificate, private key, and the certificate chain can be large, you should use POST rather than GET when calling ``UploadServerCertificate`` . For information about setting up signatures and authorization through the API, see `Signing AWS API requests <https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html>`_ in the *AWS General Reference* . For general information about using the Query API with IAM, see `Calling the API by making HTTP query requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/programming.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::ServerCertificate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        cfn_server_certificate = iam.CfnServerCertificate(self, "MyCfnServerCertificate",
            certificate_body="certificateBody",
            certificate_chain="certificateChain",
            path="path",
            private_key="privateKey",
            server_certificate_name="serverCertificateName",
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
        certificate_body: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        server_certificate_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::ServerCertificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_body: The contents of the public key certificate.
        :param certificate_chain: The contents of the public key certificate chain.
        :param path: The path for the server certificate. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).
        :param private_key: The contents of the private key in PEM-encoded format. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param server_certificate_name: The name for the server certificate. Do not include the path in this value. The name of the certificate cannot contain any spaces. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that are attached to the server certificate. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cd82141ea6355567bc319b1fe2b2203f37f59540405b28851d1ab9fededcea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServerCertificateProps(
            certificate_body=certificate_body,
            certificate_chain=certificate_chain,
            path=path,
            private_key=private_key,
            server_certificate_name=server_certificate_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fabbaf3c54b332f1efcff2fc31539d4a4b3635017217ee1e16a7663723bd9fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0c856c41abeabb83d77254a5dd612869bed959ba0890ef797b94d1cda690737)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::ServerCertificate`` resource.

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
        '''A list of tags that are attached to the server certificate.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="certificateBody")
    def certificate_body(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatebody
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateBody"))

    @certificate_body.setter
    def certificate_body(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b56584bea6da770dc90f791cc3021e6209b63e7a7a3b0e75bb27aba3420b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateBody", value)

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate chain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatechain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54da6c0bae8473a1e96681fd895db465ac1c31f1499e129fe217f67982ed5953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the server certificate.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d6615c145581b22b8b38012d8276a84e75437939bbfe03cac719994df8f404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The contents of the private key in PEM-encoded format.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430aa87a52c8287e859646c8f91284c1312380f1592e581741b8b249cd44ee36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="serverCertificateName")
    def server_certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name for the server certificate.

        Do not include the path in this value. The name of the certificate cannot contain any spaces.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-servercertificatename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverCertificateName"))

    @server_certificate_name.setter
    def server_certificate_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20a33fac28932709bae8ec0bd7663167891cad2bf7bcab7c9b4219e33ca8546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCertificateName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnServerCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_body": "certificateBody",
        "certificate_chain": "certificateChain",
        "path": "path",
        "private_key": "privateKey",
        "server_certificate_name": "serverCertificateName",
        "tags": "tags",
    },
)
class CfnServerCertificateProps:
    def __init__(
        self,
        *,
        certificate_body: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        server_certificate_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServerCertificate``.

        :param certificate_body: The contents of the public key certificate.
        :param certificate_chain: The contents of the public key certificate chain.
        :param path: The path for the server certificate. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).
        :param private_key: The contents of the private key in PEM-encoded format. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param server_certificate_name: The name for the server certificate. Do not include the path in this value. The name of the certificate cannot contain any spaces. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that are attached to the server certificate. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            cfn_server_certificate_props = iam.CfnServerCertificateProps(
                certificate_body="certificateBody",
                certificate_chain="certificateChain",
                path="path",
                private_key="privateKey",
                server_certificate_name="serverCertificateName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1b05b92f28b40d20becb202eb7f404df49537aa800d0c58abbd24875e06840)
            check_type(argname="argument certificate_body", value=certificate_body, expected_type=type_hints["certificate_body"])
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument server_certificate_name", value=server_certificate_name, expected_type=type_hints["server_certificate_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_body is not None:
            self._values["certificate_body"] = certificate_body
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if path is not None:
            self._values["path"] = path
        if private_key is not None:
            self._values["private_key"] = private_key
        if server_certificate_name is not None:
            self._values["server_certificate_name"] = server_certificate_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_body(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatebody
        '''
        result = self._values.get("certificate_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate chain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatechain
        '''
        result = self._values.get("certificate_chain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the server certificate.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The contents of the private key in PEM-encoded format.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name for the server certificate.

        Do not include the path in this value. The name of the certificate cannot contain any spaces.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-servercertificatename
        '''
        result = self._values.get("server_certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags that are attached to the server certificate.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnServiceLinkedRole(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnServiceLinkedRole",
):
    '''A CloudFormation ``AWS::IAM::ServiceLinkedRole``.

    Creates an IAM role that is linked to a specific AWS service. The service controls the attached policies and when the role can be deleted. This helps ensure that the service is not broken by an unexpectedly changed or deleted role, which could put your AWS resources into an unknown state. Allowing the service to control the role helps improve service stability and proper cleanup when a service and its role are no longer needed. For more information, see `Using service-linked roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html>`_ in the *IAM User Guide* .

    To attach a policy to this service-linked role, you must make the request using the AWS service that depends on this role.

    :cloudformationResource: AWS::IAM::ServiceLinkedRole
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
    :exampleMetadata: infused

    Example::

        slr = iam.CfnServiceLinkedRole(self, "ElasticSLR",
            aws_service_name="es.amazonaws.com"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        aws_service_name: builtins.str,
        custom_suffix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::ServiceLinkedRole``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param aws_service_name: The service principal for the AWS service to which this role is attached. You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` . Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.
        :param custom_suffix: A string that you provide, which is combined with the service-provided prefix to form the complete role name. If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix. Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.
        :param description: The description of the role.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9c457397f8d73807e52c34de324915223e172462011ef0b9fbb4679047dff2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceLinkedRoleProps(
            aws_service_name=aws_service_name,
            custom_suffix=custom_suffix,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa81902f3634794fbba9a0a17e9b04bb4785c72d5ea8279252a333070da4bb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__415a69be8c7687f580e2fec8645c0ec4b6fb6161e226e8ca9193054d418fb85e)
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
    @jsii.member(jsii_name="awsServiceName")
    def aws_service_name(self) -> builtins.str:
        '''The service principal for the AWS service to which this role is attached.

        You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` .

        Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-awsservicename
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsServiceName"))

    @aws_service_name.setter
    def aws_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7639b31b7544076a3afb9ce56a6d1f745ea9949a1a30fd8ed9695d65a2794b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsServiceName", value)

    @builtins.property
    @jsii.member(jsii_name="customSuffix")
    def custom_suffix(self) -> typing.Optional[builtins.str]:
        '''A string that you provide, which is combined with the service-provided prefix to form the complete role name.

        If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix.

        Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-customsuffix
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customSuffix"))

    @custom_suffix.setter
    def custom_suffix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57de2588b87139ce77be8f2ec0d3e4dc9cf32a682e08e38abcfb0e220f4700e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace96d55f7a9e12f6b0c1eab1597d57aea340c6ff0c90d46c267da74c2b4d3a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnServiceLinkedRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_service_name": "awsServiceName",
        "custom_suffix": "customSuffix",
        "description": "description",
    },
)
class CfnServiceLinkedRoleProps:
    def __init__(
        self,
        *,
        aws_service_name: builtins.str,
        custom_suffix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceLinkedRole``.

        :param aws_service_name: The service principal for the AWS service to which this role is attached. You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` . Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.
        :param custom_suffix: A string that you provide, which is combined with the service-provided prefix to form the complete role name. If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix. Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.
        :param description: The description of the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
        :exampleMetadata: infused

        Example::

            slr = iam.CfnServiceLinkedRole(self, "ElasticSLR",
                aws_service_name="es.amazonaws.com"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c9b5f7c3adb35711c582f832e2278f409957d357b28fb87606914f7226bd39)
            check_type(argname="argument aws_service_name", value=aws_service_name, expected_type=type_hints["aws_service_name"])
            check_type(argname="argument custom_suffix", value=custom_suffix, expected_type=type_hints["custom_suffix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_service_name": aws_service_name,
        }
        if custom_suffix is not None:
            self._values["custom_suffix"] = custom_suffix
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def aws_service_name(self) -> builtins.str:
        '''The service principal for the AWS service to which this role is attached.

        You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` .

        Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-awsservicename
        '''
        result = self._values.get("aws_service_name")
        assert result is not None, "Required property 'aws_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_suffix(self) -> typing.Optional[builtins.str]:
        '''A string that you provide, which is combined with the service-provided prefix to form the complete role name.

        If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix.

        Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-customsuffix
        '''
        result = self._values.get("custom_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceLinkedRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnUser(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnUser",
):
    '''A CloudFormation ``AWS::IAM::User``.

    Creates a new IAM user for your AWS account .

    For information about quotas for the number of IAM users you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # policy_document: Any
        
        cfn_user = iam.CfnUser(self, "MyCfnUser",
            groups=["groups"],
            login_profile=iam.CfnUser.LoginProfileProperty(
                password="password",
        
                # the properties below are optional
                password_reset_required=False
            ),
            managed_policy_arns=["managedPolicyArns"],
            path="path",
            permissions_boundary="permissionsBoundary",
            policies=[iam.CfnUser.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_name="userName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_profile: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnUser.LoginProfileProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnUser.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param groups: A list of group names to which you want to add the user.
        :param login_profile: Creates a password for the specified IAM user. A password allows an IAM user to access AWS services through the AWS Management Console . You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console . For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path for the user name. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the managed policy that is used to set the permissions boundary for the user. A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* . For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM user. To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ . .. epigraph:: The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        :param tags: A list of tags that you want to attach to the new user. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param user_name: The name of the user to create. Do not include the path in this value. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d3dd58f27d1d8e709d36cb51a4600afb8243e6c2101e832629874c3bf74414)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            groups=groups,
            login_profile=login_profile,
            managed_policy_arns=managed_policy_arns,
            path=path,
            permissions_boundary=permissions_boundary,
            policies=policies,
            tags=tags,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2398f45a3f7a4e911de2f808b00634f074f5a280db21237dc439e86daf62d2ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e8047352af7d4214a63ff9f4d8c2c0363d3429a2708de78bb67427ceaf971c2)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::User`` resource.

        For example: ``arn:aws:iam::123456789012:user/mystack-myuser-1CCXAFG2H2U4D`` .

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
        '''A list of tags that you want to attach to the new user.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of group names to which you want to add the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-groups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d88ed2617b5090b2a6eb2ca7b9e7bb0e53828ea13522ec7359711a3485ca6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="loginProfile")
    def login_profile(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.LoginProfileProperty"]]:
        '''Creates a password for the specified IAM user.

        A password allows an IAM user to access AWS services through the AWS Management Console .

        You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console .

        For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-loginprofile
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.LoginProfileProperty"]], jsii.get(self, "loginProfile"))

    @login_profile.setter
    def login_profile(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.LoginProfileProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddc2ec817dc66d81c9d457ef7449ce29220048e088caa0356e911120ae38fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginProfile", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-managepolicyarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managedPolicyArns"))

    @managed_policy_arns.setter
    def managed_policy_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78eb07ccf26a62787fb26b2d61e8319e5a80da4e6dfb4cf5dae978520a6710ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the user name.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7629f315b417f7cf63fbec0abbe4b2fba0e28654641f3a7e43c129d9003140c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the managed policy that is used to set the permissions boundary for the user.

        A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-permissionsboundary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundary"))

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8647130c8721eb12e608b6fa0f887311da5518d9d3f2c7361293def7065102e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.PolicyProperty"]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM user.

        To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ .
        .. epigraph::

           The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-policies
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.PolicyProperty"]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.PolicyProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eeeae1c0ee5573c8f6828270a73d8028e1dfe05fb65de0520d6c0dcf09d7eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user to create. Do not include the path in this value.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-username
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee6ff12d58390aca893e9061e4663303463fc7faec174f0ead590a5578903d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iam.CfnUser.LoginProfileProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "password_reset_required": "passwordResetRequired",
        },
    )
    class LoginProfileProperty:
        def __init__(
            self,
            *,
            password: builtins.str,
            password_reset_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Creates a password for the specified user, giving the user the ability to access AWS services through the AWS Management Console .

            For more information about managing passwords, see `Managing Passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

            :param password: The user's password.
            :param password_reset_required: Specifies whether the user is required to set a new password on next sign-in.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iam as iam
                
                login_profile_property = iam.CfnUser.LoginProfileProperty(
                    password="password",
                
                    # the properties below are optional
                    password_reset_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae6f98a39b2c2196cf0e1286024bc9e868a2ee7f516604e1eff049fc5aa6c3bc)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument password_reset_required", value=password_reset_required, expected_type=type_hints["password_reset_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
            }
            if password_reset_required is not None:
                self._values["password_reset_required"] = password_reset_required

        @builtins.property
        def password(self) -> builtins.str:
            '''The user's password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def password_reset_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether the user is required to set a new password on next sign-in.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-passwordresetrequired
            '''
            result = self._values.get("password_reset_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoginProfileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iam.CfnUser.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any,
            policy_name: builtins.str,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, refer to `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The entire contents of the policy that defines permissions. For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iam as iam
                
                # policy_document: Any
                
                policy_property = iam.CfnUser.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c990e121f3865cf05866339719021ab0d1b2a4316fd082823896e43d0d789da6)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_document": policy_document,
                "policy_name": policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The entire contents of the policy that defines permissions.

            For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            '''
            result = self._values.get("policy_document")
            assert result is not None, "Required property 'policy_document' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "groups": "groups",
        "login_profile": "loginProfile",
        "managed_policy_arns": "managedPolicyArns",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "tags": "tags",
        "user_name": "userName",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_profile: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.LoginProfileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param groups: A list of group names to which you want to add the user.
        :param login_profile: Creates a password for the specified IAM user. A password allows an IAM user to access AWS services through the AWS Management Console . You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console . For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path for the user name. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the managed policy that is used to set the permissions boundary for the user. A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* . For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM user. To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ . .. epigraph:: The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        :param tags: A list of tags that you want to attach to the new user. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param user_name: The name of the user to create. Do not include the path in this value. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # policy_document: Any
            
            cfn_user_props = iam.CfnUserProps(
                groups=["groups"],
                login_profile=iam.CfnUser.LoginProfileProperty(
                    password="password",
            
                    # the properties below are optional
                    password_reset_required=False
                ),
                managed_policy_arns=["managedPolicyArns"],
                path="path",
                permissions_boundary="permissionsBoundary",
                policies=[iam.CfnUser.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2f2cc6b4f4550946b5d6d7176e1cd03666697b01d8c186bd975d069253e6e1)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument login_profile", value=login_profile, expected_type=type_hints["login_profile"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if login_profile is not None:
            self._values["login_profile"] = login_profile
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if tags is not None:
            self._values["tags"] = tags
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of group names to which you want to add the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_profile(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.LoginProfileProperty]]:
        '''Creates a password for the specified IAM user.

        A password allows an IAM user to access AWS services through the AWS Management Console .

        You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console .

        For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-loginprofile
        '''
        result = self._values.get("login_profile")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.LoginProfileProperty]], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-managepolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the user name.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the managed policy that is used to set the permissions boundary for the user.

        A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.PolicyProperty]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM user.

        To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ .
        .. epigraph::

           The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.PolicyProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags that you want to attach to the new user.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user to create. Do not include the path in this value.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnUserToGroupAddition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnUserToGroupAddition",
):
    '''A CloudFormation ``AWS::IAM::UserToGroupAddition``.

    Adds the specified user to the specified group.

    :cloudformationResource: AWS::IAM::UserToGroupAddition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        cfn_user_to_group_addition = iam.CfnUserToGroupAddition(self, "MyCfnUserToGroupAddition",
            group_name="groupName",
            users=["users"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        group_name: builtins.str,
        users: typing.Sequence[builtins.str],
    ) -> None:
        '''Create a new ``AWS::IAM::UserToGroupAddition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: The name of the group to update. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param users: A list of the names of the users that you want to add to the group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e21103b6d2b9e4cb45590a6b552238202915f4bf4de2a94fa11ea06ea7abf3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserToGroupAdditionProps(group_name=group_name, users=users)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f592bca0c422bf0da5a558e6dbf00521f0acb93d7bb2bd989cfc93d6cd1f83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40bd028a6468e999067863fd39eccd1eff7b2ca135753f53ff810aec4aeff5ab)
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
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''The name of the group to update.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-groupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07df7e49e6ac358cbdbaf168473a69aeb005aebb726c6c1fbf177b03478bbee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        '''A list of the names of the users that you want to add to the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-users
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478f6d094573da9b31689ae02c56352f8662729751c552faeaba3d824adb99aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnUserToGroupAdditionProps",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName", "users": "users"},
)
class CfnUserToGroupAdditionProps:
    def __init__(
        self,
        *,
        group_name: builtins.str,
        users: typing.Sequence[builtins.str],
    ) -> None:
        '''Properties for defining a ``CfnUserToGroupAddition``.

        :param group_name: The name of the group to update. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param users: A list of the names of the users that you want to add to the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            cfn_user_to_group_addition_props = iam.CfnUserToGroupAdditionProps(
                group_name="groupName",
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a659b0fc99fe7eb7e5fba845551db31be9b1bb584be89b92a8bf8b52093cc0f)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
            "users": users,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        '''The name of the group to update.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-groupname
        '''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def users(self) -> typing.List[builtins.str]:
        '''A list of the names of the users that you want to add to the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-users
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserToGroupAdditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVirtualMFADevice(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CfnVirtualMFADevice",
):
    '''A CloudFormation ``AWS::IAM::VirtualMFADevice``.

    Creates a new virtual MFA device for the AWS account . After creating the virtual MFA, use `EnableMFADevice <https://docs.aws.amazon.com/IAM/latest/APIReference/API_EnableMFADevice.html>`_ to attach the MFA device to an IAM user. For more information about creating and working with virtual MFA devices, see `Using a virtual MFA device <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_VirtualMFA.html>`_ in the *IAM User Guide* .

    For information about the maximum number of MFA devices you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       The seed information contained in the QR code and the Base32 string should be treated like any other secret access information. In other words, protect the seed information as you would your AWS access keys or your passwords. After you provision your virtual device, you should ensure that the information is destroyed following secure procedures.

    :cloudformationResource: AWS::IAM::VirtualMFADevice
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        cfn_virtual_mFADevice = iam.CfnVirtualMFADevice(self, "MyCfnVirtualMFADevice",
            users=["users"],
        
            # the properties below are optional
            path="path",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_mfa_device_name="virtualMfaDeviceName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        users: typing.Sequence[builtins.str],
        path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_mfa_device_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::VirtualMFADevice``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param users: The IAM user associated with this virtual MFA device.
        :param path: The path for the virtual MFA device. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param tags: A list of tags that you want to attach to the new IAM virtual MFA device. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param virtual_mfa_device_name: The name of the virtual MFA device, which must be unique. Use with path to uniquely identify a virtual MFA device. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3403f08c73f1980bec4173c88d8530bef1e628771b1c0cdb6eb85e3a086dc5a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVirtualMFADeviceProps(
            users=users,
            path=path,
            tags=tags,
            virtual_mfa_device_name=virtual_mfa_device_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5894ada85a21a17dca4bdf04bde1bcc5bbe810ff08f9c57eeb0b0cbdadd33ad2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd6f5b00cb555552851e4c561f485c8816a4fe1afa3b3769b8bbb64a7059bb87)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSerialNumber")
    def attr_serial_number(self) -> builtins.str:
        '''Returns the serial number for the specified ``AWS::IAM::VirtualMFADevice`` resource.

        :cloudformationAttribute: SerialNumber
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSerialNumber"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of tags that you want to attach to the new IAM virtual MFA device.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        '''The IAM user associated with this virtual MFA device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-users
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab0cd4b6cfc16f8435ab6a9868cb6ad51c88488fe7d6b157574690bedb1a0e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the virtual MFA device.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d15db6ecc07b7c414a88d5a8d3f73fbd5016555d499a54d0b4247cd35b248a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="virtualMfaDeviceName")
    def virtual_mfa_device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual MFA device, which must be unique.

        Use with path to uniquely identify a virtual MFA device.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-virtualmfadevicename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMfaDeviceName"))

    @virtual_mfa_device_name.setter
    def virtual_mfa_device_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cc407504f6903d73f2cb88aa0db80515592dcde339bf20579699bd3ba9bb4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMfaDeviceName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CfnVirtualMFADeviceProps",
    jsii_struct_bases=[],
    name_mapping={
        "users": "users",
        "path": "path",
        "tags": "tags",
        "virtual_mfa_device_name": "virtualMfaDeviceName",
    },
)
class CfnVirtualMFADeviceProps:
    def __init__(
        self,
        *,
        users: typing.Sequence[builtins.str],
        path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_mfa_device_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnVirtualMFADevice``.

        :param users: The IAM user associated with this virtual MFA device.
        :param path: The path for the virtual MFA device. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param tags: A list of tags that you want to attach to the new IAM virtual MFA device. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param virtual_mfa_device_name: The name of the virtual MFA device, which must be unique. Use with path to uniquely identify a virtual MFA device. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            cfn_virtual_mFADevice_props = iam.CfnVirtualMFADeviceProps(
                users=["users"],
            
                # the properties below are optional
                path="path",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_mfa_device_name="virtualMfaDeviceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555c031cad888108e49ac8e771b5195d9a951c9a2707000d35cd98096d183cdb)
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_mfa_device_name", value=virtual_mfa_device_name, expected_type=type_hints["virtual_mfa_device_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "users": users,
        }
        if path is not None:
            self._values["path"] = path
        if tags is not None:
            self._values["tags"] = tags
        if virtual_mfa_device_name is not None:
            self._values["virtual_mfa_device_name"] = virtual_mfa_device_name

    @builtins.property
    def users(self) -> typing.List[builtins.str]:
        '''The IAM user associated with this virtual MFA device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-users
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the virtual MFA device.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of tags that you want to attach to the new IAM virtual MFA device.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def virtual_mfa_device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual MFA device, which must be unique.

        Use with path to uniquely identify a virtual MFA device.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-virtualmfadevicename
        '''
        result = self._values.get("virtual_mfa_device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualMFADeviceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.CommonGrantOptions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
    },
)
class CommonGrantOptions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''Basic options for a grant operation.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # grantable: iam.IGrantable
            
            common_grant_options = iam.CommonGrantOptions(
                actions=["actions"],
                grantee=grantable,
                resource_arns=["resourceArns"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80c243305a2120343036db9aac3ad9d03fa7f24316bdcd867921cae2d30a5bf)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''The actions to grant.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''The principal to grant to.

        :default: if principal is undefined, no work is done.
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''The resource ARNs to grant to.'''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonGrantOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComparablePrincipal(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.ComparablePrincipal",
):
    '''Helper class for working with ``IComparablePrincipal``s.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        comparable_principal = iam.ComparablePrincipal()
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="dedupeStringFor")
    @builtins.classmethod
    def dedupe_string_for(cls, x: "IPrincipal") -> typing.Optional[builtins.str]:
        '''Return the dedupeString of the given principal, if available.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feca08928fe78692eb852482844809c53b740556f35309f719722e4aafff0e06)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "dedupeStringFor", [x]))

    @jsii.member(jsii_name="isComparablePrincipal")
    @builtins.classmethod
    def is_comparable_principal(cls, x: "IPrincipal") -> builtins.bool:
        '''Whether or not the given principal is a comparable principal.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5a72947168d3b6e1aa60ee5367b2d93ee05c6cdbceeaf5fbd17c379bedfe3e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isComparablePrincipal", [x]))


@jsii.implements(_aws_cdk_core_f4b25747.IDependable)
class CompositeDependable(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CompositeDependable",
):
    '''Composite dependable.

    Not as simple as eagerly getting the dependency roots from the
    inner dependables, as they may be mutable so we need to defer
    the query.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import aws_cdk.core as cdk
        
        # dependable: cdk.IDependable
        
        composite_dependable = iam.CompositeDependable(dependable)
    '''

    def __init__(self, *dependables: _aws_cdk_core_f4b25747.IDependable) -> None:
        '''
        :param dependables: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dad6afeb9a260846d8c4772b9f0c830e599b888951cb7e6cc643004d7e47b43)
            check_type(argname="argument dependables", value=dependables, expected_type=typing.Tuple[type_hints["dependables"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*dependables])


@jsii.enum(jsii_type="@aws-cdk/aws-iam.Effect")
class Effect(enum.Enum):
    '''The Effect element of an IAM policy.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_effect.html
    :exampleMetadata: infused

    Example::

        # books: apigateway.Resource
        # iam_user: iam.User
        
        
        get_books = books.add_method("GET", apigateway.HttpIntegration("http://amazon.com"),
            authorization_type=apigateway.AuthorizationType.IAM
        )
        
        iam_user.attach_inline_policy(iam.Policy(self, "AllowBooks",
            statements=[
                iam.PolicyStatement(
                    actions=["execute-api:Invoke"],
                    effect=iam.Effect.ALLOW,
                    resources=[get_books.method_arn]
                )
            ]
        ))
    '''

    ALLOW = "ALLOW"
    '''Allows access to a resource in an IAM policy statement.

    By default, access to resources are denied.
    '''
    DENY = "DENY"
    '''Explicitly deny access to a resource.

    By default, all requests are denied implicitly.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.FromRoleArnOptions",
    jsii_struct_bases=[],
    name_mapping={
        "add_grants_to_resources": "addGrantsToResources",
        "mutable": "mutable",
    },
)
class FromRoleArnOptions:
    def __init__(
        self,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options allowing customizing the behavior of {@link Role.fromRoleArn}.

        :param add_grants_to_resources: For immutable roles: add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false
        :param mutable: Whether the imported role can be modified by attaching policy resources to it. Default: true

        :exampleMetadata: infused

        Example::

            role = iam.Role.from_role_arn(self, "Role", "arn:aws:iam::123456789012:role/MyExistingRole",
                # Set 'mutable' to 'false' to use the role as-is and prevent adding new
                # policies to it. The default is 'true', which means the role may be
                # modified as part of the deployment.
                mutable=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118646118fff9e9879f4eed824ef5eb94da275d0f04853ea376fd5bc3837faa2)
            check_type(argname="argument add_grants_to_resources", value=add_grants_to_resources, expected_type=type_hints["add_grants_to_resources"])
            check_type(argname="argument mutable", value=mutable, expected_type=type_hints["mutable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_grants_to_resources is not None:
            self._values["add_grants_to_resources"] = add_grants_to_resources
        if mutable is not None:
            self._values["mutable"] = mutable

    @builtins.property
    def add_grants_to_resources(self) -> typing.Optional[builtins.bool]:
        '''For immutable roles: add grants to resources instead of dropping them.

        If this is ``false`` or not specified, grant permissions added to this role are ignored.
        It is your own responsibility to make sure the role has the required permissions.

        If this is ``true``, any grant permissions will be added to the resource instead.

        :default: false
        '''
        result = self._values.get("add_grants_to_resources")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        '''Whether the imported role can be modified by attaching policy resources to it.

        :default: true
        '''
        result = self._values.get("mutable")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FromRoleArnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IDependable)
class Grant(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iam.Grant"):
    '''Result of a grant() operation.

    This class is not instantiable by consumers on purpose, so that they will be
    required to call the Grant factory functions.

    :exampleMetadata: infused

    Example::

        # instance: ec2.Instance
        # volume: ec2.Volume
        
        
        attach_grant = volume.grant_attach_volume_by_resource_tag(instance.grant_principal, [instance])
        detach_grant = volume.grant_detach_volume_by_resource_tag(instance.grant_principal, [instance])
    '''

    @jsii.member(jsii_name="addToPrincipal")
    @builtins.classmethod
    def add_to_principal(
        cls,
        *,
        scope: typing.Optional[_aws_cdk_core_f4b25747.IConstruct] = None,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> "Grant":
        '''Try to grant the given permissions to the given principal.

        Absence of a principal leads to a warning, but failing to add
        the permissions to a present principal is not an error.

        :param scope: Construct to report warnings on in case grant could not be registered. Default: - the construct in which this construct is defined
        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        '''
        options = GrantOnPrincipalOptions(
            scope=scope, actions=actions, grantee=grantee, resource_arns=resource_arns
        )

        return typing.cast("Grant", jsii.sinvoke(cls, "addToPrincipal", [options]))

    @jsii.member(jsii_name="addToPrincipalAndResource")
    @builtins.classmethod
    def add_to_principal_and_resource(
        cls,
        *,
        resource: "IResourceWithPolicy",
        resource_policy_principal: typing.Optional["IPrincipal"] = None,
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> "Grant":
        '''Add a grant both on the principal and on the resource.

        As long as any principal is given, granting on the principal may fail (in
        case of a non-identity principal), but granting on the resource will
        never fail.

        Statement will be the resource statement.

        :param resource: The resource with a resource policy. The statement will always be added to the resource policy.
        :param resource_policy_principal: The principal to use in the statement for the resource policy. Default: - the principal of the grantee will be used
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs
        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        '''
        options = GrantOnPrincipalAndResourceOptions(
            resource=resource,
            resource_policy_principal=resource_policy_principal,
            resource_self_arns=resource_self_arns,
            actions=actions,
            grantee=grantee,
            resource_arns=resource_arns,
        )

        return typing.cast("Grant", jsii.sinvoke(cls, "addToPrincipalAndResource", [options]))

    @jsii.member(jsii_name="addToPrincipalOrResource")
    @builtins.classmethod
    def add_to_principal_or_resource(
        cls,
        *,
        resource: "IResourceWithPolicy",
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> "Grant":
        '''Grant the given permissions to the principal.

        The permissions will be added to the principal policy primarily, falling
        back to the resource policy if necessary. The permissions must be granted
        somewhere.

        - Trying to grant permissions to a principal that does not admit adding to
          the principal policy while not providing a resource with a resource policy
          is an error.
        - Trying to grant permissions to an absent principal (possible in the
          case of imported resources) leads to a warning being added to the
          resource construct.

        :param resource: The resource with a resource policy. The statement will be added to the resource policy if it couldn't be added to the principal policy.
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs
        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        '''
        options = GrantWithResourceOptions(
            resource=resource,
            resource_self_arns=resource_self_arns,
            actions=actions,
            grantee=grantee,
            resource_arns=resource_arns,
        )

        return typing.cast("Grant", jsii.sinvoke(cls, "addToPrincipalOrResource", [options]))

    @jsii.member(jsii_name="drop")
    @builtins.classmethod
    def drop(cls, grantee: "IGrantable", _intent: builtins.str) -> "Grant":
        '''Returns a "no-op" ``Grant`` object which represents a "dropped grant".

        This can be used for e.g. imported resources where you may not be able to modify
        the resource's policy or some underlying policy which you don't know about.

        :param grantee: The intended grantee.
        :param _intent: The user's intent (will be ignored at the moment).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f55cf91f13b36d92fcdd7df44173b96a31de327d4247ee3bcd16e28ba617c46)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument _intent", value=_intent, expected_type=type_hints["_intent"])
        return typing.cast("Grant", jsii.sinvoke(cls, "drop", [grantee, _intent]))

    @jsii.member(jsii_name="applyBefore")
    def apply_before(self, *constructs: _aws_cdk_core_f4b25747.IConstruct) -> None:
        '''Make sure this grant is applied before the given constructs are deployed.

        The same as construct.node.addDependency(grant), but slightly nicer to read.

        :param constructs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4761013e67f613e450e8a418b92020eb8d035754f9897a837460850a2fe29ff)
            check_type(argname="argument constructs", value=constructs, expected_type=typing.Tuple[type_hints["constructs"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "applyBefore", [*constructs]))

    @jsii.member(jsii_name="assertSuccess")
    def assert_success(self) -> None:
        '''Throw an error if this grant wasn't successful.'''
        return typing.cast(None, jsii.invoke(self, "assertSuccess", []))

    @builtins.property
    @jsii.member(jsii_name="success")
    def success(self) -> builtins.bool:
        '''Whether the grant operation was successful.'''
        return typing.cast(builtins.bool, jsii.get(self, "success"))

    @builtins.property
    @jsii.member(jsii_name="principalStatement")
    def principal_statement(self) -> typing.Optional["PolicyStatement"]:
        '''The statement that was added to the principal's policy.

        Can be accessed to (e.g.) add additional conditions to the statement.
        '''
        return typing.cast(typing.Optional["PolicyStatement"], jsii.get(self, "principalStatement"))

    @builtins.property
    @jsii.member(jsii_name="resourceStatement")
    def resource_statement(self) -> typing.Optional["PolicyStatement"]:
        '''The statement that was added to the resource policy.

        Can be accessed to (e.g.) add additional conditions to the statement.
        '''
        return typing.cast(typing.Optional["PolicyStatement"], jsii.get(self, "resourceStatement"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.GrantOnPrincipalAndResourceOptions",
    jsii_struct_bases=[CommonGrantOptions],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
        "resource": "resource",
        "resource_policy_principal": "resourcePolicyPrincipal",
        "resource_self_arns": "resourceSelfArns",
    },
)
class GrantOnPrincipalAndResourceOptions(CommonGrantOptions):
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
        resource: "IResourceWithPolicy",
        resource_policy_principal: typing.Optional["IPrincipal"] = None,
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options for a grant operation to both identity and resource.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        :param resource: The resource with a resource policy. The statement will always be added to the resource policy.
        :param resource_policy_principal: The principal to use in the statement for the resource policy. Default: - the principal of the grantee will be used
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # grantable: iam.IGrantable
            # principal: iam.IPrincipal
            # resource_with_policy: iam.IResourceWithPolicy
            
            grant_on_principal_and_resource_options = iam.GrantOnPrincipalAndResourceOptions(
                actions=["actions"],
                grantee=grantable,
                resource=resource_with_policy,
                resource_arns=["resourceArns"],
            
                # the properties below are optional
                resource_policy_principal=principal,
                resource_self_arns=["resourceSelfArns"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5240e00ad90d35024787026562eb22cc617e4be010813eb82081bcab6b383c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_policy_principal", value=resource_policy_principal, expected_type=type_hints["resource_policy_principal"])
            check_type(argname="argument resource_self_arns", value=resource_self_arns, expected_type=type_hints["resource_self_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
            "resource": resource,
        }
        if resource_policy_principal is not None:
            self._values["resource_policy_principal"] = resource_policy_principal
        if resource_self_arns is not None:
            self._values["resource_self_arns"] = resource_self_arns

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''The actions to grant.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''The principal to grant to.

        :default: if principal is undefined, no work is done.
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''The resource ARNs to grant to.'''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource(self) -> "IResourceWithPolicy":
        '''The resource with a resource policy.

        The statement will always be added to the resource policy.
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast("IResourceWithPolicy", result)

    @builtins.property
    def resource_policy_principal(self) -> typing.Optional["IPrincipal"]:
        '''The principal to use in the statement for the resource policy.

        :default: - the principal of the grantee will be used
        '''
        result = self._values.get("resource_policy_principal")
        return typing.cast(typing.Optional["IPrincipal"], result)

    @builtins.property
    def resource_self_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When referring to the resource in a resource policy, use this as ARN.

        (Depending on the resource type, this needs to be '*' in a resource policy).

        :default: Same as regular resource ARNs
        '''
        result = self._values.get("resource_self_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOnPrincipalAndResourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.GrantOnPrincipalOptions",
    jsii_struct_bases=[CommonGrantOptions],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
        "scope": "scope",
    },
)
class GrantOnPrincipalOptions(CommonGrantOptions):
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
        scope: typing.Optional[_aws_cdk_core_f4b25747.IConstruct] = None,
    ) -> None:
        '''Options for a grant operation that only applies to principals.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        :param scope: Construct to report warnings on in case grant could not be registered. Default: - the construct in which this construct is defined

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.core as cdk
            
            # construct: cdk.Construct
            # grantable: iam.IGrantable
            
            grant_on_principal_options = iam.GrantOnPrincipalOptions(
                actions=["actions"],
                grantee=grantable,
                resource_arns=["resourceArns"],
            
                # the properties below are optional
                scope=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ed81a36fb6f343f7d3d4d71cae9df3f7b7ed222266f214c7e15e6fc22eb916)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
        }
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''The actions to grant.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''The principal to grant to.

        :default: if principal is undefined, no work is done.
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''The resource ARNs to grant to.'''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[_aws_cdk_core_f4b25747.IConstruct]:
        '''Construct to report warnings on in case grant could not be registered.

        :default: - the construct in which this construct is defined
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IConstruct], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOnPrincipalOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.GrantWithResourceOptions",
    jsii_struct_bases=[CommonGrantOptions],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
        "resource": "resource",
        "resource_self_arns": "resourceSelfArns",
    },
)
class GrantWithResourceOptions(CommonGrantOptions):
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
        resource: "IResourceWithPolicy",
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options for a grant operation.

        :param actions: The actions to grant.
        :param grantee: The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: The resource ARNs to grant to.
        :param resource: The resource with a resource policy. The statement will be added to the resource policy if it couldn't be added to the principal policy.
        :param resource_self_arns: When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # grantable: iam.IGrantable
            # resource_with_policy: iam.IResourceWithPolicy
            
            grant_with_resource_options = iam.GrantWithResourceOptions(
                actions=["actions"],
                grantee=grantable,
                resource=resource_with_policy,
                resource_arns=["resourceArns"],
            
                # the properties below are optional
                resource_self_arns=["resourceSelfArns"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99cc4cc6a10bf9d2bc27325326f4406ca09872d3e06130c542a2a17e841f3ed)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_self_arns", value=resource_self_arns, expected_type=type_hints["resource_self_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
            "resource": resource,
        }
        if resource_self_arns is not None:
            self._values["resource_self_arns"] = resource_self_arns

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''The actions to grant.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''The principal to grant to.

        :default: if principal is undefined, no work is done.
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''The resource ARNs to grant to.'''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource(self) -> "IResourceWithPolicy":
        '''The resource with a resource policy.

        The statement will be added to the resource policy if it couldn't be
        added to the principal policy.
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast("IResourceWithPolicy", result)

    @builtins.property
    def resource_self_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When referring to the resource in a resource policy, use this as ARN.

        (Depending on the resource type, this needs to be '*' in a resource policy).

        :default: Same as regular resource ARNs
        '''
        result = self._values.get("resource_self_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantWithResourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.GroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "managed_policies": "managedPolicies",
        "path": "path",
    },
)
class GroupProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policies: typing.Optional[typing.Sequence["IManagedPolicy"]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining an IAM group.

        :param group_name: A name for the IAM group. For valid values, see the GroupName parameter for the CreateGroup action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: Generated by CloudFormation (recommended)
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param path: The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_ in the IAM User Guide. Default: /

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # managed_policy: iam.ManagedPolicy
            
            group_props = iam.GroupProps(
                group_name="groupName",
                managed_policies=[managed_policy],
                path="path"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8144e7610672a1371486a23f5193a3506d0c6158e42ae9d2c6fdec2e9db510b)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM group.

        For valid values, see the GroupName parameter
        for the CreateGroup action in the IAM API Reference. If you don't specify
        a name, AWS CloudFormation generates a unique physical ID and uses that
        ID for the group name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default: Generated by CloudFormation (recommended)
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List["IManagedPolicy"]]:
        '''A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List["IManagedPolicy"]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the group.

        For more information about paths, see `IAM
        Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_
        in the IAM User Guide.

        :default: /
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IAccessKey")
class IAccessKey(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''Represents an IAM Access Key.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
    '''

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        '''The Access Key ID.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> _aws_cdk_core_f4b25747.SecretValue:
        '''The Secret Access Key.

        :attribute: true
        '''
        ...


class _IAccessKeyProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Represents an IAM Access Key.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IAccessKey"

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        '''The Access Key ID.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> _aws_cdk_core_f4b25747.SecretValue:
        '''The Secret Access Key.

        :attribute: true
        '''
        return typing.cast(_aws_cdk_core_f4b25747.SecretValue, jsii.get(self, "secretAccessKey"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccessKey).__jsii_proxy_class__ = lambda : _IAccessKeyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IGrantable")
class IGrantable(typing_extensions.Protocol):
    '''Any object that has an associated principal that a permission can be granted to.'''

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        '''The principal to grant permissions to.'''
        ...


class _IGrantableProxy:
    '''Any object that has an associated principal that a permission can be granted to.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IGrantable"

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        '''The principal to grant permissions to.'''
        return typing.cast("IPrincipal", jsii.get(self, "grantPrincipal"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGrantable).__jsii_proxy_class__ = lambda : _IGrantableProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IManagedPolicy")
class IManagedPolicy(typing_extensions.Protocol):
    '''A managed policy.'''

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> builtins.str:
        '''The ARN of the managed policy.

        :attribute: true
        '''
        ...


class _IManagedPolicyProxy:
    '''A managed policy.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IManagedPolicy"

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> builtins.str:
        '''The ARN of the managed policy.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedPolicyArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManagedPolicy).__jsii_proxy_class__ = lambda : _IManagedPolicyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IOpenIdConnectProvider")
class IOpenIdConnectProvider(
    _aws_cdk_core_f4b25747.IResource,
    typing_extensions.Protocol,
):
    '''Represents an IAM OpenID Connect provider.'''

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderArn")
    def open_id_connect_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM OpenID Connect provider.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderIssuer")
    def open_id_connect_provider_issuer(self) -> builtins.str:
        '''The issuer for OIDC Provider.'''
        ...


class _IOpenIdConnectProviderProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Represents an IAM OpenID Connect provider.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IOpenIdConnectProvider"

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderArn")
    def open_id_connect_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM OpenID Connect provider.'''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderArn"))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderIssuer")
    def open_id_connect_provider_issuer(self) -> builtins.str:
        '''The issuer for OIDC Provider.'''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderIssuer"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOpenIdConnectProvider).__jsii_proxy_class__ = lambda : _IOpenIdConnectProviderProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IPolicy")
class IPolicy(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''Represents an IAM Policy.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html
    '''

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of this policy.

        :attribute: true
        '''
        ...


class _IPolicyProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Represents an IAM Policy.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IPolicy"

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of this policy.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPolicy).__jsii_proxy_class__ = lambda : _IPolicyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IPrincipal")
class IPrincipal(IGrantable, typing_extensions.Protocol):
    '''Represents a logical IAM principal.

    An IPrincipal describes a logical entity that can perform AWS API calls
    against sets of resources, optionally under certain conditions.

    Examples of simple principals are IAM objects that you create, such
    as Users or Roles.

    An example of a more complex principals is a ``ServicePrincipal`` (such as
    ``new ServicePrincipal("sns.amazonaws.com")``, which represents the Simple
    Notifications Service).

    A single logical Principal may also map to a set of physical principals.
    For example, ``new OrganizationPrincipal('o-1234')`` represents all
    identities that are part of the given AWS Organization.
    '''

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        '''Return the policy fragment that identifies this principal in a Policy.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        ...

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> builtins.bool:
        '''(deprecated) Add to the policy of this principal.

        :param statement: -

        :return:

        true if the statement was added, false if the principal in
        question does not have a policy document to add the statement to.

        :deprecated: Use ``addToPrincipalPolicy`` instead.

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToPrincipalPolicyResult:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        ...


class _IPrincipalProxy(
    jsii.proxy_for(IGrantable), # type: ignore[misc]
):
    '''Represents a logical IAM principal.

    An IPrincipal describes a logical entity that can perform AWS API calls
    against sets of resources, optionally under certain conditions.

    Examples of simple principals are IAM objects that you create, such
    as Users or Roles.

    An example of a more complex principals is a ``ServicePrincipal`` (such as
    ``new ServicePrincipal("sns.amazonaws.com")``, which represents the Simple
    Notifications Service).

    A single logical Principal may also map to a set of physical principals.
    For example, ``new OrganizationPrincipal('o-1234')`` represents all
    identities that are part of the given AWS Organization.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IPrincipal"

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast("PrincipalPolicyFragment", jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> builtins.bool:
        '''(deprecated) Add to the policy of this principal.

        :param statement: -

        :return:

        true if the statement was added, false if the principal in
        question does not have a policy document to add the statement to.

        :deprecated: Use ``addToPrincipalPolicy`` instead.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be94004d36c6ccf929d56b50921aaa08f12fd4b36aff03724f30a2576afabdf)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToPrincipalPolicyResult:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d2dc41bf91a97a85e83ebf9fbced7c0a0993c1fa413d6a4bc8d01bd10d515d)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPrincipal).__jsii_proxy_class__ = lambda : _IPrincipalProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IResourceWithPolicy")
class IResourceWithPolicy(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''A resource with a resource policy that can be added to.'''

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToResourcePolicyResult:
        '''Add a statement to the resource's resource policy.

        :param statement: -
        '''
        ...


class _IResourceWithPolicyProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''A resource with a resource policy that can be added to.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IResourceWithPolicy"

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToResourcePolicyResult:
        '''Add a statement to the resource's resource policy.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3101adf8418762c0ef550bd95db42a41657d386de7d7a813402ecbbe5d3575d2)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceWithPolicy).__jsii_proxy_class__ = lambda : _IResourceWithPolicyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.ISamlProvider")
class ISamlProvider(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''A SAML provider.'''

    @builtins.property
    @jsii.member(jsii_name="samlProviderArn")
    def saml_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the provider.

        :attribute: true
        '''
        ...


class _ISamlProviderProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''A SAML provider.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.ISamlProvider"

    @builtins.property
    @jsii.member(jsii_name="samlProviderArn")
    def saml_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the provider.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "samlProviderArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISamlProvider).__jsii_proxy_class__ = lambda : _ISamlProviderProxy


@jsii.implements(IManagedPolicy)
class ManagedPolicy(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.ManagedPolicy",
):
    '''Managed policy.

    :exampleMetadata: infused

    Example::

        my_role = iam.Role(self, "My Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        
        fn = lambda_.Function(self, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_16_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            role=my_role
        )
        
        my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        document: typing.Optional["PolicyDocument"] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: A description of the managed policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed. Default: - empty
        :param document: Initial PolicyDocument to use for this ManagedPolicy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param managed_policy_name: The name of the managed policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - A name is automatically generated.
        :param path: The path for the policy. This parameter allows (through its regex pattern) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\\u0021) through the DEL character (\\u007F), including most punctuation characters, digits, and upper and lowercased letters. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: - "/"
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3225cc4e0f8f69f258239a228ad417ea6dea2cafc61e44523faa4936a40f8473)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ManagedPolicyProps(
            description=description,
            document=document,
            groups=groups,
            managed_policy_name=managed_policy_name,
            path=path,
            roles=roles,
            statements=statements,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAwsManagedPolicyName")
    @builtins.classmethod
    def from_aws_managed_policy_name(
        cls,
        managed_policy_name: builtins.str,
    ) -> IManagedPolicy:
        '''Import a managed policy from one of the policies that AWS manages.

        For this managed policy, you only need to know the name to be able to use it.

        Some managed policy names start with "service-role/", some start with
        "job-function/", and some don't start with anything. Include the
        prefix when constructing this object.

        :param managed_policy_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ca0bf5f67b2e0333106fd1ddb31099a017160cff348eb85e49658624e833c3)
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
        return typing.cast(IManagedPolicy, jsii.sinvoke(cls, "fromAwsManagedPolicyName", [managed_policy_name]))

    @jsii.member(jsii_name="fromManagedPolicyArn")
    @builtins.classmethod
    def from_managed_policy_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        managed_policy_arn: builtins.str,
    ) -> IManagedPolicy:
        '''Import an external managed policy by ARN.

        For this managed policy, you only need to know the ARN to be able to use it.
        This can be useful if you got the ARN from a CloudFormation Export.

        If the imported Managed Policy ARN is a Token (such as a
        ``CfnParameter.valueAsString`` or a ``Fn.importValue()``) *and* the referenced
        managed policy has a ``path`` (like ``arn:...:policy/AdminPolicy/AdminAllow``), the
        ``managedPolicyName`` property will not resolve to the correct value. Instead it
        will resolve to the first path component. We unfortunately cannot express
        the correct calculation of the full path name as a CloudFormation
        expression. In this scenario the Managed Policy ARN should be supplied without the
        ``path`` in order to resolve the correct managed policy resource.

        :param scope: construct scope.
        :param id: construct id.
        :param managed_policy_arn: the ARN of the managed policy to import.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f18dc25f63148092b66f1a0a7e4b01eaad4acd2edaa00f8d07e18e0d24aba5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_policy_arn", value=managed_policy_arn, expected_type=type_hints["managed_policy_arn"])
        return typing.cast(IManagedPolicy, jsii.sinvoke(cls, "fromManagedPolicyArn", [scope, id, managed_policy_arn]))

    @jsii.member(jsii_name="fromManagedPolicyName")
    @builtins.classmethod
    def from_managed_policy_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        managed_policy_name: builtins.str,
    ) -> IManagedPolicy:
        '''Import a customer managed policy from the managedPolicyName.

        For this managed policy, you only need to know the name to be able to use it.

        :param scope: -
        :param id: -
        :param managed_policy_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c0b4e1f3b803e535e5d207b1dbc6d60c5c7ac1c6743c4e231b8bfccf7836af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
        return typing.cast(IManagedPolicy, jsii.sinvoke(cls, "fromManagedPolicyName", [scope, id, managed_policy_name]))

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        '''Adds a statement to the policy document.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f351fb358e3ea248741489c402ca382cf140d52b7ec4a3454366d03b6b09a375)
            check_type(argname="argument statement", value=statement, expected_type=typing.Tuple[type_hints["statement"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addStatements", [*statement]))

    @jsii.member(jsii_name="attachToGroup")
    def attach_to_group(self, group: "IGroup") -> None:
        '''Attaches this policy to a group.

        :param group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d8669a04f27c8c1e416bff9e17f9ceb769f71560cc35cd6a145280271146b1)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "attachToGroup", [group]))

    @jsii.member(jsii_name="attachToRole")
    def attach_to_role(self, role: "IRole") -> None:
        '''Attaches this policy to a role.

        :param role: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33284e52b2fdf499b024f7f58ca36c5f1291b3ba2f6e35b649f36c4a56163864)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "attachToRole", [role]))

    @jsii.member(jsii_name="attachToUser")
    def attach_to_user(self, user: "IUser") -> None:
        '''Attaches this policy to a user.

        :param user: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfba60db4b1faad126f6fa61bcb991dca47a4c474af6d103fcec30648eb43ac)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "attachToUser", [user]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''The description of this policy.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "PolicyDocument":
        '''The policy document.'''
        return typing.cast("PolicyDocument", jsii.get(self, "document"))

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> builtins.str:
        '''Returns the ARN of this managed policy.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="managedPolicyName")
    def managed_policy_name(self) -> builtins.str:
        '''The name of this policy.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedPolicyName"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''The path of this policy.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.ManagedPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "document": "document",
        "groups": "groups",
        "managed_policy_name": "managedPolicyName",
        "path": "path",
        "roles": "roles",
        "statements": "statements",
        "users": "users",
    },
)
class ManagedPolicyProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        document: typing.Optional["PolicyDocument"] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''Properties for defining an IAM managed policy.

        :param description: A description of the managed policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed. Default: - empty
        :param document: Initial PolicyDocument to use for this ManagedPolicy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param managed_policy_name: The name of the managed policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - A name is automatically generated.
        :param path: The path for the policy. This parameter allows (through its regex pattern) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\\u0021) through the DEL character (\\u007F), including most punctuation characters, digits, and upper and lowercased letters. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: - "/"
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.

        :exampleMetadata: infused

        Example::

            policy_document = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Sid": "FirstStatement",
                    "Effect": "Allow",
                    "Action": ["iam:ChangePassword"],
                    "Resource": "*"
                }, {
                    "Sid": "SecondStatement",
                    "Effect": "Allow",
                    "Action": "s3:ListAllMyBuckets",
                    "Resource": "*"
                }, {
                    "Sid": "ThirdStatement",
                    "Effect": "Allow",
                    "Action": ["s3:List*", "s3:Get*"
                    ],
                    "Resource": ["arn:aws:s3:::confidential-data", "arn:aws:s3:::confidential-data/*"
                    ],
                    "Condition": {"Bool": {"aws:_multi_factor_auth_present": "true"}}
                }
                ]
            }
            
            custom_policy_document = iam.PolicyDocument.from_json(policy_document)
            
            # You can pass this document as an initial document to a ManagedPolicy
            # or inline Policy.
            new_managed_policy = iam.ManagedPolicy(self, "MyNewManagedPolicy",
                document=custom_policy_document
            )
            new_policy = iam.Policy(self, "MyNewPolicy",
                document=custom_policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4bf03e8d3d35225b12b08a40692e485e7fbeb0faac774b2a22fc17e194d19df)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if document is not None:
            self._values["document"] = document
        if groups is not None:
            self._values["groups"] = groups
        if managed_policy_name is not None:
            self._values["managed_policy_name"] = managed_policy_name
        if path is not None:
            self._values["path"] = path
        if roles is not None:
            self._values["roles"] = roles
        if statements is not None:
            self._values["statements"] = statements
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the managed policy.

        Typically used to store information about the
        permissions defined in the policy. For example, "Grants access to production DynamoDB tables."
        The policy description is immutable. After a value is assigned, it cannot be changed.

        :default: - empty
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document(self) -> typing.Optional["PolicyDocument"]:
        '''Initial PolicyDocument to use for this ManagedPolicy.

        If omited, any
        ``PolicyStatement`` provided in the ``statements`` property will be applied
        against the empty default ``PolicyDocument``.

        :default: - An empty policy.
        '''
        result = self._values.get("document")
        return typing.cast(typing.Optional["PolicyDocument"], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        '''Groups to attach this policy to.

        You can also use ``attachToGroup(group)`` to attach this policy to a group.

        :default: - No groups.
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List["IGroup"]], result)

    @builtins.property
    def managed_policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the managed policy.

        If you specify multiple policies for an entity,
        specify unique names. For example, if you specify a list of policies for
        an IAM role, each policy must have a unique name.

        :default: - A name is automatically generated.
        '''
        result = self._values.get("managed_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the policy.

        This parameter allows (through its regex pattern) a string of characters
        consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes.
        In addition, it can contain any ASCII character from the ! (\\u0021) through the DEL character (\\u007F),
        including most punctuation characters, digits, and upper and lowercased letters.

        For more information about paths, see IAM Identifiers in the IAM User Guide.

        :default: - "/"
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List["IRole"]]:
        '''Roles to attach this policy to.

        You can also use ``attachToRole(role)`` to attach this policy to a role.

        :default: - No roles.
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List["IRole"]], result)

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        '''Initial set of permissions to add to this policy document.

        You can also use ``addPermission(statement)`` to add permissions later.

        :default: - No statements.
        '''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[typing.List["PolicyStatement"]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List["IUser"]]:
        '''Users to attach this policy to.

        You can also use ``attachToUser(user)`` to attach this policy to a user.

        :default: - No users.
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List["IUser"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IOpenIdConnectProvider)
class OpenIdConnectProvider(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.OpenIdConnectProvider",
):
    '''IAM OIDC identity providers are entities in IAM that describe an external identity provider (IdP) service that supports the OpenID Connect (OIDC) standard, such as Google or Salesforce.

    You use an IAM OIDC identity provider
    when you want to establish trust between an OIDC-compatible IdP and your AWS
    account. This is useful when creating a mobile app or web application that
    requires access to AWS resources, but you don't want to create custom sign-in
    code or manage your own user identities.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html
    :resource: AWS::CloudFormation::CustomResource
    :exampleMetadata: infused

    Example::

        provider = iam.OpenIdConnectProvider(self, "MyProvider",
            url="https://openid/connect",
            client_ids=["myclient1", "myclient2"]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        url: builtins.str,
        client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Defines an OpenID Connect provider.

        :param scope: The definition scope.
        :param id: Construct ID.
        :param url: The URL of the identity provider. The URL must begin with https:// and should correspond to the iss claim in the provider's OpenID Connect ID tokens. Per the OIDC standard, path components are allowed but query parameters are not. Typically the URL consists of only a hostname, like https://server.example.org or https://example.com. You cannot register the same provider multiple times in a single AWS account. If you try to submit a URL that has already been used for an OpenID Connect provider in the AWS account, you will get an error.
        :param client_ids: A list of client IDs (also known as audiences). When a mobile or web app registers with an OpenID Connect provider, they establish a value that identifies the application. (This is the value that's sent as the client_id parameter on OAuth requests.) You can register multiple client IDs with the same provider. For example, you might have multiple applications that use the same OIDC provider. You cannot register more than 100 client IDs with a single IAM OIDC provider. Client IDs are up to 255 characters long. Default: - no clients are allowed
        :param thumbprints: A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider's server certificates. Typically this list includes only one entry. However, IAM lets you have up to five thumbprints for an OIDC provider. This lets you maintain multiple thumbprints if the identity provider is rotating certificates. The server certificate thumbprint is the hex-encoded SHA-1 hash value of the X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string. You must provide at least one thumbprint when creating an IAM OIDC provider. For example, assume that the OIDC provider is server.example.com and the provider stores its keys at https://keys.server.example.com/openid-connect. In that case, the thumbprint string would be the hex-encoded SHA-1 hash value of the certificate used by https://keys.server.example.com. Default: - If no thumbprints are specified (an empty array or ``undefined``), the thumbprint of the root certificate authority will be obtained from the provider's server as described in https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d05e6241268ec0fd867633aa632dc97381c9a485e59fdba8d689f6fe6ad7101)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = OpenIdConnectProviderProps(
            url=url, client_ids=client_ids, thumbprints=thumbprints
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromOpenIdConnectProviderArn")
    @builtins.classmethod
    def from_open_id_connect_provider_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        open_id_connect_provider_arn: builtins.str,
    ) -> IOpenIdConnectProvider:
        '''Imports an Open ID connect provider from an ARN.

        :param scope: The definition scope.
        :param id: ID of the construct.
        :param open_id_connect_provider_arn: the ARN to import.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a4e6a2506d8d1375dc8f48a81a60fdbba25071f5a2b7ac40e5f2581340fbd8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument open_id_connect_provider_arn", value=open_id_connect_provider_arn, expected_type=type_hints["open_id_connect_provider_arn"])
        return typing.cast(IOpenIdConnectProvider, jsii.sinvoke(cls, "fromOpenIdConnectProviderArn", [scope, id, open_id_connect_provider_arn]))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderArn")
    def open_id_connect_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM OpenID Connect provider.'''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderArn"))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderIssuer")
    def open_id_connect_provider_issuer(self) -> builtins.str:
        '''The issuer for OIDC Provider.'''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderIssuer"))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderthumbprints")
    def open_id_connect_providerthumbprints(self) -> builtins.str:
        '''The thumbprints configured for this provider.'''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderthumbprints"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.OpenIdConnectProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "client_ids": "clientIds",
        "thumbprints": "thumbprints",
    },
)
class OpenIdConnectProviderProps:
    def __init__(
        self,
        *,
        url: builtins.str,
        client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Initialization properties for ``OpenIdConnectProvider``.

        :param url: The URL of the identity provider. The URL must begin with https:// and should correspond to the iss claim in the provider's OpenID Connect ID tokens. Per the OIDC standard, path components are allowed but query parameters are not. Typically the URL consists of only a hostname, like https://server.example.org or https://example.com. You cannot register the same provider multiple times in a single AWS account. If you try to submit a URL that has already been used for an OpenID Connect provider in the AWS account, you will get an error.
        :param client_ids: A list of client IDs (also known as audiences). When a mobile or web app registers with an OpenID Connect provider, they establish a value that identifies the application. (This is the value that's sent as the client_id parameter on OAuth requests.) You can register multiple client IDs with the same provider. For example, you might have multiple applications that use the same OIDC provider. You cannot register more than 100 client IDs with a single IAM OIDC provider. Client IDs are up to 255 characters long. Default: - no clients are allowed
        :param thumbprints: A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider's server certificates. Typically this list includes only one entry. However, IAM lets you have up to five thumbprints for an OIDC provider. This lets you maintain multiple thumbprints if the identity provider is rotating certificates. The server certificate thumbprint is the hex-encoded SHA-1 hash value of the X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string. You must provide at least one thumbprint when creating an IAM OIDC provider. For example, assume that the OIDC provider is server.example.com and the provider stores its keys at https://keys.server.example.com/openid-connect. In that case, the thumbprint string would be the hex-encoded SHA-1 hash value of the certificate used by https://keys.server.example.com. Default: - If no thumbprints are specified (an empty array or ``undefined``), the thumbprint of the root certificate authority will be obtained from the provider's server as described in https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html

        :exampleMetadata: infused

        Example::

            provider = iam.OpenIdConnectProvider(self, "MyProvider",
                url="https://openid/connect",
                client_ids=["myclient1", "myclient2"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bdf22e31ec661f995d8a432db47cb0019a8a9ed2909c335ea3c4bac43f127f)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument client_ids", value=client_ids, expected_type=type_hints["client_ids"])
            check_type(argname="argument thumbprints", value=thumbprints, expected_type=type_hints["thumbprints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if client_ids is not None:
            self._values["client_ids"] = client_ids
        if thumbprints is not None:
            self._values["thumbprints"] = thumbprints

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the identity provider.

        The URL must begin with https:// and
        should correspond to the iss claim in the provider's OpenID Connect ID
        tokens. Per the OIDC standard, path components are allowed but query
        parameters are not. Typically the URL consists of only a hostname, like
        https://server.example.org or https://example.com.

        You cannot register the same provider multiple times in a single AWS
        account. If you try to submit a URL that has already been used for an
        OpenID Connect provider in the AWS account, you will get an error.
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of client IDs (also known as audiences).

        When a mobile or web app
        registers with an OpenID Connect provider, they establish a value that
        identifies the application. (This is the value that's sent as the client_id
        parameter on OAuth requests.)

        You can register multiple client IDs with the same provider. For example,
        you might have multiple applications that use the same OIDC provider. You
        cannot register more than 100 client IDs with a single IAM OIDC provider.

        Client IDs are up to 255 characters long.

        :default: - no clients are allowed
        '''
        result = self._values.get("client_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def thumbprints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider's server certificates.

        Typically this list includes only one entry. However, IAM lets you have up
        to five thumbprints for an OIDC provider. This lets you maintain multiple
        thumbprints if the identity provider is rotating certificates.

        The server certificate thumbprint is the hex-encoded SHA-1 hash value of
        the X.509 certificate used by the domain where the OpenID Connect provider
        makes its keys available. It is always a 40-character string.

        You must provide at least one thumbprint when creating an IAM OIDC
        provider. For example, assume that the OIDC provider is server.example.com
        and the provider stores its keys at
        https://keys.server.example.com/openid-connect. In that case, the
        thumbprint string would be the hex-encoded SHA-1 hash value of the
        certificate used by https://keys.server.example.com.

        :default:

        - If no thumbprints are specified (an empty array or ``undefined``),
        the thumbprint of the root certificate authority will be obtained from the
        provider's server as described in https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html
        '''
        result = self._values.get("thumbprints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenIdConnectProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PermissionsBoundary(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.PermissionsBoundary",
):
    '''Modify the Permissions Boundaries of Users and Roles in a construct tree.

    Example::

       policy = iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")
       iam.PermissionsBoundary.of(self).apply(policy)

    :exampleMetadata: infused

    Example::

        # project: codebuild.Project
        
        iam.PermissionsBoundary.of(project).apply(codebuild.UntrustedCodeBoundaryPolicy(self, "Boundary"))
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: _constructs_77d1e7e8.IConstruct) -> "PermissionsBoundary":
        '''Access the Permissions Boundaries of a construct tree.

        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d69da7b6d8bc505990e1eb87895379b0813715b8c882b44571a72df54fea0d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("PermissionsBoundary", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="apply")
    def apply(self, boundary_policy: IManagedPolicy) -> None:
        '''Apply the given policy as Permissions Boundary to all Roles and Users in the scope.

        Will override any Permissions Boundaries configured previously; in case
        a Permission Boundary is applied in multiple scopes, the Boundary applied
        closest to the Role wins.

        :param boundary_policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a004abccfb7e9f520a9bee4b1e82d9a8274fb48f15b9de19243d42d756f196)
            check_type(argname="argument boundary_policy", value=boundary_policy, expected_type=type_hints["boundary_policy"])
        return typing.cast(None, jsii.invoke(self, "apply", [boundary_policy]))

    @jsii.member(jsii_name="clear")
    def clear(self) -> None:
        '''Remove previously applied Permissions Boundaries.'''
        return typing.cast(None, jsii.invoke(self, "clear", []))


@jsii.implements(IPolicy)
class Policy(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.Policy",
):
    '''The AWS::IAM::Policy resource associates an IAM policy with IAM users, roles, or groups.

    For more information about IAM policies, see `Overview of IAM
    Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies_overview.html>`_
    in the IAM User Guide guide.

    :exampleMetadata: infused

    Example::

        # post_auth_fn: lambda.Function
        
        
        userpool = cognito.UserPool(self, "myuserpool",
            lambda_triggers=cognito.UserPoolTriggers(
                post_authentication=post_auth_fn
            )
        )
        
        # provide permissions to describe the user pool scoped to the ARN the user pool
        post_auth_fn.role.attach_inline_policy(iam.Policy(self, "userpool-policy",
            statements=[iam.PolicyStatement(
                actions=["cognito-idp:DescribeUserPool"],
                resources=[userpool.user_pool_arn]
            )]
        ))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        document: typing.Optional["PolicyDocument"] = None,
        force: typing.Optional[builtins.bool] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        policy_name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param document: Initial PolicyDocument to use for this Policy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param force: Force creation of an ``AWS::IAM::Policy``. Unless set to ``true``, this ``Policy`` construct will not materialize to an ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect (for example, if it remains unattached to an IAM identity or if it has no statements). This is generally desired behavior, since it prevents creating invalid--and hence undeployable--CloudFormation templates. In cases where you know the policy must be created and it is actually an error if no statements have been added to it, you can set this to ``true``. Default: false
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param policy_name: The name of the policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - Uses the logical ID of the policy resource, which is ensured to be unique within the stack.
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addStatements(...statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826753427ab7d968332a2c9889e2e91d777ec1dadc89bd3838de29445311231d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PolicyProps(
            document=document,
            force=force,
            groups=groups,
            policy_name=policy_name,
            roles=roles,
            statements=statements,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPolicyName")
    @builtins.classmethod
    def from_policy_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        policy_name: builtins.str,
    ) -> IPolicy:
        '''Import a policy in this app based on its name.

        :param scope: -
        :param id: -
        :param policy_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30dc7936b2b6c50f65f512617c0599c3aa41af2c273a864b732fa441fa198362)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        return typing.cast(IPolicy, jsii.sinvoke(cls, "fromPolicyName", [scope, id, policy_name]))

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        '''Adds a statement to the policy document.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba6b094378fd4f2577b6973a340330e66bffa279da207f8bc38121d48ebf715)
            check_type(argname="argument statement", value=statement, expected_type=typing.Tuple[type_hints["statement"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addStatements", [*statement]))

    @jsii.member(jsii_name="attachToGroup")
    def attach_to_group(self, group: "IGroup") -> None:
        '''Attaches this policy to a group.

        :param group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5813c479c73eea905bb9c38cbb869508b378836a228270dc3af8967047f0ad78)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "attachToGroup", [group]))

    @jsii.member(jsii_name="attachToRole")
    def attach_to_role(self, role: "IRole") -> None:
        '''Attaches this policy to a role.

        :param role: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c377a0806fbb4e951ecc0fabfcd5d658a92c984c16bb23750a8a305d66a5b4dc)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "attachToRole", [role]))

    @jsii.member(jsii_name="attachToUser")
    def attach_to_user(self, user: "IUser") -> None:
        '''Attaches this policy to a user.

        :param user: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ebee8ef3734a2a3f714ebfc0c63c08ae85d0c5a96e2744852c0a25b844cf3e)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "attachToUser", [user]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "PolicyDocument":
        '''The policy document.'''
        return typing.cast("PolicyDocument", jsii.get(self, "document"))

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of this policy.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))


@jsii.implements(_aws_cdk_core_f4b25747.IResolvable)
class PolicyDocument(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.PolicyDocument",
):
    '''A PolicyDocument is a collection of statements.

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

    def __init__(
        self,
        *,
        assign_sids: typing.Optional[builtins.bool] = None,
        minimize: typing.Optional[builtins.bool] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
    ) -> None:
        '''
        :param assign_sids: Automatically assign Statement Ids to all statements. Default: false
        :param minimize: Try to minimize the policy by merging statements. To avoid overrunning the maximum policy size, combine statements if they produce the same result. Merging happens according to the following rules: - The Effect of both statements is the same - Neither of the statements have a 'Sid' - Combine Principals if the rest of the statement is exactly the same. - Combine Resources if the rest of the statement is exactly the same. - Combine Actions if the rest of the statement is exactly the same. - We will never combine NotPrincipals, NotResources or NotActions, because doing so would change the meaning of the policy document. Default: - false, unless the feature flag ``@aws-cdk/aws-iam:minimizePolicies`` is set
        :param statements: Initial statements to add to the policy document. Default: - No statements
        '''
        props = PolicyDocumentProps(
            assign_sids=assign_sids, minimize=minimize, statements=statements
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromJson")
    @builtins.classmethod
    def from_json(cls, obj: typing.Any) -> "PolicyDocument":
        '''Creates a new PolicyDocument based on the object provided.

        This will accept an object created from the ``.toJSON()`` call

        :param obj: the PolicyDocument in object form.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5047bd36f25a6706e3652db23871597db2c9d3102b878e80c347f7e5d3b0b3)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("PolicyDocument", jsii.sinvoke(cls, "fromJson", [obj]))

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        '''Adds a statement to the policy document.

        :param statement: the statement to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac383c516d1eddb9c561e401aa91d954df10304f6c77b6b7670ef4b4e79739fa)
            check_type(argname="argument statement", value=statement, expected_type=typing.Tuple[type_hints["statement"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addStatements", [*statement]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: _aws_cdk_core_f4b25747.IResolveContext) -> typing.Any:
        '''Produce the Token's value at resolution time.

        :param context: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedd05de5132f9de2d9fc998e675b63abc427a8da23aeff8c4f95cfb1f76b766)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [context]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        '''JSON-ify the document.

        Used when JSON.stringify() is called
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Encode the policy document as a string.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="validateForAnyPolicy")
    def validate_for_any_policy(self) -> typing.List[builtins.str]:
        '''Validate that all policy statements in the policy document satisfies the requirements for any policy.

        :return: An array of validation error messages, or an empty array if the document is valid.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForAnyPolicy", []))

    @jsii.member(jsii_name="validateForIdentityPolicy")
    def validate_for_identity_policy(self) -> typing.List[builtins.str]:
        '''Validate that all policy statements in the policy document satisfies the requirements for an identity-based policy.

        :return: An array of validation error messages, or an empty array if the document is valid.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForIdentityPolicy", []))

    @jsii.member(jsii_name="validateForResourcePolicy")
    def validate_for_resource_policy(self) -> typing.List[builtins.str]:
        '''Validate that all policy statements in the policy document satisfies the requirements for a resource-based policy.

        :return: An array of validation error messages, or an empty array if the document is valid.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForResourcePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''The creation stack of this resolvable which will be appended to errors thrown during resolution.

        This may return an array with a single informational element indicating how
        to get this property populated, if it was skipped for performance reasons.
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="isEmpty")
    def is_empty(self) -> builtins.bool:
        '''Whether the policy document contains any statements.'''
        return typing.cast(builtins.bool, jsii.get(self, "isEmpty"))

    @builtins.property
    @jsii.member(jsii_name="statementCount")
    def statement_count(self) -> jsii.Number:
        '''The number of statements already added to this policy.

        Can be used, for example, to generate unique "sid"s within the policy.
        '''
        return typing.cast(jsii.Number, jsii.get(self, "statementCount"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.PolicyDocumentProps",
    jsii_struct_bases=[],
    name_mapping={
        "assign_sids": "assignSids",
        "minimize": "minimize",
        "statements": "statements",
    },
)
class PolicyDocumentProps:
    def __init__(
        self,
        *,
        assign_sids: typing.Optional[builtins.bool] = None,
        minimize: typing.Optional[builtins.bool] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
    ) -> None:
        '''Properties for a new PolicyDocument.

        :param assign_sids: Automatically assign Statement Ids to all statements. Default: false
        :param minimize: Try to minimize the policy by merging statements. To avoid overrunning the maximum policy size, combine statements if they produce the same result. Merging happens according to the following rules: - The Effect of both statements is the same - Neither of the statements have a 'Sid' - Combine Principals if the rest of the statement is exactly the same. - Combine Resources if the rest of the statement is exactly the same. - Combine Actions if the rest of the statement is exactly the same. - We will never combine NotPrincipals, NotResources or NotActions, because doing so would change the meaning of the policy document. Default: - false, unless the feature flag ``@aws-cdk/aws-iam:minimizePolicies`` is set
        :param statements: Initial statements to add to the policy document. Default: - No statements

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
            type_hints = typing.get_type_hints(_typecheckingstub__76f4f7d7d8014bab5f0c27a543d9c04050866092f6c5e9172d4a638f41c319aa)
            check_type(argname="argument assign_sids", value=assign_sids, expected_type=type_hints["assign_sids"])
            check_type(argname="argument minimize", value=minimize, expected_type=type_hints["minimize"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assign_sids is not None:
            self._values["assign_sids"] = assign_sids
        if minimize is not None:
            self._values["minimize"] = minimize
        if statements is not None:
            self._values["statements"] = statements

    @builtins.property
    def assign_sids(self) -> typing.Optional[builtins.bool]:
        '''Automatically assign Statement Ids to all statements.

        :default: false
        '''
        result = self._values.get("assign_sids")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minimize(self) -> typing.Optional[builtins.bool]:
        '''Try to minimize the policy by merging statements.

        To avoid overrunning the maximum policy size, combine statements if they produce
        the same result. Merging happens according to the following rules:

        - The Effect of both statements is the same
        - Neither of the statements have a 'Sid'
        - Combine Principals if the rest of the statement is exactly the same.
        - Combine Resources if the rest of the statement is exactly the same.
        - Combine Actions if the rest of the statement is exactly the same.
        - We will never combine NotPrincipals, NotResources or NotActions, because doing
          so would change the meaning of the policy document.

        :default: - false, unless the feature flag ``@aws-cdk/aws-iam:minimizePolicies`` is set
        '''
        result = self._values.get("minimize")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        '''Initial statements to add to the policy document.

        :default: - No statements
        '''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[typing.List["PolicyStatement"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyDocumentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.PolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "document": "document",
        "force": "force",
        "groups": "groups",
        "policy_name": "policyName",
        "roles": "roles",
        "statements": "statements",
        "users": "users",
    },
)
class PolicyProps:
    def __init__(
        self,
        *,
        document: typing.Optional[PolicyDocument] = None,
        force: typing.Optional[builtins.bool] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        policy_name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''Properties for defining an IAM inline policy document.

        :param document: Initial PolicyDocument to use for this Policy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param force: Force creation of an ``AWS::IAM::Policy``. Unless set to ``true``, this ``Policy`` construct will not materialize to an ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect (for example, if it remains unattached to an IAM identity or if it has no statements). This is generally desired behavior, since it prevents creating invalid--and hence undeployable--CloudFormation templates. In cases where you know the policy must be created and it is actually an error if no statements have been added to it, you can set this to ``true``. Default: false
        :param groups: Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param policy_name: The name of the policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - Uses the logical ID of the policy resource, which is ensured to be unique within the stack.
        :param roles: Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: Initial set of permissions to add to this policy document. You can also use ``addStatements(...statement)`` to add permissions later. Default: - No statements.
        :param users: Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.

        :exampleMetadata: infused

        Example::

            # post_auth_fn: lambda.Function
            
            
            userpool = cognito.UserPool(self, "myuserpool",
                lambda_triggers=cognito.UserPoolTriggers(
                    post_authentication=post_auth_fn
                )
            )
            
            # provide permissions to describe the user pool scoped to the ARN the user pool
            post_auth_fn.role.attach_inline_policy(iam.Policy(self, "userpool-policy",
                statements=[iam.PolicyStatement(
                    actions=["cognito-idp:DescribeUserPool"],
                    resources=[userpool.user_pool_arn]
                )]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8a546acac37b02e421f4948eb464fbbe9eac668ce499bcc146b926205251ca)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if document is not None:
            self._values["document"] = document
        if force is not None:
            self._values["force"] = force
        if groups is not None:
            self._values["groups"] = groups
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if roles is not None:
            self._values["roles"] = roles
        if statements is not None:
            self._values["statements"] = statements
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def document(self) -> typing.Optional[PolicyDocument]:
        '''Initial PolicyDocument to use for this Policy.

        If omited, any
        ``PolicyStatement`` provided in the ``statements`` property will be applied
        against the empty default ``PolicyDocument``.

        :default: - An empty policy.
        '''
        result = self._values.get("document")
        return typing.cast(typing.Optional[PolicyDocument], result)

    @builtins.property
    def force(self) -> typing.Optional[builtins.bool]:
        '''Force creation of an ``AWS::IAM::Policy``.

        Unless set to ``true``, this ``Policy`` construct will not materialize to an
        ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect
        (for example, if it remains unattached to an IAM identity or if it has no
        statements). This is generally desired behavior, since it prevents
        creating invalid--and hence undeployable--CloudFormation templates.

        In cases where you know the policy must be created and it is actually
        an error if no statements have been added to it, you can set this to ``true``.

        :default: false
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        '''Groups to attach this policy to.

        You can also use ``attachToGroup(group)`` to attach this policy to a group.

        :default: - No groups.
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List["IGroup"]], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        If you specify multiple policies for an entity,
        specify unique names. For example, if you specify a list of policies for
        an IAM role, each policy must have a unique name.

        :default:

        - Uses the logical ID of the policy resource, which is ensured
        to be unique within the stack.
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List["IRole"]]:
        '''Roles to attach this policy to.

        You can also use ``attachToRole(role)`` to attach this policy to a role.

        :default: - No roles.
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List["IRole"]], result)

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        '''Initial set of permissions to add to this policy document.

        You can also use ``addStatements(...statement)`` to add permissions later.

        :default: - No statements.
        '''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[typing.List["PolicyStatement"]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List["IUser"]]:
        '''Users to attach this policy to.

        You can also use ``attachToUser(user)`` to attach this policy to a user.

        :default: - No users.
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List["IUser"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyStatement(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.PolicyStatement",
):
    '''Represents a statement in an IAM policy document.

    :exampleMetadata: lit=test/integ.vpc-endpoint.lit.ts infused

    Example::

        # Add gateway endpoints when creating the VPC
        vpc = ec2.Vpc(self, "MyVpc",
            gateway_endpoints={
                "S3": ec2.GatewayVpcEndpointOptions(
                    service=ec2.GatewayVpcEndpointAwsService.S3
                )
            }
        )
        
        # Alternatively gateway endpoints can be added on the VPC
        dynamo_db_endpoint = vpc.add_gateway_endpoint("DynamoDbEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.DYNAMODB
        )
        
        # This allows to customize the endpoint policy
        dynamo_db_endpoint.add_to_policy(
            iam.PolicyStatement( # Restrict to listing and describing tables
                principals=[iam.AnyPrincipal()],
                actions=["dynamodb:DescribeTable", "dynamodb:ListTables"],
                resources=["*"]))
        
        # Add an interface endpoint
        vpc.add_interface_endpoint("EcrDockerEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER
        )
    '''

    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        effect: typing.Optional[Effect] = None,
        not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        sid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: List of actions to add to the statement. Default: - no actions
        :param conditions: Conditions to add to the statement. Default: - no condition
        :param effect: Whether to allow or deny the actions in this statement. Default: Effect.ALLOW
        :param not_actions: List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: List of not principals to add to the statement. Default: - no not principals
        :param not_resources: NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: List of principals to add to the statement. Default: - no principals
        :param resources: Resource ARNs to add to the statement. Default: - no resources
        :param sid: The Sid (statement ID) is an optional identifier that you provide for the policy statement. You can assign a Sid value to each statement in a statement array. In services that let you specify an ID element, such as SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In IAM, the Sid value must be unique within a JSON policy. Default: - no sid
        '''
        props = PolicyStatementProps(
            actions=actions,
            conditions=conditions,
            effect=effect,
            not_actions=not_actions,
            not_principals=not_principals,
            not_resources=not_resources,
            principals=principals,
            resources=resources,
            sid=sid,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromJson")
    @builtins.classmethod
    def from_json(cls, obj: typing.Any) -> "PolicyStatement":
        '''Creates a new PolicyStatement based on the object provided.

        This will accept an object created from the ``.toJSON()`` call

        :param obj: the PolicyStatement in object form.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffcea937441550e9184ac00ae00ba3e3812c13f41565e8591ef60253c4f2542)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("PolicyStatement", jsii.sinvoke(cls, "fromJson", [obj]))

    @jsii.member(jsii_name="addAccountCondition")
    def add_account_condition(self, account_id: builtins.str) -> None:
        '''Add a condition that limits to a given account.

        This method can only be called once: subsequent calls will overwrite earlier calls.

        :param account_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532f9bdafed4a223baf813860d6386e5626ec0022d7dd63f96c518d4fc6c521a)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        return typing.cast(None, jsii.invoke(self, "addAccountCondition", [account_id]))

    @jsii.member(jsii_name="addAccountRootPrincipal")
    def add_account_root_principal(self) -> None:
        '''Adds an AWS account root user principal to this policy statement.'''
        return typing.cast(None, jsii.invoke(self, "addAccountRootPrincipal", []))

    @jsii.member(jsii_name="addActions")
    def add_actions(self, *actions: builtins.str) -> None:
        '''Specify allowed actions into the "Action" section of the policy statement.

        :param actions: actions that will be allowed.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_action.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2938b71b67747eee407f9c817bf7d1a41197aa4bfa37eec68c9b3110516135)
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addActions", [*actions]))

    @jsii.member(jsii_name="addAllResources")
    def add_all_resources(self) -> None:
        '''Adds a ``"*"`` resource to this statement.'''
        return typing.cast(None, jsii.invoke(self, "addAllResources", []))

    @jsii.member(jsii_name="addAnyPrincipal")
    def add_any_principal(self) -> None:
        '''Adds all identities in all accounts ("*") to this policy statement.'''
        return typing.cast(None, jsii.invoke(self, "addAnyPrincipal", []))

    @jsii.member(jsii_name="addArnPrincipal")
    def add_arn_principal(self, arn: builtins.str) -> None:
        '''Specify a principal using the ARN  identifier of the principal.

        You cannot specify IAM groups and instance profiles as principals.

        :param arn: ARN identifier of AWS account, IAM user, or IAM role (i.e. arn:aws:iam::123456789012:user/user-name).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483f632408ecc823fa3364619179350afb31a3ea4cd21a3ef4b29c1c0ae1e73e)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast(None, jsii.invoke(self, "addArnPrincipal", [arn]))

    @jsii.member(jsii_name="addAwsAccountPrincipal")
    def add_aws_account_principal(self, account_id: builtins.str) -> None:
        '''Specify AWS account ID as the principal entity to the "Principal" section of a policy statement.

        :param account_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da47be57b0ae9584c58020e316eeaad991fc445c802b144d29b78e76f9c19d47)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        return typing.cast(None, jsii.invoke(self, "addAwsAccountPrincipal", [account_id]))

    @jsii.member(jsii_name="addCanonicalUserPrincipal")
    def add_canonical_user_principal(self, canonical_user_id: builtins.str) -> None:
        '''Adds a canonical user ID principal to this policy document.

        :param canonical_user_id: unique identifier assigned by AWS for every account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690b4b4d99807d694786a792027f9fd41ea7017855647b353d7966e72a1b4332)
            check_type(argname="argument canonical_user_id", value=canonical_user_id, expected_type=type_hints["canonical_user_id"])
        return typing.cast(None, jsii.invoke(self, "addCanonicalUserPrincipal", [canonical_user_id]))

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, key: builtins.str, value: typing.Any) -> None:
        '''Add a condition to the Policy.

        If multiple calls are made to add a condition with the same operator and field, only
        the last one wins. For example::

           # stmt: iam.PolicyStatement


           stmt.add_condition("StringEquals", {"aws:SomeField": "1"})
           stmt.add_condition("StringEquals", {"aws:SomeField": "2"})

        Will end up with the single condition ``StringEquals: { 'aws:SomeField': '2' }``.

        If you meant to add a condition to say that the field can be *either* ``1`` or ``2``, write
        this::

           # stmt: iam.PolicyStatement


           stmt.add_condition("StringEquals", {"aws:SomeField": ["1", "2"]})

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd98c5a27dd5fde5f772f6487662333d0fd941a121ca07313aaee1437d3db5e2)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addCondition", [key, value]))

    @jsii.member(jsii_name="addConditions")
    def add_conditions(
        self,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''Add multiple conditions to the Policy.

        See the ``addCondition`` function for a caveat on calling this method multiple times.

        :param conditions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e920f9d0d1b0486f7e2c114fd7ce570cae5cd4c934512d76ef199347118a6a)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast(None, jsii.invoke(self, "addConditions", [conditions]))

    @jsii.member(jsii_name="addFederatedPrincipal")
    def add_federated_principal(
        self,
        federated: typing.Any,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''Adds a federated identity provider such as Amazon Cognito to this policy statement.

        :param federated: federated identity provider (i.e. 'cognito-identity.amazonaws.com').
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e17c77733d830a7932a666a4315c4c32cced578919c0ea52ecfaabd69d84a2c)
            check_type(argname="argument federated", value=federated, expected_type=type_hints["federated"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast(None, jsii.invoke(self, "addFederatedPrincipal", [federated, conditions]))

    @jsii.member(jsii_name="addNotActions")
    def add_not_actions(self, *not_actions: builtins.str) -> None:
        '''Explicitly allow all actions except the specified list of actions into the "NotAction" section of the policy document.

        :param not_actions: actions that will be denied. All other actions will be permitted.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notaction.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed140998c0bcec41ca7a0ccb53441498e621c3c91be74b100641b46a63dde00)
            check_type(argname="argument not_actions", value=not_actions, expected_type=typing.Tuple[type_hints["not_actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addNotActions", [*not_actions]))

    @jsii.member(jsii_name="addNotPrincipals")
    def add_not_principals(self, *not_principals: IPrincipal) -> None:
        '''Specify principals that is not allowed or denied access to the "NotPrincipal" section of a policy statement.

        :param not_principals: IAM principals that will be denied access.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notprincipal.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c637ee98701df2ea8affe16cd5efc393dc1c1429b4a43de89ffbd3155d6c099c)
            check_type(argname="argument not_principals", value=not_principals, expected_type=typing.Tuple[type_hints["not_principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addNotPrincipals", [*not_principals]))

    @jsii.member(jsii_name="addNotResources")
    def add_not_resources(self, *arns: builtins.str) -> None:
        '''Specify resources that this policy statement will not apply to in the "NotResource" section of this policy statement.

        All resources except the specified list will be matched.

        :param arns: Amazon Resource Names (ARNs) of the resources that this policy statement does not apply to.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notresource.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff17183088dfe1dcfb47a2dcdddc0129480f6f1cb678f299d0fb58f9cac024a)
            check_type(argname="argument arns", value=arns, expected_type=typing.Tuple[type_hints["arns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addNotResources", [*arns]))

    @jsii.member(jsii_name="addPrincipals")
    def add_principals(self, *principals: IPrincipal) -> None:
        '''Adds principals to the "Principal" section of a policy statement.

        :param principals: IAM principals that will be added.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511578cfb7d00fb67864fdc75942e9e6b391f4177c1a8d8f7e32f07d37a877b8)
            check_type(argname="argument principals", value=principals, expected_type=typing.Tuple[type_hints["principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPrincipals", [*principals]))

    @jsii.member(jsii_name="addResources")
    def add_resources(self, *arns: builtins.str) -> None:
        '''Specify resources that this policy statement applies into the "Resource" section of this policy statement.

        :param arns: Amazon Resource Names (ARNs) of the resources that this policy statement applies to.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30f77d6f049aa7034b3e7e4e68a6c455a551ec07dea1404987c504b0e82af9c)
            check_type(argname="argument arns", value=arns, expected_type=typing.Tuple[type_hints["arns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addResources", [*arns]))

    @jsii.member(jsii_name="addServicePrincipal")
    def add_service_principal(
        self,
        service: builtins.str,
        *,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Adds a service principal to this policy statement.

        :param service: the service name for which a service principal is requested (e.g: ``s3.amazonaws.com``).
        :param conditions: Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: (deprecated) The region in which the service is operating. Default: - the current Stack's region.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9183104f297e8c384356c5525bdb50beb752042d8e5f137a136893a573a50904)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        opts = ServicePrincipalOpts(conditions=conditions, region=region)

        return typing.cast(None, jsii.invoke(self, "addServicePrincipal", [service, opts]))

    @jsii.member(jsii_name="copy")
    def copy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        effect: typing.Optional[Effect] = None,
        not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        sid: typing.Optional[builtins.str] = None,
    ) -> "PolicyStatement":
        '''Create a new ``PolicyStatement`` with the same exact properties as this one, except for the overrides.

        :param actions: List of actions to add to the statement. Default: - no actions
        :param conditions: Conditions to add to the statement. Default: - no condition
        :param effect: Whether to allow or deny the actions in this statement. Default: Effect.ALLOW
        :param not_actions: List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: List of not principals to add to the statement. Default: - no not principals
        :param not_resources: NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: List of principals to add to the statement. Default: - no principals
        :param resources: Resource ARNs to add to the statement. Default: - no resources
        :param sid: The Sid (statement ID) is an optional identifier that you provide for the policy statement. You can assign a Sid value to each statement in a statement array. In services that let you specify an ID element, such as SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In IAM, the Sid value must be unique within a JSON policy. Default: - no sid
        '''
        overrides = PolicyStatementProps(
            actions=actions,
            conditions=conditions,
            effect=effect,
            not_actions=not_actions,
            not_principals=not_principals,
            not_resources=not_resources,
            principals=principals,
            resources=resources,
            sid=sid,
        )

        return typing.cast("PolicyStatement", jsii.invoke(self, "copy", [overrides]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        '''JSON-ify the statement.

        Used when JSON.stringify() is called
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toStatementJson")
    def to_statement_json(self) -> typing.Any:
        '''JSON-ify the policy statement.

        Used when JSON.stringify() is called
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toStatementJson", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''String representation of this policy statement.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="validateForAnyPolicy")
    def validate_for_any_policy(self) -> typing.List[builtins.str]:
        '''Validate that the policy statement satisfies base requirements for a policy.

        :return: An array of validation error messages, or an empty array if the statement is valid.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForAnyPolicy", []))

    @jsii.member(jsii_name="validateForIdentityPolicy")
    def validate_for_identity_policy(self) -> typing.List[builtins.str]:
        '''Validate that the policy statement satisfies all requirements for an identity-based policy.

        :return: An array of validation error messages, or an empty array if the statement is valid.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForIdentityPolicy", []))

    @jsii.member(jsii_name="validateForResourcePolicy")
    def validate_for_resource_policy(self) -> typing.List[builtins.str]:
        '''Validate that the policy statement satisfies all requirements for a resource-based policy.

        :return: An array of validation error messages, or an empty array if the statement is valid.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForResourcePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        '''The Actions added to this statement.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Any:
        '''The conditions added to this statement.'''
        return typing.cast(typing.Any, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="hasPrincipal")
    def has_principal(self) -> builtins.bool:
        '''Indicates if this permission has a "Principal" section.'''
        return typing.cast(builtins.bool, jsii.get(self, "hasPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="hasResource")
    def has_resource(self) -> builtins.bool:
        '''Indicates if this permission has at least one resource associated with it.'''
        return typing.cast(builtins.bool, jsii.get(self, "hasResource"))

    @builtins.property
    @jsii.member(jsii_name="notActions")
    def not_actions(self) -> typing.List[builtins.str]:
        '''The NotActions added to this statement.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notActions"))

    @builtins.property
    @jsii.member(jsii_name="notPrincipals")
    def not_principals(self) -> typing.List[IPrincipal]:
        '''The NotPrincipals added to this statement.'''
        return typing.cast(typing.List[IPrincipal], jsii.get(self, "notPrincipals"))

    @builtins.property
    @jsii.member(jsii_name="notResources")
    def not_resources(self) -> typing.List[builtins.str]:
        '''The NotResources added to this statement.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notResources"))

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[IPrincipal]:
        '''The Principals added to this statement.'''
        return typing.cast(typing.List[IPrincipal], jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        '''The Resources added to this statement.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> Effect:
        '''Whether to allow or deny the actions in this statement.'''
        return typing.cast(Effect, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: Effect) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340628b0426921b2e665bee0834f6217f29fe7d2ba3b0204aacd588972951e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value)

    @builtins.property
    @jsii.member(jsii_name="sid")
    def sid(self) -> typing.Optional[builtins.str]:
        '''Statement ID for this statement.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sid"))

    @sid.setter
    def sid(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5e46ae9483d42a2b2cc9d51a7c483f01c2975f1aee84d7d53cda8135d1f0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sid", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.PolicyStatementProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "conditions": "conditions",
        "effect": "effect",
        "not_actions": "notActions",
        "not_principals": "notPrincipals",
        "not_resources": "notResources",
        "principals": "principals",
        "resources": "resources",
        "sid": "sid",
    },
)
class PolicyStatementProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        effect: typing.Optional[Effect] = None,
        not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        sid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Interface for creating a policy statement.

        :param actions: List of actions to add to the statement. Default: - no actions
        :param conditions: Conditions to add to the statement. Default: - no condition
        :param effect: Whether to allow or deny the actions in this statement. Default: Effect.ALLOW
        :param not_actions: List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: List of not principals to add to the statement. Default: - no not principals
        :param not_resources: NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: List of principals to add to the statement. Default: - no principals
        :param resources: Resource ARNs to add to the statement. Default: - no resources
        :param sid: The Sid (statement ID) is an optional identifier that you provide for the policy statement. You can assign a Sid value to each statement in a statement array. In services that let you specify an ID element, such as SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In IAM, the Sid value must be unique within a JSON policy. Default: - no sid

        :exampleMetadata: lit=test/integ.vpc-endpoint.lit.ts infused

        Example::

            # Add gateway endpoints when creating the VPC
            vpc = ec2.Vpc(self, "MyVpc",
                gateway_endpoints={
                    "S3": ec2.GatewayVpcEndpointOptions(
                        service=ec2.GatewayVpcEndpointAwsService.S3
                    )
                }
            )
            
            # Alternatively gateway endpoints can be added on the VPC
            dynamo_db_endpoint = vpc.add_gateway_endpoint("DynamoDbEndpoint",
                service=ec2.GatewayVpcEndpointAwsService.DYNAMODB
            )
            
            # This allows to customize the endpoint policy
            dynamo_db_endpoint.add_to_policy(
                iam.PolicyStatement( # Restrict to listing and describing tables
                    principals=[iam.AnyPrincipal()],
                    actions=["dynamodb:DescribeTable", "dynamodb:ListTables"],
                    resources=["*"]))
            
            # Add an interface endpoint
            vpc.add_interface_endpoint("EcrDockerEndpoint",
                service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1215e5692cd37bffdb5cbb63a11f28f91f3d97de3c749304ae97b4edca60f785)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument not_actions", value=not_actions, expected_type=type_hints["not_actions"])
            check_type(argname="argument not_principals", value=not_principals, expected_type=type_hints["not_principals"])
            check_type(argname="argument not_resources", value=not_resources, expected_type=type_hints["not_resources"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument sid", value=sid, expected_type=type_hints["sid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if conditions is not None:
            self._values["conditions"] = conditions
        if effect is not None:
            self._values["effect"] = effect
        if not_actions is not None:
            self._values["not_actions"] = not_actions
        if not_principals is not None:
            self._values["not_principals"] = not_principals
        if not_resources is not None:
            self._values["not_resources"] = not_resources
        if principals is not None:
            self._values["principals"] = principals
        if resources is not None:
            self._values["resources"] = resources
        if sid is not None:
            self._values["sid"] = sid

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of actions to add to the statement.

        :default: - no actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Conditions to add to the statement.

        :default: - no condition
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def effect(self) -> typing.Optional[Effect]:
        '''Whether to allow or deny the actions in this statement.

        :default: Effect.ALLOW
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[Effect], result)

    @builtins.property
    def not_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of not actions to add to the statement.

        :default: - no not-actions
        '''
        result = self._values.get("not_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_principals(self) -> typing.Optional[typing.List[IPrincipal]]:
        '''List of not principals to add to the statement.

        :default: - no not principals
        '''
        result = self._values.get("not_principals")
        return typing.cast(typing.Optional[typing.List[IPrincipal]], result)

    @builtins.property
    def not_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''NotResource ARNs to add to the statement.

        :default: - no not-resources
        '''
        result = self._values.get("not_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[IPrincipal]]:
        '''List of principals to add to the statement.

        :default: - no principals
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[IPrincipal]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Resource ARNs to add to the statement.

        :default: - no resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sid(self) -> typing.Optional[builtins.str]:
        '''The Sid (statement ID) is an optional identifier that you provide for the policy statement.

        You can assign a Sid value to each statement in a
        statement array. In services that let you specify an ID element, such as
        SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In
        IAM, the Sid value must be unique within a JSON policy.

        :default: - no sid
        '''
        result = self._values.get("sid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyStatementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrincipalPolicyFragment(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.PrincipalPolicyFragment",
):
    '''A collection of the fields in a PolicyStatement that can be used to identify a principal.

    This consists of the JSON used in the "Principal" field, and optionally a
    set of "Condition"s that need to be applied to the policy.

    Generally, a principal looks like::

        { '<TYPE>': ['ID', 'ID', ...] }

    And this is also the type of the field ``principalJson``.  However, there is a
    special type of principal that is just the string '*', which is treated
    differently by some services. To represent that principal, ``principalJson``
    should contain ``{ 'LiteralString': ['*'] }``.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # conditions: Any
        
        principal_policy_fragment = iam.PrincipalPolicyFragment({
            "principal_json_key": ["principalJson"]
        }, {
            "conditions_key": conditions
        })
    '''

    def __init__(
        self,
        principal_json: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param principal_json: JSON of the "Principal" section in a policy statement.
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_. conditions that need to be applied to this policy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6e266a1a41bfc081c3549a3b433b33593a3357a68668058dc4a383ee85283b)
            check_type(argname="argument principal_json", value=principal_json, expected_type=type_hints["principal_json"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [principal_json, conditions])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''The conditions under which the policy is in effect.

        See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        conditions that need to be applied to this policy
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="principalJson")
    def principal_json(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''JSON of the "Principal" section in a policy statement.'''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.get(self, "principalJson"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.RoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "assumed_by": "assumedBy",
        "description": "description",
        "external_id": "externalId",
        "external_ids": "externalIds",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "role_name": "roleName",
    },
)
class RoleProps:
    def __init__(
        self,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining an IAM Role.

        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :exampleMetadata: infused

        Example::

            lambda_role = iam.Role(self, "Role",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                description="Example role..."
            )
            
            stream = kinesis.Stream(self, "MyEncryptedStream",
                encryption=kinesis.StreamEncryption.KMS
            )
            
            # give lambda permissions to read stream
            stream.grant_read(lambda_role)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2557f999f89ee6454e622453703ead23ed34fc87d644d852566458d89abe754d)
            check_type(argname="argument assumed_by", value=assumed_by, expected_type=type_hints["assumed_by"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument external_ids", value=external_ids, expected_type=type_hints["external_ids"])
            check_type(argname="argument inline_policies", value=inline_policies, expected_type=type_hints["inline_policies"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument max_session_duration", value=max_session_duration, expected_type=type_hints["max_session_duration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assumed_by": assumed_by,
        }
        if description is not None:
            self._values["description"] = description
        if external_id is not None:
            self._values["external_id"] = external_id
        if external_ids is not None:
            self._values["external_ids"] = external_ids
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def assumed_by(self) -> IPrincipal:
        '''The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role.

        You can later modify the assume role policy document by accessing it via
        the ``assumeRolePolicy`` property.
        '''
        result = self._values.get("assumed_by")
        assert result is not None, "Required property 'assumed_by' is missing"
        return typing.cast(IPrincipal, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role.

        It can be up to 1000 characters long.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ID that the role assumer needs to provide when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required

        :deprecated: see {@link externalIds}

        :stability: deprecated
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required
        '''
        result = self._values.get("external_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PolicyDocument]]:
        '''A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        :default: - No policy is inlined in the Role resource.
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PolicyDocument]], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[IManagedPolicy]]:
        '''A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[IManagedPolicy]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        :default: Duration.hours(1)

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        :default: /
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[IManagedPolicy], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the role name.
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SamlMetadataDocument(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-iam.SamlMetadataDocument",
):
    '''A SAML metadata document.

    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        principal = iam.SamlPrincipal(provider, {
            "StringEquals": {
                "SAML:iss": "issuer"
            }
        })
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(cls, path: builtins.str) -> "SamlMetadataDocument":
        '''Create a SAML metadata document from a XML file.

        :param path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739ee5b6d6fa73cd50b8a861cc98102f227f3e5532eada8621c0998547141e5c)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("SamlMetadataDocument", jsii.sinvoke(cls, "fromFile", [path]))

    @jsii.member(jsii_name="fromXml")
    @builtins.classmethod
    def from_xml(cls, xml: builtins.str) -> "SamlMetadataDocument":
        '''Create a SAML metadata document from a XML string.

        :param xml: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e36bdc25b503e6858c06fbe71e06fb8c47db9917d362747f4ffb100fdce961)
            check_type(argname="argument xml", value=xml, expected_type=type_hints["xml"])
        return typing.cast("SamlMetadataDocument", jsii.sinvoke(cls, "fromXml", [xml]))

    @builtins.property
    @jsii.member(jsii_name="xml")
    @abc.abstractmethod
    def xml(self) -> builtins.str:
        '''The XML content of the metadata document.'''
        ...


class _SamlMetadataDocumentProxy(SamlMetadataDocument):
    @builtins.property
    @jsii.member(jsii_name="xml")
    def xml(self) -> builtins.str:
        '''The XML content of the metadata document.'''
        return typing.cast(builtins.str, jsii.get(self, "xml"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SamlMetadataDocument).__jsii_proxy_class__ = lambda : _SamlMetadataDocumentProxy


@jsii.implements(ISamlProvider)
class SamlProvider(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.SamlProvider",
):
    '''A SAML provider.

    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        iam.Role(self, "Role",
            assumed_by=iam.SamlConsolePrincipal(provider)
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        metadata_document: SamlMetadataDocument,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param metadata_document: An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.
        :param name: The name of the provider to create. This parameter allows a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- Length must be between 1 and 128 characters. Default: - a CloudFormation generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beba1e161374af536b36e0e63753cb8a9b8860fdbc4a956e4f8eb0ae899b272c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SamlProviderProps(metadata_document=metadata_document, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSamlProviderArn")
    @builtins.classmethod
    def from_saml_provider_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        saml_provider_arn: builtins.str,
    ) -> ISamlProvider:
        '''Import an existing provider.

        :param scope: -
        :param id: -
        :param saml_provider_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4847e26d898ac5e2c11dd5c2594fd44b4e7e7c30b23390dc4bc1ea4ba0ac0234)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument saml_provider_arn", value=saml_provider_arn, expected_type=type_hints["saml_provider_arn"])
        return typing.cast(ISamlProvider, jsii.sinvoke(cls, "fromSamlProviderArn", [scope, id, saml_provider_arn]))

    @builtins.property
    @jsii.member(jsii_name="samlProviderArn")
    def saml_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the provider.'''
        return typing.cast(builtins.str, jsii.get(self, "samlProviderArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.SamlProviderProps",
    jsii_struct_bases=[],
    name_mapping={"metadata_document": "metadataDocument", "name": "name"},
)
class SamlProviderProps:
    def __init__(
        self,
        *,
        metadata_document: SamlMetadataDocument,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a SAML provider.

        :param metadata_document: An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.
        :param name: The name of the provider to create. This parameter allows a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- Length must be between 1 and 128 characters. Default: - a CloudFormation generated name

        :exampleMetadata: infused

        Example::

            provider = iam.SamlProvider(self, "Provider",
                metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
            )
            iam.Role(self, "Role",
                assumed_by=iam.SamlConsolePrincipal(provider)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8a837d1e0d2af05a654af566e5dab166691061a32ea1ece7ce339f074a03b9)
            check_type(argname="argument metadata_document", value=metadata_document, expected_type=type_hints["metadata_document"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata_document": metadata_document,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def metadata_document(self) -> SamlMetadataDocument:
        '''An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.'''
        result = self._values.get("metadata_document")
        assert result is not None, "Required property 'metadata_document' is missing"
        return typing.cast(SamlMetadataDocument, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the provider to create.

        This parameter allows a string of characters consisting of upper and
        lowercase alphanumeric characters with no spaces. You can also include
        any of the following characters: _+=,.@-

        Length must be between 1 and 128 characters.

        :default: - a CloudFormation generated name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SamlProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.ServicePrincipalOpts",
    jsii_struct_bases=[],
    name_mapping={"conditions": "conditions", "region": "region"},
)
class ServicePrincipalOpts:
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for a service principal.

        :param conditions: Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: (deprecated) The region in which the service is operating. Default: - the current Stack's region.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            # conditions: Any
            
            service_principal_opts = iam.ServicePrincipalOpts(
                conditions={
                    "conditions_key": conditions
                },
                region="region"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f790361a69d2878fd5cc0b57a28b0561662de83463f3fa1ce7edeabe8ddb84f5)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def conditions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional conditions to add to the Service Principal.

        :default: - No conditions
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The region in which the service is operating.

        :default: - the current Stack's region.

        :deprecated: You should not need to set this. The stack's region is always correct.

        :stability: deprecated
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalOpts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPrincipal)
class UnknownPrincipal(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.UnknownPrincipal",
):
    '''A principal for use in resources that need to have a role but it's unknown.

    Some resources have roles associated with them which they assume, such as
    Lambda Functions, CodeBuild projects, StepFunctions machines, etc.

    When those resources are imported, their actual roles are not always
    imported with them. When that happens, we use an instance of this class
    instead, which will add user warnings when statements are attempted to be
    added to it.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import constructs as constructs
        
        # construct: constructs.Construct
        
        unknown_principal = iam.UnknownPrincipal(
            resource=construct
        )
    '''

    def __init__(self, *, resource: _constructs_77d1e7e8.IConstruct) -> None:
        '''
        :param resource: The resource the role proxy is for.
        '''
        props = UnknownPrincipalProps(resource=resource)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a13978d1b7af5dc1ecfaa5aa431b875e1efa6d2b8f64424d32a10a1bb1529a2)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71bffd0ad97751c05dddc0b182fa1cc44ef882ba8b8e118a71021c0dde7e06c)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.UnknownPrincipalProps",
    jsii_struct_bases=[],
    name_mapping={"resource": "resource"},
)
class UnknownPrincipalProps:
    def __init__(self, *, resource: _constructs_77d1e7e8.IConstruct) -> None:
        '''Properties for an UnknownPrincipal.

        :param resource: The resource the role proxy is for.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import constructs as constructs
            
            # construct: constructs.Construct
            
            unknown_principal_props = iam.UnknownPrincipalProps(
                resource=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2ff83013aa8d2751c9d23a8bf54b989cecfcc3128e830c3702657b9cc311d7)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource": resource,
        }

    @builtins.property
    def resource(self) -> _constructs_77d1e7e8.IConstruct:
        '''The resource the role proxy is for.'''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(_constructs_77d1e7e8.IConstruct, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UnknownPrincipalProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.UserAttributes",
    jsii_struct_bases=[],
    name_mapping={"user_arn": "userArn"},
)
class UserAttributes:
    def __init__(self, *, user_arn: builtins.str) -> None:
        '''Represents a user defined outside of this stack.

        :param user_arn: The ARN of the user. Format: arn::iam:::user/

        :exampleMetadata: infused

        Example::

            user = iam.User.from_user_attributes(self, "MyImportedUserByAttributes",
                user_arn="arn:aws:iam::123456789012:user/johnsmith"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae70989695d7a0446847476b9b8039389e197a26b5591db4da99409b788a265)
            check_type(argname="argument user_arn", value=user_arn, expected_type=type_hints["user_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_arn": user_arn,
        }

    @builtins.property
    def user_arn(self) -> builtins.str:
        '''The ARN of the user.

        Format: arn::iam:::user/
        '''
        result = self._values.get("user_arn")
        assert result is not None, "Required property 'user_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.UserProps",
    jsii_struct_bases=[],
    name_mapping={
        "groups": "groups",
        "managed_policies": "managedPolicies",
        "password": "password",
        "password_reset_required": "passwordResetRequired",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "user_name": "userName",
    },
)
class UserProps:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
        password_reset_required: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining an IAM user.

        :param groups: Groups to add this user to. You can also use ``addToGroup`` to add this user to a group. Default: - No groups.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param password: The password for the user. This is required so the user can access the AWS Management Console. You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - User won't be able to access the management console without a password.
        :param password_reset_required: Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console. If this is set to 'true', you must also specify "initialPassword". Default: false
        :param path: The path for the user name. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param user_name: A name for the IAM user. For valid values, see the UserName parameter for the CreateUser action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - Generated by CloudFormation (recommended)

        :exampleMetadata: lit=test/example.attaching.lit.ts infused

        Example::

            user = User(self, "MyUser", password=cdk.SecretValue.unsafe_plain_text("1234"))
            group = Group(self, "MyGroup")
            
            policy = Policy(self, "MyPolicy")
            policy.attach_to_user(user)
            group.attach_inline_policy(policy)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bbdec7edf55e340fa7e131634dc50f0987688d4a15a2d6a018c8efd08343f2)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument password_reset_required", value=password_reset_required, expected_type=type_hints["password_reset_required"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if password is not None:
            self._values["password"] = password
        if password_reset_required is not None:
            self._values["password_reset_required"] = password_reset_required
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        '''Groups to add this user to.

        You can also use ``addToGroup`` to add this
        user to a group.

        :default: - No groups.
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List["IGroup"]], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[IManagedPolicy]]:
        '''A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[IManagedPolicy]], result)

    @builtins.property
    def password(self) -> typing.Optional[_aws_cdk_core_f4b25747.SecretValue]:
        '''The password for the user. This is required so the user can access the AWS Management Console.

        You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or
        use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in
        Secrets Manager.

        :default: - User won't be able to access the management console without a password.
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SecretValue], result)

    @builtins.property
    def password_reset_required(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console.

        If this is set to 'true', you must also specify "initialPassword".

        :default: false
        '''
        result = self._values.get("password_reset_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the user name.

        For more information about paths, see IAM
        Identifiers in the IAM User Guide.

        :default: /
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[IManagedPolicy], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM user.

        For valid values, see the UserName parameter for
        the CreateUser action in the IAM API Reference. If you don't specify a
        name, AWS CloudFormation generates a unique physical ID and uses that ID
        for the user name.

        If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default: - Generated by CloudFormation (recommended)
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.WithoutPolicyUpdatesOptions",
    jsii_struct_bases=[],
    name_mapping={"add_grants_to_resources": "addGrantsToResources"},
)
class WithoutPolicyUpdatesOptions:
    def __init__(
        self,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options for the ``withoutPolicyUpdates()`` modifier of a Role.

        :param add_grants_to_resources: Add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            
            without_policy_updates_options = iam.WithoutPolicyUpdatesOptions(
                add_grants_to_resources=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73638bc56584c021f9745d8cb4ebead059b67a3c5c4e2f1e08fff8af7854c120)
            check_type(argname="argument add_grants_to_resources", value=add_grants_to_resources, expected_type=type_hints["add_grants_to_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_grants_to_resources is not None:
            self._values["add_grants_to_resources"] = add_grants_to_resources

    @builtins.property
    def add_grants_to_resources(self) -> typing.Optional[builtins.bool]:
        '''Add grants to resources instead of dropping them.

        If this is ``false`` or not specified, grant permissions added to this role are ignored.
        It is your own responsibility to make sure the role has the required permissions.

        If this is ``true``, any grant permissions will be added to the resource instead.

        :default: false
        '''
        result = self._values.get("add_grants_to_resources")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WithoutPolicyUpdatesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAccessKey)
class AccessKey(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.AccessKey",
):
    '''Define a new IAM Access Key.

    :exampleMetadata: infused

    Example::

        # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
        user = iam.User(self, "User")
        access_key = iam.AccessKey(self, "AccessKey", user=user)
        secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
        secretsmanager.Secret(self, "Secret",
            secret_string_beta1=secret_value
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        user: "IUser",
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[AccessKeyStatus] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param user: The IAM user this key will belong to. Changing this value will result in the access key being deleted and a new access key (with a different ID and secret value) being assigned to the new user.
        :param serial: A CloudFormation-specific value that signifies the access key should be replaced/rotated. This value can only be incremented. Incrementing this value will cause CloudFormation to replace the Access Key resource. Default: - No serial value
        :param status: The status of the access key. An Active access key is allowed to be used to make API calls; An Inactive key cannot. Default: - The access key is active
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1196ea5a664392f4cfd3a1177cf82ad458813724c85cd2d45289c2f2824821)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccessKeyProps(user=user, serial=serial, status=status)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        '''The Access Key ID.'''
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> _aws_cdk_core_f4b25747.SecretValue:
        '''The Secret Access Key.'''
        return typing.cast(_aws_cdk_core_f4b25747.SecretValue, jsii.get(self, "secretAccessKey"))


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IAssumeRolePrincipal")
class IAssumeRolePrincipal(IPrincipal, typing_extensions.Protocol):
    '''A type of principal that has more control over its own representation in AssumeRolePolicyDocuments.

    More complex types of identity providers need more control over Role's policy documents
    than simply ``{ Effect: 'Allow', Action: 'AssumeRole', Principal: <Whatever> }``.

    If that control is necessary, they can implement ``IAssumeRolePrincipal`` to get full
    access to a Role's AssumeRolePolicyDocument.
    '''

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, document: PolicyDocument) -> None:
        '''Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param document: -
        '''
        ...


class _IAssumeRolePrincipalProxy(
    jsii.proxy_for(IPrincipal), # type: ignore[misc]
):
    '''A type of principal that has more control over its own representation in AssumeRolePolicyDocuments.

    More complex types of identity providers need more control over Role's policy documents
    than simply ``{ Effect: 'Allow', Action: 'AssumeRole', Principal: <Whatever> }``.

    If that control is necessary, they can implement ``IAssumeRolePrincipal`` to get full
    access to a Role's AssumeRolePolicyDocument.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IAssumeRolePrincipal"

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, document: PolicyDocument) -> None:
        '''Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param document: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972a428e334ed7557d17a312b1a5ce5ab4170289638f751ee67dcb114d2d0cbf)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [document]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAssumeRolePrincipal).__jsii_proxy_class__ = lambda : _IAssumeRolePrincipalProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IComparablePrincipal")
class IComparablePrincipal(IPrincipal, typing_extensions.Protocol):
    '''Interface for principals that can be compared.

    This only needs to be implemented for principals that could potentially be value-equal.
    Identity-equal principals will be handled correctly by default.
    '''

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return a string format of this principal which should be identical if the two principals are the same.'''
        ...


class _IComparablePrincipalProxy(
    jsii.proxy_for(IPrincipal), # type: ignore[misc]
):
    '''Interface for principals that can be compared.

    This only needs to be implemented for principals that could potentially be value-equal.
    Identity-equal principals will be handled correctly by default.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IComparablePrincipal"

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return a string format of this principal which should be identical if the two principals are the same.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComparablePrincipal).__jsii_proxy_class__ = lambda : _IComparablePrincipalProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IIdentity")
class IIdentity(
    IPrincipal,
    _aws_cdk_core_f4b25747.IResource,
    typing_extensions.Protocol,
):
    '''A construct that represents an IAM principal, such as a user, group or role.'''

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''Attaches a managed policy to this principal.

        :param policy: The managed policy.
        '''
        ...

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''Attaches an inline policy to this principal.

        This is the same as calling ``policy.addToXxx(principal)``.

        :param policy: The policy resource to attach to this principal [disable-awslint:ref-via-interface].
        '''
        ...


class _IIdentityProxy(
    jsii.proxy_for(IPrincipal), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''A construct that represents an IAM principal, such as a user, group or role.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IIdentity"

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''Attaches a managed policy to this principal.

        :param policy: The managed policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2642bda5e4ebb783baa8fd71c9f1225762beb2d586a47c5826c18db719ad57b)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''Attaches an inline policy to this principal.

        This is the same as calling ``policy.addToXxx(principal)``.

        :param policy: The policy resource to attach to this principal [disable-awslint:ref-via-interface].
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31256906c2b77ab2b201f0ade60935c825f65bd1df7004c7d2f4bf6dfaffa7ce)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIdentity).__jsii_proxy_class__ = lambda : _IIdentityProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IRole")
class IRole(IIdentity, typing_extensions.Protocol):
    '''A Role object.'''

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''Returns the ARN of this role.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''Returns the name of this role.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: IPrincipal, *actions: builtins.str) -> Grant:
        '''Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -
        '''
        ...

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, grantee: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to assume this role.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to pass this role.

        :param grantee: -
        '''
        ...


class _IRoleProxy(
    jsii.proxy_for(IIdentity), # type: ignore[misc]
):
    '''A Role object.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IRole"

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''Returns the ARN of this role.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''Returns the name of this role.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: IPrincipal, *actions: builtins.str) -> Grant:
        '''Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bbf007e438e8a325f2443245fe2bfbbd84c18086467993163047b69084597f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, grantee: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to assume this role.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea08784bf3a8fca3be421be0c84aa317fc766521bff27cb315f5e0d53c9b069)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(Grant, jsii.invoke(self, "grantAssumeRole", [grantee]))

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to pass this role.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9780945a90890af7ddac80bb2bc0e3be8634b7e2e3eec5876ad0365516166e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(Grant, jsii.invoke(self, "grantPassRole", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRole).__jsii_proxy_class__ = lambda : _IRoleProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IUser")
class IUser(IIdentity, typing_extensions.Protocol):
    '''Represents an IAM user.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html
    '''

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> builtins.str:
        '''The user's ARN.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The user's name.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        '''Adds this user to a group.

        :param group: -
        '''
        ...


class _IUserProxy(
    jsii.proxy_for(IIdentity), # type: ignore[misc]
):
    '''Represents an IAM user.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IUser"

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> builtins.str:
        '''The user's ARN.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userArn"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The user's name.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        '''Adds this user to a group.

        :param group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cec78607c2ad8f3a60f7e6ca0dd40627fc0fb139e6fc5859478e1eebbd958a)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "addToGroup", [group]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUser).__jsii_proxy_class__ = lambda : _IUserProxy


@jsii.implements(IRole)
class LazyRole(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.LazyRole",
):
    '''An IAM role that only gets attached to the construct tree once it gets used, not before.

    This construct can be used to simplify logic in other constructs
    which need to create a role but only if certain configurations occur
    (such as when AutoScaling is configured). The role can be configured in one
    place, but if it never gets used it doesn't get instantiated and will
    not be synthesized or deployed.

    :resource: AWS::IAM::Role
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import aws_cdk.core as cdk
        
        # managed_policy: iam.ManagedPolicy
        # policy_document: iam.PolicyDocument
        # principal: iam.IPrincipal
        
        lazy_role = iam.LazyRole(self, "MyLazyRole",
            assumed_by=principal,
        
            # the properties below are optional
            description="description",
            external_id="externalId",
            external_ids=["externalIds"],
            inline_policies={
                "inline_policies_key": policy_document
            },
            managed_policies=[managed_policy],
            max_session_duration=cdk.Duration.minutes(30),
            path="path",
            permissions_boundary=managed_policy,
            role_name="roleName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8320125dcd239abc42a114eab6bfe14fb580a77496edd667a6e4da944de817b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LazyRoleProps(
            assumed_by=assumed_by,
            description=description,
            external_id=external_id,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''Attaches a managed policy to this role.

        :param policy: The managed policy to attach.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e4bdb4c847eba36b4bf83015f6cf2a6300c3c75349321d51f355707d236885)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8656d2c87037829495462582804ee7e0936cd11a330744192b58f5a7ecab8a8)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Adds a permission to the role's default policy document.

        If there is no default policy attached to this role, it will be created.

        :param statement: The permission statement to add to the policy document.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a953333ba85b431f4c1993553c5e2a85803b713710beb7f8206289e0dc1feae2)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''Attaches a policy to this role.

        :param policy: The policy to attach.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b754135137ad1ce46a7a3fc747726c15950dc4896358f19dbf155c176932e05)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @jsii.member(jsii_name="grant")
    def grant(self, identity: IPrincipal, *actions: builtins.str) -> Grant:
        '''Grant the actions defined in actions to the identity Principal on this resource.

        :param identity: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a784b4445844efe61a8cbfcc5764b3e83aafebfc471c236d2fa64d9f446371ef)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(Grant, jsii.invoke(self, "grant", [identity, *actions]))

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, identity: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to assume this role.

        :param identity: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328682402597832ac7d8b80f349a466132a8cf29ec8f5d4a25f738ac48898b8b)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantAssumeRole", [identity]))

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to pass this role.

        :param identity: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd25e6fb7fa044bacc3b73c9291a9d35dc4433d60128cc851a22b0d4d4f04375)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantPassRole", [identity]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''Returns the ARN of this role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''Returns the stable and unique string identifying the role (i.e. AIDAJQABLZS4A3QDU576Q).

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''Returns the name of this role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iam.LazyRoleProps",
    jsii_struct_bases=[RoleProps],
    name_mapping={
        "assumed_by": "assumedBy",
        "description": "description",
        "external_id": "externalId",
        "external_ids": "externalIds",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "role_name": "roleName",
    },
)
class LazyRoleProps(RoleProps):
    def __init__(
        self,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a LazyRole.

        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.core as cdk
            
            # managed_policy: iam.ManagedPolicy
            # policy_document: iam.PolicyDocument
            # principal: iam.IPrincipal
            
            lazy_role_props = iam.LazyRoleProps(
                assumed_by=principal,
            
                # the properties below are optional
                description="description",
                external_id="externalId",
                external_ids=["externalIds"],
                inline_policies={
                    "inline_policies_key": policy_document
                },
                managed_policies=[managed_policy],
                max_session_duration=cdk.Duration.minutes(30),
                path="path",
                permissions_boundary=managed_policy,
                role_name="roleName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ea9408bae156a8893fade732747f6c0b5b8711aeda7ff9c0a32a7b9b96e400)
            check_type(argname="argument assumed_by", value=assumed_by, expected_type=type_hints["assumed_by"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument external_ids", value=external_ids, expected_type=type_hints["external_ids"])
            check_type(argname="argument inline_policies", value=inline_policies, expected_type=type_hints["inline_policies"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument max_session_duration", value=max_session_duration, expected_type=type_hints["max_session_duration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assumed_by": assumed_by,
        }
        if description is not None:
            self._values["description"] = description
        if external_id is not None:
            self._values["external_id"] = external_id
        if external_ids is not None:
            self._values["external_ids"] = external_ids
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def assumed_by(self) -> IPrincipal:
        '''The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role.

        You can later modify the assume role policy document by accessing it via
        the ``assumeRolePolicy`` property.
        '''
        result = self._values.get("assumed_by")
        assert result is not None, "Required property 'assumed_by' is missing"
        return typing.cast(IPrincipal, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role.

        It can be up to 1000 characters long.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ID that the role assumer needs to provide when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required

        :deprecated: see {@link externalIds}

        :stability: deprecated
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required
        '''
        result = self._values.get("external_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PolicyDocument]]:
        '''A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        :default: - No policy is inlined in the Role resource.
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PolicyDocument]], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[IManagedPolicy]]:
        '''A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[IManagedPolicy]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        :default: Duration.hours(1)

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        :default: /
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[IManagedPolicy], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the role name.
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAssumeRolePrincipal, IComparablePrincipal)
class PrincipalBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-iam.PrincipalBase",
):
    '''Base class for policy principals.

    :exampleMetadata: infused

    Example::

        tag_param = CfnParameter(self, "TagName")
        
        string_equals = CfnJson(self, "ConditionJson",
            value={
                "f"aws:PrincipalTag/{tagParam.valueAsString}"": True
            }
        )
        
        principal = iam.AccountRootPrincipal().with_conditions({
            "StringEquals": string_equals
        })
        
        iam.Role(self, "MyRole", assumed_by=principal)
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, document: PolicyDocument) -> None:
        '''Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param document: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6509d0fe8a3195b520146085db72e93f1e5f02ba2243b923c655abc6cd3b097)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [document]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b81846823e1c416ed2f15b2066fa88880fa369f8901a1152563ba841db4ab71)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        _statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Add to the policy of this principal.

        :param _statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5d0bfdc9eb297bb2b4cc6bcdc9ba4a455873fd46445eef0349077535e994d7)
            check_type(argname="argument _statement", value=_statement, expected_type=type_hints["_statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [_statement]))

    @jsii.member(jsii_name="dedupeString")
    @abc.abstractmethod
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        ...

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''JSON-ify the principal.

        Used when JSON.stringify() is called
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="withConditions")
    def with_conditions(
        self,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> "PrincipalBase":
        '''Returns a new PrincipalWithConditions using this principal as the base, with the passed conditions added.

        When there is a value for the same operator and key in both the principal and the
        conditions parameter, the value from the conditions parameter will be used.

        :param conditions: -

        :return: a new PrincipalWithConditions object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4647de623099170c468b7b7ce413d55eae89eee6b0430f23994c2382c4392e4c)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast("PrincipalBase", jsii.invoke(self, "withConditions", [conditions]))

    @jsii.member(jsii_name="withSessionTags")
    def with_session_tags(self) -> "PrincipalBase":
        '''Returns a new principal using this principal as the base, with session tags enabled.

        :return: a new SessionTagsPrincipal object.
        '''
        return typing.cast("PrincipalBase", jsii.invoke(self, "withSessionTags", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    @abc.abstractmethod
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class _PrincipalBaseProxy(PrincipalBase):
    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PrincipalBase).__jsii_proxy_class__ = lambda : _PrincipalBaseProxy


class PrincipalWithConditions(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.PrincipalWithConditions",
):
    '''An IAM principal with additional conditions specifying when the policy is in effect.

    For more information about conditions, see:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # conditions: Any
        # principal: iam.IPrincipal
        
        principal_with_conditions = iam.PrincipalWithConditions(principal, {
            "conditions_key": conditions
        })
    '''

    def __init__(
        self,
        principal: IPrincipal,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''
        :param principal: -
        :param conditions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d8ce15b8a96ebb7ad13cd2d9ae0ac51ce7b4665bb51e601fef6ffd75d2f8b6)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [principal, conditions])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, key: builtins.str, value: typing.Any) -> None:
        '''Add a condition to the principal.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318b378235d5bc15e4fe80d91f6feb5a24db531e0885f842c579023de4ad51b4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addCondition", [key, value]))

    @jsii.member(jsii_name="addConditions")
    def add_conditions(
        self,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''Adds multiple conditions to the principal.

        Values from the conditions parameter will overwrite existing values with the same operator
        and key.

        :param conditions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6664357d004f0b7c02759cc786577cbafcfb15bca7f5cb2a00ad44e3b84b97)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast(None, jsii.invoke(self, "addConditions", [conditions]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f665f540b23cee37ee4fbf5c2969dd8ce2f308824c4ba8befa586b832431596)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba50917207740ba8aedfc135d52dfd99e7719c5460f5a052b95812036f3d34b5)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="appendDedupe")
    def _append_dedupe(self, append: builtins.str) -> typing.Optional[builtins.str]:
        '''Append the given string to the wrapped principal's dedupe string (if available).

        :param append: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02204e082a4920651e1aa8c2236c92067880094f3e49f7a1eb3bd72713fb044)
            check_type(argname="argument append", value=append, expected_type=type_hints["append"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "appendDedupe", [append]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''JSON-ify the principal.

        Used when JSON.stringify() is called
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''The conditions under which the policy is in effect.

        See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


@jsii.implements(IRole)
class Role(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.Role",
):
    '''IAM Role.

    Defines an IAM role. The role is created with an assume policy document associated with
    the specified AWS service principal defined in ``serviceAssumeRole``.

    :exampleMetadata: infused

    Example::

        lambda_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Example role..."
        )
        
        stream = kinesis.Stream(self, "MyEncryptedStream",
            encryption=kinesis.StreamEncryption.KMS
        )
        
        # give lambda permissions to read stream
        stream.grant_read(lambda_role)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5310503b06cb08bf4e519ee12a836aed92f0157b0098b61f40394151e6c68d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RoleProps(
            assumed_by=assumed_by,
            description=description,
            external_id=external_id,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRoleArn")
    @builtins.classmethod
    def from_role_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        role_arn: builtins.str,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> IRole:
        '''Import an external role by ARN.

        If the imported Role ARN is a Token (such as a
        ``CfnParameter.valueAsString`` or a ``Fn.importValue()``) *and* the referenced
        role has a ``path`` (like ``arn:...:role/AdminRoles/Alice``), the
        ``roleName`` property will not resolve to the correct value. Instead it
        will resolve to the first path component. We unfortunately cannot express
        the correct calculation of the full path name as a CloudFormation
        expression. In this scenario the Role ARN should be supplied without the
        ``path`` in order to resolve the correct role resource.

        :param scope: construct scope.
        :param id: construct id.
        :param role_arn: the ARN of the role to import.
        :param add_grants_to_resources: For immutable roles: add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false
        :param mutable: Whether the imported role can be modified by attaching policy resources to it. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc04d40f94cd6d0f99a4b58dbff2622ef59c97d6d0e89b44138c085a55baed5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        options = FromRoleArnOptions(
            add_grants_to_resources=add_grants_to_resources, mutable=mutable
        )

        return typing.cast(IRole, jsii.sinvoke(cls, "fromRoleArn", [scope, id, role_arn, options]))

    @jsii.member(jsii_name="fromRoleName")
    @builtins.classmethod
    def from_role_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        role_name: builtins.str,
    ) -> IRole:
        '''Import an external role by name.

        The imported role is assumed to exist in the same account as the account
        the scope's containing Stack is being deployed to.

        :param scope: -
        :param id: -
        :param role_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b0801e8767218a1f10a6b7f943066a2bfd13f8dd703870ffe8fb0fe070ad48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        return typing.cast(IRole, jsii.sinvoke(cls, "fromRoleName", [scope, id, role_name]))

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''Attaches a managed policy to this role.

        :param policy: The the managed policy to attach.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1409c8d57af433c248a3cb14497f90b18f4961bee23fdd10841633f37365f13)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c8f4cd4d560f7674297c9d27079a906f9df6a5f59002d1505284e5c496dfcc)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Adds a permission to the role's default policy document.

        If there is no default policy attached to this role, it will be created.

        :param statement: The permission statement to add to the policy document.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1663903ef35b51c36e52a32d691c4315a662e7192dbf0725d3ecf8f3adbf20e)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''Attaches a policy to this role.

        :param policy: The policy to attach.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9476a5a3896120f258e0dbf2171197d018922281c1a496c483e88f9c3a78e26)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: IPrincipal, *actions: builtins.str) -> Grant:
        '''Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c73fa12ae3016bd2f877477f5c46e739db8e8f59c24a717c4c5a3d1530e9ed2)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, identity: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to assume this role.

        :param identity: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ce147fd473fe9ab3d27e627921bd1ce9619cac7db8bcbd195be72797bc04d6)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantAssumeRole", [identity]))

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: IPrincipal) -> Grant:
        '''Grant permissions to the given principal to pass this role.

        :param identity: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06a0013905fac13736121e4670a1d2f35a3cc6f3c9e558503ef4f8488b3b40a)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantPassRole", [identity]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @jsii.member(jsii_name="withoutPolicyUpdates")
    def without_policy_updates(
        self,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
    ) -> IRole:
        '''Return a copy of this Role object whose Policies will not be updated.

        Use the object returned by this method if you want this Role to be used by
        a construct without it automatically updating the Role's Policies.

        If you do, you are responsible for adding the correct statements to the
        Role's policies yourself.

        :param add_grants_to_resources: Add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false
        '''
        options = WithoutPolicyUpdatesOptions(
            add_grants_to_resources=add_grants_to_resources
        )

        return typing.cast(IRole, jsii.invoke(self, "withoutPolicyUpdates", [options]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Returns the role.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''Returns the ARN of this role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''Returns the stable and unique string identifying the role.

        For example,
        AIDAJQABLZS4A3QDU576Q.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''Returns the name of the role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicy")
    def assume_role_policy(self) -> typing.Optional[PolicyDocument]:
        '''The assume role policy document associated with this role.'''
        return typing.cast(typing.Optional[PolicyDocument], jsii.get(self, "assumeRolePolicy"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''Returns the permissions boundary attached to this role.'''
        return typing.cast(typing.Optional[IManagedPolicy], jsii.get(self, "permissionsBoundary"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class ServicePrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.ServicePrincipal",
):
    '''An IAM principal that represents an AWS service (i.e. sqs.amazonaws.com).

    :exampleMetadata: infused

    Example::

        lambda_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Example role..."
        )
        
        stream = kinesis.Stream(self, "MyEncryptedStream",
            encryption=kinesis.StreamEncryption.KMS
        )
        
        # give lambda permissions to read stream
        stream.grant_read(lambda_role)
    '''

    def __init__(
        self,
        service: builtins.str,
        *,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: AWS service (i.e. sqs.amazonaws.com).
        :param conditions: Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: (deprecated) The region in which the service is operating. Default: - the current Stack's region.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1376a4c35e10feb7c23273982992d9c562526a4539d121c5e3d4984c3737e5)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        opts = ServicePrincipalOpts(conditions=conditions, region=region)

        jsii.create(self.__class__, self, [service, opts])

    @jsii.member(jsii_name="servicePrincipalName")
    @builtins.classmethod
    def service_principal_name(cls, service: builtins.str) -> builtins.str:
        '''Translate the given service principal name based on the region it's used in.

        For example, for Chinese regions this may (depending on whether that's necessary
        for the given service principal) append ``.cn`` to the name.

        The ``region-info`` module is used to obtain this information.

        :param service: -

        Example::

            principal_name = iam.ServicePrincipal.service_principal_name("ec2.amazonaws.com")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761e37ce11275c00b8a2906ea6ce2266748a75cfc7812d4a06fae7133d17cf73)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "servicePrincipalName", [service]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        '''AWS service (i.e. sqs.amazonaws.com).'''
        return typing.cast(builtins.str, jsii.get(self, "service"))


class SessionTagsPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.SessionTagsPrincipal",
):
    '''Enables session tags on role assumptions from a principal.

    For more information on session tags, see:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # principal: iam.IPrincipal
        
        session_tags_principal = iam.SessionTagsPrincipal(principal)
    '''

    def __init__(self, principal: IPrincipal) -> None:
        '''
        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365c69e8ecce37f35d494d0bfbb5a829e8fe67517b51d7bee7dfb8d4fce9e796)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        jsii.create(self.__class__, self, [principal])

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, doc: PolicyDocument) -> None:
        '''Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param doc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3034a859e597fc2177ebeeca8441efa20b59d5d48e716133676bf9b86893e2)
            check_type(argname="argument doc", value=doc, expected_type=type_hints["doc"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [doc]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c77de2f3d061a35230b1294017f54f4e3c4497e6be22b32c505c88ab0c86ea)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872615722a89f3e56e0888f565b04c4ea7e211ae81b7acfcfe14a7cbbd4236dc)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="appendDedupe")
    def _append_dedupe(self, append: builtins.str) -> typing.Optional[builtins.str]:
        '''Append the given string to the wrapped principal's dedupe string (if available).

        :param append: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1276bcf70faa8b5916bd4daf4ee04cd191a005c5a546748eee76aa18f2b3be17)
            check_type(argname="argument append", value=append, expected_type=type_hints["append"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "appendDedupe", [append]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class StarPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.StarPrincipal",
):
    '''A principal that uses a literal '*' in the IAM JSON language.

    Some services behave differently when you specify ``Principal: "*"``
    or ``Principal: { AWS: "*" }`` in their resource policy.

    ``StarPrincipal`` renders to ``Principal: *``. Most of the time, you
    should use ``AnyPrincipal`` instead.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        star_principal = iam.StarPrincipal()
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.implements(IIdentity, IUser)
class User(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.User",
):
    '''Define a new IAM user.

    :exampleMetadata: infused

    Example::

        user = iam.User(self, "MyUser") # or User.fromUserName(stack, 'User', 'johnsmith');
        group = iam.Group(self, "MyGroup") # or Group.fromGroupArn(stack, 'Group', 'arn:aws:iam::account-id:group/group-name');
        
        user.add_to_group(group)
        # or
        group.add_user(user)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
        password_reset_required: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param groups: Groups to add this user to. You can also use ``addToGroup`` to add this user to a group. Default: - No groups.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param password: The password for the user. This is required so the user can access the AWS Management Console. You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - User won't be able to access the management console without a password.
        :param password_reset_required: Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console. If this is set to 'true', you must also specify "initialPassword". Default: false
        :param path: The path for the user name. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param user_name: A name for the IAM user. For valid values, see the UserName parameter for the CreateUser action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - Generated by CloudFormation (recommended)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1cc66bf08bcddd3308411891a0f8625a835d950450ee83f69f66c94068383c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UserProps(
            groups=groups,
            managed_policies=managed_policies,
            password=password,
            password_reset_required=password_reset_required,
            path=path,
            permissions_boundary=permissions_boundary,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserArn")
    @builtins.classmethod
    def from_user_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        user_arn: builtins.str,
    ) -> IUser:
        '''Import an existing user given a user ARN.

        If the ARN comes from a Token, the User cannot have a path; if so, any attempt
        to reference its username will fail.

        :param scope: construct scope.
        :param id: construct id.
        :param user_arn: the ARN of an existing user to import.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28e97129edf7fe21756abb20a6b9b5874b9e53f4e40c5a770746d01b0a33541)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument user_arn", value=user_arn, expected_type=type_hints["user_arn"])
        return typing.cast(IUser, jsii.sinvoke(cls, "fromUserArn", [scope, id, user_arn]))

    @jsii.member(jsii_name="fromUserAttributes")
    @builtins.classmethod
    def from_user_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        user_arn: builtins.str,
    ) -> IUser:
        '''Import an existing user given user attributes.

        If the ARN comes from a Token, the User cannot have a path; if so, any attempt
        to reference its username will fail.

        :param scope: construct scope.
        :param id: construct id.
        :param user_arn: The ARN of the user. Format: arn::iam:::user/
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd81e2731e9d7dc60231f87606b00244609f91da50545761fdb45fcf0b2bc520)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = UserAttributes(user_arn=user_arn)

        return typing.cast(IUser, jsii.sinvoke(cls, "fromUserAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromUserName")
    @builtins.classmethod
    def from_user_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        user_name: builtins.str,
    ) -> IUser:
        '''Import an existing user given a username.

        :param scope: construct scope.
        :param id: construct id.
        :param user_name: the username of the existing user to import.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b6fd2a7895a68ff3a54418adbb02f0ebd749df17f41da28d85319ea549c26e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        return typing.cast(IUser, jsii.sinvoke(cls, "fromUserName", [scope, id, user_name]))

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''Attaches a managed policy to the user.

        :param policy: The managed policy to attach.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117bd5146bf9ba7e7b245046f07c7a2a69a3d7cbcd4cb627ded955c13962b241)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        '''Adds this user to a group.

        :param group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad68249279606cb48fda691ebaa18dd3945afa15a131e08f63dad99484856ea)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "addToGroup", [group]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9e829f6f9d4874baace56b79e3aa49d6aeecb70395de96910ef5671acef3ec)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Adds an IAM statement to the default policy.

        :param statement: -

        :return: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e483cede26202629b9c596a6c9e40a80980f076337924fe4af4d736c08b75a7b)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''Attaches a policy to this user.

        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2166432f7837b87207999329845580e5a907d3dc23c64c7d781c7e8b196999d9)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> builtins.str:
        '''An attribute that represents the user's ARN.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userArn"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''An attribute that represents the user name.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''Returns the permissions boundary attached  to this user.'''
        return typing.cast(typing.Optional[IManagedPolicy], jsii.get(self, "permissionsBoundary"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class ArnPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.ArnPrincipal",
):
    '''Specify a principal by the Amazon Resource Name (ARN).

    You can specify AWS accounts, IAM users, Federated SAML users, IAM roles, and specific assumed-role sessions.
    You cannot specify IAM groups or instance profiles as principals

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html
    :exampleMetadata: infused

    Example::

        # network_load_balancer1: elbv2.NetworkLoadBalancer
        # network_load_balancer2: elbv2.NetworkLoadBalancer
        
        
        ec2.VpcEndpointService(self, "EndpointService",
            vpc_endpoint_service_load_balancers=[network_load_balancer1, network_load_balancer2],
            acceptance_required=True,
            allowed_principals=[iam.ArnPrincipal("arn:aws:iam::123456789012:root")]
        )
    '''

    def __init__(self, arn: builtins.str) -> None:
        '''
        :param arn: Amazon Resource Name (ARN) of the principal entity (i.e. arn:aws:iam::123456789012:user/user-name).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c88d55d60093b47e26b74a1f2704359eeddf189e30966955f6a47bbcb0e3dfb)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        jsii.create(self.__class__, self, [arn])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="inOrganization")
    def in_organization(self, organization_id: builtins.str) -> PrincipalBase:
        '''A convenience method for adding a condition that the principal is part of the specified AWS Organization.

        :param organization_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b07a6f49468f29c51c0efdb8a100cdcd964be7ce1a2458a1b18e5ee4f34832c)
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
        return typing.cast(PrincipalBase, jsii.invoke(self, "inOrganization", [organization_id]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''Amazon Resource Name (ARN) of the principal entity (i.e. arn:aws:iam::123456789012:user/user-name).'''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class CanonicalUserPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CanonicalUserPrincipal",
):
    '''A policy principal for canonicalUserIds - useful for S3 bucket policies that use Origin Access identities.

    See https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html

    and

    https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html

    for more details.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        canonical_user_principal = iam.CanonicalUserPrincipal("canonicalUserId")
    '''

    def __init__(self, canonical_user_id: builtins.str) -> None:
        '''
        :param canonical_user_id: unique identifier assigned by AWS for every account. root user and IAM users for an account all see the same ID. (i.e. 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a11266efb4c826f02227dc9055445517d67e75f8ecaffe55232d66e30255a8)
            check_type(argname="argument canonical_user_id", value=canonical_user_id, expected_type=type_hints["canonical_user_id"])
        jsii.create(self.__class__, self, [canonical_user_id])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="canonicalUserId")
    def canonical_user_id(self) -> builtins.str:
        '''unique identifier assigned by AWS for every account.

        root user and IAM users for an account all see the same ID.
        (i.e. 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be)
        '''
        return typing.cast(builtins.str, jsii.get(self, "canonicalUserId"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class CompositePrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.CompositePrincipal",
):
    '''Represents a principal that has multiple types of principals.

    A composite principal cannot
    have conditions. i.e. multiple ServicePrincipals that form a composite principal

    :exampleMetadata: infused

    Example::

        role = iam.Role(self, "MyRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ec2.amazonaws.com"),
                iam.AccountPrincipal("1818188181818187272"))
        )
    '''

    def __init__(self, *principals: IPrincipal) -> None:
        '''
        :param principals: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60652f5792946851af521599a262d1ce8987aa24b66de3eb5f772bddb18238d9)
            check_type(argname="argument principals", value=principals, expected_type=typing.Tuple[type_hints["principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*principals])

    @jsii.member(jsii_name="addPrincipals")
    def add_principals(self, *principals: IPrincipal) -> "CompositePrincipal":
        '''Adds IAM principals to the composite principal.

        Composite principals cannot have
        conditions.

        :param principals: IAM principals that will be added to the composite principal.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72b9a571d348b3b16e06a6e73b9ccdf291162dc75c9630192317efc5852b3df)
            check_type(argname="argument principals", value=principals, expected_type=typing.Tuple[type_hints["principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("CompositePrincipal", jsii.invoke(self, "addPrincipals", [*principals]))

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, doc: PolicyDocument) -> None:
        '''Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param doc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45e66df71d2b0bb2499f9685e9bba94ca2f67ad21fb5b4b4a612a2eb5002140)
            check_type(argname="argument doc", value=doc, expected_type=type_hints["doc"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [doc]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class FederatedPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.FederatedPrincipal",
):
    '''Principal entity that represents a federated identity provider such as Amazon Cognito, that can be used to provide temporary security credentials to users who have been authenticated.

    Additional condition keys are available when the temporary security credentials are used to make a request.
    You can use these keys to write policies that limit the access of federated users.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#condition-keys-wif
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        # conditions: Any
        
        federated_principal = iam.FederatedPrincipal("federated", {
            "conditions_key": conditions
        }, "assumeRoleAction")
    '''

    def __init__(
        self,
        federated: builtins.str,
        conditions: typing.Mapping[builtins.str, typing.Any],
        assume_role_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param federated: federated identity provider (i.e. 'cognito-identity.amazonaws.com' for users authenticated through Cognito).
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        :param assume_role_action: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319be364073e04fce09ad1ef6829af793d0f7193ba238809c0a3f4cbf1bd252d)
            check_type(argname="argument federated", value=federated, expected_type=type_hints["federated"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument assume_role_action", value=assume_role_action, expected_type=type_hints["assume_role_action"])
        jsii.create(self.__class__, self, [federated, conditions, assume_role_action])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''The conditions under which the policy is in effect.

        See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="federated")
    def federated(self) -> builtins.str:
        '''federated identity provider (i.e. 'cognito-identity.amazonaws.com' for users authenticated through Cognito).'''
        return typing.cast(builtins.str, jsii.get(self, "federated"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.interface(jsii_type="@aws-cdk/aws-iam.IGroup")
class IGroup(IIdentity, typing_extensions.Protocol):
    '''Represents an IAM Group.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html
    '''

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''Returns the IAM Group ARN.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''Returns the IAM Group Name.

        :attribute: true
        '''
        ...


class _IGroupProxy(
    jsii.proxy_for(IIdentity), # type: ignore[misc]
):
    '''Represents an IAM Group.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iam.IGroup"

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''Returns the IAM Group ARN.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''Returns the IAM Group Name.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGroup).__jsii_proxy_class__ = lambda : _IGroupProxy


class OrganizationPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.OrganizationPrincipal",
):
    '''A principal that represents an AWS Organization.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        organization_principal = iam.OrganizationPrincipal("organizationId")
    '''

    def __init__(self, organization_id: builtins.str) -> None:
        '''
        :param organization_id: The unique identifier (ID) of an organization (i.e. o-12345abcde).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562487b4013dd2fd82be5ae3009fa1fc859a99b5d75a6d8651b6a8c7e4361db8)
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
        jsii.create(self.__class__, self, [organization_id])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        '''The unique identifier (ID) of an organization (i.e. o-12345abcde).'''
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class SamlPrincipal(
    FederatedPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.SamlPrincipal",
):
    '''Principal entity that represents a SAML federated identity provider.

    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        principal = iam.SamlPrincipal(provider, {
            "StringEquals": {
                "SAML:iss": "issuer"
            }
        })
    '''

    def __init__(
        self,
        saml_provider: ISamlProvider,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''
        :param saml_provider: -
        :param conditions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8481f3c1ca211152a5191d582999d8e7bb2fff5d0e149356327018a98743c01b)
            check_type(argname="argument saml_provider", value=saml_provider, expected_type=type_hints["saml_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [saml_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


class WebIdentityPrincipal(
    FederatedPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.WebIdentityPrincipal",
):
    '''A principal that represents a federated identity provider as Web Identity such as Cognito, Amazon, Facebook, Google, etc.

    :exampleMetadata: infused

    Example::

        principal = iam.WebIdentityPrincipal("cognito-identity.amazonaws.com", {
            "StringEquals": {"cognito-identity.amazonaws.com:aud": "us-east-2:12345678-abcd-abcd-abcd-123456"},
            "ForAnyValue:StringLike": {"cognito-identity.amazonaws.com:amr": "unauthenticated"}
        })
    '''

    def __init__(
        self,
        identity_provider: builtins.str,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param identity_provider: identity provider (i.e. 'cognito-identity.amazonaws.com' for users authenticated through Cognito).
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2caca9727510c3ea3cd74a70ea73a3e1adbbbb87080ed6373bfcdc14e19bef)
            check_type(argname="argument identity_provider", value=identity_provider, expected_type=type_hints["identity_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [identity_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class AccountPrincipal(
    ArnPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.AccountPrincipal",
):
    '''Specify AWS account ID as the principal entity in a policy to delegate authority to the account.

    :exampleMetadata: infused

    Example::

        cluster = neptune.DatabaseCluster(self, "Cluster",
            vpc=vpc,
            instance_type=neptune.InstanceType.R5_LARGE,
            iam_authentication=True
        )
        role = iam.Role(self, "DBRole", assumed_by=iam.AccountPrincipal(self.account))
        cluster.grant_connect(role)
    '''

    def __init__(self, account_id: typing.Any) -> None:
        '''
        :param account_id: AWS account ID (i.e. 123456789012).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b1a3fd75474b5951cc226ed31323155cea4b73c2f8df408c5332dbb6e42f9a)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        jsii.create(self.__class__, self, [account_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> typing.Any:
        '''AWS account ID (i.e. 123456789012).'''
        return typing.cast(typing.Any, jsii.get(self, "accountId"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class AccountRootPrincipal(
    AccountPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.AccountRootPrincipal",
):
    '''Use the AWS account into which a stack is deployed as the principal entity in a policy.

    :exampleMetadata: infused

    Example::

        bucket = s3.Bucket(self, "MyBucket")
        result = bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[bucket.arn_for_objects("file.txt")],
            principals=[iam.AccountRootPrincipal()]
        ))
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


class AnyPrincipal(
    ArnPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.AnyPrincipal",
):
    '''A principal representing all AWS identities in all accounts.

    Some services behave differently when you specify ``Principal: '*'``
    or ``Principal: { AWS: "*" }`` in their resource policy.

    ``AnyPrincipal`` renders to ``Principal: { AWS: "*" }``. This is correct
    most of the time, but in cases where you need the other principal,
    use ``StarPrincipal`` instead.

    :exampleMetadata: infused

    Example::

        topic = sns.Topic(self, "Topic")
        topic_policy = sns.TopicPolicy(self, "TopicPolicy",
            topics=[topic]
        )
        
        topic_policy.document.add_statements(iam.PolicyStatement(
            actions=["sns:Subscribe"],
            principals=[iam.AnyPrincipal()],
            resources=[topic.topic_arn]
        ))
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


class Anyone(
    AnyPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.Anyone",
):
    '''(deprecated) A principal representing all identities in all accounts.

    :deprecated: use ``AnyPrincipal``

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        
        anyone = iam.Anyone()
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])


@jsii.implements(IGroup)
class Group(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.Group",
):
    '''An IAM Group (collection of IAM users) lets you specify permissions for multiple users, which can make it easier to manage permissions for those users.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html
    :exampleMetadata: infused

    Example::

        user = iam.User(self, "MyUser") # or User.fromUserName(stack, 'User', 'johnsmith');
        group = iam.Group(self, "MyGroup") # or Group.fromGroupArn(stack, 'Group', 'arn:aws:iam::account-id:group/group-name');
        
        user.add_to_group(group)
        # or
        group.add_user(user)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param group_name: A name for the IAM group. For valid values, see the GroupName parameter for the CreateGroup action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: Generated by CloudFormation (recommended)
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param path: The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_ in the IAM User Guide. Default: /
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409cfeca6e6922e7ee3cdf263415a04a486073dd467345e230f31c297f0b79b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GroupProps(
            group_name=group_name, managed_policies=managed_policies, path=path
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGroupArn")
    @builtins.classmethod
    def from_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_arn: builtins.str,
    ) -> IGroup:
        '''Import an external group by ARN.

        If the imported Group ARN is a Token (such as a
        ``CfnParameter.valueAsString`` or a ``Fn.importValue()``) *and* the referenced
        group has a ``path`` (like ``arn:...:group/AdminGroup/NetworkAdmin``), the
        ``groupName`` property will not resolve to the correct value. Instead it
        will resolve to the first path component. We unfortunately cannot express
        the correct calculation of the full path name as a CloudFormation
        expression. In this scenario the Group ARN should be supplied without the
        ``path`` in order to resolve the correct group resource.

        :param scope: construct scope.
        :param id: construct id.
        :param group_arn: the ARN of the group to import (e.g. ``arn:aws:iam::account-id:group/group-name``).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af8f05aea5eb6362bcc8f7aeda9062007508bac177ae79d0ae1fb101bcfcd1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_arn", value=group_arn, expected_type=type_hints["group_arn"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupArn", [scope, id, group_arn]))

    @jsii.member(jsii_name="fromGroupName")
    @builtins.classmethod
    def from_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_name: builtins.str,
    ) -> IGroup:
        '''Import an existing group by given name (with path).

        This method has same caveats of ``fromGroupArn``

        :param scope: construct scope.
        :param id: construct id.
        :param group_name: the groupName (path included) of the existing group to import.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb5bb3baceeab48f20d3209703cb59da83880a94cc8ec150e6d5efdc541f4c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupName", [scope, id, group_name]))

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''Attaches a managed policy to this group.

        :param policy: The managed policy to attach.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9385cd1dd4945c15cc2a3995aed43175a8bec43dc44783cb1a4c8e05222ff90)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''Add to the policy of this principal.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496ca44e870019b4c461eea4f219308f9801fb5b28a85ab4dfc098f0e32b7893)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''Adds an IAM statement to the default policy.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3dc32e918311088c1b9a74f434356723433fffaeed088de8369221de62f1b9)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="addUser")
    def add_user(self, user: IUser) -> None:
        '''Adds a user to this group.

        :param user: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44228d06c84d7053e8f7c57a0798f1cc000aa0dc20b87550f88fbaccc1e45c2)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "addUser", [user]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''Attaches a policy to this group.

        :param policy: The policy to attach.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b184157e50f3eee6c022b25e939b0489a4c08286f7d405747d1041931cb88006)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''When this Principal is used in an AssumeRole policy, the action to use.'''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''Returns the IAM Group ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''Returns the IAM Group Name.'''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class OpenIdConnectPrincipal(
    WebIdentityPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.OpenIdConnectPrincipal",
):
    '''A principal that represents a federated identity provider as from a OpenID Connect provider.

    :exampleMetadata: infused

    Example::

        provider = iam.OpenIdConnectProvider(self, "MyProvider",
            url="https://openid/connect",
            client_ids=["myclient1", "myclient2"]
        )
        principal = iam.OpenIdConnectPrincipal(provider)
    '''

    def __init__(
        self,
        open_id_connect_provider: IOpenIdConnectProvider,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param open_id_connect_provider: OpenID Connect provider.
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e33149b9cb725fe8da999822da7179a8de13ade53853aa2a3b246285d9b2bc)
            check_type(argname="argument open_id_connect_provider", value=open_id_connect_provider, expected_type=type_hints["open_id_connect_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [open_id_connect_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class SamlConsolePrincipal(
    SamlPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iam.SamlConsolePrincipal",
):
    '''Principal entity that represents a SAML federated identity provider for programmatic and AWS Management Console access.

    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        iam.Role(self, "Role",
            assumed_by=iam.SamlConsolePrincipal(provider)
        )
    '''

    def __init__(
        self,
        saml_provider: ISamlProvider,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param saml_provider: -
        :param conditions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91c6812d31a6288a1beea15086a8d79996b41aaba3ec3728ab8b1047e057155)
            check_type(argname="argument saml_provider", value=saml_provider, expected_type=type_hints["saml_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [saml_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of an object.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


__all__ = [
    "AccessKey",
    "AccessKeyProps",
    "AccessKeyStatus",
    "AccountPrincipal",
    "AccountRootPrincipal",
    "AddToPrincipalPolicyResult",
    "AddToResourcePolicyResult",
    "AnyPrincipal",
    "Anyone",
    "ArnPrincipal",
    "CanonicalUserPrincipal",
    "CfnAccessKey",
    "CfnAccessKeyProps",
    "CfnGroup",
    "CfnGroupProps",
    "CfnInstanceProfile",
    "CfnInstanceProfileProps",
    "CfnManagedPolicy",
    "CfnManagedPolicyProps",
    "CfnOIDCProvider",
    "CfnOIDCProviderProps",
    "CfnPolicy",
    "CfnPolicyProps",
    "CfnRole",
    "CfnRoleProps",
    "CfnSAMLProvider",
    "CfnSAMLProviderProps",
    "CfnServerCertificate",
    "CfnServerCertificateProps",
    "CfnServiceLinkedRole",
    "CfnServiceLinkedRoleProps",
    "CfnUser",
    "CfnUserProps",
    "CfnUserToGroupAddition",
    "CfnUserToGroupAdditionProps",
    "CfnVirtualMFADevice",
    "CfnVirtualMFADeviceProps",
    "CommonGrantOptions",
    "ComparablePrincipal",
    "CompositeDependable",
    "CompositePrincipal",
    "Effect",
    "FederatedPrincipal",
    "FromRoleArnOptions",
    "Grant",
    "GrantOnPrincipalAndResourceOptions",
    "GrantOnPrincipalOptions",
    "GrantWithResourceOptions",
    "Group",
    "GroupProps",
    "IAccessKey",
    "IAssumeRolePrincipal",
    "IComparablePrincipal",
    "IGrantable",
    "IGroup",
    "IIdentity",
    "IManagedPolicy",
    "IOpenIdConnectProvider",
    "IPolicy",
    "IPrincipal",
    "IResourceWithPolicy",
    "IRole",
    "ISamlProvider",
    "IUser",
    "LazyRole",
    "LazyRoleProps",
    "ManagedPolicy",
    "ManagedPolicyProps",
    "OpenIdConnectPrincipal",
    "OpenIdConnectProvider",
    "OpenIdConnectProviderProps",
    "OrganizationPrincipal",
    "PermissionsBoundary",
    "Policy",
    "PolicyDocument",
    "PolicyDocumentProps",
    "PolicyProps",
    "PolicyStatement",
    "PolicyStatementProps",
    "PrincipalBase",
    "PrincipalPolicyFragment",
    "PrincipalWithConditions",
    "Role",
    "RoleProps",
    "SamlConsolePrincipal",
    "SamlMetadataDocument",
    "SamlPrincipal",
    "SamlProvider",
    "SamlProviderProps",
    "ServicePrincipal",
    "ServicePrincipalOpts",
    "SessionTagsPrincipal",
    "StarPrincipal",
    "UnknownPrincipal",
    "UnknownPrincipalProps",
    "User",
    "UserAttributes",
    "UserProps",
    "WebIdentityPrincipal",
    "WithoutPolicyUpdatesOptions",
]

publication.publish()

def _typecheckingstub__c3a1416c22de88a620b216c5e13428adb6716ba5f4284a6bb32b744db11b9a6a(
    *,
    user: IUser,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[AccessKeyStatus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ef98f6e162ecc49216a84424a34cbcd99b925e29023b1e6b0a9fce25ea1b3d(
    *,
    statement_added: builtins.bool,
    policy_dependable: typing.Optional[_aws_cdk_core_f4b25747.IDependable] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d9e4e3a3d0914c75521a1473c8de7bb301f6791cdb68e3b3b1bb1f8582d1b1(
    *,
    statement_added: builtins.bool,
    policy_dependable: typing.Optional[_aws_cdk_core_f4b25747.IDependable] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa6cbae092328b8aff5cda78e1da7ba9a694031046f305bb48ecb2139e1c2bb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    user_name: builtins.str,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f15da46a99bc07348d19740b25b14184a985d28f13a8be30e11685b4e8f0ea4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5676e3c6392e8cb0473b4e8782eda56ef98533c8228359495f58e40f44791e65(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860cf915a0ac64b28b68db2c008c248935780719c99ffbf203c320ee0d91ee88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150c776515b1c7523874b462c62a35a1005a23087485081d878132b3a20552a5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d872830178849f932d025904b16ffe79838915ab95f3ee898835f3ebe980037(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7ed84b5ec8a936c144ed47067cb468cacb975f83e5049a1aa8df388b2211e2(
    *,
    user_name: builtins.str,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4017e26628b4ac40c45ae3de3d527ff4ecadaa9969645b50be89f187b5e763(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58dea00a5cd1032971b7708e014f8fdf6e2f535643811c41abd30f74b08a1a91(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2406f072d1428f166ea587cc677807c082d5879a108a89e151aedb3100d638(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c4745df9cc7871b99dffd6f2d05519570d4c623a64f348fedb26d44994a91b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1320df791d0fbdb2f9945b814789f3e61ffe602d962cd041df89a7403b750aee(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9a3f88e09c80c00ca9a22d4d7e27becafee90c18df582b9ff771926216b11e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db9e4304586acb1e7788cc3d393e30ada4edc231c6c9a229611d105ba979c21(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.PolicyProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841b8e984be5df111232d9c9e13f84b35ee9bdce0330bce1446562c8afa01ef7(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c711db90d1b5a925d9125ecd09b35213fb1789bfc4ee6ae24c723c777d58a7(
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7d68a9ce06737826e7884e1c0308d9a217296bcd4fcd51aff93ed3fb01cd2f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    roles: typing.Sequence[builtins.str],
    instance_profile_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48069dc5a780f331b553b4afd9a95cdeb108094e6b93c8d1d7ac02be20fd2af4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455e6a839e50f149eaf163b882a8923c6da91013cca943d98949acc75432d4c4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8dad48aa81c8069fe7c92065526deba65cf5e8dde62a523c27d5db69285bd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4416a6aef16c477160d51976111f48dc45cbb067755c0676bbf135a640348fc5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5291fdd81326b970a438f7a808c39f2afb0268e3df6038d258acf415f50ea29(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5012b618b5e1682b35a1700191a6564fde84e254bfa938a7749a75ad1db0d082(
    *,
    roles: typing.Sequence[builtins.str],
    instance_profile_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7405bd778db44d00c800df1ff74a743b4f71443476bbbf82bbb7d59647a92f0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401a4638da40774f3940f52739980773f86d3a3d2d9d044f4e99745610b6a81f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0de0e4e32e9f9c79989dc34a2ddf138af5b8dc57ab7c813f62cd3254ef51f6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dfa7120d72994241ef14e2366eda9cffadbef2a9b34387428dc1143737735d(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6f95eade608491e1aecd5314e8b30fdc478a0bb58546fd703abddcff4c9d46(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a20464338fa4ab0038165ce78610d3c26ca0e1cf7a42bc4bbe9f5eea156184(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8934b0078389739c7333b9895c38040426347a67cc9b67183e2b1c25ee22da(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5719d42cfe0c8bfb7f56c9921d590677a0616f52f67f2f41e91a09b99b570526(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e4fa36440ede7dabb105c8d71ca16b4592db51c2b48f52ae0f39a0fd9b040d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0f543477844162f6d0d8d8df5bae0ec4edf62f16f5ad382fddf1c891f542f0(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62d487b0e5adc2faf71d6792a8bde6282615f37234599431f92701eed79c5f1(
    *,
    policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64d829cf2255983b6697aaabba068760e784de1807b9c47a49d1b34a7956ce9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    thumbprint_list: typing.Sequence[builtins.str],
    client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ed625d5dc4318aff35627ae253d05ea0ce179c7b09f3f644ce3142f454862e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf722ffce1a2fba9118f611a3c9f9845e4faecb8bdf7e90637b51855bcd8521(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fc4bbecf9e2cc2cabe79ef4b4dfd16cae9e2f208f7df4a45dc785c5b877e42(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79c112e6971b0a138d8e6e383e5afc56227471d7f4505c70cc962668c0638cc(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f82aca862212d2897f4d0cf19491f10b5de81ce369cdadf57b19f2389f790a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9826c7762172f597ccaaa167d81f46fbf181f9114f5ff3f21e111a206ab92e07(
    *,
    thumbprint_list: typing.Sequence[builtins.str],
    client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53162e251261ed8b83b4a1e526c2fbc7a1b73c60fe284f975ca54e9142ff60f4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83ff569c112bcc2c7df18fda83c34af21fa3994a7b0166fa26c24ba34411b66(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c799ad27e30d5147cbcc46b9dd04c3929304116cecb52716ccb568aff25cdc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2006575d3dc0eb086ac238513796a36357a675ee4e1caeb4084bb822853fdf32(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8100e578d852455fc7e3f3dd63215ff3c3c519e1e33c796557866c0f6a743f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c1d43829c7d40c491c798edd408c805b090d47c57bffa10c87cd9a55bedac8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183599a3e80b946121ea4b10ef27ce3acae62930ebac5225501294bac8d599a8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4790e7d3a2a32b62bb7c1204efd6ff86aef80a310da66eb71df7f540e01da93d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd52a4d00a1936382a0a104f9d73ff692ac2923da2c65aad072b062899e7758(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e20f55c1a36eee3998dee673995816ac45fa24cba02d7b0f338417f9a063dd9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    assume_role_policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_session_duration: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRole.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed1a9ba5968e0bfefa71739e4c7effa4d8526abb3ba63359884c3dd3fe1218d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1a61dcb42675b18fb5e48c623661827af4e75e57247f3395f6dd8b4cd47cbe(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b114ac2e39bbff6321e8c6e77f09603448faebed181a5d375725c17143754cbf(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a45d0f55b630b2ee54ea84ce4aeee37cd04205f662404e8cc8c21990b6d141d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbb7787a3d274f9b7e986e6048d6e2e8ef572b452753efa16fdbf0827e4d2b1(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083b7f6a883dc28ffeb90cfa10b1a4b1f0c95d1e20583b27eaa1f6cd665c7c66(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7104656480ab5b150db3309e2d6297a79b04b8c057a3a09a775cfd78ac24490a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1ff4af19ba56e41512ff3c64a881a13912eb1ecf6b36b205cf8265b12f1dc0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f6852edff1517b44bb2125313d6a63ba69b942ee9c5cc599b02035a7504957(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRole.PolicyProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4939c84e3d855a135a406c0160a28bdd110bffe4cc472f852af7ee497f568e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db348398319580afb09df9a6e8aaac71b9cd38e33fc0d1ef33df424c8c72a44b(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e23ac1f54a2cf6c4b3e974cee549ae8cab3cf6b8cc4975c71190746b04aaaa(
    *,
    assume_role_policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_session_duration: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRole.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294dab5076af8fe4c1eb063300635f68b22c4ce3c734b57a8a86d8705f4fdad8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    saml_metadata_document: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa90a949db9ec5ce2faaf15b7f7f4978f4b5d2fc1cc02f9d58b71019c7f00ec(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8c4c5a48a8ceb137cba61aea505824c333479278ed776599e74fbb1fe9fbfc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e00073cf2cb0100ab06d01cbb11a1bd87efc2eecf6c4e8145d7022928958bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646f2fc0c953ba2a1fd3a0476573568efc94bd196135b0e90e507c07e4881b0c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050a5fc7218c11c3ef6cf83de71f21e208ff338265ba15f1f7249e25edb01132(
    *,
    saml_metadata_document: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cd82141ea6355567bc319b1fe2b2203f37f59540405b28851d1ab9fededcea(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    certificate_body: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    server_certificate_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fabbaf3c54b332f1efcff2fc31539d4a4b3635017217ee1e16a7663723bd9fa(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c856c41abeabb83d77254a5dd612869bed959ba0890ef797b94d1cda690737(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b56584bea6da770dc90f791cc3021e6209b63e7a7a3b0e75bb27aba3420b32(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54da6c0bae8473a1e96681fd895db465ac1c31f1499e129fe217f67982ed5953(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d6615c145581b22b8b38012d8276a84e75437939bbfe03cac719994df8f404(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430aa87a52c8287e859646c8f91284c1312380f1592e581741b8b249cd44ee36(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20a33fac28932709bae8ec0bd7663167891cad2bf7bcab7c9b4219e33ca8546(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1b05b92f28b40d20becb202eb7f404df49537aa800d0c58abbd24875e06840(
    *,
    certificate_body: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    server_certificate_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9c457397f8d73807e52c34de324915223e172462011ef0b9fbb4679047dff2(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    aws_service_name: builtins.str,
    custom_suffix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa81902f3634794fbba9a0a17e9b04bb4785c72d5ea8279252a333070da4bb1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415a69be8c7687f580e2fec8645c0ec4b6fb6161e226e8ca9193054d418fb85e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7639b31b7544076a3afb9ce56a6d1f745ea9949a1a30fd8ed9695d65a2794b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57de2588b87139ce77be8f2ec0d3e4dc9cf32a682e08e38abcfb0e220f4700e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace96d55f7a9e12f6b0c1eab1597d57aea340c6ff0c90d46c267da74c2b4d3a1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c9b5f7c3adb35711c582f832e2278f409957d357b28fb87606914f7226bd39(
    *,
    aws_service_name: builtins.str,
    custom_suffix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d3dd58f27d1d8e709d36cb51a4600afb8243e6c2101e832629874c3bf74414(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_profile: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.LoginProfileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2398f45a3f7a4e911de2f808b00634f074f5a280db21237dc439e86daf62d2ab(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8047352af7d4214a63ff9f4d8c2c0363d3429a2708de78bb67427ceaf971c2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d88ed2617b5090b2a6eb2ca7b9e7bb0e53828ea13522ec7359711a3485ca6b8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddc2ec817dc66d81c9d457ef7449ce29220048e088caa0356e911120ae38fe1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.LoginProfileProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78eb07ccf26a62787fb26b2d61e8319e5a80da4e6dfb4cf5dae978520a6710ae(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7629f315b417f7cf63fbec0abbe4b2fba0e28654641f3a7e43c129d9003140c5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8647130c8721eb12e608b6fa0f887311da5518d9d3f2c7361293def7065102e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eeeae1c0ee5573c8f6828270a73d8028e1dfe05fb65de0520d6c0dcf09d7eb6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.PolicyProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee6ff12d58390aca893e9061e4663303463fc7faec174f0ead590a5578903d3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6f98a39b2c2196cf0e1286024bc9e868a2ee7f516604e1eff049fc5aa6c3bc(
    *,
    password: builtins.str,
    password_reset_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c990e121f3865cf05866339719021ab0d1b2a4316fd082823896e43d0d789da6(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2f2cc6b4f4550946b5d6d7176e1cd03666697b01d8c186bd975d069253e6e1(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_profile: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.LoginProfileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e21103b6d2b9e4cb45590a6b552238202915f4bf4de2a94fa11ea06ea7abf3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    group_name: builtins.str,
    users: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f592bca0c422bf0da5a558e6dbf00521f0acb93d7bb2bd989cfc93d6cd1f83(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40bd028a6468e999067863fd39eccd1eff7b2ca135753f53ff810aec4aeff5ab(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07df7e49e6ac358cbdbaf168473a69aeb005aebb726c6c1fbf177b03478bbee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478f6d094573da9b31689ae02c56352f8662729751c552faeaba3d824adb99aa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a659b0fc99fe7eb7e5fba845551db31be9b1bb584be89b92a8bf8b52093cc0f(
    *,
    group_name: builtins.str,
    users: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3403f08c73f1980bec4173c88d8530bef1e628771b1c0cdb6eb85e3a086dc5a5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    users: typing.Sequence[builtins.str],
    path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_mfa_device_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5894ada85a21a17dca4bdf04bde1bcc5bbe810ff08f9c57eeb0b0cbdadd33ad2(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6f5b00cb555552851e4c561f485c8816a4fe1afa3b3769b8bbb64a7059bb87(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab0cd4b6cfc16f8435ab6a9868cb6ad51c88488fe7d6b157574690bedb1a0e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d15db6ecc07b7c414a88d5a8d3f73fbd5016555d499a54d0b4247cd35b248a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cc407504f6903d73f2cb88aa0db80515592dcde339bf20579699bd3ba9bb4e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555c031cad888108e49ac8e771b5195d9a951c9a2707000d35cd98096d183cdb(
    *,
    users: typing.Sequence[builtins.str],
    path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_mfa_device_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80c243305a2120343036db9aac3ad9d03fa7f24316bdcd867921cae2d30a5bf(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feca08928fe78692eb852482844809c53b740556f35309f719722e4aafff0e06(
    x: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5a72947168d3b6e1aa60ee5367b2d93ee05c6cdbceeaf5fbd17c379bedfe3e(
    x: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dad6afeb9a260846d8c4772b9f0c830e599b888951cb7e6cc643004d7e47b43(
    *dependables: _aws_cdk_core_f4b25747.IDependable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118646118fff9e9879f4eed824ef5eb94da275d0f04853ea376fd5bc3837faa2(
    *,
    add_grants_to_resources: typing.Optional[builtins.bool] = None,
    mutable: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f55cf91f13b36d92fcdd7df44173b96a31de327d4247ee3bcd16e28ba617c46(
    grantee: IGrantable,
    _intent: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4761013e67f613e450e8a418b92020eb8d035754f9897a837460850a2fe29ff(
    *constructs: _aws_cdk_core_f4b25747.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5240e00ad90d35024787026562eb22cc617e4be010813eb82081bcab6b383c(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
    resource: IResourceWithPolicy,
    resource_policy_principal: typing.Optional[IPrincipal] = None,
    resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ed81a36fb6f343f7d3d4d71cae9df3f7b7ed222266f214c7e15e6fc22eb916(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
    scope: typing.Optional[_aws_cdk_core_f4b25747.IConstruct] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99cc4cc6a10bf9d2bc27325326f4406ca09872d3e06130c542a2a17e841f3ed(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
    resource: IResourceWithPolicy,
    resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8144e7610672a1371486a23f5193a3506d0c6158e42ae9d2c6fdec2e9db510b(
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be94004d36c6ccf929d56b50921aaa08f12fd4b36aff03724f30a2576afabdf(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d2dc41bf91a97a85e83ebf9fbced7c0a0993c1fa413d6a4bc8d01bd10d515d(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3101adf8418762c0ef550bd95db42a41657d386de7d7a813402ecbbe5d3575d2(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3225cc4e0f8f69f258239a228ad417ea6dea2cafc61e44523faa4936a40f8473(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    document: typing.Optional[PolicyDocument] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ca0bf5f67b2e0333106fd1ddb31099a017160cff348eb85e49658624e833c3(
    managed_policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f18dc25f63148092b66f1a0a7e4b01eaad4acd2edaa00f8d07e18e0d24aba5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    managed_policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c0b4e1f3b803e535e5d207b1dbc6d60c5c7ac1c6743c4e231b8bfccf7836af(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    managed_policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f351fb358e3ea248741489c402ca382cf140d52b7ec4a3454366d03b6b09a375(
    *statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d8669a04f27c8c1e416bff9e17f9ceb769f71560cc35cd6a145280271146b1(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33284e52b2fdf499b024f7f58ca36c5f1291b3ba2f6e35b649f36c4a56163864(
    role: IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfba60db4b1faad126f6fa61bcb991dca47a4c474af6d103fcec30648eb43ac(
    user: IUser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bf03e8d3d35225b12b08a40692e485e7fbeb0faac774b2a22fc17e194d19df(
    *,
    description: typing.Optional[builtins.str] = None,
    document: typing.Optional[PolicyDocument] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d05e6241268ec0fd867633aa632dc97381c9a485e59fdba8d689f6fe6ad7101(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    url: builtins.str,
    client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a4e6a2506d8d1375dc8f48a81a60fdbba25071f5a2b7ac40e5f2581340fbd8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    open_id_connect_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bdf22e31ec661f995d8a432db47cb0019a8a9ed2909c335ea3c4bac43f127f(
    *,
    url: builtins.str,
    client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d69da7b6d8bc505990e1eb87895379b0813715b8c882b44571a72df54fea0d(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a004abccfb7e9f520a9bee4b1e82d9a8274fb48f15b9de19243d42d756f196(
    boundary_policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826753427ab7d968332a2c9889e2e91d777ec1dadc89bd3838de29445311231d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    document: typing.Optional[PolicyDocument] = None,
    force: typing.Optional[builtins.bool] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    policy_name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30dc7936b2b6c50f65f512617c0599c3aa41af2c273a864b732fa441fa198362(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba6b094378fd4f2577b6973a340330e66bffa279da207f8bc38121d48ebf715(
    *statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5813c479c73eea905bb9c38cbb869508b378836a228270dc3af8967047f0ad78(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c377a0806fbb4e951ecc0fabfcd5d658a92c984c16bb23750a8a305d66a5b4dc(
    role: IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ebee8ef3734a2a3f714ebfc0c63c08ae85d0c5a96e2744852c0a25b844cf3e(
    user: IUser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5047bd36f25a6706e3652db23871597db2c9d3102b878e80c347f7e5d3b0b3(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac383c516d1eddb9c561e401aa91d954df10304f6c77b6b7670ef4b4e79739fa(
    *statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedd05de5132f9de2d9fc998e675b63abc427a8da23aeff8c4f95cfb1f76b766(
    context: _aws_cdk_core_f4b25747.IResolveContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f4f7d7d8014bab5f0c27a543d9c04050866092f6c5e9172d4a638f41c319aa(
    *,
    assign_sids: typing.Optional[builtins.bool] = None,
    minimize: typing.Optional[builtins.bool] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8a546acac37b02e421f4948eb464fbbe9eac668ce499bcc146b926205251ca(
    *,
    document: typing.Optional[PolicyDocument] = None,
    force: typing.Optional[builtins.bool] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    policy_name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffcea937441550e9184ac00ae00ba3e3812c13f41565e8591ef60253c4f2542(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532f9bdafed4a223baf813860d6386e5626ec0022d7dd63f96c518d4fc6c521a(
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2938b71b67747eee407f9c817bf7d1a41197aa4bfa37eec68c9b3110516135(
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483f632408ecc823fa3364619179350afb31a3ea4cd21a3ef4b29c1c0ae1e73e(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da47be57b0ae9584c58020e316eeaad991fc445c802b144d29b78e76f9c19d47(
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690b4b4d99807d694786a792027f9fd41ea7017855647b353d7966e72a1b4332(
    canonical_user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd98c5a27dd5fde5f772f6487662333d0fd941a121ca07313aaee1437d3db5e2(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e920f9d0d1b0486f7e2c114fd7ce570cae5cd4c934512d76ef199347118a6a(
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e17c77733d830a7932a666a4315c4c32cced578919c0ea52ecfaabd69d84a2c(
    federated: typing.Any,
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed140998c0bcec41ca7a0ccb53441498e621c3c91be74b100641b46a63dde00(
    *not_actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c637ee98701df2ea8affe16cd5efc393dc1c1429b4a43de89ffbd3155d6c099c(
    *not_principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff17183088dfe1dcfb47a2dcdddc0129480f6f1cb678f299d0fb58f9cac024a(
    *arns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511578cfb7d00fb67864fdc75942e9e6b391f4177c1a8d8f7e32f07d37a877b8(
    *principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30f77d6f049aa7034b3e7e4e68a6c455a551ec07dea1404987c504b0e82af9c(
    *arns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9183104f297e8c384356c5525bdb50beb752042d8e5f137a136893a573a50904(
    service: builtins.str,
    *,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340628b0426921b2e665bee0834f6217f29fe7d2ba3b0204aacd588972951e2a(
    value: Effect,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5e46ae9483d42a2b2cc9d51a7c483f01c2975f1aee84d7d53cda8135d1f0aa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1215e5692cd37bffdb5cbb63a11f28f91f3d97de3c749304ae97b4edca60f785(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    effect: typing.Optional[Effect] = None,
    not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
    not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    sid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6e266a1a41bfc081c3549a3b433b33593a3357a68668058dc4a383ee85283b(
    principal_json: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2557f999f89ee6454e622453703ead23ed34fc87d644d852566458d89abe754d(
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739ee5b6d6fa73cd50b8a861cc98102f227f3e5532eada8621c0998547141e5c(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e36bdc25b503e6858c06fbe71e06fb8c47db9917d362747f4ffb100fdce961(
    xml: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beba1e161374af536b36e0e63753cb8a9b8860fdbc4a956e4f8eb0ae899b272c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    metadata_document: SamlMetadataDocument,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4847e26d898ac5e2c11dd5c2594fd44b4e7e7c30b23390dc4bc1ea4ba0ac0234(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    saml_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8a837d1e0d2af05a654af566e5dab166691061a32ea1ece7ce339f074a03b9(
    *,
    metadata_document: SamlMetadataDocument,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f790361a69d2878fd5cc0b57a28b0561662de83463f3fa1ce7edeabe8ddb84f5(
    *,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a13978d1b7af5dc1ecfaa5aa431b875e1efa6d2b8f64424d32a10a1bb1529a2(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71bffd0ad97751c05dddc0b182fa1cc44ef882ba8b8e118a71021c0dde7e06c(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2ff83013aa8d2751c9d23a8bf54b989cecfcc3128e830c3702657b9cc311d7(
    *,
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae70989695d7a0446847476b9b8039389e197a26b5591db4da99409b788a265(
    *,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bbdec7edf55e340fa7e131634dc50f0987688d4a15a2d6a018c8efd08343f2(
    *,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
    password_reset_required: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73638bc56584c021f9745d8cb4ebead059b67a3c5c4e2f1e08fff8af7854c120(
    *,
    add_grants_to_resources: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1196ea5a664392f4cfd3a1177cf82ad458813724c85cd2d45289c2f2824821(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    user: IUser,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[AccessKeyStatus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972a428e334ed7557d17a312b1a5ce5ab4170289638f751ee67dcb114d2d0cbf(
    document: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2642bda5e4ebb783baa8fd71c9f1225762beb2d586a47c5826c18db719ad57b(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31256906c2b77ab2b201f0ade60935c825f65bd1df7004c7d2f4bf6dfaffa7ce(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bbf007e438e8a325f2443245fe2bfbbd84c18086467993163047b69084597f(
    grantee: IPrincipal,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea08784bf3a8fca3be421be0c84aa317fc766521bff27cb315f5e0d53c9b069(
    grantee: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9780945a90890af7ddac80bb2bc0e3be8634b7e2e3eec5876ad0365516166e(
    grantee: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cec78607c2ad8f3a60f7e6ca0dd40627fc0fb139e6fc5859478e1eebbd958a(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8320125dcd239abc42a114eab6bfe14fb580a77496edd667a6e4da944de817b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e4bdb4c847eba36b4bf83015f6cf2a6300c3c75349321d51f355707d236885(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8656d2c87037829495462582804ee7e0936cd11a330744192b58f5a7ecab8a8(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a953333ba85b431f4c1993553c5e2a85803b713710beb7f8206289e0dc1feae2(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b754135137ad1ce46a7a3fc747726c15950dc4896358f19dbf155c176932e05(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a784b4445844efe61a8cbfcc5764b3e83aafebfc471c236d2fa64d9f446371ef(
    identity: IPrincipal,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328682402597832ac7d8b80f349a466132a8cf29ec8f5d4a25f738ac48898b8b(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd25e6fb7fa044bacc3b73c9291a9d35dc4433d60128cc851a22b0d4d4f04375(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ea9408bae156a8893fade732747f6c0b5b8711aeda7ff9c0a32a7b9b96e400(
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6509d0fe8a3195b520146085db72e93f1e5f02ba2243b923c655abc6cd3b097(
    document: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b81846823e1c416ed2f15b2066fa88880fa369f8901a1152563ba841db4ab71(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5d0bfdc9eb297bb2b4cc6bcdc9ba4a455873fd46445eef0349077535e994d7(
    _statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4647de623099170c468b7b7ce413d55eae89eee6b0430f23994c2382c4392e4c(
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d8ce15b8a96ebb7ad13cd2d9ae0ac51ce7b4665bb51e601fef6ffd75d2f8b6(
    principal: IPrincipal,
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318b378235d5bc15e4fe80d91f6feb5a24db531e0885f842c579023de4ad51b4(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6664357d004f0b7c02759cc786577cbafcfb15bca7f5cb2a00ad44e3b84b97(
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f665f540b23cee37ee4fbf5c2969dd8ce2f308824c4ba8befa586b832431596(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba50917207740ba8aedfc135d52dfd99e7719c5460f5a052b95812036f3d34b5(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02204e082a4920651e1aa8c2236c92067880094f3e49f7a1eb3bd72713fb044(
    append: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5310503b06cb08bf4e519ee12a836aed92f0157b0098b61f40394151e6c68d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc04d40f94cd6d0f99a4b58dbff2622ef59c97d6d0e89b44138c085a55baed5d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    role_arn: builtins.str,
    *,
    add_grants_to_resources: typing.Optional[builtins.bool] = None,
    mutable: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b0801e8767218a1f10a6b7f943066a2bfd13f8dd703870ffe8fb0fe070ad48(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    role_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1409c8d57af433c248a3cb14497f90b18f4961bee23fdd10841633f37365f13(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c8f4cd4d560f7674297c9d27079a906f9df6a5f59002d1505284e5c496dfcc(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1663903ef35b51c36e52a32d691c4315a662e7192dbf0725d3ecf8f3adbf20e(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9476a5a3896120f258e0dbf2171197d018922281c1a496c483e88f9c3a78e26(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c73fa12ae3016bd2f877477f5c46e739db8e8f59c24a717c4c5a3d1530e9ed2(
    grantee: IPrincipal,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ce147fd473fe9ab3d27e627921bd1ce9619cac7db8bcbd195be72797bc04d6(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06a0013905fac13736121e4670a1d2f35a3cc6f3c9e558503ef4f8488b3b40a(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1376a4c35e10feb7c23273982992d9c562526a4539d121c5e3d4984c3737e5(
    service: builtins.str,
    *,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761e37ce11275c00b8a2906ea6ce2266748a75cfc7812d4a06fae7133d17cf73(
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365c69e8ecce37f35d494d0bfbb5a829e8fe67517b51d7bee7dfb8d4fce9e796(
    principal: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3034a859e597fc2177ebeeca8441efa20b59d5d48e716133676bf9b86893e2(
    doc: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c77de2f3d061a35230b1294017f54f4e3c4497e6be22b32c505c88ab0c86ea(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872615722a89f3e56e0888f565b04c4ea7e211ae81b7acfcfe14a7cbbd4236dc(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1276bcf70faa8b5916bd4daf4ee04cd191a005c5a546748eee76aa18f2b3be17(
    append: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1cc66bf08bcddd3308411891a0f8625a835d950450ee83f69f66c94068383c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    password: typing.Optional[_aws_cdk_core_f4b25747.SecretValue] = None,
    password_reset_required: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28e97129edf7fe21756abb20a6b9b5874b9e53f4e40c5a770746d01b0a33541(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd81e2731e9d7dc60231f87606b00244609f91da50545761fdb45fcf0b2bc520(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b6fd2a7895a68ff3a54418adbb02f0ebd749df17f41da28d85319ea549c26e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    user_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117bd5146bf9ba7e7b245046f07c7a2a69a3d7cbcd4cb627ded955c13962b241(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad68249279606cb48fda691ebaa18dd3945afa15a131e08f63dad99484856ea(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9e829f6f9d4874baace56b79e3aa49d6aeecb70395de96910ef5671acef3ec(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e483cede26202629b9c596a6c9e40a80980f076337924fe4af4d736c08b75a7b(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2166432f7837b87207999329845580e5a907d3dc23c64c7d781c7e8b196999d9(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c88d55d60093b47e26b74a1f2704359eeddf189e30966955f6a47bbcb0e3dfb(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b07a6f49468f29c51c0efdb8a100cdcd964be7ce1a2458a1b18e5ee4f34832c(
    organization_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a11266efb4c826f02227dc9055445517d67e75f8ecaffe55232d66e30255a8(
    canonical_user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60652f5792946851af521599a262d1ce8987aa24b66de3eb5f772bddb18238d9(
    *principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72b9a571d348b3b16e06a6e73b9ccdf291162dc75c9630192317efc5852b3df(
    *principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45e66df71d2b0bb2499f9685e9bba94ca2f67ad21fb5b4b4a612a2eb5002140(
    doc: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319be364073e04fce09ad1ef6829af793d0f7193ba238809c0a3f4cbf1bd252d(
    federated: builtins.str,
    conditions: typing.Mapping[builtins.str, typing.Any],
    assume_role_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562487b4013dd2fd82be5ae3009fa1fc859a99b5d75a6d8651b6a8c7e4361db8(
    organization_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8481f3c1ca211152a5191d582999d8e7bb2fff5d0e149356327018a98743c01b(
    saml_provider: ISamlProvider,
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2caca9727510c3ea3cd74a70ea73a3e1adbbbb87080ed6373bfcdc14e19bef(
    identity_provider: builtins.str,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b1a3fd75474b5951cc226ed31323155cea4b73c2f8df408c5332dbb6e42f9a(
    account_id: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409cfeca6e6922e7ee3cdf263415a04a486073dd467345e230f31c297f0b79b3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af8f05aea5eb6362bcc8f7aeda9062007508bac177ae79d0ae1fb101bcfcd1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb5bb3baceeab48f20d3209703cb59da83880a94cc8ec150e6d5efdc541f4c5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9385cd1dd4945c15cc2a3995aed43175a8bec43dc44783cb1a4c8e05222ff90(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496ca44e870019b4c461eea4f219308f9801fb5b28a85ab4dfc098f0e32b7893(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3dc32e918311088c1b9a74f434356723433fffaeed088de8369221de62f1b9(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44228d06c84d7053e8f7c57a0798f1cc000aa0dc20b87550f88fbaccc1e45c2(
    user: IUser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b184157e50f3eee6c022b25e939b0489a4c08286f7d405747d1041931cb88006(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e33149b9cb725fe8da999822da7179a8de13ade53853aa2a3b246285d9b2bc(
    open_id_connect_provider: IOpenIdConnectProvider,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91c6812d31a6288a1beea15086a8d79996b41aaba3ec3728ab8b1047e057155(
    saml_provider: ISamlProvider,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass
