---
Title: Get Semantic Versioning Right in Your Python Library - Part 3
Slug: semantic-versioning-p3
Date: Sep 28, 2025
Summary: In this final part of getting versioning right in your Python library, I explore practical steps to ensure your library is maintainable, PEP-compliant, and future-proof. I also plan to add more code and practical examples in the future.
Tags:
  - python
  - pypi
  - pep standards
---

<p>In this final part of getting versioning right in your Python library, I explore practical steps to ensure your library is maintainable, PEP-compliant, and future-proof. I also plan to add more code and practical examples in the future.</p>
<h2 id="how-should-i-version-my-libraries">How Should I Version My Libraries?</h2>
<p>The best practice for Python library versioning under PEP 440 is to adopt a three-part scheme like SemVer. SemVer is widely recognized, easy to understand, and helps standardize which changes are backward-compatible versus breaking. Setting your package’s versioning policy this way makes it clear to users which upgrades are safe.</p>
<p>The following rules are recommended:</p>
<div style="text-align: center;">
  <b>[MAJOR].[MINOR].[PATCH]</b>
</div>
<p><br></p>
<ul>
<li>MAJOR → backward-incompatible changes.</li>
<li>MINOR → backward-compatible features.</li>
<li>PATCH → backward-compatible bug fixes.</li>
</ul>
<h3 id="development-pre-release-versions">Development &amp; Pre-release Versions</h3>
<p>When a library is preparing a new release, there are several intermediate stages before the final stable version. PEP 440 defines how these are labeled.</p>
<h4 id="example-backward-compatible-update">Example: Backward-Compatible Update</h4>
<p>Suppose a library is at 1.2.0 and wants to release backward-compatible new features. 
According to SemVer / PEP 440, this means a minor bump → 1.3.0.</p>
<p>Development &amp; pre-release versions could look like this:</p>
<pre class="codehilite"><code class="language-bash">1.3.0.dev1   # dev snapshot
1.3.0a1      # alpha pre-release
1.3.0b1      # beta pre-release
1.3.0rc1     # release candidate
1.3.0        # final release
</code></pre>

<p>Users can use <code>pip install library==1.3.0</code> to install the latest stable release. Pre-release versions (alpha, beta, release candidates) are ignored by default.
Developers can test pre-releases explicitly with <code>pip install library==1.3.0a1</code> or by using the <code>--pre</code> flag.</p>
<h4 id="example-backward-incompatible-update">Example: Backward-Incompatible Update</h4>
<p>Suppose the library now introduces breaking changes (e.g., removes a function, changes API signature).
According to SemVer / PEP 440, this is a major bump → 2.0.0.
Version progression:</p>
<pre class="codehilite"><code class="language-bash">2.0.0.dev1
2.0.0a1
2.0.0b1
2.0.0rc1
2.0.0
</code></pre>

<p>This signals to users that upgrading may break code relying on 1.x.x.</p>
<h3 id="how-pandas-uses-a-semver-variant">How Pandas uses a SemVer Variant</h3>
<p>I am providing an example of a popular library and its <a href="https://pandas.pydata.org/docs/development/policies.html">versioning policy</a> here to provide some perspective. </p>
<ul>
  <li>Follows a loose SemVer with MAJOR.MINOR.PATCH.</li>
  <li>Major releases: Can introduce breaking API changes, with migration guidance.</li>
  <li>Minor releases: Introduce deprecations that warn users but preserve current behavior.</li>
  <li>Patch releases: Do not add new deprecations; may include bug fixes.</li>
  <li>Deprecated behavior remains until the next major release (e.g., deprecated in 1.2.x, removed in 2.0.0).</li>
  <li>Experimental features: Behavior may change at any time.</li>
  <li>Judgement is used to classify bug fixes vs. API-breaking changes, with community input encouraged.</li>
</ul>

