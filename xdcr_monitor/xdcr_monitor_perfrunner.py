### Create two clusters with an XDCR relationship, run a workload against the clusters for example:
### cbc-pillowfight -t 1 -B 10  -U couchbase://NODE_IP/default -m 512 -M 1024 -r 50
### Move this file to the root of the perfrunner repo and run ./env/bin/python xdcr_test.py -c clusters/Hermes.spec
### The actual cluster spec is irrelevant for this test so long as it is valid.

from optparse import OptionParser

from perfrunner.settings import ClusterSpec
from perfrunner.helpers.monitor import Monitor


def get_options():
    usage = '%prog -c cluster -t test_config'

    parser = OptionParser(usage)

    parser.add_option('-c', dest='cluster_spec_fname',
                      help='path to cluster specification file',
                      metavar='cluster.spec')
    options, args = parser.parse_args()
    return options, args


options, args = get_options()
cluster_spec = ClusterSpec()
cluster_spec.parse(options.cluster_spec_fname)

monitor = Monitor(cluster_spec)

monitor.monitor_xdcr_queues('192.168.42.101:8091', 'default')
