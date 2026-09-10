---
Title: Ticket House
Slug: microservices-based-web-app
Project Type: University Project
Duration: May 2023 - Jun 2023
Summary: Built a scalable E-Commerce Web Application using a microservices and event-driven architecture.
Skills: Node.js · JavaScript · React.js · TypeScript · Docker · Kubernetes
Image: microservices-based-web-app.jpg
Order: 1
---

<h2 id="overview">Overview</h2>
<p>Built a scalable E-Commerce Web Application using a microservices and event-driven architecture.  </p>
<h2 id="highlights">Highlights</h2>
<ul>
<li>Backend implemented with Node.js and TypeScript.  </li>
<li>Minimalist front-end using React and Next.js with server-side rendering.  </li>
<li>Deployed using Docker and Kubernetes for scalability.  </li>
<li>Orders managed efficiently using Redis and Bull.js for queueing.  </li>
</ul>
<h2 id="repository">Repository</h2>
<p><a href="https://github.com/shrishtinigam/ticket-house">ticket-house - GitHub Link</a></p>
<h1 id="ticket-house">Ticket House</h1>
<p>An E-Commerce Web Application with Microservices and Event-Based Architecture.</p>
<h2 id="technologies-used">Technologies Used</h2>
<ul>
<li>
<p><strong>Backend / Microservices</strong><br>
  Node.js, Express, TypeScript</p>
</li>
<li>
<p><strong>Frontend / Rendering</strong><br>
  React, Next.js (server-side rendering)</p>
</li>
<li>
<p><strong>Communication / Event Architecture</strong><br>
  NATS as event bus</p>
</li>
<li>
<p><strong>Infrastructure / Deployment / Jobs</strong><br>
  Docker, Kubernetes, Bull.js + Redis for job queues</p>
</li>
<li>
<p><strong>Payments</strong><br>
  StripeJS</p>
</li>
</ul>
<h2 id="setup-instructions">Setup Instructions</h2>
<p>To get the project running locally:</p>
<ol>
<li>Clone the repository (ideally under WSL2 on Windows) </li>
<li>Make sure Docker is running and Kubernetes is enabled </li>
<li>Create a Kubernetes secret for JWT:<br>
<code>bash
   kubectl create secret generic jwt-secret --from-literal=JWT_KEY=random_secret</code></li>
</ol>
<h2 id="development-setup">Development Setup</h2>
<p>Run the development environment:</p>
<pre class="codehilite"><code class="language-bash">skaffold dev
</code></pre>

<h1 id="rest-apis">REST APIs</h1>
<p>Here are the exposed endpoints grouped by domain:</p>
<table border="1" cellspacing="0" cellpadding="5">
  <thead>
    <tr>
      <th>Service</th>
      <th>HTTP Method</th>
      <th>Endpoint</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tickets</td>
      <td>GET</td>
      <td>/api/tickets</td>
    </tr>
    <tr>
      <td></td>
      <td>GET</td>
      <td>/api/tickets/:id</td>
    </tr>
    <tr>
      <td></td>
      <td>POST</td>
      <td>/api/tickets</td>
    </tr>
    <tr>
      <td></td>
      <td>PUT</td>
      <td>/api/tickets/:id</td>
    </tr>
    <tr>
      <td>Auth</td>
      <td>GET</td>
      <td>/api/users/currentUser</td>
    </tr>
    <tr>
      <td></td>
      <td>POST</td>
      <td>/api/users/signup</td>
    </tr>
    <tr>
      <td></td>
      <td>POST</td>
      <td>/api/users/signin</td>
    </tr>
    <tr>
      <td></td>
      <td>POST</td>
      <td>/api/users/signout</td>
    </tr>
    <tr>
      <td>Orders</td>
      <td>GET</td>
      <td>/api/orders</td>
    </tr>
    <tr>
      <td></td>
      <td>GET</td>
      <td>/api/orders/:id</td>
    </tr>
    <tr>
      <td></td>
      <td>POST</td>
      <td>/api/orders</td>
    </tr>
    <tr>
      <td></td>
      <td>DELETE</td>
      <td>/api/orders/:id</td>
    </tr>
    <tr>
      <td>Payments</td>
      <td>POST</td>
      <td>/api/payments</td>
    </tr>
  </tbody>
</table>

<hr>
<h1 id="common-module">Common Module</h1>
<p>There is a shared NPM module used across services:<br>
<code>@tickethouse/common</code></p>
<hr>
<h1 id="architecture">Architecture</h1>
<ul>
<li><strong>Microservices architecture</strong>: independent services such as auth, tickets, orders, payments  </li>
<li><strong>Event-based communication</strong> through <strong>NATS</strong> for decoupling and asynchronous flows  </li>
<li><strong>Job queue</strong> with <strong>Bull.js + Redis</strong> for background tasks or delayed operations  </li>
<li><strong>Deployment and orchestration</strong> using <strong>Docker + Kubernetes</strong>, with local development via <strong>skaffold</strong>  </li>
</ul>
<hr>
<h1 id="file-folder-structure-key-components">File / Folder Structure (Key Components)</h1>
<ul>
<li><code>auth/</code> — user authentication and session management service  </li>
<li><code>client/</code> — frontend application (React / Next.js)  </li>
<li><code>infra/k8s/</code> — Kubernetes manifests / infrastructure definitions  </li>
<li><code>orders/</code>, <code>payments/</code>, <code>tickets/</code> — microservices for respective business domains  </li>
<li><code>nats-test/</code> — NATS event bus  </li>
<li><code>.gitignore</code>, <code>skaffold.yaml</code>, etc. — project configuration files  </li>
</ul>
<hr>
<h1 id="additional-notes">Additional Notes</h1>
<ul>
<li>Written predominantly in <strong>TypeScript</strong> (backend microservices)  </li>
<li>Frontend uses <strong>JavaScript / TypeScript</strong>  </li>
<li>Uses <strong>Docker + Kubernetes</strong> for containerization and orchestration  </li>
<li><strong>skaffold dev</strong> is used for local development and continuous deployment flow  </li>
</ul>
<hr>
<h1 id="usage-contribution">Usage / Contribution</h1>
<ol>
<li>Ensure you have Docker and Kubernetes ready.  </li>
<li>Set up the JWT secret.  </li>
<li>Run <code>skaffold dev</code> to spin up all services + frontend.  </li>
</ol>
<p>If contributing, you might explore or extend:
- Adding more services (e.g., shipping, user profiles)<br>
- Improving error handling / observability<br>
- Adding tests for event flows<br>
- Enhancing performance, scaling, or security  </p>
<hr>
<h1 id="license-misc">License &amp; Misc</h1>
<ul>
<li>Repository is <strong>public</strong>  </li>
<li>Languages breakdown: ~89% <strong>TypeScript</strong>, ~10% <strong>JavaScript</strong>, small parts in <strong>Dockerfile</strong></li>
</ul>
