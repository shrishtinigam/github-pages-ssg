---
Title: Get Semantic Versioning Right in Your Python Library - Part 2
Slug: semantic-versioning-p2
Date: Sep 21, 2025
Summary: Now that we have a basic understanding of software versioning principles and the Python interpreter/standard libraries, we can get on with how Python libraries are versioned.
Tags:
  - python
  - semver
  - pep standards
  - pip
---

<p>Now that we have a basic understanding of software versioning principles and the Python interpreter/standard libraries, we can get on with how Python libraries are versioned.</p>
<h2 id="right-what-about-python-libraries">Right, What About Python Libraries?</h2>
<p>Great question, we are getting there.</p>
<p>Third-party Python libraries aren’t controlled by the core Python team, so authors are technically free to choose their own versioning schemes. That said, PyPI package versions must be <a href="https://peps.python.org/pep-0440/">PEP 440</a> compliant. Most popular libraries follow this PEP, which puts down the official Python versioning standards for Python libraries and packages.</p>
<p><strong>PEP 440</strong> states that the version identifiers must comply with this scheme:</p>
<div style="text-align: center;">
<b>[N!]N(.N)*[{a|b|rc}N][.postN][.devN] </b>
</div>
<p><br></p>
<p>Public version identifiers are separated into up to <a href="https://packaging.python.org/en/latest/specifications/version-specifiers/">five segments</a>:</p>
<ol>
<li>
<p><strong>Epoch segment: N!</strong></p>
<ul>
<li>This is used very rarely, and its primary purpose is to reset the version numbering. I won't go into detail about this.</li>
</ul>
</li>
<li>
<p><strong>Release segment: N(.N)</strong></p>
<ul>
<li>The main version numbers, usually in <code>major.minor.micro</code> format. Eg: <code>2.1.3</code></li>
<li>Sometimes <code>major.minor</code> is also used.</li>
</ul>
</li>
<li>
<p><strong>Pre-release segment: {a|b|rc}N</strong></p>
<ul>
<li>Marks alpha, beta, or release candidate versions.</li>
<li>Excluded by default unless explicitly requested.</li>
<li>Examples:<ul>
<li>1.0a1 → first alpha of version 1.0</li>
<li>2.0b2 → second beta of version 2.0</li>
<li>3.1rc1 → first release candidate of 3.1</li>
</ul>
</li>
</ul>
</li>
<li>
<p><strong>Post-release segment: .postN</strong></p>
<ul>
<li>Marks minor fixes after a release.</li>
<li>Example: 1.0.post1 → first post-release of version 1.0</li>
</ul>
</li>
<li>
<p><strong>Development release segment: .devN</strong></p>
<ul>
<li>Marks ongoing development versions that are not yet stable.</li>
<li>Example: 1.0.dev1 → first development build of version 1.0</li>
<li>Example: 2.0.0.dev5 → fifth development build of version 2.0.0</li>
</ul>
</li>
</ol>
<p>PEP 440 also allows date-based versions, which can be handy for automated builds.</p>
<ul>
<li>Example: 2025.09 → September 2025 release</li>
<li>Example: 2025.09.14 → September 14, 2025 release</li>
</ul>
<p>While the scheme allows many segments, most libraries use two or three components:</p>
<ul>
<li>Major.Minor: 1.2 → Major release 1, minor update 2</li>
<li>Major.Minor.Micro: 1.2.3 → Major 1, minor 2, micro 3 (typical for bug fixes)</li>
</ul>
<p><strong>Stable releases</strong> omit pre-release, post-release, and development suffixes:</p>
<div style="text-align: center;">
<b>N(.N)*</b>
</div>

<h4 id="example-order-ladder">Example Order Ladder</h4>
<p>PEP 440 defines Python version ordering so tools like pip know which is newer:</p>
<pre class="codehilite"><code class="language-bash">1.2.dev1 &lt; 1.2a1 &lt; 1.2b1 &lt; 1.2rc1 &lt; 1.2 &lt; 1.2.post1
</code></pre>

<ul>
<li>devN: early dev release</li>
<li>aN / bN / rcN: alpha, beta, release candidate</li>
<li>final: stable release</li>
<li>.postN: post-release hotfix or docs</li>
<li>+local versions are ignored in comparisons</li>
</ul>
<hr>
<h2 id="my-job-its-just-pip">.. My Job? It's Just <code>pip</code></h2>
<p>When you run the simple command </p>
<pre class="codehilite"><code class="language-bash">pip install numpy
</code></pre>

<p>or</p>
<pre class="codehilite"><code class="language-bash">pip install requirements.txt
</code></pre>

<p>or if you're using <code>pyproject.toml</code></p>
<pre class="codehilite"><code class="language-bash">pip install .
</code></pre>