<h3 id="modern-minimum-build-system-requirements-pep-518">Modern Minimum Build System Requirements - PEP 518</h3>
<p><a href="https://peps.python.org/pep-0518/">PEP 518</a> defines a standard way for Python projects to declare their build dependencies in a separate configuration file, rather than relying on setup.py. </p>
<p>Historically, distutils and setuptools used executable setup.py scripts to build distributions. The PEP resolves this by allowing projects to declaratively list the minimal dependencies needed for the build system, so tools like pip can install them upfront. There are more details, which you can read about in PEP 517/518.</p>
<p>The pyproject.toml file is a configuration file standard for Python projects, defined by this PEP. It uses the TOML (Tom's Obvious, Minimal Language) format, which is designed to be human-readable and easy to parse. This is adopted by newer libraries like <code>poetry</code> and <code>flit</code>, that help your create these dependencies. </p>
<p>I will delve into a full Python setup guide in a separate post.</p>
<h2 id="conclusion">Conclusion</h2>
<p>Here’s a quick reference for modern Python library best practices.</p>
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>Aspect</th>
      <th>Standard Practice</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Versioning</td>
      <td>PEP 440 / non-enforced SemVer</td>
    </tr>
    <tr>
      <td>Dependency declaration</td>
      <td>pyproject.toml (modern), setup.py (older projects)</td>
    </tr>
    <tr>
      <td>Dev dependencies</td>
      <td>optional-dependencies in pyproject.toml or requirements-dev.txt</td>
    </tr>
    <tr>
      <td>Locking dependencies</td>
      <td>Use pip-tools (requirements.txt + requirements.lock) or poetry.lock</td>
    </tr>
    <tr>
      <td>Build / distribution</td>
      <td>python -m build to generate .whl and .tar.gz</td>
    </tr>
  </tbody>
</table>

<p>And there you have it: </p>
<blockquote>
<p>Follow SemVer's Major-Minor-Patch and backwards compatibility rules, </p>
<p>Don't assume everyone else follows them,</p>
<p>Read the versioning scheme policy docs of the libraries you are using, and </p>
<p>Use pyproject.toml.</p>
</blockquote>
<p>Now release that package you've been postponing!</p>
<p><br><br></p>
<h2 id="ps-commit-style">PS: Commit Style</h2>
<p>This part of the article is something I care about deeply personally but mostly unrelated to the rest. When SemVer is applied to commit messages, it helps maintain consistent, meaningful, and easy-to-understand commit histories. Whether you are a "commit everything in one go" or a "small incremental features" person, the core idea behind this style is to categorize commits based on their impact, and help in automated generation of changelogs and releases.</p>
<p>Ultimately, it helps you maintain a clean Git history. This is the format I follow generally, and helps me jump around my commits, as I know what was added or deleted in each commit. I hope this helps you write better commits.</p>
<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>Type</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>feat:</td>
      <td>Adds a new feature</td>
    </tr>
    <tr>
      <td>fix:</td>
      <td>Fixes a bug</td>
    </tr>
    <tr>
      <td>chore:</td>
      <td>Maintenance tasks</td>
    </tr>
    <tr>
      <td>build:</td>
      <td>Build system or dependencies</td>
    </tr>
    <tr>
      <td>docs:</td>
      <td>Documentation updates</td>
    </tr>
    <tr>
      <td>perf:</td>
      <td>Performance improvements</td>
    </tr>
    <tr>
      <td>refactor:</td>
      <td>Code refactoring</td>
    </tr>
    <tr>
      <td>style:</td>
      <td>Code formatting</td>
    </tr>
    <tr>
      <td>test:</td>
      <td>Adding or modifying tests</td>
    </tr>
    <tr>
      <td>ci:</td>
      <td>CI/CD changes</td>
    </tr>
    <tr>
      <td>revert:</td>
      <td>Reverting a commit</td>
    </tr>
    <tr>
      <td>BREAKING CHANGE:</td>
      <td>Major breaking changes</td>
    </tr>
  </tbody>
</table>

<p><br></p>
<details>

I remember being 11-12 years old, sitting at a restaurant with my brother while he was reciting different Andriod versions for me. Each candy-named version evoked a higher pitched laugh, and this remains a fond memory of mine. 

</details>
