# MT25019
# cleanup namespaces 
# required only when experiment is rerun, for cleaning up previous runs

NS_SERVER="ns_server_arya"
NS_CLIENT="ns_client_arya"
SERVER_BIN="server"
CLIENT_BIN="client"

sudo ip netns del $NS_SERVER
sudo ip netns del $NS_CLIENT

# also clean the binaries
rm -rf $SERVER_BIN $CLIENT_BIN