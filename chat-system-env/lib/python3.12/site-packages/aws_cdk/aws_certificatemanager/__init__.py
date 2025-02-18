'''
# AWS Certificate Manager Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

AWS Certificate Manager (ACM) handles the complexity of creating, storing, and renewing public and private SSL/TLS X.509 certificates and keys that
protect your AWS websites and applications. ACM certificates can secure singular domain names, multiple specific domain names, wildcard domains, or
combinations of these. ACM wildcard certificates can protect an unlimited number of subdomains.

This package provides Constructs for provisioning and referencing ACM certificates which can be used with CloudFront and ELB.

After requesting a certificate, you will need to prove that you own the
domain in question before the certificate will be granted. The CloudFormation
deployment will wait until this verification process has been completed.

Because of this wait time, when using manual validation methods, it's better
to provision your certificates either in a separate stack from your main
service, or provision them manually and import them into your CDK application.

**Note:** There is a limit on total number of ACM certificates that can be requested on an account and region within a year.
The default limit is 2000, but this limit may be (much) lower on new AWS accounts.
See https://docs.aws.amazon.com/acm/latest/userguide/acm-limits.html for more information.

## DNS validation

DNS validation is the preferred method to validate domain ownership, as it has a number of advantages over email validation.
See also [Validate with DNS](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html)
in the AWS Certificate Manager User Guide.

If Amazon Route 53 is your DNS provider for the requested domain, the DNS record can be
created automatically:

```python
my_hosted_zone = route53.HostedZone(self, "HostedZone",
    zone_name="example.com"
)
acm.Certificate(self, "Certificate",
    domain_name="hello.example.com",
    validation=acm.CertificateValidation.from_dns(my_hosted_zone)
)
```

If Route 53 is not your DNS provider, the DNS records must be added manually and the stack will not complete
creating until the records are added.

```python
acm.Certificate(self, "Certificate",
    domain_name="hello.example.com",
    validation=acm.CertificateValidation.from_dns()
)
```

When working with multiple domains, use the `CertificateValidation.fromDnsMultiZone()`:

```python
example_com = route53.HostedZone(self, "ExampleCom",
    zone_name="example.com"
)
example_net = route53.HostedZone(self, "ExampleNet",
    zone_name="example.net"
)

cert = acm.Certificate(self, "Certificate",
    domain_name="test.example.com",
    subject_alternative_names=["cool.example.com", "test.example.net"],
    validation=acm.CertificateValidation.from_dns_multi_zone({
        "test.example.com": example_com,
        "cool.example.com": example_com,
        "test.example.net": example_net
    })
)
```

## Email validation

Email-validated certificates (the default) are validated by receiving an
email on one of a number of predefined domains and following the instructions
in the email.

See [Validate with Email](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html)
in the AWS Certificate Manager User Guide.

```python
acm.Certificate(self, "Certificate",
    domain_name="hello.example.com",
    validation=acm.CertificateValidation.from_email()
)
```

## Cross-region Certificates

ACM certificates that are used with CloudFront -- or higher-level constructs which rely on CloudFront -- must be in the `us-east-1` region.
The `DnsValidatedCertificate` construct exists to facilitate creating these certificates cross-region. This resource can only be used with
Route53-based DNS validation.

```python
# my_hosted_zone: route53.HostedZone

acm.DnsValidatedCertificate(self, "CrossRegionCertificate",
    domain_name="hello.example.com",
    hosted_zone=my_hosted_zone,
    region="us-east-1"
)
```

## Requesting private certificates

AWS Certificate Manager can create [private certificates](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-private.html) issued by [Private Certificate Authority (PCA)](https://docs.aws.amazon.com/acm-pca/latest/userguide/PcaWelcome.html). Validation of private certificates is not necessary.

```python
import aws_cdk.aws_acmpca as acmpca


acm.PrivateCertificate(self, "PrivateCertificate",
    domain_name="test.example.com",
    subject_alternative_names=["cool.example.com", "test.example.net"],  # optional
    certificate_authority=acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CA", "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/023077d8-2bfa-4eb0-8f22-05c96deade77")
)
```

## Importing

If you want to import an existing certificate, you can do so from its ARN:

```python
arn = "arn:aws:..."
certificate = acm.Certificate.from_certificate_arn(self, "Certificate", arn)
```

## Sharing between Stacks

To share the certificate between stacks in the same CDK application, simply
pass the `Certificate` object between the stacks.

## Metrics

The `DaysToExpiry` metric is available via the `metricDaysToExpiry` method for
all certificates. This metric is emitted by AWS Certificates Manager once per
day until the certificate has effectively expired.

An alarm can be created to determine whether a certificate is soon due for
renewal ussing the following code:

```python
import aws_cdk.aws_cloudwatch as cloudwatch

# my_hosted_zone: route53.HostedZone

certificate = acm.Certificate(self, "Certificate",
    domain_name="hello.example.com",
    validation=acm.CertificateValidation.from_dns(my_hosted_zone)
)
certificate.metric_days_to_expiry().create_alarm(self, "Alarm",
    comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
    evaluation_periods=1,
    threshold=45
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

import aws_cdk.aws_acmpca as _aws_cdk_aws_acmpca_8c4081d6
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_9b88bb94
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_f47b29d4
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-certificatemanager.CertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "subject_alternative_names": "subjectAlternativeNames",
        "validation": "validation",
        "validation_domains": "validationDomains",
        "validation_method": "validationMethod",
    },
)
class CertificateProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        validation: typing.Optional["CertificateValidation"] = None,
        validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        validation_method: typing.Optional["ValidationMethod"] = None,
    ) -> None:
        '''Properties for your certificate.

        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation: How to validate this certificate. Default: CertificateValidation.fromEmail()
        :param validation_domains: (deprecated) What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: (deprecated) Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_cloudwatch as cloudwatch
            
            # my_hosted_zone: route53.HostedZone
            
            certificate = acm.Certificate(self, "Certificate",
                domain_name="hello.example.com",
                validation=acm.CertificateValidation.from_dns(my_hosted_zone)
            )
            certificate.metric_days_to_expiry().create_alarm(self, "Alarm",
                comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                evaluation_periods=1,
                threshold=45
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07eee4869bda1d699f13a82ed6a8346f04e2866672285937db18e94da5a9cecc)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            check_type(argname="argument validation_domains", value=validation_domains, expected_type=type_hints["validation_domains"])
            check_type(argname="argument validation_method", value=validation_method, expected_type=type_hints["validation_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names
        if validation is not None:
            self._values["validation"] = validation
        if validation_domains is not None:
            self._values["validation_domains"] = validation_domains
        if validation_method is not None:
            self._values["validation_method"] = validation_method

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Fully-qualified domain name to request a certificate for.

        May contain wildcards, such as ``*.domain.com``.
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Alternative domain names on your certificate.

        Use this to register alternative domain names that represent the same site.

        :default: - No additional FQDNs will be included as alternative domain names.
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def validation(self) -> typing.Optional["CertificateValidation"]:
        '''How to validate this certificate.

        :default: CertificateValidation.fromEmail()
        '''
        result = self._values.get("validation")
        return typing.cast(typing.Optional["CertificateValidation"], result)

    @builtins.property
    def validation_domains(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) What validation domain to use for every requested domain.

        Has to be a superdomain of the requested domain.

        :default: - Apex domain is used for every domain that's not overridden.

        :deprecated: use ``validation`` instead.

        :stability: deprecated
        '''
        result = self._values.get("validation_domains")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def validation_method(self) -> typing.Optional["ValidationMethod"]:
        '''(deprecated) Validation method used to assert domain ownership.

        :default: ValidationMethod.EMAIL

        :deprecated: use ``validation`` instead.

        :stability: deprecated
        '''
        result = self._values.get("validation_method")
        return typing.cast(typing.Optional["ValidationMethod"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CertificateValidation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-certificatemanager.CertificateValidation",
):
    '''How to validate a certificate.

    :exampleMetadata: infused

    Example::

        my_hosted_zone = route53.HostedZone(self, "HostedZone",
            zone_name="example.com"
        )
        acm.Certificate(self, "Certificate",
            domain_name="hello.example.com",
            validation=acm.CertificateValidation.from_dns(my_hosted_zone)
        )
    '''

    @jsii.member(jsii_name="fromDns")
    @builtins.classmethod
    def from_dns(
        cls,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    ) -> "CertificateValidation":
        '''Validate the certificate with DNS.

        IMPORTANT: If ``hostedZone`` is not specified, DNS records must be added
        manually and the stack will not complete creating until the records are
        added.

        :param hosted_zone: the hosted zone where DNS records must be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ad0adcce6346d80c4db02efbd6d7ee2567f252b88535866ee0f03bd198a757)
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
        return typing.cast("CertificateValidation", jsii.sinvoke(cls, "fromDns", [hosted_zone]))

    @jsii.member(jsii_name="fromDnsMultiZone")
    @builtins.classmethod
    def from_dns_multi_zone(
        cls,
        hosted_zones: typing.Mapping[builtins.str, _aws_cdk_aws_route53_f47b29d4.IHostedZone],
    ) -> "CertificateValidation":
        '''Validate the certificate with automatically created DNS records in multiple Amazon Route 53 hosted zones.

        :param hosted_zones: a map of hosted zones where DNS records must be created for the domains in the certificate.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe61f6707b3a5d302a4da32266d0270ce7358e78304a4d55b40f4a674ab37ac)
            check_type(argname="argument hosted_zones", value=hosted_zones, expected_type=type_hints["hosted_zones"])
        return typing.cast("CertificateValidation", jsii.sinvoke(cls, "fromDnsMultiZone", [hosted_zones]))

    @jsii.member(jsii_name="fromEmail")
    @builtins.classmethod
    def from_email(
        cls,
        validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> "CertificateValidation":
        '''Validate the certificate with Email.

        IMPORTANT: if you are creating a certificate as part of your stack, the stack
        will not complete creating until you read and follow the instructions in the
        email that you will receive.

        ACM will send validation emails to the following addresses:

        admin@domain.com
        administrator@domain.com
        hostmaster@domain.com
        postmaster@domain.com
        webmaster@domain.com

        For every domain that you register.

        :param validation_domains: a map of validation domains to use for domains in the certificate.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ef87519e08c2056242ca072568b3824000e520462c6261b7ea05320c3b0213)
            check_type(argname="argument validation_domains", value=validation_domains, expected_type=type_hints["validation_domains"])
        return typing.cast("CertificateValidation", jsii.sinvoke(cls, "fromEmail", [validation_domains]))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> "ValidationMethod":
        '''The validation method.'''
        return typing.cast("ValidationMethod", jsii.get(self, "method"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CertificationValidationProps":
        '''Certification validation properties.'''
        return typing.cast("CertificationValidationProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-certificatemanager.CertificationValidationProps",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone": "hostedZone",
        "hosted_zones": "hostedZones",
        "method": "method",
        "validation_domains": "validationDomains",
    },
)
class CertificationValidationProps:
    def __init__(
        self,
        *,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        hosted_zones: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_route53_f47b29d4.IHostedZone]] = None,
        method: typing.Optional["ValidationMethod"] = None,
        validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for certificate validation.

        :param hosted_zone: Hosted zone to use for DNS validation. Default: - use email validation
        :param hosted_zones: A map of hosted zones to use for DNS validation. Default: - use ``hostedZone``
        :param method: Validation method. Default: ValidationMethod.EMAIL
        :param validation_domains: Validation domains to use for email validation. Default: - Apex domain

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_certificatemanager as certificatemanager
            import aws_cdk.aws_route53 as route53
            
            # hosted_zone: route53.HostedZone
            
            certification_validation_props = certificatemanager.CertificationValidationProps(
                hosted_zone=hosted_zone,
                hosted_zones={
                    "hosted_zones_key": hosted_zone
                },
                method=certificatemanager.ValidationMethod.EMAIL,
                validation_domains={
                    "validation_domains_key": "validationDomains"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48da59f7382d88ab2d6c8522c904091ae5e2d8642c60024a45ec5e5ea3c05fd)
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument hosted_zones", value=hosted_zones, expected_type=type_hints["hosted_zones"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument validation_domains", value=validation_domains, expected_type=type_hints["validation_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone
        if hosted_zones is not None:
            self._values["hosted_zones"] = hosted_zones
        if method is not None:
            self._values["method"] = method
        if validation_domains is not None:
            self._values["validation_domains"] = validation_domains

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''Hosted zone to use for DNS validation.

        :default: - use email validation
        '''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def hosted_zones(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_route53_f47b29d4.IHostedZone]]:
        '''A map of hosted zones to use for DNS validation.

        :default: - use ``hostedZone``
        '''
        result = self._values.get("hosted_zones")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_route53_f47b29d4.IHostedZone]], result)

    @builtins.property
    def method(self) -> typing.Optional["ValidationMethod"]:
        '''Validation method.

        :default: ValidationMethod.EMAIL
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["ValidationMethod"], result)

    @builtins.property
    def validation_domains(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Validation domains to use for email validation.

        :default: - Apex domain
        '''
        result = self._values.get("validation_domains")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CertificationValidationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAccount(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-certificatemanager.CfnAccount",
):
    '''A CloudFormation ``AWS::CertificateManager::Account``.

    The ``AWS::CertificateManager::Account`` resource defines the expiry event configuration that determines the number of days prior to expiry when ACM starts generating EventBridge events.

    :cloudformationResource: AWS::CertificateManager::Account
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-account.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_certificatemanager as certificatemanager
        
        cfn_account = certificatemanager.CfnAccount(self, "MyCfnAccount",
            expiry_events_configuration=certificatemanager.CfnAccount.ExpiryEventsConfigurationProperty(
                days_before_expiry=123
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        expiry_events_configuration: typing.Union[typing.Union["CfnAccount.ExpiryEventsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        '''Create a new ``AWS::CertificateManager::Account``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param expiry_events_configuration: Object containing expiration events options associated with an AWS account . For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23e45ca4cc31b8d44283875567a80800091912eece0c5763fcb8f7410ce9862)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccountProps(
            expiry_events_configuration=expiry_events_configuration
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b7668affbd2288301d2655ee8726c1cd7d1c44bae9a3627463989ac2ff2713)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e1c2f310de06940b379bd28a78aa91d84b8f955c99190c6b53d790c84baa4b5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountId")
    def attr_account_id(self) -> builtins.str:
        '''ID of the AWS account that owns the certificate.

        :cloudformationAttribute: AccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccountId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="expiryEventsConfiguration")
    def expiry_events_configuration(
        self,
    ) -> typing.Union["CfnAccount.ExpiryEventsConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Object containing expiration events options associated with an AWS account .

        For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-account.html#cfn-certificatemanager-account-expiryeventsconfiguration
        '''
        return typing.cast(typing.Union["CfnAccount.ExpiryEventsConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "expiryEventsConfiguration"))

    @expiry_events_configuration.setter
    def expiry_events_configuration(
        self,
        value: typing.Union["CfnAccount.ExpiryEventsConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2d2575448d25618f4706d315bf4d81460bd89a55082113e78773591787afb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryEventsConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-certificatemanager.CfnAccount.ExpiryEventsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"days_before_expiry": "daysBeforeExpiry"},
    )
    class ExpiryEventsConfigurationProperty:
        def __init__(
            self,
            *,
            days_before_expiry: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Object containing expiration events options associated with an AWS account .

            For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.

            :param days_before_expiry: This option specifies the number of days prior to certificate expiration when ACM starts generating ``EventBridge`` events. ACM sends one event per day per certificate until the certificate expires. By default, accounts receive events starting 45 days before certificate expiration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-account-expiryeventsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_certificatemanager as certificatemanager
                
                expiry_events_configuration_property = certificatemanager.CfnAccount.ExpiryEventsConfigurationProperty(
                    days_before_expiry=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ad74fe50da176264b01b1312e4a29aa0d0dfcde3892b3ca3623b47ad8c26d9b)
                check_type(argname="argument days_before_expiry", value=days_before_expiry, expected_type=type_hints["days_before_expiry"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days_before_expiry is not None:
                self._values["days_before_expiry"] = days_before_expiry

        @builtins.property
        def days_before_expiry(self) -> typing.Optional[jsii.Number]:
            '''This option specifies the number of days prior to certificate expiration when ACM starts generating ``EventBridge`` events.

            ACM sends one event per day per certificate until the certificate expires. By default, accounts receive events starting 45 days before certificate expiration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-account-expiryeventsconfiguration.html#cfn-certificatemanager-account-expiryeventsconfiguration-daysbeforeexpiry
            '''
            result = self._values.get("days_before_expiry")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpiryEventsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-certificatemanager.CfnAccountProps",
    jsii_struct_bases=[],
    name_mapping={"expiry_events_configuration": "expiryEventsConfiguration"},
)
class CfnAccountProps:
    def __init__(
        self,
        *,
        expiry_events_configuration: typing.Union[typing.Union[CfnAccount.ExpiryEventsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        '''Properties for defining a ``CfnAccount``.

        :param expiry_events_configuration: Object containing expiration events options associated with an AWS account . For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-account.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_certificatemanager as certificatemanager
            
            cfn_account_props = certificatemanager.CfnAccountProps(
                expiry_events_configuration=certificatemanager.CfnAccount.ExpiryEventsConfigurationProperty(
                    days_before_expiry=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19bee2772c049853523980ea3e9548f0e823787ee6d951fb15079f9f8828a86)
            check_type(argname="argument expiry_events_configuration", value=expiry_events_configuration, expected_type=type_hints["expiry_events_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expiry_events_configuration": expiry_events_configuration,
        }

    @builtins.property
    def expiry_events_configuration(
        self,
    ) -> typing.Union[CfnAccount.ExpiryEventsConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Object containing expiration events options associated with an AWS account .

        For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-account.html#cfn-certificatemanager-account-expiryeventsconfiguration
        '''
        result = self._values.get("expiry_events_configuration")
        assert result is not None, "Required property 'expiry_events_configuration' is missing"
        return typing.cast(typing.Union[CfnAccount.ExpiryEventsConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCertificate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificate",
):
    '''A CloudFormation ``AWS::CertificateManager::Certificate``.

    The ``AWS::CertificateManager::Certificate`` resource requests an AWS Certificate Manager ( ACM ) certificate that you can use to enable secure connections. For example, you can deploy an ACM certificate to an Elastic Load Balancer to enable HTTPS support. For more information, see `RequestCertificate <https://docs.aws.amazon.com/acm/latest/APIReference/API_RequestCertificate.html>`_ in the AWS Certificate Manager API Reference.
    .. epigraph::

       When you use the ``AWS::CertificateManager::Certificate`` resource in a CloudFormation stack, domain validation is handled automatically if all three of the following are true: The certificate domain is hosted in Amazon Route 53, the domain resides in your AWS account , and you are using DNS validation.

       However, if the certificate uses email validation, or if the domain is not hosted in Route 53, then the stack will remain in the ``CREATE_IN_PROGRESS`` state. Further stack operations are delayed until you validate the certificate request, either by acting upon the instructions in the validation email, or by adding a CNAME record to your DNS configuration. For more information, see `Option 1: DNS Validation <https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html>`_ and `Option 2: Email Validation <https://docs.aws.amazon.com/acm/latest/userguide/email-validation.html>`_ .

    :cloudformationResource: AWS::CertificateManager::Certificate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_certificatemanager as certificatemanager
        
        cfn_certificate = certificatemanager.CfnCertificate(self, "MyCfnCertificate",
            domain_name="domainName",
        
            # the properties below are optional
            certificate_authority_arn="certificateAuthorityArn",
            certificate_transparency_logging_preference="certificateTransparencyLoggingPreference",
            domain_validation_options=[certificatemanager.CfnCertificate.DomainValidationOptionProperty(
                domain_name="domainName",
        
                # the properties below are optional
                hosted_zone_id="hostedZoneId",
                validation_domain="validationDomain"
            )],
            subject_alternative_names=["subjectAlternativeNames"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            validation_method="validationMethod"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        certificate_transparency_logging_preference: typing.Optional[builtins.str] = None,
        domain_validation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.DomainValidationOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        validation_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CertificateManager::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: The fully qualified domain name (FQDN), such as www.example.com, with which you want to secure an ACM certificate. Use an asterisk (*) to create a wildcard certificate that protects several sites in the same domain. For example, ``*.example.com`` protects ``www.example.com`` , ``site.example.com`` , and ``images.example.com.``.
        :param certificate_authority_arn: The Amazon Resource Name (ARN) of the private certificate authority (CA) that will be used to issue the certificate. If you do not provide an ARN and you are trying to request a private certificate, ACM will attempt to issue a public certificate. For more information about private CAs, see the `AWS Private Certificate Authority <https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html>`_ user guide. The ARN must have the following form: ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``
        :param certificate_transparency_logging_preference: You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt in by specifying ``ENABLED`` . If you do not specify a certificate transparency logging preference on a new CloudFormation template, or if you remove the logging preference from an existing template, this is the same as explicitly enabling the preference. Changing the certificate transparency logging preference will update the existing resource by calling ``UpdateCertificateOptions`` on the certificate. This action will not create a new resource.
        :param domain_validation_options: Domain information that domain name registrars use to verify your identity. .. epigraph:: In order for a AWS::CertificateManager::Certificate to be provisioned and validated in CloudFormation automatically, the ``DomainName`` property needs to be identical to one of the ``DomainName`` property supplied in DomainValidationOptions, if the ValidationMethod is **DNS**. Failing to keep them like-for-like will result in failure to create the domain validation records in Route53.
        :param subject_alternative_names: Additional FQDNs to be included in the Subject Alternative Name extension of the ACM certificate. For example, you can add www.example.net to a certificate for which the ``DomainName`` field is www.example.com if users can reach your site by using either name.
        :param tags: Key-value pairs that can identify the certificate.
        :param validation_method: The method you want to use to validate that you own or control the domain associated with a public certificate. You can `validate with DNS <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`_ or `validate with email <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html>`_ . We recommend that you use DNS validation. If not specified, this property defaults to email validation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78acff60e7f2cd388833af17cd9bff3fb31dd6b31070cb3b4672358d477a3f99)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCertificateProps(
            domain_name=domain_name,
            certificate_authority_arn=certificate_authority_arn,
            certificate_transparency_logging_preference=certificate_transparency_logging_preference,
            domain_validation_options=domain_validation_options,
            subject_alternative_names=subject_alternative_names,
            tags=tags,
            validation_method=validation_method,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd872b3b23cd9ba82705fd300a078271e7c78253fe4531c45e766ac8d7167af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1c0026ee5e1d0c7719f9926217bc56106448b5def35f393c45d8349811c763c)
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Key-value pairs that can identify the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The fully qualified domain name (FQDN), such as www.example.com, with which you want to secure an ACM certificate. Use an asterisk (*) to create a wildcard certificate that protects several sites in the same domain. For example, ``*.example.com`` protects ``www.example.com`` , ``site.example.com`` , and ``images.example.com.``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9a3305c8a79e438bb46a2d9ee6b8e4135da7e689ecb7ab5fb4e644da129c4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the private certificate authority (CA) that will be used to issue the certificate.

        If you do not provide an ARN and you are trying to request a private certificate, ACM will attempt to issue a public certificate. For more information about private CAs, see the `AWS Private Certificate Authority <https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html>`_ user guide. The ARN must have the following form:

        ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificateauthorityarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateAuthorityArn"))

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394b786c0395a3e062ad8a5c3f8ddf2d7ef5a10bae6d8fb48908b35497f8411a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property
    @jsii.member(jsii_name="certificateTransparencyLoggingPreference")
    def certificate_transparency_logging_preference(
        self,
    ) -> typing.Optional[builtins.str]:
        '''You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt in by specifying ``ENABLED`` .

        If you do not specify a certificate transparency logging preference on a new CloudFormation template, or if you remove the logging preference from an existing template, this is the same as explicitly enabling the preference.

        Changing the certificate transparency logging preference will update the existing resource by calling ``UpdateCertificateOptions`` on the certificate. This action will not create a new resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificatetransparencyloggingpreference
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateTransparencyLoggingPreference"))

    @certificate_transparency_logging_preference.setter
    def certificate_transparency_logging_preference(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd745f54b51b7cec826cd7318a41c8aec435641c13256f454b12914a8a825c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateTransparencyLoggingPreference", value)

    @builtins.property
    @jsii.member(jsii_name="domainValidationOptions")
    def domain_validation_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.DomainValidationOptionProperty"]]]]:
        '''Domain information that domain name registrars use to verify your identity.

        .. epigraph::

           In order for a AWS::CertificateManager::Certificate to be provisioned and validated in CloudFormation automatically, the ``DomainName`` property needs to be identical to one of the ``DomainName`` property supplied in DomainValidationOptions, if the ValidationMethod is **DNS**. Failing to keep them like-for-like will result in failure to create the domain validation records in Route53.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.DomainValidationOptionProperty"]]]], jsii.get(self, "domainValidationOptions"))

    @domain_validation_options.setter
    def domain_validation_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.DomainValidationOptionProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844b446d1ef35fc8a6cf0720190630fed02af574470208431340add9c25b9614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainValidationOptions", value)

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional FQDNs to be included in the Subject Alternative Name extension of the ACM certificate.

        For example, you can add www.example.net to a certificate for which the ``DomainName`` field is www.example.com if users can reach your site by using either name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-subjectalternativenames
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subjectAlternativeNames"))

    @subject_alternative_names.setter
    def subject_alternative_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431c29079b1cba692a45c2522bd8166c5cbe42abec31c1a9b590ff1304a62af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAlternativeNames", value)

    @builtins.property
    @jsii.member(jsii_name="validationMethod")
    def validation_method(self) -> typing.Optional[builtins.str]:
        '''The method you want to use to validate that you own or control the domain associated with a public certificate.

        You can `validate with DNS <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`_ or `validate with email <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html>`_ . We recommend that you use DNS validation.

        If not specified, this property defaults to email validation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-validationmethod
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validationMethod"))

    @validation_method.setter
    def validation_method(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08908a2bb9aa075dc18f555ac8842a12512e6e85f2bfd52e9a7bc5fdaa67d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationMethod", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificate.DomainValidationOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "hosted_zone_id": "hostedZoneId",
            "validation_domain": "validationDomain",
        },
    )
    class DomainValidationOptionProperty:
        def __init__(
            self,
            *,
            domain_name: builtins.str,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            validation_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``DomainValidationOption`` is a property of the `AWS::CertificateManager::Certificate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html>`_ resource that specifies the AWS Certificate Manager ( ACM ) certificate domain to validate. Depending on the chosen validation method, ACM checks the domain's DNS record for a validation CNAME, or it attempts to send a validation email message to the domain owner.

            :param domain_name: A fully qualified domain name (FQDN) in the certificate request.
            :param hosted_zone_id: The ``HostedZoneId`` option, which is available if you are using Route 53 as your domain registrar, causes ACM to add your CNAME to the domain record. Your list of ``DomainValidationOptions`` must contain one and only one of the domain-validation options, and the ``HostedZoneId`` can be used only when ``DNS`` is specified as your validation method. Use the Route 53 ``ListHostedZones`` API to discover IDs for available hosted zones. This option is required for publicly trusted certificates. .. epigraph:: The ``ListHostedZones`` API returns IDs in the format "/hostedzone/Z111111QQQQQQQ", but CloudFormation requires the IDs to be in the format "Z111111QQQQQQQ". When you change your ``DomainValidationOptions`` , a new resource is created.
            :param validation_domain: The domain name to which you want ACM to send validation emails. This domain name is the suffix of the email addresses that you want ACM to use. This must be the same as the ``DomainName`` value or a superdomain of the ``DomainName`` value. For example, if you request a certificate for ``testing.example.com`` , you can specify ``example.com`` as this value. In that case, ACM sends domain validation emails to the following five addresses: - admin@example.com - administrator@example.com - hostmaster@example.com - postmaster@example.com - webmaster@example.com

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_certificatemanager as certificatemanager
                
                domain_validation_option_property = certificatemanager.CfnCertificate.DomainValidationOptionProperty(
                    domain_name="domainName",
                
                    # the properties below are optional
                    hosted_zone_id="hostedZoneId",
                    validation_domain="validationDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__477b08cfc0e04f8a880e4dda182ecde2cea00f41b84a9573d05a21bd993a3c37)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument validation_domain", value=validation_domain, expected_type=type_hints["validation_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "domain_name": domain_name,
            }
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if validation_domain is not None:
                self._values["validation_domain"] = validation_domain

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''A fully qualified domain name (FQDN) in the certificate request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoptions-domainname
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The ``HostedZoneId`` option, which is available if you are using Route 53 as your domain registrar, causes ACM to add your CNAME to the domain record.

            Your list of ``DomainValidationOptions`` must contain one and only one of the domain-validation options, and the ``HostedZoneId`` can be used only when ``DNS`` is specified as your validation method.

            Use the Route 53 ``ListHostedZones`` API to discover IDs for available hosted zones.

            This option is required for publicly trusted certificates.
            .. epigraph::

               The ``ListHostedZones`` API returns IDs in the format "/hostedzone/Z111111QQQQQQQ", but CloudFormation requires the IDs to be in the format "Z111111QQQQQQQ".

            When you change your ``DomainValidationOptions`` , a new resource is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def validation_domain(self) -> typing.Optional[builtins.str]:
            '''The domain name to which you want ACM to send validation emails.

            This domain name is the suffix of the email addresses that you want ACM to use. This must be the same as the ``DomainName`` value or a superdomain of the ``DomainName`` value. For example, if you request a certificate for ``testing.example.com`` , you can specify ``example.com`` as this value. In that case, ACM sends domain validation emails to the following five addresses:

            - admin@example.com
            - administrator@example.com
            - hostmaster@example.com
            - postmaster@example.com
            - webmaster@example.com

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-validationdomain
            '''
            result = self._values.get("validation_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainValidationOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-certificatemanager.CfnCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_transparency_logging_preference": "certificateTransparencyLoggingPreference",
        "domain_validation_options": "domainValidationOptions",
        "subject_alternative_names": "subjectAlternativeNames",
        "tags": "tags",
        "validation_method": "validationMethod",
    },
)
class CfnCertificateProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        certificate_transparency_logging_preference: typing.Optional[builtins.str] = None,
        domain_validation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.DomainValidationOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        validation_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCertificate``.

        :param domain_name: The fully qualified domain name (FQDN), such as www.example.com, with which you want to secure an ACM certificate. Use an asterisk (*) to create a wildcard certificate that protects several sites in the same domain. For example, ``*.example.com`` protects ``www.example.com`` , ``site.example.com`` , and ``images.example.com.``.
        :param certificate_authority_arn: The Amazon Resource Name (ARN) of the private certificate authority (CA) that will be used to issue the certificate. If you do not provide an ARN and you are trying to request a private certificate, ACM will attempt to issue a public certificate. For more information about private CAs, see the `AWS Private Certificate Authority <https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html>`_ user guide. The ARN must have the following form: ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``
        :param certificate_transparency_logging_preference: You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt in by specifying ``ENABLED`` . If you do not specify a certificate transparency logging preference on a new CloudFormation template, or if you remove the logging preference from an existing template, this is the same as explicitly enabling the preference. Changing the certificate transparency logging preference will update the existing resource by calling ``UpdateCertificateOptions`` on the certificate. This action will not create a new resource.
        :param domain_validation_options: Domain information that domain name registrars use to verify your identity. .. epigraph:: In order for a AWS::CertificateManager::Certificate to be provisioned and validated in CloudFormation automatically, the ``DomainName`` property needs to be identical to one of the ``DomainName`` property supplied in DomainValidationOptions, if the ValidationMethod is **DNS**. Failing to keep them like-for-like will result in failure to create the domain validation records in Route53.
        :param subject_alternative_names: Additional FQDNs to be included in the Subject Alternative Name extension of the ACM certificate. For example, you can add www.example.net to a certificate for which the ``DomainName`` field is www.example.com if users can reach your site by using either name.
        :param tags: Key-value pairs that can identify the certificate.
        :param validation_method: The method you want to use to validate that you own or control the domain associated with a public certificate. You can `validate with DNS <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`_ or `validate with email <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html>`_ . We recommend that you use DNS validation. If not specified, this property defaults to email validation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_certificatemanager as certificatemanager
            
            cfn_certificate_props = certificatemanager.CfnCertificateProps(
                domain_name="domainName",
            
                # the properties below are optional
                certificate_authority_arn="certificateAuthorityArn",
                certificate_transparency_logging_preference="certificateTransparencyLoggingPreference",
                domain_validation_options=[certificatemanager.CfnCertificate.DomainValidationOptionProperty(
                    domain_name="domainName",
            
                    # the properties below are optional
                    hosted_zone_id="hostedZoneId",
                    validation_domain="validationDomain"
                )],
                subject_alternative_names=["subjectAlternativeNames"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                validation_method="validationMethod"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf091bbc992e3d46f9d9f7ff5de0fca3a55258e4528c55aec687bc2c2ebff57)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument certificate_transparency_logging_preference", value=certificate_transparency_logging_preference, expected_type=type_hints["certificate_transparency_logging_preference"])
            check_type(argname="argument domain_validation_options", value=domain_validation_options, expected_type=type_hints["domain_validation_options"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument validation_method", value=validation_method, expected_type=type_hints["validation_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if certificate_transparency_logging_preference is not None:
            self._values["certificate_transparency_logging_preference"] = certificate_transparency_logging_preference
        if domain_validation_options is not None:
            self._values["domain_validation_options"] = domain_validation_options
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names
        if tags is not None:
            self._values["tags"] = tags
        if validation_method is not None:
            self._values["validation_method"] = validation_method

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The fully qualified domain name (FQDN), such as www.example.com, with which you want to secure an ACM certificate. Use an asterisk (*) to create a wildcard certificate that protects several sites in the same domain. For example, ``*.example.com`` protects ``www.example.com`` , ``site.example.com`` , and ``images.example.com.``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the private certificate authority (CA) that will be used to issue the certificate.

        If you do not provide an ARN and you are trying to request a private certificate, ACM will attempt to issue a public certificate. For more information about private CAs, see the `AWS Private Certificate Authority <https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html>`_ user guide. The ARN must have the following form:

        ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_transparency_logging_preference(
        self,
    ) -> typing.Optional[builtins.str]:
        '''You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt in by specifying ``ENABLED`` .

        If you do not specify a certificate transparency logging preference on a new CloudFormation template, or if you remove the logging preference from an existing template, this is the same as explicitly enabling the preference.

        Changing the certificate transparency logging preference will update the existing resource by calling ``UpdateCertificateOptions`` on the certificate. This action will not create a new resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificatetransparencyloggingpreference
        '''
        result = self._values.get("certificate_transparency_logging_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_validation_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificate.DomainValidationOptionProperty]]]]:
        '''Domain information that domain name registrars use to verify your identity.

        .. epigraph::

           In order for a AWS::CertificateManager::Certificate to be provisioned and validated in CloudFormation automatically, the ``DomainName`` property needs to be identical to one of the ``DomainName`` property supplied in DomainValidationOptions, if the ValidationMethod is **DNS**. Failing to keep them like-for-like will result in failure to create the domain validation records in Route53.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions
        '''
        result = self._values.get("domain_validation_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificate.DomainValidationOptionProperty]]]], result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional FQDNs to be included in the Subject Alternative Name extension of the ACM certificate.

        For example, you can add www.example.net to a certificate for which the ``DomainName`` field is www.example.com if users can reach your site by using either name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-subjectalternativenames
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Key-value pairs that can identify the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def validation_method(self) -> typing.Optional[builtins.str]:
        '''The method you want to use to validate that you own or control the domain associated with a public certificate.

        You can `validate with DNS <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`_ or `validate with email <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html>`_ . We recommend that you use DNS validation.

        If not specified, this property defaults to email validation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-validationmethod
        '''
        result = self._values.get("validation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-certificatemanager.DnsValidatedCertificateProps",
    jsii_struct_bases=[CertificateProps],
    name_mapping={
        "domain_name": "domainName",
        "subject_alternative_names": "subjectAlternativeNames",
        "validation": "validation",
        "validation_domains": "validationDomains",
        "validation_method": "validationMethod",
        "hosted_zone": "hostedZone",
        "cleanup_route53_records": "cleanupRoute53Records",
        "custom_resource_role": "customResourceRole",
        "region": "region",
        "route53_endpoint": "route53Endpoint",
    },
)
class DnsValidatedCertificateProps(CertificateProps):
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        validation: typing.Optional[CertificateValidation] = None,
        validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        validation_method: typing.Optional["ValidationMethod"] = None,
        hosted_zone: _aws_cdk_aws_route53_f47b29d4.IHostedZone,
        cleanup_route53_records: typing.Optional[builtins.bool] = None,
        custom_resource_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        region: typing.Optional[builtins.str] = None,
        route53_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties to create a DNS validated certificate managed by AWS Certificate Manager.

        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation: How to validate this certificate. Default: CertificateValidation.fromEmail()
        :param validation_domains: (deprecated) What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: (deprecated) Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL
        :param hosted_zone: Route 53 Hosted Zone used to perform DNS validation of the request. The zone must be authoritative for the domain name specified in the Certificate Request.
        :param cleanup_route53_records: When set to true, when the DnsValidatedCertificate is deleted, the associated Route53 validation records are removed. CAUTION: If multiple certificates share the same domains (and same validation records), this can cause the other certificates to fail renewal and/or not validate. Not recommended for production use. Default: false
        :param custom_resource_role: Role to use for the custom resource that creates the validated certificate. Default: - A new role will be created
        :param region: AWS region that will host the certificate. This is needed especially for certificates used for CloudFront distributions, which require the region to be us-east-1. Default: the region the stack is deployed in.
        :param route53_endpoint: An endpoint of Route53 service, which is not necessary as AWS SDK could figure out the right endpoints for most regions, but for some regions such as those in aws-cn partition, the default endpoint is not working now, hence the right endpoint need to be specified through this prop. Route53 is not been officially launched in China, it is only available for AWS internal accounts now. To make DnsValidatedCertificate work for internal accounts now, a special endpoint needs to be provided. Default: - The AWS SDK will determine the Route53 endpoint to use based on region

        :exampleMetadata: infused

        Example::

            # my_hosted_zone: route53.HostedZone
            
            acm.DnsValidatedCertificate(self, "CrossRegionCertificate",
                domain_name="hello.example.com",
                hosted_zone=my_hosted_zone,
                region="us-east-1"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e177870cc744dc4ccbb34eb3b47cc5c50139c0f835b208143484f4c4e28492f)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            check_type(argname="argument validation_domains", value=validation_domains, expected_type=type_hints["validation_domains"])
            check_type(argname="argument validation_method", value=validation_method, expected_type=type_hints["validation_method"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument cleanup_route53_records", value=cleanup_route53_records, expected_type=type_hints["cleanup_route53_records"])
            check_type(argname="argument custom_resource_role", value=custom_resource_role, expected_type=type_hints["custom_resource_role"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument route53_endpoint", value=route53_endpoint, expected_type=type_hints["route53_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "hosted_zone": hosted_zone,
        }
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names
        if validation is not None:
            self._values["validation"] = validation
        if validation_domains is not None:
            self._values["validation_domains"] = validation_domains
        if validation_method is not None:
            self._values["validation_method"] = validation_method
        if cleanup_route53_records is not None:
            self._values["cleanup_route53_records"] = cleanup_route53_records
        if custom_resource_role is not None:
            self._values["custom_resource_role"] = custom_resource_role
        if region is not None:
            self._values["region"] = region
        if route53_endpoint is not None:
            self._values["route53_endpoint"] = route53_endpoint

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Fully-qualified domain name to request a certificate for.

        May contain wildcards, such as ``*.domain.com``.
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Alternative domain names on your certificate.

        Use this to register alternative domain names that represent the same site.

        :default: - No additional FQDNs will be included as alternative domain names.
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def validation(self) -> typing.Optional[CertificateValidation]:
        '''How to validate this certificate.

        :default: CertificateValidation.fromEmail()
        '''
        result = self._values.get("validation")
        return typing.cast(typing.Optional[CertificateValidation], result)

    @builtins.property
    def validation_domains(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(deprecated) What validation domain to use for every requested domain.

        Has to be a superdomain of the requested domain.

        :default: - Apex domain is used for every domain that's not overridden.

        :deprecated: use ``validation`` instead.

        :stability: deprecated
        '''
        result = self._values.get("validation_domains")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def validation_method(self) -> typing.Optional["ValidationMethod"]:
        '''(deprecated) Validation method used to assert domain ownership.

        :default: ValidationMethod.EMAIL

        :deprecated: use ``validation`` instead.

        :stability: deprecated
        '''
        result = self._values.get("validation_method")
        return typing.cast(typing.Optional["ValidationMethod"], result)

    @builtins.property
    def hosted_zone(self) -> _aws_cdk_aws_route53_f47b29d4.IHostedZone:
        '''Route 53 Hosted Zone used to perform DNS validation of the request.

        The zone
        must be authoritative for the domain name specified in the Certificate Request.
        '''
        result = self._values.get("hosted_zone")
        assert result is not None, "Required property 'hosted_zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_f47b29d4.IHostedZone, result)

    @builtins.property
    def cleanup_route53_records(self) -> typing.Optional[builtins.bool]:
        '''When set to true, when the DnsValidatedCertificate is deleted, the associated Route53 validation records are removed.

        CAUTION: If multiple certificates share the same domains (and same validation records),
        this can cause the other certificates to fail renewal and/or not validate.
        Not recommended for production use.

        :default: false
        '''
        result = self._values.get("cleanup_route53_records")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_resource_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''Role to use for the custom resource that creates the validated certificate.

        :default: - A new role will be created
        '''
        result = self._values.get("custom_resource_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''AWS region that will host the certificate.

        This is needed especially
        for certificates used for CloudFront distributions, which require the region
        to be us-east-1.

        :default: the region the stack is deployed in.
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route53_endpoint(self) -> typing.Optional[builtins.str]:
        '''An endpoint of Route53 service, which is not necessary as AWS SDK could figure out the right endpoints for most regions, but for some regions such as those in aws-cn partition, the default endpoint is not working now, hence the right endpoint need to be specified through this prop.

        Route53 is not been officially launched in China, it is only available for AWS
        internal accounts now. To make DnsValidatedCertificate work for internal accounts
        now, a special endpoint needs to be provided.

        :default: - The AWS SDK will determine the Route53 endpoint to use based on region
        '''
        result = self._values.get("route53_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsValidatedCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-certificatemanager.ICertificate")
class ICertificate(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''Represents a certificate in AWS Certificate Manager.'''

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''The certificate's ARN.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="metricDaysToExpiry")
    def metric_days_to_expiry(
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
        '''Return the DaysToExpiry metric for this AWS Certificate Manager Certificate. By default, this is the minimum value over 1 day.

        This metric is no longer emitted once the certificate has effectively
        expired, so alarms configured on this metric should probably treat missing
        data as "breaching".

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...


class _ICertificateProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Represents a certificate in AWS Certificate Manager.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-certificatemanager.ICertificate"

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''The certificate's ARN.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @jsii.member(jsii_name="metricDaysToExpiry")
    def metric_days_to_expiry(
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
        '''Return the DaysToExpiry metric for this AWS Certificate Manager Certificate. By default, this is the minimum value over 1 day.

        This metric is no longer emitted once the certificate has effectively
        expired, so alarms configured on this metric should probably treat missing
        data as "breaching".

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricDaysToExpiry", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICertificate).__jsii_proxy_class__ = lambda : _ICertificateProxy


@jsii.implements(ICertificate)
class PrivateCertificate(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-certificatemanager.PrivateCertificate",
):
    '''A private certificate managed by AWS Certificate Manager.

    :resource: AWS::CertificateManager::Certificate
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_acmpca as acmpca
        
        
        acm.PrivateCertificate(self, "PrivateCertificate",
            domain_name="test.example.com",
            subject_alternative_names=["cool.example.com", "test.example.net"],  # optional
            certificate_authority=acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CA", "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/023077d8-2bfa-4eb0-8f22-05c96deade77")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificate_authority: _aws_cdk_aws_acmpca_8c4081d6.ICertificateAuthority,
        domain_name: builtins.str,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param certificate_authority: Private certificate authority (CA) that will be used to issue the certificate.
        :param domain_name: Fully-qualified domain name to request a private certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your private certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3911c7520c26c16633489359e93339c9b414f93e33f178263fd5f531f9432dd0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PrivateCertificateProps(
            certificate_authority=certificate_authority,
            domain_name=domain_name,
            subject_alternative_names=subject_alternative_names,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCertificateArn")
    @builtins.classmethod
    def from_certificate_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        certificate_arn: builtins.str,
    ) -> ICertificate:
        '''Import a certificate.

        :param scope: -
        :param id: -
        :param certificate_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7892d5b4b8ae9c9ca5d407c7c63de37a58529175e0e01dbee387334a033419)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
        return typing.cast(ICertificate, jsii.sinvoke(cls, "fromCertificateArn", [scope, id, certificate_arn]))

    @jsii.member(jsii_name="metricDaysToExpiry")
    def metric_days_to_expiry(
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
        '''Return the DaysToExpiry metric for this AWS Certificate Manager Certificate. By default, this is the minimum value over 1 day.

        This metric is no longer emitted once the certificate has effectively
        expired, so alarms configured on this metric should probably treat missing
        data as "breaching".

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricDaysToExpiry", [props]))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''The certificate's ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def _region(self) -> typing.Optional[builtins.str]:
        '''If the certificate is provisionned in a different region than the containing stack, this should be the region in which the certificate lives so we can correctly create ``Metric`` instances.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-certificatemanager.PrivateCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority": "certificateAuthority",
        "domain_name": "domainName",
        "subject_alternative_names": "subjectAlternativeNames",
    },
)
class PrivateCertificateProps:
    def __init__(
        self,
        *,
        certificate_authority: _aws_cdk_aws_acmpca_8c4081d6.ICertificateAuthority,
        domain_name: builtins.str,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for your private certificate.

        :param certificate_authority: Private certificate authority (CA) that will be used to issue the certificate.
        :param domain_name: Fully-qualified domain name to request a private certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your private certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_acmpca as acmpca
            
            
            acm.PrivateCertificate(self, "PrivateCertificate",
                domain_name="test.example.com",
                subject_alternative_names=["cool.example.com", "test.example.net"],  # optional
                certificate_authority=acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CA", "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/023077d8-2bfa-4eb0-8f22-05c96deade77")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55bd5a5f8367daed4ba1ca1d233c462ad8d0eaa4fb895c733440ed8ea43447e)
            check_type(argname="argument certificate_authority", value=certificate_authority, expected_type=type_hints["certificate_authority"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_authority": certificate_authority,
            "domain_name": domain_name,
        }
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names

    @builtins.property
    def certificate_authority(
        self,
    ) -> _aws_cdk_aws_acmpca_8c4081d6.ICertificateAuthority:
        '''Private certificate authority (CA) that will be used to issue the certificate.'''
        result = self._values.get("certificate_authority")
        assert result is not None, "Required property 'certificate_authority' is missing"
        return typing.cast(_aws_cdk_aws_acmpca_8c4081d6.ICertificateAuthority, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Fully-qualified domain name to request a private certificate for.

        May contain wildcards, such as ``*.domain.com``.
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Alternative domain names on your private certificate.

        Use this to register alternative domain names that represent the same site.

        :default: - No additional FQDNs will be included as alternative domain names.
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivateCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-certificatemanager.ValidationMethod")
class ValidationMethod(enum.Enum):
    '''Method used to assert ownership of the domain.'''

    EMAIL = "EMAIL"
    '''Send email to a number of email addresses associated with the domain.

    :see: https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html
    '''
    DNS = "DNS"
    '''Validate ownership by adding appropriate DNS records.

    :see: https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html
    '''


@jsii.implements(ICertificate)
class Certificate(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-certificatemanager.Certificate",
):
    '''A certificate managed by AWS Certificate Manager.

    :exampleMetadata: infused

    Example::

        pool = cognito.UserPool(self, "Pool")
        
        pool.add_domain("CognitoDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="my-awesome-app"
            )
        )
        
        certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/11-3336f1-44483d-adc7-9cd375c5169d"
        
        domain_cert = certificatemanager.Certificate.from_certificate_arn(self, "domainCert", certificate_arn)
        pool.add_domain("CustomDomain",
            custom_domain=cognito.CustomDomainOptions(
                domain_name="user.myapp.com",
                certificate=domain_cert
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        validation: typing.Optional[CertificateValidation] = None,
        validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        validation_method: typing.Optional[ValidationMethod] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation: How to validate this certificate. Default: CertificateValidation.fromEmail()
        :param validation_domains: (deprecated) What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: (deprecated) Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94e8c0f842fce696dc1f7b179a00cf8587dec3bef406b779640e949673ab92d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CertificateProps(
            domain_name=domain_name,
            subject_alternative_names=subject_alternative_names,
            validation=validation,
            validation_domains=validation_domains,
            validation_method=validation_method,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCertificateArn")
    @builtins.classmethod
    def from_certificate_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        certificate_arn: builtins.str,
    ) -> ICertificate:
        '''Import a certificate.

        :param scope: -
        :param id: -
        :param certificate_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a4a4d318a4baaac3b259f4863f53a7afd075fe2ac866ef6549ea4661edc471)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
        return typing.cast(ICertificate, jsii.sinvoke(cls, "fromCertificateArn", [scope, id, certificate_arn]))

    @jsii.member(jsii_name="metricDaysToExpiry")
    def metric_days_to_expiry(
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
        '''Return the DaysToExpiry metric for this AWS Certificate Manager Certificate. By default, this is the minimum value over 1 day.

        This metric is no longer emitted once the certificate has effectively
        expired, so alarms configured on this metric should probably treat missing
        data as "breaching".

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricDaysToExpiry", [props]))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''The certificate's ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def _region(self) -> typing.Optional[builtins.str]:
        '''If the certificate is provisionned in a different region than the containing stack, this should be the region in which the certificate lives so we can correctly create ``Metric`` instances.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.implements(ICertificate, _aws_cdk_core_f4b25747.ITaggable)
class DnsValidatedCertificate(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-certificatemanager.DnsValidatedCertificate",
):
    '''A certificate managed by AWS Certificate Manager.

    Will be automatically
    validated using DNS validation against the specified Route 53 hosted zone.

    :resource: AWS::CertificateManager::Certificate
    :exampleMetadata: infused

    Example::

        # my_hosted_zone: route53.HostedZone
        
        acm.DnsValidatedCertificate(self, "CrossRegionCertificate",
            domain_name="hello.example.com",
            hosted_zone=my_hosted_zone,
            region="us-east-1"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        hosted_zone: _aws_cdk_aws_route53_f47b29d4.IHostedZone,
        cleanup_route53_records: typing.Optional[builtins.bool] = None,
        custom_resource_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        region: typing.Optional[builtins.str] = None,
        route53_endpoint: typing.Optional[builtins.str] = None,
        domain_name: builtins.str,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        validation: typing.Optional[CertificateValidation] = None,
        validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        validation_method: typing.Optional[ValidationMethod] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param hosted_zone: Route 53 Hosted Zone used to perform DNS validation of the request. The zone must be authoritative for the domain name specified in the Certificate Request.
        :param cleanup_route53_records: When set to true, when the DnsValidatedCertificate is deleted, the associated Route53 validation records are removed. CAUTION: If multiple certificates share the same domains (and same validation records), this can cause the other certificates to fail renewal and/or not validate. Not recommended for production use. Default: false
        :param custom_resource_role: Role to use for the custom resource that creates the validated certificate. Default: - A new role will be created
        :param region: AWS region that will host the certificate. This is needed especially for certificates used for CloudFront distributions, which require the region to be us-east-1. Default: the region the stack is deployed in.
        :param route53_endpoint: An endpoint of Route53 service, which is not necessary as AWS SDK could figure out the right endpoints for most regions, but for some regions such as those in aws-cn partition, the default endpoint is not working now, hence the right endpoint need to be specified through this prop. Route53 is not been officially launched in China, it is only available for AWS internal accounts now. To make DnsValidatedCertificate work for internal accounts now, a special endpoint needs to be provided. Default: - The AWS SDK will determine the Route53 endpoint to use based on region
        :param domain_name: Fully-qualified domain name to request a certificate for. May contain wildcards, such as ``*.domain.com``.
        :param subject_alternative_names: Alternative domain names on your certificate. Use this to register alternative domain names that represent the same site. Default: - No additional FQDNs will be included as alternative domain names.
        :param validation: How to validate this certificate. Default: CertificateValidation.fromEmail()
        :param validation_domains: (deprecated) What validation domain to use for every requested domain. Has to be a superdomain of the requested domain. Default: - Apex domain is used for every domain that's not overridden.
        :param validation_method: (deprecated) Validation method used to assert domain ownership. Default: ValidationMethod.EMAIL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff60fa89dd98f0e19241de448621f4ae4c8cfe8c095f7eda36a58cf01ddd504)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DnsValidatedCertificateProps(
            hosted_zone=hosted_zone,
            cleanup_route53_records=cleanup_route53_records,
            custom_resource_role=custom_resource_role,
            region=region,
            route53_endpoint=route53_endpoint,
            domain_name=domain_name,
            subject_alternative_names=subject_alternative_names,
            validation=validation,
            validation_domains=validation_domains,
            validation_method=validation_method,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="metricDaysToExpiry")
    def metric_days_to_expiry(
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
        '''Return the DaysToExpiry metric for this AWS Certificate Manager Certificate. By default, this is the minimum value over 1 day.

        This metric is no longer emitted once the certificate has effectively
        expired, so alarms configured on this metric should probably treat missing
        data as "breaching".

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
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

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metricDaysToExpiry", [props]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''The certificate's ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Resource Tags.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def _region(self) -> typing.Optional[builtins.str]:
        '''If the certificate is provisionned in a different region than the containing stack, this should be the region in which the certificate lives so we can correctly create ``Metric`` instances.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


__all__ = [
    "Certificate",
    "CertificateProps",
    "CertificateValidation",
    "CertificationValidationProps",
    "CfnAccount",
    "CfnAccountProps",
    "CfnCertificate",
    "CfnCertificateProps",
    "DnsValidatedCertificate",
    "DnsValidatedCertificateProps",
    "ICertificate",
    "PrivateCertificate",
    "PrivateCertificateProps",
    "ValidationMethod",
]

publication.publish()

def _typecheckingstub__07eee4869bda1d699f13a82ed6a8346f04e2866672285937db18e94da5a9cecc(
    *,
    domain_name: builtins.str,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    validation: typing.Optional[CertificateValidation] = None,
    validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    validation_method: typing.Optional[ValidationMethod] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ad0adcce6346d80c4db02efbd6d7ee2567f252b88535866ee0f03bd198a757(
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe61f6707b3a5d302a4da32266d0270ce7358e78304a4d55b40f4a674ab37ac(
    hosted_zones: typing.Mapping[builtins.str, _aws_cdk_aws_route53_f47b29d4.IHostedZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ef87519e08c2056242ca072568b3824000e520462c6261b7ea05320c3b0213(
    validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48da59f7382d88ab2d6c8522c904091ae5e2d8642c60024a45ec5e5ea3c05fd(
    *,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    hosted_zones: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_route53_f47b29d4.IHostedZone]] = None,
    method: typing.Optional[ValidationMethod] = None,
    validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23e45ca4cc31b8d44283875567a80800091912eece0c5763fcb8f7410ce9862(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    expiry_events_configuration: typing.Union[typing.Union[CfnAccount.ExpiryEventsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b7668affbd2288301d2655ee8726c1cd7d1c44bae9a3627463989ac2ff2713(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1c2f310de06940b379bd28a78aa91d84b8f955c99190c6b53d790c84baa4b5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2d2575448d25618f4706d315bf4d81460bd89a55082113e78773591787afb7(
    value: typing.Union[CfnAccount.ExpiryEventsConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad74fe50da176264b01b1312e4a29aa0d0dfcde3892b3ca3623b47ad8c26d9b(
    *,
    days_before_expiry: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19bee2772c049853523980ea3e9548f0e823787ee6d951fb15079f9f8828a86(
    *,
    expiry_events_configuration: typing.Union[typing.Union[CfnAccount.ExpiryEventsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78acff60e7f2cd388833af17cd9bff3fb31dd6b31070cb3b4672358d477a3f99(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    certificate_transparency_logging_preference: typing.Optional[builtins.str] = None,
    domain_validation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.DomainValidationOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    validation_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd872b3b23cd9ba82705fd300a078271e7c78253fe4531c45e766ac8d7167af(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c0026ee5e1d0c7719f9926217bc56106448b5def35f393c45d8349811c763c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9a3305c8a79e438bb46a2d9ee6b8e4135da7e689ecb7ab5fb4e644da129c4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394b786c0395a3e062ad8a5c3f8ddf2d7ef5a10bae6d8fb48908b35497f8411a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd745f54b51b7cec826cd7318a41c8aec435641c13256f454b12914a8a825c7e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844b446d1ef35fc8a6cf0720190630fed02af574470208431340add9c25b9614(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificate.DomainValidationOptionProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431c29079b1cba692a45c2522bd8166c5cbe42abec31c1a9b590ff1304a62af2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08908a2bb9aa075dc18f555ac8842a12512e6e85f2bfd52e9a7bc5fdaa67d41(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477b08cfc0e04f8a880e4dda182ecde2cea00f41b84a9573d05a21bd993a3c37(
    *,
    domain_name: builtins.str,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    validation_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf091bbc992e3d46f9d9f7ff5de0fca3a55258e4528c55aec687bc2c2ebff57(
    *,
    domain_name: builtins.str,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    certificate_transparency_logging_preference: typing.Optional[builtins.str] = None,
    domain_validation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.DomainValidationOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    validation_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e177870cc744dc4ccbb34eb3b47cc5c50139c0f835b208143484f4c4e28492f(
    *,
    domain_name: builtins.str,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    validation: typing.Optional[CertificateValidation] = None,
    validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    validation_method: typing.Optional[ValidationMethod] = None,
    hosted_zone: _aws_cdk_aws_route53_f47b29d4.IHostedZone,
    cleanup_route53_records: typing.Optional[builtins.bool] = None,
    custom_resource_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    region: typing.Optional[builtins.str] = None,
    route53_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3911c7520c26c16633489359e93339c9b414f93e33f178263fd5f531f9432dd0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificate_authority: _aws_cdk_aws_acmpca_8c4081d6.ICertificateAuthority,
    domain_name: builtins.str,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7892d5b4b8ae9c9ca5d407c7c63de37a58529175e0e01dbee387334a033419(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    certificate_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55bd5a5f8367daed4ba1ca1d233c462ad8d0eaa4fb895c733440ed8ea43447e(
    *,
    certificate_authority: _aws_cdk_aws_acmpca_8c4081d6.ICertificateAuthority,
    domain_name: builtins.str,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94e8c0f842fce696dc1f7b179a00cf8587dec3bef406b779640e949673ab92d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    validation: typing.Optional[CertificateValidation] = None,
    validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    validation_method: typing.Optional[ValidationMethod] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a4a4d318a4baaac3b259f4863f53a7afd075fe2ac866ef6549ea4661edc471(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    certificate_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff60fa89dd98f0e19241de448621f4ae4c8cfe8c095f7eda36a58cf01ddd504(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    hosted_zone: _aws_cdk_aws_route53_f47b29d4.IHostedZone,
    cleanup_route53_records: typing.Optional[builtins.bool] = None,
    custom_resource_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    region: typing.Optional[builtins.str] = None,
    route53_endpoint: typing.Optional[builtins.str] = None,
    domain_name: builtins.str,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    validation: typing.Optional[CertificateValidation] = None,
    validation_domains: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    validation_method: typing.Optional[ValidationMethod] = None,
) -> None:
    """Type checking stubs"""
    pass