<p>what’s actually happening behind the scenes is called <a href="https://pip.pypa.io/en/stable/topics/dependency-resolution/">dependency resolution</a>.</p>
<blockquote>
<p>pip is capable of determining and installing the dependencies of packages. The process of determining which version of a dependency to install is known as dependency resolution.</p>
</blockquote>
<p>Most Python packages need other packages to work, which they declare as <code>dependencies</code>. <code>numpy</code> may require <code>mkl</code> to work, <code>pandas</code> requires <code>numpy</code> to work, <code>seaborn</code> required <code>pandas</code> to work and so on, leading to a <code>dependency tree</code>.</p>
<p>When you run <code>pip install .</code>, pip does the following:</p>
<ol>
<li>Selects the requested packages.</li>
<li>Looks up the dependencies of each package.</li>
<li>Repeats the process recursively for dependencies of dependencies.</li>
<li>Tries to find compatible versions of packages.</li>
</ol>
<p>This sounds simple, but it gets complicated quickly.</p>
<p>If <code>pip</code> finds incompatible versions, it <strong>backtracks</strong>, i.e., tries older versions until it finds a combination that works. This is why sometimes <code>pip</code> seems to download multiple versions of the same package. It's just testing versions to find a compatible set. Even after backtracking, pip might not be able to find a version that is compatible which raises a <strong>version conflict</strong>. </p>
<blockquote>
<p>A version conflict happens when two or more Python packages you want to install depend on different versions of the same library, and there is no single version that satisfies all of them. </p>
</blockquote>
<p><code>pip</code> can’t magically install multiple versions of the same package in the same environment, so it raises an error. Suppose you have the following dependencies:
- Package A requires numpy &gt;= 1.25.0
- Package B requires numpy &lt; 1.24.0
In this case, there is no version of numpy that satisfies both. <code>pip</code> throws a <code>ResolutionImpossible</code> error.</p>
<details>

<h4>Why Version Conflicts Happen</h4>
<ul>
  <li>Pinned versions – Some packages explicitly require a very specific version (e.g., numpy==1.23.0), which reduces flexibility.</li>
  <li>Fast-moving libraries – Libraries like pandas, scikit-learn, and tensorflow release updates frequently, sometimes breaking compatibility with older dependencies.</li>
  <li>Transitive dependencies – Packages often depend on other packages (and those have their own dependencies), which can lead to chains of conflicts.</li>
</ul>

<h4>How to Solve Version Conflicts</h4>
<ul>
  <li>Audit your top-level requirements – Remove unnecessary or overly strict version pins.</li>
  <li>Loosen version constraints – Instead of numpy==1.23.0, try numpy>=1.23.0,&lt;2.0.</li>
  <li>Use a virtual environment – Keeps each project isolated.</li>
  <li>Use a lockfile – Tools like pip-tools or poetry can lock exact working versions to avoid conflicts.</li>
  <li>Check the dependency tree – You can inspect dependencies using:
    <pre><code>pip show package_name
pipdeptree
</code></pre>
  </li>
</ul>

<h4>Reducing Backtracking</h4>
<p>Excessive backtracking can make installs slow. You can let pip resolve the dependencies, or you can help pip by:</p>
<ul>
  <li>Constraining versions – Tell pip to only consider versions within a certain range. This narrows the search space and speeds up resolution.</li>
  <li>Loosen overly strict version pins – If you’ve pinned packages too tightly, pip may struggle to find compatible versions. Relaxing bounds lets pip find a working combination more easily.</li>
  <li>Use constraint or lock files – Constraint files let you fix versions for dependencies, including transitive ones, without modifying your main requirements.</li>
  <li>Use the --upgrade flag – Forcing pip to consider the latest versions of installed packages can prevent unnecessary backtracking (to be used with caution, as you would need to ensure your code is compatible with the latest API).</li>
</ul>


</details>

<p>I hope you noticed the irony too. Make the dependencies too loose, and your resolution time increases or worse, a version is resolved that is not right for you code. Make it too tight, and there is a chances your transitive dependencies may throw a version conflict.</p>
<h2 id="how-does-semantic-versioning-come-into-picture">How Does Semantic Versioning Come Into Picture?</h2>
<p><a href="https://semver.org/">SemVer</a> was introduced in 2009 by GitHub co-founder Tom Preston-Werner, and is a widely accepted. </p>
<blockquote>
<p><strong>Important: PEP 440 version numbers and pip installation do not enforce SemVer. Many libraries adopt SemVer rules voluntarily, but you can’t assume it’s guaranteed.</strong></p>
</blockquote>
<p><strong>PEP 440 says nothing about API stability/backwards compatibility.</strong> It only defines how versions are formatted and compared. <code>pip</code> mostly does <strong>numeric comparisions</strong> of version numbers, guided by PEP 440. <code>pip</code> won’t stop you from installing a "breaking" version. <strong>Thus, many projects adopt SemVer rules within PEP 440</strong>. Please note that <strong>some libraries ignore SemVer or have their own scheme</strong>. Thus, you will need to make sure that the backwards compatibility policy defined by the library is reflected in your version constriant. </p>
<pre class="codehilite"><code class="language-bash">pip install &quot;package&gt;=1.0,&lt;2.0&quot;
</code></pre>

