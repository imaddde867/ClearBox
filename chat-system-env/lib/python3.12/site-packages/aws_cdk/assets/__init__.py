'''
# AWS CDK Assets

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All types moved to @aws-cdk/core.
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


@jsii.data_type(
    jsii_type="@aws-cdk/assets.CopyOptions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
    },
)
class CopyOptions:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    ) -> None:
        '''(deprecated) Obtains applied when copying directories into the staging location.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '

        :deprecated: see ``core.CopyOptions``

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.assets as assets
            import aws_cdk.core as cdk
            
            copy_options = assets.CopyOptions(
                exclude=["exclude"],
                follow=assets.FollowMode.NEVER,
                ignore_mode=cdk.IgnoreMode.GLOB
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c31160d5ef89ffade3b3be46900d2484f3a1fc5ddfb51958187d1fac2a4deda)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow(self) -> typing.Optional["FollowMode"]:
        '''(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :deprecated: use ``followSymlinks`` instead

        :stability: deprecated
        '''
        result = self._values.get("follow")
        return typing.cast(typing.Optional["FollowMode"], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode]:
        '''(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CopyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/assets.FingerprintOptions",
    jsii_struct_bases=[CopyOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
    },
)
class FingerprintOptions(CopyOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        extra_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Options related to calculating source hash.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content

        :deprecated: see ``core.FingerprintOptions``

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.assets as assets
            import aws_cdk.core as cdk
            
            fingerprint_options = assets.FingerprintOptions(
                exclude=["exclude"],
                extra_hash="extraHash",
                follow=assets.FollowMode.NEVER,
                ignore_mode=cdk.IgnoreMode.GLOB
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963398353180dddd3dec8051c093761f869fca7c4495e3598147f0403cfdb61c)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument extra_hash", value=extra_hash, expected_type=type_hints["extra_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow(self) -> typing.Optional["FollowMode"]:
        '''(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :deprecated: use ``followSymlinks`` instead

        :stability: deprecated
        '''
        result = self._values.get("follow")
        return typing.cast(typing.Optional["FollowMode"], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode]:
        '''(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: deprecated
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FingerprintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/assets.FollowMode")
class FollowMode(enum.Enum):
    '''(deprecated) Symlink follow mode.

    :deprecated: see ``core.SymlinkFollowMode``

    :stability: deprecated
    '''

    NEVER = "NEVER"
    '''(deprecated) Never follow symlinks.

    :stability: deprecated
    '''
    ALWAYS = "ALWAYS"
    '''(deprecated) Materialize all symlinks, whether they are internal or external to the source directory.

    :stability: deprecated
    '''
    EXTERNAL = "EXTERNAL"
    '''(deprecated) Only follows symlinks that are external to the source directory.

    :stability: deprecated
    '''
    BLOCK_EXTERNAL = "BLOCK_EXTERNAL"
    '''(deprecated) Forbids source from having any symlinks pointing outside of the source tree.

    This is the safest mode of operation as it ensures that copy operations
    won't materialize files from the user's file system. Internal symlinks are
    not followed.

    If the copy operation runs into an external symlink, it will fail.

    :stability: deprecated
    '''


@jsii.interface(jsii_type="@aws-cdk/assets.IAsset")
class IAsset(typing_extensions.Protocol):
    '''(deprecated) Common interface for all assets.

    :deprecated: use ``core.IAsset``

    :stability: deprecated
    '''

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        '''(deprecated) A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        :stability: deprecated
        '''
        ...


class _IAssetProxy:
    '''(deprecated) Common interface for all assets.

    :deprecated: use ``core.IAsset``

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/assets.IAsset"

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        '''(deprecated) A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceHash"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAsset).__jsii_proxy_class__ = lambda : _IAssetProxy


class Staging(
    _aws_cdk_core_f4b25747.AssetStaging,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/assets.Staging",
):
    '''(deprecated) Deprecated.

    :deprecated: use ``core.AssetStaging``

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.assets as assets
        import aws_cdk.core as cdk
        
        staging = assets.Staging(self, "MyStaging",
            source_path="sourcePath",
        
            # the properties below are optional
            exclude=["exclude"],
            extra_hash="extraHash",
            follow=assets.FollowMode.NEVER,
            ignore_mode=cdk.IgnoreMode.GLOB
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        source_path: builtins.str,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source_path: (deprecated) Local file or directory to stage.
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4e92f99d2d00973ffc95cb4f366216b74d67380eb2cabb6431ddb101fa022c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StagingProps(
            source_path=source_path,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/assets.StagingProps",
    jsii_struct_bases=[FingerprintOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "source_path": "sourcePath",
    },
)
class StagingProps(FingerprintOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        source_path: builtins.str,
    ) -> None:
        '''(deprecated) Deprecated.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param source_path: (deprecated) Local file or directory to stage.

        :deprecated: use ``core.AssetStagingProps``

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.assets as assets
            import aws_cdk.core as cdk
            
            staging_props = assets.StagingProps(
                source_path="sourcePath",
            
                # the properties below are optional
                exclude=["exclude"],
                extra_hash="extraHash",
                follow=assets.FollowMode.NEVER,
                ignore_mode=cdk.IgnoreMode.GLOB
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035fe31b9324453a6a2cd3c518df53372af7f64ce8f2493461b11e0e5edef405)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument extra_hash", value=extra_hash, expected_type=type_hints["extra_hash"])
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_path": source_path,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow(self) -> typing.Optional[FollowMode]:
        '''(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :deprecated: use ``followSymlinks`` instead

        :stability: deprecated
        '''
        result = self._values.get("follow")
        return typing.cast(typing.Optional[FollowMode], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode]:
        '''(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: deprecated
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_path(self) -> builtins.str:
        '''(deprecated) Local file or directory to stage.

        :stability: deprecated
        '''
        result = self._values.get("source_path")
        assert result is not None, "Required property 'source_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StagingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CopyOptions",
    "FingerprintOptions",
    "FollowMode",
    "IAsset",
    "Staging",
    "StagingProps",
]

publication.publish()

def _typecheckingstub__1c31160d5ef89ffade3b3be46900d2484f3a1fc5ddfb51958187d1fac2a4deda(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963398353180dddd3dec8051c093761f869fca7c4495e3598147f0403cfdb61c(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    extra_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4e92f99d2d00973ffc95cb4f366216b74d67380eb2cabb6431ddb101fa022c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    source_path: builtins.str,
    extra_hash: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035fe31b9324453a6a2cd3c518df53372af7f64ce8f2493461b11e0e5edef405(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    extra_hash: typing.Optional[builtins.str] = None,
    source_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
