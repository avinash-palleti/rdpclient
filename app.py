from flask import Flask, render_template, request
from rdpy3.protocol.rdp import rdp
from twisted.internet import reactor
class MyRDPFactory(rdp.ClientFactory):
    def __init__(self, server_ip, password):
        self.server_ip = server_ip
        self.password = password
    def clientConnectionLost(self, connector, reason):
        reactor.stop()
    def clientConnectionFailed(self, connector, reason):
        reactor.stop()
    def buildProtocol(self, addr):
        return rdp.RDPClientProtocol(self)
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        server_ip = request.form.get('server_ip')
        password = request.form.get('password')
        if server_ip and password:
            reactor.connectTCP(server_ip, 3389, MyRDPFactory(server_ip, password))
            reactor.run()
        else:
            return "Please enter both IP and password", 400
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
