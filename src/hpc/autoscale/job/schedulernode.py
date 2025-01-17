import socket
import typing
from uuid import uuid4

from immutabledict import ImmutableOrderedDict

from hpc.autoscale import hpclogging as logging
from hpc.autoscale import hpctypes as ht
from hpc.autoscale.codeanalysis import hpcwrapclass
from hpc.autoscale.node.delayednodeid import DelayedNodeId
from hpc.autoscale.node.node import Node


@hpcwrapclass
class SchedulerNode(Node):
    # used only internally for testing
    ignore_hostnames: bool = False

    def __init__(
        self,
        hostname: str,
        resources: typing.Optional[dict] = None,
        bucket_id: typing.Optional[ht.BucketId] = None,
    ) -> None:
        resources = resources or ht.ResourceDict({})
        private_ip: typing.Optional[ht.IpAddress]
        if SchedulerNode.ignore_hostnames:
            private_ip = None
        else:
            try:
                private_ip = ht.IpAddress(socket.gethostbyname(hostname))
            except Exception as e:
                logging.warning("Could not find private ip for %s: %s", hostname, e)
                private_ip = None

        Node.__init__(
            self,
            node_id=DelayedNodeId(ht.NodeName(hostname)),
            name=ht.NodeName(hostname),
            nodearray=ht.NodeArrayName("unknown"),
            bucket_id=bucket_id or ht.BucketId(str(uuid4())),
            hostname=ht.Hostname(hostname),
            private_ip=private_ip,
            instance_id=None,
            vm_size=ht.VMSize("unknown"),
            location=ht.Location("unknown"),
            spot=False,
            vcpu_count=1,
            memory=ht.Memory(0, "b"),
            infiniband=False,
            state=ht.NodeStatus("running"),
            target_state=ht.NodeStatus("running"),
            power_state=ht.NodeStatus("running"),
            exists=True,
            placement_group=None,
            managed=False,
            resources=ht.ResourceDict(resources),
            software_configuration=ImmutableOrderedDict({}),
            keep_alive=False,
        )

    def to_dict(self) -> typing.Dict:
        ret = super().to_dict()
        ret["memory"] = self.memory
        ret["vcpu-count"] = self.vcpu_count
        ret["pcpu-count"] = self.pcpu_count
        ret["gpu-count"] = self.gpu_count
        return ret

    def __lt__(self, node: typing.Any) -> int:
        return node.hostname_or_uuid < self.hostname_or_uuid

    def __str__(self) -> str:
        return "Scheduler{}".format(Node.__str__(self))

    def __repr__(self) -> str:
        return "Scheduler{}".format(Node.__repr__(self))


class TempNode(Node):
    def __init__(
        self,
        hostname: str,
        resources: typing.Optional[dict] = None,
        bucket_id: typing.Optional[ht.BucketId] = None,
        **overrides: typing.Any,
    ) -> None:
        resources = resources or ht.ResourceDict({})

        node_init_args = dict(
            self=self,
            node_id=DelayedNodeId(ht.NodeName(hostname)),
            name=ht.NodeName(hostname),
            nodearray=ht.NodeArrayName("unknown"),
            bucket_id=bucket_id or ht.BucketId(str(uuid4())),
            hostname=ht.Hostname(hostname),
            private_ip=None,
            instance_id=None,
            vm_size=ht.VMSize("unknown"),
            location=ht.Location("unknown"),
            spot=False,
            vcpu_count=1,
            memory=ht.Memory(0, "b"),
            infiniband=False,
            state=ht.NodeStatus("running"),
            target_state=ht.NodeStatus("running"),
            power_state=ht.NodeStatus("running"),
            exists=True,
            placement_group=None,
            managed=False,
            resources=ht.ResourceDict(resources),
            software_configuration=ImmutableOrderedDict({}),
            keep_alive=False,
        )
        node_init_args.update(overrides)
        Node.__init__(**node_init_args)

    def to_dict(self) -> typing.Dict:
        ret = super().to_dict()
        ret["memory"] = self.memory
        ret["vcpu-count"] = self.vcpu_count
        ret["pcpu-count"] = self.pcpu_count
        ret["gpu-count"] = self.gpu_count
        return ret

    def __lt__(self, node: typing.Any) -> int:
        return node.hostname_or_uuid < self.hostname_or_uuid

    def __str__(self) -> str:
        return "Temp{}".format(Node.__str__(self))

    def __repr__(self) -> str:
        return "Temp{}".format(Node.__repr__(self))
