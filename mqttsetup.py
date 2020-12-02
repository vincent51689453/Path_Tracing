import paho.mqtt.client as mqtt


def mqtt_client_setup(server):
    client = mqtt.Client()
    client.connect(server,1883,60)
    return client


def mqtt_publish_record(node,topic,mqtt_message):
    node.publish(topic, mqtt_message)
    node.loop_stop()
    node.disconnect()

def mqtt_message_generator(comp_patient,incomp_patient,comp_leave,incomp_leave):
    #Generate message for node red dashboard display
    a = comp_patient
    b = incomp_patient
    c = comp_leave
    d = incomp_leave
    total_contact = a + b + c + d
    if(total_contact>0):
        success_rate = int(((a+c)/total_contact)*100)
    else:
        success_rate = 0

    mqtt_message =' { "total_count" :' + str(total_contact)+ \
                ', "valid_patient_counter" :'+ str(a)+ \
                ', "invalid_patient_counter" :'+str(b)+\
                ', "valid_exit_counter":'+str(c)+\
                ', "invalid_exit_counter":'+str(d) +\
                ', "success_rate":'+str(success_rate) +\
                ', "total_sucess":'+str(a+c) +\
                ', "total_fail":'+str(b+d) + ' } '

    return mqtt_message     