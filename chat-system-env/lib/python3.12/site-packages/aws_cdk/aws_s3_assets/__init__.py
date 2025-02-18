'''
# AWS CDK Assets

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

Assets are local files or directories which are needed by a CDK app. A common
example is a directory which contains the handler code for a Lambda function,
but assets can represent any artifact that is needed for the app's operation.

When deploying a CDK app that includes constructs with assets, the CDK toolkit
will first upload all the assets to S3, and only then deploy the stacks. The S3
locations of the uploaded assets will be passed in as CloudFormation Parameters
to the relevant stacks.

The following JavaScript example defines a directory asset which is archived as
a .zip file and uploaded to S3 during deployment.

```python
asset = assets.Asset(self, "SampleAsset",
    path=path.join(__dirname, "sample-asset-directory")
)
```

The following JavaScript example defines a file asset, which is uploaded as-is
to an S3 bucket during deployment.

```python
asset = assets.Asset(self, "SampleAsset",
    path=path.join(__dirname, "file-asset.txt")
)
```

## Attributes

`Asset` constructs expose the following deploy-time attributes:

* `s3BucketName` - the name of the assets S3 bucket.
* `s3ObjectKey` - the S3 object key of the asset file (whether it's a file or a zip archive)
* `s3ObjectUrl` - the S3 object URL of the asset (i.e. s3://mybucket/mykey.zip)
* `httpUrl` - the S3 HTTP URL of the asset (i.e. https://s3.us-east-1.amazonaws.com/mybucket/mykey.zip)

In the following example, the various asset attributes are exported as stack outputs:

```python
asset = assets.Asset(self, "SampleAsset",
    path=path.join(__dirname, "sample-asset-directory")
)

cdk.CfnOutput(self, "S3BucketName", value=asset.s3_bucket_name)
cdk.CfnOutput(self, "S3ObjectKey", value=asset.s3_object_key)
cdk.CfnOutput(self, "S3HttpURL", value=asset.http_url)
cdk.CfnOutput(self, "S3ObjectURL", value=asset.s3_object_url)
```

## Permissions

IAM roles, users or groups which need to be able to read assets in runtime will should be
granted IAM permissions. To do that use the `asset.grantRead(principal)` method:

The following example grants an IAM group read permissions on an asset:

```python
group = iam.Group(self, "MyUserGroup")
asset.grant_read(group)
```

## How does it work

When an asset is defined in a construct, a construct metadata entry
`aws:cdk:asset` is emitted with instructions on where to find the asset and what
type of packaging to perform (`zip` or `file`). Furthermore, the synthesized
CloudFormation template will also include two CloudFormation parameters: one for
the asset's bucket and one for the asset S3 key. Those parameters are used to
reference the deploy-time values of the asset (using `{ Ref: "Param" }`).

Then, when the stack is deployed, the toolkit will package the asset (i.e. zip
the directory), calculate an MD5 hash of the contents and will render an S3 key
for this asset within the toolkit's asset store. If the file doesn't exist in
the asset store, it is uploaded during deployment.

> The toolkit's asset store is an S3 bucket created by the toolkit for each
> environment the toolkit operates in (environment = account + region).

Now, when the toolkit deploys the stack, it will set the relevant CloudFormation
Parameters to point to the actual bucket and key for each asset.

## Asset Bundling

When defining an asset, you can use the `bundling` option to specify a command
to run inside a docker container. The command can read the contents of the asset
source from `/asset-input` and is expected to write files under `/asset-output`
(directories mapped inside the container). The files under `/asset-output` will
be zipped and uploaded to S3 as the asset.

The following example uses custom asset bundling to convert a markdown file to html:

```python
asset = assets.Asset(self, "BundledAsset",
    path=path.join(__dirname, "markdown-asset"),  # /asset-input and working directory in the container
    bundling=BundlingOptions(
        image=DockerImage.from_build(path.join(__dirname, "alpine-markdown")),  # Build an image
        command=["sh", "-c", """
                        markdown index.md > /asset-output/index.html
                      """
        ]
    )
)
```

The bundling docker image (`image`) can either come from a registry (`DockerImage.fromRegistry`)
or it can be built from a `Dockerfile` located inside your project (`DockerImage.fromBuild`).

You can set the `CDK_DOCKER` environment variable in order to provide a custom
docker program to execute. This may sometime be needed when building in
environments where the standard docker cannot be executed (see
https://github.com/aws/aws-cdk/issues/8460 for details).

Use `local` to specify a local bundling provider. The provider implements a
method `tryBundle()` which should return `true` if local bundling was performed.
If `false` is returned, docker bundling will be done:

```python
@jsii.implements(ILocalBundling)
class MyBundle:
    def try_bundle(self, output_dir, *, image, entrypoint=None, command=None, volumes=None, environment=None, workingDirectory=None, user=None, local=None, outputType=None, securityOpt=None):
        can_run_locally = True # replace with actual logic
        if can_run_locally:
            # perform local bundling here
            return True
        return False

assets.Asset(self, "BundledAsset",
    path="/path/to/asset",
    bundling=BundlingOptions(
        local=MyBundle(),
        # Docker bundling fallback
        image=DockerImage.from_registry("alpine"),
        entrypoint=["/bin/sh", "-c"],
        command=["bundle"]
    )
)
```

Although optional, it's recommended to provide a local bundling method which can
greatly improve performance.

If the bundling output contains a single archive file (zip or jar) it will be
uploaded to S3 as-is and will not be zipped. Otherwise the contents of the
output directory will be zipped and the zip file will be uploaded to S3. This
is the default behavior for `bundling.outputType` (`BundlingOutput.AUTO_DISCOVER`).

Use `BundlingOutput.NOT_ARCHIVED` if the bundling output must always be zipped:

```python
asset = assets.Asset(self, "BundledAsset",
    path="/path/to/asset",
    bundling=BundlingOptions(
        image=DockerImage.from_registry("alpine"),
        command=["command-that-produces-an-archive.sh"],
        output_type=BundlingOutput.NOT_ARCHIVED
    )
)
```

Use `BundlingOutput.ARCHIVED` if the bundling output contains a single archive file and
you don't want it to be zipped.

## CloudFormation Resource Metadata

> NOTE: This section is relevant for authors of AWS Resource Constructs.

In certain situations, it is desirable for tools to be able to know that a certain CloudFormation
resource is using a local asset. For example, SAM CLI can be used to invoke AWS Lambda functions
locally for debugging purposes.

To enable such use cases, external tools will consult a set of metadata entries on AWS CloudFormation
resources:

* `aws:asset:path` points to the local path of the asset.
* `aws:asset:property` is the name of the resource property where the asset is used

Using these two metadata entries, tools will be able to identify that assets are used
by a certain resource, and enable advanced local experiences.

To add these metadata entries to a resource, use the
`asset.addResourceMetadata(resource, property)` method.

See https://github.com/aws/aws-cdk/issues/1432 for more details
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
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_core_f4b25747.IAsset)
class Asset(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3-assets.Asset",
):
    '''An asset represents a local file or directory, which is automatically uploaded to S3 and then can be referenced within a CDK application.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_s3_assets as s3_assets
        
        # cluster: eks.Cluster
        
        chart_asset = s3_assets.Asset(self, "ChartAsset",
            path="/path/to/asset"
        )
        
        cluster.add_helm_chart("test-chart",
            chart_asset=chart_asset
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371efbe09ba74d7b5c93abee259d17859b58586965fa485eca285928e19c7db1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AssetProps(
            path=path,
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            follow_symlinks=follow_symlinks,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
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
        :param resource_property: The property name where this asset is referenced (e.g. "Code" for AWS::Lambda::Function).

        :see: https://github.com/aws/aws-cdk/issues/1432
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e45727fb49da620ab5e9c9ba4a7b0de6956a25be2a089f62e090cd0d4221fd68)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_property", value=resource_property, expected_type=type_hints["resource_property"])
        return typing.cast(None, jsii.invoke(self, "addResourceMetadata", [resource, resource_property]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable) -> None:
        '''Grants read permissions to the principal on the assets bucket.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1ed74733ef9f040c6e435ac79bddf1c109faacc4983456034d22ed4586cafc)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee]))

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
    @jsii.member(jsii_name="assetPath")
    def asset_path(self) -> builtins.str:
        '''The path to the asset, relative to the current Cloud Assembly.

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetPath"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_55f001a5.IBucket:
        '''The S3 bucket in which this asset resides.'''
        return typing.cast(_aws_cdk_aws_s3_55f001a5.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="httpUrl")
    def http_url(self) -> builtins.str:
        '''Attribute which represents the S3 HTTP URL of this asset.

        For example, ``https://s3.us-west-1.amazonaws.com/bucket/key``
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpUrl"))

    @builtins.property
    @jsii.member(jsii_name="isFile")
    def is_file(self) -> builtins.bool:
        '''Indicates if this asset is a single file.

        Allows constructs to ensure that the
        correct file type was used.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isFile"))

    @builtins.property
    @jsii.member(jsii_name="isZipArchive")
    def is_zip_archive(self) -> builtins.bool:
        '''Indicates if this asset is a zip archive.

        Allows constructs to ensure that the
        correct file type was used.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isZipArchive"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        '''Attribute that represents the name of the bucket this asset exists in.'''
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @builtins.property
    @jsii.member(jsii_name="s3ObjectKey")
    def s3_object_key(self) -> builtins.str:
        '''Attribute which represents the S3 object key of this asset.'''
        return typing.cast(builtins.str, jsii.get(self, "s3ObjectKey"))

    @builtins.property
    @jsii.member(jsii_name="s3ObjectUrl")
    def s3_object_url(self) -> builtins.str:
        '''Attribute which represents the S3 URL of this asset.

        For example, ``s3://bucket/key``
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3ObjectUrl"))

    @builtins.property
    @jsii.member(jsii_name="s3Url")
    def s3_url(self) -> builtins.str:
        '''(deprecated) Attribute which represents the S3 URL of this asset.

        :deprecated: use ``httpUrl``

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Url"))

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        '''(deprecated) A cryptographic hash of the asset.

        :deprecated: see ``assetHash``

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceHash"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3-assets.AssetOptions",
    jsii_struct_bases=[
        _aws_cdk_assets_b1c45fb6.CopyOptions,
        _aws_cdk_core_f4b25747.FileCopyOptions,
        _aws_cdk_core_f4b25747.AssetOptions,
    ],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "follow_symlinks": "followSymlinks",
        "asset_hash": "assetHash",
        "asset_hash_type": "assetHashType",
        "bundling": "bundling",
        "readers": "readers",
        "source_hash": "sourceHash",
    },
)
class AssetOptions(
    _aws_cdk_assets_b1c45fb6.CopyOptions,
    _aws_cdk_core_f4b25747.FileCopyOptions,
    _aws_cdk_core_f4b25747.AssetOptions,
):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
        source_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: The ignore behavior to use for exclude patterns. Default: IgnoreMode.GLOB
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.

        :exampleMetadata: infused

        Example::

            lambda_.Function(self, "Function",
                code=lambda_.Code.from_asset(path.join(__dirname, "my-python-handler"),
                    bundling=BundlingOptions(
                        image=lambda_.Runtime.PYTHON_3_9.bundling_image,
                        command=["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                        ]
                    )
                ),
                runtime=lambda_.Runtime.PYTHON_3_9,
                handler="index.handler"
            )
        '''
        if isinstance(bundling, dict):
            bundling = _aws_cdk_core_f4b25747.BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a47492610c554a6c8d07bf426d502afa0db882e9d86e33c9602607163c728ee)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument follow_symlinks", value=follow_symlinks, expected_type=type_hints["follow_symlinks"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument asset_hash_type", value=asset_hash_type, expected_type=type_hints["asset_hash_type"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument readers", value=readers, expected_type=type_hints["readers"])
            check_type(argname="argument source_hash", value=source_hash, expected_type=type_hints["source_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None:
            self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None:
            self._values["bundling"] = bundling
        if readers is not None:
            self._values["readers"] = readers
        if source_hash is not None:
            self._values["source_hash"] = source_hash

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
    def follow_symlinks(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode]:
        '''A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        :default: - based on ``assetHashType``
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_aws_cdk_core_f4b25747.AssetHashType]:
        '''Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
        explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        '''
        result = self._values.get("asset_hash_type")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.AssetHashType], result)

    @builtins.property
    def bundling(self) -> typing.Optional[_aws_cdk_core_f4b25747.BundlingOptions]:
        '''Bundle the asset by executing a command in a Docker container or a custom bundling provider.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
        archived into a .zip file and uploaded to S3 otherwise
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.BundlingOptions], result)

    @builtins.property
    def readers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.IGrantable]]:
        '''A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        :default: - No principals that can read file asset.
        '''
        result = self._values.get("readers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.IGrantable]], result)

    @builtins.property
    def source_hash(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Custom hash to use when identifying the specific version of the asset.

        For consistency,
        this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be
        the asset hash.

        NOTE: the source hash is used in order to identify a specific revision of the asset,
        and used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the source hash,
        you will need to make sure it is updated every time the source changes, or otherwise
        it is possible that some deployments will not be invalidated.

        :default:

        - automatically calculate source hash based on the contents
        of the source file or directory.

        :deprecated: see ``assetHash`` and ``assetHashType``

        :stability: deprecated
        '''
        result = self._values.get("source_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3-assets.AssetProps",
    jsii_struct_bases=[AssetOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "follow_symlinks": "followSymlinks",
        "asset_hash": "assetHash",
        "asset_hash_type": "assetHashType",
        "bundling": "bundling",
        "readers": "readers",
        "source_hash": "sourceHash",
        "path": "path",
    },
)
class AssetProps(AssetOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
        follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        path: builtins.str,
    ) -> None:
        '''
        :param exclude: Glob patterns to exclude from the copy. Default: - nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: The ignore behavior to use for exclude patterns. Default: IgnoreMode.GLOB
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.

        :exampleMetadata: lit=test/integ.assets.bundling.lit.ts infused

        Example::

            asset = assets.Asset(self, "BundledAsset",
                path=path.join(__dirname, "markdown-asset"),  # /asset-input and working directory in the container
                bundling=BundlingOptions(
                    image=DockerImage.from_build(path.join(__dirname, "alpine-markdown")),  # Build an image
                    command=["sh", "-c", """
                                    markdown index.md > /asset-output/index.html
                                  """
                    ]
                )
            )
        '''
        if isinstance(bundling, dict):
            bundling = _aws_cdk_core_f4b25747.BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba50a2a296de1bf05b13a925970fcbc5590519c848189da620d8cfc10aa70e9e)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument ignore_mode", value=ignore_mode, expected_type=type_hints["ignore_mode"])
            check_type(argname="argument follow_symlinks", value=follow_symlinks, expected_type=type_hints["follow_symlinks"])
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument asset_hash_type", value=asset_hash_type, expected_type=type_hints["asset_hash_type"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument readers", value=readers, expected_type=type_hints["readers"])
            check_type(argname="argument source_hash", value=source_hash, expected_type=type_hints["source_hash"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if follow_symlinks is not None:
            self._values["follow_symlinks"] = follow_symlinks
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None:
            self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None:
            self._values["bundling"] = bundling
        if readers is not None:
            self._values["readers"] = readers
        if source_hash is not None:
            self._values["source_hash"] = source_hash

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
    def follow_symlinks(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode]:
        '''A strategy for how to handle symlinks.

        :default: SymlinkFollowMode.NEVER
        '''
        result = self._values.get("follow_symlinks")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode], result)

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        :default: - based on ``assetHashType``
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_aws_cdk_core_f4b25747.AssetHashType]:
        '''Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
        explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        '''
        result = self._values.get("asset_hash_type")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.AssetHashType], result)

    @builtins.property
    def bundling(self) -> typing.Optional[_aws_cdk_core_f4b25747.BundlingOptions]:
        '''Bundle the asset by executing a command in a Docker container or a custom bundling provider.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
        archived into a .zip file and uploaded to S3 otherwise
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.BundlingOptions], result)

    @builtins.property
    def readers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.IGrantable]]:
        '''A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        :default: - No principals that can read file asset.
        '''
        result = self._values.get("readers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_940a1ce0.IGrantable]], result)

    @builtins.property
    def source_hash(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Custom hash to use when identifying the specific version of the asset.

        For consistency,
        this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be
        the asset hash.

        NOTE: the source hash is used in order to identify a specific revision of the asset,
        and used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the source hash,
        you will need to make sure it is updated every time the source changes, or otherwise
        it is possible that some deployments will not be invalidated.

        :default:

        - automatically calculate source hash based on the contents
        of the source file or directory.

        :deprecated: see ``assetHash`` and ``assetHashType``

        :stability: deprecated
        '''
        result = self._values.get("source_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The disk location of the asset.

        The path should refer to one of the following:

        - A regular file or a .zip file, in which case the file will be uploaded as-is to S3.
        - A directory, in which case it will be archived into a .zip file and uploaded to S3.
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Asset",
    "AssetOptions",
    "AssetProps",
]

publication.publish()

def _typecheckingstub__371efbe09ba74d7b5c93abee259d17859b58586965fa485eca285928e19c7db1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    path: builtins.str,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
    source_hash: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45727fb49da620ab5e9c9ba4a7b0de6956a25be2a089f62e090cd0d4221fd68(
    resource: _aws_cdk_core_f4b25747.CfnResource,
    resource_property: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1ed74733ef9f040c6e435ac79bddf1c109faacc4983456034d22ed4586cafc(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a47492610c554a6c8d07bf426d502afa0db882e9d86e33c9602607163c728ee(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
    source_hash: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba50a2a296de1bf05b13a925970fcbc5590519c848189da620d8cfc10aa70e9e(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_aws_cdk_assets_b1c45fb6.FollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_core_f4b25747.IgnoreMode] = None,
    follow_symlinks: typing.Optional[_aws_cdk_core_f4b25747.SymlinkFollowMode] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_core_f4b25747.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_940a1ce0.IGrantable]] = None,
    source_hash: typing.Optional[builtins.str] = None,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
