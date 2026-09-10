---
Title: Pathfinding Algorithms Visualizer (SFML)
Slug: pathfinding-algorithms-visualizer
Project Type: University Project
Duration: May 2023 - Jun 2023
Summary: Visualized four pathfinding algorithms (Dijkstra's, A*, BFS, DFS) on a grid map.
Skills: Object-Oriented Programming (OOP) · C++ · SFML
Image: pathfinding-algorithms-visualizer.jpg
Order: 2
---

<h2 id="overview">Overview</h2>
<p>Visualized four pathfinding algorithms (Dijkstra's, A*, BFS, DFS) on a grid map.  </p>
<h2 id="highlights">Highlights</h2>
<ul>
<li>Calculated total execution time, number of checks, and final path length.  </li>
<li>Optimized A* implementation using priority queues for efficiency.  </li>
</ul>
<h2 id="repository">Repository</h2>
<p><a href="https://github.com/shrishtinigam/pathfinding_algorithms_visualizer_sfml">pathfinding_algorithms_visualizer_sfml - GitHub Link</a></p>
<h1 id="pathfinding-algorithms-visualizer-sfml">Pathfinding Algorithms Visualizer (SFML)</h1>
<p>A C++ application that visually demonstrates four fundamental pathfinding algorithms:</p>
<ul>
<li><strong>Breadth-First Search (BFS)</strong></li>
<li><strong>Depth-First Search (DFS)</strong></li>
<li><strong>Dijkstra's Algorithm</strong></li>
<li><strong>A* (A-Star) Algorithm</strong></li>
</ul>
<p>Built using the SFML graphics library, this tool allows users to interactively explore how these algorithms traverse a grid to find the shortest path between two points.</p>
<h2 id="features">Features</h2>
<ul>
<li><strong>Interactive Grid:</strong> Click to set start and end points.</li>
<li><strong>Algorithm Selection:</strong> Choose between BFS, DFS, Dijkstra, and A*.</li>
<li><strong>Wall Placement:</strong> Block paths by clicking to add walls.</li>
<li><strong>Real-Time Visualization:</strong> Watch the algorithms in action step-by-step.</li>
</ul>
<h2 id="added-dfs-visualization">Added DFS visualization</h2>
<ul>
<li>Added another map and window that shows visualization for the DFS pathfinding algorithm.</li>
<li>DFS uses stack data structure to perform its search.</li>
<li>The time complexity of the DFS algorithm is O(V+E), where V is the number of vertices and E is the number of edges in the graph</li>
</ul>
<h2 id="optimized-a-star-code">Optimized A Star code</h2>
<ul>
<li>Instead of using a vector to store the visited cells values, I used a priority queue.</li>
<li>In particular, I implemented a min heap data structure.</li>
<li>This reduced the search time complexity from O(n) to O(1)</li>
<li>Previously, A star was performing just as good or worse than BFS/Dijsktra's.</li>
<li>Now, it performs much faster. However, this ofcourse depends on the case and the given map.</li>
<li>In order to create a min heap, I used the following template -</li>
</ul>
<p><code>cpp
  std::priority_queue &lt;std::pair&lt;int, gbl::Position&lt;&gt;&gt;&gt; astar_path_minheap;</code></p>
<ul>
<li>Here, in the first 'int', I store the f score of the cell, multiplied by (-1). This way, the cells with the minimum f scores rise up to the top.</li>
</ul>
<h2 id="installation">Installation</h2>
<h3 id="prerequisites">Prerequisites</h3>
<p>Ensure you have the following installed:</p>
<ul>
<li><strong>SFML 2.5+</strong>: <a href="https://www.sfml-dev.org/download.php">SFML Downloads</a></li>
<li><strong>C++ Compiler</strong>: Compatible with C++11 or later</li>
</ul>
<h3 id="building-the-project">Building the Project</h3>
<ol>
<li>Clone the repository:</li>
</ol>
<pre class="codehilite"><code class="language-bash">git clone https://github.com/shrishtinigam/pathfinding_algorithms_visualizer_sfml.git
cd pathfinding_algorithms_visualizer_sfml
</code></pre>

<ol>
<li>Compile the project:</li>
</ol>
<pre class="codehilite"><code class="language-bash">g++ -std=c++11 -o pathfinder Main.cpp BFS.cpp DFS.cpp Dijkstra.cpp AStar.cpp -lsfml-graphics -lsfml-window -lsfml-system
</code></pre>

<ol>
<li>Run the application:</li>
</ol>
<pre class="codehilite"><code class="language-bash">./pathfinder
</code></pre>

<h2 id="usage">Usage</h2>
<ul>
<li><strong>Left Click:</strong> Place walls on the grid  </li>
<li><strong>Right Click:</strong> Set start and end points  </li>
<li><strong>Press 'B':</strong> Run BFS  </li>
<li><strong>Press 'D':</strong> Run DFS  </li>
<li><strong>Press 'I':</strong> Run Dijkstra  </li>
<li><strong>Press 'A':</strong> Run A*  </li>
</ul>
<h2 id="screenshots">Screenshots</h2>
<p>![Pathfinding Visualization]</p>
