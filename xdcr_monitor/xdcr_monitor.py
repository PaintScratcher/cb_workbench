import requests
import time

POLLING_INTERVAL = 2
XDCR_QUEUES = (
	'replication_changes_left',
)
version = 4
auth = ('Administrator', 'password')
def monitor_xdcr_queues(host_port, bucket):
	print('Monitoring XDCR queues: {}'.format(bucket))
	# MB-14366: XDCR stats endpoint changed in 4.0
	if version >= 4:
		_wait_for_empty_queues(host_port, bucket, XDCR_QUEUES, get_go_xdcr_stats)
	else:
		_wait_for_empty_queues(host_port, bucket, XDCR_QUEUES)

def _wait_for_empty_queues(host_port, bucket, queues, stats_function=None):
	metrics = list(queues)
	while metrics:
		if stats_function:
			bucket_stats = stats_function(host_port, bucket)
		else:
			bucket_stats = get_bucket_stats(host_port, bucket)
		# As we are changing metrics in the loop; take a copy of
		# it to iterate over.
		for metric in list(metrics):
			stats = bucket_stats['op']['samples'].get(metric)
			if stats:
				last_value = stats[-1]
				if last_value:
					print('{} = {}'.format(metric, last_value))
					continue
				else:
					print('{} reached 0'.format(metric))
			metrics.remove(metric)
		if metrics:
			time.sleep(POLLING_INTERVAL)

def get_go_xdcr_stats(host_port, bucket):
	api = 'http://{}/pools/default/buckets/@goxdcr-{}/stats'.format(host_port,
																	bucket)
	return get(url=api).json()

def get(**kwargs):
	return requests.get(auth = auth, **kwargs)

monitor_xdcr_queues('192.168.46.101:8091', 'default')
