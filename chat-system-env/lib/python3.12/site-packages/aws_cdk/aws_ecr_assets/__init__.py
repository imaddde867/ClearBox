'''
# AWS CDK Docker Image Assets

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module allows bundling Docker images as assets.

## Images from Dockerfile

Images are built from a local Docker context directory (with a `Dockerfile`),
uploaded to Amazon Elastic Container Registry (ECR) by the CDK toolkit
and/or your app's CI/CD pipeline, and can be naturally referenced in your CDK app.

```python
from aws_cdk.aws_ecr_assets import DockerImageAsset


asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image")
)
```

The directory `my-image` must include a `Dockerfile`.

This will instruct the toolkit to build a Docker image from `my-image`, push it
to an Amazon ECR repository and wire the name of the repository as CloudFormation
parameters to your stack.

By default, all files in the given directory will be copied into the docker
*build context*. If there is a large directory that you know you definitely
don't need in the build context you can improve the performance by adding the
names of files and directories to ignore to a file called `.dockerignore`, or
pass them via the `exclude` property. If both are available, the patterns
found in `exclude` are appended to the patterns found in `.dockerignore`.

The `ignoreMode` property controls how the set of ignore patterns is
interpreted. The recommended setting for Docker image assets is
`IgnoreMode.DOCKER`. If the context flag
`@aws-cdk/aws-ecr-assets:dockerIgnoreSupport` is set to `true` in your
`cdk.json` (this is by default for new projects, but must be set manually for
old projects) then `IgnoreMode.DOCKER` is the default and you don't need to
configure it on the asset itself.

Use `asset.imageUri` to reference the image. It includes both the ECR image URL
and tag.

You can optionally pass build args to the `docker build` command by specifying
the `buildArgs` property. It is recommended to skip hashing of `buildArgs` for
values that can change between different machines to maintain a consistent
asset hash.

```python
from aws_cdk.aws_ecr_assets import DockerImageAsset


asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    build_args={
        "HTTP_PROXY": "http://10.20.30.2:1234"
    },
    invalidation=DockerImageAssetInvalidationOptions(
        build_args=False
    )
)
```

You can optionally pass a target to the `docker build` command by specifying
the `target` property:

```python
from aws_cdk.aws_ecr_assets import DockerImageAsset


asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    target="a-target"
)
```

You can optionally pass networking mode to the `docker build` command by specifying
the `networkMode` property:

```python
from aws_cdk.aws_ecr_assets import DockerImageAsset, NetworkMode


asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    network_mode=NetworkMode.HOST
)
```

You can optionally pass an alternate platform to the `docker build` command by specifying
the `platform` property:

```python
from aws_cdk.aws_ecr_assets import DockerImageAsset, Platform


asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    platform=Platform.LINUX_ARM64
)
```

## Images from Tarball

Images are loaded from a local tarball, uploaded to ECR by the CDK toolkit and/or your app's CI-CD pipeline, and can be
naturally referenced in your CDK app.

```python
from aws_cdk.aws_ecr_assets import TarballImageAsset


asset = TarballImageAsset(self, "MyBuildImage",
    tarball_file="local-image.tar"
)
```

This will instruct the toolkit to add the tarball as a file asset. During deployment it will load the container image
from `local-image.tar`, push it to an Amazon ECR repository and wire the name of the repository as CloudFormation parameters
to your stack.

## Publishing images to ECR repositories

`DockerImageAsset` is designed for seamless build & consumption of image assets by CDK code deployed to multiple environments
through the CDK CLI or through CI/CD workflows. To that end, the ECR repository behind this construct is controlled by the AWS CDK.
The mechanics of where these images are published and how are intentionally kept as an implementation detail, and the construct
does not support customizations such as specifying the ECR repository name or tags.

If you are looking for a way to *publish* image assets to an ECR repository in your control, you should consider using
[cdklabs/cdk-ecr-deployment](https://github.com/cdklabs/cdk-ecr-deployment), which is able to replicate an image asset from the CDK-controlled ECR repository to a repository of
your choice.

Here an example from the [cdklabs/cdk-ecr-deployment](https://github.com/cdklabs/cdk-ecr-deployment) project:

```text
// This example available in TypeScript only

import { DockerImageAsset } from '@aws-cdk/aws-ecr-assets';
import * as ecrdeploy from 'cdk-ecr-deployment';

const image = new DockerImageAsset(this, 'CDKDockerImage', {
  directory: path.join(__dirname, 'docker'),
});

new ecrdeploy.ECRDeployment(this, 'DeployDockerImage', {
  src: new ecrdeploy.DockerImageName(image.imageUri),
  dest: new ecrdeploy.DockerImageName(`${cdk.Aws.ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/test:nginx`),
});
```

⚠️ Please note that this is a 3rd-party construct library and is not officially supported by AWS.
You are welcome to +1 [this GitHub issue](https://github.com/aws/aws-cdk/issues/12597) if you would like to see
native support for this use-case in the AWS CDK.

## Pull Permissions

Depending on the consumer of your image asset, you will need to make sure
the principal has permissions to pull the image.

In most cases, you should use the `asset.repository.grantPull(principal)`
method. This will modify the IAM policy of the principal to allow it to
pull images from this repository.

If the pulling principal is not in the same account or is an AWS service that
doesn't assume a role in your account (e.g. AWS CodeBuild), pull permissions
must be granted on the **resource policy** (and not on the principal's policy).
To do that, you can use `asset.repository.addToResourcePolicy(statement)` to
grant the desired principal the following permissions: "ecr:GetDownloadUrlForLayer",
"ecr:BatchGetImage" and "ecr:BatchCheckLayerAvailability".
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

import aws_cdk.assets as _aws_cdk_assets_b1c45fb6
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_093ed842
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_assets_b1c45fb6.IAsset)
class DockerImageAsset(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr-assets.DockerImageAsset",
):
    '''An asset that represents a Docker image.

    The image will be created in build time and uploaded to an ECR repository.

    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_ecr_assets import DockerImageAsset, NetworkMode
        
        
        asset = DockerImageAsset(self, "MyBuildImage",
            directory=path.join(__dirname, "my-image"),
            network_mode=NetworkMode.HOST
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        directory: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        invalidation: typing.Optional[typing.Union["DockerImageAssetInvalidationOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        network_mode: typing.Optional["NetworkMode"] = None,
        platform: typing.Optional["Platform"] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param directory: The directory where the Dockerfile is stored. Any directory inside with a name that matches the CDK output folder (cdk.out by default) will be excluded from the asset
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param invalidation: Options to control which parameters are used to invalidate the asset hash. Default: - hash all parameters
        :param network_mode: Networking mode for the RUN commands during build. Support docker API 1.25+. Default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        :param platform: Platform to build for. *Requires Docker Buildx*. Default: - no platform specified (the current machine architecture will be used)
        :param repository_name: (deprecated) ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709c23cf22add049f22005fe24d009e9f9a94f46cedb3b96fa83a41a9ab5eb0c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DockerImageAssetProps(
            directory=directory,
            build_args=build_args,
            file=file,
            invalidation=invalidation,
            network_mode=network_mode,
            platform=platform,
            repository_name=repository_name,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            follow_symlinks=follow_symlinks,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addResourceMetadata")
    def add_resource_metadata(
        self,
        resource: _aws_cdk_core_f4b25747.CfnResource,
        resource_property: builtins.str,
    ) -> None:
        '''Adds CloudFormation template metadata to the specified resource with information that indicates which resource property is mapped to this local asset.

        This can be used by tools such as SAM CLI to provide local
        experience such as local invocation and debugging of Lambda functions.

        Asset metadata will only be included if the stack is synthesized with the
        "aws:cdk:enable-asset-metadata" context key defined, which is the default
        behavior when synthesizing via the CDK Toolkit.

        :param resource: The CloudFormation resource which is using this asset [disable-awslint:ref-via-interface].
        :param resource_property: The property name where this asset is referenced.

        :see: https://github.com/aws/aws-cdk/issues/1432
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4683cf5648de7ae6412503b173f94bfa6269e874c7bab1811cb46787b5a84f66)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_property", value=resource_property, expected_type=type_hints["resource_property"])
        return typing.cast(None, jsii.invoke(self, "addResourceMetadata", [resource, resource_property]))

    @builtins.property
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> builtins.str:
        '''A hash of this asset, which is available at construction time.

        As this is a plain string, it
        can be used in construct IDs in order to enforce creation of a new resource when the content
        hash has changed.
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetHash"))

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        '''(deprecated) A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        :deprecated: use assetHash

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceHash"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        '''The full URI of the image (including a tag).

        Use this reference to pull
        the asset.
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4577d754af388a62037c5b19ecbcd4e7c7e1c3926d390bb177b21deaf9972b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> _aws_cdk_aws_ecr_093ed842.IRepository:
        '''Repository where the image is stored.'''
        return typing.cast(_aws_cdk_aws_ecr_093ed842.IRepository, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: _aws_cdk_aws_ecr_093ed842.IRepository) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291eeaab676dc2b0b50c48214294c484e6342cc20c157fce09247012eb6bc432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr-assets.DockerImageAssetInvalidationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "build_args": "buildArgs",
        "extra_hash": "extraHash",
        "file": "file",
        "network_mode": "networkMode",
        "platform": "platform",
        "repository_name": "repositoryName",
        "target": "target",
    },
)
class DockerImageAssetInvalidationOptions:
    def __init__(
        self,
        *,
        build_args: typing.Optional[builtins.bool] = None,
        extra_hash: typing.Optional[builtins.bool] = None,
        file: typing.Optional[builtins.bool] = None,
        network_mode: typing.Optional[builtins.bool] = None,
        platform: typing.Optional[builtins.bool] = None,
        repository_name: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options to control invalidation of ``DockerImageAsset`` asset hashes.

        :param build_args: Use ``buildArgs`` while calculating the asset hash. Default: true
        :param extra_hash: Use ``extraHash`` while calculating the asset hash. Default: true
        :param file: Use ``file`` while calculating the asset hash. Default: true
        :param network_mode: Use ``networkMode`` while calculating the asset hash. Default: true
        :param platform: Use ``platform`` while calculating the asset hash. Default: true
        :param repository_name: Use ``repositoryName`` while calculating the asset hash. Default: true
        :param target: Use ``target`` while calculating the asset hash. Default: true

        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_ecr_assets import DockerImageAsset
            
            
            asset = DockerImageAsset(self, "MyBuildImage",
                directory=path.join(__dirname, "my-image"),
                build_args={
                    "HTTP_PROXY": "http://10.20.30.2:1234"
                },
                invalidation=DockerImageAssetInvalidationOptions(
                    build_args=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17dcd23665a5eb1e3efebe09bff420ff71a0add8b6006a15d9518e379686a80)
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument extra_hash", value=extra_hash, expected_type=type_hints["extra_hash"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_args is not None:
            self._values["build_args"] = build_args
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if file is not None:
            self._values["file"] = file
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if platform is not None:
            self._values["platform"] = platform
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def build_args(self) -> typing.Optional[builtins.bool]:
        '''Use ``buildArgs`` while calculating the asset hash.

        :default: true
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.bool]:
        '''Use ``extraHash`` while calculating the asset hash.

        :default: true
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.bool]:
        '''Use ``file`` while calculating the asset hash.

        :default: true
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.bool]:
        '''Use ``networkMode`` while calculating the asset hash.

        :default: true
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.bool]:
        '''Use ``platform`` while calculating the asset hash.

        :default: true
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.bool]:
        '''Use ``repositoryName`` while calculating the asset hash.

        :default: true
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.bool]:
        '''Use ``target`` while calculating the asset hash.

        :default: true
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAssetInvalidationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr-assets.DockerImageAssetOptions",
    jsii_struct_bases=[
        _aws_cdk_assets_b1c45fb6.FingerprintOptions,
        _aws_cdk_core_f4b25747.FileFingerprintOptions,
    ],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "follow_symlinks": "followSymlinks",
        "build_args": "buildArgs",
        "file": "file",
        "invalidation": "invalidation",
        "network_mode": "networkMode",
        "platform": "platform",
        "repository_name": "repositoryName",
        "target": "target",
    },
)
class DockerImageAssetOptions(
    _aws_cdk_assets_b1c45fb6.FingerprintOptions,
    _aws_cdk_core_f4b25747.FileFingerprintOptions,
):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        invalidation: typing.Optional[typing.Union[DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        network_mode: typing.Optional["NetworkMode"] = None,
        platform: typing.Optional["Platform"] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for DockerImageAsset.

        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: The ignore behavior to use for exclude patterns. Default: IgnoreMode.GLOB
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param invalidation: Options to control which parameters are used to invalidate the asset hash. Default: - hash all parameters
        :param network_mode: Networking mode for the RUN commands during build. Support docker API 1.25+. Default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        :param platform: Platform to build for. *Requires Docker Buildx*. Default: - no platform specified (the current machine architecture will be used)
        :param repository_name: (deprecated) ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.assets as assets
            import aws_cdk.aws_ecr_assets as ecr_assets
            import aws_cdk.core as cdk
            
            # network_mode: ecr_assets.NetworkMode
            # platform: ecr_assets.Platform
            
            docker_image_asset_options = ecr_assets.DockerImageAssetOptions(
                build_args={
                    "build_args_key": "buildArgs"
                },
                exclude=["exclude"],
                extra_hash="extraHash",
                file="file",
                follow=assets.FollowMode.NEVER,
                follow_symlinks=cdk.SymlinkFollowMode.NEVER,
                ignore_mode=cdk.IgnoreMode.GLOB,
                invalidation=ecr_assets.DockerImageAssetInvalidationOptions(
                    build_args=False,
                    extra_hash=False,
                    file=False,
                    network_mode=False,
                    platform=False,
                    repository_name=False,
                    target=False
                ),
                network_mode=network_mode,
                platform=platform,
                repository_name="repositoryName",
                target="target"
            )
        '''
        if isinstance(invalidation, dict):
            invalidation = DockerImageAssetInvalidationOptions(**invalidation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac835e9861a2cd211c985660477e319754ba6593ad967320698e9263ff04357a)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument extra_hash", value=extra_hash, expected_type=type_hints["extra_hash"])
            check_type(argname="argument follow_symlinks", value=follow_symlinks, expected_type=type_hints["follow_symlinks"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument invalidation", value=invalidation, expected_type=type_hints["invalidation"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if invalidation is not None:
            self._values["invalidation"] = invalidation
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if platform is not None:
            self._values["platform"] = platform
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Glob patterns to exclude from the copy.

        :default: - nothing is excluded
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow(self) -> typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode]:
        '''(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :deprecated: use ``followSymlinks`` instead

        :stability: deprecated
        '''
        result = self._values.get("follow")
        return typing.cast(typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode]:
        '''The ignore behavior to use for exclude patterns.

        :default: IgnoreMode.GLOB
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def follow_symlinks(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode]:
        '''A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        :default: - no build args are passed
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''Path to the Dockerfile (relative to the directory).

        :default: 'Dockerfile'
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invalidation(self) -> typing.Optional[DockerImageAssetInvalidationOptions]:
        '''Options to control which parameters are used to invalidate the asset hash.

        :default: - hash all parameters
        '''
        result = self._values.get("invalidation")
        return typing.cast(typing.Optional[DockerImageAssetInvalidationOptions], result)

    @builtins.property
    def network_mode(self) -> typing.Optional["NetworkMode"]:
        '''Networking mode for the RUN commands during build.

        Support docker API 1.25+.

        :default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional["NetworkMode"], result)

    @builtins.property
    def platform(self) -> typing.Optional["Platform"]:
        '''Platform to build for.

        *Requires Docker Buildx*.

        :default: - no platform specified (the current machine architecture will be used)
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional["Platform"], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        :default: - the default ECR repository for CDK assets

        :deprecated:

        to control the location of docker image assets, please override
        ``Stack.addDockerImageAsset``. this feature will be removed in future
        releases.

        :stability: deprecated
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docker target to build to.

        :default: - no target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAssetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr-assets.DockerImageAssetProps",
    jsii_struct_bases=[DockerImageAssetOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "follow_symlinks": "followSymlinks",
        "build_args": "buildArgs",
        "file": "file",
        "invalidation": "invalidation",
        "network_mode": "networkMode",
        "platform": "platform",
        "repository_name": "repositoryName",
        "target": "target",
        "directory": "directory",
    },
)
class DockerImageAssetProps(DockerImageAssetOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        invalidation: typing.Optional[typing.Union[DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        network_mode: typing.Optional["NetworkMode"] = None,
        platform: typing.Optional["Platform"] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        directory: builtins.str,
    ) -> None:
        '''Props for DockerImageAssets.

        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: The ignore behavior to use for exclude patterns. Default: IgnoreMode.GLOB
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param invalidation: Options to control which parameters are used to invalidate the asset hash. Default: - hash all parameters
        :param network_mode: Networking mode for the RUN commands during build. Support docker API 1.25+. Default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        :param platform: Platform to build for. *Requires Docker Buildx*. Default: - no platform specified (the current machine architecture will be used)
        :param repository_name: (deprecated) ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param directory: The directory where the Dockerfile is stored. Any directory inside with a name that matches the CDK output folder (cdk.out by default) will be excluded from the asset

        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_ecr_assets import DockerImageAsset
            
            
            asset = DockerImageAsset(self, "MyBuildImage",
                directory=path.join(__dirname, "my-image"),
                build_args={
                    "HTTP_PROXY": "http://10.20.30.2:1234"
                },
                invalidation=DockerImageAssetInvalidationOptions(
                    build_args=False
                )
            )
        '''
        if isinstance(invalidation, dict):
            invalidation = DockerImageAssetInvalidationOptions(**invalidation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0bcd95c437ed71516fb943960a885df385ad9885382ee2220249bd5b7d63c3)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument extra_hash", value=extra_hash, expected_type=type_hints["extra_hash"])
            check_type(argname="argument follow_symlinks", value=follow_symlinks, expected_type=type_hints["follow_symlinks"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument invalidation", value=invalidation, expected_type=type_hints["invalidation"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory": directory,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if invalidation is not None:
            self._values["invalidation"] = invalidation
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if platform is not None:
            self._values["platform"] = platform
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Glob patterns to exclude from the copy.

        :default: - nothing is excluded
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow(self) -> typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode]:
        '''(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :deprecated: use ``followSymlinks`` instead

        :stability: deprecated
        '''
        result = self._values.get("follow")
        return typing.cast(typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode]:
        '''The ignore behavior to use for exclude patterns.

        :default: IgnoreMode.GLOB
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def follow_symlinks(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode]:
        '''A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        :default: - no build args are passed
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''Path to the Dockerfile (relative to the directory).

        :default: 'Dockerfile'
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invalidation(self) -> typing.Optional[DockerImageAssetInvalidationOptions]:
        '''Options to control which parameters are used to invalidate the asset hash.

        :default: - hash all parameters
        '''
        result = self._values.get("invalidation")
        return typing.cast(typing.Optional[DockerImageAssetInvalidationOptions], result)

    @builtins.property
    def network_mode(self) -> typing.Optional["NetworkMode"]:
        '''Networking mode for the RUN commands during build.

        Support docker API 1.25+.

        :default: - no networking mode specified (the default networking mode ``NetworkMode.DEFAULT`` will be used)
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional["NetworkMode"], result)

    @builtins.property
    def platform(self) -> typing.Optional["Platform"]:
        '''Platform to build for.

        *Requires Docker Buildx*.

        :default: - no platform specified (the current machine architecture will be used)
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional["Platform"], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        :default: - the default ECR repository for CDK assets

        :deprecated:

        to control the location of docker image assets, please override
        ``Stack.addDockerImageAsset``. this feature will be removed in future
        releases.

        :stability: deprecated
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docker target to build to.

        :default: - no target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory(self) -> builtins.str:
        '''The directory where the Dockerfile is stored.

        Any directory inside with a name that matches the CDK output folder (cdk.out by default) will be excluded from the asset
        '''
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkMode(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr-assets.NetworkMode",
):
    '''networking mode on build time supported by docker.

    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_ecr_assets import DockerImageAsset, NetworkMode
        
        
        asset = DockerImageAsset(self, "MyBuildImage",
            directory=path.join(__dirname, "my-image"),
            network_mode=NetworkMode.HOST
        )
    '''

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, mode: builtins.str) -> "NetworkMode":
        '''Used to specify a custom networking mode Use this if the networking mode name is not yet supported by the CDK.

        :param mode: The networking mode to use for docker build.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a09f6c95a1cdf809479d3304a1c866d111a83ba941cde755a70a53c36d2b75)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        return typing.cast("NetworkMode", jsii.sinvoke(cls, "custom", [mode]))

    @jsii.member(jsii_name="fromContainer")
    @builtins.classmethod
    def from_container(cls, container_id: builtins.str) -> "NetworkMode":
        '''Reuse another container's network stack.

        :param container_id: The target container's id or name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc44ce07f98410bd9ba2a99b24df3ba5201ea415e625375aa1ded6b54086bc83)
            check_type(argname="argument container_id", value=container_id, expected_type=type_hints["container_id"])
        return typing.cast("NetworkMode", jsii.sinvoke(cls, "fromContainer", [container_id]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT")
    def DEFAULT(cls) -> "NetworkMode":
        '''The default networking mode if omitted, create a network stack on the default Docker bridge.'''
        return typing.cast("NetworkMode", jsii.sget(cls, "DEFAULT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HOST")
    def HOST(cls) -> "NetworkMode":
        '''Use the Docker host network stack.'''
        return typing.cast("NetworkMode", jsii.sget(cls, "HOST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NONE")
    def NONE(cls) -> "NetworkMode":
        '''Disable the network stack, only the loopback device will be created.'''
        return typing.cast("NetworkMode", jsii.sget(cls, "NONE"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        '''The networking mode to use for docker build.'''
        return typing.cast(builtins.str, jsii.get(self, "mode"))


class Platform(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecr-assets.Platform"):
    '''platform supported by docker.

    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_ecr_assets import DockerImageAsset, Platform
        
        
        asset = DockerImageAsset(self, "MyBuildImage",
            directory=path.join(__dirname, "my-image"),
            platform=Platform.LINUX_ARM64
        )
    '''

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, platform: builtins.str) -> "Platform":
        '''Used to specify a custom platform Use this if the platform name is not yet supported by the CDK.

        :param platform: The platform to use for docker build.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af37d4e80aa0d5188455e208b63c1e344f0ef8445d0e69d8a0667bdf2a7d2515)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
        return typing.cast("Platform", jsii.sinvoke(cls, "custom", [platform]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_AMD64")
    def LINUX_AMD64(cls) -> "Platform":
        '''Build for linux/amd64.'''
        return typing.cast("Platform", jsii.sget(cls, "LINUX_AMD64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_ARM64")
    def LINUX_ARM64(cls) -> "Platform":
        '''Build for linux/arm64.'''
        return typing.cast("Platform", jsii.sget(cls, "LINUX_ARM64"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        '''The platform to use for docker build.'''
        return typing.cast(builtins.str, jsii.get(self, "platform"))


@jsii.implements(_aws_cdk_assets_b1c45fb6.IAsset)
class TarballImageAsset(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr-assets.TarballImageAsset",
):
    '''An asset that represents a Docker image.

    The image will loaded from an existing tarball and uploaded to an ECR repository.

    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_ecr_assets import TarballImageAsset
        
        
        asset = TarballImageAsset(self, "MyBuildImage",
            tarball_file="local-image.tar"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        tarball_file: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param tarball_file: Absolute path to the tarball. It is recommended to to use the script running directory (e.g. ``__dirname`` in Node.js projects or dirname of ``__file__`` in Python) if your tarball is located as a resource inside your project.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3745ae0608923542be7ddc86e217bd7a121e5ba442268949ed0530f3fcf09fe0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TarballImageAssetProps(tarball_file=tarball_file)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> builtins.str:
        '''A hash of this asset, which is available at construction time.

        As this is a plain string, it
        can be used in construct IDs in order to enforce creation of a new resource when the content
        hash has changed.
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetHash"))

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        '''(deprecated) A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        :deprecated: use assetHash

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceHash"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        '''The full URI of the image (including a tag).

        Use this reference to pull
        the asset.
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b1340304a4d9964cefc0496a14378b2e4cd3eaa2b7ecdbac989e1492f8049b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> _aws_cdk_aws_ecr_093ed842.IRepository:
        '''Repository where the image is stored.'''
        return typing.cast(_aws_cdk_aws_ecr_093ed842.IRepository, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: _aws_cdk_aws_ecr_093ed842.IRepository) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67dc4808cec4cf66f0616595c0b38bf5805a28d1e368f61cd37194236066b197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr-assets.TarballImageAssetProps",
    jsii_struct_bases=[],
    name_mapping={"tarball_file": "tarballFile"},
)
class TarballImageAssetProps:
    def __init__(self, *, tarball_file: builtins.str) -> None:
        '''Options for TarballImageAsset.

        :param tarball_file: Absolute path to the tarball. It is recommended to to use the script running directory (e.g. ``__dirname`` in Node.js projects or dirname of ``__file__`` in Python) if your tarball is located as a resource inside your project.

        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_ecr_assets import TarballImageAsset
            
            
            asset = TarballImageAsset(self, "MyBuildImage",
                tarball_file="local-image.tar"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2da8884b6ac125af79035b3956fd1d762d74b26fb4e755aecccf16151bdb14)
            check_type(argname="argument tarball_file", value=tarball_file, expected_type=type_hints["tarball_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tarball_file": tarball_file,
        }

    @builtins.property
    def tarball_file(self) -> builtins.str:
        '''Absolute path to the tarball.

        It is recommended to to use the script running directory (e.g. ``__dirname``
        in Node.js projects or dirname of ``__file__`` in Python) if your tarball
        is located as a resource inside your project.
        '''
        result = self._values.get("tarball_file")
        assert result is not None, "Required property 'tarball_file' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TarballImageAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DockerImageAsset",
    "DockerImageAssetInvalidationOptions",
    "DockerImageAssetOptions",
    "DockerImageAssetProps",
    "NetworkMode",
    "Platform",
    "TarballImageAsset",
    "TarballImageAssetProps",
]

publication.publish()

def _typecheckingstub__709c23cf22add049f22005fe24d009e9f9a94f46cedb3b96fa83a41a9ab5eb0c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    directory: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file: typing.Optional[builtins.str] = None,
    invalidation: typing.Optional[typing.Union[DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    network_mode: typing.Optional[NetworkMode] = None,
    platform: typing.Optional[Platform] = None,
    repository_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    extra_hash: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4683cf5648de7ae6412503b173f94bfa6269e874c7bab1811cb46787b5a84f66(
    resource: _aws_cdk_core_f4b25747.CfnResource,
    resource_property: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4577d754af388a62037c5b19ecbcd4e7c7e1c3926d390bb177b21deaf9972b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291eeaab676dc2b0b50c48214294c484e6342cc20c157fce09247012eb6bc432(
    value: _aws_cdk_aws_ecr_093ed842.IRepository,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17dcd23665a5eb1e3efebe09bff420ff71a0add8b6006a15d9518e379686a80(
    *,
    build_args: typing.Optional[builtins.bool] = None,
    extra_hash: typing.Optional[builtins.bool] = None,
    file: typing.Optional[builtins.bool] = None,
    network_mode: typing.Optional[builtins.bool] = None,
    platform: typing.Optional[builtins.bool] = None,
    repository_name: typing.Optional[builtins.bool] = None,
    target: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac835e9861a2cd211c985660477e319754ba6593ad967320698e9263ff04357a(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    extra_hash: typing.Optional[builtins.str] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file: typing.Optional[builtins.str] = None,
    invalidation: typing.Optional[typing.Union[DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    network_mode: typing.Optional[NetworkMode] = None,
    platform: typing.Optional[Platform] = None,
    repository_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0bcd95c437ed71516fb943960a885df385ad9885382ee2220249bd5b7d63c3(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    extra_hash: typing.Optional[builtins.str] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file: typing.Optional[builtins.str] = None,
    invalidation: typing.Optional[typing.Union[DockerImageAssetInvalidationOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    network_mode: typing.Optional[NetworkMode] = None,
    platform: typing.Optional[Platform] = None,
    repository_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a09f6c95a1cdf809479d3304a1c866d111a83ba941cde755a70a53c36d2b75(
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc44ce07f98410bd9ba2a99b24df3ba5201ea415e625375aa1ded6b54086bc83(
    container_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af37d4e80aa0d5188455e208b63c1e344f0ef8445d0e69d8a0667bdf2a7d2515(
    platform: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3745ae0608923542be7ddc86e217bd7a121e5ba442268949ed0530f3fcf09fe0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    tarball_file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b1340304a4d9964cefc0496a14378b2e4cd3eaa2b7ecdbac989e1492f8049b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67dc4808cec4cf66f0616595c0b38bf5805a28d1e368f61cd37194236066b197(
    value: _aws_cdk_aws_ecr_093ed842.IRepository,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2da8884b6ac125af79035b3956fd1d762d74b26fb4e755aecccf16151bdb14(
    *,
    tarball_file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
