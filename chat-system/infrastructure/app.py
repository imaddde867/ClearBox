from deploy import ChatSystemStack
from aws_cdk import core

app = core.App()
ChatSystemStack(app, "ChatSystemStack")
