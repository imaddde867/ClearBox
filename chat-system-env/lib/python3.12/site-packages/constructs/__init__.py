'''
# Constructs

> Software-defined persistent state

![Release](https://github.com/aws/constructs/workflows/Release/badge.svg)
[![npm version](https://badge.fury.io/js/constructs.svg)](https://badge.fury.io/js/constructs)
[![PyPI version](https://badge.fury.io/py/constructs.svg)](https://badge.fury.io/py/constructs)
[![NuGet version](https://badge.fury.io/nu/Constructs.svg)](https://badge.fury.io/nu/Constructs)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/software.constructs/constructs/badge.svg?style=plastic)](https://maven-badges.herokuapp.com/maven-central/software.constructs/constructs)

## What are constructs?

Constructs are classes which define a "piece of system state". Constructs can be composed together to form higher-level building blocks which represent more complex state.

Constructs are often used to represent the *desired state* of cloud applications. For example, in the AWS CDK, which is used to define the desired state for AWS infrastructure using CloudFormation, the lowest-level construct represents a *resource definition* in a CloudFormation template. These resources are composed to represent higher-level logical units of a cloud application, etc.

## Contributing

This project has adopted the [Amazon Open Source Code of
Conduct](https://aws.github.io/code-of-conduct).

We welcome community contributions and pull requests. See our [contribution
guide](./CONTRIBUTING.md) for more information on how to report issues, set up a
development environment and submit code.

## License

This project is distributed under the [Apache License, Version 2.0](./LICENSE).
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


class ConstructMetadata(
    metaclass=jsii.JSIIMeta,
    jsii_type="constructs.ConstructMetadata",
):
    '''Metadata keys used by constructs.'''

    @jsii.python.classproperty
    @jsii.member(jsii_name="DISABLE_STACK_TRACE_IN_METADATA")
    def DISABLE_STACK_TRACE_IN_METADATA(cls) -> builtins.str:
        '''If set in the construct's context, omits stack traces from metadata entries.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DISABLE_STACK_TRACE_IN_METADATA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ERROR_METADATA_KEY")
    def ERROR_METADATA_KEY(cls) -> builtins.str:
        '''Context type for error level messages.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ERROR_METADATA_KEY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INFO_METADATA_KEY")
    def INFO_METADATA_KEY(cls) -> builtins.str:
        '''Context type for info level messages.'''
        return typing.cast(builtins.str, jsii.sget(cls, "INFO_METADATA_KEY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WARNING_METADATA_KEY")
    def WARNING_METADATA_KEY(cls) -> builtins.str:
        '''Context type for warning level messages.'''
        return typing.cast(builtins.str, jsii.sget(cls, "WARNING_METADATA_KEY"))


@jsii.data_type(
    jsii_type="constructs.ConstructOptions",
    jsii_struct_bases=[],
    name_mapping={"node_factory": "nodeFactory"},
)
class ConstructOptions:
    def __init__(self, *, node_factory: typing.Optional["INodeFactory"] = None) -> None:
        '''Options for creating constructs.

        :param node_factory: A factory for attaching ``Node``s to the construct. Default: - the default ``Node`` is associated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1012f6773721d1c461d9ac99fdffb6683206f6792321e9ee786f5a574378e0e)
            check_type(argname="argument node_factory", value=node_factory, expected_type=type_hints["node_factory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_factory is not None:
            self._values["node_factory"] = node_factory

    @builtins.property
    def node_factory(self) -> typing.Optional["INodeFactory"]:
        '''A factory for attaching ``Node``s to the construct.

        :default: - the default ``Node`` is associated
        '''
        result = self._values.get("node_factory")
        return typing.cast(typing.Optional["INodeFactory"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstructOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="constructs.ConstructOrder")
class ConstructOrder(enum.Enum):
    '''In what order to return constructs.'''

    PREORDER = "PREORDER"
    '''Depth-first, pre-order.'''
    POSTORDER = "POSTORDER"
    '''Depth-first, post-order (leaf nodes first).'''


@jsii.data_type(
    jsii_type="constructs.Dependency",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "target": "target"},
)
class Dependency:
    def __init__(self, *, source: "IConstruct", target: "IConstruct") -> None:
        '''A single dependency.

        :param source: Source the dependency.
        :param target: Target of the dependency.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538d4a9d29db75f4dde4d525a17b8a1f69c206a824be508b9771e98cb1c66519)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }

    @builtins.property
    def source(self) -> "IConstruct":
        '''Source the dependency.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("IConstruct", result)

    @builtins.property
    def target(self) -> "IConstruct":
        '''Target of the dependency.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("IConstruct", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Dependency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="constructs.IAspect")
class IAspect(typing_extensions.Protocol):
    '''Represents an Aspect.'''

    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        ...


class _IAspectProxy:
    '''Represents an Aspect.'''

    __jsii_type__: typing.ClassVar[str] = "constructs.IAspect"

    @jsii.member(jsii_name="visit")
    def visit(self, node: "IConstruct") -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223778a82b7624d4bc9dc5758be8c71d16c0440da8dd252e2097e3f5b95aa433)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAspect).__jsii_proxy_class__ = lambda : _IAspectProxy


@jsii.interface(jsii_type="constructs.IConstruct")
class IConstruct(typing_extensions.Protocol):
    '''Represents a construct.'''

    pass


class _IConstructProxy:
    '''Represents a construct.'''

    __jsii_type__: typing.ClassVar[str] = "constructs.IConstruct"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConstruct).__jsii_proxy_class__ = lambda : _IConstructProxy


@jsii.interface(jsii_type="constructs.INodeFactory")
class INodeFactory(typing_extensions.Protocol):
    '''A factory for attaching ``Node``s to the construct.'''

    @jsii.member(jsii_name="createNode")
    def create_node(
        self,
        host: "Construct",
        scope: IConstruct,
        id: builtins.str,
    ) -> "Node":
        '''Returns a new ``Node`` associated with ``host``.

        :param host: the associated construct.
        :param scope: the construct's scope (parent).
        :param id: the construct id.
        '''
        ...


class _INodeFactoryProxy:
    '''A factory for attaching ``Node``s to the construct.'''

    __jsii_type__: typing.ClassVar[str] = "constructs.INodeFactory"

    @jsii.member(jsii_name="createNode")
    def create_node(
        self,
        host: "Construct",
        scope: IConstruct,
        id: builtins.str,
    ) -> "Node":
        '''Returns a new ``Node`` associated with ``host``.

        :param host: the associated construct.
        :param scope: the construct's scope (parent).
        :param id: the construct id.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34bc482ce404247eda29d0e41391d1a250e245798c9863dd3ee972713a871c13)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("Node", jsii.invoke(self, "createNode", [host, scope, id]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodeFactory).__jsii_proxy_class__ = lambda : _INodeFactoryProxy


@jsii.interface(jsii_type="constructs.ISynthesisSession")
class ISynthesisSession(typing_extensions.Protocol):
    '''Represents a single session of synthesis.

    Passed into ``construct.onSynthesize()`` methods.
    '''

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''The output directory for this synthesis session.'''
        ...


class _ISynthesisSessionProxy:
    '''Represents a single session of synthesis.

    Passed into ``construct.onSynthesize()`` methods.
    '''

    __jsii_type__: typing.ClassVar[str] = "constructs.ISynthesisSession"

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''The output directory for this synthesis session.'''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISynthesisSession).__jsii_proxy_class__ = lambda : _ISynthesisSessionProxy


@jsii.interface(jsii_type="constructs.IValidation")
class IValidation(typing_extensions.Protocol):
    '''Implement this interface in order for the construct to be able to validate itself.'''

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :return: An array of validation error messages, or an empty array if there the construct is valid.
        '''
        ...


class _IValidationProxy:
    '''Implement this interface in order for the construct to be able to validate itself.'''

    __jsii_type__: typing.ClassVar[str] = "constructs.IValidation"

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :return: An array of validation error messages, or an empty array if there the construct is valid.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IValidation).__jsii_proxy_class__ = lambda : _IValidationProxy


@jsii.data_type(
    jsii_type="constructs.MetadataEntry",
    jsii_struct_bases=[],
    name_mapping={"data": "data", "type": "type", "trace": "trace"},
)
class MetadataEntry:
    def __init__(
        self,
        *,
        data: typing.Any,
        type: builtins.str,
        trace: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''An entry in the construct metadata table.

        :param data: The data.
        :param type: The metadata entry type.
        :param trace: Stack trace. Can be omitted by setting the context key ``ConstructMetadata.DISABLE_STACK_TRACE_IN_METADATA`` to 1. Default: - no trace information
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0c2f394c95b32376bd2487bfa65b455507f8363a71e56bbcfef3a690552658)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument trace", value=trace, expected_type=type_hints["trace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "type": type,
        }
        if trace is not None:
            self._values["trace"] = trace

    @builtins.property
    def data(self) -> typing.Any:
        '''The data.'''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The metadata entry type.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trace(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Stack trace.

        Can be omitted by setting the context key
        ``ConstructMetadata.DISABLE_STACK_TRACE_IN_METADATA`` to 1.

        :default: - no trace information
        '''
        result = self._values.get("trace")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Node(metaclass=jsii.JSIIMeta, jsii_type="constructs.Node"):
    '''Represents the construct node in the scope tree.'''

    def __init__(self, host: "Construct", scope: IConstruct, id: builtins.str) -> None:
        '''
        :param host: -
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d6f98f49be8b52dd81458a10a699ba3c2baedf270e915aff9ad4a199629f16)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [host, scope, id])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: IConstruct) -> "Node":
        '''Returns the node associated with a construct.

        :param construct: the construct.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e976ef1a5da0fe82b55c8d7dec2b729e665c685a6fd4cf13e79d119b83e883b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast("Node", jsii.sinvoke(cls, "of", [construct]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: IConstruct) -> None:
        '''Add an ordering dependency on another Construct.

        All constructs in the dependency's scope will be deployed before any
        construct in this construct's scope.

        :param dependencies: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cad7dd42c6c671e9f87ba7d66096044214dd8c5bfed807ecb8eee7b41edd21)
            check_type(argname="argument dependencies", value=dependencies, expected_type=typing.Tuple[type_hints["dependencies"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDependency", [*dependencies]))

    @jsii.member(jsii_name="addError")
    def add_error(self, message: builtins.str) -> None:
        '''Adds an { "error":  } metadata entry to this construct.

        The toolkit will fail synthesis when errors are reported.

        :param message: The error message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b10c8983f831f0595e1925d7f6eb015d422544a564b543ef588a464ee1214f)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addError", [message]))

    @jsii.member(jsii_name="addInfo")
    def add_info(self, message: builtins.str) -> None:
        '''Adds a { "info":  } metadata entry to this construct.

        The toolkit will display the info message when apps are synthesized.

        :param message: The info message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff664c61d0573f00f4be24e1b2cc00fbc3dc310f8d38b986c033a778f4d85c3)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addInfo", [message]))

    @jsii.member(jsii_name="addMetadata")
    def add_metadata(
        self,
        type: builtins.str,
        data: typing.Any,
        from_function: typing.Any = None,
    ) -> None:
        '''Adds a metadata entry to this construct.

        Entries are arbitrary values and will also include a stack trace to allow tracing back to
        the code location for when the entry was added. It can be used, for example, to include source
        mapping in CloudFormation templates to improve diagnostics.

        :param type: a string denoting the type of metadata.
        :param data: the value of the metadata (can be a Token). If null/undefined, metadata will not be added.
        :param from_function: a function under which to restrict the metadata entry's stack trace (defaults to this.addMetadata).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023b8c3b11b2c1279fbfa8d54f858cec54fb8d9621c584addfbcccc63dbce202)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument from_function", value=from_function, expected_type=type_hints["from_function"])
        return typing.cast(None, jsii.invoke(self, "addMetadata", [type, data, from_function]))

    @jsii.member(jsii_name="addValidation")
    def add_validation(self, validation: IValidation) -> None:
        '''Adds a validation to this construct.

        When ``node.validate()`` is called, the ``validate()`` method will be called on
        all validations and all errors will be returned.

        :param validation: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67eb37a7475000d487d8124e00d1a8f5c0da44f9b68527dd02d18a3a789e11a0)
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
        return typing.cast(None, jsii.invoke(self, "addValidation", [validation]))

    @jsii.member(jsii_name="addWarning")
    def add_warning(self, message: builtins.str) -> None:
        '''Adds a { "warning":  } metadata entry to this construct.

        The toolkit will display the warning when an app is synthesized, or fail
        if run in --strict mode.

        :param message: The warning message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f9b2355d557213b106eed1902c1a6560c71c25cf9cff0f72bed4224b01f584)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addWarning", [message]))

    @jsii.member(jsii_name="applyAspect")
    def apply_aspect(self, aspect: IAspect) -> None:
        '''Applies the aspect to this Constructs node.

        :param aspect: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ed174dadbd41ce8923a2c9b692beccb5d6f7253f7bf4d06913dce24c7022ff)
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
        return typing.cast(None, jsii.invoke(self, "applyAspect", [aspect]))

    @jsii.member(jsii_name="findAll")
    def find_all(
        self,
        order: typing.Optional[ConstructOrder] = None,
    ) -> typing.List[IConstruct]:
        '''Return this construct and all of its children in the given order.

        :param order: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc361d795aa7b43307a9b4d8126549b970305e1487dfba0b95baabe4805e7c1b)
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        return typing.cast(typing.List[IConstruct], jsii.invoke(self, "findAll", [order]))

    @jsii.member(jsii_name="findChild")
    def find_child(self, id: builtins.str) -> IConstruct:
        '''Return a direct child by id.

        Throws an error if the child is not found.

        :param id: Identifier of direct child.

        :return: Child with the given id.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad30dac2587986f1ad461ddbfadd8c7bdb66542692e2272c9ea5e2487f4fa5f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(IConstruct, jsii.invoke(self, "findChild", [id]))

    @jsii.member(jsii_name="prepare")
    def prepare(self) -> None:
        '''Invokes "prepare" on all constructs (depth-first, post-order) in the tree under ``node``.'''
        return typing.cast(None, jsii.invoke(self, "prepare", []))

    @jsii.member(jsii_name="setContext")
    def set_context(self, key: builtins.str, value: typing.Any) -> None:
        '''This can be used to set contextual values.

        Context must be set before any children are added, since children may consult context info during construction.
        If the key already exists, it will be overridden.

        :param key: The context key.
        :param value: The context value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c20143e21f2a664bb5dbe7722603b1619d511e670df423c20328efe6ebfea2)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setContext", [key, value]))

    @jsii.member(jsii_name="synthesize")
    def synthesize(
        self,
        *,
        outdir: builtins.str,
        session_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Synthesizes a CloudAssembly from a construct tree.

        :param outdir: The output directory into which to synthesize the cloud assembly. Default: - creates a temporary directory
        :param session_context: Additional context passed into the synthesis session object when ``construct.synth`` is called. Default: - no additional context is passed to ``onSynthesize``
        :param skip_validation: Whether synthesis should skip the validation phase. Default: false
        '''
        options = SynthesisOptions(
            outdir=outdir,
            session_context=session_context,
            skip_validation=skip_validation,
        )

        return typing.cast(None, jsii.invoke(self, "synthesize", [options]))

    @jsii.member(jsii_name="tryFindChild")
    def try_find_child(self, id: builtins.str) -> typing.Optional[IConstruct]:
        '''Return a direct child by id, or undefined.

        :param id: Identifier of direct child.

        :return: the child if found, or undefined
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd332a688f70d4b16d58ad213f452996e4d14aa0f1ab9a377000ebd711a387e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(typing.Optional[IConstruct], jsii.invoke(self, "tryFindChild", [id]))

    @jsii.member(jsii_name="tryGetContext")
    def try_get_context(self, key: builtins.str) -> typing.Any:
        '''Retrieves a value from tree context.

        Context is usually initialized at the root, but can be overridden at any point in the tree.

        :param key: The context key.

        :return: The context value or ``undefined`` if there is no context value for thie key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736aac5a797564303e88fbc9bbd5d9ec05b62a898284a05b7d16b1761c28b181)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Any, jsii.invoke(self, "tryGetContext", [key]))

    @jsii.member(jsii_name="tryRemoveChild")
    def try_remove_child(self, child_name: builtins.str) -> builtins.bool:
        '''(experimental) Remove the child with the given name, if present.

        :param child_name: -

        :return: Whether a child with the given name was deleted.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cebd94ba5b2c7d277443dcec352c8c4c87ccbf209e78088ca08a915eb956e36)
            check_type(argname="argument child_name", value=child_name, expected_type=type_hints["child_name"])
        return typing.cast(builtins.bool, jsii.invoke(self, "tryRemoveChild", [child_name]))

    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.List["ValidationError"]:
        '''Validates tree (depth-first, pre-order) and returns the list of all errors.

        An empty list indicates that there are no errors.
        '''
        return typing.cast(typing.List["ValidationError"], jsii.invoke(self, "validate", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH_SEP")
    def PATH_SEP(cls) -> builtins.str:
        '''Separator used to delimit construct path components.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PATH_SEP"))

    @builtins.property
    @jsii.member(jsii_name="addr")
    def addr(self) -> builtins.str:
        '''Returns an opaque tree-unique address for this construct.

        Addresses are 42 characters hexadecimal strings. They begin with "c8"
        followed by 40 lowercase hexadecimal characters (0-9a-f).

        Addresses are calculated using a SHA-1 of the components of the construct
        path.

        To enable refactorings of construct trees, constructs with the ID ``Default``
        will be excluded from the calculation. In those cases constructs in the
        same tree may have the same addreess.

        Example::

            c83a2846e506bcc5f10682b564084bca2d275709ee
        '''
        return typing.cast(builtins.str, jsii.get(self, "addr"))

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List[IConstruct]:
        '''All direct children of this construct.'''
        return typing.cast(typing.List[IConstruct], jsii.get(self, "children"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List[Dependency]:
        '''Return all dependencies registered on this node or any of its children.'''
        return typing.cast(typing.List[Dependency], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''The id of this construct within the current scope.

        This is a a scope-unique id. To obtain an app-unique id for this construct, use ``uniqueId``.
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> builtins.bool:
        '''Returns true if this construct or the scopes in which it is defined are locked.'''
        return typing.cast(builtins.bool, jsii.get(self, "locked"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.List[MetadataEntry]:
        '''An immutable array of metadata objects associated with this construct.

        This can be used, for example, to implement support for deprecation notices, source mapping, etc.
        '''
        return typing.cast(typing.List[MetadataEntry], jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''The full, absolute path of this construct in the tree.

        Components are separated by '/'.
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> IConstruct:
        '''Returns the root of the construct tree.

        :return: The root of the construct tree.
        '''
        return typing.cast(IConstruct, jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[IConstruct]:
        '''All parent scopes of this construct.

        :return:

        a list of parent scopes. The last element in the list will always
        be the current construct and the first element will be the root of the
        tree.
        '''
        return typing.cast(typing.List[IConstruct], jsii.get(self, "scopes"))

    @builtins.property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> builtins.str:
        '''(deprecated) A tree-global unique alphanumeric identifier for this construct.

        Includes
        all components of the tree.

        :deprecated:

        please avoid using this property and use ``addr`` to form unique names.
        This algorithm uses MD5, which is not FIPS-complient and also excludes the
        identity of the root construct from the calculation.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "uniqueId"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional[IConstruct]:
        '''Returns the scope in which this construct is defined.

        The value is ``undefined`` at the root of the construct scope tree.
        '''
        return typing.cast(typing.Optional[IConstruct], jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="defaultChild")
    def default_child(self) -> typing.Optional[IConstruct]:
        '''Returns the child construct that has the id ``Default`` or ``Resource"``.

        This is usually the construct that provides the bulk of the underlying functionality.
        Useful for modifications of the underlying construct that are not available at the higher levels.
        Override the defaultChild property.

        This should only be used in the cases where the correct
        default child is not named 'Resource' or 'Default' as it
        should be.

        If you set this to undefined, the default behavior of finding
        the child named 'Resource' or 'Default' will be used.

        :return: a construct or undefined if there is no default child

        :throws: if there is more than one child
        '''
        return typing.cast(typing.Optional[IConstruct], jsii.get(self, "defaultChild"))

    @default_child.setter
    def default_child(self, value: typing.Optional[IConstruct]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbcfb9c1c2a97493a49545b146e41d7f6c46f63ff45f96526d7abf737620ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultChild", value)


@jsii.data_type(
    jsii_type="constructs.SynthesisOptions",
    jsii_struct_bases=[],
    name_mapping={
        "outdir": "outdir",
        "session_context": "sessionContext",
        "skip_validation": "skipValidation",
    },
)
class SynthesisOptions:
    def __init__(
        self,
        *,
        outdir: builtins.str,
        session_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options for synthesis.

        :param outdir: The output directory into which to synthesize the cloud assembly. Default: - creates a temporary directory
        :param session_context: Additional context passed into the synthesis session object when ``construct.synth`` is called. Default: - no additional context is passed to ``onSynthesize``
        :param skip_validation: Whether synthesis should skip the validation phase. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0e2b644e9e354811f411e1def5a2342f7a8c045657fc102c890ceee12c83f4)
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument session_context", value=session_context, expected_type=type_hints["session_context"])
            check_type(argname="argument skip_validation", value=skip_validation, expected_type=type_hints["skip_validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "outdir": outdir,
        }
        if session_context is not None:
            self._values["session_context"] = session_context
        if skip_validation is not None:
            self._values["skip_validation"] = skip_validation

    @builtins.property
    def outdir(self) -> builtins.str:
        '''The output directory into which to synthesize the cloud assembly.

        :default: - creates a temporary directory
        '''
        result = self._values.get("outdir")
        assert result is not None, "Required property 'outdir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional context passed into the synthesis session object when ``construct.synth`` is called.

        :default: - no additional context is passed to ``onSynthesize``
        '''
        result = self._values.get("session_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def skip_validation(self) -> typing.Optional[builtins.bool]:
        '''Whether synthesis should skip the validation phase.

        :default: false
        '''
        result = self._values.get("skip_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynthesisOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="constructs.ValidationError",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "source": "source"},
)
class ValidationError:
    def __init__(self, *, message: builtins.str, source: "Construct") -> None:
        '''An error returned during the validation phase.

        :param message: The error message.
        :param source: The construct which emitted the error.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7eb7b5b566f91387e6f1eb882d99e59e0e15cab92cef6099bc96813f2cf05f)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
            "source": source,
        }

    @builtins.property
    def message(self) -> builtins.str:
        '''The error message.'''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "Construct":
        '''The construct which emitted the error.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("Construct", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValidationError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IConstruct)
class Construct(metaclass=jsii.JSIIMeta, jsii_type="constructs.Construct"):
    '''Represents the building block of the construct graph.

    All constructs besides the root construct must be created within the scope of
    another construct.
    '''

    def __init__(
        self,
        scope: "Construct",
        id: builtins.str,
        *,
        node_factory: typing.Optional[INodeFactory] = None,
    ) -> None:
        '''Creates a new construct node.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings. If the ID includes a path separator (``/``), then it will be replaced by double dash ``--``.
        :param node_factory: A factory for attaching ``Node``s to the construct. Default: - the default ``Node`` is associated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020ca90e326a91c7b0f70a5c5df3471c78175b709d5adcbee2cb463d0367e387)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ConstructOptions(node_factory=node_factory)

        jsii.create(self.__class__, self, [scope, id, options])

    @jsii.member(jsii_name="onPrepare")
    def _on_prepare(self) -> None:
        '''Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.
        '''
        return typing.cast(None, jsii.invoke(self, "onPrepare", []))

    @jsii.member(jsii_name="onSynthesize")
    def _on_synthesize(self, session: ISynthesisSession) -> None:
        '''Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: The synthesis session.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62be2223d6c5360788aa6310c2a3a2de880f93725bd07ef18eeddf28cdb642ab)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        return typing.cast(None, jsii.invoke(self, "onSynthesize", [session]))

    @jsii.member(jsii_name="onValidate")
    def _on_validate(self) -> typing.List[builtins.str]:
        '''(deprecated) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :return: An array of validation error messages, or an empty array if there the construct is valid.

        :deprecated:

        use ``Node.addValidation()`` to subscribe validation functions on this construct
        instead of overriding this method.

        :stability: deprecated
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "onValidate", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Returns a string representation of this construct.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


__all__ = [
    "Construct",
    "ConstructMetadata",
    "ConstructOptions",
    "ConstructOrder",
    "Dependency",
    "IAspect",
    "IConstruct",
    "INodeFactory",
    "ISynthesisSession",
    "IValidation",
    "MetadataEntry",
    "Node",
    "SynthesisOptions",
    "ValidationError",
]

publication.publish()

def _typecheckingstub__c1012f6773721d1c461d9ac99fdffb6683206f6792321e9ee786f5a574378e0e(
    *,
    node_factory: typing.Optional[INodeFactory] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538d4a9d29db75f4dde4d525a17b8a1f69c206a824be508b9771e98cb1c66519(
    *,
    source: IConstruct,
    target: IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223778a82b7624d4bc9dc5758be8c71d16c0440da8dd252e2097e3f5b95aa433(
    node: IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34bc482ce404247eda29d0e41391d1a250e245798c9863dd3ee972713a871c13(
    host: Construct,
    scope: IConstruct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0c2f394c95b32376bd2487bfa65b455507f8363a71e56bbcfef3a690552658(
    *,
    data: typing.Any,
    type: builtins.str,
    trace: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d6f98f49be8b52dd81458a10a699ba3c2baedf270e915aff9ad4a199629f16(
    host: Construct,
    scope: IConstruct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e976ef1a5da0fe82b55c8d7dec2b729e665c685a6fd4cf13e79d119b83e883b(
    construct: IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cad7dd42c6c671e9f87ba7d66096044214dd8c5bfed807ecb8eee7b41edd21(
    *dependencies: IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b10c8983f831f0595e1925d7f6eb015d422544a564b543ef588a464ee1214f(
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff664c61d0573f00f4be24e1b2cc00fbc3dc310f8d38b986c033a778f4d85c3(
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023b8c3b11b2c1279fbfa8d54f858cec54fb8d9621c584addfbcccc63dbce202(
    type: builtins.str,
    data: typing.Any,
    from_function: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67eb37a7475000d487d8124e00d1a8f5c0da44f9b68527dd02d18a3a789e11a0(
    validation: IValidation,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f9b2355d557213b106eed1902c1a6560c71c25cf9cff0f72bed4224b01f584(
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ed174dadbd41ce8923a2c9b692beccb5d6f7253f7bf4d06913dce24c7022ff(
    aspect: IAspect,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc361d795aa7b43307a9b4d8126549b970305e1487dfba0b95baabe4805e7c1b(
    order: typing.Optional[ConstructOrder] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad30dac2587986f1ad461ddbfadd8c7bdb66542692e2272c9ea5e2487f4fa5f(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c20143e21f2a664bb5dbe7722603b1619d511e670df423c20328efe6ebfea2(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd332a688f70d4b16d58ad213f452996e4d14aa0f1ab9a377000ebd711a387e(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736aac5a797564303e88fbc9bbd5d9ec05b62a898284a05b7d16b1761c28b181(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cebd94ba5b2c7d277443dcec352c8c4c87ccbf209e78088ca08a915eb956e36(
    child_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbcfb9c1c2a97493a49545b146e41d7f6c46f63ff45f96526d7abf737620ea6(
    value: typing.Optional[IConstruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0e2b644e9e354811f411e1def5a2342f7a8c045657fc102c890ceee12c83f4(
    *,
    outdir: builtins.str,
    session_context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    skip_validation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7eb7b5b566f91387e6f1eb882d99e59e0e15cab92cef6099bc96813f2cf05f(
    *,
    message: builtins.str,
    source: Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020ca90e326a91c7b0f70a5c5df3471c78175b709d5adcbee2cb463d0367e387(
    scope: Construct,
    id: builtins.str,
    *,
    node_factory: typing.Optional[INodeFactory] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62be2223d6c5360788aa6310c2a3a2de880f93725bd07ef18eeddf28cdb642ab(
    session: ISynthesisSession,
) -> None:
    """Type checking stubs"""
    pass
