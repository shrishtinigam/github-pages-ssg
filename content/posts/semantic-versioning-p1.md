---
Title: Get Semantic Versioning Right in Your Python Library - Part 1
Slug: semantic-versioning-p1
Date: Sep 10, 2025
Summary: Understanding versioning and release management of Python is crucial if you maintain Python libraries for a living, as I do. A thorough understanding helps you avoid dependency hell and ensures smooth upgrades during releases. To truly unde
Tags:
  - python
  - software versioning
  - pep standards
---

<p>Understanding versioning and release management of Python is crucial if you maintain Python libraries for a living, as I do. A thorough understanding helps you avoid dependency hell and ensures smooth upgrades during releases. To truly understand how versioning works in Python interpreters and Python libraries, we must begin at the beginning. The first stable version of Python was released in early 1991 (eleven years before I was born) and Python 2.0 was released in the middle of the dot-com crash. Meanwhile, in the wider world of software versioning, Semantic Versioning (SemVer) was introduced in 2009. Python itself didn’t see its latest standardization of versioning until the mid-2010s. In Part 1 of this three-part series, I’ll explore what software versioning is and how Python interpreters are versioned.</p>
<p>Let's unravel this timeline together.</p>
<h2 id="what-is-software-versioning">What is Software Versioning?</h2>
<p>Software versioning can be defined simply -</p>
<blockquote>
<p><a href="https://en.wikipedia.org/wiki/Software_versioning">Software versioning</a> is the process of assigning either unique version names or unique version numbers to unique states of computer software.</p>
</blockquote>
<p><br></p>
<blockquote>
<p>A <a href="https://dhtmlx.com/blog/versioning-schemes-importance-web-development/">versioning scheme</a> is a practice of categorizing changes in a software product during its lifecycle. To put it simply, these are unique identifiers containing numbers (or letters) given to different software iterations.</p>
</blockquote>
<p>There is a large variety of version numbering schemes, including but not limited to</p>
<ul>
<li>Semantic Versioning - <code>MAJOR.MINOR.PATCH</code> + strict standard rules</li>
<li>Calendar Versioning - <code>YY.MM</code> like Ubuntu or <code>YYYY.R</code> like Chrome</li>
<li>Marketing Versions - macOS - <code>Tahoe</code>, <code>Sequoia</code>, <code>Sonoma</code> etc, Android <code>Marshmallow</code>, <code>Nougat</code>, <code>Oreo</code></li>
<li>And most commonly, Hybrid Schemes, like <a href="https://openjdk.org/jeps/223">JEP:223 for Java</a>, <a href="https://peps.python.org/pep-0440/">PEP:440 for Python</a></li>
</ul>
<p>.. this list is by no means exhaustive. Some schemes are primarily for developers, some for end-users, and many software projects mix approaches.</p>
<h2 id="okay-so-how-does-python-interpreter-versioning-work">Okay, So How Does Python Interpreter Versioning Work?</h2>
<h3 id="pep-602">PEP 602</h3>
<p><a href="https://peps.python.org/pep-0602/">PEP 602</a> governs Python interpreter <strong>(CPython)</strong> releases starting with Python 3.9. It enforces a predictable annual release cycle, where a new feature version is released in October, once per year. </p>
<p>The development cycle is set to ~17 months per feature version, and each release has a lifecycle of <strong>five</strong> years. This includes <strong>two</strong> years of full support, with bug fixes and security updates, and <strong>three</strong> years of security fixes (source-only releases). This model of versioned and scheduled releases is called a 'software release train'.</p>
<blockquote>
<p>A <a href="https://en.wikipedia.org/wiki/Software_versioning#Release_train">software release train</a> is a form of software release schedule in which a number of distinct series of versioned software releases for multiple products are released as a number of different "trains" on a regular schedule. </p>
</blockquote>
<p>Generally, for each product line, a number of different release trains are running at a given time, with each train moving from initial release to eventual maturity and retirement on a planned schedule.</p>
<p>This standard simply: </p>
<ul>
<li>Makes releases smaller</li>
<li>Puts features and bug fixes in hands of users sooner</li>
<li>Creates a predictable calendar for releases</li>
</ul>
<p>The versioning works like -  </p>
<div style="text-align: center;">
  <b>[major].[minor].[micro][pre-release]</b>
</div>
<p><br></p>
<ol>
<li><strong>Major</strong> → Big changes, only happened from 1 → 2 → 3 (No official Python 4 release is planned as of now)</li>
<li><strong>Minor</strong> → Annual Feature Releases (since PEP 602)</li>
<li><strong>Micro</strong> → Patch/BugFixes, Maintenance releases, typically released ~2 months </li>
<li><strong>Pre-release</strong> → a (alpha), b (beta), rc (release candidate)</li>
</ol>
<p>Of course, dev releases also exist. In short, Python 3.x releases follow a predictable annual schedule, with clear rules for feature and bug fix releases, giving developers a predictable upgrade path. You can explore the incremental additions in recent Python releases.</p>
<h3 id="pep-387">PEP 387</h3>
<p>How backwards compatible are these 'stable' python interpreter releases? How much of my existing code could break with each new Python release, and how should I plan for it - especially since each release is supported for only 5 years? (a brief period of time in terms of enterprise software). Thankfully, PEP 387 defines how Python itself handles backward compatibility in its standard library.</p>
<blockquote>
<p>This <a href="https://peps.python.org/pep-0387/">PEP</a> takes the perspective that “backwards incompatibility” means preexisting code ceases to comparatively function after a change.</p>
</blockquote>
<p>The basic policy applies to all public APIs and dictates the following:</p>
<ol>
<li>No incompatible changes between consecutive releases unless:
    <ul>
        <li>Proper deprecation warnings are provided</li>
        <li>The change has high benefit relative to breakage</li>
    </ul></li>
<li>Deprecation periods typically last at least 2 years, often 5 years for practical purposes.</li>
<li>The Steering Council can grant exceptions for urgent security issues or obsolete features.</li>
</ol>
<p>Note that it does not govern backward compatibility rules for third-party libraries like pandas, numpy, etc.</p>
<p>An example of this deprecation is the <code>collections</code> import style. It was officially deprecated in Python 3.9 and removed later. Warnings are used to slowly warn developers of the changes. This includes <code>PendingDeprecationWarning</code> and <code>DeprecationWarning</code>.</p>
<pre class="codehilite"><code class="language-python"># Old way (deprecated)
from collections import Iterable
# Recommended new way
from collections.abc import Iterable
</code></pre>

<p>If you are planning to deprecate anything in your library, you can use the <code>deprecated</code> decorator from the warning library, as outlined by <a href="http://peps.python.org/pep-0702/">PEP 702</a>.</p>
<pre class="codehilite"><code class="language-python">from warnings import deprecated

@deprecated(&quot;Use Spam instead&quot;)
class Ham: ...
</code></pre>
