'''
# AWS::ACMPCA Construct Library

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
import aws_cdk.aws_acmpca as acmpca
```

## Certificate Authority

This package contains a `CertificateAuthority` class.
At the moment, you cannot create new Authorities using it,
but you can import existing ones using the `fromCertificateAuthorityArn` static method:

```python
certificate_authority = acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CA", "arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/023077d8-2bfa-4eb0-8f22-05c96deade77")
```

## Low-level `Cfn*` classes

You can always use the low-level classes
(starting with `Cfn*`) to create resources like the Certificate Authority:

```python
cfn_certificate_authority = acmpca.CfnCertificateAuthority(self, "CA",
    type="ROOT",
    key_algorithm="RSA_2048",
    signing_algorithm="SHA256WITHRSA",
    subject=acmpca.CfnCertificateAuthority.SubjectProperty(
        country="US",
        organization="string",
        organizational_unit="string",
        distinguished_name_qualifier="string",
        state="string",
        common_name="123",
        serial_number="string",
        locality="string",
        title="string",
        surname="string",
        given_name="string",
        initials="DG",
        pseudonym="string",
        generation_qualifier="DBG"
    )
)
```

If you need to pass the higher-level `ICertificateAuthority` somewhere,
you can get it from the lower-level `CfnCertificateAuthority` using the same `fromCertificateAuthorityArn` method:

```python
# cfn_certificate_authority: acmpca.CfnCertificateAuthority


certificate_authority = acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", cfn_certificate_authority.attr_arn)
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

import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


class CertificateAuthority(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CertificateAuthority",
):
    '''Defines a Certificate for ACMPCA.

    :resource: AWS::ACMPCA::CertificateAuthority
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_acmpca as acmpca
        
        # vpc: ec2.Vpc
        
        cluster = msk.Cluster(self, "Cluster",
            cluster_name="myCluster",
            kafka_version=msk.KafkaVersion.V2_8_1,
            vpc=vpc,
            encryption_in_transit=msk.EncryptionInTransitConfig(
                client_broker=msk.ClientBrokerEncryption.TLS
            ),
            client_authentication=msk.ClientAuthentication.tls(
                certificate_authorities=[
                    acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
                ]
            )
        )
    '''

    @jsii.member(jsii_name="fromCertificateAuthorityArn")
    @builtins.classmethod
    def from_certificate_authority_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        certificate_authority_arn: builtins.str,
    ) -> "ICertificateAuthority":
        '''Import an existing Certificate given an ARN.

        :param scope: -
        :param id: -
        :param certificate_authority_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b779f19c53698e23b2d8dd482a155c35242462848352fb14b975b18ea0746f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
        return typing.cast("ICertificateAuthority", jsii.sinvoke(cls, "fromCertificateAuthorityArn", [scope, id, certificate_authority_arn]))


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCertificate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificate",
):
    '''A CloudFormation ``AWS::ACMPCA::Certificate``.

    The ``AWS::ACMPCA::Certificate`` resource is used to issue a certificate using your private certificate authority. For more information, see the `IssueCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_IssueCertificate.html>`_ action.

    :cloudformationResource: AWS::ACMPCA::Certificate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_acmpca as acmpca
        
        cfn_certificate = acmpca.CfnCertificate(self, "MyCfnCertificate",
            certificate_authority_arn="certificateAuthorityArn",
            certificate_signing_request="certificateSigningRequest",
            signing_algorithm="signingAlgorithm",
            validity=acmpca.CfnCertificate.ValidityProperty(
                type="type",
                value=123
            ),
        
            # the properties below are optional
            api_passthrough=acmpca.CfnCertificate.ApiPassthroughProperty(
                extensions=acmpca.CfnCertificate.ExtensionsProperty(
                    certificate_policies=[acmpca.CfnCertificate.PolicyInformationProperty(
                        cert_policy_id="certPolicyId",
        
                        # the properties below are optional
                        policy_qualifiers=[acmpca.CfnCertificate.PolicyQualifierInfoProperty(
                            policy_qualifier_id="policyQualifierId",
                            qualifier=acmpca.CfnCertificate.QualifierProperty(
                                cps_uri="cpsUri"
                            )
                        )]
                    )],
                    custom_extensions=[acmpca.CfnCertificate.CustomExtensionProperty(
                        object_identifier="objectIdentifier",
                        value="value",
        
                        # the properties below are optional
                        critical=False
                    )],
                    extended_key_usage=[acmpca.CfnCertificate.ExtendedKeyUsageProperty(
                        extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                        extended_key_usage_type="extendedKeyUsageType"
                    )],
                    key_usage=acmpca.CfnCertificate.KeyUsageProperty(
                        crl_sign=False,
                        data_encipherment=False,
                        decipher_only=False,
                        digital_signature=False,
                        encipher_only=False,
                        key_agreement=False,
                        key_cert_sign=False,
                        key_encipherment=False,
                        non_repudiation=False
                    ),
                    subject_alternative_names=[acmpca.CfnCertificate.GeneralNameProperty(
                        directory_name=acmpca.CfnCertificate.SubjectProperty(
                            common_name="commonName",
                            country="country",
                            custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                                object_identifier="objectIdentifier",
                                value="value"
                            )],
                            distinguished_name_qualifier="distinguishedNameQualifier",
                            generation_qualifier="generationQualifier",
                            given_name="givenName",
                            initials="initials",
                            locality="locality",
                            organization="organization",
                            organizational_unit="organizationalUnit",
                            pseudonym="pseudonym",
                            serial_number="serialNumber",
                            state="state",
                            surname="surname",
                            title="title"
                        ),
                        dns_name="dnsName",
                        edi_party_name=acmpca.CfnCertificate.EdiPartyNameProperty(
                            name_assigner="nameAssigner",
                            party_name="partyName"
                        ),
                        ip_address="ipAddress",
                        other_name=acmpca.CfnCertificate.OtherNameProperty(
                            type_id="typeId",
                            value="value"
                        ),
                        registered_id="registeredId",
                        rfc822_name="rfc822Name",
                        uniform_resource_identifier="uniformResourceIdentifier"
                    )]
                ),
                subject=acmpca.CfnCertificate.SubjectProperty(
                    common_name="commonName",
                    country="country",
                    custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    distinguished_name_qualifier="distinguishedNameQualifier",
                    generation_qualifier="generationQualifier",
                    given_name="givenName",
                    initials="initials",
                    locality="locality",
                    organization="organization",
                    organizational_unit="organizationalUnit",
                    pseudonym="pseudonym",
                    serial_number="serialNumber",
                    state="state",
                    surname="surname",
                    title="title"
                )
            ),
            template_arn="templateArn",
            validity_not_before=acmpca.CfnCertificate.ValidityProperty(
                type="type",
                value=123
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        certificate_authority_arn: builtins.str,
        certificate_signing_request: builtins.str,
        signing_algorithm: builtins.str,
        validity: typing.Union[typing.Union["CfnCertificate.ValidityProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        api_passthrough: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.ApiPassthroughProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        template_arn: typing.Optional[builtins.str] = None,
        validity_not_before: typing.Optional[typing.Union[typing.Union["CfnCertificate.ValidityProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::ACMPCA::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_authority_arn: The Amazon Resource Name (ARN) for the private CA issues the certificate.
        :param certificate_signing_request: The certificate signing request (CSR) for the certificate.
        :param signing_algorithm: The name of the algorithm that will be used to sign the certificate to be issued. This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign a CSR in the ``CreateCertificateAuthority`` action. .. epigraph:: The specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key.
        :param validity: The period of time during which the certificate will be valid.
        :param api_passthrough: Specifies X.509 certificate information to be included in the issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.
        :param template_arn: Specifies a custom configuration template to use when issuing a certificate. If this parameter is not provided, AWS Private CA defaults to the ``EndEntityCertificate/V1`` template. For more information about AWS Private CA templates, see `Using Templates <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html>`_ .
        :param validity_not_before: Information describing the start of the validity period of the certificate. This parameter sets the “Not Before" date for the certificate. By default, when issuing a certificate, AWS Private CA sets the "Not Before" date to the issuance time minus 60 minutes. This compensates for clock inconsistencies across computer systems. The ``ValidityNotBefore`` parameter can be used to customize the “Not Before” value. Unlike the ``Validity`` parameter, the ``ValidityNotBefore`` parameter is optional. The ``ValidityNotBefore`` value is expressed as an explicit date and time, using the ``Validity`` type value ``ABSOLUTE`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a0a1072e9f353dc3ff3e9116e76340a54ad697a4417471337a42e7a72378ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCertificateProps(
            certificate_authority_arn=certificate_authority_arn,
            certificate_signing_request=certificate_signing_request,
            signing_algorithm=signing_algorithm,
            validity=validity,
            api_passthrough=api_passthrough,
            template_arn=template_arn,
            validity_not_before=validity_not_before,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c06e49a9bdff97b0e473f2aaf32c664ba189ba301ceae2140e1a558e240dddc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a2c48fe1bcbdf74f60d160666116a09e64b051569b2e1f650f13be9d1bfb5ff)
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
        '''The Amazon Resource Name (ARN) of the issued certificate.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCertificate")
    def attr_certificate(self) -> builtins.str:
        '''The issued Base64 PEM-encoded certificate.

        :cloudformationAttribute: Certificate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCertificate"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the private CA issues the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthorityArn"))

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572d0abf21d692ee812fc2cd284b7f5f13612f8a92daf661130ec9f03a72acde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property
    @jsii.member(jsii_name="certificateSigningRequest")
    def certificate_signing_request(self) -> builtins.str:
        '''The certificate signing request (CSR) for the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateSigningRequest"))

    @certificate_signing_request.setter
    def certificate_signing_request(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a599ab5ceb72e84d3e82b81d48b745f513636ee459ccac6a0a82f80afed8cbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateSigningRequest", value)

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        '''The name of the algorithm that will be used to sign the certificate to be issued.

        This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign a CSR in the ``CreateCertificateAuthority`` action.
        .. epigraph::

           The specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingAlgorithm"))

    @signing_algorithm.setter
    def signing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db41702a33ddeb9f9c5c8226369147ac3d7ed616a99aa66bbc4f2d12434a421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="validity")
    def validity(
        self,
    ) -> typing.Union["CfnCertificate.ValidityProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The period of time during which the certificate will be valid.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        '''
        return typing.cast(typing.Union["CfnCertificate.ValidityProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "validity"))

    @validity.setter
    def validity(
        self,
        value: typing.Union["CfnCertificate.ValidityProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290bce6750f48c1dd860aec70e8a58f84c2cd885defdfe31dbdd54d78fd6f6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validity", value)

    @builtins.property
    @jsii.member(jsii_name="apiPassthrough")
    def api_passthrough(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.ApiPassthroughProperty"]]:
        '''Specifies X.509 certificate information to be included in the issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-apipassthrough
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.ApiPassthroughProperty"]], jsii.get(self, "apiPassthrough"))

    @api_passthrough.setter
    def api_passthrough(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.ApiPassthroughProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619d7ddd269b7c84d19ccbadf67472c82f51c3c1ba43c4fa6e302850d1565a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiPassthrough", value)

    @builtins.property
    @jsii.member(jsii_name="templateArn")
    def template_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies a custom configuration template to use when issuing a certificate.

        If this parameter is not provided, AWS Private CA defaults to the ``EndEntityCertificate/V1`` template. For more information about AWS Private CA templates, see `Using Templates <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateArn"))

    @template_arn.setter
    def template_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ee6f79370132ffcb0e4c34505498476414bc3c96bb8acfa4d609c544eae905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateArn", value)

    @builtins.property
    @jsii.member(jsii_name="validityNotBefore")
    def validity_not_before(
        self,
    ) -> typing.Optional[typing.Union["CfnCertificate.ValidityProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''Information describing the start of the validity period of the certificate.

        This parameter sets the “Not Before" date for the certificate.

        By default, when issuing a certificate, AWS Private CA sets the "Not Before" date to the issuance time minus 60 minutes. This compensates for clock inconsistencies across computer systems. The ``ValidityNotBefore`` parameter can be used to customize the “Not Before” value.

        Unlike the ``Validity`` parameter, the ``ValidityNotBefore`` parameter is optional.

        The ``ValidityNotBefore`` value is expressed as an explicit date and time, using the ``Validity`` type value ``ABSOLUTE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validitynotbefore
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCertificate.ValidityProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "validityNotBefore"))

    @validity_not_before.setter
    def validity_not_before(
        self,
        value: typing.Optional[typing.Union["CfnCertificate.ValidityProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8697a8d670b4b60188223097ee218739bac0327dd665a252aba128f6a3b3c3a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validityNotBefore", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ApiPassthroughProperty",
        jsii_struct_bases=[],
        name_mapping={"extensions": "extensions", "subject": "subject"},
    )
    class ApiPassthroughProperty:
        def __init__(
            self,
            *,
            extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.ExtensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.SubjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains X.509 certificate information to be placed in an issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.

            If conflicting or duplicate certificate information is supplied from other sources, AWS Private CA applies `order of operation rules <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html#template-order-of-operations>`_ to determine what information is used.

            :param extensions: Specifies X.509 extension information for a certificate.
            :param subject: Contains information about the certificate subject. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                api_passthrough_property = acmpca.CfnCertificate.ApiPassthroughProperty(
                    extensions=acmpca.CfnCertificate.ExtensionsProperty(
                        certificate_policies=[acmpca.CfnCertificate.PolicyInformationProperty(
                            cert_policy_id="certPolicyId",
                
                            # the properties below are optional
                            policy_qualifiers=[acmpca.CfnCertificate.PolicyQualifierInfoProperty(
                                policy_qualifier_id="policyQualifierId",
                                qualifier=acmpca.CfnCertificate.QualifierProperty(
                                    cps_uri="cpsUri"
                                )
                            )]
                        )],
                        custom_extensions=[acmpca.CfnCertificate.CustomExtensionProperty(
                            object_identifier="objectIdentifier",
                            value="value",
                
                            # the properties below are optional
                            critical=False
                        )],
                        extended_key_usage=[acmpca.CfnCertificate.ExtendedKeyUsageProperty(
                            extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                            extended_key_usage_type="extendedKeyUsageType"
                        )],
                        key_usage=acmpca.CfnCertificate.KeyUsageProperty(
                            crl_sign=False,
                            data_encipherment=False,
                            decipher_only=False,
                            digital_signature=False,
                            encipher_only=False,
                            key_agreement=False,
                            key_cert_sign=False,
                            key_encipherment=False,
                            non_repudiation=False
                        ),
                        subject_alternative_names=[acmpca.CfnCertificate.GeneralNameProperty(
                            directory_name=acmpca.CfnCertificate.SubjectProperty(
                                common_name="commonName",
                                country="country",
                                custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                                    object_identifier="objectIdentifier",
                                    value="value"
                                )],
                                distinguished_name_qualifier="distinguishedNameQualifier",
                                generation_qualifier="generationQualifier",
                                given_name="givenName",
                                initials="initials",
                                locality="locality",
                                organization="organization",
                                organizational_unit="organizationalUnit",
                                pseudonym="pseudonym",
                                serial_number="serialNumber",
                                state="state",
                                surname="surname",
                                title="title"
                            ),
                            dns_name="dnsName",
                            edi_party_name=acmpca.CfnCertificate.EdiPartyNameProperty(
                                name_assigner="nameAssigner",
                                party_name="partyName"
                            ),
                            ip_address="ipAddress",
                            other_name=acmpca.CfnCertificate.OtherNameProperty(
                                type_id="typeId",
                                value="value"
                            ),
                            registered_id="registeredId",
                            rfc822_name="rfc822Name",
                            uniform_resource_identifier="uniformResourceIdentifier"
                        )]
                    ),
                    subject=acmpca.CfnCertificate.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff91782eacbaa78222a37678f74b9c61b6d477a306e2d2895ac0331c8522299d)
                check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if extensions is not None:
                self._values["extensions"] = extensions
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def extensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.ExtensionsProperty"]]:
            '''Specifies X.509 extension information for a certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html#cfn-acmpca-certificate-apipassthrough-extensions
            '''
            result = self._values.get("extensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.ExtensionsProperty"]], result)

        @builtins.property
        def subject(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.SubjectProperty"]]:
            '''Contains information about the certificate subject.

            The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html#cfn-acmpca-certificate-apipassthrough-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.SubjectProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiPassthroughProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.CustomAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"object_identifier": "objectIdentifier", "value": "value"},
    )
    class CustomAttributeProperty:
        def __init__(
            self,
            *,
            object_identifier: builtins.str,
            value: builtins.str,
        ) -> None:
            '''Defines the X.500 relative distinguished name (RDN).

            :param object_identifier: Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).
            :param value: Specifies the attribute value of relative distinguished name (RDN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                custom_attribute_property = acmpca.CfnCertificate.CustomAttributeProperty(
                    object_identifier="objectIdentifier",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__087eef006c1f99facb7d2e7fb96bdb59575caa7cf2c9e46f07e962499844af25)
                check_type(argname="argument object_identifier", value=object_identifier, expected_type=type_hints["object_identifier"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object_identifier": object_identifier,
                "value": value,
            }

        @builtins.property
        def object_identifier(self) -> builtins.str:
            '''Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customattribute.html#cfn-acmpca-certificate-customattribute-objectidentifier
            '''
            result = self._values.get("object_identifier")
            assert result is not None, "Required property 'object_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Specifies the attribute value of relative distinguished name (RDN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customattribute.html#cfn-acmpca-certificate-customattribute-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.CustomExtensionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object_identifier": "objectIdentifier",
            "value": "value",
            "critical": "critical",
        },
    )
    class CustomExtensionProperty:
        def __init__(
            self,
            *,
            object_identifier: builtins.str,
            value: builtins.str,
            critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Specifies the X.509 extension information for a certificate.

            Extensions present in ``CustomExtensions`` follow the ``ApiPassthrough`` `template rules <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html#template-order-of-operations>`_ .

            :param object_identifier: Specifies the object identifier (OID) of the X.509 extension. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.
            :param value: Specifies the base64-encoded value of the X.509 extension.
            :param critical: Specifies the critical flag of the X.509 extension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                custom_extension_property = acmpca.CfnCertificate.CustomExtensionProperty(
                    object_identifier="objectIdentifier",
                    value="value",
                
                    # the properties below are optional
                    critical=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c546930085bb5cf8212c3606334df99f3d44cc5bd323f6c8bfce90907ee3b206)
                check_type(argname="argument object_identifier", value=object_identifier, expected_type=type_hints["object_identifier"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object_identifier": object_identifier,
                "value": value,
            }
            if critical is not None:
                self._values["critical"] = critical

        @builtins.property
        def object_identifier(self) -> builtins.str:
            '''Specifies the object identifier (OID) of the X.509 extension. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html#cfn-acmpca-certificate-customextension-objectidentifier
            '''
            result = self._values.get("object_identifier")
            assert result is not None, "Required property 'object_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Specifies the base64-encoded value of the X.509 extension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html#cfn-acmpca-certificate-customextension-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def critical(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies the critical flag of the X.509 extension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html#cfn-acmpca-certificate-customextension-critical
            '''
            result = self._values.get("critical")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomExtensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.EdiPartyNameProperty",
        jsii_struct_bases=[],
        name_mapping={"name_assigner": "nameAssigner", "party_name": "partyName"},
    )
    class EdiPartyNameProperty:
        def __init__(
            self,
            *,
            name_assigner: builtins.str,
            party_name: builtins.str,
        ) -> None:
            '''Describes an Electronic Data Interchange (EDI) entity as described in as defined in `Subject Alternative Name <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ in RFC 5280.

            :param name_assigner: Specifies the name assigner.
            :param party_name: Specifies the party name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                edi_party_name_property = acmpca.CfnCertificate.EdiPartyNameProperty(
                    name_assigner="nameAssigner",
                    party_name="partyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4212f757de164ed8e15f74c347e401c6e38aace2fd454c09d2ef85d78fcfbf73)
                check_type(argname="argument name_assigner", value=name_assigner, expected_type=type_hints["name_assigner"])
                check_type(argname="argument party_name", value=party_name, expected_type=type_hints["party_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name_assigner": name_assigner,
                "party_name": party_name,
            }

        @builtins.property
        def name_assigner(self) -> builtins.str:
            '''Specifies the name assigner.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html#cfn-acmpca-certificate-edipartyname-nameassigner
            '''
            result = self._values.get("name_assigner")
            assert result is not None, "Required property 'name_assigner' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def party_name(self) -> builtins.str:
            '''Specifies the party name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html#cfn-acmpca-certificate-edipartyname-partyname
            '''
            result = self._values.get("party_name")
            assert result is not None, "Required property 'party_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiPartyNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ExtendedKeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "extended_key_usage_object_identifier": "extendedKeyUsageObjectIdentifier",
            "extended_key_usage_type": "extendedKeyUsageType",
        },
    )
    class ExtendedKeyUsageProperty:
        def __init__(
            self,
            *,
            extended_key_usage_object_identifier: typing.Optional[builtins.str] = None,
            extended_key_usage_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies additional purposes for which the certified public key may be used other than basic purposes indicated in the ``KeyUsage`` extension.

            :param extended_key_usage_object_identifier: Specifies a custom ``ExtendedKeyUsage`` with an object identifier (OID).
            :param extended_key_usage_type: Specifies a standard ``ExtendedKeyUsage`` as defined as in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                extended_key_usage_property = acmpca.CfnCertificate.ExtendedKeyUsageProperty(
                    extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                    extended_key_usage_type="extendedKeyUsageType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6cf98e5d4e826e748b992e19e50b9df7750e621171f629d540f34addea270ad2)
                check_type(argname="argument extended_key_usage_object_identifier", value=extended_key_usage_object_identifier, expected_type=type_hints["extended_key_usage_object_identifier"])
                check_type(argname="argument extended_key_usage_type", value=extended_key_usage_type, expected_type=type_hints["extended_key_usage_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if extended_key_usage_object_identifier is not None:
                self._values["extended_key_usage_object_identifier"] = extended_key_usage_object_identifier
            if extended_key_usage_type is not None:
                self._values["extended_key_usage_type"] = extended_key_usage_type

        @builtins.property
        def extended_key_usage_object_identifier(self) -> typing.Optional[builtins.str]:
            '''Specifies a custom ``ExtendedKeyUsage`` with an object identifier (OID).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html#cfn-acmpca-certificate-extendedkeyusage-extendedkeyusageobjectidentifier
            '''
            result = self._values.get("extended_key_usage_object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def extended_key_usage_type(self) -> typing.Optional[builtins.str]:
            '''Specifies a standard ``ExtendedKeyUsage`` as defined as in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html#cfn-acmpca-certificate-extendedkeyusage-extendedkeyusagetype
            '''
            result = self._values.get("extended_key_usage_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtendedKeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ExtensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_policies": "certificatePolicies",
            "custom_extensions": "customExtensions",
            "extended_key_usage": "extendedKeyUsage",
            "key_usage": "keyUsage",
            "subject_alternative_names": "subjectAlternativeNames",
        },
    )
    class ExtensionsProperty:
        def __init__(
            self,
            *,
            certificate_policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.PolicyInformationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.CustomExtensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            extended_key_usage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.ExtendedKeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            key_usage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.KeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.GeneralNameProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains X.509 extension information for a certificate.

            :param certificate_policies: Contains a sequence of one or more policy information terms, each of which consists of an object identifier (OID) and optional qualifiers. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ . In an end-entity certificate, these terms indicate the policy under which the certificate was issued and the purposes for which it may be used. In a CA certificate, these terms limit the set of policies for certification paths that include this certificate.
            :param custom_extensions: Contains a sequence of one or more X.509 extensions, each of which consists of an object identifier (OID), a base64-encoded value, and the critical flag. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.
            :param extended_key_usage: Specifies additional purposes for which the certified public key may be used other than basic purposes indicated in the ``KeyUsage`` extension.
            :param key_usage: Defines one or more purposes for which the key contained in the certificate can be used. Default value for each option is false.
            :param subject_alternative_names: The subject alternative name extension allows identities to be bound to the subject of the certificate. These identities may be included in addition to or in place of the identity in the subject field of the certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                extensions_property = acmpca.CfnCertificate.ExtensionsProperty(
                    certificate_policies=[acmpca.CfnCertificate.PolicyInformationProperty(
                        cert_policy_id="certPolicyId",
                
                        # the properties below are optional
                        policy_qualifiers=[acmpca.CfnCertificate.PolicyQualifierInfoProperty(
                            policy_qualifier_id="policyQualifierId",
                            qualifier=acmpca.CfnCertificate.QualifierProperty(
                                cps_uri="cpsUri"
                            )
                        )]
                    )],
                    custom_extensions=[acmpca.CfnCertificate.CustomExtensionProperty(
                        object_identifier="objectIdentifier",
                        value="value",
                
                        # the properties below are optional
                        critical=False
                    )],
                    extended_key_usage=[acmpca.CfnCertificate.ExtendedKeyUsageProperty(
                        extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                        extended_key_usage_type="extendedKeyUsageType"
                    )],
                    key_usage=acmpca.CfnCertificate.KeyUsageProperty(
                        crl_sign=False,
                        data_encipherment=False,
                        decipher_only=False,
                        digital_signature=False,
                        encipher_only=False,
                        key_agreement=False,
                        key_cert_sign=False,
                        key_encipherment=False,
                        non_repudiation=False
                    ),
                    subject_alternative_names=[acmpca.CfnCertificate.GeneralNameProperty(
                        directory_name=acmpca.CfnCertificate.SubjectProperty(
                            common_name="commonName",
                            country="country",
                            custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                                object_identifier="objectIdentifier",
                                value="value"
                            )],
                            distinguished_name_qualifier="distinguishedNameQualifier",
                            generation_qualifier="generationQualifier",
                            given_name="givenName",
                            initials="initials",
                            locality="locality",
                            organization="organization",
                            organizational_unit="organizationalUnit",
                            pseudonym="pseudonym",
                            serial_number="serialNumber",
                            state="state",
                            surname="surname",
                            title="title"
                        ),
                        dns_name="dnsName",
                        edi_party_name=acmpca.CfnCertificate.EdiPartyNameProperty(
                            name_assigner="nameAssigner",
                            party_name="partyName"
                        ),
                        ip_address="ipAddress",
                        other_name=acmpca.CfnCertificate.OtherNameProperty(
                            type_id="typeId",
                            value="value"
                        ),
                        registered_id="registeredId",
                        rfc822_name="rfc822Name",
                        uniform_resource_identifier="uniformResourceIdentifier"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75777752be170e0349d0a684b775a3ceb2ca93513e9acbec57f24673d7535579)
                check_type(argname="argument certificate_policies", value=certificate_policies, expected_type=type_hints["certificate_policies"])
                check_type(argname="argument custom_extensions", value=custom_extensions, expected_type=type_hints["custom_extensions"])
                check_type(argname="argument extended_key_usage", value=extended_key_usage, expected_type=type_hints["extended_key_usage"])
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
                check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_policies is not None:
                self._values["certificate_policies"] = certificate_policies
            if custom_extensions is not None:
                self._values["custom_extensions"] = custom_extensions
            if extended_key_usage is not None:
                self._values["extended_key_usage"] = extended_key_usage
            if key_usage is not None:
                self._values["key_usage"] = key_usage
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names

        @builtins.property
        def certificate_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.PolicyInformationProperty"]]]]:
            '''Contains a sequence of one or more policy information terms, each of which consists of an object identifier (OID) and optional qualifiers.

            For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            In an end-entity certificate, these terms indicate the policy under which the certificate was issued and the purposes for which it may be used. In a CA certificate, these terms limit the set of policies for certification paths that include this certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-certificatepolicies
            '''
            result = self._values.get("certificate_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.PolicyInformationProperty"]]]], result)

        @builtins.property
        def custom_extensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.CustomExtensionProperty"]]]]:
            '''Contains a sequence of one or more X.509 extensions, each of which consists of an object identifier (OID), a base64-encoded value, and the critical flag. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-customextensions
            '''
            result = self._values.get("custom_extensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.CustomExtensionProperty"]]]], result)

        @builtins.property
        def extended_key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.ExtendedKeyUsageProperty"]]]]:
            '''Specifies additional purposes for which the certified public key may be used other than basic purposes indicated in the ``KeyUsage`` extension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-extendedkeyusage
            '''
            result = self._values.get("extended_key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.ExtendedKeyUsageProperty"]]]], result)

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.KeyUsageProperty"]]:
            '''Defines one or more purposes for which the key contained in the certificate can be used.

            Default value for each option is false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.KeyUsageProperty"]], result)

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.GeneralNameProperty"]]]]:
            '''The subject alternative name extension allows identities to be bound to the subject of the certificate.

            These identities may be included in addition to or in place of the identity in the subject field of the certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.GeneralNameProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.GeneralNameProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "dns_name": "dnsName",
            "edi_party_name": "ediPartyName",
            "ip_address": "ipAddress",
            "other_name": "otherName",
            "registered_id": "registeredId",
            "rfc822_name": "rfc822Name",
            "uniform_resource_identifier": "uniformResourceIdentifier",
        },
    )
    class GeneralNameProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.SubjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dns_name: typing.Optional[builtins.str] = None,
            edi_party_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.EdiPartyNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_address: typing.Optional[builtins.str] = None,
            other_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.OtherNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            registered_id: typing.Optional[builtins.str] = None,
            rfc822_name: typing.Optional[builtins.str] = None,
            uniform_resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an ASN.1 X.400 ``GeneralName`` as defined in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ . Only one of the following naming options should be provided. Providing more than one option results in an ``InvalidArgsException`` error.

            :param directory_name: Contains information about the certificate subject. The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.
            :param dns_name: Represents ``GeneralName`` as a DNS name.
            :param edi_party_name: Represents ``GeneralName`` as an ``EdiPartyName`` object.
            :param ip_address: Represents ``GeneralName`` as an IPv4 or IPv6 address.
            :param other_name: Represents ``GeneralName`` using an ``OtherName`` object.
            :param registered_id: Represents ``GeneralName`` as an object identifier (OID).
            :param rfc822_name: Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.
            :param uniform_resource_identifier: Represents ``GeneralName`` as a URI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                general_name_property = acmpca.CfnCertificate.GeneralNameProperty(
                    directory_name=acmpca.CfnCertificate.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    ),
                    dns_name="dnsName",
                    edi_party_name=acmpca.CfnCertificate.EdiPartyNameProperty(
                        name_assigner="nameAssigner",
                        party_name="partyName"
                    ),
                    ip_address="ipAddress",
                    other_name=acmpca.CfnCertificate.OtherNameProperty(
                        type_id="typeId",
                        value="value"
                    ),
                    registered_id="registeredId",
                    rfc822_name="rfc822Name",
                    uniform_resource_identifier="uniformResourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e50b9009d68d9e053cade424315d94cff9232ce6a718275ede806c8efdb8648)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
                check_type(argname="argument edi_party_name", value=edi_party_name, expected_type=type_hints["edi_party_name"])
                check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
                check_type(argname="argument other_name", value=other_name, expected_type=type_hints["other_name"])
                check_type(argname="argument registered_id", value=registered_id, expected_type=type_hints["registered_id"])
                check_type(argname="argument rfc822_name", value=rfc822_name, expected_type=type_hints["rfc822_name"])
                check_type(argname="argument uniform_resource_identifier", value=uniform_resource_identifier, expected_type=type_hints["uniform_resource_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if edi_party_name is not None:
                self._values["edi_party_name"] = edi_party_name
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if other_name is not None:
                self._values["other_name"] = other_name
            if registered_id is not None:
                self._values["registered_id"] = registered_id
            if rfc822_name is not None:
                self._values["rfc822_name"] = rfc822_name
            if uniform_resource_identifier is not None:
                self._values["uniform_resource_identifier"] = uniform_resource_identifier

        @builtins.property
        def directory_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.SubjectProperty"]]:
            '''Contains information about the certificate subject.

            The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.SubjectProperty"]], result)

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a DNS name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-dnsname
            '''
            result = self._values.get("dns_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def edi_party_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.EdiPartyNameProperty"]]:
            '''Represents ``GeneralName`` as an ``EdiPartyName`` object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-edipartyname
            '''
            result = self._values.get("edi_party_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.EdiPartyNameProperty"]], result)

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an IPv4 or IPv6 address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-ipaddress
            '''
            result = self._values.get("ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def other_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.OtherNameProperty"]]:
            '''Represents ``GeneralName`` using an ``OtherName`` object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-othername
            '''
            result = self._values.get("other_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.OtherNameProperty"]], result)

        @builtins.property
        def registered_id(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an object identifier (OID).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-registeredid
            '''
            result = self._values.get("registered_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rfc822_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-rfc822name
            '''
            result = self._values.get("rfc822_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a URI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-uniformresourceidentifier
            '''
            result = self._values.get("uniform_resource_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.KeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_sign": "crlSign",
            "data_encipherment": "dataEncipherment",
            "decipher_only": "decipherOnly",
            "digital_signature": "digitalSignature",
            "encipher_only": "encipherOnly",
            "key_agreement": "keyAgreement",
            "key_cert_sign": "keyCertSign",
            "key_encipherment": "keyEncipherment",
            "non_repudiation": "nonRepudiation",
        },
    )
    class KeyUsageProperty:
        def __init__(
            self,
            *,
            crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Defines one or more purposes for which the key contained in the certificate can be used.

            Default value for each option is false.

            :param crl_sign: Key can be used to sign CRLs.
            :param data_encipherment: Key can be used to decipher data.
            :param decipher_only: Key can be used only to decipher data.
            :param digital_signature: Key can be used for digital signing.
            :param encipher_only: Key can be used only to encipher data.
            :param key_agreement: Key can be used in a key-agreement protocol.
            :param key_cert_sign: Key can be used to sign certificates.
            :param key_encipherment: Key can be used to encipher data.
            :param non_repudiation: Key can be used for non-repudiation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                key_usage_property = acmpca.CfnCertificate.KeyUsageProperty(
                    crl_sign=False,
                    data_encipherment=False,
                    decipher_only=False,
                    digital_signature=False,
                    encipher_only=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    key_encipherment=False,
                    non_repudiation=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f246ef49af70cdbea69263b309e8145387262940970094957a0a5408a27e4fb8)
                check_type(argname="argument crl_sign", value=crl_sign, expected_type=type_hints["crl_sign"])
                check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
                check_type(argname="argument decipher_only", value=decipher_only, expected_type=type_hints["decipher_only"])
                check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
                check_type(argname="argument encipher_only", value=encipher_only, expected_type=type_hints["encipher_only"])
                check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
                check_type(argname="argument key_cert_sign", value=key_cert_sign, expected_type=type_hints["key_cert_sign"])
                check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
                check_type(argname="argument non_repudiation", value=non_repudiation, expected_type=type_hints["non_repudiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crl_sign is not None:
                self._values["crl_sign"] = crl_sign
            if data_encipherment is not None:
                self._values["data_encipherment"] = data_encipherment
            if decipher_only is not None:
                self._values["decipher_only"] = decipher_only
            if digital_signature is not None:
                self._values["digital_signature"] = digital_signature
            if encipher_only is not None:
                self._values["encipher_only"] = encipher_only
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if key_cert_sign is not None:
                self._values["key_cert_sign"] = key_cert_sign
            if key_encipherment is not None:
                self._values["key_encipherment"] = key_encipherment
            if non_repudiation is not None:
                self._values["non_repudiation"] = non_repudiation

        @builtins.property
        def crl_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to sign CRLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-crlsign
            '''
            result = self._values.get("crl_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def data_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to decipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-dataencipherment
            '''
            result = self._values.get("data_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def decipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used only to decipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-decipheronly
            '''
            result = self._values.get("decipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def digital_signature(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used for digital signing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-digitalsignature
            '''
            result = self._values.get("digital_signature")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def encipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used only to encipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-encipheronly
            '''
            result = self._values.get("encipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used in a key-agreement protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keyagreement
            '''
            result = self._values.get("key_agreement")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def key_cert_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to sign certificates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keycertsign
            '''
            result = self._values.get("key_cert_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def key_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to encipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keyencipherment
            '''
            result = self._values.get("key_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def non_repudiation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used for non-repudiation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-nonrepudiation
            '''
            result = self._values.get("non_repudiation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.OtherNameProperty",
        jsii_struct_bases=[],
        name_mapping={"type_id": "typeId", "value": "value"},
    )
    class OtherNameProperty:
        def __init__(self, *, type_id: builtins.str, value: builtins.str) -> None:
            '''Defines a custom ASN.1 X.400 ``GeneralName`` using an object identifier (OID) and value. The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :param type_id: Specifies an OID.
            :param value: Specifies an OID value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                other_name_property = acmpca.CfnCertificate.OtherNameProperty(
                    type_id="typeId",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__185d5a603add99146f161899be0716184e3739037cdbc9e06031afd19caf3f0c)
                check_type(argname="argument type_id", value=type_id, expected_type=type_hints["type_id"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type_id": type_id,
                "value": value,
            }

        @builtins.property
        def type_id(self) -> builtins.str:
            '''Specifies an OID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html#cfn-acmpca-certificate-othername-typeid
            '''
            result = self._values.get("type_id")
            assert result is not None, "Required property 'type_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Specifies an OID value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html#cfn-acmpca-certificate-othername-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtherNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.PolicyInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cert_policy_id": "certPolicyId",
            "policy_qualifiers": "policyQualifiers",
        },
    )
    class PolicyInformationProperty:
        def __init__(
            self,
            *,
            cert_policy_id: builtins.str,
            policy_qualifiers: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.PolicyQualifierInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines the X.509 ``CertificatePolicies`` extension.

            :param cert_policy_id: Specifies the object identifier (OID) of the certificate policy under which the certificate was issued. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .
            :param policy_qualifiers: Modifies the given ``CertPolicyId`` with a qualifier. AWS Private CA supports the certification practice statement (CPS) qualifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                policy_information_property = acmpca.CfnCertificate.PolicyInformationProperty(
                    cert_policy_id="certPolicyId",
                
                    # the properties below are optional
                    policy_qualifiers=[acmpca.CfnCertificate.PolicyQualifierInfoProperty(
                        policy_qualifier_id="policyQualifierId",
                        qualifier=acmpca.CfnCertificate.QualifierProperty(
                            cps_uri="cpsUri"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a47696af32c3748dd9b1051ce2debc5f3ec7fdc48a09e9f9029a6d820f0af8e4)
                check_type(argname="argument cert_policy_id", value=cert_policy_id, expected_type=type_hints["cert_policy_id"])
                check_type(argname="argument policy_qualifiers", value=policy_qualifiers, expected_type=type_hints["policy_qualifiers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cert_policy_id": cert_policy_id,
            }
            if policy_qualifiers is not None:
                self._values["policy_qualifiers"] = policy_qualifiers

        @builtins.property
        def cert_policy_id(self) -> builtins.str:
            '''Specifies the object identifier (OID) of the certificate policy under which the certificate was issued.

            For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html#cfn-acmpca-certificate-policyinformation-certpolicyid
            '''
            result = self._values.get("cert_policy_id")
            assert result is not None, "Required property 'cert_policy_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def policy_qualifiers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.PolicyQualifierInfoProperty"]]]]:
            '''Modifies the given ``CertPolicyId`` with a qualifier.

            AWS Private CA supports the certification practice statement (CPS) qualifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html#cfn-acmpca-certificate-policyinformation-policyqualifiers
            '''
            result = self._values.get("policy_qualifiers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.PolicyQualifierInfoProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.PolicyQualifierInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_qualifier_id": "policyQualifierId",
            "qualifier": "qualifier",
        },
    )
    class PolicyQualifierInfoProperty:
        def __init__(
            self,
            *,
            policy_qualifier_id: builtins.str,
            qualifier: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.QualifierProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Modifies the ``CertPolicyId`` of a ``PolicyInformation`` object with a qualifier.

            AWS Private CA supports the certification practice statement (CPS) qualifier.

            :param policy_qualifier_id: Identifies the qualifier modifying a ``CertPolicyId`` .
            :param qualifier: Defines the qualifier type. AWS Private CA supports the use of a URI for a CPS qualifier in this field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                policy_qualifier_info_property = acmpca.CfnCertificate.PolicyQualifierInfoProperty(
                    policy_qualifier_id="policyQualifierId",
                    qualifier=acmpca.CfnCertificate.QualifierProperty(
                        cps_uri="cpsUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e19aeaed58965cf242fc88c10b684b75e2f6890f77dbc250ebf2aa2df7d3b3a)
                check_type(argname="argument policy_qualifier_id", value=policy_qualifier_id, expected_type=type_hints["policy_qualifier_id"])
                check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_qualifier_id": policy_qualifier_id,
                "qualifier": qualifier,
            }

        @builtins.property
        def policy_qualifier_id(self) -> builtins.str:
            '''Identifies the qualifier modifying a ``CertPolicyId`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html#cfn-acmpca-certificate-policyqualifierinfo-policyqualifierid
            '''
            result = self._values.get("policy_qualifier_id")
            assert result is not None, "Required property 'policy_qualifier_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def qualifier(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.QualifierProperty"]:
            '''Defines the qualifier type.

            AWS Private CA supports the use of a URI for a CPS qualifier in this field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html#cfn-acmpca-certificate-policyqualifierinfo-qualifier
            '''
            result = self._values.get("qualifier")
            assert result is not None, "Required property 'qualifier' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.QualifierProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyQualifierInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.QualifierProperty",
        jsii_struct_bases=[],
        name_mapping={"cps_uri": "cpsUri"},
    )
    class QualifierProperty:
        def __init__(self, *, cps_uri: builtins.str) -> None:
            '''Defines a ``PolicyInformation`` qualifier.

            AWS Private CA supports the `certification practice statement (CPS) qualifier <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.4>`_ defined in RFC 5280.

            :param cps_uri: Contains a pointer to a certification practice statement (CPS) published by the CA.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-qualifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                qualifier_property = acmpca.CfnCertificate.QualifierProperty(
                    cps_uri="cpsUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87e2b6c419ad9af26a4a909a0bb6138e56e7e5e2cdbe4980a6c99b32094da39a)
                check_type(argname="argument cps_uri", value=cps_uri, expected_type=type_hints["cps_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cps_uri": cps_uri,
            }

        @builtins.property
        def cps_uri(self) -> builtins.str:
            '''Contains a pointer to a certification practice statement (CPS) published by the CA.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-qualifier.html#cfn-acmpca-certificate-qualifier-cpsuri
            '''
            result = self._values.get("cps_uri")
            assert result is not None, "Required property 'cps_uri' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QualifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.SubjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_name": "commonName",
            "country": "country",
            "custom_attributes": "customAttributes",
            "distinguished_name_qualifier": "distinguishedNameQualifier",
            "generation_qualifier": "generationQualifier",
            "given_name": "givenName",
            "initials": "initials",
            "locality": "locality",
            "organization": "organization",
            "organizational_unit": "organizationalUnit",
            "pseudonym": "pseudonym",
            "serial_number": "serialNumber",
            "state": "state",
            "surname": "surname",
            "title": "title",
        },
    )
    class SubjectProperty:
        def __init__(
            self,
            *,
            common_name: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            custom_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificate.CustomAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            distinguished_name_qualifier: typing.Optional[builtins.str] = None,
            generation_qualifier: typing.Optional[builtins.str] = None,
            given_name: typing.Optional[builtins.str] = None,
            initials: typing.Optional[builtins.str] = None,
            locality: typing.Optional[builtins.str] = None,
            organization: typing.Optional[builtins.str] = None,
            organizational_unit: typing.Optional[builtins.str] = None,
            pseudonym: typing.Optional[builtins.str] = None,
            serial_number: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
            surname: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the certificate subject.

            The ``Subject`` field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The ``Subject`` must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate.

            :param common_name: For CA and end-entity certificates in a private PKI, the common name (CN) can be any string within the length limit. Note: In publicly trusted certificates, the common name must be a fully qualified domain name (FQDN) associated with the certificate subject.
            :param country: Two-digit code that specifies the country in which the certificate subject located.
            :param custom_attributes: Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ . .. epigraph:: Custom attributes cannot be used in combination with standard attributes.
            :param distinguished_name_qualifier: Disambiguating information for the certificate subject.
            :param generation_qualifier: Typically a qualifier appended to the name of an individual. Examples include Jr. for junior, Sr. for senior, and III for third.
            :param given_name: First name.
            :param initials: Concatenation that typically contains the first letter of the *GivenName* , the first letter of the middle name if one exists, and the first letter of the *Surname* .
            :param locality: The locality (such as a city or town) in which the certificate subject is located.
            :param organization: Legal name of the organization with which the certificate subject is affiliated.
            :param organizational_unit: A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.
            :param pseudonym: Typically a shortened version of a longer *GivenName* . For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.
            :param serial_number: The certificate serial number.
            :param state: State in which the subject of the certificate is located.
            :param surname: Family name. In the US and the UK, for example, the surname of an individual is ordered last. In Asian cultures the surname is typically ordered first.
            :param title: A title such as Mr. or Ms., which is pre-pended to the name to refer formally to the certificate subject.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                subject_property = acmpca.CfnCertificate.SubjectProperty(
                    common_name="commonName",
                    country="country",
                    custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    distinguished_name_qualifier="distinguishedNameQualifier",
                    generation_qualifier="generationQualifier",
                    given_name="givenName",
                    initials="initials",
                    locality="locality",
                    organization="organization",
                    organizational_unit="organizationalUnit",
                    pseudonym="pseudonym",
                    serial_number="serialNumber",
                    state="state",
                    surname="surname",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a71d5be4c35fb13969e5c8f04109b8b7740570efecc4e8491df2b468a3f6929e)
                check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
                check_type(argname="argument distinguished_name_qualifier", value=distinguished_name_qualifier, expected_type=type_hints["distinguished_name_qualifier"])
                check_type(argname="argument generation_qualifier", value=generation_qualifier, expected_type=type_hints["generation_qualifier"])
                check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
                check_type(argname="argument initials", value=initials, expected_type=type_hints["initials"])
                check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
                check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
                check_type(argname="argument pseudonym", value=pseudonym, expected_type=type_hints["pseudonym"])
                check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if common_name is not None:
                self._values["common_name"] = common_name
            if country is not None:
                self._values["country"] = country
            if custom_attributes is not None:
                self._values["custom_attributes"] = custom_attributes
            if distinguished_name_qualifier is not None:
                self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None:
                self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None:
                self._values["given_name"] = given_name
            if initials is not None:
                self._values["initials"] = initials
            if locality is not None:
                self._values["locality"] = locality
            if organization is not None:
                self._values["organization"] = organization
            if organizational_unit is not None:
                self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None:
                self._values["pseudonym"] = pseudonym
            if serial_number is not None:
                self._values["serial_number"] = serial_number
            if state is not None:
                self._values["state"] = state
            if surname is not None:
                self._values["surname"] = surname
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            '''For CA and end-entity certificates in a private PKI, the common name (CN) can be any string within the length limit.

            Note: In publicly trusted certificates, the common name must be a fully qualified domain name (FQDN) associated with the certificate subject.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-commonname
            '''
            result = self._values.get("common_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            '''Two-digit code that specifies the country in which the certificate subject located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.CustomAttributeProperty"]]]]:
            '''Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            .. epigraph::

               Custom attributes cannot be used in combination with standard attributes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-customattributes
            '''
            result = self._values.get("custom_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificate.CustomAttributeProperty"]]]], result)

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
            '''Disambiguating information for the certificate subject.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-distinguishednamequalifier
            '''
            result = self._values.get("distinguished_name_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[builtins.str]:
            '''Typically a qualifier appended to the name of an individual.

            Examples include Jr. for junior, Sr. for senior, and III for third.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-generationqualifier
            '''
            result = self._values.get("generation_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def given_name(self) -> typing.Optional[builtins.str]:
            '''First name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-givenname
            '''
            result = self._values.get("given_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def initials(self) -> typing.Optional[builtins.str]:
            '''Concatenation that typically contains the first letter of the *GivenName* , the first letter of the middle name if one exists, and the first letter of the *Surname* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-initials
            '''
            result = self._values.get("initials")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locality(self) -> typing.Optional[builtins.str]:
            '''The locality (such as a city or town) in which the certificate subject is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-locality
            '''
            result = self._values.get("locality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organization(self) -> typing.Optional[builtins.str]:
            '''Legal name of the organization with which the certificate subject is affiliated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-organization
            '''
            result = self._values.get("organization")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit(self) -> typing.Optional[builtins.str]:
            '''A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-organizationalunit
            '''
            result = self._values.get("organizational_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pseudonym(self) -> typing.Optional[builtins.str]:
            '''Typically a shortened version of a longer *GivenName* .

            For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-pseudonym
            '''
            result = self._values.get("pseudonym")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def serial_number(self) -> typing.Optional[builtins.str]:
            '''The certificate serial number.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-serialnumber
            '''
            result = self._values.get("serial_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''State in which the subject of the certificate is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def surname(self) -> typing.Optional[builtins.str]:
            '''Family name.

            In the US and the UK, for example, the surname of an individual is ordered last. In Asian cultures the surname is typically ordered first.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-surname
            '''
            result = self._values.get("surname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''A title such as Mr.

            or Ms., which is pre-pended to the name to refer formally to the certificate subject.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ValidityProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ValidityProperty:
        def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
            '''Length of time for which the certificate issued by your private certificate authority (CA), or by the private CA itself, is valid in days, months, or years.

            You can issue a certificate by calling the ``IssueCertificate`` operation.

            :param type: Specifies whether the ``Value`` parameter represents days, months, or years.
            :param value: A long integer interpreted according to the value of ``Type`` , below.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                validity_property = acmpca.CfnCertificate.ValidityProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80efff0e667ab1ac7f8e1a2a13dd9072b7281cb46b7c2d45bf401dd9226116d4)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''Specifies whether the ``Value`` parameter represents days, months, or years.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> jsii.Number:
            '''A long integer interpreted according to the value of ``Type`` , below.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCertificateAuthority(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority",
):
    '''A CloudFormation ``AWS::ACMPCA::CertificateAuthority``.

    Use the ``AWS::ACMPCA::CertificateAuthority`` resource to create a private CA. Once the CA exists, you can use the ``AWS::ACMPCA::Certificate`` resource to issue a new CA certificate. Alternatively, you can issue a CA certificate using an on-premises CA, and then use the ``AWS::ACMPCA::CertificateAuthorityActivation`` resource to import the new CA certificate and activate the CA.
    .. epigraph::

       Before removing a ``AWS::ACMPCA::CertificateAuthority`` resource from the CloudFormation stack, disable the affected CA. Otherwise, the action will fail. You can disable the CA by removing its associated ``AWS::ACMPCA::CertificateAuthorityActivation`` resource from CloudFormation.

    :cloudformationResource: AWS::ACMPCA::CertificateAuthority
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
    :exampleMetadata: infused

    Example::

        cfn_certificate_authority = acmpca.CfnCertificateAuthority(self, "CA",
            type="ROOT",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            subject=acmpca.CfnCertificateAuthority.SubjectProperty(
                country="US",
                organization="string",
                organizational_unit="string",
                distinguished_name_qualifier="string",
                state="string",
                common_name="123",
                serial_number="string",
                locality="string",
                title="string",
                surname="string",
                given_name="string",
                initials="DG",
                pseudonym="string",
                generation_qualifier="DBG"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.SubjectProperty", typing.Dict[builtins.str, typing.Any]]],
        type: builtins.str,
        csr_extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.CsrExtensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        key_storage_security_standard: typing.Optional[builtins.str] = None,
        revocation_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.RevocationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        usage_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ACMPCA::CertificateAuthority``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_algorithm: Type of the public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate. When you create a subordinate CA, you must use a key algorithm supported by the parent CA.
        :param signing_algorithm: Name of the algorithm your private CA uses to sign certificate requests. This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign certificates when they are issued.
        :param subject: Structure that contains X.500 distinguished name information for your private CA.
        :param type: Type of your private CA.
        :param csr_extensions: Specifies information to be added to the extension section of the certificate signing request (CSR).
        :param key_storage_security_standard: Specifies a cryptographic key management compliance standard used for handling CA keys. Default: FIPS_140_2_LEVEL_3_OR_HIGHER .. epigraph:: Some AWS Regions do not support the default. When creating a CA in these Regions, you must provide ``FIPS_140_2_LEVEL_2_OR_HIGHER`` as the argument for ``KeyStorageSecurityStandard`` . Failure to do this results in an ``InvalidArgsException`` with the message, "A certificate authority cannot be created in this region with the specified security standard." For information about security standard support in various Regions, see `Storage and security compliance of AWS Private CA private keys <https://docs.aws.amazon.com/privateca/latest/userguide/data-protection.html#private-keys>`_ .
        :param revocation_configuration: Certificate revocation information used by the `CreateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthority.html>`_ and `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ actions. Your private certificate authority (CA) can configure Online Certificate Status Protocol (OCSP) support and/or maintain a certificate revocation list (CRL). OCSP returns validation information about certificates as requested by clients, and a CRL contains an updated list of certificates revoked by your CA. For more information, see `RevokeCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_RevokeCertificate.html>`_ in the *AWS Private CA API Reference* and `Setting up a certificate revocation method <https://docs.aws.amazon.com/privateca/latest/userguide/revocation-setup.html>`_ in the *AWS Private CA User Guide* . .. epigraph:: The following requirements apply to revocation configurations. - A configuration disabling CRLs or OCSP must contain only the ``Enabled=False`` parameter, and will fail if other parameters such as ``CustomCname`` or ``ExpirationInDays`` are included. - In a CRL configuration, the ``S3BucketName`` parameter must conform to the `Amazon S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ . - A configuration containing a custom Canonical Name (CNAME) parameter for CRLs or OCSP must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in a CNAME. - In a CRL or OCSP configuration, the value of a CNAME parameter must not include a protocol prefix such as "http://" or "https://".
        :param tags: Key-value pairs that will be attached to the new private CA. You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see `Controlling Access Using IAM Tags <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html>`_ .
        :param usage_mode: Specifies whether the CA issues general-purpose certificates that typically require a revocation mechanism, or short-lived certificates that may optionally omit revocation because they expire quickly. Short-lived certificate validity is limited to seven days. The default value is GENERAL_PURPOSE.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904b84401209c2e616777422173fb01eca51f0f550133e510c4934900062d21b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCertificateAuthorityProps(
            key_algorithm=key_algorithm,
            signing_algorithm=signing_algorithm,
            subject=subject,
            type=type,
            csr_extensions=csr_extensions,
            key_storage_security_standard=key_storage_security_standard,
            revocation_configuration=revocation_configuration,
            tags=tags,
            usage_mode=usage_mode,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5049dbbe41c10b4287e548826cbb537cb872060550a25e1e231a8fbf15ac37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b81f5dd8f7bca59193588bf155cc66ddf4f04d41f758765dd1316eb798b13336)
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
        '''The Amazon Resource Name (ARN) for the private CA that issued the certificate.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCertificateSigningRequest")
    def attr_certificate_signing_request(self) -> builtins.str:
        '''The Base64 PEM-encoded certificate signing request (CSR) for your certificate authority certificate.

        :cloudformationAttribute: CertificateSigningRequest
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCertificateSigningRequest"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Key-value pairs that will be attached to the new private CA.

        You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see `Controlling Access Using IAM Tags <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        '''Type of the public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate.

        When you create a subordinate CA, you must use a key algorithm supported by the parent CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        '''
        return typing.cast(builtins.str, jsii.get(self, "keyAlgorithm"))

    @key_algorithm.setter
    def key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eea6ad2d46b1584a705dcbda5b5879e737056c269531a0ba433f219c10a08c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        '''Name of the algorithm your private CA uses to sign certificate requests.

        This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign certificates when they are issued.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        '''
        return typing.cast(builtins.str, jsii.get(self, "signingAlgorithm"))

    @signing_algorithm.setter
    def signing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321aa7b8346c5f938fad1275eb85ed3a3aedcf7a83a987c9d26ae159294c7bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.SubjectProperty"]:
        '''Structure that contains X.500 distinguished name information for your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.SubjectProperty"], jsii.get(self, "subject"))

    @subject.setter
    def subject(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.SubjectProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c844f3587ad1b3cc5aaf83bc47dcfcfbcfe13cf3dfcd55259c1cb22780f0ee0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Type of your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754bb5ab5b1abf7ee53fa0951241546c8e8bd51bd160b33cbdfd78e63153b779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="csrExtensions")
    def csr_extensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.CsrExtensionsProperty"]]:
        '''Specifies information to be added to the extension section of the certificate signing request (CSR).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-csrextensions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.CsrExtensionsProperty"]], jsii.get(self, "csrExtensions"))

    @csr_extensions.setter
    def csr_extensions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.CsrExtensionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6b5e5d60b1095a51b9f6a4401bdc80608aab99f9f67f0b38a654292eb7e95c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "csrExtensions", value)

    @builtins.property
    @jsii.member(jsii_name="keyStorageSecurityStandard")
    def key_storage_security_standard(self) -> typing.Optional[builtins.str]:
        '''Specifies a cryptographic key management compliance standard used for handling CA keys.

        Default: FIPS_140_2_LEVEL_3_OR_HIGHER
        .. epigraph::

           Some AWS Regions do not support the default. When creating a CA in these Regions, you must provide ``FIPS_140_2_LEVEL_2_OR_HIGHER`` as the argument for ``KeyStorageSecurityStandard`` . Failure to do this results in an ``InvalidArgsException`` with the message, "A certificate authority cannot be created in this region with the specified security standard."

           For information about security standard support in various Regions, see `Storage and security compliance of AWS Private CA private keys <https://docs.aws.amazon.com/privateca/latest/userguide/data-protection.html#private-keys>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keystoragesecuritystandard
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyStorageSecurityStandard"))

    @key_storage_security_standard.setter
    def key_storage_security_standard(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c600bd111dfb393965c27e306fa7bac53607f8bce97ed3864b1970d236a2e705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyStorageSecurityStandard", value)

    @builtins.property
    @jsii.member(jsii_name="revocationConfiguration")
    def revocation_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]]:
        '''Certificate revocation information used by the `CreateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthority.html>`_ and `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ actions. Your private certificate authority (CA) can configure Online Certificate Status Protocol (OCSP) support and/or maintain a certificate revocation list (CRL). OCSP returns validation information about certificates as requested by clients, and a CRL contains an updated list of certificates revoked by your CA. For more information, see `RevokeCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_RevokeCertificate.html>`_ in the *AWS Private CA API Reference* and `Setting up a certificate revocation method <https://docs.aws.amazon.com/privateca/latest/userguide/revocation-setup.html>`_ in the *AWS Private CA User Guide* .

        .. epigraph::

           The following requirements apply to revocation configurations.

           - A configuration disabling CRLs or OCSP must contain only the ``Enabled=False`` parameter, and will fail if other parameters such as ``CustomCname`` or ``ExpirationInDays`` are included.
           - In a CRL configuration, the ``S3BucketName`` parameter must conform to the `Amazon S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .
           - A configuration containing a custom Canonical Name (CNAME) parameter for CRLs or OCSP must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in a CNAME.
           - In a CRL or OCSP configuration, the value of a CNAME parameter must not include a protocol prefix such as "http://" or "https://".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]], jsii.get(self, "revocationConfiguration"))

    @revocation_configuration.setter
    def revocation_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650ad4c1e8b020232753ad4079ae422710c0a23c449258c8d86312f51f136c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revocationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="usageMode")
    def usage_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the CA issues general-purpose certificates that typically require a revocation mechanism, or short-lived certificates that may optionally omit revocation because they expire quickly.

        Short-lived certificate validity is limited to seven days.

        The default value is GENERAL_PURPOSE.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-usagemode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageMode"))

    @usage_mode.setter
    def usage_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8fe2bbc91b58f7e370945ee64cb7f1ec42f41e5d548cb7c8df426697e10798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usageMode", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.AccessDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_location": "accessLocation",
            "access_method": "accessMethod",
        },
    )
    class AccessDescriptionProperty:
        def __init__(
            self,
            *,
            access_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.GeneralNameProperty", typing.Dict[builtins.str, typing.Any]]],
            access_method: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.AccessMethodProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Provides access information used by the ``authorityInfoAccess`` and ``subjectInfoAccess`` extensions described in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ .

            :param access_location: The location of ``AccessDescription`` information.
            :param access_method: The type and format of ``AccessDescription`` information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                access_description_property = acmpca.CfnCertificateAuthority.AccessDescriptionProperty(
                    access_location=acmpca.CfnCertificateAuthority.GeneralNameProperty(
                        directory_name=acmpca.CfnCertificateAuthority.SubjectProperty(
                            common_name="commonName",
                            country="country",
                            custom_attributes=[acmpca.CfnCertificateAuthority.CustomAttributeProperty(
                                object_identifier="objectIdentifier",
                                value="value"
                            )],
                            distinguished_name_qualifier="distinguishedNameQualifier",
                            generation_qualifier="generationQualifier",
                            given_name="givenName",
                            initials="initials",
                            locality="locality",
                            organization="organization",
                            organizational_unit="organizationalUnit",
                            pseudonym="pseudonym",
                            serial_number="serialNumber",
                            state="state",
                            surname="surname",
                            title="title"
                        ),
                        dns_name="dnsName",
                        edi_party_name=acmpca.CfnCertificateAuthority.EdiPartyNameProperty(
                            name_assigner="nameAssigner",
                            party_name="partyName"
                        ),
                        ip_address="ipAddress",
                        other_name=acmpca.CfnCertificateAuthority.OtherNameProperty(
                            type_id="typeId",
                            value="value"
                        ),
                        registered_id="registeredId",
                        rfc822_name="rfc822Name",
                        uniform_resource_identifier="uniformResourceIdentifier"
                    ),
                    access_method=acmpca.CfnCertificateAuthority.AccessMethodProperty(
                        access_method_type="accessMethodType",
                        custom_object_identifier="customObjectIdentifier"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10f59d7d46e13f4f7d3ab4d7b78d637dae1a7a3c5c254abceffc0664973d5cc8)
                check_type(argname="argument access_location", value=access_location, expected_type=type_hints["access_location"])
                check_type(argname="argument access_method", value=access_method, expected_type=type_hints["access_method"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "access_location": access_location,
                "access_method": access_method,
            }

        @builtins.property
        def access_location(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.GeneralNameProperty"]:
            '''The location of ``AccessDescription`` information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html#cfn-acmpca-certificateauthority-accessdescription-accesslocation
            '''
            result = self._values.get("access_location")
            assert result is not None, "Required property 'access_location' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.GeneralNameProperty"], result)

        @builtins.property
        def access_method(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.AccessMethodProperty"]:
            '''The type and format of ``AccessDescription`` information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html#cfn-acmpca-certificateauthority-accessdescription-accessmethod
            '''
            result = self._values.get("access_method")
            assert result is not None, "Required property 'access_method' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.AccessMethodProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.AccessMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_method_type": "accessMethodType",
            "custom_object_identifier": "customObjectIdentifier",
        },
    )
    class AccessMethodProperty:
        def __init__(
            self,
            *,
            access_method_type: typing.Optional[builtins.str] = None,
            custom_object_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the type and format of extension access.

            Only one of ``CustomObjectIdentifier`` or ``AccessMethodType`` may be provided. Providing both results in ``InvalidArgsException`` .

            :param access_method_type: Specifies the ``AccessMethod`` .
            :param custom_object_identifier: An object identifier (OID) specifying the ``AccessMethod`` . The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                access_method_property = acmpca.CfnCertificateAuthority.AccessMethodProperty(
                    access_method_type="accessMethodType",
                    custom_object_identifier="customObjectIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4df046a28f007886432b8640a92b8c310bf2c7f6400379b866b023082fbaad9f)
                check_type(argname="argument access_method_type", value=access_method_type, expected_type=type_hints["access_method_type"])
                check_type(argname="argument custom_object_identifier", value=custom_object_identifier, expected_type=type_hints["custom_object_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_method_type is not None:
                self._values["access_method_type"] = access_method_type
            if custom_object_identifier is not None:
                self._values["custom_object_identifier"] = custom_object_identifier

        @builtins.property
        def access_method_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the ``AccessMethod`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html#cfn-acmpca-certificateauthority-accessmethod-accessmethodtype
            '''
            result = self._values.get("access_method_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_object_identifier(self) -> typing.Optional[builtins.str]:
            '''An object identifier (OID) specifying the ``AccessMethod`` .

            The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html#cfn-acmpca-certificateauthority-accessmethod-customobjectidentifier
            '''
            result = self._values.get("custom_object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.CrlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_cname": "customCname",
            "enabled": "enabled",
            "expiration_in_days": "expirationInDays",
            "s3_bucket_name": "s3BucketName",
            "s3_object_acl": "s3ObjectAcl",
        },
    )
    class CrlConfigurationProperty:
        def __init__(
            self,
            *,
            custom_cname: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_object_acl: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configuration information for a certificate revocation list (CRL).

            Your private certificate authority (CA) creates base CRLs. Delta CRLs are not supported. You can enable CRLs for your new or an existing private CA by setting the *Enabled* parameter to ``true`` . Your private CA writes CRLs to an S3 bucket that you specify in the *S3BucketName* parameter. You can hide the name of your bucket by specifying a value for the *CustomCname* parameter. Your private CA copies the CNAME or the S3 bucket name to the *CRL Distribution Points* extension of each certificate it issues. Your S3 bucket policy must give write permission to AWS Private CA.

            AWS Private CA assets that are stored in Amazon S3 can be protected with encryption. For more information, see `Encrypting Your CRLs <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#crl-encryption>`_ .

            Your private CA uses the value in the *ExpirationInDays* parameter to calculate the *nextUpdate* field in the CRL. The CRL is refreshed prior to a certificate's expiration date or when a certificate is revoked. When a certificate is revoked, it appears in the CRL until the certificate expires, and then in one additional CRL after expiration, and it always appears in the audit report.

            A CRL is typically updated approximately 30 minutes after a certificate is revoked. If for any reason a CRL update fails, AWS Private CA makes further attempts every 15 minutes.

            CRLs contain the following fields:

            - *Version* : The current version number defined in RFC 5280 is V2. The integer value is 0x1.
            - *Signature Algorithm* : The name of the algorithm used to sign the CRL.
            - *Issuer* : The X.500 distinguished name of your private CA that issued the CRL.
            - *Last Update* : The issue date and time of this CRL.
            - *Next Update* : The day and time by which the next CRL will be issued.
            - *Revoked Certificates* : List of revoked certificates. Each list item contains the following information.
            - *Serial Number* : The serial number, in hexadecimal format, of the revoked certificate.
            - *Revocation Date* : Date and time the certificate was revoked.
            - *CRL Entry Extensions* : Optional extensions for the CRL entry.
            - *X509v3 CRL Reason Code* : Reason the certificate was revoked.
            - *CRL Extensions* : Optional extensions for the CRL.
            - *X509v3 Authority Key Identifier* : Identifies the public key associated with the private key used to sign the certificate.
            - *X509v3 CRL Number:* : Decimal sequence number for the CRL.
            - *Signature Algorithm* : Algorithm used by your private CA to sign the CRL.
            - *Signature Value* : Signature computed over the CRL.

            Certificate revocation lists created by AWS Private CA are DER-encoded. You can use the following OpenSSL command to list a CRL.

            ``openssl crl -inform DER -text -in *crl_path* -noout``

            For more information, see `Planning a certificate revocation list (CRL) <https://docs.aws.amazon.com/privateca/latest/userguide/crl-planning.html>`_ in the *AWS Private Certificate Authority User Guide*

            :param custom_cname: Name inserted into the certificate *CRL Distribution Points* extension that enables the use of an alias for the CRL distribution point. Use this value if you don't want the name of your S3 bucket to be public. .. epigraph:: The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".
            :param enabled: Boolean value that specifies whether certificate revocation lists (CRLs) are enabled. You can use this value to enable certificate revocation for a new CA when you call the ``CreateCertificateAuthority`` operation or for an existing CA when you call the ``UpdateCertificateAuthority`` operation.
            :param expiration_in_days: Validity period of the CRL in days.
            :param s3_bucket_name: Name of the S3 bucket that contains the CRL. If you do not provide a value for the *CustomCname* argument, the name of your S3 bucket is placed into the *CRL Distribution Points* extension of the issued certificate. You can change the name of your bucket by calling the `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ operation. You must specify a `bucket policy <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-policies>`_ that allows AWS Private CA to write the CRL to your bucket. .. epigraph:: The ``S3BucketName`` parameter must conform to the `S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .
            :param s3_object_acl: Determines whether the CRL will be publicly readable or privately held in the CRL Amazon S3 bucket. If you choose PUBLIC_READ, the CRL will be accessible over the public internet. If you choose BUCKET_OWNER_FULL_CONTROL, only the owner of the CRL S3 bucket can access the CRL, and your PKI clients may need an alternative method of access. If no value is specified, the default is PUBLIC_READ. *Note:* This default can cause CA creation to fail in some circumstances. If you have have enabled the Block Public Access (BPA) feature in your S3 account, then you must specify the value of this parameter as ``BUCKET_OWNER_FULL_CONTROL`` , and not doing so results in an error. If you have disabled BPA in S3, then you can specify either ``BUCKET_OWNER_FULL_CONTROL`` or ``PUBLIC_READ`` as the value. For more information, see `Blocking public access to the S3 bucket <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-bpa>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                crl_configuration_property = acmpca.CfnCertificateAuthority.CrlConfigurationProperty(
                    custom_cname="customCname",
                    enabled=False,
                    expiration_in_days=123,
                    s3_bucket_name="s3BucketName",
                    s3_object_acl="s3ObjectAcl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d793b80e787d87c0baa48202af901a7bbf05fcd4e7e3514816b3e5a121f5349)
                check_type(argname="argument custom_cname", value=custom_cname, expected_type=type_hints["custom_cname"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument expiration_in_days", value=expiration_in_days, expected_type=type_hints["expiration_in_days"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_object_acl", value=s3_object_acl, expected_type=type_hints["s3_object_acl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_cname is not None:
                self._values["custom_cname"] = custom_cname
            if enabled is not None:
                self._values["enabled"] = enabled
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_object_acl is not None:
                self._values["s3_object_acl"] = s3_object_acl

        @builtins.property
        def custom_cname(self) -> typing.Optional[builtins.str]:
            '''Name inserted into the certificate *CRL Distribution Points* extension that enables the use of an alias for the CRL distribution point.

            Use this value if you don't want the name of your S3 bucket to be public.
            .. epigraph::

               The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-customcname
            '''
            result = self._values.get("custom_cname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Boolean value that specifies whether certificate revocation lists (CRLs) are enabled.

            You can use this value to enable certificate revocation for a new CA when you call the ``CreateCertificateAuthority`` operation or for an existing CA when you call the ``UpdateCertificateAuthority`` operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''Validity period of the CRL in days.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-expirationindays
            '''
            result = self._values.get("expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''Name of the S3 bucket that contains the CRL.

            If you do not provide a value for the *CustomCname* argument, the name of your S3 bucket is placed into the *CRL Distribution Points* extension of the issued certificate. You can change the name of your bucket by calling the `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ operation. You must specify a `bucket policy <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-policies>`_ that allows AWS Private CA to write the CRL to your bucket.
            .. epigraph::

               The ``S3BucketName`` parameter must conform to the `S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_acl(self) -> typing.Optional[builtins.str]:
            '''Determines whether the CRL will be publicly readable or privately held in the CRL Amazon S3 bucket.

            If you choose PUBLIC_READ, the CRL will be accessible over the public internet. If you choose BUCKET_OWNER_FULL_CONTROL, only the owner of the CRL S3 bucket can access the CRL, and your PKI clients may need an alternative method of access.

            If no value is specified, the default is PUBLIC_READ.

            *Note:* This default can cause CA creation to fail in some circumstances. If you have have enabled the Block Public Access (BPA) feature in your S3 account, then you must specify the value of this parameter as ``BUCKET_OWNER_FULL_CONTROL`` , and not doing so results in an error. If you have disabled BPA in S3, then you can specify either ``BUCKET_OWNER_FULL_CONTROL`` or ``PUBLIC_READ`` as the value.

            For more information, see `Blocking public access to the S3 bucket <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-bpa>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-s3objectacl
            '''
            result = self._values.get("s3_object_acl")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.CsrExtensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key_usage": "keyUsage",
            "subject_information_access": "subjectInformationAccess",
        },
    )
    class CsrExtensionsProperty:
        def __init__(
            self,
            *,
            key_usage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.KeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject_information_access: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.AccessDescriptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the certificate extensions to be added to the certificate signing request (CSR).

            :param key_usage: Indicates the purpose of the certificate and of the key contained in the certificate.
            :param subject_information_access: For CA certificates, provides a path to additional information pertaining to the CA, such as revocation and policy. For more information, see `Subject Information Access <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.2.2>`_ in RFC 5280.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                csr_extensions_property = acmpca.CfnCertificateAuthority.CsrExtensionsProperty(
                    key_usage=acmpca.CfnCertificateAuthority.KeyUsageProperty(
                        crl_sign=False,
                        data_encipherment=False,
                        decipher_only=False,
                        digital_signature=False,
                        encipher_only=False,
                        key_agreement=False,
                        key_cert_sign=False,
                        key_encipherment=False,
                        non_repudiation=False
                    ),
                    subject_information_access=[acmpca.CfnCertificateAuthority.AccessDescriptionProperty(
                        access_location=acmpca.CfnCertificateAuthority.GeneralNameProperty(
                            directory_name=acmpca.CfnCertificateAuthority.SubjectProperty(
                                common_name="commonName",
                                country="country",
                                custom_attributes=[acmpca.CfnCertificateAuthority.CustomAttributeProperty(
                                    object_identifier="objectIdentifier",
                                    value="value"
                                )],
                                distinguished_name_qualifier="distinguishedNameQualifier",
                                generation_qualifier="generationQualifier",
                                given_name="givenName",
                                initials="initials",
                                locality="locality",
                                organization="organization",
                                organizational_unit="organizationalUnit",
                                pseudonym="pseudonym",
                                serial_number="serialNumber",
                                state="state",
                                surname="surname",
                                title="title"
                            ),
                            dns_name="dnsName",
                            edi_party_name=acmpca.CfnCertificateAuthority.EdiPartyNameProperty(
                                name_assigner="nameAssigner",
                                party_name="partyName"
                            ),
                            ip_address="ipAddress",
                            other_name=acmpca.CfnCertificateAuthority.OtherNameProperty(
                                type_id="typeId",
                                value="value"
                            ),
                            registered_id="registeredId",
                            rfc822_name="rfc822Name",
                            uniform_resource_identifier="uniformResourceIdentifier"
                        ),
                        access_method=acmpca.CfnCertificateAuthority.AccessMethodProperty(
                            access_method_type="accessMethodType",
                            custom_object_identifier="customObjectIdentifier"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1420c61eadb790f5013cd1762889a48d1e024b3e94a09891e9bbf177280d33d2)
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
                check_type(argname="argument subject_information_access", value=subject_information_access, expected_type=type_hints["subject_information_access"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_usage is not None:
                self._values["key_usage"] = key_usage
            if subject_information_access is not None:
                self._values["subject_information_access"] = subject_information_access

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.KeyUsageProperty"]]:
            '''Indicates the purpose of the certificate and of the key contained in the certificate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html#cfn-acmpca-certificateauthority-csrextensions-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.KeyUsageProperty"]], result)

        @builtins.property
        def subject_information_access(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.AccessDescriptionProperty"]]]]:
            '''For CA certificates, provides a path to additional information pertaining to the CA, such as revocation and policy.

            For more information, see `Subject Information Access <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.2.2>`_ in RFC 5280.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html#cfn-acmpca-certificateauthority-csrextensions-subjectinformationaccess
            '''
            result = self._values.get("subject_information_access")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.AccessDescriptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsrExtensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.CustomAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"object_identifier": "objectIdentifier", "value": "value"},
    )
    class CustomAttributeProperty:
        def __init__(
            self,
            *,
            object_identifier: builtins.str,
            value: builtins.str,
        ) -> None:
            '''Defines the X.500 relative distinguished name (RDN).

            :param object_identifier: Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).
            :param value: Specifies the attribute value of relative distinguished name (RDN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-customattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                custom_attribute_property = acmpca.CfnCertificateAuthority.CustomAttributeProperty(
                    object_identifier="objectIdentifier",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c538e42b2ad1438a491acc1835d642cb8791ba57e3c00217e3fb810021ef447a)
                check_type(argname="argument object_identifier", value=object_identifier, expected_type=type_hints["object_identifier"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object_identifier": object_identifier,
                "value": value,
            }

        @builtins.property
        def object_identifier(self) -> builtins.str:
            '''Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-customattribute.html#cfn-acmpca-certificateauthority-customattribute-objectidentifier
            '''
            result = self._values.get("object_identifier")
            assert result is not None, "Required property 'object_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Specifies the attribute value of relative distinguished name (RDN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-customattribute.html#cfn-acmpca-certificateauthority-customattribute-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.EdiPartyNameProperty",
        jsii_struct_bases=[],
        name_mapping={"name_assigner": "nameAssigner", "party_name": "partyName"},
    )
    class EdiPartyNameProperty:
        def __init__(
            self,
            *,
            name_assigner: builtins.str,
            party_name: builtins.str,
        ) -> None:
            '''Describes an Electronic Data Interchange (EDI) entity as described in as defined in `Subject Alternative Name <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ in RFC 5280.

            :param name_assigner: Specifies the name assigner.
            :param party_name: Specifies the party name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                edi_party_name_property = acmpca.CfnCertificateAuthority.EdiPartyNameProperty(
                    name_assigner="nameAssigner",
                    party_name="partyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de69eb9c0b68be1be94126679d147f5ea519215dd4c88c6308c0e64dbea75649)
                check_type(argname="argument name_assigner", value=name_assigner, expected_type=type_hints["name_assigner"])
                check_type(argname="argument party_name", value=party_name, expected_type=type_hints["party_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name_assigner": name_assigner,
                "party_name": party_name,
            }

        @builtins.property
        def name_assigner(self) -> builtins.str:
            '''Specifies the name assigner.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html#cfn-acmpca-certificateauthority-edipartyname-nameassigner
            '''
            result = self._values.get("name_assigner")
            assert result is not None, "Required property 'name_assigner' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def party_name(self) -> builtins.str:
            '''Specifies the party name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html#cfn-acmpca-certificateauthority-edipartyname-partyname
            '''
            result = self._values.get("party_name")
            assert result is not None, "Required property 'party_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiPartyNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.GeneralNameProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "dns_name": "dnsName",
            "edi_party_name": "ediPartyName",
            "ip_address": "ipAddress",
            "other_name": "otherName",
            "registered_id": "registeredId",
            "rfc822_name": "rfc822Name",
            "uniform_resource_identifier": "uniformResourceIdentifier",
        },
    )
    class GeneralNameProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.SubjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dns_name: typing.Optional[builtins.str] = None,
            edi_party_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.EdiPartyNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_address: typing.Optional[builtins.str] = None,
            other_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.OtherNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            registered_id: typing.Optional[builtins.str] = None,
            rfc822_name: typing.Optional[builtins.str] = None,
            uniform_resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an ASN.1 X.400 ``GeneralName`` as defined in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ . Only one of the following naming options should be provided. Providing more than one option results in an ``InvalidArgsException`` error.

            :param directory_name: Contains information about the certificate subject. The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.
            :param dns_name: Represents ``GeneralName`` as a DNS name.
            :param edi_party_name: Represents ``GeneralName`` as an ``EdiPartyName`` object.
            :param ip_address: Represents ``GeneralName`` as an IPv4 or IPv6 address.
            :param other_name: Represents ``GeneralName`` using an ``OtherName`` object.
            :param registered_id: Represents ``GeneralName`` as an object identifier (OID).
            :param rfc822_name: Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.
            :param uniform_resource_identifier: Represents ``GeneralName`` as a URI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                general_name_property = acmpca.CfnCertificateAuthority.GeneralNameProperty(
                    directory_name=acmpca.CfnCertificateAuthority.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca.CfnCertificateAuthority.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    ),
                    dns_name="dnsName",
                    edi_party_name=acmpca.CfnCertificateAuthority.EdiPartyNameProperty(
                        name_assigner="nameAssigner",
                        party_name="partyName"
                    ),
                    ip_address="ipAddress",
                    other_name=acmpca.CfnCertificateAuthority.OtherNameProperty(
                        type_id="typeId",
                        value="value"
                    ),
                    registered_id="registeredId",
                    rfc822_name="rfc822Name",
                    uniform_resource_identifier="uniformResourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f93aeef42c4138b4e40fa52678f274b9aa3f140335402de29b5a8335b46ece67)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
                check_type(argname="argument edi_party_name", value=edi_party_name, expected_type=type_hints["edi_party_name"])
                check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
                check_type(argname="argument other_name", value=other_name, expected_type=type_hints["other_name"])
                check_type(argname="argument registered_id", value=registered_id, expected_type=type_hints["registered_id"])
                check_type(argname="argument rfc822_name", value=rfc822_name, expected_type=type_hints["rfc822_name"])
                check_type(argname="argument uniform_resource_identifier", value=uniform_resource_identifier, expected_type=type_hints["uniform_resource_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if edi_party_name is not None:
                self._values["edi_party_name"] = edi_party_name
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if other_name is not None:
                self._values["other_name"] = other_name
            if registered_id is not None:
                self._values["registered_id"] = registered_id
            if rfc822_name is not None:
                self._values["rfc822_name"] = rfc822_name
            if uniform_resource_identifier is not None:
                self._values["uniform_resource_identifier"] = uniform_resource_identifier

        @builtins.property
        def directory_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.SubjectProperty"]]:
            '''Contains information about the certificate subject.

            The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.SubjectProperty"]], result)

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a DNS name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-dnsname
            '''
            result = self._values.get("dns_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def edi_party_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.EdiPartyNameProperty"]]:
            '''Represents ``GeneralName`` as an ``EdiPartyName`` object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-edipartyname
            '''
            result = self._values.get("edi_party_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.EdiPartyNameProperty"]], result)

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an IPv4 or IPv6 address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-ipaddress
            '''
            result = self._values.get("ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def other_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.OtherNameProperty"]]:
            '''Represents ``GeneralName`` using an ``OtherName`` object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-othername
            '''
            result = self._values.get("other_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.OtherNameProperty"]], result)

        @builtins.property
        def registered_id(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an object identifier (OID).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-registeredid
            '''
            result = self._values.get("registered_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rfc822_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-rfc822name
            '''
            result = self._values.get("rfc822_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a URI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-uniformresourceidentifier
            '''
            result = self._values.get("uniform_resource_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.KeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_sign": "crlSign",
            "data_encipherment": "dataEncipherment",
            "decipher_only": "decipherOnly",
            "digital_signature": "digitalSignature",
            "encipher_only": "encipherOnly",
            "key_agreement": "keyAgreement",
            "key_cert_sign": "keyCertSign",
            "key_encipherment": "keyEncipherment",
            "non_repudiation": "nonRepudiation",
        },
    )
    class KeyUsageProperty:
        def __init__(
            self,
            *,
            crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Defines one or more purposes for which the key contained in the certificate can be used.

            Default value for each option is false.

            :param crl_sign: Key can be used to sign CRLs.
            :param data_encipherment: Key can be used to decipher data.
            :param decipher_only: Key can be used only to decipher data.
            :param digital_signature: Key can be used for digital signing.
            :param encipher_only: Key can be used only to encipher data.
            :param key_agreement: Key can be used in a key-agreement protocol.
            :param key_cert_sign: Key can be used to sign certificates.
            :param key_encipherment: Key can be used to encipher data.
            :param non_repudiation: Key can be used for non-repudiation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                key_usage_property = acmpca.CfnCertificateAuthority.KeyUsageProperty(
                    crl_sign=False,
                    data_encipherment=False,
                    decipher_only=False,
                    digital_signature=False,
                    encipher_only=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    key_encipherment=False,
                    non_repudiation=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b354c1d4587ea02f628b419327f22a622798e5aff2b25dcd89944266ffa48737)
                check_type(argname="argument crl_sign", value=crl_sign, expected_type=type_hints["crl_sign"])
                check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
                check_type(argname="argument decipher_only", value=decipher_only, expected_type=type_hints["decipher_only"])
                check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
                check_type(argname="argument encipher_only", value=encipher_only, expected_type=type_hints["encipher_only"])
                check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
                check_type(argname="argument key_cert_sign", value=key_cert_sign, expected_type=type_hints["key_cert_sign"])
                check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
                check_type(argname="argument non_repudiation", value=non_repudiation, expected_type=type_hints["non_repudiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crl_sign is not None:
                self._values["crl_sign"] = crl_sign
            if data_encipherment is not None:
                self._values["data_encipherment"] = data_encipherment
            if decipher_only is not None:
                self._values["decipher_only"] = decipher_only
            if digital_signature is not None:
                self._values["digital_signature"] = digital_signature
            if encipher_only is not None:
                self._values["encipher_only"] = encipher_only
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if key_cert_sign is not None:
                self._values["key_cert_sign"] = key_cert_sign
            if key_encipherment is not None:
                self._values["key_encipherment"] = key_encipherment
            if non_repudiation is not None:
                self._values["non_repudiation"] = non_repudiation

        @builtins.property
        def crl_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to sign CRLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-crlsign
            '''
            result = self._values.get("crl_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def data_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to decipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-dataencipherment
            '''
            result = self._values.get("data_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def decipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used only to decipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-decipheronly
            '''
            result = self._values.get("decipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def digital_signature(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used for digital signing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-digitalsignature
            '''
            result = self._values.get("digital_signature")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def encipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used only to encipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-encipheronly
            '''
            result = self._values.get("encipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used in a key-agreement protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keyagreement
            '''
            result = self._values.get("key_agreement")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def key_cert_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to sign certificates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keycertsign
            '''
            result = self._values.get("key_cert_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def key_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used to encipher data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keyencipherment
            '''
            result = self._values.get("key_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def non_repudiation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Key can be used for non-repudiation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-nonrepudiation
            '''
            result = self._values.get("non_repudiation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.OcspConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "ocsp_custom_cname": "ocspCustomCname"},
    )
    class OcspConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            ocsp_custom_cname: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information to enable and configure Online Certificate Status Protocol (OCSP) for validating certificate revocation status.

            :param enabled: Flag enabling use of the Online Certificate Status Protocol (OCSP) for validating certificate revocation status.
            :param ocsp_custom_cname: By default, AWS Private CA injects an Amazon domain into certificates being validated by the Online Certificate Status Protocol (OCSP). A customer can alternatively use this object to define a CNAME specifying a customized OCSP domain. .. epigraph:: The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-ocspconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                ocsp_configuration_property = acmpca.CfnCertificateAuthority.OcspConfigurationProperty(
                    enabled=False,
                    ocsp_custom_cname="ocspCustomCname"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e859a7ff73aba5c5e4444c4cab16b0314e10688a2f58a251fdd3467fd8367478)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument ocsp_custom_cname", value=ocsp_custom_cname, expected_type=type_hints["ocsp_custom_cname"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if ocsp_custom_cname is not None:
                self._values["ocsp_custom_cname"] = ocsp_custom_cname

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Flag enabling use of the Online Certificate Status Protocol (OCSP) for validating certificate revocation status.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-ocspconfiguration.html#cfn-acmpca-certificateauthority-ocspconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def ocsp_custom_cname(self) -> typing.Optional[builtins.str]:
            '''By default, AWS Private CA injects an Amazon domain into certificates being validated by the Online Certificate Status Protocol (OCSP).

            A customer can alternatively use this object to define a CNAME specifying a customized OCSP domain.
            .. epigraph::

               The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-ocspconfiguration.html#cfn-acmpca-certificateauthority-ocspconfiguration-ocspcustomcname
            '''
            result = self._values.get("ocsp_custom_cname")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcspConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.OtherNameProperty",
        jsii_struct_bases=[],
        name_mapping={"type_id": "typeId", "value": "value"},
    )
    class OtherNameProperty:
        def __init__(self, *, type_id: builtins.str, value: builtins.str) -> None:
            '''Defines a custom ASN.1 X.400 ``GeneralName`` using an object identifier (OID) and value. The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :param type_id: Specifies an OID.
            :param value: Specifies an OID value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                other_name_property = acmpca.CfnCertificateAuthority.OtherNameProperty(
                    type_id="typeId",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3188d1b75a6b53f01012257d5c7492143c9f20d55764b0d4b2a684710fce408e)
                check_type(argname="argument type_id", value=type_id, expected_type=type_hints["type_id"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type_id": type_id,
                "value": value,
            }

        @builtins.property
        def type_id(self) -> builtins.str:
            '''Specifies an OID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html#cfn-acmpca-certificateauthority-othername-typeid
            '''
            result = self._values.get("type_id")
            assert result is not None, "Required property 'type_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Specifies an OID value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html#cfn-acmpca-certificateauthority-othername-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtherNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.RevocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_configuration": "crlConfiguration",
            "ocsp_configuration": "ocspConfiguration",
        },
    )
    class RevocationConfigurationProperty:
        def __init__(
            self,
            *,
            crl_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.CrlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ocsp_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.OcspConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Certificate revocation information used by the `CreateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthority.html>`_ and `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ actions. Your private certificate authority (CA) can configure Online Certificate Status Protocol (OCSP) support and/or maintain a certificate revocation list (CRL). OCSP returns validation information about certificates as requested by clients, and a CRL contains an updated list of certificates revoked by your CA. For more information, see `RevokeCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_RevokeCertificate.html>`_ in the *AWS Private CA API Reference* and `Setting up a certificate revocation method <https://docs.aws.amazon.com/privateca/latest/userguide/revocation-setup.html>`_ in the *AWS Private CA User Guide* .

            .. epigraph::

               The following requirements apply to revocation configurations.

               - A configuration disabling CRLs or OCSP must contain only the ``Enabled=False`` parameter, and will fail if other parameters such as ``CustomCname`` or ``ExpirationInDays`` are included.
               - In a CRL configuration, the ``S3BucketName`` parameter must conform to the `Amazon S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .
               - A configuration containing a custom Canonical Name (CNAME) parameter for CRLs or OCSP must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in a CNAME.
               - In a CRL or OCSP configuration, the value of a CNAME parameter must not include a protocol prefix such as "http://" or "https://".

            :param crl_configuration: Configuration of the certificate revocation list (CRL), if any, maintained by your private CA.
            :param ocsp_configuration: Configuration of Online Certificate Status Protocol (OCSP) support, if any, maintained by your private CA.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                revocation_configuration_property = acmpca.CfnCertificateAuthority.RevocationConfigurationProperty(
                    crl_configuration=acmpca.CfnCertificateAuthority.CrlConfigurationProperty(
                        custom_cname="customCname",
                        enabled=False,
                        expiration_in_days=123,
                        s3_bucket_name="s3BucketName",
                        s3_object_acl="s3ObjectAcl"
                    ),
                    ocsp_configuration=acmpca.CfnCertificateAuthority.OcspConfigurationProperty(
                        enabled=False,
                        ocsp_custom_cname="ocspCustomCname"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__460720819d076c013e704d6db14529fcec65928deb89755e928453d5e9bd40e0)
                check_type(argname="argument crl_configuration", value=crl_configuration, expected_type=type_hints["crl_configuration"])
                check_type(argname="argument ocsp_configuration", value=ocsp_configuration, expected_type=type_hints["ocsp_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crl_configuration is not None:
                self._values["crl_configuration"] = crl_configuration
            if ocsp_configuration is not None:
                self._values["ocsp_configuration"] = ocsp_configuration

        @builtins.property
        def crl_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.CrlConfigurationProperty"]]:
            '''Configuration of the certificate revocation list (CRL), if any, maintained by your private CA.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html#cfn-acmpca-certificateauthority-revocationconfiguration-crlconfiguration
            '''
            result = self._values.get("crl_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.CrlConfigurationProperty"]], result)

        @builtins.property
        def ocsp_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.OcspConfigurationProperty"]]:
            '''Configuration of Online Certificate Status Protocol (OCSP) support, if any, maintained by your private CA.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html#cfn-acmpca-certificateauthority-revocationconfiguration-ocspconfiguration
            '''
            result = self._values.get("ocsp_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.OcspConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.SubjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_name": "commonName",
            "country": "country",
            "custom_attributes": "customAttributes",
            "distinguished_name_qualifier": "distinguishedNameQualifier",
            "generation_qualifier": "generationQualifier",
            "given_name": "givenName",
            "initials": "initials",
            "locality": "locality",
            "organization": "organization",
            "organizational_unit": "organizationalUnit",
            "pseudonym": "pseudonym",
            "serial_number": "serialNumber",
            "state": "state",
            "surname": "surname",
            "title": "title",
        },
    )
    class SubjectProperty:
        def __init__(
            self,
            *,
            common_name: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            custom_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCertificateAuthority.CustomAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            distinguished_name_qualifier: typing.Optional[builtins.str] = None,
            generation_qualifier: typing.Optional[builtins.str] = None,
            given_name: typing.Optional[builtins.str] = None,
            initials: typing.Optional[builtins.str] = None,
            locality: typing.Optional[builtins.str] = None,
            organization: typing.Optional[builtins.str] = None,
            organizational_unit: typing.Optional[builtins.str] = None,
            pseudonym: typing.Optional[builtins.str] = None,
            serial_number: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
            surname: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''ASN1 subject for the certificate authority.

            :param common_name: Fully qualified domain name (FQDN) associated with the certificate subject.
            :param country: Two-digit code that specifies the country in which the certificate subject located.
            :param custom_attributes: Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ . .. epigraph:: Custom attributes cannot be used in combination with standard attributes.
            :param distinguished_name_qualifier: Disambiguating information for the certificate subject.
            :param generation_qualifier: Typically a qualifier appended to the name of an individual. Examples include Jr. for junior, Sr. for senior, and III for third.
            :param given_name: First name.
            :param initials: Concatenation that typically contains the first letter of the GivenName, the first letter of the middle name if one exists, and the first letter of the SurName.
            :param locality: The locality (such as a city or town) in which the certificate subject is located.
            :param organization: Legal name of the organization with which the certificate subject is affiliated.
            :param organizational_unit: A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.
            :param pseudonym: Typically a shortened version of a longer GivenName. For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.
            :param serial_number: The certificate serial number.
            :param state: State in which the subject of the certificate is located.
            :param surname: Family name.
            :param title: A personal title such as Mr.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_acmpca as acmpca
                
                subject_property = acmpca.CfnCertificateAuthority.SubjectProperty(
                    common_name="commonName",
                    country="country",
                    custom_attributes=[acmpca.CfnCertificateAuthority.CustomAttributeProperty(
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    distinguished_name_qualifier="distinguishedNameQualifier",
                    generation_qualifier="generationQualifier",
                    given_name="givenName",
                    initials="initials",
                    locality="locality",
                    organization="organization",
                    organizational_unit="organizationalUnit",
                    pseudonym="pseudonym",
                    serial_number="serialNumber",
                    state="state",
                    surname="surname",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d513279afce51b6189a9601130939fe428009bd86280efadeb996d7b3413132)
                check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
                check_type(argname="argument distinguished_name_qualifier", value=distinguished_name_qualifier, expected_type=type_hints["distinguished_name_qualifier"])
                check_type(argname="argument generation_qualifier", value=generation_qualifier, expected_type=type_hints["generation_qualifier"])
                check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
                check_type(argname="argument initials", value=initials, expected_type=type_hints["initials"])
                check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
                check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
                check_type(argname="argument pseudonym", value=pseudonym, expected_type=type_hints["pseudonym"])
                check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if common_name is not None:
                self._values["common_name"] = common_name
            if country is not None:
                self._values["country"] = country
            if custom_attributes is not None:
                self._values["custom_attributes"] = custom_attributes
            if distinguished_name_qualifier is not None:
                self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None:
                self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None:
                self._values["given_name"] = given_name
            if initials is not None:
                self._values["initials"] = initials
            if locality is not None:
                self._values["locality"] = locality
            if organization is not None:
                self._values["organization"] = organization
            if organizational_unit is not None:
                self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None:
                self._values["pseudonym"] = pseudonym
            if serial_number is not None:
                self._values["serial_number"] = serial_number
            if state is not None:
                self._values["state"] = state
            if surname is not None:
                self._values["surname"] = surname
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            '''Fully qualified domain name (FQDN) associated with the certificate subject.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-commonname
            '''
            result = self._values.get("common_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            '''Two-digit code that specifies the country in which the certificate subject located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.CustomAttributeProperty"]]]]:
            '''Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            .. epigraph::

               Custom attributes cannot be used in combination with standard attributes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-customattributes
            '''
            result = self._values.get("custom_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCertificateAuthority.CustomAttributeProperty"]]]], result)

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
            '''Disambiguating information for the certificate subject.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-distinguishednamequalifier
            '''
            result = self._values.get("distinguished_name_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[builtins.str]:
            '''Typically a qualifier appended to the name of an individual.

            Examples include Jr. for junior, Sr. for senior, and III for third.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-generationqualifier
            '''
            result = self._values.get("generation_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def given_name(self) -> typing.Optional[builtins.str]:
            '''First name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-givenname
            '''
            result = self._values.get("given_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def initials(self) -> typing.Optional[builtins.str]:
            '''Concatenation that typically contains the first letter of the GivenName, the first letter of the middle name if one exists, and the first letter of the SurName.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-initials
            '''
            result = self._values.get("initials")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locality(self) -> typing.Optional[builtins.str]:
            '''The locality (such as a city or town) in which the certificate subject is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-locality
            '''
            result = self._values.get("locality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organization(self) -> typing.Optional[builtins.str]:
            '''Legal name of the organization with which the certificate subject is affiliated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organization
            '''
            result = self._values.get("organization")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit(self) -> typing.Optional[builtins.str]:
            '''A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organizationalunit
            '''
            result = self._values.get("organizational_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pseudonym(self) -> typing.Optional[builtins.str]:
            '''Typically a shortened version of a longer GivenName.

            For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-pseudonym
            '''
            result = self._values.get("pseudonym")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def serial_number(self) -> typing.Optional[builtins.str]:
            '''The certificate serial number.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-serialnumber
            '''
            result = self._values.get("serial_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''State in which the subject of the certificate is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def surname(self) -> typing.Optional[builtins.str]:
            '''Family name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-surname
            '''
            result = self._values.get("surname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''A personal title such as Mr.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCertificateAuthorityActivation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityActivation",
):
    '''A CloudFormation ``AWS::ACMPCA::CertificateAuthorityActivation``.

    The ``AWS::ACMPCA::CertificateAuthorityActivation`` resource creates and installs a CA certificate on a CA. If no status is specified, the ``AWS::ACMPCA::CertificateAuthorityActivation`` resource status defaults to ACTIVE. Once the CA has a CA certificate installed, you can use the resource to toggle the CA status field between ``ACTIVE`` and ``DISABLED`` .

    :cloudformationResource: AWS::ACMPCA::CertificateAuthorityActivation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_acmpca as acmpca
        
        cfn_certificate_authority_activation = acmpca.CfnCertificateAuthorityActivation(self, "MyCfnCertificateAuthorityActivation",
            certificate="certificate",
            certificate_authority_arn="certificateAuthorityArn",
        
            # the properties below are optional
            certificate_chain="certificateChain",
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        certificate: builtins.str,
        certificate_authority_arn: builtins.str,
        certificate_chain: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: The Base64 PEM-encoded certificate authority certificate.
        :param certificate_authority_arn: The Amazon Resource Name (ARN) of your private CA.
        :param certificate_chain: The Base64 PEM-encoded certificate chain that chains up to the root CA certificate that you used to sign your private CA certificate.
        :param status: Status of your private CA.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8e54de089101906c093a5a0bbefb293640c2d8bedaa1326e1736fd45584b3b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCertificateAuthorityActivationProps(
            certificate=certificate,
            certificate_authority_arn=certificate_authority_arn,
            certificate_chain=certificate_chain,
            status=status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8641985c15afb8be3fb317e7595700f5a3673c929a8118185edffe1adce6c4d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5a88557f8faa0d954c1f0fbacce803e70b0ceef9a6c239997b5a380e89240d1)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCompleteCertificateChain")
    def attr_complete_certificate_chain(self) -> builtins.str:
        '''The complete Base64 PEM-encoded certificate chain, including the certificate authority certificate.

        :cloudformationAttribute: CompleteCertificateChain
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCompleteCertificateChain"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        '''The Base64 PEM-encoded certificate authority certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a3ba6580fee61242aeacccca90a8ad87be67e4eb4c3521709a6e33ca3a3ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthorityArn"))

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b440670e09d0a27c396292d15ea076dd6f9abd389986ef4a6766a6ccc6510c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The Base64 PEM-encoded certificate chain that chains up to the root CA certificate that you used to sign your private CA certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49fa3d75972f73a3ad05b2bc6487e220fc8323e8733b860f1d5521b826acb01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86cdf660338bad03422e5f68774742d424ee442a140837bf8dbe15c71e5bed60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityActivationProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_chain": "certificateChain",
        "status": "status",
    },
)
class CfnCertificateAuthorityActivationProps:
    def __init__(
        self,
        *,
        certificate: builtins.str,
        certificate_authority_arn: builtins.str,
        certificate_chain: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCertificateAuthorityActivation``.

        :param certificate: The Base64 PEM-encoded certificate authority certificate.
        :param certificate_authority_arn: The Amazon Resource Name (ARN) of your private CA.
        :param certificate_chain: The Base64 PEM-encoded certificate chain that chains up to the root CA certificate that you used to sign your private CA certificate.
        :param status: Status of your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_acmpca as acmpca
            
            cfn_certificate_authority_activation_props = acmpca.CfnCertificateAuthorityActivationProps(
                certificate="certificate",
                certificate_authority_arn="certificateAuthorityArn",
            
                # the properties below are optional
                certificate_chain="certificateChain",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506390c4f397f325d39dd7fd432b3f6d2840e8ea0ff75154b09e0736b716be06)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "certificate_authority_arn": certificate_authority_arn,
        }
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def certificate(self) -> builtins.str:
        '''The Base64 PEM-encoded certificate authority certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        assert result is not None, "Required property 'certificate_authority_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The Base64 PEM-encoded certificate chain that chains up to the root CA certificate that you used to sign your private CA certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        '''
        result = self._values.get("certificate_chain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityActivationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_algorithm": "keyAlgorithm",
        "signing_algorithm": "signingAlgorithm",
        "subject": "subject",
        "type": "type",
        "csr_extensions": "csrExtensions",
        "key_storage_security_standard": "keyStorageSecurityStandard",
        "revocation_configuration": "revocationConfiguration",
        "tags": "tags",
        "usage_mode": "usageMode",
    },
)
class CfnCertificateAuthorityProps:
    def __init__(
        self,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.SubjectProperty, typing.Dict[builtins.str, typing.Any]]],
        type: builtins.str,
        csr_extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.CsrExtensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        key_storage_security_standard: typing.Optional[builtins.str] = None,
        revocation_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.RevocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        usage_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCertificateAuthority``.

        :param key_algorithm: Type of the public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate. When you create a subordinate CA, you must use a key algorithm supported by the parent CA.
        :param signing_algorithm: Name of the algorithm your private CA uses to sign certificate requests. This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign certificates when they are issued.
        :param subject: Structure that contains X.500 distinguished name information for your private CA.
        :param type: Type of your private CA.
        :param csr_extensions: Specifies information to be added to the extension section of the certificate signing request (CSR).
        :param key_storage_security_standard: Specifies a cryptographic key management compliance standard used for handling CA keys. Default: FIPS_140_2_LEVEL_3_OR_HIGHER .. epigraph:: Some AWS Regions do not support the default. When creating a CA in these Regions, you must provide ``FIPS_140_2_LEVEL_2_OR_HIGHER`` as the argument for ``KeyStorageSecurityStandard`` . Failure to do this results in an ``InvalidArgsException`` with the message, "A certificate authority cannot be created in this region with the specified security standard." For information about security standard support in various Regions, see `Storage and security compliance of AWS Private CA private keys <https://docs.aws.amazon.com/privateca/latest/userguide/data-protection.html#private-keys>`_ .
        :param revocation_configuration: Certificate revocation information used by the `CreateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthority.html>`_ and `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ actions. Your private certificate authority (CA) can configure Online Certificate Status Protocol (OCSP) support and/or maintain a certificate revocation list (CRL). OCSP returns validation information about certificates as requested by clients, and a CRL contains an updated list of certificates revoked by your CA. For more information, see `RevokeCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_RevokeCertificate.html>`_ in the *AWS Private CA API Reference* and `Setting up a certificate revocation method <https://docs.aws.amazon.com/privateca/latest/userguide/revocation-setup.html>`_ in the *AWS Private CA User Guide* . .. epigraph:: The following requirements apply to revocation configurations. - A configuration disabling CRLs or OCSP must contain only the ``Enabled=False`` parameter, and will fail if other parameters such as ``CustomCname`` or ``ExpirationInDays`` are included. - In a CRL configuration, the ``S3BucketName`` parameter must conform to the `Amazon S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ . - A configuration containing a custom Canonical Name (CNAME) parameter for CRLs or OCSP must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in a CNAME. - In a CRL or OCSP configuration, the value of a CNAME parameter must not include a protocol prefix such as "http://" or "https://".
        :param tags: Key-value pairs that will be attached to the new private CA. You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see `Controlling Access Using IAM Tags <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html>`_ .
        :param usage_mode: Specifies whether the CA issues general-purpose certificates that typically require a revocation mechanism, or short-lived certificates that may optionally omit revocation because they expire quickly. Short-lived certificate validity is limited to seven days. The default value is GENERAL_PURPOSE.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
        :exampleMetadata: infused

        Example::

            cfn_certificate_authority = acmpca.CfnCertificateAuthority(self, "CA",
                type="ROOT",
                key_algorithm="RSA_2048",
                signing_algorithm="SHA256WITHRSA",
                subject=acmpca.CfnCertificateAuthority.SubjectProperty(
                    country="US",
                    organization="string",
                    organizational_unit="string",
                    distinguished_name_qualifier="string",
                    state="string",
                    common_name="123",
                    serial_number="string",
                    locality="string",
                    title="string",
                    surname="string",
                    given_name="string",
                    initials="DG",
                    pseudonym="string",
                    generation_qualifier="DBG"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca0dfa4926c4fb4473c5c17eae1bb4fbee86fbbde531e9a48a5509a24d2f8f1)
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument csr_extensions", value=csr_extensions, expected_type=type_hints["csr_extensions"])
            check_type(argname="argument key_storage_security_standard", value=key_storage_security_standard, expected_type=type_hints["key_storage_security_standard"])
            check_type(argname="argument revocation_configuration", value=revocation_configuration, expected_type=type_hints["revocation_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument usage_mode", value=usage_mode, expected_type=type_hints["usage_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_algorithm": key_algorithm,
            "signing_algorithm": signing_algorithm,
            "subject": subject,
            "type": type,
        }
        if csr_extensions is not None:
            self._values["csr_extensions"] = csr_extensions
        if key_storage_security_standard is not None:
            self._values["key_storage_security_standard"] = key_storage_security_standard
        if revocation_configuration is not None:
            self._values["revocation_configuration"] = revocation_configuration
        if tags is not None:
            self._values["tags"] = tags
        if usage_mode is not None:
            self._values["usage_mode"] = usage_mode

    @builtins.property
    def key_algorithm(self) -> builtins.str:
        '''Type of the public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate.

        When you create a subordinate CA, you must use a key algorithm supported by the parent CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        '''
        result = self._values.get("key_algorithm")
        assert result is not None, "Required property 'key_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        '''Name of the algorithm your private CA uses to sign certificate requests.

        This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign certificates when they are issued.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        '''
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.SubjectProperty]:
        '''Structure that contains X.500 distinguished name information for your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.SubjectProperty], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of your private CA.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def csr_extensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.CsrExtensionsProperty]]:
        '''Specifies information to be added to the extension section of the certificate signing request (CSR).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-csrextensions
        '''
        result = self._values.get("csr_extensions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.CsrExtensionsProperty]], result)

    @builtins.property
    def key_storage_security_standard(self) -> typing.Optional[builtins.str]:
        '''Specifies a cryptographic key management compliance standard used for handling CA keys.

        Default: FIPS_140_2_LEVEL_3_OR_HIGHER
        .. epigraph::

           Some AWS Regions do not support the default. When creating a CA in these Regions, you must provide ``FIPS_140_2_LEVEL_2_OR_HIGHER`` as the argument for ``KeyStorageSecurityStandard`` . Failure to do this results in an ``InvalidArgsException`` with the message, "A certificate authority cannot be created in this region with the specified security standard."

           For information about security standard support in various Regions, see `Storage and security compliance of AWS Private CA private keys <https://docs.aws.amazon.com/privateca/latest/userguide/data-protection.html#private-keys>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keystoragesecuritystandard
        '''
        result = self._values.get("key_storage_security_standard")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revocation_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.RevocationConfigurationProperty]]:
        '''Certificate revocation information used by the `CreateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthority.html>`_ and `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ actions. Your private certificate authority (CA) can configure Online Certificate Status Protocol (OCSP) support and/or maintain a certificate revocation list (CRL). OCSP returns validation information about certificates as requested by clients, and a CRL contains an updated list of certificates revoked by your CA. For more information, see `RevokeCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_RevokeCertificate.html>`_ in the *AWS Private CA API Reference* and `Setting up a certificate revocation method <https://docs.aws.amazon.com/privateca/latest/userguide/revocation-setup.html>`_ in the *AWS Private CA User Guide* .

        .. epigraph::

           The following requirements apply to revocation configurations.

           - A configuration disabling CRLs or OCSP must contain only the ``Enabled=False`` parameter, and will fail if other parameters such as ``CustomCname`` or ``ExpirationInDays`` are included.
           - In a CRL configuration, the ``S3BucketName`` parameter must conform to the `Amazon S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .
           - A configuration containing a custom Canonical Name (CNAME) parameter for CRLs or OCSP must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in a CNAME.
           - In a CRL or OCSP configuration, the value of a CNAME parameter must not include a protocol prefix such as "http://" or "https://".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        '''
        result = self._values.get("revocation_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.RevocationConfigurationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Key-value pairs that will be attached to the new private CA.

        You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see `Controlling Access Using IAM Tags <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def usage_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the CA issues general-purpose certificates that typically require a revocation mechanism, or short-lived certificates that may optionally omit revocation because they expire quickly.

        Short-lived certificate validity is limited to seven days.

        The default value is GENERAL_PURPOSE.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-usagemode
        '''
        result = self._values.get("usage_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_signing_request": "certificateSigningRequest",
        "signing_algorithm": "signingAlgorithm",
        "validity": "validity",
        "api_passthrough": "apiPassthrough",
        "template_arn": "templateArn",
        "validity_not_before": "validityNotBefore",
    },
)
class CfnCertificateProps:
    def __init__(
        self,
        *,
        certificate_authority_arn: builtins.str,
        certificate_signing_request: builtins.str,
        signing_algorithm: builtins.str,
        validity: typing.Union[typing.Union[CfnCertificate.ValidityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        api_passthrough: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.ApiPassthroughProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        template_arn: typing.Optional[builtins.str] = None,
        validity_not_before: typing.Optional[typing.Union[typing.Union[CfnCertificate.ValidityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCertificate``.

        :param certificate_authority_arn: The Amazon Resource Name (ARN) for the private CA issues the certificate.
        :param certificate_signing_request: The certificate signing request (CSR) for the certificate.
        :param signing_algorithm: The name of the algorithm that will be used to sign the certificate to be issued. This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign a CSR in the ``CreateCertificateAuthority`` action. .. epigraph:: The specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key.
        :param validity: The period of time during which the certificate will be valid.
        :param api_passthrough: Specifies X.509 certificate information to be included in the issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.
        :param template_arn: Specifies a custom configuration template to use when issuing a certificate. If this parameter is not provided, AWS Private CA defaults to the ``EndEntityCertificate/V1`` template. For more information about AWS Private CA templates, see `Using Templates <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html>`_ .
        :param validity_not_before: Information describing the start of the validity period of the certificate. This parameter sets the “Not Before" date for the certificate. By default, when issuing a certificate, AWS Private CA sets the "Not Before" date to the issuance time minus 60 minutes. This compensates for clock inconsistencies across computer systems. The ``ValidityNotBefore`` parameter can be used to customize the “Not Before” value. Unlike the ``Validity`` parameter, the ``ValidityNotBefore`` parameter is optional. The ``ValidityNotBefore`` value is expressed as an explicit date and time, using the ``Validity`` type value ``ABSOLUTE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_acmpca as acmpca
            
            cfn_certificate_props = acmpca.CfnCertificateProps(
                certificate_authority_arn="certificateAuthorityArn",
                certificate_signing_request="certificateSigningRequest",
                signing_algorithm="signingAlgorithm",
                validity=acmpca.CfnCertificate.ValidityProperty(
                    type="type",
                    value=123
                ),
            
                # the properties below are optional
                api_passthrough=acmpca.CfnCertificate.ApiPassthroughProperty(
                    extensions=acmpca.CfnCertificate.ExtensionsProperty(
                        certificate_policies=[acmpca.CfnCertificate.PolicyInformationProperty(
                            cert_policy_id="certPolicyId",
            
                            # the properties below are optional
                            policy_qualifiers=[acmpca.CfnCertificate.PolicyQualifierInfoProperty(
                                policy_qualifier_id="policyQualifierId",
                                qualifier=acmpca.CfnCertificate.QualifierProperty(
                                    cps_uri="cpsUri"
                                )
                            )]
                        )],
                        custom_extensions=[acmpca.CfnCertificate.CustomExtensionProperty(
                            object_identifier="objectIdentifier",
                            value="value",
            
                            # the properties below are optional
                            critical=False
                        )],
                        extended_key_usage=[acmpca.CfnCertificate.ExtendedKeyUsageProperty(
                            extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                            extended_key_usage_type="extendedKeyUsageType"
                        )],
                        key_usage=acmpca.CfnCertificate.KeyUsageProperty(
                            crl_sign=False,
                            data_encipherment=False,
                            decipher_only=False,
                            digital_signature=False,
                            encipher_only=False,
                            key_agreement=False,
                            key_cert_sign=False,
                            key_encipherment=False,
                            non_repudiation=False
                        ),
                        subject_alternative_names=[acmpca.CfnCertificate.GeneralNameProperty(
                            directory_name=acmpca.CfnCertificate.SubjectProperty(
                                common_name="commonName",
                                country="country",
                                custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                                    object_identifier="objectIdentifier",
                                    value="value"
                                )],
                                distinguished_name_qualifier="distinguishedNameQualifier",
                                generation_qualifier="generationQualifier",
                                given_name="givenName",
                                initials="initials",
                                locality="locality",
                                organization="organization",
                                organizational_unit="organizationalUnit",
                                pseudonym="pseudonym",
                                serial_number="serialNumber",
                                state="state",
                                surname="surname",
                                title="title"
                            ),
                            dns_name="dnsName",
                            edi_party_name=acmpca.CfnCertificate.EdiPartyNameProperty(
                                name_assigner="nameAssigner",
                                party_name="partyName"
                            ),
                            ip_address="ipAddress",
                            other_name=acmpca.CfnCertificate.OtherNameProperty(
                                type_id="typeId",
                                value="value"
                            ),
                            registered_id="registeredId",
                            rfc822_name="rfc822Name",
                            uniform_resource_identifier="uniformResourceIdentifier"
                        )]
                    ),
                    subject=acmpca.CfnCertificate.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca.CfnCertificate.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    )
                ),
                template_arn="templateArn",
                validity_not_before=acmpca.CfnCertificate.ValidityProperty(
                    type="type",
                    value=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b363860748f59b1bc6e46a309553107cfd7de7b0f56cbc20c24d25547e10406)
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument certificate_signing_request", value=certificate_signing_request, expected_type=type_hints["certificate_signing_request"])
            check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            check_type(argname="argument validity", value=validity, expected_type=type_hints["validity"])
            check_type(argname="argument api_passthrough", value=api_passthrough, expected_type=type_hints["api_passthrough"])
            check_type(argname="argument template_arn", value=template_arn, expected_type=type_hints["template_arn"])
            check_type(argname="argument validity_not_before", value=validity_not_before, expected_type=type_hints["validity_not_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_authority_arn": certificate_authority_arn,
            "certificate_signing_request": certificate_signing_request,
            "signing_algorithm": signing_algorithm,
            "validity": validity,
        }
        if api_passthrough is not None:
            self._values["api_passthrough"] = api_passthrough
        if template_arn is not None:
            self._values["template_arn"] = template_arn
        if validity_not_before is not None:
            self._values["validity_not_before"] = validity_not_before

    @builtins.property
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the private CA issues the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        assert result is not None, "Required property 'certificate_authority_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate_signing_request(self) -> builtins.str:
        '''The certificate signing request (CSR) for the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        '''
        result = self._values.get("certificate_signing_request")
        assert result is not None, "Required property 'certificate_signing_request' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        '''The name of the algorithm that will be used to sign the certificate to be issued.

        This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign a CSR in the ``CreateCertificateAuthority`` action.
        .. epigraph::

           The specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        '''
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validity(
        self,
    ) -> typing.Union[CfnCertificate.ValidityProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The period of time during which the certificate will be valid.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        '''
        result = self._values.get("validity")
        assert result is not None, "Required property 'validity' is missing"
        return typing.cast(typing.Union[CfnCertificate.ValidityProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def api_passthrough(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificate.ApiPassthroughProperty]]:
        '''Specifies X.509 certificate information to be included in the issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-apipassthrough
        '''
        result = self._values.get("api_passthrough")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificate.ApiPassthroughProperty]], result)

    @builtins.property
    def template_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies a custom configuration template to use when issuing a certificate.

        If this parameter is not provided, AWS Private CA defaults to the ``EndEntityCertificate/V1`` template. For more information about AWS Private CA templates, see `Using Templates <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        '''
        result = self._values.get("template_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validity_not_before(
        self,
    ) -> typing.Optional[typing.Union[CfnCertificate.ValidityProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Information describing the start of the validity period of the certificate.

        This parameter sets the “Not Before" date for the certificate.

        By default, when issuing a certificate, AWS Private CA sets the "Not Before" date to the issuance time minus 60 minutes. This compensates for clock inconsistencies across computer systems. The ``ValidityNotBefore`` parameter can be used to customize the “Not Before” value.

        Unlike the ``Validity`` parameter, the ``ValidityNotBefore`` parameter is optional.

        The ``ValidityNotBefore`` value is expressed as an explicit date and time, using the ``Validity`` type value ``ABSOLUTE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validitynotbefore
        '''
        result = self._values.get("validity_not_before")
        return typing.cast(typing.Optional[typing.Union[CfnCertificate.ValidityProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPermission(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnPermission",
):
    '''A CloudFormation ``AWS::ACMPCA::Permission``.

    Grants permissions to the AWS Certificate Manager ( ACM ) service principal ( ``acm.amazonaws.com`` ) to perform `IssueCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_IssueCertificate.html>`_ , `GetCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_GetCertificate.html>`_ , and `ListPermissions <https://docs.aws.amazon.com/privateca/latest/APIReference/API_ListPermissions.html>`_ actions on a CA. These actions are needed for the ACM principal to renew private PKI certificates requested through ACM and residing in the same AWS account as the CA.

    **About permissions** - If the private CA and the certificates it issues reside in the same account, you can use ``AWS::ACMPCA::Permission`` to grant permissions for ACM to carry out automatic certificate renewals.

    - For automatic certificate renewal to succeed, the ACM service principal needs permissions to create, retrieve, and list permissions.
    - If the private CA and the ACM certificates reside in different accounts, then permissions cannot be used to enable automatic renewals. Instead, the ACM certificate owner must set up a resource-based policy to enable cross-account issuance and renewals. For more information, see `Using a Resource Based Policy with AWS Private CA <https://docs.aws.amazon.com/privateca/latest/userguide/pca-rbp.html>`_ .

    .. epigraph::

       To update an ``AWS::ACMPCA::Permission`` resource, you must first delete the existing permission resource from the CloudFormation stack and then create a new permission resource with updated properties.

    :cloudformationResource: AWS::ACMPCA::Permission
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_acmpca as acmpca
        
        cfn_permission = acmpca.CfnPermission(self, "MyCfnPermission",
            actions=["actions"],
            certificate_authority_arn="certificateAuthorityArn",
            principal="principal",
        
            # the properties below are optional
            source_account="sourceAccount"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        actions: typing.Sequence[builtins.str],
        certificate_authority_arn: builtins.str,
        principal: builtins.str,
        source_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ACMPCA::Permission``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param actions: The private CA actions that can be performed by the designated AWS service. Supported actions are ``IssueCertificate`` , ``GetCertificate`` , and ``ListPermissions`` .
        :param certificate_authority_arn: The Amazon Resource Number (ARN) of the private CA from which the permission was issued.
        :param principal: The AWS service or entity that holds the permission. At this time, the only valid principal is ``acm.amazonaws.com`` .
        :param source_account: The ID of the account that assigned the permission.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07af52cbc35534a158db19c84f71a208aa2952fb5fd0a276ce5fa1cfcef57f72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPermissionProps(
            actions=actions,
            certificate_authority_arn=certificate_authority_arn,
            principal=principal,
            source_account=source_account,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39ad14375d3f68918b768ba076802b4a3603710585bf8d389d087da53d99572)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec47161ce77a120d6a58809895e62db5bba9cde162318a7e0ecae305979f39f5)
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
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        '''The private CA actions that can be performed by the designated AWS service.

        Supported actions are ``IssueCertificate`` , ``GetCertificate`` , and ``ListPermissions`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-actions
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96246b1330fcd5400935a2fbbbcdcad9918af1683ad86589815a1c7f0c910e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value)

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the private CA from which the permission was issued.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-certificateauthorityarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthorityArn"))

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e8db112163d5c076e953a22320c0721039a3164cb8c81257f2d6baf9dad3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        '''The AWS service or entity that holds the permission.

        At this time, the only valid principal is ``acm.amazonaws.com`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-principal
        '''
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d1322e1a48926d878ddb18687bf8865ecf4215d4a268926831f3ef22f5c6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="sourceAccount")
    def source_account(self) -> typing.Optional[builtins.str]:
        '''The ID of the account that assigned the permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-sourceaccount
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceAccount"))

    @source_account.setter
    def source_account(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03213c19683dc14b93c9342ac8af6a25e3283621174a01c123084b320069fe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceAccount", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnPermissionProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "certificate_authority_arn": "certificateAuthorityArn",
        "principal": "principal",
        "source_account": "sourceAccount",
    },
)
class CfnPermissionProps:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        certificate_authority_arn: builtins.str,
        principal: builtins.str,
        source_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPermission``.

        :param actions: The private CA actions that can be performed by the designated AWS service. Supported actions are ``IssueCertificate`` , ``GetCertificate`` , and ``ListPermissions`` .
        :param certificate_authority_arn: The Amazon Resource Number (ARN) of the private CA from which the permission was issued.
        :param principal: The AWS service or entity that holds the permission. At this time, the only valid principal is ``acm.amazonaws.com`` .
        :param source_account: The ID of the account that assigned the permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_acmpca as acmpca
            
            cfn_permission_props = acmpca.CfnPermissionProps(
                actions=["actions"],
                certificate_authority_arn="certificateAuthorityArn",
                principal="principal",
            
                # the properties below are optional
                source_account="sourceAccount"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71c537381b53b48c77ba846954722c50dbe608cc665570c89adbf6cf0ab5f7c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument source_account", value=source_account, expected_type=type_hints["source_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "certificate_authority_arn": certificate_authority_arn,
            "principal": principal,
        }
        if source_account is not None:
            self._values["source_account"] = source_account

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''The private CA actions that can be performed by the designated AWS service.

        Supported actions are ``IssueCertificate`` , ``GetCertificate`` , and ``ListPermissions`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-actions
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the private CA from which the permission was issued.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        assert result is not None, "Required property 'certificate_authority_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''The AWS service or entity that holds the permission.

        At this time, the only valid principal is ``acm.amazonaws.com`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-principal
        '''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_account(self) -> typing.Optional[builtins.str]:
        '''The ID of the account that assigned the permission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-sourceaccount
        '''
        result = self._values.get("source_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-acmpca.ICertificateAuthority")
class ICertificateAuthority(
    _aws_cdk_core_f4b25747.IResource,
    typing_extensions.Protocol,
):
    '''Interface which all CertificateAuthority based class must implement.'''

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Name of the Certificate.

        :attribute: true
        '''
        ...


class _ICertificateAuthorityProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Interface which all CertificateAuthority based class must implement.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-acmpca.ICertificateAuthority"

    @builtins.property
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        '''The Amazon Resource Name of the Certificate.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateAuthorityArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICertificateAuthority).__jsii_proxy_class__ = lambda : _ICertificateAuthorityProxy


__all__ = [
    "CertificateAuthority",
    "CfnCertificate",
    "CfnCertificateAuthority",
    "CfnCertificateAuthorityActivation",
    "CfnCertificateAuthorityActivationProps",
    "CfnCertificateAuthorityProps",
    "CfnCertificateProps",
    "CfnPermission",
    "CfnPermissionProps",
    "ICertificateAuthority",
]

publication.publish()

def _typecheckingstub__5b779f19c53698e23b2d8dd482a155c35242462848352fb14b975b18ea0746f3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    certificate_authority_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a0a1072e9f353dc3ff3e9116e76340a54ad697a4417471337a42e7a72378ef(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    certificate_authority_arn: builtins.str,
    certificate_signing_request: builtins.str,
    signing_algorithm: builtins.str,
    validity: typing.Union[typing.Union[CfnCertificate.ValidityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    api_passthrough: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.ApiPassthroughProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_arn: typing.Optional[builtins.str] = None,
    validity_not_before: typing.Optional[typing.Union[typing.Union[CfnCertificate.ValidityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c06e49a9bdff97b0e473f2aaf32c664ba189ba301ceae2140e1a558e240dddc(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2c48fe1bcbdf74f60d160666116a09e64b051569b2e1f650f13be9d1bfb5ff(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572d0abf21d692ee812fc2cd284b7f5f13612f8a92daf661130ec9f03a72acde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a599ab5ceb72e84d3e82b81d48b745f513636ee459ccac6a0a82f80afed8cbac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db41702a33ddeb9f9c5c8226369147ac3d7ed616a99aa66bbc4f2d12434a421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290bce6750f48c1dd860aec70e8a58f84c2cd885defdfe31dbdd54d78fd6f6ed(
    value: typing.Union[CfnCertificate.ValidityProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619d7ddd269b7c84d19ccbadf67472c82f51c3c1ba43c4fa6e302850d1565a17(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificate.ApiPassthroughProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ee6f79370132ffcb0e4c34505498476414bc3c96bb8acfa4d609c544eae905(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8697a8d670b4b60188223097ee218739bac0327dd665a252aba128f6a3b3c3a5(
    value: typing.Optional[typing.Union[CfnCertificate.ValidityProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff91782eacbaa78222a37678f74b9c61b6d477a306e2d2895ac0331c8522299d(
    *,
    extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.ExtensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.SubjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087eef006c1f99facb7d2e7fb96bdb59575caa7cf2c9e46f07e962499844af25(
    *,
    object_identifier: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c546930085bb5cf8212c3606334df99f3d44cc5bd323f6c8bfce90907ee3b206(
    *,
    object_identifier: builtins.str,
    value: builtins.str,
    critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4212f757de164ed8e15f74c347e401c6e38aace2fd454c09d2ef85d78fcfbf73(
    *,
    name_assigner: builtins.str,
    party_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf98e5d4e826e748b992e19e50b9df7750e621171f629d540f34addea270ad2(
    *,
    extended_key_usage_object_identifier: typing.Optional[builtins.str] = None,
    extended_key_usage_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75777752be170e0349d0a684b775a3ceb2ca93513e9acbec57f24673d7535579(
    *,
    certificate_policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.PolicyInformationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.CustomExtensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    extended_key_usage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.ExtendedKeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    key_usage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.KeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.GeneralNameProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e50b9009d68d9e053cade424315d94cff9232ce6a718275ede806c8efdb8648(
    *,
    directory_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.SubjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dns_name: typing.Optional[builtins.str] = None,
    edi_party_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.EdiPartyNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    other_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.OtherNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    registered_id: typing.Optional[builtins.str] = None,
    rfc822_name: typing.Optional[builtins.str] = None,
    uniform_resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f246ef49af70cdbea69263b309e8145387262940970094957a0a5408a27e4fb8(
    *,
    crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185d5a603add99146f161899be0716184e3739037cdbc9e06031afd19caf3f0c(
    *,
    type_id: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47696af32c3748dd9b1051ce2debc5f3ec7fdc48a09e9f9029a6d820f0af8e4(
    *,
    cert_policy_id: builtins.str,
    policy_qualifiers: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.PolicyQualifierInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e19aeaed58965cf242fc88c10b684b75e2f6890f77dbc250ebf2aa2df7d3b3a(
    *,
    policy_qualifier_id: builtins.str,
    qualifier: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.QualifierProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e2b6c419ad9af26a4a909a0bb6138e56e7e5e2cdbe4980a6c99b32094da39a(
    *,
    cps_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71d5be4c35fb13969e5c8f04109b8b7740570efecc4e8491df2b468a3f6929e(
    *,
    common_name: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    custom_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.CustomAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    distinguished_name_qualifier: typing.Optional[builtins.str] = None,
    generation_qualifier: typing.Optional[builtins.str] = None,
    given_name: typing.Optional[builtins.str] = None,
    initials: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    pseudonym: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    surname: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80efff0e667ab1ac7f8e1a2a13dd9072b7281cb46b7c2d45bf401dd9226116d4(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904b84401209c2e616777422173fb01eca51f0f550133e510c4934900062d21b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    key_algorithm: builtins.str,
    signing_algorithm: builtins.str,
    subject: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.SubjectProperty, typing.Dict[builtins.str, typing.Any]]],
    type: builtins.str,
    csr_extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.CsrExtensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_storage_security_standard: typing.Optional[builtins.str] = None,
    revocation_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.RevocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    usage_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5049dbbe41c10b4287e548826cbb537cb872060550a25e1e231a8fbf15ac37(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81f5dd8f7bca59193588bf155cc66ddf4f04d41f758765dd1316eb798b13336(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eea6ad2d46b1584a705dcbda5b5879e737056c269531a0ba433f219c10a08c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321aa7b8346c5f938fad1275eb85ed3a3aedcf7a83a987c9d26ae159294c7bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c844f3587ad1b3cc5aaf83bc47dcfcfbcfe13cf3dfcd55259c1cb22780f0ee0c(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.SubjectProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754bb5ab5b1abf7ee53fa0951241546c8e8bd51bd160b33cbdfd78e63153b779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6b5e5d60b1095a51b9f6a4401bdc80608aab99f9f67f0b38a654292eb7e95c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.CsrExtensionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c600bd111dfb393965c27e306fa7bac53607f8bce97ed3864b1970d236a2e705(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650ad4c1e8b020232753ad4079ae422710c0a23c449258c8d86312f51f136c2e(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCertificateAuthority.RevocationConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8fe2bbc91b58f7e370945ee64cb7f1ec42f41e5d548cb7c8df426697e10798(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f59d7d46e13f4f7d3ab4d7b78d637dae1a7a3c5c254abceffc0664973d5cc8(
    *,
    access_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.GeneralNameProperty, typing.Dict[builtins.str, typing.Any]]],
    access_method: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.AccessMethodProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df046a28f007886432b8640a92b8c310bf2c7f6400379b866b023082fbaad9f(
    *,
    access_method_type: typing.Optional[builtins.str] = None,
    custom_object_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d793b80e787d87c0baa48202af901a7bbf05fcd4e7e3514816b3e5a121f5349(
    *,
    custom_cname: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    expiration_in_days: typing.Optional[jsii.Number] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_object_acl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1420c61eadb790f5013cd1762889a48d1e024b3e94a09891e9bbf177280d33d2(
    *,
    key_usage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.KeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject_information_access: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.AccessDescriptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c538e42b2ad1438a491acc1835d642cb8791ba57e3c00217e3fb810021ef447a(
    *,
    object_identifier: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de69eb9c0b68be1be94126679d147f5ea519215dd4c88c6308c0e64dbea75649(
    *,
    name_assigner: builtins.str,
    party_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93aeef42c4138b4e40fa52678f274b9aa3f140335402de29b5a8335b46ece67(
    *,
    directory_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.SubjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dns_name: typing.Optional[builtins.str] = None,
    edi_party_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.EdiPartyNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    other_name: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.OtherNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    registered_id: typing.Optional[builtins.str] = None,
    rfc822_name: typing.Optional[builtins.str] = None,
    uniform_resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b354c1d4587ea02f628b419327f22a622798e5aff2b25dcd89944266ffa48737(
    *,
    crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e859a7ff73aba5c5e4444c4cab16b0314e10688a2f58a251fdd3467fd8367478(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ocsp_custom_cname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3188d1b75a6b53f01012257d5c7492143c9f20d55764b0d4b2a684710fce408e(
    *,
    type_id: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460720819d076c013e704d6db14529fcec65928deb89755e928453d5e9bd40e0(
    *,
    crl_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.CrlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ocsp_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.OcspConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d513279afce51b6189a9601130939fe428009bd86280efadeb996d7b3413132(
    *,
    common_name: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    custom_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.CustomAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    distinguished_name_qualifier: typing.Optional[builtins.str] = None,
    generation_qualifier: typing.Optional[builtins.str] = None,
    given_name: typing.Optional[builtins.str] = None,
    initials: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    pseudonym: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    surname: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8e54de089101906c093a5a0bbefb293640c2d8bedaa1326e1736fd45584b3b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    certificate: builtins.str,
    certificate_authority_arn: builtins.str,
    certificate_chain: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8641985c15afb8be3fb317e7595700f5a3673c929a8118185edffe1adce6c4d3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a88557f8faa0d954c1f0fbacce803e70b0ceef9a6c239997b5a380e89240d1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a3ba6580fee61242aeacccca90a8ad87be67e4eb4c3521709a6e33ca3a3ea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b440670e09d0a27c396292d15ea076dd6f9abd389986ef4a6766a6ccc6510c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49fa3d75972f73a3ad05b2bc6487e220fc8323e8733b860f1d5521b826acb01(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cdf660338bad03422e5f68774742d424ee442a140837bf8dbe15c71e5bed60(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506390c4f397f325d39dd7fd432b3f6d2840e8ea0ff75154b09e0736b716be06(
    *,
    certificate: builtins.str,
    certificate_authority_arn: builtins.str,
    certificate_chain: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca0dfa4926c4fb4473c5c17eae1bb4fbee86fbbde531e9a48a5509a24d2f8f1(
    *,
    key_algorithm: builtins.str,
    signing_algorithm: builtins.str,
    subject: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.SubjectProperty, typing.Dict[builtins.str, typing.Any]]],
    type: builtins.str,
    csr_extensions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.CsrExtensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_storage_security_standard: typing.Optional[builtins.str] = None,
    revocation_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificateAuthority.RevocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    usage_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b363860748f59b1bc6e46a309553107cfd7de7b0f56cbc20c24d25547e10406(
    *,
    certificate_authority_arn: builtins.str,
    certificate_signing_request: builtins.str,
    signing_algorithm: builtins.str,
    validity: typing.Union[typing.Union[CfnCertificate.ValidityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    api_passthrough: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCertificate.ApiPassthroughProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_arn: typing.Optional[builtins.str] = None,
    validity_not_before: typing.Optional[typing.Union[typing.Union[CfnCertificate.ValidityProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07af52cbc35534a158db19c84f71a208aa2952fb5fd0a276ce5fa1cfcef57f72(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    actions: typing.Sequence[builtins.str],
    certificate_authority_arn: builtins.str,
    principal: builtins.str,
    source_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39ad14375d3f68918b768ba076802b4a3603710585bf8d389d087da53d99572(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec47161ce77a120d6a58809895e62db5bba9cde162318a7e0ecae305979f39f5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96246b1330fcd5400935a2fbbbcdcad9918af1683ad86589815a1c7f0c910e5b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e8db112163d5c076e953a22320c0721039a3164cb8c81257f2d6baf9dad3ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d1322e1a48926d878ddb18687bf8865ecf4215d4a268926831f3ef22f5c6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03213c19683dc14b93c9342ac8af6a25e3283621174a01c123084b320069fe9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71c537381b53b48c77ba846954722c50dbe608cc665570c89adbf6cf0ab5f7c(
    *,
    actions: typing.Sequence[builtins.str],
    certificate_authority_arn: builtins.str,
    principal: builtins.str,
    source_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
