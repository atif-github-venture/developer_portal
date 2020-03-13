import consul


def filter_service_info(dict_list, name):
    addr = port = None
    for k,v in dict_list.items():
        if v['Service'] == name:
            addr = v['Address']
            port = v['Port']
            break
    return addr, port


class ConsulRegistration:

    @staticmethod
    def register_service(consult_host, consul_port, service_name, service_addr, service_port):

        try:
            c = consul.Consul(host=consult_host, port=consul_port)
            # print(c.status.leader())
            c.agent.service.register(
                name=service_name, port=service_port, service_id=service_name, tags=[service_name],
                address=service_addr)
            return True, None
        except Exception as e:
            print(e)
            return False, e

    @staticmethod
    def deregister_service(consult_host, consul_port, service_name):
        c = consul.Consul(host=consult_host, port=consul_port)
        c.agent.service.deregister(service_name)

    @staticmethod
    def query_consul(consult_host, consul_port, service_name):
        c = consul.Consul(host=consult_host, port=consul_port)
        lst = c.agent.services()
        return filter_service_info(lst, service_name)
