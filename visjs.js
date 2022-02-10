
  nodes_list = {{ nodes_list|safe }};
  // create an array with nodes
  var nodes  = new vis.DataSet();
  for (const element of nodes_list) {
    nodes.add(element);
  }

  // create an array with edges
  edges_list = {{ edges_list|safe }};
  var edges = new vis.DataSet();
  for (const element of edges_list) {
    edges.add(element);
  }
  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    nodes: {borderWidth: 2},
    interaction: {hover: true}
  }
  var network = new vis.Network(container, data, options);
