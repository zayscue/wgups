def tsp(graph):
  shortest = {
    'dist': float('inf'),
    'path': [],
    'count': 0
  }

  # Function to find the minimum weight  
  # Hamiltonian Cycle
  def run(g, v, t, p, n, cnt, cos): 
    # If last node is reached and it has  
    # a link to the starting node i.e  
    # the source then keep the minimum  
    # value out of the total cost of  
    # traversal and "ans" 
    # Finally return to check for  
    # more possible values 
    if cnt == n and g[p][0]:
      t[n - 1] = p
      if (cos + g[p][0]) < shortest['dist']:
        shortest['dist'] = cos + g[p][0]
        shortest['path'] = list(t)
        shortest['count'] = shortest['count'] + 1 
      return

    # BACKTRACKING STEP 
    # Loop to traverse the adjacency list 
    # of currPos node and increasing the count 
    # by 1 and cost by graph[currPos][i] value 
    for i in range(n):
      if shortest['count'] == n:
        return
      if v[i] == False and g[p][i]: 
        # Mark as visited 
        v[i] = True
        t[i-1] = p
        run(g, v, t, i, n, cnt + 1, cos + g[p][i]) 
        # Mark ith node as unvisited 
        v[i] = False
  

  n = len(graph)
  v = [False for i in range(n)]
  t = [None for i in range(n)] 
  v[0] = True

  run(graph, v, t, 0, n, 1, 0)

  return shortest