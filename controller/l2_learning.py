from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class LearningSwitch(object):
    def __init__(self, connection):
        self.connection = connection
        self.macToPort = {}
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed

        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp
        in_port = packet_in.in_port

        # Learn MAC address
        self.macToPort[packet.src] = in_port

        # 🔥 IP-based firewall
        ip_packet = packet.find('ipv4')

        if ip_packet:
            src_ip = str(ip_packet.srcip)
            dst_ip = str(ip_packet.dstip)

            # 🚫 BLOCK h1s1 → h2s2
            if src_ip == "10.0.0.1" and dst_ip == "10.0.0.4":
                log.info("BLOCKED: %s -> %s", src_ip, dst_ip)
                return

        # Normal forwarding
        if packet.dst in self.macToPort:
            out_port = self.macToPort[packet.dst]
        else:
            out_port = of.OFPP_FLOOD

        actions = [of.ofp_action_output(port=out_port)]

        # Install flow rule
        if out_port != of.OFPP_FLOOD:
            match = of.ofp_match.from_packet(packet, in_port)
            msg = of.ofp_flow_mod()
            msg.match = match
            msg.actions = actions
            self.connection.send(msg)

        # Send packet
        msg = of.ofp_packet_out()
        msg.data = packet_in
        msg.actions = actions
        msg.in_port = in_port
        self.connection.send(msg)


def launch():
    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        LearningSwitch(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
