from kafka import KafkaProducer
from kafka.errors import KafkaError
import ssl
import json

############################################
# Service credentials from Bluemix UI:
# !Please replace below examples with your credentials
############################################
bootstrap_servers = "kafka01-prod01.messagehub.services.us-south.bluemix.net:9093"
sasl_plain_username = "gkyIt44JC9S1eGDv"
sasl_plain_password = "Ptg1KfpKcbWd2FdtaN8ExRZKYNjQgfr5"
############################################

sasl_mechanism = 'PLAIN'
security_protocol = 'SASL_SSL'

# Create a new context using system defaults, disable all but TLS1.2
context = ssl.create_default_context()
context.options &= ssl.OP_NO_TLSv1
context.options &= ssl.OP_NO_TLSv1_1

producer = KafkaProducer(bootstrap_servers = bootstrap_servers,
                         sasl_plain_username = sasl_plain_username,
                         sasl_plain_password = sasl_plain_password,
                         security_protocol = security_protocol,
                         ssl_context = context,
                         sasl_mechanism = sasl_mechanism,
                         api_version=(0,10),
                         value_serializer = lambda v: json.dumps(v).encode('utf-8'))

# !Put your topic name and tweet message here
future = producer.send('umitsInput', {'tweet': 'umits tweet is sooo cooooll'})

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)
