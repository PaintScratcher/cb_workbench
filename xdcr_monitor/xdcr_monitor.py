import requests
import time

POLLING_INTERVAL = 2
XDCR_QUEUES = (
	'replication_changes_left',
)
auth = ('Administrator', 'password')

def monitor_xdcr_queues(host_port, bucket):
	print('Monitoring XDCR queues: {}'.format(bucket))
	# MB-14366: XDCR stats endpoint changed in 4.0
	try:
		get_goxdcr_stats(host_port, bucket)
	except ValueError:
		# Use default stats function for older builds.
		stats_function = None
	else:
		stats_function = get_goxdcr_stats
	_wait_for_empty_queues(host_port, bucket, XDCR_QUEUES,
								stats_function)

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

def get(self, **kwargs):
 	return requests.get(auth=auth, **kwargs)

def get_bucket_stats(host_port, bucket):
	api = 'http://{}/pools/default/buckets/{}/stats'.format(host_port,
															bucket)
	return get(url=api).json()

def get_goxdcr_stats(host_port, bucket):
	api = 'http://{}/pools/default/buckets/@goxdcr-{}/stats'.format(host_port,
																	bucket)
	return get(url=api).json()

def get(**kwargs):
	return requests.get(auth = auth, **kwargs)

monitor_xdcr_queues('ip:port', 'bucket_name')