<blockquote>
<p>TLDR: When it comes to package versions, SemVer is not enforced and its better to check policies explicitly.</p>
</blockquote>
<details>
<table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="background-color: #171716;">
      <th>Aspect</th>
      <th>PEP 440 (Python Packaging Standard)</th>
      <th>Semantic Versioning (SemVer)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Purpose</strong></td>
      <td>Defines how Python packages must be versioned so <code>pip</code> and PyPI can parse, compare, and resolve them consistently.</td>
      <td>Communicates the type of changes (breaking, new features, bugfixes) across versions.</td>
    </tr>
    <tr>
      <td><strong>Basic Format</strong></td>
      <td><code>N(.N)*[{a b rc}N][.postN][.devN][+local]</code><br>Examples: <code>1.2.0</code>, <code>1.2.0a1</code>, <code>1.2.0rc1</code>, <code>1.2.0.post1</code>, <code>1.2.0.dev1</code>, <code>1.2.0+local.abc123</code></td>
      <td><code>MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]</code><br>Examples: <code>1.2.0</code>, <code>1.2.0-alpha.1</code>, <code>1.2.0-rc.1</code>, <code>1.2.0+20130313144700</code></td>
    </tr>
    <tr>
      <td><strong>Version Segments</strong></td>
      <td>Allows multiple segments: <code>1.2.3.4</code> is valid.</td>
      <td>Exactly three segments: <code>MAJOR.MINOR.PATCH</code>.</td>
    </tr>
    <tr>
      <td><strong>Pre-release Labels</strong></td>
      <td><code>aN</code> (alpha), <code>bN</code> (beta), <code>rcN</code> (release candidate).<br>Example: <code>1.0a1</code>, <code>1.0b2</code>, <code>1.0rc3</code></td>
      <td>Dash-separated identifiers: <code>-alpha.N</code>, <code>-beta.N</code>, <code>-rc.N</code>.<br>Example: <code>1.0.0-alpha.1</code>, <code>1.0.0-beta.2</code>, <code>1.0.0-rc.3</code></td>
    </tr>
    <tr>
      <td><strong>Post Releases</strong></td>
      <td>Supported with <code>.postN</code> (for hotfixes, doc-only updates, etc.).<br>Example: <code>1.0.post1</code></td>
      <td>Not part of the spec — usually bump <code>PATCH</code> instead.</td>
    </tr>
    <tr>
      <td><strong>Development Releases</strong></td>
      <td>Explicit <code>.devN</code> suffix for nightly or dev snapshots.<br>Example: <code>1.0.dev2</code></td>
      <td>No direct equivalent. Some ecosystems use <code>-dev</code> informally, but not standardized.</td>
    </tr>
    <tr>
      <td><strong>Local Versions / Build Metadata</strong></td>
      <td><code>+tag</code> for local builds or downstream variants.<br>Example: <code>1.0+local.1</code></td>
      <td><code>+metadata</code> for build information.<br>Example: <code>1.0.0+build.1</code></td>
    </tr>
    <tr>
      <td><strong>Comparison Rules</strong></td>
      <td>Strict, fully defined.<br><strong>Order ladder:</strong> <code>X.Y.devN &lt; X.YaN &lt; X.YbN &lt; X.YrcN &lt; X.Y &lt; X.Y.postN</code></td>
      <td>Defined but simpler.<br><strong>Order ladder:</strong> <code>X.Y.Z-alpha &lt; X.Y.Z-beta &lt; X.Y.Z-rc &lt; X.Y.Z</code><br>Build metadata (<code>+</code>) ignored for ordering.</td>
    </tr>
    <tr>
      <td><strong>Backward Compatibility Signaling</strong></td>
      <td>Not intrinsic — projects may adopt SemVer rules within PEP 440.</td>
      <td>Core principle:<br>- <code>MAJOR</code> = breaking changes<br>- <code>MINOR</code> = new, backward-compatible features<br>- <code>PATCH</code> = bug fixes</td>
    </tr>
    <tr>
      <td><strong>Flexibility</strong></td>
      <td>Very flexible — supports multi-part versions, dev cycles, post releases, local variants.</td>
      <td>Strict — exactly 3 numeric parts + optional pre-release/build metadata.</td>
    </tr>
    <tr>
      <td><strong>Tooling</strong></td>
      <td>Enforced by Python packaging tools (<code>pip</code>, <code>setuptools</code>, PyPI).</td>
      <td>Enforced differently per ecosystem (npm, cargo, Maven, etc.), not Python.</td>
    </tr>
  </tbody>
</table>

</details>
